from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('report/', views.report_issue, name='report_issue'),
    path('issues/', views.public_issues, name='public_issues'),
    path('issues/<int:id>/', views.issue_detail, name='issue_detail'),
    path('my-reports/', views.my_reports, name='my_reports'),
    path('profile/', views.profile, name='profile'),
    path('issues/<int:id>/update/', views.update_status, name='update_status'),
    path('officer/dashboard/', views.officer_dashboard, name='officer_dashboard'),
    path('issues/<int:id>/support/', views.support_issue, name='support_issue'),
    path('issue/edit/<int:issue_id>/', views.edit_issue, name='edit_issue'),
    path('issue/delete/<int:issue_id>/', views.delete_issue, name='delete_issue'),

]