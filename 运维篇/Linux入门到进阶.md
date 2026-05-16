# Linux 入门到进阶

## 一、Linux 概述

### 什么是 Linux

**Linux** 是一个开源的类 Unix 操作系统内核，由 Linus Torvalds 于 1991 年创建。Linux 被广泛用于服务器、嵌入式系统、超级计算机和移动设备（Android）。

### Linux 发行版

```
发行版家族树
┌────────────────────────────────┐
│            Linux 内核           │
└────────────┬───────────────────┘
             │
    ┌────────┴────────┐
    │                 │
  Debian 系         Red Hat 系
    │                 │
├─ Debian         ├─ RHEL（企业版）
├─ Ubuntu         ├─ CentOS（已停止）
├─ Linux Mint     ├─ Rocky Linux
├─ Kali Linux     ├─ AlmaLinux
│                 └─ Fedora
│                 │
              SUSE 系
                ├─ OpenSUSE
                └─ SLES
```

| 发行版 | 适合场景 | 包管理器 | 说明 |
|:------:|:--------:|:--------:|:----:|
| **Ubuntu** | 桌面/服务器 | `apt` | **初学者首选**，文档丰富 |
| **Debian** | 服务器 | `apt` | 稳定，服务器广泛使用 |
| **CentOS Stream** | 服务器 | `dnf/yum` | 介于 RHEL 和 Fedora 之间 |
| **Rocky Linux** | 服务器 | `dnf/yum` | CentOS 替代品 |
| **Fedora** | 桌面/开发者 | `dnf` | 新技术尝鲜 |
| **Alpine** | 容器 | `apk` | **极小体积**，Docker 常用 |

> [!tip] **学习推荐**：服务器用 **Ubuntu LTS** 或 **Debian**，Docker 容器用 **Alpine**。

### 快速连接服务器

```bash
# SSH 连接
ssh user@server-ip
ssh -p 2222 user@server-ip          # 指定端口
ssh -i ~/.ssh/id_rsa user@server-ip # 使用密钥

# SSH 配置（简化连接）
# ~/.ssh/config
Host myserver
    HostName 192.168.1.100
    User root
    Port 22
    IdentityFile ~/.ssh/id_rsa

# 之后可以直接: ssh myserver
```

---

## 二、文件系统与目录结构

### Linux 目录结构

```
/ ───────── 根目录，一切从这里开始
├── bin/    系统命令（二进制文件，如 ls、cp）
├── sbin/   系统管理命令（如 fdisk、mkfs）
├── etc/    ⭐ 配置文件（最重要的目录之一）
├── var/    可变数据（日志、缓存、数据库）
│   ├── log/    系统日志
│   ├── lib/    数据库文件
│   └── tmp/    临时文件
├── usr/    用户程序和数据
│   ├── bin/    用户命令
│   ├── lib/    库文件
│   ├── local/  用户安装的程序（编译安装）
│   └── share/  共享数据
├── home/   ⭐ 用户家目录（/home/username）
├── root/    root 用户家目录
├── opt/     第三方软件
├── tmp/     临时文件（重启后清理）
├── dev/     设备文件（硬盘、终端等）
├── proc/    ⭐ 虚拟文件系统（运行中进程信息）
├── sys/     内核相关信息
├── media/   可移动媒体挂载点
├── mnt/     临时挂载点
└── boot/    启动文件（内核、grub）
```

### 文件类型

```bash
ls -la                                  # 查看文件详细信息

# 文件类型标识（第一个字符）
# -  普通文件
# d  目录
# l  符号链接
# c  字符设备（如 /dev/tty）
# b  块设备（如 /dev/sda）
# s  套接字（socket）
# p  命名管道（pipe）

# 硬链接 vs 软链接
ln file1 link1                          # 硬链接（同一 inode，不能跨文件系统）
ln -s /path/to/file symlink             # 软链接（类似快捷方式，可跨文件系统）
```

---

## 三、常用命令 ⭐

### 文件操作

```bash
# ⭐ 列出文件
ls                      # 列出当前目录
ls -l                   # 详细信息（权限、大小、日期）
ls -a                   # 显示隐藏文件（以 . 开头）
ls -lh                  # 人性化大小显示（KB/MB）
ls -lt                  # 按时间排序
ls -lS                  # 按大小排序
ls -R                   # 递归显示子目录

# ⭐ 目录切换
pwd                     # 显示当前路径
cd /home/user           # 切换到指定目录
cd ..                   # 上级目录
cd ~                    # 家目录
cd -                    # 上一个目录

# ⭐ 文件操作
touch file.txt          # 创建空文件或更新文件时间
cp file1 file2          # 复制文件
cp -r dir1 dir2         # 递归复制目录
mv file1 file2          # 移动或重命名
rm file.txt             # 删除文件
rm -rf dir/             # ⚠️ 强制递归删除（极其危险！）
rm -i file.txt          # 交互式删除（确认）

# ⭐ 查看文件
cat file.txt            # 显示全部内容
less file.txt           # 分页查看（上下翻页，q 退出）
more file.txt           # 分页查看（只能下翻）
head -n 10 file.txt     # 前 10 行
tail -n 10 file.txt     # 后 10 行
tail -f file.txt        # ⭐ 实时跟踪（日志监控利器）

# ⭐ 创建目录
mkdir dir               # 创建目录
mkdir -p a/b/c/d        # 递归创建

# ⭐ 查找文件
find / -name "file.txt" # 按名称查找（全盘搜索）
find . -name "*.log"    # 当前目录下所有 .log 文件
find /var -size +100M   # 大于 100MB 的文件
find . -mtime -1        # 最近 1 天内修改的文件
find . -type d          # 只查找目录
find . -exec rm {} \;   # 对找到的文件执行操作

# locate（更快，需要先 updatedb）
locate nginx.conf       # 基于数据库搜索
```

### 文本处理 ⭐

```bash
# ⭐ grep：搜索文本内容
grep "pattern" file.txt                 # 搜索关键词
grep -i "pattern" file.txt              # 忽略大小写
grep -r "pattern" /path/                # 递归搜索目录
grep -n "pattern" file.txt              # 显示行号
grep -v "pattern" file.txt              # 反向匹配（不包含的）
grep -c "pattern" file.txt              # 计数
grep "error\|warning" log.txt           # 多条件（或）
grep -E "error|warning" log.txt         # 扩展正则
grep "error" *.log --color              # 高亮显示

# ⭐ sed：流编辑器
sed 's/old/new/' file.txt               # 替换第一个匹配
sed 's/old/new/g' file.txt              # 全局替换
sed -i 's/old/new/g' file.txt           # 直接修改文件
sed '/pattern/d' file.txt               # 删除匹配行
sed -n '10,20p' file.txt                # 打印 10-20 行

# ⭐ awk：文本分析工具
awk '{print $1, $3}' file.txt           # 打印第1、3列
awk '{sum+=$1} END {print sum}' file.txt # 求和
awk '/error/ {print}' log.txt           # 过滤并打印
awk -F: '{print $1}' /etc/passwd        # 指定分隔符

# ⭐ sort & uniq
sort file.txt                           # 排序
sort -n file.txt                        # 按数字排序
sort -r file.txt                        # 逆序
sort -u file.txt                        # 排序并去重
sort file.txt | uniq                    # 去重（相邻重复）
sort file.txt | uniq -c                 # 统计重复次数
sort file.txt | uniq -d                 # 显示重复行

# ⭐ 管道组合（⭐ 核心能力）
cat access.log | grep "ERROR" | awk '{print $1}' | sort | uniq -c | sort -nr

# 查看最耗 CPU 的进程
ps aux | sort -nrk 3 | head -5

# 统计 IP 访问次数
cat access.log | awk '{print $1}' | sort | uniq -c | sort -nr | head -10
```

### 压缩与归档

```bash
# ⭐ tar
tar -cvf archive.tar dir/              # 打包（不压缩）
tar -xvf archive.tar                    # 解包
tar -czvf archive.tar.gz dir/           # 打包并 gzip 压缩
tar -xzvf archive.tar.gz                # 解压
tar -cjvf archive.tar.bz2 dir/          # bzip2 压缩
tar -xzvf archive.tar.gz -C /target     # 解压到指定目录

# gzip / gunzip
gzip file.txt                           # 压缩（生成 file.txt.gz）
gunzip file.txt.gz                      # 解压
gzip -d file.txt.gz                     # 解压

# zip / unzip
zip -r archive.zip dir/                 # 压缩
unzip archive.zip                       # 解压
unzip archive.zip -d /target            # 解压到指定目录
```

---

## 四、权限管理 ⭐

### 文件权限

```bash
# 权限表示
-rwxr-xr--  1 user group  1024  May 10 10:00 script.sh
^^^^^^^^^^^^
│││││││││
││││││││└─ other 权限（读）
│││││││└── other 权限（执行）
││││││└─── other 权限（写）
│││││└──── group 权限（读）
││││└───── group 权限（执行）
│││└────── group 权限（写）
││└─────── owner 权限（读）
│└──────── owner 权限（执行）
└───────── owner 权限（写）
│
└──── 文件类型（- 普通文件，d 目录，l 链接）

# 权限数字表示
# r=4, w=2, x=1
# rwx = 7, r-x = 5, r-- = 4, --- = 0

chmod 755 script.sh                     # rwxr-xr-x（常用）
chmod 644 file.txt                      # rw-r--r--（常用）
chmod 700 private.sh                    # rwx------（仅自己）

chmod u+x script.sh                     # 给所有者加执行权限
chmod g-w file.txt                      # 去掉组写权限
chmod o+r file.txt                      # 给其他人加读权限
chmod -R 755 dir/                       # 递归修改目录权限

chown user:group file.txt               # 修改所有者和组
chown -R user:group dir/                # 递归修改
chgrp group file.txt                    # 仅修改组
```

### 特殊权限

```bash
# SUID（4xxx）：运行时临时获得文件所有者的权限
chmod u+s /usr/bin/passwd              # passwd 运行时获得 root 权限

# SGID（2xxx）：运行时获得文件所属组的权限
chmod g+s dir/                          # 目录下新建文件继承组

# Sticky Bit（1xxx）：仅文件所有者可删除
chmod +t /tmp                           # /tmp 目录（防止用户删别人的文件）

# umask：默认权限掩码
umask                                    # 查看当前 umask
umask 022                                # 文件默认 644，目录默认 755
```

### 用户与组管理

```bash
# ⭐ 用户管理
useradd -m username                     # 创建用户并创建家目录
userdel -r username                     # 删除用户并删除家目录
passwd username                         # 设置或修改密码
usermod -aG groupname username          # 将用户添加到组

# ⭐ 组管理
groupadd groupname                      # 创建组
groupdel groupname                      # 删除组
groups username                         # 查看用户所属组

# 查看用户
whoami                                  # 当前用户名
id                                      # 查看 uid/gid
who                                     # 当前登录的用户
w                                       # 当前登录用户详细信息
last                                    # 最近登录记录
```

### sudo 权限

```bash
# ⭐ 编辑 sudo 配置（用 visudo，不要直接编辑）
visudo                                  # 安全编辑 /etc/sudoers

# 用户有完整 sudo 权限
username ALL=(ALL:ALL) ALL

# 用户组有完整 sudo 权限
%admin ALL=(ALL) ALL

# 特定命令免密码
username ALL=(ALL) NOPASSWD: /usr/bin/systemctl

# 常用 sudo 操作
sudo command                            # 以 root 执行
sudo -u username command                # 以指定用户执行
sudo -i                                 # 切换到 root shell
sudo -s                                 # 以 root shell（保留当前环境）
```

---

## 五、进程管理

```bash
# ⭐ 查看进程
ps aux                                  # 所有进程详细信息
ps -ef                                  # 标准格式
ps aux | grep nginx                     # 搜索指定进程

top                                     # 实时进程监控（按 q 退出）
htop                                    # top 增强版（需要安装）

# ⭐ 进程信号
kill -l                                # 列出所有信号（共 64 个）
kill -15 PID                            # SIGTERM：优雅终止（默认）
kill -9 PID                             # SIGKILL：强制杀死
kill -2 PID                             # SIGINT：Ctrl+C 中断

pkill nginx                             # 按进程名杀死
killall nginx                           # 杀死所有同名进程

# ⭐ 进程优先级
nice -n -5 command                      # 以更高优先级启动
renice -n -5 -p PID                     # 修改运行中进程优先级

# ⭐ 后台运行
command &                               # 后台运行
nohup command &                         # 即使退出终端也继续运行
nohup command > output.log 2>&1 &       # 日志重定向 + 后台
jobs                                    # 查看后台任务
fg %1                                  # 将后台任务调到前台
bg %1                                  # 将前台任务调到后台
Ctrl + Z                                # 暂停当前任务放到后台

# ⭐ systemd 服务管理
systemctl start nginx                   # 启动服务
systemctl stop nginx                    # 停止服务
systemctl restart nginx                 # 重启服务
systemctl reload nginx                  # 重载配置（不中断服务）
systemctl status nginx                  # 查看服务状态
systemctl enable nginx                  # 开机自启
systemctl disable nginx                 # 禁用开机自启
systemctl is-active nginx               # 检查是否运行中
systemctl list-units --type=service     # 列出所有服务

# journalctl（查看 systemd 日志）
journalctl -u nginx                     # 查看 nginx 服务日志
journalctl -u nginx -f                  # 实时跟踪
journalctl --since "1 hour ago"         # 最近 1 小时
journalctl -u nginx --since today       # 今天的日志
```

---

## 六、网络管理 ⭐

### 网络配置

```bash
# ⭐ 查看网络信息
ip addr                                 # IP 地址（替代 ifconfig）
ip route                                # 路由表（替代 route -n）
ip link                                 # 网络接口
ip neigh                                # ARP 表

# 传统命令
ifconfig                                # 网络接口信息
netstat -tulpn                          # 监听端口和进程
ss -tulpn                               # netstat 的现代替代（更快）

# ⭐ 网络连接测试
ping -c 4 google.com                    # ping（4 次）
ping -i 0.5 192.168.1.1                 # 0.5 秒间隔

# ⭐ DNS 查询
nslookup example.com                    # DNS 查询
dig example.com                         # 详细 DNS 信息
host example.com                        # 简化 DNS 查询

# ⭐ 网络诊断
traceroute google.com                   # 追踪路由路径
mtr google.com                          # traceroute + ping 结合
curl -I https://example.com             # HTTP 头部测试
wget -q -O- http://example.com          # 下载并输出到 stdout

# ⭐ 端口检测
nc -zv 192.168.1.1 22                   # TCP 端口检测
nc -zv -w 3 192.168.1.1 1-1000         # 扫描端口范围
telnet 192.168.1.1 80                   # 连接测试
```

### 防火墙

```bash
# ⭐ ufw（Ubuntu 默认）
ufw enable                              # 启用防火墙
ufw disable                             # 禁用
ufw status verbose                      # 查看规则
ufw default deny incoming               # 默认拒绝入站
ufw default allow outgoing              # 默认允许出站
ufw allow 22/tcp                        # 开放 SSH 端口
ufw allow 80/tcp                        # 开放 HTTP
ufw allow 443/tcp                       # 开放 HTTPS
ufw allow from 192.168.1.0/24           # 允许特定网段
ufw deny 3306                           # 拒绝 MySQL 端口
ufw delete allow 80                     # 删除规则
ufw app list                            # 查看应用配置

# ⭐ firewalld（CentOS/RHEL）
firewall-cmd --list-all                 # 查看所有规则
firewall-cmd --add-port=80/tcp          # 开放端口（临时）
firewall-cmd --permanent --add-port=80/tcp  # 永久开放
firewall-cmd --reload                   # 重载配置
firewall-cmd --zone=public --add-service=http  # 开放 HTTP 服务
```

### 网络文件传输

```bash
# ⭐ scp（SSH 传输）
scp file.txt user@server:/path/         # 上传本地文件到服务器
scp user@server:/path/file.txt ./       # 下载服务器文件到本地
scp -r dir/ user@server:/path/          # 递归复制目录
scp -P 2222 file.txt user@server:/path/ # 指定端口

# ⭐ rsync（增量同步）
rsync -avz dir/ user@server:/path/      # 同步目录到服务器
rsync -avz user@server:/path/ ./        # 从服务器同步到本地
rsync -avz --delete dir/ user@server:/path/  # 删除目标端多余文件
# 常用参数：-a（归档）、-v（详细）、-z（压缩）、--progress（进度）
```

---

## 七、磁盘与存储管理

```bash
# ⭐ 查看磁盘
lsblk                                   # 列出块设备
fdisk -l                                # 查看磁盘分区
df -h                                   # 查看磁盘使用情况（⭐ 常用）
du -sh dir/                             # 查看目录总大小
du -h --max-depth=1 /home               # 一级目录大小

# ⭐ 磁盘分区
fdisk /dev/sda                          # 分区工具（MBR）
gdisk /dev/sda                          # GPT 分区
parted /dev/sda                         # 高级分区工具

# ⭐ 挂载
mount /dev/sdb1 /mnt/data               # 挂载分区
umount /mnt/data                        # 卸载
mount -a                                # 挂载 /etc/fstab 中的所有

# 开机自动挂载（/etc/fstab）
# /dev/sdb1  /mnt/data  ext4  defaults  0  2

# ⭐ LVM（逻辑卷管理）
pvcreate /dev/sdb                       # 创建物理卷
vgcreate vg_data /dev/sdb               # 创建卷组
lvcreate -L 100G -n lv_data vg_data     # 创建逻辑卷
mkfs.ext4 /dev/vg_data/lv_data          # 格式化
mount /dev/vg_data/lv_data /mnt/data    # 挂载

lvextend -L +50G /dev/vg_data/lv_data   # 扩展逻辑卷
resize2fs /dev/vg_data/lv_data          # 调整文件系统大小
```

---

## 八、Shell 脚本 ⭐

### 基础语法

```bash
#!/bin/bash
# ⭐ 第一行：Shebang，指明解释器

# ⭐ 变量
name="World"
echo "Hello, $name!"                    # 变量引用
echo "Hello, ${name}!"                  # 带花括号（推荐）
readonly PI=3.14159                     # 只读变量
unset name                              # 删除变量

# ⭐ 位置参数
echo "脚本名: $0"
echo "第一个参数: $1"
echo "所有参数: $@"
echo "参数个数: $#"

# ⭐ 特殊变量
$?                                      # 上一条命令的退出码（0=成功）
$$                                      # 当前脚本的 PID
$!                                      # 最后一个后台命令的 PID

# ⭐ 数组
fruits=("apple" "banana" "orange")
echo ${fruits[0]}                       # apple
echo ${fruits[@]}                       # 所有元素
echo ${#fruits[@]}                      # 数组长度
```

### 运算符

```bash
# ⭐ 算术运算
a=10
b=3
echo $((a + b))                         # 13
echo $((a - b))                         # 7
echo $((a * b))                         # 30
echo $((a / b))                         # 3（整数除法）
echo $((a % b))                         # 1
echo $((a ** 2))                        # 100（幂运算）
let c=a+b                               # let 命令

# ⭐ 字符串比较
[[ "$str1" == "$str2" ]]                # 相等
[[ "$str1" != "$str2" ]]                # 不等
[[ -z "$str" ]]                         # 空字符串
[[ -n "$str" ]]                         # 非空字符串

# ⭐ 数字比较
(( a > b ))
[[ $a -gt $b ]]                         # 大于（-gt）
[[ $a -ge $b ]]                         # 大于等于（-ge）
[[ $a -lt $b ]]                         # 小于（-lt）
[[ $a -le $b ]]                         # 小于等于（-le）
[[ $a -eq $b ]]                         # 等于（-eq）
[[ $a -ne $b ]]                         # 不等于（-ne）

# ⭐ 文件测试
[[ -f "$file" ]]                        # 是普通文件
[[ -d "$dir" ]]                         # 是目录
[[ -e "$path" ]]                        # 存在
[[ -r "$file" ]]                        # 可读
[[ -w "$file" ]]                        # 可写
[[ -x "$file" ]]                        # 可执行
[[ -s "$file" ]]                        # 文件非空
[[ -L "$file" ]]                        # 是符号链接
```

### 流程控制

```bash
# ⭐ if / elif / else
if [[ $score -ge 90 ]]; then
    echo "优秀"
elif [[ $score -ge 60 ]]; then
    echo "及格"
else
    echo "不及格"
fi

# ⭐ for 循环
# 方式一：列表
for i in 1 2 3 4 5; do
    echo "Number: $i"
done

# 方式二：序列
for i in {1..5}; do
    echo "Number: $i"
done

# 方式三：C 风格
for ((i=0; i<5; i++)); do
    echo "i = $i"
done

# 方式四：文件遍历
for file in /var/log/*.log; do
    echo "Processing: $file"
done

# ⭐ while 循环
count=0
while [[ $count -lt 5 ]]; do
    echo "Count: $count"
    ((count++))
done

# ⭐ until 循环（条件为假时执行）
until [[ $count -ge 5 ]]; do
    echo "Count: $count"
    ((count++))
done

# ⭐ case 分支
case "$1" in
    start)
        echo "Starting..."
        ;;
    stop)
        echo "Stopping..."
        ;;
    restart|reload)
        echo "Restarting..."
        ;;
    *)
        echo "Usage: $0 {start|stop|restart}"
        exit 1
        ;;
esac
```

### 函数

```bash
# ⭐ 定义函数
function info() {
    echo "[INFO] $1"
}

warn() {
    echo "[WARN] $1"
}

error() {
    echo "[ERROR] $1" >&2
    exit 1
}

# ⭐ 使用函数
info "开始部署"
warn "配置文件不存在，使用默认配置"

# ⭐ 函数返回值
is_running() {
    pgrep -x "$1" > /dev/null && return 0 || return 1
}

if is_running "nginx"; then
    info "Nginx 正在运行"
fi
```

### 完整脚本示例 ⭐

```bash
#!/bin/bash
#
# ⭐ 系统信息收集脚本
# 用法: ./sysinfo.sh [output-file]
#

set -euo pipefail                        # 安全模式
# -e: 出错即退出
# -u: 未定义变量视为错误
# -o pipefail: 管道中任一命令失败整体失败

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'                             # No Color

# 日志函数
log_info() {
    echo -e "${GREEN}[INFO]${NC} $(date '+%Y-%m-%d %H:%M:%S') - $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $(date '+%Y-%m-%d %H:%M:%S') - $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $(date '+%Y-%m-%d %H:%M:%S') - $1" >&2
}

# 清理函数（脚本退出时执行）
cleanup() {
    log_info "清理临时文件..."
    [[ -f /tmp/sysinfo.tmp ]] && rm -f /tmp/sysinfo.tmp
}

trap cleanup EXIT

# 主函数
main() {
    local output="${1:-/tmp/sysinfo.txt}"
    log_info "开始收集系统信息..."

    {
        echo "===== 系统信息 ====="
        echo "主机名: $(hostname)"
        echo "操作系统: $(cat /etc/os-release | grep PRETTY_NAME | cut -d= -f2 | tr -d '\"')"
        echo "内核版本: $(uname -r)"
        echo "运行时间: $(uptime -p)"

        echo -e "\n===== CPU 信息 ====="
        echo "CPU 型号: $(grep 'model name' /proc/cpuinfo | head -1 | cut -d: -f2 | xargs)"
        echo "CPU 核心数: $(nproc)"
        echo "CPU 负载: $(uptime | awk -F'load average:' '{print $2}')"

        echo -e "\n===== 内存信息 ====="
        free -h | grep -v Swap

        echo -e "\n===== 磁盘信息 ====="
        df -h / /home /var 2>/dev/null

        echo -e "\n===== 网络信息 ====="
        ip -4 addr show | grep inet | awk '{print $2}'
        echo "默认网关: $(ip route | grep default | awk '{print $3}')"

        echo -e "\n===== 运行中的服务 ====="
        systemctl list-units --type=service --state=running --no-pager | head -20

    } > "$output"

    log_info "系统信息已保存到: $output"
}

# 执行主函数
main "$@"
```

---

## 九、软件包管理

### apt（Debian/Ubuntu）⭐

```bash
# ⭐ 更新包列表
sudo apt update

# ⭐ 升级系统
sudo apt upgrade                        # 升级所有包
sudo apt dist-upgrade                   # 升级包括依赖变更

# ⭐ 安装/卸载
sudo apt install nginx                  # 安装
sudo apt install -y nginx               # 自动确认
sudo apt remove nginx                   # 卸载（保留配置文件）
sudo apt purge nginx                    # 彻底卸载（含配置文件）
sudo apt autoremove                     # 清理不再需要的依赖包

# ⭐ 搜索
apt search nginx                        # 搜索软件包
apt show nginx                          # 显示包信息

# ⭐ 清理
sudo apt clean                          # 清理下载的包缓存
sudo apt autoclean                      # 清理过期的包缓存
```

### dnf（RHEL/Rocky/Alma）⭐

```bash
# CentOS/RHEL 8+ 使用 dnf（取代 yum）
sudo dnf update                         # 更新
sudo dnf install nginx                  # 安装
sudo dnf remove nginx                   # 卸载
sudo dnf search nginx                   # 搜索
sudo dnf info nginx                     # 查看信息
sudo dnf autoremove                     # 清理
sudo dnf groupinstall "Development Tools"  # 安装开发工具组
```

### apk（Alpine）

```bash
# Alpine Linux 包管理（Docker 镜像常用）
apk update                              # 更新索引
apk add nginx                           # 安装
apk del nginx                           # 卸载
apk info nginx                          # 查看信息
apk search nginx                        # 搜索
```

---

## 十、Vim 编辑器 ⭐

### 三种模式

```
Vim 的三种核心模式
┌──────────┐     i / a / o     ┌──────────┐
│  Normal  │ ──────────────►  │  Insert  │
│ (默认)   │ ◄──────────────  │ (编辑)   │
│ 浏览/操作 │     Esc / Ctrl+c │ 输入文本  │
└────┬─────┘                  └──────────┘
     │      : / / / ?
     ▼
┌──────────┐
│ Command  │
│ (命令行)  │
│ 保存/退出 │
│ 搜索/替换 │
└──────────┘
```

### 核心命令

```bash
# ⭐ Normal 模式（默认）
# 移动光标
h j k l           # 左 下 上 右
w b               # 下一个/上一个单词开头
e                 # 单词结尾
0 ^ $             # 行首(0/^)  / 行尾($)
gg G              # 文件开头 / 文件结尾
:n                # 跳转到第 n 行
Ctrl+f Ctrl+b     # 下一页 / 上一页

# 编辑操作
x                 # 删除光标处字符
dd                # 删除当前行
3dd               # 删除 3 行
dw                # 删除一个单词
d$ / d0           # 删除到行尾 / 行首
yy                # 复制当前行
3yy               # 复制 3 行
p                 # 粘贴到光标后
P                 # 粘贴到光标前
u                 # 撤销
Ctrl+r            # 重做
.                 # 重复上次操作

# ⭐ 搜索
/pattern          # 向下搜索
?pattern          # 向上搜索
n                 # 下一个匹配
N                 # 上一个匹配

# ⭐ Command 模式（按 : 进入）
:w                # 保存
:q                # 退出
:wq               # 保存并退出
:q!               # 强制退出（不保存）
:x                # 保存并退出（同 :wq）
:w !sudo tee %    # ⚡ 用 sudo 权限保存只读文件

:set nu           # 显示行号
:set nonu         # 隐藏行号
:syntax on        # 语法高亮

# ⭐ 替换
:%s/old/new/g            # 全文替换
:%s/old/new/gc           # 全文替换（逐个确认）
:1,10s/old/new/g         # 第 1-10 行替换

# 分屏
:sp file.txt      # 水平分屏
:vsp file.txt     # 垂直分屏
Ctrl+ww           # 切换窗口
Ctrl+wq           # 关闭当前窗口
```

---

## 十一、性能监控与调优

### 常用监控命令

```bash
# ⭐ CPU
top -bn1                               # 一次性输出
vmstat 1 5                             # 每 1 秒输出一次，共 5 次
mpstat -P ALL 1                        # 每个 CPU 核心使用率
lscpu                                  # CPU 详细信息

# ⭐ 内存
free -h                                # 内存使用情况
vmstat -s                              # 内存统计
cat /proc/meminfo                      # 详细内存信息

# ⭐ 磁盘 I/O
iostat -x 1                            # 磁盘 I/O 详细（需安装 sysstat）
iotop                                  # 实时磁盘 I/O（需安装）
dstat -d                               # 磁盘读写统计

# ⭐ 网络
iftop                                  # 实时带宽监控（需安装）
nethogs                                # 按进程查看带宽（需安装）
tcptrack                               # TCP 连接监控（需安装）

# ⭐ 综合监控
dstat -c -d -n -m                      # CPU + 磁盘 + 网络 + 内存
sar -u 1 3                             # 历史/实时 CPU 统计（sysstat）
sar -r 1 3                             # 内存统计
```

### 常用排查命令 ⭐

```bash
# 场景一：CPU 飙高
top -c                                 # 查看高 CPU 进程
ps -eo pid,ppid,cmd,%cpu,%mem --sort=-%cpu | head

# 场景二：内存不足
free -h
ps -eo pid,ppid,cmd,%mem --sort=-%mem | head
cat /proc/meminfo | grep -E "^(MemTotal|MemFree|MemAvailable|SwapTotal|SwapFree)"

# 场景三：磁盘空间满
df -h
du -sh /* 2>/dev/null | sort -rh | head -10
find / -type f -size +500M -exec ls -lh {} \; 2>/dev/null

# 场景四：端口被占
ss -tulpn | grep :80
lsof -i :80                            # 列出使用 80 端口的进程

# 场景五：连接数过多
ss -s                                  # 连接统计
ss -tan | awk '{print $5}' | sort | uniq -c | sort -nr | head
netstat -nat | awk '{print $6}' | sort | uniq -c | sort -nr

# 场景六：系统负载高
uptime                                 # 查看负载
dmesg -T | tail                        # 内核日志（看 OOM 等）
```

---

## 十二、Linux 面试常见问题

### 1. 硬链接和软链接的区别？

> **硬链接**共享同一个 inode，删除原文件不影响硬链接访问，不能跨文件系统。**软链接（符号链接）**有独立的 inode，类似于 Windows 快捷方式，原文件删除后软链接失效，可以跨文件系统。

### 2. 如何查找大文件？

> `find / -type f -size +100M -exec ls -lh {} \; 2>/dev/null` 或 `du -sh /* | sort -rh | head -10` 查看根目录下最大的目录。

### 3. Linux 的启动过程？

> BIOS/UEFI → 引导加载器（GRUB）→ 加载内核 → 启动 init 进程（systemd）→ 检测硬件 → 挂载文件系统 → 启动服务 → 启动登录管理器。

### 4. 什么是 inode？

> inode 是文件的**元数据**结构，存储文件的权限、所有者、大小、时间戳、数据块指针等信息。每个文件（或目录）都有一个唯一的 inode。`ls -i` 查看 inode 号。

### 5. 如何排查系统负载高？

> 1）`top` / `htop` 看 CPU 和内存；2）`iostat -x 1` 看磁盘 I/O；3）`vmstat 1` 看整体状况；4）`dmesg` 看内核日志；5）`ss -tan` 看网络连接；6）`strace -p PID` 跟踪系统调用。

### 6. crontab 如何配置定时任务？

> `crontab -e` 编辑：`* * * * * command`（分 时 日 月 周）。`crontab -l` 列出任务。`systemctl status cron` 检查服务状态。

### 7. swap 分区的作用？

> Swap 是磁盘上的交换空间，当物理内存不足时，将不活跃的内存页交换到磁盘。但严重依赖 swap 说明需要增加物理内存。`swapon -s` 查看 swap 使用情况。

### 8. Linux 文件权限中的 SUID、SGID、Sticky Bit？

> **SUID**（4）：程序运行时临时获得文件所有者的权限（如 passwd）。**SGID**（2）：目录下新建文件继承组。**Sticky Bit**（1）：/tmp 目录下用户只能删除自己的文件。

### 9. 如何配置静态 IP？

> Ubuntu（Netplan）：编辑 `/etc/netplan/*.yaml` 然后 `netplan apply`。
> RHEL：编辑 `/etc/sysconfig/network-scripts/ifcfg-eth0` 然后 `systemctl restart network`。

### 10. Linux 中的僵尸进程是什么？如何处理？

> 子进程结束后，父进程没有调用 `wait()` 回收其退出状态，子进程的进程表项仍然保留，即为**僵尸进程**。处理：1）`ps aux | grep Z` 找到僵尸进程；2）kill 其父进程（僵尸进程被 init 收养后自动清理）；3）检查父进程代码，修复未调用 `wait()` 的 bug。

---

> [!tip] **学习路径建议**
> 1. **入门**：安装 Linux → 基本命令（ls/cd/cp/mv/rm/cat）→ 文件权限
> 2. **基础**：Vim → 管道/grep/awk → 进程管理 → 用户管理
> 3. **进阶**：Shell 脚本 → 网络管理 → 磁盘管理 → systemd
> 4. **深入**：性能调优 → 安全配置 → iptables → SELinux
> 5. **实战**：搭建 LAMP/LEMP → 配置 Nginx → Docker 部署
