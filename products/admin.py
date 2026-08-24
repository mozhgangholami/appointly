from django.contrib import admin
from .models import Category, Product, Comment
from django.utils.html import format_html


# ✅ نمایش محصولات مربوط به هر دسته داخل همان صفحه‌ی دسته‌بندی
class ProductInline(admin.TabularInline):
    model = Product
    # extra = 1  # چند فرم خالی برای افزودن محصول جدید


# ✅ مدیریت دسته‌ها در ادمین
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'image_category')   # نمایش در لیست
    prepopulated_fields = {'slug': ('name',)}  # خودکار پر شدن slug
    inlines = [ProductInline]   # نمایش محصولات مرتبط داخل هر دسته

    def show_image_category(self, obj):
        if obj.image_category:  # مطمئن شو فیلد در مدل همین اسم رو داره
            return format_html(
                '<img src="{}" width="80" height="80" style="object-fit:cover; border-radius:6px;" />',
                obj.image_category.url
            )
        return "بدون تصویر"

    show_image_category.short_description = "تصویر"


# ✅ مدیریت محصولات در ادمین
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'actual_price', 'created_at', 'image',)
    list_filter = ('category',)  # فیلتر سمت راست بر اساس دسته
    search_fields = ('title', 'category__title')  # جستجو

    def show_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 60px; height: 60px; border-radius: 8px;" />', obj.image.url)
        return "بدون تصویر"
    show_image.short_description = "پیش‌نمایش"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.order_by('-created_at') # فقط ۵ محصول اخیر رو نشون بده

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['title'] = 'آخرین محصولات'
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'body', 'stars', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at', 'product')
    search_fields = ('body', 'user__username', 'product__title')