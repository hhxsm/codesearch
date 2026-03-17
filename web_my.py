import http.server, socketserver, os
PORT = 8088
os.chdir(os.path.dirname(os.path.abspath(__file__)))
Handler = http.server.SimpleHTTPRequestHandler
with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
    print("✅ 网页地址：http://127.0.0.1:8088")
    httpd.serve_forever()