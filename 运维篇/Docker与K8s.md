# Docker 与 Kubernetes

## 一、容器化概述

### 什么是容器

**容器** 是一种轻量级的虚拟化技术，将应用及其依赖打包在一起，实现"一次构建，到处运行"。

```
传统部署                    容器化部署
┌─────────────┐            ┌─────────────┐
│   App A     │            │  App A  │ B │
│   Libs A    │            │  Libs   │   │
│   Guest OS  │            └───Container──┘
├─────────────┤            ┌─────────────┐
│   App B     │            │  App C  │ D │
│   Libs B    │            │  Libs   │   │
│   Guest OS  │            └───Container──┘
├─────────────┤            ├─────────────┤
│ Hypervisor  │            │  Host OS    │
├─────────────┤            ├─────────────┤
│  Host OS    │            │  Hardware   │
└─────────────┘            └─────────────┘
    VM 方案                    容器方案
```

| 对比 | 虚拟机 (VM) | 容器 (Container) |
|:----:|:----------:|:----------------:|
| 启动时间 | 分钟级（需启动 Guest OS） | **秒级**（共享宿主内核） |
| 占用空间 | GB 级（完整 OS） | **MB 级**（仅应用+依赖） |
| 性能 | 有损耗（硬件虚拟化） | **接近原生**（直接调用宿主内核） |
| 隔离性 | **完全隔离**（独立内核） | 进程级隔离（共享宿主内核） |
| 密度 | 一台主机十几个 | **一台主机成百上千个** |

### Docker 架构

```
┌─────────────────────────────────────────────┐
│                Docker Client                 │
│          (docker pull, run, build...)        │
└──────────────────┬──────────────────────────┘
                   │ REST API
                   ▼
┌─────────────────────────────────────────────┐
│              Docker Daemon (dockerd)         │
│    ┌──────────┐ ┌──────────┐ ┌──────────┐   │
│    │  Images  │ │Containers│ │  Volumes │   │
│    └──────────┘ └──────────┘ └──────────┘   │
└──────────────────┬──────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────┐
│           Docker Registry (Hub)              │
│         存储和分发镜像的仓库                  │
└─────────────────────────────────────────────┘
```

### 安装 Docker

```bash
# Ubuntu / Debian
sudo apt update && sudo apt install docker.io

# CentOS / RHEL
sudo yum install -y docker
sudo systemctl start docker
sudo systemctl enable docker

# macOS / Windows
# 下载 Docker Desktop: https://www.docker.com/products/docker-desktop

# 验证安装
docker --version
docker run hello-world
```

---

## 二、Docker 基础操作 ⭐

### 镜像管理

```bash
# ⭐ 搜索镜像
docker search nginx
docker search ubuntu

# ⭐ 拉取镜像
docker pull nginx:latest           # 默认 latest 标签
docker pull ubuntu:22.04           # 指定版本
docker pull registry.cn-hangzhou.aliyuncs.com/xxx/yyy  # 国内镜像源

# ⭐ 列出本地镜像
docker images
docker image ls
docker images -a                   # 列出所有（包括中间层）

# 查看镜像详情
docker image inspect nginx

# 删除镜像
docker rmi nginx                   # 删除指定镜像
docker rmi $(docker images -q)     # 删除所有镜像
docker image prune                 # 清理未使用的镜像

# ⭐ 标记镜像
docker tag nginx:latest my-nginx:v1

# 推送镜像到仓库
docker push my-nginx:v1
```

### 容器生命周期 ⭐

```bash
# ⭐ 创建并启动容器
docker run nginx                           # 前台运行（阻塞终端）
docker run -d nginx                        # 后台运行（detached）
docker run --name my-nginx nginx           # 指定容器名称
docker run -p 8080:80 nginx                # 端口映射：宿主机:容器
docker run -v /host/data:/app/data nginx   # 挂载数据卷
docker run -e ENV=prod nginx               # 设置环境变量
docker run --restart=always nginx          # 容器退出时自动重启
docker run --rm nginx                      # 容器停止后自动删除

# 常用组合
docker run -d --name web -p 8080:80 -v ./html:/usr/share/nginx/html nginx

# ⭐ 容器管理
docker ps                                  # 查看运行中的容器
docker ps -a                               # 查看所有容器（包括已停止的）
docker stop <container>                    # 停止容器
docker start <container>                   # 启动已停止的容器
docker restart <container>                 # 重启容器
docker pause <container>                   # 暂停容器
docker unpause <container>                 # 恢复容器
docker rm <container>                      # 删除容器
docker rm -f <container>                   # 强制删除运行中的容器
docker rm $(docker ps -aq)                 # 删除所有容器

# ⭐ 进入容器
docker exec -it <container> bash           # 在运行中的容器中执行命令
docker exec -it <container> sh             # 如果容器没有 bash
docker attach <container>                  # 附加到容器的标准输入输出

# ⭐ 查看日志
docker logs <container>                    # 查看日志
docker logs -f <container>                 # 实时跟踪日志（tail -f）
docker logs --tail 100 <container>         # 查看最后 100 行
docker logs -t <container>                 # 显示时间戳
```

### 端口映射详解

```bash
# 端口映射格式
docker run -p <宿主机端口>:<容器端口> <镜像>

# 示例
docker run -p 8080:80 nginx                # 宿主机 8080 → 容器 80
docker run -p 80:80 nginx                  # 相同端口
docker run -p 127.0.0.1:8080:80 nginx      # 只监听本机
docker run -p 8080:80 -p 443:443 nginx     # 映射多个端口
docker run -P nginx                        # 随机分配宿主机端口
```

### 数据持久化 ⭐

```bash
# ⭐ 方式一：bind mount（绑定挂载，指定宿主机路径）
docker run -v /host/data:/container/data nginx
docker run --mount type=bind,src=/host/data,target=/container/data nginx

# ⭐ 方式二：volume（卷管理，Docker 管理路径）
docker volume create my-volume              # 创建卷
docker volume ls                            # 列出卷
docker volume inspect my-volume             # 查看卷详情
docker run -v my-volume:/container/data nginx
docker run --mount type=volume,src=my-volume,target=/app/data nginx

# 方式三：tmpfs（临时文件系统，存在内存中）
docker run --tmpfs /tmp nginx

# 查看数据卷
docker volume inspect <volume-name>
# 默认路径：/var/lib/docker/volumes/<volume-name>/_data
```

> [!tip] **bind mount vs volume**
> | 对比 | bind mount | volume |
> |:----:|:----------:|:------:|
> | 管理方式 | 用户管理 | Docker 管理 |
> | 位置 | 任意宿主机路径 | `/var/lib/docker/volumes/` |
> | 备份 | 手动 | `docker run --volumes-from` |
> | 跨主机 | 不支持 | 可通过驱动支持 |
> | 推荐 | 开发环境 | **生产环境** |

---

## 三、Dockerfile ⭐

### 指令详解

```dockerfile
# ⭐ FROM：指定基础镜像（必须是第一条指令）
FROM node:20-alpine          # Alpine 版本（更小）
FROM ubuntu:22.04
FROM python:3.12-slim
FROM scratch                 # 空镜像（构建静态编译二进制）

# ⭐ LABEL：元数据
LABEL maintainer="dev@example.com"
LABEL version="1.0"
LABEL description="生产环境 Node.js 应用"

# ⭐ WORKDIR：设置工作目录（自动创建）
WORKDIR /app

# ⭐ COPY：复制文件（从构建上下文到镜像）
COPY package.json package-lock.json ./     # 先复制依赖文件（利用缓存）
COPY . .                                    # 复制所有源码

# ⭐ RUN：在构建时执行命令
RUN npm install                             # 安装依赖
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
RUN pip install -r requirements.txt

# ⭐ ENV：设置环境变量
ENV NODE_ENV=production
ENV PORT=3000
ENV DB_HOST=localhost

# ⭐ EXPOSE：声明容器监听端口（仅文档作用）
EXPOSE 3000
EXPOSE 80 443

# ⭐ CMD：容器启动时的默认命令（可以被覆盖）
CMD ["node", "server.js"]
CMD npm start                               # shell 格式

# ⭐ ENTRYPOINT：容器入口点（不可覆盖）
ENTRYPOINT ["python"]
CMD ["app.py"]                              # ENTRYPOINT 的默认参数

# ⭐ USER：指定运行用户（安全）
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser

# ⭐ ARG：构建参数（构建时可覆盖）
ARG VERSION=latest
RUN echo "Building version ${VERSION}"

# ⭐ HEALTHCHECK：健康检查
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
    CMD curl -f http://localhost:3000/health || exit 1
```

### 多阶段构建 ⭐

```dockerfile
# ⭐ 阶段一：构建环境
FROM node:20-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

# ⭐ 阶段二：运行环境（只复制构建产物）
FROM node:20-alpine AS runner

WORKDIR /app

# 只复制需要的文件
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY package.json ./

EXPOSE 3000
CMD ["node", "dist/server.js"]

# 最终镜像只有 100MB+，而非包含构建工具的 1GB+
```

```dockerfile
# ⭐ Go 多阶段构建（极致精简，最终镜像约 10MB）
FROM golang:1.22 AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o /app/server

FROM scratch
COPY --from=builder /app/server /server
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
EXPOSE 8080
CMD ["/server"]
```

### .dockerignore

```dockerignore
# ⭐ 忽略文件（加快构建速度，避免敏感信息泄露）
node_modules
.git
.env
.env.local
*.md
.gitignore
Dockerfile
.dockerignore
dist
.cache
```

### 最佳实践 Dockerfile ⭐

```dockerfile
# 生产 Node.js 应用
FROM node:20-alpine AS base
RUN apk add --no-cache tini                    # 正确的 init 进程
WORKDIR /app

# 依赖层（利用构建缓存）
FROM base AS deps
COPY package.json package-lock.json ./
RUN npm ci --only=production && npm cache clean --force

# 构建层
FROM deps AS build
COPY . .
RUN npm run build

# 运行层
FROM base AS run
RUN addgroup -S app && adduser -S app -G app

COPY --from=deps /app/node_modules ./node_modules
COPY --from=build /app/dist ./dist
COPY package.json ./

USER app
EXPOSE 3000

ENTRYPOINT ["/sbin/tini", "--"]
CMD ["node", "dist/server.js"]

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:3000/health || exit 1
```

---

## 四、Docker Compose ⭐

### 基本概念

**Docker Compose** 用于定义和运行多容器 Docker 应用，通过 YAML 文件配置所有服务。

### docker-compose.yml ⭐

```yaml
# docker-compose.yml
version: "3.9"

services:
  # ⭐ Web 服务
  web:
    build:
      context: .                   # Dockerfile 所在目录
      dockerfile: Dockerfile
      args:
        NODE_ENV: production
    image: my-app:latest
    container_name: my-web
    ports:
      - "80:3000"
      - "443:3001"
    environment:
      NODE_ENV: production
      DB_HOST: postgres
      REDIS_HOST: redis
    env_file:
      - .env.production
    volumes:
      - uploads:/app/uploads
      - ./logs:/app/logs
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_started
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 3s
      retries: 3
    networks:
      - frontend
      - backend

  # 数据库
  postgres:
    image: postgres:16-alpine
    container_name: my-postgres
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: app
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "5432:5432"          # 开发时暴露，生产不暴露
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U app -d myapp"]
      interval: 5s
      timeout: 3s
      retries: 5
    networks:
      - backend

  # 缓存
  redis:
    image: redis:7-alpine
    container_name: my-redis
    volumes:
      - redis_data:/data
    command: redis-server --appendonly yes
    networks:
      - backend

  # 消息队列
  queue:
    image: rabbitmq:3-management-alpine
    container_name: my-rabbitmq
    environment:
      RABBITMQ_DEFAULT_USER: admin
      RABBITMQ_DEFAULT_PASS: ${RABBITMQ_PASSWORD}
    ports:
      - "15672:15672"        # 管理界面
    networks:
      - backend

  # Nginx 反向代理
  nginx:
    image: nginx:alpine
    container_name: my-nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - web
    networks:
      - frontend

volumes:
  postgres_data:
  redis_data:
  uploads:

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true           # 后端网络对外不可见
```

### 常用命令

```bash
# ⭐ 启动所有服务
docker compose up                           # 前台启动
docker compose up -d                        # 后台启动
docker compose up -d --build                # 重新构建后启动

# ⭐ 管理服务
docker compose ps                           # 查看状态
docker compose logs -f                      # 跟踪所有日志
docker compose logs -f web                  # 跟踪指定服务日志
docker compose stop                         # 停止所有
docker compose stop web                     # 停止指定服务
docker compose start                        # 启动所有
docker compose restart                      # 重启所有

# ⭐ 执行命令
docker compose exec web bash                # 在 web 容器中执行命令
docker compose exec web npm test            # 运行测试

# ⭐ 构建
docker compose build                        # 构建所有
docker compose build web                    # 构建指定服务
docker compose build --no-cache             # 不使用缓存

# ⭐ 清理
docker compose down                         # 停止并删除容器
docker compose down -v                      # 同时删除数据卷
docker compose down --rmi all               # 同时删除镜像

# ⭐ 查看
docker compose images                       # 列出使用的镜像
docker compose top                          # 列出各个服务的进程
docker compose config                       # 验证并查看合并配置
```

---

## 五、Docker 网络

### 网络模式

```bash
# ⭐ 五种网络模式
# 1. bridge（默认）：通过虚拟网桥通信，同主机的容器互联
docker run --network=bridge nginx

# 2. host：直接使用宿主机网络，无网络隔离
docker run --network=host nginx

# 3. none：无网络
docker run --network=none nginx

# 4. container：共享另一个容器的网络栈
docker run --network=container:<container-name> nginx

# 5. overlay：跨多台主机的网络（Swarm/K8s 环境）
docker network create -d overlay my-overlay
```

```bash
# ⭐ 自定义 bridge 网络（推荐）
docker network create --driver bridge \
    --subnet=172.20.0.0/16 \
    --ip-range=172.20.0.0/24 \
    --gateway=172.20.0.1 \
    my-network

# 在自定义网络中，容器可以通过名称直接通信
docker run --network=my-network --name web nginx
docker run --network=my-network --name api node
# web 可以通过 "api" 这个主机名访问 api 容器

# 网络管理
docker network ls                           # 列出网络
docker network inspect my-network           # 查看网络详情
docker network connect my-network web       # 将容器连接到网络
docker network disconnect my-network web    # 断开连接
```

---

## 六、Kubernetes 概述

### 什么是 Kubernetes

**Kubernetes（K8s）** 是 Google 开源的容器编排平台，用于自动部署、扩展和管理容器化应用。

```
目标状态（Desired State）
    │
    ▼
┌──────────────────┐
│   Control Plane  │  ← 控制面
│  (API Server)    │
└──────┬───────────┘
       │ watch
       ▼
┌──────────────────┐
│     Node 1       │
│  ┌──────┐       │
│  │ Pod  │       │
│  └──────┘       │
│  ┌──────┐       │
│  │ Pod  │       │
│  └──────┘       │
└──────────────────┘
┌──────────────────┐
│     Node 2       │
│  ┌──────┐       │
│  │ Pod  │       │
│  └──────┘       │
└──────────────────┘
```

### 核心架构

| 组件 | 作用 | 部署位置 |
|:----:|:----:|:--------:|
| **API Server** | K8s 的入口，所有操作的唯一入口 | Control Plane |
| **etcd** | 分布式键值存储，存储所有集群数据 | Control Plane |
| **Scheduler** | 调度 Pod 到合适的 Node | Control Plane |
| **Controller Manager** | 管理各种控制器（Deployment、Node 等） | Control Plane |
| **kubelet** | 每个 Node 的代理，管理 Pod 生命周期 | Worker Node |
| **kube-proxy** | 网络代理和负载均衡 | Worker Node |
| **Container Runtime** | 实际运行容器的引擎（containerd、CRI-O） | Worker Node |

### minikube 快速开始

```bash
# 安装 minikube
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# 启动集群
minikube start --driver=docker
minikube start --cpus=4 --memory=8g          # 指定资源

# 查看状态
minikube status
kubectl cluster-info
kubectl get nodes

# 打开 Dashboard
minikube dashboard

# 停止集群
minikube stop
minikube delete
```

### kubectl 基础 ⭐

```bash
# ⭐ 集群管理
kubectl cluster-info                # 查看集群信息
kubectl get nodes                   # 查看节点
kubectl describe node <node-name>   # 查看节点详情

# ⭐ 命名空间
kubectl get namespaces              # 列出命名空间
kubectl config set-context --current --namespace=prod  # 切换默认命名空间

# ⭐ 资源管理
kubectl get all                     # 查看所有资源
kubectl api-resources               # 列出所有 API 资源

# ⭐ 简写
# po = pods, svc = services, deploy = deployments
# ns = namespaces, cm = configmaps, secret = secrets
# pv = persistentvolumes, pvc = persistentvolumeclaims
# ing = ingresses, no = nodes
```

---

## 七、Kubernetes 核心资源 ⭐

### Pod

Pod 是 K8s 最小的可部署单元，包含一个或多个容器。

```yaml
# pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
  labels:
    app: my-app
    env: production
spec:
  containers:
    - name: web
      image: nginx:alpine
      ports:
        - containerPort: 80
      env:
        - name: NODE_ENV
          value: "production"
      resources:
        requests:
          cpu: "100m"         # 0.1 核
          memory: "128Mi"
        limits:
          cpu: "500m"         # 0.5 核
          memory: "256Mi"
      livenessProbe:          # 存活探针（容器挂了就重启）
        httpGet:
          path: /health
          port: 80
        initialDelaySeconds: 5
        periodSeconds: 10
      readinessProbe:         # 就绪探针（是否接收流量）
        httpGet:
          path: /ready
          port: 80
        initialDelaySeconds: 3
        periodSeconds: 5
      volumeMounts:
        - name: config
          mountPath: /etc/config
  volumes:
    - name: config
      configMap:
        name: app-config
```

```bash
# Pod 操作
kubectl apply -f pod.yaml
kubectl get pods
kubectl get pods -o wide                # 显示节点 IP 等信息
kubectl describe pod my-pod
kubectl logs my-pod
kubectl logs -f my-pod                  # 跟踪日志
kubectl exec -it my-pod -- sh           # 进入容器
kubectl delete pod my-pod
```

### Deployment ⭐

Deployment 管理 Pod 的声明式更新和扩缩容。

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-deployment
  labels:
    app: web
spec:
  # ⭐ 副本数
  replicas: 3

  # ⭐ 选择器
  selector:
    matchLabels:
      app: web

  # ⭐ Pod 模板
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
        - name: web
          image: my-app:1.2.3
          ports:
            - containerPort: 3000
          env:
            - name: DB_HOST
              value: postgres-service

  # ⭐ 更新策略
  strategy:
    type: RollingUpdate               # 滚动更新（默认）
    rollingUpdate:
      maxSurge: 1                     # 最大超出副本数
      maxUnavailable: 0               # 最大不可用副本数（零停机）

  # ⭐ 回滚配置
  revisionHistoryLimit: 5             # 保留历史版本数
```

```bash
# Deployment 操作
kubectl apply -f deployment.yaml
kubectl get deployments

# ⭐ 扩缩容
kubectl scale deployment web-deployment --replicas=5
kubectl autoscale deployment web-deployment --min=2 --max=10 --cpu-percent=80

# ⭐ 更新镜像
kubectl set image deployment/web-deployment web=my-app:2.0.0

# ⭐ 滚动更新状态
kubectl rollout status deployment/web-deployment

# ⭐ 回滚
kubectl rollout undo deployment/web-deployment         # 回滚到上一个版本
kubectl rollout undo deployment/web-deployment --to-revision=2  # 回滚到指定版本
kubectl rollout history deployment/web-deployment       # 查看历史版本
```

### Service ⭐

Service 提供稳定的网络端点访问 Pod。

```yaml
# service.yaml
apiVersion: v1
kind: Service
metadata:
  name: web-service
spec:
  # ⭐ 类型
  type: ClusterIP    # 集群内可访问（默认）
  # type: NodePort   # 每个 Node 的端口访问
  # type: LoadBalancer  # 云厂商 LB

  selector:
    app: web

  ports:
    - port: 80           # Service 端口
      targetPort: 3000   # Pod 端口
      nodePort: 30080    # NodePort 类型的节点端口（30000-32767）
      protocol: TCP
```

```bash
# Service 操作
kubectl apply -f service.yaml
kubectl get svc
kubectl describe svc web-service

# 访问服务
# ClusterIP: curl http://web-service:80（集群内部）
# NodePort:  curl http://<node-ip>:30080
# LoadBalancer: 使用云厂商提供的外部 IP

# ⭐ 临时端口转发（调试用）
kubectl port-forward service/web-service 8080:80
# 然后访问 http://localhost:8080
```

### ConfigMap & Secret

```yaml
# configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  # 键值对
  NODE_ENV: "production"
  LOG_LEVEL: "info"

  # 配置文件内容
  nginx.conf: |
    server {
      listen 80;
      location / {
        proxy_pass http://localhost:3000;
      }
    }
```

```yaml
# secret.yaml（值需要 base64 编码）
apiVersion: v1
kind: Secret
metadata:
  name: app-secret
type: Opaque
data:
  DB_PASSWORD: cGFzc3dvcmQxMjM=        # echo -n "password123" | base64
  API_KEY: YXBpLWtleS14eHg=

# 或者用 kubectl 创建（自动编码）
# kubectl create secret generic app-secret \
#   --from-literal=DB_PASSWORD=password123
```

```yaml
# 在 Pod 中使用 ConfigMap 和 Secret
apiVersion: v1
kind: Pod
metadata:
  name: config-pod
spec:
  containers:
    - name: app
      image: my-app:latest

      # 方式一：环境变量
      envFrom:
        - configMapRef:
            name: app-config
        - secretRef:
            name: app-secret

      # 方式二：指定变量
      env:
        - name: DB_HOST
          value: postgres-service
        - name: DB_PASSWORD
          valueFrom:
            secretKeyRef:
              name: app-secret
              key: DB_PASSWORD

      # 方式三：挂载为文件
      volumeMounts:
        - name: config-volume
          mountPath: /etc/config
          readOnly: true
  volumes:
    - name: config-volume
      configMap:
        name: app-config
```

### Ingress ⭐

Ingress 将外部 HTTP/HTTPS 流量路由到集群内 Service。

```yaml
# ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: my-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
    kubernetes.io/ingress.class: nginx
spec:
  rules:
    # ⭐ 基于主机名路由
    - host: api.myapp.com
      http:
        paths:
          - path: /v1
            pathType: Prefix
            backend:
              service:
                name: api-v1-service
                port:
                  number: 80
          - path: /v2
            pathType: Prefix
            backend:
              service:
                name: api-v2-service
                port:
                  number: 80

    - host: admin.myapp.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: admin-service
                port:
                  number: 80

  # ⭐ TLS 配置
  tls:
    - hosts:
        - api.myapp.com
        - admin.myapp.com
      secretName: myapp-tls
```

### PersistentVolume & PersistentVolumeClaim

```yaml
# pv.yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: my-pv
spec:
  capacity:
    storage: 10Gi
  accessModes:
    - ReadWriteOnce     # 单节点读写
    # - ReadOnlyMany    # 多节点只读
    # - ReadWriteMany   # 多节点读写
  persistentVolumeReclaimPolicy: Retain   # 释放后保留
  storageClassName: standard
  hostPath:
    path: /data/pv
---
# pvc.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: my-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 5Gi
  storageClassName: standard
```

```yaml
# 在 Pod 中使用 PVC
apiVersion: apps/v1
kind: Deployment
metadata:
  name: postgres
spec:
  template:
    spec:
      containers:
        - name: postgres
          image: postgres:16-alpine
          volumeMounts:
            - name: data
              mountPath: /var/lib/postgresql/data
      volumes:
        - name: data
          persistentVolumeClaim:
            claimName: my-pvc
```

---

## 八、Kubernetes 进阶

### Namespace

```yaml
# namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: production
```

```bash
# Namespace 操作
kubectl create namespace staging
kubectl get namespaces
kubectl get pods -n production
kubectl config set-context --current --namespace=production  # 切换默认 ns

# ⭐ 资源限额
# ResourceQuota
kubectl create quota my-quota --hard=cpu=10,memory=20G,pods=10 -n production
```

### HorizontalPodAutoscaler（HPA）⭐

```yaml
# hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: web-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: web-deployment
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 80
```

### Helm ⭐

**Helm** 是 K8s 的包管理器，使用 Chart 打包和管理应用。

```bash
# 安装 Helm
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# ⭐ 仓库管理
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
helm repo list

# ⭐ 安装 Chart
helm install my-release bitnami/nginx
helm install my-release bitnami/postgresql --set auth.database=myapp

# ⭐ 自定义 values
helm install my-release bitnami/nginx -f values.yaml
helm install my-release bitnami/nginx --set replicaCount=3

# ⭐ 管理 Releases
helm list                               # 列出已安装
helm upgrade my-release bitnami/nginx   # 升级
helm rollback my-release 1              # 回滚
helm uninstall my-release               # 卸载

# ⭐ 创建自己的 Chart
helm create my-chart
# my-chart/
# ├── Chart.yaml              # Chart 元数据
# ├── values.yaml             # 默认配置值
# ├── templates/              # K8s 资源模板（Go template）
# │   ├── deployment.yaml
# │   ├── service.yaml
# │   ├── _helpers.tpl        # 辅助模板
# │   └── NOTES.txt           # 安装后提示
# └── charts/                 # 依赖的子 Chart
```

### Kustomize（kubectl 原生）

```bash
# Kustomize 无需安装，kubectl 内置
```

```yaml
# kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

# ⭐ 基础资源
resources:
  - deployment.yaml
  - service.yaml

# ⭐ 命名空间前缀
namePrefix: prod-

# ⭐ 通用标签
commonLabels:
  app: my-app
  env: production

# ⭐ 镜像替换
images:
  - name: my-app
    newTag: v2.0.0

# ⭐ 配置映射生成
configMapGenerator:
  - name: app-config
    literals:
      - NODE_ENV=production
      - LOG_LEVEL=info
```

```bash
# 使用 Kustomize
kubectl apply -k ./
kubectl kustomize ./overlays/production
```

---

## 九、K8s 网络模型

```
                          Internet
                             │
                       [Ingress]
                             │
                      [Service] (ClusterIP)
                             │
              ┌──────────────┼──────────────┐
              │              │              │
          [Pod:80]      [Pod:80]      [Pod:80]
              │              │              │
        (Container)    (Container)    (Container)
```

### 网络插件（CNI）

```bash
# ⭐ Calico（最常用，支持网络策略）
kubectl apply -f https://raw.githubusercontent.com/projectcalico/calico/master/manifests/calico.yaml

# Flannel（简单，适合小集群）
kubectl apply -f https://raw.githubusercontent.com/flannel-io/flannel/master/Documentation/kube-flannel.yml

# Cilium（基于 eBPF，性能强）
helm repo add cilium https://helm.cilium.io/
helm install cilium cilium/cilium --namespace kube-system
```

### NetworkPolicy

```yaml
# network-policy.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: api-allow
spec:
  podSelector:
    matchLabels:
      app: api
  policyTypes:
    - Ingress
    - Egress
  ingress:
    - from:
        - podSelector:
            matchLabels:
              app: web
        - namespaceSelector:
            matchLabels:
              name: monitoring
      ports:
        - port: 3000
  egress:
    - to:
        - podSelector:
            matchLabels:
              app: database
      ports:
        - port: 5432
```

---

## 十、监控与日志

### kubectl 排错 ⭐

```bash
# ⭐ 查看事件
kubectl get events --sort-by='.lastTimestamp'
kubectl get events -n production --watch

# ⭐ 查看 Pod 状态
kubectl get pods
kubectl describe pod <pod-name>      # 查看事件和状态详情
kubectl logs <pod-name> -c <container> # 多容器时指定容器

# ⭐ 节点状态
kubectl top nodes                    # 节点资源使用
kubectl top pods                     # Pod 资源使用

# ⭐ 进入容器调试
kubectl exec -it <pod-name> -- sh
kubectl exec -it <pod-name> -- cat /var/log/app.log

# ⭐ 临时调试 Pod
kubectl run debug --image=nicolaka/netshoot -it --rm -- bash
```

### 常用监控方案

| 方案 | 组件 | 说明 |
|:----:|:----:|:----:|
| **Prometheus + Grafana** | Prometheus（采集）、Grafana（可视化） | **行业标准** |
| **Metrics Server** | K8s 内置资源指标 | HPA 必备 |
| **Loki** | 轻量日志聚合 | Grafana 生态 |
| **ELK** | Elasticsearch + Logstash + Kibana | 传统日志方案 |
| **Datadog** | SaaS 全栈监控 | 商业方案 |

```bash
# ⭐ 安装 Prometheus Stack（推荐）
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install monitoring prometheus-community/kube-prometheus-stack -n monitoring --create-namespace

# 访问 Grafana
kubectl port-forward -n monitoring svc/monitoring-grafana 3000:80
# 默认账号: admin / prom-operator
```

---

## 十一、面试常见问题

### 1. Docker 和虚拟机有什么区别？

> Docker 是**进程级隔离**（共享宿主内核），虚拟机是**硬件级虚拟化**（独立 Guest OS）。Docker 启动更快（秒级 vs 分钟级），资源占用更小（MB vs GB），但隔离性比虚拟机弱。两者不是替代关系，而是互补。

### 2. Dockerfile 中 CMD 和 ENTRYPOINT 的区别？

> `CMD` 提供默认命令，可以被 `docker run` 后的参数覆盖。`ENTRYPOINT` 定义容器的入口程序，不可被覆盖（除非 `--entrypoint`）。常用组合：`ENTRYPOINT ["python"]` + `CMD ["app.py"]`，这样 `docker run my-image test.py` 会执行 `python test.py`。

### 3. 多阶段构建的优势？

> 多阶段构建可以在一个 Dockerfile 中使用多个 FROM 指令，每个 FROM 是一个独立的构建阶段。最终镜像只包含最后一个阶段的内容，**显著减小镜像体积**（例如 Go 应用从 1GB+ 减少到 10MB），且不包含构建工具和中间文件。

### 4. Kubernetes 中 Pod 和 Deployment 的关系？

> **Pod** 是最小部署单元，封装一个或多个容器。**Deployment** 管理 Pod 的副本、更新和回滚。通常不直接创建 Pod，而是通过 Deployment 声明期望状态，由 Deployment Controller 自动维持 Pod 数量。

### 5. Service 有哪些类型？

> **ClusterIP**（默认）：集群内部可访问。**NodePort**：在每个节点上暴露端口。**LoadBalancer**：云厂商提供外部负载均衡器。**ExternalName**：通过 DNS CNAME 映射到外部地址。

### 6. ConfigMap 和 Secret 的区别？

> ConfigMap 存储非敏感配置（明文），Secret 存储敏感信息（Base64 编码）。Secret 有更严格的访问控制，etcd 中可加密存储。使用时都可以作为环境变量或挂载文件。

### 7. 滚动更新和回滚的原理？

> RollingUpdate 策略会逐步替换 Pod：先将新版本的 Pod 启动并等待就绪，然后停止旧版本的 Pod。通过 `maxSurge`（最多超出多少个新 Pod）和 `maxUnavailable`（最多允许多少个旧 Pod 不可用）控制更新速率。如果新版异常，`kubectl rollout undo` 可以快速回滚到上一个版本。

### 8. 如何实现零停机部署？

> 需要同时满足：1）Deployment 设置 `maxUnavailable: 0` 和 `maxSurge: 1`；2）Pod 配置 `readinessProbe`（确保新 Pod 就绪才接流量）；3）Service 的 `targetPort` 指向正确的端口；4）Ingress 控制器支持优雅的流量切换。

### 9. Pod 的生命周期有哪些状态？

> **Pending**：等待调度或镜像拉取。**Running**：至少一个容器在运行。**Succeeded**：所有容器成功退出（Job）。**Failed**：容器异常退出。**CrashLoopBackOff**：容器反复崩溃。**ImagePullBackOff**：镜像拉取失败。

### 10. 如何在 K8s 中管理数据库有状态应用？

> 使用 **StatefulSet** 而非 Deployment。StatefulSet 提供稳定的网络标识（pod-name-0、pod-name-1）、稳定的持久化存储（每个 Pod 独立的 PVC）、有序的部署和伸缩。配合 **Headless Service** 实现 Pod 间的直接通信。

---

> [!tip] **学习路径建议**
> 1. **Docker 入门**：安装 → 基本命令 → Dockerfile → docker-compose
> 2. **Docker 进阶**：多阶段构建 → 网络 → 数据卷 → 安全
> 3. **K8s 入门**：minikube → kubectl → Pod → Deployment → Service
> 4. **K8s 进阶**：ConfigMap/Secret → Ingress → HPA → Helm
> 5. **K8s 深入**：网络策略 → StatefulSet → Operator → 监控
