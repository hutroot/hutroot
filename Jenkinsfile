pipeline {
    agent any
    
    environment {
        REMOTE_USER = 'root'
        REMOTE_HOST = '192.168.1.56'
        REMOTE_PATH = '/home/myapp_build'
        CONTAINER_NAME = 'myapp'
        IMAGE_NAME = 'myapp:latest'
        HOST_PORT = '8080'
        CONTAINER_PORT = '8080'
    }

    stages {
        stage('拉取代码') {
            steps {
                echo '正在拉取代码'
                git url: 'https://github.com/hutroot/hutroot/', branch: 'main'
                echo '代码拉取完成'
            }
        }

        stage('传输代码到远程机器') {
            steps {
                echo "传输代码到 ${REMOTE_HOST}:${REMOTE_PATH}"
                sh """
                    ssh ${REMOTE_USER}@${REMOTE_HOST} "mkdir -p ${REMOTE_PATH}"
                    tar czf - --exclude='.git' . | ssh ${REMOTE_USER}@${REMOTE_HOST} "tar xzf - -C ${REMOTE_PATH}"
                    echo "✓ 代码传输完成"
                """
            }
        }

        stage('远程构建和部署') {
            steps {
                sh """
                    ssh ${REMOTE_USER}@${REMOTE_HOST} << 'EOF'
                        cd ${REMOTE_PATH}

                        echo "=== 开始构建和部署流程 ==="
                        
                        # 1. 检查并停止正在运行的容器
                        echo "1. 检查并停止正在运行的容器..."
                        if docker ps -a | grep -q ${CONTAINER_NAME}; then
                            echo "发现正在运行的容器 ${CONTAINER_NAME}，正在停止..."
                            docker stop ${CONTAINER_NAME} || echo "停止容器失败或容器未运行"
                            docker rm ${CONTAINER_NAME} || echo "删除容器失败或容器不存在"
                            echo "✓ 旧容器清理完成"
                        else
                            echo "未发现正在运行的容器 ${CONTAINER_NAME}"
                        fi

                        # 2. 清理旧镜像（可选，避免磁盘空间不足）
                        echo "2. 清理旧镜像..."
                        OLD_IMAGES=\$(docker images ${IMAGE_NAME} -q | tail -n +2)
                        if [ -n "\$OLD_IMAGES" ]; then
                            echo "发现旧镜像，正在清理..."
                            echo \$OLD_IMAGES | xargs -r docker rmi || echo "清理旧镜像失败或不存在"
                        fi

                        # 3. 构建新镜像
                        echo "3. 开始构建 Docker 镜像..."
                        docker build --no-cache -t ${IMAGE_NAME} .

                        # 4. 启动新容器
                        echo "4. 启动新容器..."
                        docker run -d \\
                            --name ${CONTAINER_NAME} \\
                            --restart unless-stopped \\
                            -p ${HOST_PORT}:${CONTAINER_PORT} \\
                            ${IMAGE_NAME}

                        # 等待容器启动后，强制更新部署时间
                        echo "强制更新部署时间..."
                        sleep 5
                        docker exec ${CONTAINER_NAME} sh -c 'echo "{\\\"deployment_time\\\": \\\"'\$(date +"%Y-%m-%d %H:%M:%S")\"'\\\"}" > deployment_info.json' || echo "更新部署时间失败"

                        # 5. 清理无用镜像和容器
                        echo "5. 清理无用资源..."
                        docker container prune -f
                        docker image prune -f

                        echo "✓ 部署完成"
EOF
                """
            }
        }

        stage('清理远程临时文件') {
            steps {
                echo "清理远程临时文件"
                sh """
                    ssh ${REMOTE_USER}@${REMOTE_HOST} "rm -rf ${REMOTE_PATH}"
                """
            }
        }

        stage('健康检查') {
            steps {
                echo "等待服务启动..."
                sleep time: 10, unit: 'SECONDS'

                sh """
                    ssh ${REMOTE_USER}@${REMOTE_HOST} "docker ps | grep ${CONTAINER_NAME} && echo '✓ 容器运行正常'"
                """
            }
        }
    }

    post {
        success {
            echo '🎉 部署成功！'
        }
        failure {
            echo '❌ 部署失败！'
            sh """
                ssh ${REMOTE_USER}@${REMOTE_HOST} "docker logs --tail 50 ${CONTAINER_NAME}" || true
            """
        }
    }
}