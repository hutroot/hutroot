#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
简单的 HTTP 服务脚本，用于测试 Jenkins 部署
默认端口: 80 (可通过命令行参数指定其他端口)
Jenkins部署端口: 8080
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
    
    def _generate_css(self):
        """生成CSS样式"""
        return """
        * {
          margin: 0;
          padding: 0;
          box-sizing: border-box;
        }

        body {
          background: radial-gradient(ellipse at 30% 20%, #0a101f, #02050b);
          font-family: 'Inter', sans-serif;
          min-height: 100vh;
          display: flex;
          align-items: center;
          justify-content: center;
          padding: 2rem;
          position: relative;
          overflow-x: auto;
        }

        /* 动态科技网格背景 */
        body::before {
          content: "";
          position: fixed;
          width: 200%;
          height: 200%;
          top: -50%;
          left: -50%;
          background-image: 
            linear-gradient(rgba(0, 212, 255, 0.05) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 212, 255, 0.05) 1px, transparent 1px);
          background-size: 45px 45px;
          pointer-events: none;
          z-index: 0;
          animation: gridMove 50s linear infinite;
        }

        @keyframes gridMove {
          0% { transform: translate(0, 0); }
          100% { transform: translate(40px, 40px); }
        }

        /* 主容器 */
        .dashboard {
          position: relative;
          z-index: 10;
          max-width: 1400px;
          width: 100%;
          margin: 0 auto;
        }

        /* 头部区域增强 */
        .hero {
          text-align: center;
          margin-bottom: 2.8rem;
        }

        .hero-icon {
          font-size: 3.2rem;
          background: linear-gradient(145deg, #00e0ff, #2b6ef0);
          -webkit-background-clip: text;
          background-clip: text;
          color: transparent;
          display: inline-block;
          margin-bottom: 0.5rem;
          filter: drop-shadow(0 0 10px rgba(0, 182, 232, 0.5));
        }

        .hero h1 {
          font-size: 2.9rem;
          font-weight: 800;
          background: linear-gradient(135deg, #FFFFFF 0%, #a0dcff 80%);
          background-clip: text;
          -webkit-background-clip: text;
          color: transparent;
          letter-spacing: -0.5px;
        }

        .hero p {
          color: #8eb8e0;
          margin-top: 0.6rem;
          font-weight: 500;
          font-size: 1rem;
          border-bottom: 1px dashed rgba(0, 212, 255, 0.4);
          display: inline-block;
          padding-bottom: 0.4rem;
        }

        /* 服务卡片网格 */
        .service-grid {
          display: flex;
          flex-wrap: wrap;
          justify-content: center;
          gap: 1.8rem;
          margin: 2rem 0 2rem;
        }

        .service-card {
          background: rgba(10, 22, 36, 0.7);
          backdrop-filter: blur(14px);
          border-radius: 2rem;
          padding: 1.8rem 1.4rem 2rem;
          width: 280px;
          transition: all 0.35s cubic-bezier(0.2, 0.9, 0.4, 1.1);
          border: 1px solid rgba(0, 200, 230, 0.3);
          box-shadow: 0 20px 32px -12px rgba(0, 0, 0, 0.5);
          text-align: center;
          position: relative;
          overflow: hidden;
        }

        .service-card::before {
          content: '';
          position: absolute;
          top: 0;
          left: 0;
          width: 100%;
          height: 100%;
          background: radial-gradient(circle at top right, rgba(0, 212, 255, 0.08), transparent 70%);
          pointer-events: none;
        }

        .service-card:hover {
          transform: translateY(-8px) scale(1.02);
          border-color: rgba(0, 230, 255, 0.6);
          box-shadow: 0 30px 50px -15px rgba(0, 0, 0, 0.6);
        }

        .card-icon {
          font-size: 2.5rem;
          margin-bottom: 1rem;
          background: linear-gradient(145deg, #00e0ff, #2b6ef0);
          -webkit-background-clip: text;
          background-clip: text;
          color: transparent;
          display: inline-block;
        }

        .service-card h2 {
          font-size: 1.4rem;
          font-weight: 700;
          color: #ffffff;
          margin-bottom: 0.8rem;
        }

        .service-desc {
          color: #a8c7e8;
          font-size: 0.9rem;
          line-height: 1.5;
          margin-bottom: 1.2rem;
          min-height: 4rem;
        }

        .port-badge {
          background: rgba(0, 30, 60, 0.6);
          color: #2dd4ff;
          padding: 0.5rem 1rem;
          border-radius: 40px;
          font-size: 0.85rem;
          font-weight: 500;
          margin-bottom: 1.5rem;
          display: inline-block;
          border: 1px solid rgba(0, 180, 255, 0.3);
        }

        .btn-service {
          display: flex;
          align-items: center;
          justify-content: center;
          background: linear-gradient(135deg, #0066cc, #0099ff);
          color: white;
          text-decoration: none;
          padding: 0.9rem 1.8rem;
          border-radius: 50px;
          font-weight: 600;
          font-size: 0.95rem;
          transition: all 0.3s ease;
          border: 1px solid rgba(0, 180, 255, 0.5);
          width: 100%;
          gap: 10px;
        }

        .btn-service i {
          transition: transform 0.2s;
        }

        .btn-service:hover {
          background: #0f4662;
          border-color: #00f2ff;
          color: white;
          box-shadow: 0 0 14px rgba(0, 210, 255, 0.5);
          gap: 16px;
        }

        .btn-service:hover i {
          transform: translateX(5px);
        }

        /* 多集群信息栏 */
        .info-strip {
          margin-top: 2rem;
          display: flex;
          flex-wrap: wrap;
          justify-content: center;
          gap: 1rem;
          background: rgba(0, 0, 0, 0.4);
          border-radius: 2rem;
          padding: 1rem 1.8rem;
          backdrop-filter: blur(10px);
          border: 1px solid rgba(0, 230, 250, 0.25);
        }

        .info-item {
          display: flex;
          align-items: center;
          gap: 8px;
          font-size: 0.85rem;
          color: #cae3ff;
          background: rgba(0, 25, 45, 0.6);
          padding: 0.4rem 1.2rem;
          border-radius: 40px;
          transition: 0.2s;
        }

        .info-item i {
          color: #2dd4ff;
          width: 1.2rem;
        }

        .live-dot {
          display: inline-block;
          width: 8px;
          height: 8px;
          background: #2eff9e;
          border-radius: 50%;
          box-shadow: 0 0 6px #3effa0;
          margin-right: 6px;
          animation: pulse 1.8s infinite;
        }

        @keyframes pulse {
          0% { opacity: 0.4; transform: scale(0.8);}
          100% { opacity: 1; transform: scale(1.2);}
        }

        /* 地址映射特殊标签 */
        .ip-tag {
          font-weight: 600;
          font-family: monospace;
        }

        .footer-note {
          margin-top: 2.2rem;
          text-align: center;
          font-size: 0.72rem;
          color: #5982a8;
          display: flex;
          justify-content: center;
          gap: 1.5rem;
          flex-wrap: wrap;
        }

        /* 响应式布局 */
        @media (max-width: 860px) {
          .service-card { width: 260px; padding: 1.4rem 1rem; }
          .hero h1 { font-size: 2.2rem; }
          .btn-service { width: 95%; font-size: 0.85rem; }
        }

        @media (max-width: 640px) {
          body { padding: 1rem; }
          .service-grid { gap: 1.2rem; }
          .service-card { width: 100%; max-width: 320px; }
          .info-item { font-size: 0.7rem; padding: 0.3rem 0.8rem; }
        }

        ::-webkit-scrollbar { width: 5px; height: 5px; }
        ::-webkit-scrollbar-track { background: #0a121f; border-radius: 8px; }
        ::-webkit-scrollbar-thumb { background: #1e7898; border-radius: 8px; }
        """

    def _generate_services_data(self):
        """生成服务数据"""
        return [
            {
                "icon": "fas fa-chart-line",
                "title": "ELK 日志分析",
                "description": "集中日志 · Kibana 可视化 · 实时监控与智能告警",
                "port": "192.168.1.60 : 5601",
                "url": "http://192.168.1.60:5601/app/home",
                "button_text": "进入 Kibana"
            },
            {
                "icon": "fas fa-microchip",
                "title": "智能家居中枢",
                "description": "Home Assistant / IoT 网关 · 设备联动 · 自动化场景",
                "port": "192.168.1.60 : 8123",
                "url": "http://192.168.1.60:8123",
                "button_text": "管理智能设备"
            },
            {
                "icon": "fas fa-database",
                "title": "Elasticsearch",
                "description": "分布式搜索与分析 · REST API · 高性能数据引擎",
                "port": "192.168.1.60 : 9200",
                "url": "https://192.168.1.60:9200",
                "button_text": "集群状态 & API"
            },
            {
                "icon": "fas fa-shield-hooded",
                "title": "360 管控平台",
                "description": "安全运营中心 · 终端检测响应 · 全网态势与策略管控",
                "port": "192.168.1.54 : 443 / Web",
                "url": "https://192.168.1.54/dist/#/login",
                "button_text": "进入管控平台"
            }
        ]

    def _generate_service_card(self, service):
        """生成单个服务卡片HTML"""
        return f"""
        <div class="service-card">
          <div class="card-icon">
            <i class="{service['icon']}"></i>
          </div>
          <h2>{service['title']}</h2>
          <div class="service-desc">
            {service['description']}
          </div>
          <div class="port-badge">
            <i class="fas fa-location-dot"></i> {service['port']}
          </div>
          <a href="{service['url']}" class="btn-service" target="_blank" rel="noopener noreferrer">
            <span>{service['button_text']}</span>
            <i class="fas fa-arrow-right"></i>
          </a>
        </div>
        """

    def _generate_javascript(self):
        """生成JavaScript代码"""
        return """
        <script>
          (function() {
            // 定义所有集成服务配置
            const services = [
              { name: "ELK Kibana", ip: "192.168.1.60", port: 5601, url: "http://192.168.1.60:5601/app/home" },
              { name: "智能家居平台", ip: "192.168.1.60", port: 8123, url: "http://192.168.1.60:8123" },
              { name: "Elasticsearch API", ip: "192.168.1.60", port: 9200, url: "http://192.168.1.60:9200" },
              { name: "360 管控平台", ip: "192.168.1.54", port: "80/443", url: "http://192.168.1.54" }
            ];

            console.log("%c🛡️ 统一服务管控中枢 · 已加载全部服务入口", "color: #2dd4ff; font-size: 14px; font-weight: bold; background: #0a1428; padding: 2px 6px; border-radius: 8px;");
            console.table(services.map(s => ({ 服务名称: s.name, IP地址: s.ip, 端口: s.port, 访问链接: s.url })));
            console.log("%c💡 提示：点击对应卡片按钮，可直接访问 192.168.1.60 下的三大服务及 192.168.1.54 的360管控平台", "color: #9ec8ff;");

            // 优雅的卡片双击反馈
            const cards = document.querySelectorAll('.service-card');
            cards.forEach(card => {
              const btn = card.querySelector('.btn-service');
              if (!btn) return;
              card.addEventListener('dblclick', (e) => {
                if (e.target.closest('.btn-service')) return;
                if (btn.href) {
                  window.open(btn.href, '_blank');
                  card.style.transform = "scale(0.98)";
                  setTimeout(() => { card.style.transform = ""; }, 150);
                }
              });
            });

            console.log("✅ 当前可用节点: 192.168.1.60 (ELK/智能家居/ES)  +  192.168.1.54 (360管控)");
          })();
        </script>
        """

    def _generate_dashboard_html(self, hostname, pid, current_time, git_branch, git_commit):
        """生成完整的仪表板HTML"""
        services_data = self._generate_services_data()
        service_cards = ''.join([self._generate_service_card(service) for service in services_data])
        
        return f"""
        <!DOCTYPE html>
        <html lang="zh-CN">
        <head>
          <meta charset="UTF-8">
          <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
          <title>智能服务中枢 · 统一管控门户 | ELK + 智能家居 + ES + 360平台</title>
          <link href="https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,300;14..32,400;14..32,500;14..32,600;14..32,700;14..32,800&display=swap" rel="stylesheet">
          <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
          <style>
            {self._generate_css()}
          </style>
        </head>
        <body>
          <div class="dashboard">
            <!-- 头部区域 -->
            <div class="hero">
              <div class="hero-icon">
                <i class="fas fa-network-wired"></i>
              </div>
              <h1>统一服务管控中枢</h1>
              <p><i class="fas fa-globe"></i> 多节点 · 多服务聚合入口 | 实时运维 & 安全管理</p>
            </div>

            <!-- 服务卡片网格 -->
            <div class="service-grid">
              {service_cards}
            </div>

            <!-- 统一信息栏 -->
            <div class="info-strip">
              <div class="info-item">
                <i class="fas fa-server"></i> 
                <span><span class="live-dot"></span> 主节点 192.168.1.60</span>
              </div>
              <div class="info-item">
                <i class="fas fa-chart-simple"></i> ELK:5601
              </div>
              <div class="info-item">
                <i class="fas fa-microchip"></i> 智能家居:8123
              </div>
              <div class="info-item">
                <i class="fas fa-database"></i> ES:9200
              </div>
              <div class="info-item">
                <i class="fas fa-shield-virus"></i> <span class="ip-tag">360平台: 192.168.1.54</span>
              </div>
              <div class="info-item">
                <i class="fas fa-shield-alt"></i> 安全策略已启用
              </div>
            </div>

            <!-- 详细地址及服务说明栏 -->
            <div class="footer-note">
              <span><i class="far fa-check-circle"></i> 日志中枢 · 智能家居生态 · ES 数据湖 · 360安全大脑</span>
              <span><i class="fas fa-sync-alt"></i> 跨平台统一入口 | 支持快速跳转</span>
              <span><i class="fas fa-chart-line"></i> 实时监控 & 集中管控</span>
            </div>
          </div>
          {self._generate_javascript()}
        </body>
        </html>
        """

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
            git_branch = "要成功"
            try:
                with open('.git/HEAD', 'r') as f:
                    head_content = f.read().strip()
                    if 'ref:' in head_content:
                        git_branch = head_content.split('/')[-1]
                with open('.git/refs/heads/' + git_branch, 'r') as f:
                    git_commit = f.read().strip()[:7]
            except:
                pass
            
            # 生成HTML响应内容
            html_content = self._generate_dashboard_html(hostname, pid, current_time, git_branch, git_commit)
            self.wfile.write(html_content.encode())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404 Not Found")
    
    def log_message(self, format, *args):
        """自定义日志输出"""
        print(f"[{datetime.datetime.now()}] {args[0]}")

def run_server(port=80):
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
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 80
    run_server(port)