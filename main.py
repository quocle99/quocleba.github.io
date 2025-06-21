from flask import Flask, request
import datetime

app = Flask(__name__)

@app.route('/')
def index():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    ua = request.headers.get('User-Agent')
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log = f"{now} - IP: {ip} - Agent: {ua}\n"
    with open("ip_log.txt", "a") as f:
        f.write(log)
    return "<h2>Giao dịch đang được xử lý...</h2>"

@app.route('/log')
def view_log():
    try:
        with open("ip_log.txt", "r") as f:
            return f"<pre>{f.read()}</pre>"
    except:
        return "Chưa có dữ liệu truy cập"
