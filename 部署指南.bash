安装依赖
# 1. 安装系统工具（IPMI/SNMP扫描必需）
sudo apt-get update
sudo apt-get install -y ipmitool snmp

# 2. 安装Docker（如果未安装）
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo systemctl enable docker
sudo systemctl start docker

构建并启动服务
# 1. 创建项目目录
mkdir -p monitor-platform/data
cd monitor-platform

# 2. 下载代码（复制上面所有文件到本地）
# （此处假设您已将代码放入当前目录）

# 3. 构建Docker镜像
docker build -t monitor-platform .

# 4. 启动容器（包含数据库）
docker run -d -p 8000:8000 -v $(pwd)/data:/app/data monitor-platform


验证运行
# 1. 检查容器状态
docker ps | grep monitor-platform

# 2. 测试API（在浏览器或curl中）
curl -X 'POST' \
  'http://localhost:8000/devices/discover' \
  -H 'Content-Type: application/json' \
  -d '{"network": "192.168.1.0/24"}'

# 3. 查看告警
curl http://localhost:8000/alerts
# 返回示例：[{"device_ip":"192.168.1.100","metric":{"cpu":82,"memory":88},"severity":"P1"}]

关键功能演示
1. 批量添加设备（通过CSV）
上传文件
ip,protocol,username,password,group
192.168.1.100,ipmi,admin,password,Web-Servers
192.168.1.101,snmp,public,public,DB-Cluster

API请求：
curl -X 'POST' \
  'http://localhost:8000/devices/batch_add' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@devices.csv'

  自动发现设备
  运行扫描
  curl -X 'POST' \
  'http://localhost:8000/devices/discover' \
  -H 'Content-Type: application/json' \
  -d '{"network": "192.168.1.0/24"}'
