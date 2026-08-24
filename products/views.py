from django.shortcuts import render, get_object_or_404
from .forms import CommentForm
from .models import Product, Category, Comment
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DetailView, DeleteView


class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    paginate_by = 6  # برای صفحه‌بندی (اختیاری)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class CategoryProductListView(ListView):
    model = Product
    template_name = 'products/category_product.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        self.category = get_object_or_404(Category, pk=self.kwargs['pk'])
        return Product.objects.filter(category=self.category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(Category, pk=self.kwargs['pk'])
        context['categories'] = Category.objects.all()
        context['category'] = self.category
        return context


class ProductDetailView(DetailView):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        comments = product.comments.all()
        form = CommentForm()
        return render(request, "products/product_detail.html", {
            "product": product,
            "comments": comments,
            "form": form,
        })

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            print(comment.body)
            comment.user = request.user
            comment.product = product
            comment.save()
            return redirect("products:product_detail", pk=product.pk)

        # ❗ مهم: اگر فرم معتبر نبود، حتما باید render برگردونه، نه None
        comments = product.comments.all()
        return render(request, "products/product_detail.html", {
            "product": product,
            "comments": comments,
            "form": form,
        })


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    fields = ['body', 'stars']
    template_name = 'products/comment_form.html'
    pk_url_kwarg = 'comment_pk'

    def get_success_url(self):
        return reverse_lazy('products:product_detail', kwargs={'pk': self.object.product.pk})

    def test_func(self):
        # فقط کسی که نویسنده کامنته بتونه ویرایش کنه
        comment = self.get_object()
        return comment.user == self.request.user


# ✅ حذف کامنت
class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'products/comment_confirm_delete.html'
    pk_url_kwarg = 'comment_pk'

    def get_success_url(self):
        return reverse_lazy('products:product_detail', kwargs={'pk': self.object.product.pk})

    def test_func(self):
        comment = self.get_object()
        return comment.user == self.request.user


