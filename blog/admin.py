from django.contrib import admin

from .models import Article, ArticleCategory, Comment, ArticleGallery


class Inline(admin.TabularInline):
    model = Article

class CommentInLine(admin.TabularInline):
    model = Comment

class ArticleCategoryAdmin(admin.ModelAdmin):
    model = ArticleCategory
    inlines = [Inline,]

class ArticleAdmin(admin.ModelAdmin):
    model = Article

class ArticleGalleryAdmin(admin.ModelAdmin):
    model = ArticleGallery

admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleCategory, ArticleCategoryAdmin)
admin.site.register(ArticleGallery, ArticleGalleryAdmin)