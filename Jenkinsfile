pipeline {
    agent any
    
    environment {
        REMOTE_USER = 'root'
        REMOTE_HOST = '192.168.1.56'
        REMOTE_PATH = '/home/myapp_build'
        CONTAINER_NAME = 'myapp'
        IMAGE_NAME = 'myapp:latest'
        HOST_PORT = '80'
        CONTAINER_PORT = '80'
    }

    stages {
        stage('代码准备') {
            steps {
                git url: 'https://github.com/hutroot/hutroot/', branch: 'main'
                
                sh """
                    ssh ${REMOTE_USER}@${REMOTE_HOST} "mkdir -p ${REMOTE_PATH}"
                    tar czf - --exclude='.git' . | ssh ${REMOTE_USER}@${REMOTE_HOST} "tar xzf - -C ${REMOTE_PATH}"
                """
            }
        }

        stage('构建部署') {
            steps {
                sh """
                    ssh ${REMOTE_USER}@${REMOTE_HOST} << 'EOF'
                        cd ${REMOTE_PATH}
                        
                        # 清理旧容器
                        docker stop ${CONTAINER_NAME} 2>/dev/null || true
                        docker rm ${CONTAINER_NAME} 2>/dev/null || true
                        
                        # 清理旧镜像（保留最新）
                        docker images ${IMAGE_NAME} -q | tail -n +2 | xargs -r docker rmi 2>/dev/null || true
                        
                        # 构建并运行
                        docker build --no-cache -t ${IMAGE_NAME} .
                        docker run -d \\
                            --name ${CONTAINER_NAME} \\
                            --restart unless-stopped \\
                            -p ${HOST_PORT}:${CONTAINER_PORT} \\
                            ${IMAGE_NAME}
                        
                        # 更新部署时间
                        sleep 3
                        DEPLOYMENT_TIME=\$(date +"%Y-%m-%d %H:%M:%S")
                        docker exec ${CONTAINER_NAME} sh -c "echo '{\"deployment_time\": \"'\$DEPLOYMENT_TIME'\"}' > deployment_info.json" 2>/dev/null || true
                        
                        # 清理资源
                        docker container prune -f
                        docker image prune -f
EOF
                """
            }
        }

        stage('验证清理') {
            steps {
                sleep time: 5, unit: 'SECONDS'
                
                sh """
                    ssh ${REMOTE_USER}@${REMOTE_HOST} "docker ps | grep ${CONTAINER_NAME}"
                    ssh ${REMOTE_USER}@${REMOTE_HOST} "rm -rf ${REMOTE_PATH}"
                """
            }
        }
    }

    post {
        success {
            echo '✅ 部署成功'
        }
        failure {
            echo '❌ 部署失败'
            sh """
                ssh ${REMOTE_USER}@${REMOTE_HOST} "docker logs --tail 30 ${CONTAINER_NAME}" 2>/dev/null || true
            """
        }
    }
}