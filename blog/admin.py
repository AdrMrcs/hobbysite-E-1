from django.contrib import admin

from .models import Article, ArticleCategory

class Inline(admin.TabularInline):
    model = Article

class ArticleCategoryAdmin(admin.ModelAdmin):
    model = ArticleCategory
    inlines = [Inline,]

class ArticleAdmin(admin.ModelAdmin):
    model = Article

admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleCategory, ArticleCategoryAdmin)