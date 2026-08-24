from django.db import models
from django.urls import reverse


class PageItem(models.Model):
    """مدل برای نمایش نمونه‌کار یا خدمات"""
    title = models.CharField(max_length=150, verbose_name="عنوان")
    # image = models.ImageField(upload_to="pages/", blank=True, null=True, verbose_name="تصویر")
    short_description = models.CharField(max_length=255, verbose_name="توضیح کوتاه")
    content = models.TextField(verbose_name="توضیح کامل")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="آخرین ویرایش")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "مطلب"
        verbose_name_plural = "مطالب"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("pages:page_detail", args=[str(self.id)])

