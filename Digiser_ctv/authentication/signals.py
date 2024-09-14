from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from .models import LoginLog
from .utils import get_client_ip

# Khi người dùng đăng nhập
@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    # Lấy địa chỉ IP từ request
    ip = get_client_ip(request)
    
    # Tạo một bản ghi lịch sử đăng nhập
    LoginLog.objects.create(user=user, ip_address=ip)

# # Khi người dùng đăng xuất
# @receiver(user_logged_out)
# def log_user_logout(sender, request, user, **kwargs):
#     # Cập nhật thời gian đăng xuất cho người dùng
#     login_history = LoginHistory.objects.filter(user=user, logout_time__isnull=True).last()
#     if login_history:
#         login_history.logout_time = timezone.now()
#         login_history.save()
