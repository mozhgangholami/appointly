from django.urls import path
from .views import ProductListView, ProductDetailView, CategoryProductListView
from .views import CommentUpdateView, CommentDeleteView

app_name = 'products'

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('category/<int:pk>/', CategoryProductListView.as_view(), name='category_products'),
    path('comment/<int:product_pk>/comment/<int:comment_pk>/edit/', CommentUpdateView.as_view(), name='comment_edit'),
    path('comment/<int:product_pk>/comment/<int:comment_pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'),

]
