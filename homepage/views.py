from django.shortcuts import render
from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name = 'homepage.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        ctx['app_links'] = [
            {'name': 'Blog', 'url': 'blog:article-list'},
            {'name': 'Commissions', 'url': 'commissions:commission-list'},
            {'name': 'Merchstore', 'url': 'merchstore:product-list'},
            {'name': 'Wiki', 'url': 'wiki:article_list'},
        ]
        return ctx