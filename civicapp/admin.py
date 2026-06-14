from django.contrib import admin
from .models import *


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'category',
        'county',
        'sub_county',
        'ward',
        'status',
        'created_by',
        'created_at'
    )

    list_filter = (
        'status',
        'category',
        'county'
    )

    search_fields = (
        'title',
        'description',
        'county',
        'sub_county',
        'ward',
        'created_by__username'
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'role'
    )

    list_filter = (
        'role',
    )

    search_fields = (
        'user__username',
    )


@admin.register(IssueLog)
class IssueLogAdmin(admin.ModelAdmin):

    list_display = (
        'issue',
        'message',
        'created_at'
    )

    search_fields = (
        'issue__title',
        'message'
    )


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'issue',
        'created_at'
    )

    search_fields = (
        'user__username',
        'issue__title'
    )