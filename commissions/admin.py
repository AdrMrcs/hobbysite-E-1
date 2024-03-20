from django.contrib import admin

from .models import Commission, Comment

class CommentInline(admin.TabularInline):
    model = Comment

class CommissionAdmin(admin.ModelAdmin):
    model = Commission
    inlines = [CommentInline,]

class CommentAdmin(admin.ModelAdmin):
    model = Comment

admin.site.register(Comment, CommentAdmin)
admin.site.register(Commission, CommissionAdmin)