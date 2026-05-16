# Git 入门到进阶

## 一、Git 概述

### 什么是 Git

**Git** 是目前世界上最先进的**分布式版本控制系统**，由 Linus Torvalds 于 2005 年创建，用于管理 Linux 内核开发。

### 为什么需要 Git

| 问题 | Git 解决方式 |
|:----:|:------------:|
| ❌ 文件改来改去分不清版本 | ✅ **版本历史**，每次提交都可追溯 |
| ❌ 多人协作冲突不断 | ✅ **分支管理** + **合并策略** |
| ❌ 代码丢了找不回来 | ✅ **分布式**，每个人的本地都是完整仓库 |
| ❌ 想尝试新功能又怕搞乱 | ✅ **分支隔离**，不影响主线 |

### 集中式 vs 分布式

```
集中式（SVN）                   分布式（Git）
┌──────┐                       ┌──────┐ ┌──────┐ ┌──────┐
│ Server │                      │本地仓库│ │本地仓库│ │本地仓库│
│ 中央仓库 │   ▼ ▼ ▼             │ 完整  │ │ 完整  │ │ 完整  │
│        │ ────►  开发者         │ 历史  │ │ 历史  │ │ 历史  │
└────────┘     提交都依赖中央仓库  └──────┘ └──────┘ └──────┘
                离线不能工作       每个人都是完整的仓库
```

| 对比 | Git（分布式） | SVN（集中式） |
|:----:|:------------:|:-------------:|
| 架构 | 每个本地都是完整仓库 | 只有中央服务器有完整仓库 |
| 离线工作 | ✅ 完整功能 | ❌ 基本不能 |
| 分支 | **轻量分支**，秒级切换 | 分支是目录拷贝，很慢 |
| 速度 | 大部分操作在本地，极快 | 依赖网络速度 |
| 学习曲线 | 较高 | 较低 |

### Git 的三种状态

```
工作区（Working Directory）  ←── 实际文件
    │ git add
    ▼
暂存区（Staging Area / Index） ←── 下次要提交的内容
    │ git commit
    ▼
本地仓库（Repository） ←── 已经保存到数据库的版本
    │ git push
    ▼
远程仓库（Remote） ←── 远程服务器上的版本
```

### 基本配置

```bash
# ⭐ 必须配置（设置后显示提交者信息）
git config --global user.name "Your Name"
git config --global user.email "your@email.com"

# ⭐ 常用配置
git config --global init.defaultBranch main     # 默认分支名
git config --global core.autocrlf input         # 换行符处理（Mac/Linux）
git config --global core.autocrlf true          # Windows
git config --global core.editor vim             # 默认编辑器
git config --global color.ui auto               # 彩色输出
git config --global alias.co checkout           # 别名
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.st status
git config --global alias.lg "log --oneline --graph --all"  # ⭐ 最有用的别名

# 查看配置
git config --list                             # 所有配置
git config --global --list                    # 全局配置
git config user.name                          # 单个配置项

# 配置级别
# --system: 系统级（/etc/gitconfig）
# --global: 用户级（~/.gitconfig）
# --local:  仓库级（.git/config，默认）
```

---

## 二、基本操作 ⭐

### 创建仓库

```bash
# ⭐ 方式一：初始化新仓库
mkdir my-project && cd my-project
git init                                    # 创建 .git 目录

# ⭐ 方式二：克隆已有仓库
git clone https://github.com/user/repo.git          # HTTPS
git clone git@github.com:user/repo.git              # SSH（推荐）
git clone -b develop https://github.com/user/repo.git  # 克隆指定分支
git clone --depth 1 https://github.com/user/repo.git   # 浅克隆（只拉最新提交）
```

### 日常操作流程 ⭐

```bash
# ⭐ 查看状态
git status                                # 查看工作区、暂存区状态
git status -s                             # 简洁模式（M=修改, A=新增, ??=未跟踪）

# ⭐ 添加文件到暂存区
git add file.txt                          # 添加单个文件
git add .                                 # 添加所有文件（⚠️ 注意 .gitignore）
git add -A                                # 添加所有更改
git add -p                                # ⭐ 交互式添加（逐个区块确认）

# ⭐ 提交到本地仓库
git commit -m "feat: 添加用户登录功能"      # 提交并写信息
git commit -am "fix: 修复空指针异常"        # git add + git commit（仅对已跟踪文件）
git commit --amend -m "新的提交信息"        # 修改上次提交信息
git commit --amend --no-edit              # 不修改信息，补充文件到上次提交

# ⭐ 推送到远程
git push origin main                      # 推送到远程 main 分支
git push -u origin main                   # 首次推送并建立关联
git push --force                          # ⚠️ 强制推送（慎用！）
git push --force-with-lease               # ⭐ 更安全的强制推送

# ⭐ 拉取远程更新
git pull                                  # 拉取并合并（git fetch + git merge）
git pull --rebase                         # 拉取并变基（推荐，历史更干净）
git fetch                                 # 仅拉取，不自动合并
```

### 文件删除与移动

```bash
# ⭐ 删除文件
git rm file.txt                           # 从工作区和暂存区删除
git rm --cached file.txt                  # 仅从暂存区删除（保留工作区文件）
                                          # 相当于取消跟踪，配合 .gitignore 使用

# ⭐ 移动/重命名
git mv old.txt new.txt                    # 重命名文件
```

---

## 三、查看历史 ⭐

### git log

```bash
# ⭐ 基本查看
git log                                   # 完整历史
git log --oneline                         # 一行显示
git log --oneline --graph                 # ⭐ 分支图（最常用）
git log --oneline --graph --all           # 所有分支的历史

# ⭐ 格式化输出
git log --pretty=format:"%h - %an, %ar : %s"
# %h = 短哈希  %an = 作者  %ar = 相对时间  %s = 提交信息

# ⭐ 过滤
git log --author="Zhang"                  # 按作者
git log --since="2024-01-01"              # 指定日期之后
git log --until="2024-06-01"              # 指定日期之前
git log --grep="fix"                      # 提交信息包含 fix
git log -p                                # 显示具体修改内容（补丁）
git log -p -- file.txt                    # 只看某个文件的历史
git log --stat                            # 显示文件变更统计
git log -S "function_name"                # ⭐ 搜索代码中的字符串

# ⭐ 查看某个文件的修改历史
git log -p file.txt                       # 文件每次修改的 diff
git blame file.txt                        # 逐行显示最后修改者和提交
```

### git diff

```bash
# ⭐ 查看不同状态下的差异
git diff                                  # 工作区 vs 暂存区
git diff --staged                         # 暂存区 vs 最近提交（同 --cached）
git diff HEAD                             # 工作区 + 暂存区 vs 最近提交
git diff commit1 commit2                  # 两个提交之间的差异
git diff branch1 branch2                  # 两个分支的差异
git diff --name-only                      # 只显示文件名
git diff --stat                           # 显示统计信息
```

---

## 四、分支管理 ⭐

### 分支概念

```
main ──A──B──C────────┐
                       ├─── merge ─── E（main）
develop ──D──E──F─────┘
              │
feature       └───G──H （feature/login）
```

> [!info] Git 的分支只是指向某次提交的**指针**，创建和切换分支极快（秒级），这是 Git 相比其他 VCS 的核心优势。

### 分支操作

```bash
# ⭐ 创建分支
git branch develop                        # 创建 develop 分支（基于当前提交）
git branch feature/login main             # 从 main 创建分支

# ⭐ 查看分支
git branch                                # 本地分支列表（* 表示当前分支）
git branch -r                             # 远程分支
git branch -a                             # 所有分支（本地+远程）
git branch -v                             # 分支和最新提交

# ⭐ 切换分支
git checkout develop                      # 切换到 develop 分支
git checkout -b feature/login             # 创建并切换到新分支

# ⭐ 合并分支
git checkout main                         # 先切到目标分支
git merge develop                         # 将 develop 合并到 main
git merge --no-ff develop                 # ⭐ 强制生成合并提交（保留分支历史）

# ⭐ 删除分支
git branch -d develop                     # 删除已合并的分支
git branch -D develop                     # 强制删除（未合并也能删）
git push origin --delete develop          # 删除远程分支

# ⭐ 重命名分支
git branch -m old-name new-name           # 重命名当前分支
```

### 合并策略

```bash
# 1. Fast-Forward 合并（直线历史）
# 条件：目标分支没有新提交，只需要移动指针
# git merge develop  # 默认 Fast-Forward

# 2. 三路合并（创建合并提交）
# 条件：两个分支都有新提交
# git merge --no-ff develop  # 强制创建合并节点

# 3. 变基（Rebase）
# git checkout feature
# git rebase main              # 把 feature 的提交"搬"到 main 末尾

# 4. Cherry-Pick（挑选提交）
# git cherry-pick commit-hash  # 把某个提交应用到当前分支
```

### 分支命名规范

```
主要分支：
  main / master       生产环境（只接受合并，不直接提交）
  develop             开发环境（集成分支）

功能分支：
  feature/login       feature/xxx    从 develop 创建，合并回 develop

修复分支：
  fix/payment-bug     fix/xxx        从 main 创建，合并回 main 和 develop

发布分支：
  release/1.2.0       release/xxx    从 develop 创建，合并到 main 和 develop

热修复分支：
  hotfix/critical-bug  hotfix/xxx    从 main 创建，合并到 main 和 develop
```

---

## 五、远程仓库协作 ⭐

### SSH 密钥配置

```bash
# ⭐ 生成 SSH 密钥
ssh-keygen -t ed25519 -C "your@email.com"   # 推荐 ed25519
ssh-keygen -t rsa -b 4096 -C "your@email.com"  # 备选 RSA

# 查看公钥并添加到 GitHub/GitLab
cat ~/.ssh/id_ed25519.pub

# 测试连接
ssh -T git@github.com                     # GitHub
ssh -T git@gitlab.com                     # GitLab
```

### 远程仓库管理

```bash
# ⭐ 查看远程仓库
git remote -v

# ⭐ 添加远程仓库
git remote add origin git@github.com:user/repo.git
git remote add upstream git@github.com:other/repo.git  # 上游仓库（Fork 项目）

# ⭐ 修改远程仓库
git remote set-url origin git@github.com:user/new-repo.git
git remote rename origin upstream

# ⭐ 删除远程仓库
git remote remove origin
```

### 推送与拉取

```bash
# ⭐ 推送
git push origin main                    # 推送到远程 main 分支
git push -u origin main                 # 首次推送，建立跟踪关系
git push origin feature/login           # 推送功能分支
git push --all                          # 推送所有分支
git push --tags                         # 推送所有标签

# ⭐ 拉取
git pull                                # 拉取并合并（相当于 fetch + merge）
git pull --rebase                       # ⭐ 拉取并变基（推荐）
git pull origin main                    # 从指定远程拉取

# ⭐ 拉取但不合并
git fetch                               # 只拉取，然后可以 git diff origin/main
git fetch origin
git fetch --all                         # 拉取所有远程

# 查看远程分支
git branch -r                           # 远程分支列表
git fetch origin feature/login          # 拉取远程分支到本地
git checkout -b feature/login origin/feature/login  # 基于远程分支创建本地分支
```

### Pull Request / Merge Request 工作流

```
1. Fork 项目（或直接建立功能分支）
2. git checkout -b feature/xxx
3. 编码、提交
4. git push -u origin feature/xxx
5. 在 GitHub/GitLab 上创建 PR/MR
6. 代码审查、讨论、修改
7. 合并到主分支
8. 删除远程功能分支
```

---

## 六、撤销与恢复 ⭐

### 工作区与暂存区

```bash
# ⭐ 工作区修改（未 git add）
git checkout -- file.txt                # 丢弃工作区修改（恢复到最后一次 add/commit）
git restore file.txt                    # Git 2.23+ 更安全的写法
git checkout .                          # 丢弃所有工作区修改（⚠️ 不可恢复！）

# ⭐ 已 git add（暂存区）
git reset HEAD file.txt                 # 取消暂存（回到工作区）
git restore --staged file.txt           # Git 2.23+ 写法
git reset HEAD .                        # 取消所有暂存

# ⭐ 已 git commit（本地仓库）
git reset --soft HEAD~1                 # 撤销提交，保留工作区和暂存区修改
git reset --mixed HEAD~1                # 撤销提交，保留工作区（取消暂存）
git reset --hard HEAD~1                 # ⚠️ 完全撤销提交和修改（危险！）

# ⭐ 更安全的方式：创建新的反向提交
git revert HEAD                         # 创建一个新提交，撤销上一个提交
git revert commit-hash                  # 撤销指定提交
# revert 不重写历史，适合已推送的提交
```

### 后悔药大全书 ⭐

```bash
# 场景一：刚提交了，想改提交信息
git commit --amend -m "新的信息"

# 场景二：漏了个文件想补上
git add forgotten-file.txt
git commit --amend --no-edit

# 场景三：提交错了想撤销（还没推送）
git reset --soft HEAD~1                 # 撤销提交，修改回到暂存区
# 或
git reset HEAD~1                        # 撤销提交，修改回到工作区

# 场景四：提交错了且已推送
git revert HEAD                         # 创建反向提交
git push

# 场景五：想恢复到某次历史版本（不丢修改）
git log --oneline                       # 找到目标提交哈希
git reset --soft <hash>                 # 软重置到那个版本

# 场景六：彻底回到某个历史版本（丢弃所有后续修改）
git reset --hard <hash>                 # ⚠️ 丢失所有后续本地修改

# 场景七：后悔了想恢复 reset --hard 前的状态
git reflog                              # ⭐ 查看所有 HEAD 移动记录（救命神器）
git reset --hard HEAD@{1}               # 恢复到 reflog 中的状态
```

### git reflog ⭐

> [!warning] **`git reflog` 是你的最后一根救命稻草！**即使 `git reset --hard` 丢了提交，只要没有清理 reflog（默认 90 天），就能找回来。

```bash
git reflog                              # 查看引用日志
# 输出示例：
# abc1234 HEAD@{0}: reset: moving to HEAD~1
# def5678 HEAD@{1}: commit: feat: 添加用户登录
# ghi9012 HEAD@{2}: commit: fix: 修改样式

# 恢复到某次操作之前
git reset --hard HEAD@{1}               # 恢复 HEAD@{1} 的状态
```

---

## 七、变基（Rebase）⭐

### 基本 Rebase

```bash
# ⭐ 变基：将当前分支的提交"移植"到目标分支的最新提交之上

# 变基前：
#     A──B──C  feature
#    /
# D──E──F──G  main
#
# git checkout feature
# git rebase main
#
# 变基后：
#             A'──B'──C'  feature
#            /
# D──E──F──G  main

# ⭐ 使用场景：功能分支同步最新主分支
git checkout feature/login
git rebase main

# 如果有冲突
git status                              # 查看冲突文件
# 解决冲突后
git add .
git rebase --continue                   # 继续变基
git rebase --skip                       # 跳过一个提交
git rebase --abort                      # 放弃变基，回到之前状态
```

### 交互式变基 ⭐

```bash
# ⭐ 交互式变基：整理最近的 N 次提交
git rebase -i HEAD~3                    # 整理最近 3 次提交
git rebase -i main                      # 整理从 main 分支以来的所有提交

# 交互界面中可用的命令：
# pick     = 保留该提交
# reword/r = 修改提交信息
# edit/e   = 修改提交内容
# squash/s = 合并到上一个提交（保留信息）
# fixup/f  = 合并到上一个提交（丢弃信息）
# drop/d   = 删除提交

# 示例：将最近 3 个提交合并为 1 个
# pick abc123 feat: A
# squash def456 feat: B     ← 合并到 A
# squash ghi789 feat: C     ← 合并到 A
```

### Merge vs Rebase

```
Merge（保留分支历史）             Rebase（线性历史）
    A──B──C feature                A'──B'──C' feature
   /                              /
D──E──F──G main              D──E──F──G main
   \                              \
    H──I──J main（合并后）          （无合并节点）

特点：                          特点：
- 保留真实的分支结构              - 线性历史，更清晰
- 可以看到"谁合并了谁"            - 每个提交都是可理解的
- 会产生合并提交                  - 没有多余的合并节点
```

> [!tip] **什么时候用 merge / rebase？**
> - **公共分支**（main/develop）：用 `merge --no-ff` 保留合并历史
> - **个人功能分支**：用 `rebase main` 保持线性历史
> - **已推送的公共提交**：**永远不要 rebase**（其他人会有灾难）
> - **拉取远程更新**：`git pull --rebase`（避免无意义的合并提交）

---

## 八、标签（Tag）

```bash
# ⭐ 创建标签
git tag v1.0.0                          # 轻量标签
git tag -a v1.0.0 -m "正式版 v1.0.0"    # 附注标签（推荐，含作者日期信息）
git tag -a v1.0.0 <commit-hash> -m "v1.0.0"  # 给历史提交打标签

# ⭐ 查看标签
git tag                                  # 列出所有标签
git tag -l "v1.*"                        # 搜索标签
git show v1.0.0                          # 查看标签详情

# ⭐ 推送到远程
git push origin v1.0.0                   # 推送单个标签
git push --tags                          # 推送所有标签

# ⭐ 删除标签
git tag -d v1.0.0                        # 删除本地标签
git push origin --delete v1.0.0          # 删除远程标签
```

---

## 九、Stash（暂存）⭐

```bash
# ⭐ 场景：正在开发 feature A，突然需要修复 bug
# 工作区修改了一半，不想提交，需要切换分支

# 暂存当前工作区
git stash                                # 保存当前工作进度
git stash push -m "feat: 开发中"          # 带描述

# 查看 stash 列表
git stash list
# stash@{0}: On feature/login: feat: 开发中
# stash@{1}: On main: fix: 临时修改

# ⭐ 恢复 stash
git stash pop                            # 恢复最近一次 stash 并删除
git stash apply                          # 恢复但不删除
git stash apply stash@{1}                # 恢复指定 stash

# ⭐ 其他 stash 操作
git stash drop                           # 删除最近一次 stash
git stash drop stash@{1}                 # 删除指定 stash
git stash clear                          # 清空所有 stash
git stash show                           # 查看 stash 中的修改
git stash show -p                        # 查看修改的 diff
git stash -u                             # 暂存包括未跟踪的文件
git stash --all                          # 暂存所有文件
```

---

## 十、.gitignore ⭐

```gitignore
# ⭐ .gitignore 示例

# 依赖目录
node_modules/
vendor/
.pnp
.pnp.js

# 构建输出
dist/
build/
*.tsbuildinfo
.next/

# 环境变量和密钥
.env
.env.local
.env.*.local
*.pem
*.key

# IDE 和编辑器
.vscode/
.idea/
*.swp
*.swo
*~

# 操作系统文件
.DS_Store
Thumbs.db
ehthumbs.db
Desktop.ini

# 日志
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# 测试覆盖率
coverage/
.nyc_output/

# 临时文件
*.tmp
*.temp
.cache

# 忽略所有 .env 但保留 .env.example
.env*
!.env.example
```

```bash
# ⭐ 全局 .gitignore（对所有仓库生效）
git config --global core.excludesfile ~/.gitignore_global

# 已经跟踪的文件移到 .gitignore 中无效
# 需要先取消跟踪
git rm --cached file.txt                 # 取消跟踪但保留文件
git rm -r --cached .                     # 取消所有文件跟踪（慎用）
```

---

## 十一、Git 钩子（Hooks）

### 客户端钩子

```bash
# .git/hooks/ 目录下的脚本，在特定 Git 事件时触发

# ⭐ 常用钩子
pre-commit          # 提交前运行（代码检查、格式化、测试）
pre-push            # 推送前运行（运行测试、编译检查）
post-commit         # 提交后运行（通知）
post-merge          # 合并后运行
post-checkout       # 切换分支后运行
```

```bash
#!/bin/sh
# ⭐ pre-commit 钩子示例（.git/hooks/pre-commit）

# 检查是否在 main 分支直接提交
branch=$(git symbolic-ref HEAD 2>/dev/null | cut -d'/' -f3)
if [ "$branch" = "main" ]; then
    echo "❌ 禁止直接在 main 分支提交！"
    exit 1
fi

# 运行 linter
npm run lint
if [ $? -ne 0 ]; then
    echo "❌ Lint 未通过！"
    exit 1
fi
```

> [!tip] 使用 **Husky**（npm 包）管理 Git hooks 更方便：`npx husky-init` 一键配置。

---

## 十二、子模块（Submodule）

```bash
# ⭐ 当项目依赖另一个 Git 项目时使用

# 添加子模块
git submodule add https://github.com/user/shared-lib.git libs/shared

# ⭐ 克隆包含子模块的项目
git clone https://github.com/user/main-project.git
git submodule init                        # 初始化子模块配置
git submodule update                      # 拉取子模块

# 或一次性克隆 + 子模块
git clone --recurse-submodules https://github.com/user/main-project.git

# 更新子模块
git submodule update --remote             # 更新到最新提交

# 子模块的修改
# 1. 进入子模块目录
# 2. git checkout main && git pull
# 3. 回到主项目：git add libs/shared && git commit
```

---

## 十三、Git 工作流 ⭐

### GitHub Flow（最简单）

```
main ──────┬─────────┬────────────
            \        /            \
feature/A   └──A1──A2             \
                                    \
feature/B                          └──B1──B2

特点：
- 只有 main 分支
- 功能分支 → 发起 PR → 合并到 main
- 适合：小团队、持续部署
```

### Git Flow（最完善）

```
main ───────●──────────────●─────
             \            /
develop       ●─────●───●─
                 \     /
feature/login    └──●─●
                              \
release/1.0                    └──●──●
               \
hotfix/crash                   └──●──●
```

| 分支类型 | 命名 | 从哪创建 | 合并到哪 |
|:--------:|:----:|:--------:|:--------:|
| main | main | — | — |
| develop | develop | main | main（发布时） |
| 功能分支 | feature/* | develop | develop |
| 发布分支 | release/* | develop | main + develop |
| 热修复分支 | hotfix/* | main | main + develop |

### GitLab Flow（综合方案）

```
GitLab Flow = 环境分支 + 功能分支

main ──────●──────●────────●─────
             \    /        /
staging        ●────────●─
                  \    /
production          ●─────
```

### 推荐工作流（小型团队）

```bash
# 1. 从 main 创建功能分支
git checkout -b feature/add-login main

# 2. 日常开发，多次提交
git add . && git commit -m "feat: 登录表单"
git add . && git commit -m "feat: 登录 API"
git add . && git commit -m "feat: 登录验证"

# 3. 同步远程最新代码
git fetch origin
git rebase origin/main                    # 保持线性历史

# 4. 推送功能分支
git push -u origin feature/add-login

# 5. 创建 PR，Code Review

# 6. 合并到 main（Squash Merge：压缩合并）
# 所有 feat 提交合并为一个整洁的提交
```

---

## 十四、故障排除 ⭐

### 常见问题

```bash
# 1. 合并冲突
# 冲突标记：
# <<<<<<< HEAD
# 当前分支的内容
# =======
# 合并进来的内容
# >>>>>>> feature/login
git status                                # 查看冲突文件
# 手动解决冲突后：
git add .
git commit -m "解决合并冲突"

# 2. 推送到远程被拒绝
# 原因：远程有新提交
git pull --rebase                         # 先拉取并变基
# 或
git fetch
git rebase origin/main
git push

# 3. 文件被误删
git checkout HEAD -- file.txt             # 恢复文件

# 4. 想放弃当前所有修改
git reset --hard HEAD                     # 放弃工作区和暂存区所有修改

# 5. 提交信息写错了（已推送）
git commit --amend -m "正确的信息"
git push --force-with-lease               # 安全地强制推送

# 6. 把一个文件还原到某个历史版本
git log --oneline -- file.txt             # 查看文件修改历史
git checkout <hash> -- file.txt           # 还原到指定版本
git commit -m "revert: 还原 file.txt 到某个版本"

# 7. 在错误的分支上做了修改
git stash
git checkout correct-branch
git stash pop
```

### 常用命令速查表

| 操作 | 命令 |
|:----:|:----:|
| 初始化仓库 | `git init` |
| 克隆仓库 | `git clone <url>` |
| 查看状态 | `git status` |
| 添加文件 | `git add <file>` |
| 提交 | `git commit -m "msg"` |
| 推送 | `git push origin <branch>` |
| 拉取 | `git pull --rebase` |
| 创建分支 | `git branch <name>` |
| 切换分支 | `git checkout <name>` |
| 创建并切换 | `git checkout -b <name>` |
| 合并分支 | `git merge <branch>` |
| 查看历史 | `git log --oneline --graph` |
| 暂存修改 | `git stash` |
| 恢复修改 | `git stash pop` |
| 撤销暂存 | `git reset HEAD <file>` |
| 撤销提交（保留修改） | `git reset --soft HEAD~1` |
| 撤销提交（丢弃修改） | `git reset --hard HEAD~1` |
| 反向撤销（安全） | `git revert HEAD` |
| 查看引用日志 | `git reflog` |

---

## 十五、Git 面试常见问题

### 1. Git 中 merge 和 rebase 的区别？

> `merge` 保留完整的分支历史，会产生合并提交，适合公共分支。`rebase` 将提交移植到目标分支末尾，形成线性历史，适合个人功能分支。**黄金法则**：已经推送到远程的公共分支不要 rebase。

### 2. git pull 和 git fetch 的区别？

> `git pull = git fetch + git merge`。`fetch` 只拉取远程数据不合并，需要手动 `merge` 或 `rebase`。`pull` 直接拉取并合并。推荐先 `git fetch` 再决定如何合并，或使用 `git pull --rebase`。

### 3. 如何解决合并冲突？

> 1）`git status` 查看冲突文件；2）手动编辑文件解决冲突（删除 `<<<<<<<`、`=======`、`>>>>>>>` 标记）；3）`git add` 标记已解决；4）`git commit` 完成合并。

### 4. reset、revert、restore 的区别？

> `reset` 移动 HEAD 指针，重写历史（慎用于公共分支）。`revert` 创建反向提交撤销更改，不重写历史（安全，用于公共分支）。`restore`（Git 2.23+）专门用于撤销工作区或暂存区的修改，比 `reset` 更安全直观。

### 5. 什么是 detached HEAD？如何处理？

> HEAD 不指向任何分支，直接指向某次提交时即 detached HEAD。通常在 `git checkout <hash>` 时出现。在此状态下做的提交会成为"孤儿提交"。解决：`git checkout -b new-branch` 为这些提交创建分支。

### 6. Git 的三种状态和三个区域？

> **三个区域**：工作区（Working Directory）、暂存区（Staging Area）、本地仓库（Repository）。**三种状态**：已修改（Modified）、已暂存（Staged）、已提交（Committed）。`git add` 将修改移入暂存区，`git commit` 将暂存内容提交到仓库。

### 7. 什么是 git stash 的适用场景？

> 当工作区有未完成修改，需要临时切换到其他分支时使用。例如正在开发功能 A，需要修复紧急 bug，用 `git stash` 暂存当前工作，修复 bug 后再 `git stash pop` 恢复。

### 8. 如何修改历史提交信息？

> 最近一次：`git commit --amend -m "新信息"`。多次提交：`git rebase -i HEAD~3` 进入交互模式，将 `pick` 改为 `reword`，保存后逐个修改。

### 9. 如何把多个提交合并成一个？

> `git rebase -i HEAD~N`，将后面 commit 的 `pick` 改为 `squash`（保留提交信息）或 `fixup`（丢弃提交信息）。如果已推送到远程，需要 `--force-with-lease`。

### 10. git cherry-pick 的作用？

> `cherry-pick` 可以将**某个或某几个提交**从其他分支复制到当前分支。适用于需要挑出特定修改（而非整个分支）的场景。例如从 release 分支挑出某个修复到 main 分支。

---

> [!tip] **学习路径建议**
> 1. **入门**：安装配置 → 基本操作（add/commit/push/pull）→ 查看历史
> 2. **基础**：分支管理 → 合并 → 远程协作 → 解决冲突
> 3. **进阶**：Rebase → Stash → Cherry-pick → .gitignore
> 4. **深入**：交互式 Rebase → Reflog → 子模块 → Git Hooks
> 5. **实战**：Git Flow 工作流 → CI/CD 集成 → 团队规范
