from django.urls import path
from . import views
from .views import PageListView, PageDetailView


urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('aboutus/', views.AboutUsPagesView.as_view(), name='aboutus'),
    path('', PageListView.as_view(), name="page_list"),
    path('<int:pk>/', PageDetailView.as_view(), name="page_detail"),
]
