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
from .forms import IssueForm, ProfileImageForm

import logging

logger = logging.getLogger(__name__)

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

        # REQUIRED FIELDS CHECK
        if not username or not password:
            messages.error(
                request,
                "Username and password are required."
            )
            return redirect('register')

        # USERNAME ALREADY EXISTS
        if User.objects.filter(username=username).exists():
            messages.error(
                request,
                "Username already exists. Please choose another."
            )
            return redirect('register')

        # EMAIL ALREADY EXISTS
        if email and User.objects.filter(email=email).exists():
            messages.error(
                request,
                "This email address is already registered."
            )
            return redirect('register')

      
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
        if (
            officer_key and
            officer_key.strip() == settings.OFFICER_REGISTRATION_KEY
        ):
            profile.role = 'officer'

        profile.save()

        # SUCCESS MESSAGE
        messages.success(
            request,
            "Account created successfully. Please login."
        )

        return redirect('login')

    return render(
        request,
        'civicapp/register.html'
    )

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

            try:
                profile = user.profile
                role = profile.role

                messages.success(request, f"Welcome back {user.username}!")

                # FIRST TIME LOGIN
                if hasattr(profile, "is_new_user") and profile.is_new_user:
                    profile.is_new_user = False
                    profile.save()
                    return redirect('home')

                # RETURNING USER
                if role == 'officer':
                    return redirect('officer_dashboard')
                else:
                    return redirect('dashboard')

            except Exception:
                messages.error(request, "Profile error occurred.")
                return redirect('dashboard')

        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')

    return render(request, "civicapp/login.html")
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

    total_issues = Issue.objects.filter(
        created_by=user
    ).count()

    pending_issues = Issue.objects.filter(
        created_by=user,
        status='pending'
    ).count()

    in_progress = Issue.objects.filter(
        created_by=user,
        status='in_progress'
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
        'in_progress': in_progress,
        'resolved_issues': resolved_issues,
        'my_issues': my_issues,
    }

    return render(
        request,
        'civicapp/dashboard.html',
        context
    )

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

            # =========================
            # DUPLICATE CHECK (NEW)
            # =========================

            duplicate_issue = Issue.objects.filter(
                title__icontains=issue.title,
                category=issue.category,
                county=issue.county,
                sub_county=issue.sub_county,
                ward=issue.ward,
            ).exclude(created_by=request.user).first()

            if duplicate_issue:
                messages.error(
                    request,
                    "This issue already exists. You can only support the existing report."
                )
                return redirect('issue_detail', id=duplicate_issue.id)

            # SAVE NEW ISSUE ONLY IF NO DUPLICATE
            issue.save()

            logger.info(
                f"{request.user.username} created issue {issue.title}"
            )

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

    return render(request, 'civicapp/my_reports.html', {'issues': issues})


# =========================
# PROFILE
# =========================
@login_required
def profile(request):

    profile = request.user.profile

    total_issues = Issue.objects.filter(created_by=request.user).count()

    pending_issues = Issue.objects.filter(
        created_by=request.user,
        status='pending'
    ).count()

    in_progress_issues = Issue.objects.filter(
        created_by=request.user,
        status='in_progress'
    ).count()

    resolved_issues = Issue.objects.filter(
        created_by=request.user,
        status='resolved'
    ).count()

    if request.method == "POST":
        form = ProfileImageForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if form.is_valid():
            form.save()
            messages.success(request, "Profile photo updated successfully.")
            return redirect('profile')

    else:
        form = ProfileImageForm(instance=profile)

    context = {
        'form': form,
        'total_issues': total_issues,
        'pending_issues': pending_issues,
        'in_progress_issues': in_progress_issues,
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
    top_issues = Issue.objects.annotate(
    vote_count=Count('votes')
    ).order_by('-vote_count')[:5]

    context['top_issues'] = top_issues

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

# =========================
# EDIT ISSUE
# =========================

@login_required
def edit_issue(request, issue_id):

    issue = get_object_or_404(
        Issue,
        id=issue_id,
        created_by=request.user
    )

    # optional safety rule: block editing resolved issues
    if issue.status == "resolved":
        messages.error(request, "Resolved issues cannot be edited.")
        return redirect('my_reports')

    if request.method == "POST":
        form = IssueForm(request.POST, request.FILES, instance=issue)

        if form.is_valid():
            form.save()
            messages.success(request, "Issue updated successfully.")
            return redirect('my_reports')
        else:
            messages.error(request, "Please correct the errors.")

    else:
        form = IssueForm(instance=issue)

    return render(request, 'civicapp/edit_issue.html', {
        'form': form,
        'issue': issue
    })

# =========================
# DELETE ISSUE
# =========================

@login_required
def delete_issue(request, issue_id):

    issue = get_object_or_404(
        Issue,
        id=issue_id,
        created_by=request.user
    )

    # optional safety rule (recommended)
    if issue.status == "resolved":
        messages.error(request, "Resolved issues cannot be deleted.")
        return redirect('my_reports')

    if request.method == "POST":
        issue.delete()
        messages.success(request, "Issue deleted successfully.")
        return redirect('my_reports')

    return render(request, 'civicapp/delete_issue.html', {
        'issue': issue
    })