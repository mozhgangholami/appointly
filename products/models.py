from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="دسته بندی")
    image_category = models.ImageField(upload_to='category/', blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True, allow_unicode=True)
    description = models.TextField(blank=True, null=True, verbose_name="توضیحات")

    class Meta:
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی ها"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    title = models.CharField(max_length=150, verbose_name="عنوان محصول")
    slug = models.SlugField(max_length=255, unique=True, allow_unicode=True)
    description = models.TextField(verbose_name="توضیحات")
    image = models.ImageField(upload_to='products', null=True, blank=True)
    actual_price = models.PositiveIntegerField(default='0')
    update_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('products:product_detail', kwargs={'pk': self.pk})


class Comment(models.Model):
    PRODUCT_STARS = [
        ('1', 'very bad'),
        ('2', 'bad'),
        ('3', 'normal'),
        ('4', 'good'),
        ('5', 'perfect'),
    ]
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments', verbose_name="محصول")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments', verbose_name="کاربر" )
    body = models.TextField()
    stars = models.CharField(max_length=1, choices=PRODUCT_STARS, default=3)
    created_at = models.DateTimeField(default=timezone.now, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="آخرین بروزرسانی")
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "کامنت"

    def __str__(self):
            return f"کامنت توسط {self.user} برای محصول{self.product}"