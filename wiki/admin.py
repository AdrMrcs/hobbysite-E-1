from django.contrib import admin

from .models import Articles, ArticleCategory

class Inline(admin.TabularInline):
    model = Articles

class ArticleCategoryAdmin(admin.ModelAdmin):
    model = ArticleCategory
    inlines = [Inline,]

class ArticlesAdmin(admin.ModelAdmin):
    model = Articles

admin.site.register(Articles, ArticlesAdmin)
admin.site.register(ArticleCategory, ArticleCategoryAdmin)