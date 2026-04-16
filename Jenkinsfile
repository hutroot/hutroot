pipeline {
    agent any
    
    environment {
        // 镜像配置
        IMAGE_NAME = 'spider-test'
        IMAGE_TAG = "${env.BUILD_NUMBER}-${env.GIT_COMMIT.take(7)}"
        
        // Docker 配置（如需推送到镜像仓库，取消注释）
        // DOCKER_REGISTRY = 'your-registry.com'
        // DOCKER_CRED = 'docker-registry-credentials'
    }
    
    stages {
        // 1. 拉取代码
        stage('Checkout') {
            steps {
                checkout scm
                echo "✅ 代码拉取成功，分支: ${env.BRANCH_NAME}"
                echo "📝 Commit: ${env.GIT_COMMIT}"
            }
        }
        
        // 2. 查看代码文件（调试用）
        stage('List Files') {
            steps {
                sh 'ls -la'
                sh 'cat app.py | head -20 || echo "app.py 不存在"'
            }
        }
        
        // 3. 构建 Docker 镜像
        stage('Build Docker Image') {
            steps {
                script {
                    echo "🔨 开始构建镜像: ${IMAGE_NAME}:${IMAGE_TAG}"
                    docker.build("${IMAGE_NAME}:${IMAGE_TAG}", ".")
                }
            }
        }
        
        // 4. 运行测试（验证容器能否正常启动）
        stage('Test Container') {
            steps {
                script {
                    echo "🧪 启动测试容器..."
                    sh """
                        docker stop ${IMAGE_NAME}-test || true
                        docker rm ${IMAGE_NAME}-test || true
                        docker run -d --name ${IMAGE_NAME}-test -p 8081:8080 ${IMAGE_NAME}:${IMAGE_TAG}
                        sleep 3
                        curl -f http://localhost:8081/ || exit 1
                        echo "✅ 容器测试通过"
                    """
                }
            }
            post {
                always {
                    // 清理测试容器
                    sh """
                        docker stop ${IMAGE_NAME}-test || true
                        docker rm ${IMAGE_NAME}-test || true
                    """
                }
            }
        }
        
        // 5. 部署到生产环境
        stage('Deploy') {
            steps {
                script {
                    echo "🚀 开始部署..."
                    
                    // 停止并删除旧容器
                    sh """
                        docker stop ${IMAGE_NAME} || true
                        docker rm ${IMAGE_NAME} || true
                    """
                    
                    // 启动新容器
                    sh """
                        docker run -d \
                            --name ${IMAGE_NAME} \
                            --restart unless-stopped \
                            -p 8080:8080 \
                            ${IMAGE_NAME}:${IMAGE_TAG}
                    """
                    
                    // 等待服务启动并验证
                    sh """
                        sleep 3
                        curl -f http://localhost:8081/ || exit 1
                        echo "✅ 部署成功！"
                    """
                }
            }
        }
    }
    
    post {
        // 构建成功
        success {
            echo """
            ╔════════════════════════════════════════════════════╗
            ║  🎉 构建与部署成功！                               ║
            ╠════════════════════════════════════════════════════╣
            ║  镜像: ${IMAGE_NAME}:${IMAGE_TAG}                  ║
            ║  访问: http://<服务器IP>:8081                       ║
            ╚════════════════════════════════════════════════════╝
            """
        }
        
        // 构建失败
        failure {
            echo """
            ❌ 构建失败！
            📋 请检查控制台输出定位问题
            """
        }
        
        // 无论成功失败，清理旧镜像（保留最近5个）
        always {
            script {
                sh """
                    docker image prune -f --filter "until=24h" || true
                    echo "🧹 清理完成"
                """
            }
        }
    }
}