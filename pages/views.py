from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from .models import PageItem
from products.models import Product, Category


class HomePageView(ListView):
    model = PageItem
    template_name = "home.html"
    context_object_name = "pages"
    paginate_by = 6  # تعداد آیتم در هر صفحه
    queryset = PageItem.objects.all().order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_pages'] = PageItem.objects.all().order_by('-created_at')[:3]
        sample_products = []
        categories = Category.objects.all()
        for cat in categories:
            product = Product.objects.filter(category=cat).first()
            if product:
                sample_products.append(product)
        context['sample_products'] = sample_products
        return context


class AboutUsPagesView(TemplateView):
    template_name = 'pages/aboutus.html'


class PageListView(ListView):
    model = PageItem
    template_name = "pages/page_list.html"
    context_object_name = "pages"
    paginate_by = 6  # نمایش ۶ آیتم در هر صفحه


class PageDetailView(DetailView):
    model = PageItem
    template_name = "pages/page_detail.html"
    context_object_name = "page"
