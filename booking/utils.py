import os
from kavenegar import KavenegarAPI, APIException, HTTPException
from django.conf import settings


def send_sms(to, message):
    """
    تابع اصلی برای ارسال پیامک با استفاده از API کاوه‌نگار
    """
    api_key = os.getenv('KAVENEGAR_API_KEY') or getattr(settings, 'KAVENEGAR_API_KEY', None)

    if not api_key:
        print("❌ خطا: KAVENEGAR_API_KEY تنظیم نشده است.")
        return None

    try:
        api = KavenegarAPI(api_key)
        params = {
            'sender': '2000660110',  # در صورت داشتن شماره اختصاصی بنویس
            'receptor': to,
            'message': message,
        }
        response = api.sms_send(params)
        print("✅ پیامک ارسال شد:", response)
        return response

    except APIException as e:
        print(f"⚠️ خطای API کاوه‌نگار: {e}")
    except HTTPException as e:
        print(f"⚠️ خطای HTTP هنگام ارسال پیامک: {e}")
    except Exception as e:
        print(f"⚠️ خطای غیرمنتظره در ارسال پیامک: {e}")

    return None


def send_sms_notification(phone_number, message):
    """
    تابع کمکی برای ارسال پیام‌های سیستمی (مثلاً تأیید نوبت، یادآوری و ...)
    """
    if not phone_number:
        print("⚠️ شماره تلفن وارد نشده است، پیامک ارسال نشد.")
        return None

    print(f"📨 در حال ارسال پیام به {phone_number} ...")
    return send_sms(phone_number, message)
