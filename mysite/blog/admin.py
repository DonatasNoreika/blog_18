from django.contrib import admin
from .models import Post, Comment, CustomUser
from django.contrib.auth.admin import UserAdmin

# Register your models here.

class CommentInLine(admin.TabularInline):
    model = Comment
    extra = 0

class PostAdmin(admin.ModelAdmin):
    list_display = ['date', 'title', 'author']
    inlines = [CommentInLine]
    list_filter = ['date', 'author']
    search_fields = ['title', 'content']
    list_editable = ['title', 'author']
    readonly_fields = ['date', 'comments_count']

    fieldsets = [
        ("General", {"fields": ('title', 'content', 'author', 'photo')}),
        ("Info", {"fields": ('date', 'comments_count')})
    ]


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
    ("Additional Info", {"fields": ['photo']}),
    )

admin.site.register(Post, PostAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
