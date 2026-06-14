from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.conf import settings
from django.core.paginator import Paginator

from .models import *
from .forms import IssueForm


# =========================
# REGISTER VIEW
# =========================
def register_view(request):

    if request.method == 'POST':

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')

        username = request.POST.get('username')
        password = request.POST.get('password')
        officer_key = request.POST.get('officer_key')

        # ---- ADDED VALIDATION MESSAGES (NO LOGIC CHANGE) ----
        if not username or not password:
            messages.error(request, "Username and password are required.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')

        if email and User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return redirect('register')

        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters.")
            return redirect('register')

        # CREATE USER
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name
        )

        # PROFILE SETUP
        profile = user.profile
        profile.role = 'citizen'

        # OFFICER PROMOTION
        if officer_key and officer_key.strip() == settings.OFFICER_REGISTRATION_KEY:
            profile.role = 'officer'

        profile.save()

        # ---- SUCCESS MESSAGE ADDED ----
        messages.success(request, "Account created successfully. Please login.")

        return redirect('login')

    return render(request, 'civicapp/register.html')


# =========================
# LOGIN VIEW
# =========================
def login_view(request):

    if request.method == "POST":

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # ROLE-BASED REDIRECT (UNCHANGED)
            try:
                role = user.profile.role
            except:
                role = 'citizen'

            messages.success(request, f"Welcome back {user.username}!")

            if role == 'officer':
                return redirect('officer_dashboard')
            else:
                return redirect('dashboard')

        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')

    return render(request, 'civicapp/login.html')


# =========================
# LOGOUT VIEW
# =========================
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')


# =========================
# DASHBOARD
# =========================
@login_required
def dashboard(request):

    user = request.user

    total_issues = Issue.objects.filter(created_by=user).count()

    pending_issues = Issue.objects.filter(
        created_by=user,
        status='pending'
    ).count()

    resolved_issues = Issue.objects.filter(
        created_by=user,
        status='resolved'
    ).count()

    my_issues = Issue.objects.filter(
        created_by=user
    ).order_by('-created_at')

    context = {
        'total_issues': total_issues,
        'pending_issues': pending_issues,
        'resolved_issues': resolved_issues,
        'my_issues': my_issues,
    }

    return render(request, 'civicapp/dashboard.html', context)


# =========================
# HOME
# =========================
def home(request):
    return render(request, 'civicapp/home.html')


# =========================
# REPORT ISSUE
# =========================
@login_required
def report_issue(request):

    if request.method == "POST":
        form = IssueForm(request.POST, request.FILES)

        if form.is_valid():
            issue = form.save(commit=False)
            issue.created_by = request.user
            issue.save()

            messages.success(request, "Issue reported successfully.")
            return redirect('public_issues')

        else:
            messages.error(request, "Please correct the form errors.")

    else:
        form = IssueForm()

    return render(request, 'civicapp/report_issue.html', {'form': form})


# =========================
# PUBLIC ISSUES
# =========================
def public_issues(request):

    issues_list = Issue.objects.annotate(
        vote_count=Count('votes')
    ).order_by('-vote_count', '-created_at')

    paginator = Paginator(issues_list, 10)  # 10 per page
    page_number = request.GET.get('page')
    issues = paginator.get_page(page_number)

    return render(request, 'civicapp/public_issues.html', {
        'issues': issues
    })


# =========================
# ISSUE DETAIL
# =========================
def issue_detail(request, id):

    issue = get_object_or_404(Issue, id=id)

    return render(
        request,
        'civicapp/issue_detail.html',
        {'issue': issue}
    )


# =========================
# MY REPORTS
# =========================
@login_required
def my_reports(request):

    issues = Issue.objects.filter(
        created_by=request.user
    ).order_by('-created_at')

    return render(
        request,
        'civicapp/my_reports.html',
        {'issues': issues}
    )


# =========================
# PROFILE
# =========================
@login_required
def profile_view(request):

    user = request.user

    total_issues = Issue.objects.filter(created_by=user).count()

    pending_issues = Issue.objects.filter(
        created_by=user,
        status='pending'
    ).count()

    resolved_issues = Issue.objects.filter(
        created_by=user,
        status='resolved'
    ).count()

    context = {
        'user': user,
        'total_issues': total_issues,
        'pending_issues': pending_issues,
        'resolved_issues': resolved_issues,
    }

    return render(request, 'civicapp/profile.html', context)


# =========================
# UPDATE STATUS
# =========================
@login_required
def update_status(request, id):

    if request.user.profile.role != 'officer':
        messages.error(request, "Only officers can update issue status.")
        return redirect('issue_detail', id=id)

    issue = get_object_or_404(Issue, id=id)

    old_status = issue.status

    if issue.status == 'pending':
        issue.status = 'in_progress'
        message = "Status changed from Pending → In Progress"

    elif issue.status == 'in_progress':
        issue.status = 'resolved'
        message = "Status changed from In Progress → Resolved"
    else:
        message = "No status change"

    issue.save()

    IssueLog.objects.create(
        issue=issue,
        message=message
    )

    messages.success(request, "Issue status updated successfully.")
    return redirect('issue_detail', id=id)


# =========================
# OFFICER REQUIRED DECORATOR
# =========================
def officer_required(view_func):

    def wrapper(request, *args, **kwargs):

        if request.user.profile.role != 'officer':
            messages.error(request, "Access denied. Officers only.")
            return redirect('dashboard')

        return view_func(request, *args, **kwargs)

    return wrapper


# =========================
# OFFICER DASHBOARD
# =========================
@login_required
@officer_required
def officer_dashboard(request):

    issues = Issue.objects.all().order_by('-created_at')

    pending = Issue.objects.filter(status='pending')
    in_progress = Issue.objects.filter(status='in_progress')
    resolved = Issue.objects.filter(status='resolved')

    context = {
        'issues': issues,
        'pending': pending.count(),
        'in_progress': in_progress.count(),
        'resolved': resolved.count(),
    }

    return render(request, 'civicapp/officer_dashboard.html', context)


# =========================
# SUPPORT ISSUE
# =========================
@login_required
def support_issue(request, id):

    issue = get_object_or_404(Issue, id=id)

    vote, created = Vote.objects.get_or_create(
        user=request.user,
        issue=issue
    )

    if created:
        messages.success(request, "Thank you for supporting this issue.")
    else:
        messages.warning(request, "You already support this issue.")

    return redirect('issue_detail', id=id)