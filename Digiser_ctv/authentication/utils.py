import socket

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        # HTTP_X_FORWARDED_FOR có thể chứa nhiều địa chỉ IP,
        # địa chỉ IP thực của client là địa chỉ đầu tiên trong chuỗi.
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        # Nếu không có proxy, dùng REMOTE_ADDR
        ip = request.META.get('REMOTE_ADDR', '').strip()
        
        
    # Kiểm tra nếu IP là localhost (127.0.0.1 hoặc ::1), thay thế bằng IP thực của client nếu cần
    if ip.startswith('127.') or ip.startswith('::'):
        ip = get_local_ip()
    return ip


def get_local_ip():
    # Lấy địa chỉ IP mạng nội bộ của máy.
    try:
        # Lấy địa chỉ IP của máy trên mạng nội bộ
        local_ip = socket.gethostbyname(socket.gethostname())
        return local_ip
    except socket.error as e:
        # Nếu có lỗi khi lấy IP, trả về IP localhost
        return '127.0.0.1'