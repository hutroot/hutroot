#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
简单的 HTTP 服务脚本，用于测试 Jenkins 部署
访问 http://服务器IP:8080 即可看到效果
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import datetime
import os
import sys
import json

class TestHandler(BaseHTTPRequestHandler):
    """处理 HTTP 请求"""
    
    def __init__(self, *args, **kwargs):
        # 读取部署时间信息
        self.deployment_time = self._get_deployment_time()
        super().__init__(*args, **kwargs)
    
    def _get_deployment_time(self):
        """获取部署时间，如果不存在则创建"""
        deployment_file = 'deployment_info.json'
        
        if os.path.exists(deployment_file):
            try:
                with open(deployment_file, 'r') as f:
                    data = json.load(f)
                    return data.get('deployment_time', '未知')
            except:
                pass
        
        # 如果文件不存在或读取失败，创建新的部署时间
        deployment_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            with open(deployment_file, 'w') as f:
                json.dump({'deployment_time': deployment_time}, f)
        except:
            pass
            
        return deployment_time
    
    def do_GET(self):
        """处理 GET 请求"""
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            
            # 获取部署信息
            hostname = os.uname().nodename if hasattr(os, 'uname') else 'Unknown'
            pid = os.getpid()
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # 获取 Git 版本信息（如果存在）
            git_commit = "第4次测试"
            git_branch = "123456"
            try:
                with open('.git/HEAD', 'r') as f:
                    head_content = f.read().strip()
                    if 'ref:' in head_content:
                        git_branch = head_content.split('/')[-1]
                with open('.git/refs/heads/' + git_branch, 'r') as f:
                    git_commit = f.read().strip()[:7]
            except:
                pass
            
            # HTML 响应内容
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <title>Jenkins 部署测试</title>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        margin: 50px;
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        color: white;
                    }}
                    .container {{
                        max-width: 800px;
                        margin: 0 auto;
                        background: rgba(255,255,255,0.1);
                        border-radius: 10px;
                        padding: 30px;
                        backdrop-filter: blur(10px);
                    }}
                    h1 {{ color: #ffd700; }}
                    .info {{
                        background: rgba(0,0,0,0.3);
                        padding: 15px;
                        border-radius: 5px;
                        margin: 10px 0;
                    }}
                    .success {{ color: #90ee90; }}
                    .time {{ font-size: 14px; margin-top: 20px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>✅ Jenkins 部署成功！</h1>
                    <div class="info">
                        <p><strong>部署时间：</strong> {self.deployment_time}</p>
                        <p><strong>服务器主机名：</strong> {hostname}</p>
                        <p><strong>进程 PID：</strong> {pid}</p>
                        <p><strong>当前时间：</strong> {current_time}</p>
                        <p><strong>Git 分支：</strong> {git_branch}</p>
                        <p><strong>Git Commit：</strong> {git_commit}</p>
                        <p><strong>Python 版本：</strong> {sys.version.split()[0]}</p>
                    </div>
                    <p class="success">🎉 代码拉取并部署成功！</p>
                    <p class="time">这是由 Jenkins 自动部署的测试服务</p>
                </div>
            </body>
            </html>
            """
            self.wfile.write(html_content.encode())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404 Not Found")
    
    def log_message(self, format, *args):
        """自定义日志输出"""
        print(f"[{datetime.datetime.now()}] {args[0]}")

def run_server(port=8080):
    """启动服务器"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, TestHandler)
    print(f"🚀 服务器启动成功！")
    print(f"📍 访问地址: http://localhost:{port}")
    print(f"📍 或使用服务器IP: http://<服务器IP>:{port}")
    print(f"⏹️  按 Ctrl+C 停止服务\n")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print(f"\n\n👋 服务已停止")
        httpd.server_close()

if __name__ == '__main__':
    # 可以通过命令行参数指定端口
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    run_server(port)