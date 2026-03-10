import http.server
import webbrowser
import threading
import base64
import io
import json
import qrcode
from PIL import ImageDraw

HTML = """
<!DOCTYPE html>
<html>
<head>
  <title>QR Generator</title>
  <style>
    body { font-family: Helvetica, sans-serif; background: #1e1e2e; color: #fff; display: flex; flex-direction: column; align-items: center; padding: 40px; }
    h1 { color: #a78bff; margin-bottom: 30px; }
    .section { width: 400px; margin-bottom: 20px; }
    label { display: block; margin-bottom: 6px; font-size: 14px; color: #ccc; }
    input[type=text] { width: 100%; padding: 10px; border-radius: 8px; border: none; font-size: 14px; background: #2e2e3e; color: #fff; box-sizing: border-box; }
    .colors { display: flex; gap: 20px; justify-content: center; margin-bottom: 20px; }
    .color-box { display: flex; flex-direction: column; align-items: center; gap: 6px; font-size: 13px; color: #aaa; }
    input[type=color] { width: 60px; height: 44px; border: none; border-radius: 8px; cursor: pointer; background: none; }
    button { background: #7c6bff; color: white; border: none; padding: 12px 36px; border-radius: 10px; font-size: 15px; font-weight: bold; cursor: pointer; margin-top: 10px; }
    button:hover { background: #6a5acd; }
    #preview { margin-top: 24px; }
    #preview img { border-radius: 10px; box-shadow: 0 0 20px rgba(124,107,255,0.4); }
    #save-btn { display: none; background: #4caf82; margin-top: 14px; }
    #save-btn:hover { background: #3d9e6e; }
  </style>
</head>
<body>
  <h1>QR Generator</h1>

  <div class="section">
    <label>Enter URL:</label>
    <input type="text" id="url" placeholder="https://example.com" />
  </div>

  <div class="colors">
    <div class="color-box"><span>Dots</span><input type="color" id="dot" value="#000000"></div>
    <div class="color-box"><span>Background</span><input type="color" id="bg" value="#ffffff"></div>
    <div class="color-box"><span>Eye Frame</span><input type="color" id="eye_out" value="#7c6bff"></div>
    <div class="color-box"><span>Eye Center</span><input type="color" id="eye_in" value="#c26bff"></div>
  </div>

  <button onclick="generate()">Generate QR</button>

  <div id="preview"></div>
  <a id="save-btn-link" href="#"><button id="save-btn">Save PNG</button></a>

  <script>
    async function generate() {
      const data = {
        url: document.getElementById("url").value,
        dot: document.getElementById("dot").value,
        bg: document.getElementById("bg").value,
        eye_out: document.getElementById("eye_out").value,
        eye_in: document.getElementById("eye_in").value,
      };
      const res = await fetch("/generate", { method: "POST", body: JSON.stringify(data) });
      const json = await res.json();
      const img = document.createElement("img");
      img.src = "data:image/png;base64," + json.img;
      img.width = 260;
      document.getElementById("preview").innerHTML = "";
      document.getElementById("preview").appendChild(img);
      document.getElementById("save-btn").style.display = "block";
      document.getElementById("save-btn-link").href = img.src;
      document.getElementById("save-btn-link").download = "qr_code.png";
    }
  </script>
</body>
</html>
"""

class Handler(http.server.BaseHTTPRequestHandler):
    def log_message(self, *args): pass  # silence logs

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(HTML.encode())

    def do_POST(self):
        data = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        url     = data["url"]
        dot     = data["dot"]
        bg      = data["bg"]
        eye_out = data["eye_out"]
        eye_in  = data["eye_in"]

        qr = qrcode.QRCode(version=3, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=4)
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color=dot, back_color=bg).convert("RGBA")

        draw = ImageDraw.Draw(img)
        m, b, n = 10, 40, qr.modules_count
        for ex, ey in [(b,b), (b+(n-7)*m, b), (b, b+(n-7)*m)]:
            draw.rectangle([ex,     ey,     ex+7*m, ey+7*m], fill=eye_out)
            draw.rectangle([ex+m,   ey+m,   ex+6*m, ey+6*m], fill=bg)
            draw.rectangle([ex+2*m, ey+2*m, ex+5*m, ey+5*m], fill=eye_in)

        buf = io.BytesIO()
        img.save(buf, format="PNG")
        encoded = base64.b64encode(buf.getvalue()).decode()

        result = json.dumps({"img": encoded}).encode()
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(result)

PORT = 5555
server = http.server.HTTPServer(("localhost", PORT), Handler)
print(f"Opening QR Generator at http://localhost:{PORT}")
webbrowser.open(f"http://localhost:{PORT}")
server.serve_forever()