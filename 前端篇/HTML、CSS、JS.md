# HTML、CSS、JS 

## 一、HTML 概述

### 什么是 HTML

**HTML（HyperText Markup Language）** 是超文本标记语言，是 Web 页面的骨架。它不是编程语言，而是一种**标记语言**，用标签来描述网页的结构。

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>网页标题</title>
</head>
<body>
    <h1>Hello, World!</h1>
    <p>这是我的第一个网页。</p>
</body>
</html>
```

| 部分 | 作用 |
|:----:|------|
| `<!DOCTYPE html>` | 文档类型声明（HTML5） |
| `<html>` | 根元素，整张网页的容器 |
| `<head>` | 头部，放元数据、标题、样式、脚本 |
| `<body>` | 主体，放可见内容 |

### 标签分类

| 分类 | 说明 | 示例 |
|:----:|------|:----:|
| **块级元素** | 独占一行，可设宽高 | `div`、`p`、`h1~h6`、`ul`、`ol`、`table` |
| **行内元素** | 不独占一行，宽度由内容决定 | `span`、`a`、`strong`、`em`、`img` |
| **行内块元素** | 不独占一行，但可设宽高 | `img`、`input`、`button` |

---

## 二、HTML 常用标签

### 文本标签

```html
<!-- 标题 -->
<h1>一级标题</h1>
<h2>二级标题</h2>
<h3>三级标题</h3>
<h4>四级标题</h4>
<h5>五级标题</h5>
<h6>六级标题</h6>

<!-- 段落与换行 -->
<p>这是一个段落。</p>
这是第一行<br>这是第二行

<!-- 文本格式化 -->
<strong>加粗</strong>       <!-- 语义：重要 -->
<b>加粗</b>                 <!-- 仅样式 -->
<em>斜体</em>               <!-- 语义：强调 -->
<i>斜体</i>                 <!-- 仅样式 -->
<ins>下划线</ins>
<del>删除线</del>
<mark>高亮</mark>
<small>小字</small>
<sup>上标</sup>
<sub>下标</sub>

<!-- 引用 -->
<blockquote>长引用（块级）</blockquote>
<q>短引用（行内）</q>
<code>code</code>
<pre>保留
    换行和
      缩进</pre>

<!-- 转义字符 -->
&lt;  &gt;  &amp;  &quot;  &nbsp;
<!-- <  >   &   "   空格 -->
```

### 列表

```html
<!-- 无序列表 -->
<ul>
    <li>苹果</li>
    <li>香蕉</li>
    <li>橘子</li>
</ul>

<!-- 有序列表 -->
<ol type="1" start="3">    <!-- type: 1 A a I i -->
    <li>第一步</li>
    <li>第二步</li>
    <li>第三步</li>
</ol>

<!-- 自定义列表 -->
<dl>
    <dt>HTML</dt>
    <dd>超文本标记语言</dd>
    <dt>CSS</dt>
    <dd>层叠样式表</dd>
</dl>
```

### 超链接与图片

```html
<!-- 超链接 -->
<a href="https://example.com">普通链接</a>
<a href="page2.html" target="_blank">新窗口打开</a>    <!-- _blank 新窗口 / _self 自身 -->
<a href="#section2">跳转到锚点</a>
<a href="mailto:hello@example.com">发邮件</a>
<a href="tel:13800138000">打电话</a>
<a href="file.pdf" download>下载文件</a>

<!-- 图片 -->
<img src="logo.png" alt="网站Logo" width="200" height="100">
<img src="photo.jpg" alt="照片" style="max-width: 100%;">

<!-- 图片链接 -->
<a href="https://example.com">
    <img src="banner.jpg" alt="点击跳转">
</a>
```

### 表格

```html
<table>
    <caption>学生成绩表</caption>     <!-- 表格标题 -->
    <thead>
        <tr>
            <th>姓名</th>
            <th>语文</th>
            <th>数学</th>
            <th>英语</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>张三</td>
            <td>85</td>
            <td>92</td>
            <td>78</td>
        </tr>
        <tr>
            <td>李四</td>
            <td>90</td>
            <td>88</td>
            <td>95</td>
        </tr>
    </tbody>
    <tfoot>
        <tr>
            <td colspan="4">共 2 名学生</td>   <!-- 跨列合并 -->
        </tr>
    </tfoot>
</table>

<!-- 合并单元格 -->
<td colspan="2">占两列</td>   <!-- 跨列 -->
<td rowspan="2">占两行</td>   <!-- 跨行 -->
```

### 表单 ⭐

```html
<form action="/submit" method="POST">
    <!-- 文本框 -->
    <label for="username">用户名：</label>
    <input type="text" id="username" name="username"
           placeholder="请输入用户名" required
           minlength="3" maxlength="16">

    <!-- 密码框 -->
    <label for="password">密码：</label>
    <input type="password" id="password" name="password" required>

    <!-- 邮箱 / 电话 / 数字 / 日期 -->
    <input type="email" name="email" placeholder="邮箱">
    <input type="tel" name="phone" placeholder="手机号">
    <input type="number" name="age" min="0" max="150" step="1">
    <input type="date" name="birthday">
    <input type="url" name="website">

    <!-- 单选 / 复选 -->
    <input type="radio" name="gender" value="male" id="male">
    <label for="male">男</label>
    <input type="radio" name="gender" value="female" id="female">
    <label for="female">女</label>

    <input type="checkbox" name="hobby" value="reading"> 阅读
    <input type="checkbox" name="hobby" value="coding"> 编程

    <!-- 下拉框 -->
    <select name="city">
        <option value="">请选择城市</option>
        <option value="beijing">北京</option>
        <option value="shanghai" selected>上海</option>
        <option value="shenzhen">深圳</option>
    </select>

    <!-- 多行文本 -->
    <textarea name="intro" rows="4" cols="50" placeholder="自我介绍"></textarea>

    <!-- 文件上传 -->
    <input type="file" name="avatar" accept="image/*">

    <!-- 隐藏字段 -->
    <input type="hidden" name="token" value="abc123">

    <!-- 按钮 -->
    <button type="submit">提交</button>
    <button type="reset">重置</button>
    <button type="button" onclick="alert('点击')">普通按钮</button>
</form>
```

### 语义化标签（HTML5）

```html
<header>页头/导航区域</header>
<nav>导航链接</nav>
<main>主要内容</main>
<section>文档的章节</section>
<article>独立文章/内容块</article>
<aside>侧边栏/补充内容</aside>
<footer>页脚/版权信息</footer>
<figure>
    <img src="chart.png" alt="图表">
    <figcaption>图1：数据分析结果</figcaption>
</figure>
<time datetime="2025-01-15">2025年1月15日</time>
<details>
    <summary>点击展开</summary>
    隐藏的详细内容
</details>
```

```
语义化结构：
┌─────────────────────────────┐
│          <header>           │
│     <nav>  导航  </nav>      │
├─────────────────────────────┤
│         <main>              │
│  ┌─────────┐ ┌──────────┐   │
│  │<article>│ │ <aside>  │   │
│  │         │ │          │   │
│  └─────────┘ └──────────┘   │
│         </main>             │
├─────────────────────────────┤
│          <footer>           │
└─────────────────────────────┘
```

### 多媒体

```html
<!-- 音频 -->
<audio controls src="music.mp3">
    您的浏览器不支持音频播放
</audio>

<!-- 视频 -->
<video controls width="640" src="video.mp4">
    您的浏览器不支持视频播放
</video>

<!-- iframe（嵌入其他页面） -->
<iframe src="https://example.com" width="800" height="600"
        sandbox="allow-scripts allow-same-origin"></iframe>

<!-- Canvas（绘图） -->
<canvas id="myCanvas" width="400" height="300"></canvas>
```

> [!tip] **HTML 核心要点**
> - 标签要**正确嵌套**（先开后关的规则）
> - `<head>` 放元数据，`<body>` 放内容
> - **语义化**使网站对搜索引擎和屏幕阅读器更友好
> - 表单用 `<label>` 关联 `<input>` 提高可访问性

---

## 三、CSS 基础

### CSS 是什么

**CSS（Cascading Style Sheets）** 是层叠样式表，用来控制 HTML 的**表现**（布局、颜色、字体、动画等）。

### 三种引入方式

```html
<!-- 1. 内联样式（最不推荐） -->
<p style="color: red; font-size: 18px;">红色文字</p>

<!-- 2. 内部样式表 -->
<head>
    <style>
        p { color: blue; }
    </style>
</head>

<!-- 3. 外部样式表（⭐ 推荐） -->
<head>
    <link rel="stylesheet" href="style.css">
</head>
```

### 基本语法

```css
/* 选择器 { 属性: 值; 属性: 值; } */
h1 {
    color: #333;
    font-size: 24px;
    margin-bottom: 16px;
}
```

### 选择器 ⭐

```css
/* ============ 基础选择器 ============ */

/* 标签选择器 */
p { color: black; }

/* 类选择器（. 开头）⭐ 最常用 */
.highlight { background: yellow; }

/* ID 选择器（# 开头）— 只能用于一个元素 */
#header { height: 60px; }

/* 通配选择器 */
* { margin: 0; padding: 0; }

/* 属性选择器 */
[type="text"] { border: 1px solid #ccc; }
[href^="https"] { color: green; }          /* 以 https 开头 */
[href$=".pdf"] { color: red; }             /* 以 .pdf 结尾 */
[title*="hello"] { font-weight: bold; }    /* 包含 hello */

/* ============ 组合选择器 ============ */

/* 后代选择器（空格）— 所有后代 */
div p { color: gray; }

/* 子代选择器（>）— 直接子元素 */
ul > li { list-style: none; }

/* 相邻兄弟（+）— 紧接在后的第一个 */
h2 + p { margin-top: 0; }

/* 通用兄弟（~）— 后面的所有 */
h2 ~ p { color: #666; }

/* 多选择器（,）— 同时选择 */
h1, h2, h3 { font-family: "Microsoft YaHei", sans-serif; }

/* ============ 伪类选择器 ⭐ ============ */

/* 链接伪类（顺序很重要：LoVe HAte） */
a:link { color: blue; }       /* 未访问 */
a:visited { color: purple; }  /* 已访问 */
a:hover { color: red; }       /* ⭐ 鼠标悬停 */
a:active { color: orange; }   /* 点击时 */

/* 位置伪类 */
li:first-child { font-weight: bold; }    /* 第一个 */
li:last-child { border: none; }          /* 最后一个 */
li:nth-child(odd) { background: #f5f5f5; }  /* 奇数行 */
li:nth-child(even) { background: #fff; }     /* 偶数行 */
li:nth-child(3) { color: red; }              /* 第 3 个 */
li:nth-child(3n+1) { }                       /* 1, 4, 7... */

/* 状态伪类 */
input:focus { outline: 2px solid blue; }    /* 聚焦 */
input:disabled { opacity: 0.5; }            /* 禁用 */
input:checked { accent-color: green; }      /* 选中 */
:empty { display: none; }                   /* 空元素 */

/* ============ 伪元素 ============ */
p::before { content: "▶ "; }               /* 元素前插入 */
p::after { content: " ◀"; }                /* 元素后插入 */
p::first-line { font-weight: bold; }        /* 首行 */
p::first-letter { font-size: 2em; }        /* 首字母 */
::selection { background: yellow; }         /* 选中文本样式 */
```

### 选择器优先级（权重）

```
内联样式 > ID 选择器 > 类选择器 > 标签选择器

具体权重计算：
  - 内联样式：1,0,0,0
  - ID 选择器：0,1,0,0
  - 类/属性/伪类：0,0,1,0
  - 标签/伪元素：0,0,0,1
  - 通配符 *：0,0,0,0
  - !important：∞（⚠️ 能不用就不用）
```

```css
/* 权重比较 */
#nav .item a        /* 0,1,1,1 */
.nav a:hover        /* 0,0,2,1 */
div ul li           /* 0,0,0,3 */
```

### 盒模型 ⭐

```
┌─────────────────────────────────────┐
│               margin                │
│  ┌───────────────────────────────┐  │
│  │           border              │  │
│  │  ┌─────────────────────────┐  │  │
│  │  │        padding          │  │  │
│  │  │  ┌───────────────────┐  │  │  │
│  │  │  │     content       │  │  │  │
│  │  │  │    （内容区域）      │  │  │  │
│  │  │  └───────────────────┘  │  │  │
│  │  └─────────────────────────┘  │  │
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘
```

```css
/* 标准盒模型（默认） */
box-sizing: content-box;
/* width = content 宽度，padding + border 额外增加 */

/* ⭐ 怪异盒模型（推荐） */
box-sizing: border-box;
/* width = content + padding + border，更符合直觉 */

/* 全局设置（⭐ 推荐放在最前面） */
*, *::before, *::after {
    box-sizing: border-box;
}

/* 盒模型属性 */
.box {
    width: 200px;              /* 宽度 */
    height: 100px;             /* 高度 */
    padding: 20px;             /* 内边距（四边相同） */
    padding: 10px 20px;        /* 上下 10px，左右 20px */
    padding: 10px 20px 30px;   /* 上 10px，左右 20px，下 30px */
    padding: 10px 20px 30px 40px;  /* 上 右 下 左（顺时针）*/
    margin: 16px;              /* 外边距 */
    border: 2px solid #333;    /* 边框：宽度 样式 颜色 */
    border-radius: 8px;        /* 圆角 ⭐ */
    background: #f0f0f0;
}
```

### 常用 CSS 属性

```css
/* ============ 文字样式 ============ */
.text {
    font-family: "PingFang SC", "Microsoft YaHei", sans-serif; /* 字体系列 */
    font-size: 16px;           /* 字号 */
    font-weight: 700;          /* 字重 400=normal, 700=bold */
    font-style: italic;        /* 斜体 */
    line-height: 1.6;          /* ⭐ 行高（倍数比 px 更灵活） */
    text-align: center;        /* 对齐：left/center/right/justify */
    text-decoration: none;     /* 装饰：underline/overline/line-through/none */
    text-indent: 2em;          /* 首行缩进 */
    letter-spacing: 2px;       /* 字间距 */
    word-spacing: 4px;         /* 词间距 */
    white-space: nowrap;       /* 不换行 */
    color: #333;               /* 文字颜色 */
}

/* ============ 颜色 ============ */
/* 命名颜色 */  color: red;
/* 十六进制 */  color: #ff6600;   /* 可简写 #f60 */
/* RGB */       color: rgb(255, 0, 0);
/* RGBA */      color: rgba(255, 0, 0, 0.5);   /* ⭐ a=透明度 0~1 */
/* HSL */       color: hsl(0, 100%, 50%);

/* ============ 背景 ============ */
.bg {
    background-color: #f0f0f0;
    background-image: url("bg.png");
    background-repeat: no-repeat;     /* repeat / repeat-x / repeat-y / no-repeat */
    background-position: center;      /* top/center/bottom + left/center/right */
    background-size: cover;           /* ⭐ cover 覆盖 / contain 包含 */
    /* 简写 */
    background: #fff url("bg.png") no-repeat center/cover;
}

/* ============ 文本溢出处理 ⭐ ============ */
/* 单行文本溢出省略 */
.ellipsis {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

/* 多行文本溢出省略（WebKit 浏览器） */
.multiline-ellipsis {
    display: -webkit-box;
    -webkit-line-clamp: 3;            /* 显示 3 行 */
    -webkit-box-orient: vertical;
    overflow: hidden;
}
```

> [!tip] **CSS 最佳实践**
> - 类名用 **`-` 连接**的小写英文（如 `nav-item`、`user-avatar`）
> - 尽量用 **class** 选择器，少用 ID 和 `!important`
> - 全局设置 `box-sizing: border-box` 让盒模型更直观
> - 利用浏览器的 **DevTools** 调试样式

---

## 四、CSS 布局

### display 属性

```css
/* 常见 display 值 */
display: block;            /* 块级（div, p, h1） */
display: inline;           /* 行内（span, a） */
display: inline-block;     /* 行内块（可设宽高但不换行） */
display: none;             /* ⭐ 隐藏（不占位，不同于 visibility:hidden） */
display: flex;             /* ⭐ Flexbox */
display: grid;             /* ⭐ Grid */
```

### Flexbox（弹性布局）⭐

```css
/* 容器属性 */
.container {
    display: flex;                 /* 开启 Flex */
    flex-direction: row;           /* 主轴方向：row / column */
    flex-wrap: wrap;               /* 是否换行 */
    justify-content: center;       /* ⭐ 主轴对齐：flex-start / center / flex-end / space-between / space-around / space-evenly */
    align-items: center;           /* ⭐ 交叉轴对齐：stretch / center / flex-start / flex-end */
    align-content: flex-start;     /* 多行对齐 */
    gap: 16px;                     /* ⭐ 子项间距（推荐，替代 margin） */
}

/* 子项属性 */
.item {
    flex: 1;                       /* ⭐ 等分剩余空间 */
    flex: 0 0 auto;                /* flex-grow flex-shrink flex-basis */
    flex-grow: 1;                  /* 放大比例 */
    flex-shrink: 0;                /* 缩小比例（0=不缩小） */
    flex-basis: 200px;             /* 初始大小 */
    align-self: center;            /* 单独对齐 */
    order: -1;                     /* 排序（越小越前） */
}
```

```
Flexbox 示意图：
┌────容器─────────────────────────┐
│ justify-content: center          │
│  ┌─────┐  ┌─────┐  ┌─────┐      │
│  │  1  │  │  2  │  │  3  │      │  ← align-items: center
│  └─────┘  └─────┘  └─────┘      │
└──────────────────────────────────┘
```

```css
/* ⭐ 常用布局模式 */

/* 1. 水平居中 */
.parent { display: flex; justify-content: center; }

/* 2. 垂直居中 */
.parent { display: flex; align-items: center; }

/* 3. 完全居中 */
.parent { display: flex; justify-content: center; align-items: center; }

/* 4. 等分布局 */
.parent { display: flex; }
.child { flex: 1; }          /* 每个子项等宽 */

/* 5. Sticky Footer（footer 永远在底部）*/
body { display: flex; flex-direction: column; min-height: 100vh; }
.content { flex: 1; }

/* 6. 水平垂直居中（旧方式） */
.parent { position: relative; }
.child {
    position: absolute;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
}
```

### Grid（网格布局）

```css
/* 容器 */
.grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);     /* ⭐ 3 列等宽 */
    grid-template-columns: 200px 1fr 300px;     /* 固定 + 自适应 + 固定 */
    grid-template-rows: auto 100px auto;         /* 行高 */
    gap: 16px;                                  /* ⭐ 间距 */
    justify-items: stretch;                      /* 水平对齐 */
    align-items: stretch;                        /* 垂直对齐 */
}

/* 子项 */
.grid-item {
    grid-column: span 2;        /* 跨 2 列 */
    grid-column: 1 / 3;          /* 从第 1 线到第 3 线 */
    grid-row: 1 / 2;             /* 行范围 */
    justify-self: center;        /* 单独水平对齐 */
    align-self: center;          /* 单独垂直对齐 */
}
```

```css
/* ⭐ 经典布局：页眉 + 侧栏 + 主内容 + 页脚 */
.layout {
    display: grid;
    grid-template-areas:
        "header  header"
        "sidebar main"
        "footer  footer";
    grid-template-columns: 250px 1fr;  /* 侧栏 250px + 自适应 */
    grid-template-rows: auto 1fr auto;  /* 页眉/页脚自适应高度 */
    min-height: 100vh;
    gap: 0;
}

.header  { grid-area: header; }
.sidebar { grid-area: sidebar; }
.main    { grid-area: main; }
.footer  { grid-area: footer; }
```

### 定位

```css
/* position 定位 */
position: static;          /* 默认，正常文档流 */
position: relative;        /* 相对自己原来位置偏移 */
position: absolute;        /* ⭐ 相对于最近的 relative/absolute 父元素 */
position: fixed;           /* ⭐ 相对于视口固定 */
position: sticky;          /* 粘性定位（滚动到一定位置固定） */

/* 偏移属性（与 position 配合）*/
top: 0; right: 0; bottom: 0; left: 0;

/* z-index：层叠顺序（值越大越靠前）*/
z-index: 10;               /* 需要配合 position 使用 */

/* 示例 */
.fixed-header {
    position: fixed;
    top: 0; left: 0; right: 0;
    height: 60px;
    z-index: 1000;
}

.back-to-top {
    position: fixed;
    right: 20px;
    bottom: 20px;
}

.badge {
    position: absolute;
    top: -8px;
    right: -8px;
}
```

### 响应式布局 ⭐

```css
/* ============ 媒体查询 ============ */

/* 断点（参考 Bootstrap） */
/* xs: < 576px    sm: ≥ 576px    md: ≥ 768px
   lg: ≥ 992px    xl: ≥ 1200px   xxl: ≥ 1400px */

/* 手机 */
@media (max-width: 767px) {
    body { font-size: 14px; }
    .sidebar { display: none; }
}

/* 平板 */
@media (min-width: 768px) and (max-width: 991px) {
    .container { max-width: 720px; }
}

/* 桌面 */
@media (min-width: 992px) {
    .container { max-width: 960px; }
}

/* ⭐ 响应式图片 */
img {
    max-width: 100%;          /* 图片不超出容器 */
    height: auto;             /* 保持宽高比 */
}

/* ⭐ 响应式 Flex */
.card-container {
    display: flex;
    flex-wrap: wrap;
    gap: 16px;
}

.card {
    flex: 1 1 300px;         /* 基础 300px，可伸缩 */
    /* 等价于：flex-grow: 1; flex-shrink: 1; flex-basis: 300px; */
}
```

> [!tip] **布局选型**
> - **一维布局**（行/列方向）→ **Flexbox** ⭐
> - **二维布局**（行+列）→ **Grid**
> - **绝对定位**→ 需要层叠/固定位置
> - 日常开发 **Flexbox 使用频率最高**

---

## 五、CSS 进阶

### CSS 变量（自定义属性）

```css
/* 全局变量 */
:root {
    --primary: #1890ff;
    --success: #52c41a;
    --warning: #faad14;
    --danger: #ff4d4f;
    --text-color: #333;
    --bg-color: #fff;
    --border-radius: 8px;
    --shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

/* 使用变量 */
.button {
    background-color: var(--primary);
    color: white;
    border-radius: var(--border-radius);
    box-shadow: var(--shadow);
}

.button-danger {
    background-color: var(--danger);
}

/* 局部变量 */
.card {
    --card-padding: 16px;
    padding: var(--card-padding);
}

/* 变量默认值 */
.title {
    color: var(--text-color, #333);  /* 第二个参数为默认值 */
}
```

### 过渡与动画

```css
/* ============ 过渡 transition ⭐ ============ */
.button {
    background: #1890ff;
    color: white;
    /* 属性 持续时间 缓动函数 延迟 */
    transition: background 0.3s ease, transform 0.2s ease;
    /* transition: all 0.3s ease;  */   /* 所有属性都过渡 */
}

.button:hover {
    background: #40a9ff;
    transform: translateY(-2px);
}

/* 缓动函数 */
/* ease          : 慢→快→慢（默认）*/
/* linear        : 匀速 */
/* ease-in       : 慢→快 */
/* ease-out      : 快→慢 */
/* ease-in-out   : 慢→快→慢 */
/* cubic-bezier  : 自定义贝塞尔曲线 */

/* ============ 动画 animation ⭐ ============ */

/* 定义关键帧 */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
}

@keyframes spin {
    0%   { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

@keyframes bounce {
    0%, 100% { transform: translateY(0); }
    50%      { transform: translateY(-15px); }
}

/* 使用动画 */
.box {
    animation: fadeIn 0.5s ease forwards;
    /* 名称 持续时间 缓动函数 填充模式 */
    /* animation: spin 1s linear infinite; */   /* 旋转动画 */
}

/* animation 简写：name duration timing-function delay iteration-count direction fill-mode */
.loading {
    animation: spin 1s linear infinite;
}

.alert-enter {
    animation: bounce 0.3s ease;
}
```

### Transform 变换

```css
.transform-demo {
    /* 平移 */
    transform: translateX(50px);          /* 水平移动 */
    transform: translateY(-20px);         /* 垂直移动 */
    transform: translate(50px, -20px);    /* 同时 */

    /* 旋转 */
    transform: rotate(45deg);             /* 旋转（deg 度）*/
    transform: rotate(0.5turn);           /* 半圈 */

    /* 缩放 */
    transform: scale(1.5);                /* 放大 1.5 倍 */
    transform: scaleX(2);                 /* 水平拉伸 */

    /* 倾斜 */
    transform: skewX(10deg);

    /* ⭐ 组合 */
    transform: translate(50%, -50%) scale(1.1);

    /* ⭐ 修改变换原点 */
    transform-origin: center;             /* 默认中心 */
    transform-origin: top left;           /* 左上角 */
}
```

### 常见实用技巧

```css
/* ⭐ 三角形 */
.triangle {
    width: 0;
    height: 0;
    border: 20px solid transparent;
    border-top-color: #333;
}

/* ⭐ 阴影 */
.card {
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);  /* 盒子阴影 */
}
.text-shadow {
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3); /* 文字阴影 */
}

/* ⭐ 渐变 */
.gradient {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
.radial-gradient {
    background: radial-gradient(circle, #ff6b6b, #c92a2a);
}

/* ⭐ 滤镜 */
.blur {
    filter: blur(4px);          /* 模糊 */
    filter: brightness(1.2);    /* 亮度 */
    filter: grayscale(100%);    /* 灰度 */
    filter: blur(4px) grayscale(50%);  /* 组合 */
}

/* ⭐ 滚动条美化 */
::-webkit-scrollbar {
    width: 8px;
}
::-webkit-scrollbar-track {
    background: #f1f1f1;
}
::-webkit-scrollbar-thumb {
    background: #888;
    border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
    background: #555;
}
```

> [!tip] **CSS 学习路径**
> 1. 基础选择器 + 盒模型（一周）
> 2. **Flexbox 布局**（两周，⭐ 最常用）
> 3. 定位 + 响应式（一周）
> 4. Grid + 动效（巩固期）

---

## 六、JavaScript 基础

### JavaScript 是什么

**JavaScript（简称 JS）** 是一种**动态类型、弱类型**的脚本语言，是 Web 前端的"行为"层。HTML 是结构、CSS 是样式、JavaScript 是交互。

### 引入方式

```html
<!-- 1. 内部脚本 -->
<script>
    console.log("Hello, JS!");
</script>

<!-- 2. 外部脚本（⭐ 推荐）-->
<script src="app.js"></script>

<!-- 3. 放在 body 底部（传统）— 确保 DOM 已加载 -->
<body>
    <!-- ... 页面内容 ... -->
    <script src="app.js"></script>
</body>

<!-- 4. defer（⭐ 现代推荐：异步下载，DOM 解析完执行）-->
<script src="app.js" defer></script>

<!-- 5. async（异步下载，下载完立即执行，可能阻塞 DOM）-->
<script src="analytics.js" async></script>
```

### 变量声明

```javascript
// var — 旧方式（函数作用域，可重复声明，会提升）
var name = "Alice";
var name = "Bob";     // 可重复声明（⚠️ 容易出 Bug）

// let — ⭐ 推荐（块级作用域，不可重复声明）
let age = 25;
age = 26;              // 可修改
// let age = 30;       // ❌ 不能重复声明

// const — ⭐ 常量（块级作用域，不可重新赋值）
const PI = 3.14159;
// PI = 3;             // ❌ 不能修改
const user = { name: "Alice" };
user.name = "Bob";     // ✅ 对象内容可以修改（不能重新赋值）
```

### 数据类型

```javascript
// 基本类型（栈内存，不可变）
typeof "hello"          // "string"
typeof 42               // "number"
typeof 3.14             // "number"（没有整数类型）
typeof true             // "boolean"
typeof undefined        // "undefined"
typeof null             // "object"（⚠️ 历史遗留 bug）
typeof Symbol()         // "symbol"
typeof 9007199254740991n // "bigint"

// 引用类型（堆内存，可变）
typeof {}               // "object"
typeof []               // "object"（数组也是对象）
typeof function(){}     // "function"
```

### 类型转换

```javascript
// 隐式转换（⚠️ 容易踩坑）
console.log("5" - 3);     // 2（字符串转数字）
console.log("5" + 3);     // "53"（数字转字符串，+ 偏向字符串拼接）
console.log("5" * "2");   // 10
console.log(!0);          // true（0 为假）
console.log(!"hello");    // false（非空字符串为真）

// 显式转换（推荐）
Number("42")              // 42
String(42)                // "42"
Boolean(1)                // true
parseInt("42px")          // 42
parseFloat("3.14em")      // 3.14

// 假值：false、0、""、null、undefined、NaN
if (0) {}           // 不执行
if ("") {}          // 不执行
if (null) {}        // 不执行
if (undefined) {}   // 不执行
if (NaN) {}         // 不执行
```

### 运算符

```javascript
// 算术
+ - * / % **          // ** 是幂运算（ES7）

// 比较
==  !=   ===  !==     // ⭐ 始终用 === 和 !==（严格相等）
5 == "5"              // true（类型转换后相等）
5 === "5"             // false（类型不同）

// 逻辑
&&  ||  !             // 短路运算
true && "hello"       // "hello"（&& 返回第一个假值或最后一个值）
false || "default"    // "default"（|| 返回第一个真值或最后一个值）

// ⭐ 可选链（ES2020）
user?.address?.city   // 如果 user 或 address 为 null/undefined，返回 undefined 而不是抛错

// ⭐ 空值合并（ES2020）
const name = input ?? "默认值";   // 只有 null/undefined 时取默认值（和 || 不同）
0 ?? "默认"       // 0（?? 只对 null/undefined 生效）
0 || "默认"       // "默认"（|| 对 0 也生效）
```

### 字符串

```javascript
const name = "Alice";
const age = 25;

// ⭐ 模板字符串（推荐）
const msg = `我叫 ${name}，今年 ${age} 岁`;     // 支持插值
const multi = `多行
字符串
很方便`;                                         // 支持多行

// 常用方法
"hello".toUpperCase()       // "HELLO"
"HELLO".toLowerCase()       // "hello"
"hello".includes("ell")     // true
"hello".startsWith("he")    // true
"hello".endsWith("lo")      // true
"a,b,c".split(",")          // ["a", "b", "c"]
[1, 2, 3].join("-")         // "1-2-3"
"  hello  ".trim()          // "hello"
"hello world".replace("world", "JS")  // "hello JS"
```

### 数组

```javascript
const arr = [1, 2, 3, 4, 5];

// 增删改
arr.push(6);                 // 末尾添加    [1,2,3,4,5,6]
arr.pop();                   // 末尾移除    [1,2,3,4,5]
arr.unshift(0);              // 开头添加    [0,1,2,3,4,5]
arr.shift();                 // 开头移除    [1,2,3,4,5]
arr.splice(1, 2);            // 从索引 1 删 2 个 [1,4,5]
arr.splice(1, 0, "a", "b"); // 在索引 1 插入 [1,"a","b",4,5]

// ⭐ 常用方法
arr.includes(3)              // true（是否包含）
arr.indexOf(3)               // 2（索引位置）
arr.find(x => x > 3)         // 4（找第一个符合条件的）
arr.findIndex(x => x > 3)    // 3（找索引）
arr.some(x => x > 3)         // true（是否有符合条件的）
arr.every(x => x > 0)        // true（是否全部符合）
arr.flat()                   // 扁平化嵌套数组
```

### 对象

```javascript
// 创建对象
const user = {
    name: "Alice",
    age: 25,
    "full name": "Alice Wang",  // 键名有空格需加引号
    greet() {                   // ⭐ 简写方法
        console.log(`你好，我是 ${this.name}`);
    },
};

// 访问
user.name                      // "Alice"（点号）
user["full name"]              // "Alice Wang"（方括号）
const key = "age";
user[key]                      // 25（动态属性名）

// 增删改
user.email = "alice@example.com";  // 新增
delete user.age;                    // 删除

// ⭐ 遍历
Object.keys(user)      // ["name", "age", "greet"]
Object.values(user)    // ["Alice", 25, ƒ]
Object.entries(user)   // [["name","Alice"], ["age",25], ...]

for (const key in user) {         // 遍历 key
    console.log(key, user[key]);
}

// ⭐ 展开运算符（ES2018）
const copy = { ...user };                         // 浅拷贝
const merged = { ...user, role: "admin" };        // 合并
```

### 函数

```javascript
// 1. 函数声明（会提升）
function add(a, b) {
    return a + b;
}

// 2. 函数表达式（不提升）
const multiply = function(a, b) {
    return a * b;
};

// 3. ⭐ 箭头函数（ES6）
const subtract = (a, b) => a - b;       // 单行隐式 return
const double = x => x * 2;              // 一个参数可省略括号
const greet = (name) => {
    return `你好，${name}`;              // 多行需写 return 和 {}
};

// 箭头函数 vs 普通函数
// 1. 箭头函数没有自己的 this（继承外层 this）⭐
// 2. 箭头函数不能用作构造函数
// 3. 箭头函数没有 arguments 对象

// 默认参数
function greet(name = "游客") {
    return `你好，${name}`;
}

// 剩余参数
function sum(...numbers) {
    return numbers.reduce((a, b) => a + b, 0);
}
sum(1, 2, 3, 4)   // 10

// 展开数组作为参数
const nums = [1, 2, 3];
Math.max(...nums)                 // 3
```

### 条件与循环

```javascript
// if/else
if (score >= 90) {
    grade = "A";
} else if (score >= 80) {
    grade = "B";
} else {
    grade = "C";
}

// ⭐ 三元运算符
const status = age >= 18 ? "成年" : "未成年";

// switch
switch (day) {
    case 1: name = "周一"; break;
    case 2: name = "周二"; break;
    default: name = "未知";
}

// for 循环
for (let i = 0; i < 10; i++) { /* ... */ }

// ⭐ for...of（遍历可迭代对象）
for (const item of arr) { /* ... */ }
for (const char of "hello") { /* ... */ }

// for...in（遍历对象 key，不推荐遍历数组）
for (const key in obj) { /* ... */ }

// while / do...while
while (condition) { /* ... */ }
do { /* ... */ } while (condition);
```

### 常用数组方法 ⭐

```javascript
const numbers = [1, 2, 3, 4, 5, 6];

// ⭐ forEach — 遍历
numbers.forEach(n => console.log(n));

// ⭐ map — 映射（返回新数组）
numbers.map(n => n * 2);                // [2, 4, 6, 8, 10, 12]

// ⭐ filter — 过滤（返回新数组）
numbers.filter(n => n % 2 === 0);       // [2, 4, 6]

// ⭐ reduce — 归约
numbers.reduce((acc, cur) => acc + cur, 0);  // 21（求和）

// ⭐ sort — 排序（⚠️ 默认按字符串排序）
[3, 1, 10, 2].sort();                   // [1, 10, 2, 3]（字符串排序，不对！）
[3, 1, 10, 2].sort((a, b) => a - b);   // [1, 2, 3, 10] ✅

// 链式调用
const result = numbers
    .filter(n => n > 2)    // [3, 4, 5, 6]
    .map(n => n ** 2)      // [9, 16, 25, 36]
    .reduce((a, b) => a + b, 0);  // 86
```

> [!tip] **JS 核心要点**
> - 始终用 `===` 而不是 `==`
> - 优先用 `const`，其次 `let`，不用 `var`
> - 箭头函数简洁且 this 指向更可控
> - `map` / `filter` / `reduce` 代替传统 for 循环
> - 模板字符串代替字符串拼接

---

## 七、DOM 操作

### 什么是 DOM

**DOM（Document Object Model）** 是 JS 操作 HTML 的接口。它将网页抽象为一棵节点树。

```
document
  └── html
        ├── head
        │     ├── meta
        │     ├── title
        │     └── style
        └── body
              ├── header
              ├── main
              │     ├── section
              │     └── article
              └── footer
```

### 获取元素 ⭐

```javascript
// ⭐ 现代推荐
document.querySelector(".class");          // 获取第一个匹配的
document.querySelector("#id");
document.querySelector("div p.highlight");
document.querySelectorAll(".item");        // 获取所有匹配（NodeList）

// 传统方式
document.getElementById("id");
document.getElementsByClassName("class");  // HTMLCollection（动态）
document.getElementsByTagName("div");
```

### 操作内容与属性

```javascript
const el = document.querySelector(".title");

// ★ 文本内容
el.textContent = "新标题";          // 纯文本（安全，不解析 HTML）
el.innerText = "新标题";           // 类似，但考虑 CSS 样式

// ★ HTML 内容
el.innerHTML = "<span>带标签的内容</span>";  // ⚠️ 会解析 HTML（XSS 风险）
el.outerHTML = "<h1>替换整个元素</h1>";

// ★ 属性操作
el.getAttribute("data-id");         // 获取属性
el.setAttribute("data-id", "123");  // 设置属性
el.removeAttribute("data-id");      // 删除属性
el.hasAttribute("data-id");         // 判断是否存在

// ★ 直接操作属性
el.id = "new-id";
el.className = "box active";
el.href = "https://example.com";

// ★ data-* 自定义属性
el.dataset.id = "123";              // 对应 data-id
el.dataset.userName = "Alice";     // 对应 data-user-name
```

### 操作类名 ⭐

```javascript
const el = document.querySelector(".box");

// ⭐ classList（推荐）
el.classList.add("active");          // 添加类
el.classList.remove("hidden");       // 删除类
el.classList.toggle("expanded");     // 切换类（有→删，无→加）
el.classList.contains("active");     // 判断是否包含
el.classList.replace("old", "new");  // 替换类

// 旧方式（不推荐）
el.className = "box active";         // 会覆盖所有类
```

### 操作样式

```javascript
const el = document.querySelector(".box");

// ★ 修改内联样式
el.style.color = "red";
el.style.backgroundColor = "#f0f0f0";  // 驼峰命名
el.style.fontSize = "18px";
el.style.display = "flex";
el.style.setProperty("--primary", "blue");  // CSS 变量

// ★ 获取计算样式
const styles = getComputedStyle(el);
console.log(styles.color);         // 获取最终生效的颜色
console.log(styles.fontSize);

// ★ 批量设置样式
Object.assign(el.style, {
    color: "white",
    backgroundColor: "#333",
    padding: "16px",
    borderRadius: "8px",
});
```

### 创建与删除元素

```javascript
// ★ 创建元素
const div = document.createElement("div");
div.textContent = "新元素";
div.className = "item";
div.dataset.index = "0";

// ★ 插入
parent.append(div);            // 末尾追加（可同时插入多个）
parent.prepend(div);           // 开头插入
parent.appendChild(div);       // 末尾追加（传统）
parent.insertBefore(div, ref); // 在 ref 之前插入

// ⭐ 插入HTML（比 innerHTML 更安全）
parent.insertAdjacentHTML("beforeend", "<li>新项</li>");
// beforebegin / afterbegin / beforeend / afterend

// ★ 删除
div.remove();                  // ⭐ 直接删除（ES6）
parent.removeChild(div);       // 传统方式

// ★ 克隆
const clone = div.cloneNode(true);   // true=深克隆（包含子元素）

// ⭐ 批量创建（文档片段）
const fragment = document.createDocumentFragment();
for (let i = 0; i < 100; i++) {
    const li = document.createElement("li");
    li.textContent = `项 ${i}`;
    fragment.appendChild(li);
}
list.appendChild(fragment);     // 一次性插入，减少回流
```

### 事件处理 ⭐

```javascript
// ★ 添加事件
const btn = document.querySelector("button");

// 方式一：on 属性（只能绑定一个）
btn.onclick = function() { console.log("点击"); };

// ⭐ 方式二：addEventListener（推荐，可绑定多个）
btn.addEventListener("click", function(e) {
    console.log("点击了！");
});

// 箭头函数版本
btn.addEventListener("click", (e) => {
    console.log("点击了！");
});

// 事件对象 e
element.addEventListener("click", (e) => {
    e.target;           // 触发事件的元素
    e.currentTarget;    // 绑定事件的元素
    e.preventDefault(); // ⭐ 阻止默认行为（如表单提交、链接跳转）
    e.stopPropagation();// ⭐ 阻止事件冒泡
    e.type;             // 事件类型："click"
    e.clientX, e.clientY;   // 鼠标坐标（相对视口）
});

// 移除事件
element.removeEventListener("click", handler);  // 需要函数引用

// ⭐ 常用事件
// 鼠标: click, dblclick, mouseover, mouseout, mousedown, mouseup, mousemove
// 键盘: keydown, keyup, keypress
// 表单: submit, focus, blur, change, input
// 文档: DOMContentLoaded, load, scroll, resize
// 触摸: touchstart, touchmove, touchend
```

### 事件流

```
捕获阶段（Capture）→ 目标阶段（Target）→ 冒泡阶段（Bubble）

       ┌── document ──────────────────────┐
       │  ↓ 捕获         ↑ 冒泡            │
       │ ┌─── html ──────────────┐         │
       │ │  ↓ 捕获     ↑ 冒泡    │         │
       │ │ ┌── body ───────┐     │         │
       │ │ │  ↓ 捕获 ↑ 冒泡│     │         │
       │ │ │ ┌── div ──┐   │     │         │
       │ │ │ │ ← 目标 → │   │     │         │
       │ │ │ └─────────┘   │     │         │
       │ │ └───────────────┘     │         │
       │ └───────────────────────┘         │
       └────────────────────────────────────┘
```

```javascript
// 事件委托（利用冒泡）⭐
// 场景：给大量子元素绑定事件
document.querySelector("ul").addEventListener("click", (e) => {
    const li = e.target.closest("li");   // ⭐ 找到最近的 li
    if (li) {
        console.log("点击了:", li.textContent);
    }
});

// 阻止事件冒泡的注意点
child.addEventListener("click", (e) => {
    e.stopPropagation();   // 这样父元素的点击监听就收不到了
});
```

### DOM 操作实战

```javascript
// ★ 简单的 TODO 应用
const form = document.querySelector("#todo-form");
const input = document.querySelector("#todo-input");
const list = document.querySelector("#todo-list");

form.addEventListener("submit", (e) => {
    e.preventDefault();                   // 阻止表单提交刷新页面

    const text = input.value.trim();
    if (!text) return;

    const li = document.createElement("li");
    li.innerHTML = `
        <span>${text}</span>
        <button class="delete">✕</button>
    `;

    // 删除按钮
    li.querySelector(".delete").addEventListener("click", () => {
        li.remove();
    });

    // 点击切换完成状态
    li.addEventListener("click", (e) => {
        if (e.target.tagName !== "BUTTON") {
            li.classList.toggle("completed");
        }
    });

    list.appendChild(li);
    input.value = "";
    input.focus();
});
```

> [!tip] **DOM 操作性能建议**
> - 用 `querySelector` 系列替代旧选择器
> - 批量修改用 `classList`（少直接操作 `style`）
> - 批量插入用 `DocumentFragment`
> - **事件委托**减少事件绑定数量
> - 减少 DOM 操作次数，合并读写

---

## 八、JavaScript 进阶

### 作用域与闭包

```javascript
// 作用域
// 全局 → 函数 → 块级（let/const）

// 闭包：函数能访问外部函数的变量
function createCounter() {
    let count = 0;

    return function() {
        count++;
        return count;
    };
}

const counter = createCounter();
console.log(counter());   // 1
console.log(counter());   // 2
console.log(counter());   // 3

// 闭包应用：封装私有变量
function createUser(name) {
    let _name = name;       // 私有变量
    return {
        getName() { return _name; },
        setName(n) { _name = n; },
    };
}
const user = createUser("Alice");
console.log(user.getName());     // "Alice"
user._name;                      // undefined（无法直接访问）
```

### this 指向

```javascript
// ⭐ this 指向规则（优先级从高到低）

// 1. new 绑定
function Person(name) {
    this.name = name;     // this 指向新创建的实例
}
new Person("Alice");

// 2. 显式绑定：call / apply / bind
function greet() { console.log(this.name); }
greet.call({ name: "Alice" });    // "Alice"
greet.apply({ name: "Bob" });     // "Bob"
const bound = greet.bind({ name: "Charlie" });
bound();                          // "Charlie"

// 3. 隐式绑定（方法调用）
const obj = { name: "Alice", greet() { console.log(this.name); } };
obj.greet();    // "Alice"（this → obj）

const fn = obj.greet;
fn();           // undefined（this → window/undefined，丢失了上下文）

// 4. 默认绑定（严格模式下 undefined，非严格模式 window）
function test() { console.log(this); }
test();         // window（非严格模式）

// ⭐ 箭头函数没有自己的 this（继承外层）
const arrow = () => { console.log(this); };
arrow();        // 继承外层 this（不是 window 而是定义时的上下文）

const obj2 = {
    name: "Alice",
    greet: () => { console.log(this.name); },  // ❌ 箭头函数不适合做方法
    greet2() {
        const inner = () => { console.log(this.name); };  // ✅ 箭头函数内部 this 正确
        inner();
    },
};
obj2.greet();   // undefined（this 是外层）
obj2.greet2();  // "Alice"
```

### Promise ⭐

```javascript
// ⭐ Promise 是处理异步操作的标准方式

// 创建 Promise
const fetchData = new Promise((resolve, reject) => {
    setTimeout(() => {
        const success = true;
        if (success) {
            resolve("数据加载成功");   // 成功时调用
        } else {
            reject(new Error("加载失败"));  // 失败时调用
        }
    }, 1000);
});

// 消费 Promise
fetchData
    .then((data) => {
        console.log(data);          // "数据加载成功"
        return "处理后的数据";
    })
    .then((processed) => {
        console.log(processed);     // 链式调用
    })
    .catch((error) => {
        console.error("出错了:", error);
    })
    .finally(() => {
        console.log("无论如何都执行");   // 清理工作
    });

// ⭐ Promise 静态方法
Promise.all([p1, p2, p3])           // 全部成功才成功
Promise.allSettled([p1, p2, p3])    // 等所有结束（不论成功失败）
Promise.race([p1, p2])              // 第一个完成的
Promise.any([p1, p2])              // 第一个成功的
```

### async / await ⭐

```javascript
// ⭐ async/await 是 Promise 的语法糖，让异步代码像同步一样

// 声明 async 函数
async function loadUserData(userId) {
    try {
        const response = await fetch(`https://api.example.com/users/${userId}`);
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        const user = await response.json();
        return user;
    } catch (error) {
        console.error("请求失败:", error);
        throw error;    // 让调用方也能处理
    }
}

// ⭐ 并发请求
async function loadDashboard() {
    try {
        const [user, posts, notifications] = await Promise.all([
            fetch("/api/user").then(r => r.json()),
            fetch("/api/posts").then(r => r.json()),
            fetch("/api/notifications").then(r => r.json()),
        ]);
        return { user, posts, notifications };
    } catch (error) {
        console.error("仪表盘加载失败:", error);
    }
}

// 使用
loadUserData(1).then(user => console.log(user));
```

### 模块化（ES Module）⭐

```javascript
// utils.js — 导出
export const PI = 3.14159;

export function add(a, b) {
    return a + b;
}

export class Calculator {
    multiply(a, b) { return a * b; }
}

export default function greet(name) {  // 默认导出（一个文件只能有一个）
    return `你好，${name}`;
}

// app.js — 导入
import greet, { PI, add, Calculator } from "./utils.js";
// 默认导入（greet）     命名导入（{ PI, add, Calculator }）

import * as utils from "./utils.js";     // 全部导入为命名空间
console.log(utils.PI);
console.log(utils.add(1, 2));
```

### 常用 Web API

```javascript
// ★ 定时器
setTimeout(() => {
    console.log("延迟 1 秒执行");
}, 1000);

const intervalId = setInterval(() => {
    console.log("每隔 2 秒执行");
}, 2000);

clearTimeout(timeoutId);
clearInterval(intervalId);

// ★ 本地存储
localStorage.setItem("token", "abc123");
const token = localStorage.getItem("token");
localStorage.removeItem("token");
localStorage.clear();                    // 清除所有

sessionStorage.setItem("temp", "临时数据");  // 关闭页面就清除

// 存储对象需 JSON 序列化
localStorage.setItem("user", JSON.stringify({ name: "Alice" }));
const user = JSON.parse(localStorage.getItem("user"));

// ★ fetch API（现代网络请求）⭐
async function fetchUsers() {
    const response = await fetch("https://api.example.com/users", {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer token123",
        },
    });

    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return response.json();          // 自动解析 JSON
}

// POST 请求
async function createUser(data) {
    const response = await fetch("/api/users", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
    });
    return response.json();
}
```

### 错误处理

```javascript
// try/catch/finally
try {
    // 可能出错的代码
    const data = JSON.parse(userInput);
    process(data);
} catch (error) {
    if (error instanceof SyntaxError) {
        console.error("JSON 格式错误");
    } else if (error instanceof TypeError) {
        console.error("类型错误");
    } else {
        console.error("未知错误:", error);
    }
} finally {
    // 无论是否出错都执行
    cleanup();
}

// 自定义错误
class ValidationError extends Error {
    constructor(message, field) {
        super(message);
        this.name = "ValidationError";
        this.field = field;
    }
}

throw new ValidationError("用户名不能为空", "username");

// 全局错误处理
window.onerror = function(message, source, lineno, colno, error) {
    console.error("全局错误:", message);
    return true;    // 阻止默认错误处理
};

// 未被 catch 的 Promise 错误
window.addEventListener("unhandledrejection", (event) => {
    console.error("未处理的 Promise 拒绝:", event.reason);
    event.preventDefault();
});
```

> [!info] **JS 学习路径**
>
> **第一阶段**：变量、类型、运算符、条件循环（1周）
> **第二阶段**：函数、数组/对象操作、DOM 操作（2周）
> **第三阶段**：事件、闭包、this、异步（2周）
> **第四阶段**：Promise、async/await、fetch API（1周）
> **第五阶段**：模块化、工程化、框架入门（持续）

---

## 九、ES6+ 核心特性

| 特性 | 版本 | 说明 |
|:----:|:----:|------|
| `let` / `const` | ES6 | 块级作用域变量 |
| 箭头函数 | ES6 | 简洁的函数语法 |
| 模板字符串 | ES6 | 字符串插值 + 多行 |
| 解构赋值 | ES6 | 快速提取数组/对象值 |
| 展开运算符 `...` | ES6 | 展开/合并数组和对象 |
| `Map` / `Set` | ES6 | 新数据结构 |
| `class` | ES6 | 类的语法糖 |
| `Promise` | ES6 | 异步编程 |
| `async` / `await` | ES2017 | Promise 语法糖 |
| 可选链 `?.` | ES2020 | 安全访问嵌套属性 |
| 空值合并 `??` | ES2020 | null/undefined 兜底 |
| 逻辑赋值 `&&=` `\|\|=` `??=` | ES2021 | 简写 |
| `Array.at()` | ES2022 | 支持负索引 |

### 解构赋值

```javascript
// ★ 数组解构
const [a, b, c] = [1, 2, 3];        // a=1, b=2, c=3
const [first, ...rest] = [1,2,3,4]; // first=1, rest=[2,3,4]
const [x, y = 10] = [5];            // x=5, y=10（默认值）

// 交换变量
[a, b] = [b, a];                    // ⭐ 一行交换

// ★ 对象解构
const { name, age } = { name: "Alice", age: 25 };
const { name: userName, age: userAge } = user;  // 重命名
const { address: { city } } = user;             // 嵌套
const { role = "user" } = user;                 // 默认值

// ★ 函数参数解构
function greet({ name, age }) {
    console.log(`${name} ${age}岁`);
}
greet({ name: "Alice", age: 25 });
```

### 展开运算符

```javascript
// ★ 数组展开
const arr1 = [1, 2, 3];
const arr2 = [4, 5, 6];
const merged = [...arr1, ...arr2];      // [1,2,3,4,5,6]
const copy = [...arr1];                 // 浅拷贝

const max = Math.max(...[3, 1, 10, 5]); // 10

// ★ 对象展开
const base = { x: 1, y: 2 };
const extended = { ...base, z: 3 };     // { x:1, y:2, z:3 }
const clone = { ...base };              // 浅拷贝
const merged2 = { ...obj1, ...obj2 };   // 合并（obj2 覆盖 obj1 的同名属性）
```

### class 语法

```javascript
class Animal {
    constructor(name) {
        this.name = name;
    }

    speak() {
        return `${this.name} 发出声音`;
    }

    // 静态方法
    static isAnimal(obj) {
        return obj instanceof Animal;
    }

    // getter/setter
    get description() {
        return `动物: ${this.name}`;
    }

    set description(val) {
        this.name = val;
    }
}

class Dog extends Animal {
    constructor(name, breed) {
        super(name);          // 必须调用 super！
        this.breed = breed;
    }

    speak() {                 // 重写
        return `${this.name} 汪汪叫`;
    }

    // 私有字段（ES2022+）
    #secret = "秘密信息";

    reveal() {
        return this.#secret;
    }
}

const dog = new Dog("旺财", "金毛");
console.log(dog.speak());           // "旺财 汪汪叫"
console.log(dog.description);       // "动物: 旺财"（getter）
console.log(Animal.isAnimal(dog));  // true（静态方法）
```

### Set / Map

```javascript
// ★ Set — 不重复的集合
const set = new Set([1, 2, 2, 3, 3, 3]);
console.log(set);               // Set {1, 2, 3}

set.add(4);
set.has(2);                     // true
set.delete(1);
set.size;                       // 3

// 数组去重（⭐ 经典用法）
const unique = [...new Set([1, 2, 2, 3, 3, 4])];  // [1, 2, 3, 4]

// ★ Map — 键值对（key 可以是任意类型）
const map = new Map();
map.set("name", "Alice");
map.set(42, "数字 key");
map.set({ id: 1 }, "对象 key");

map.get("name");            // "Alice"
map.has(42);                // true
map.delete(42);
map.size;                   // 2

// 遍历
for (const [key, value] of map) {
    console.log(key, value);
}
```

---

## 十、综合实战

### Todo List 完整示例

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Todo List</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: -apple-system, "Microsoft YaHei", sans-serif;
            background: #f0f2f5;
            padding: 40px 20px;
        }
        .container {
            max-width: 500px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 2px 12px rgba(0,0,0,0.1);
            padding: 24px;
        }
        h1 {
            text-align: center;
            margin-bottom: 20px;
            color: #333;
            font-size: 24px;
        }
        .input-group {
            display: flex;
            gap: 8px;
            margin-bottom: 16px;
        }
        .input-group input {
            flex: 1;
            padding: 10px 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 14px;
            outline: none;
            transition: border-color 0.2s;
        }
        .input-group input:focus {
            border-color: #1890ff;
        }
        .input-group button {
            padding: 10px 20px;
            background: #1890ff;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
            transition: background 0.2s;
        }
        .input-group button:hover {
            background: #40a9ff;
        }

        .stats {
            display: flex;
            justify-content: space-between;
            color: #666;
            font-size: 13px;
            margin-bottom: 12px;
            padding-bottom: 12px;
            border-bottom: 1px solid #f0f0f0;
        }

        .todo-list {
            list-style: none;
        }
        .todo-item {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 10px 8px;
            border-radius: 6px;
            transition: background 0.2s;
        }
        .todo-item:hover {
            background: #f5f5f5;
        }
        .todo-item.completed .todo-text {
            text-decoration: line-through;
            color: #999;
        }
        .todo-text {
            flex: 1;
            font-size: 15px;
        }
        .todo-item input[type="checkbox"] {
            width: 18px;
            height: 18px;
            cursor: pointer;
        }
        .delete-btn {
            background: none;
            border: none;
            color: #ccc;
            cursor: pointer;
            font-size: 18px;
            padding: 0 4px;
            transition: color 0.2s;
        }
        .delete-btn:hover {
            color: #ff4d4f;
        }

        .empty-tip {
            text-align: center;
            color: #999;
            padding: 30px 0;
        }
        .clear-btn {
            display: block;
            width: 100%;
            margin-top: 12px;
            padding: 8px;
            background: none;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            color: #999;
            cursor: pointer;
            transition: all 0.2s;
        }
        .clear-btn:hover {
            border-color: #ff4d4f;
            color: #ff4d4f;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📋 待办事项</h1>

        <div class="input-group">
            <input type="text" id="todoInput" placeholder="输入待办事项...">
            <button id="addBtn">添加</button>
        </div>

        <div class="stats">
            <span>总计: <strong id="totalCount">0</strong></span>
            <span>已完成: <strong id="completedCount">0</strong></span>
            <span>未完成: <strong id="activeCount">0</strong></span>
        </div>

        <ul class="todo-list" id="todoList">
            <li class="empty-tip">暂无待办事项</li>
        </ul>

        <button class="clear-btn" id="clearBtn">清除所有已完成</button>
    </div>

    <script>
        // ★ 数据
        let todos = JSON.parse(localStorage.getItem("todos") || "[]");

        const input = document.getElementById("todoInput");
        const addBtn = document.getElementById("addBtn");
        const list = document.getElementById("todoList");
        const clearBtn = document.getElementById("clearBtn");
        const totalCount = document.getElementById("totalCount");
        const completedCount = document.getElementById("completedCount");
        const activeCount = document.getElementById("activeCount");

        // ★ 渲染
        function render() {
            const completed = todos.filter(t => t.done).length;
            const active = todos.length - completed;

            totalCount.textContent = todos.length;
            completedCount.textContent = completed;
            activeCount.textContent = active;

            if (todos.length === 0) {
                list.innerHTML = '<li class="empty-tip">暂无待办事项</li>';
                return;
            }

            list.innerHTML = todos.map((todo, index) => `
                <li class="todo-item ${todo.done ? "completed" : ""}" data-index="${index}">
                    <input type="checkbox" ${todo.done ? "checked" : ""}>
                    <span class="todo-text">${escapeHtml(todo.text)}</span>
                    <button class="delete-btn" title="删除">✕</button>
                </li>
            `).join("");

            // 保存
            localStorage.setItem("todos", JSON.stringify(todos));
        }

        // XSS 防护
        function escapeHtml(text) {
            const div = document.createElement("div");
            div.textContent = text;
            return div.innerHTML;
        }

        // ★ 添加
        function addTodo() {
            const text = input.value.trim();
            if (!text) return alert("请输入内容");
            todos.push({ text, done: false });
            input.value = "";
            input.focus();
            render();
        }

        // ★ 事件委托
        list.addEventListener("click", (e) => {
            const item = e.target.closest(".todo-item");
            if (!item) return;
            const index = parseInt(item.dataset.index);

            if (e.target.type === "checkbox") {
                // 切换完成状态
                todos[index].done = !todos[index].done;
                render();
            } else if (e.target.classList.contains("delete-btn")) {
                // 删除
                todos.splice(index, 1);
                render();
            }
        });

        // 添加
        addBtn.addEventListener("click", addTodo);
        input.addEventListener("keydown", (e) => {
            if (e.key === "Enter") addTodo();
        });

        // 清除已完成
        clearBtn.addEventListener("click", () => {
            todos = todos.filter(t => !t.done);
            render();
        });

        // 初始渲染
        render();
    </script>
</body>
</html>
```

> [!tip] **三剑客的关系**
>
> ```
> HTML = 结构（房子的骨架）
> CSS  = 样式（装修、墙面颜色、家具摆放）
> JS   = 行为（开关灯、按门铃、开空调）
> ```
>
> 学习顺序：**HTML → CSS → JavaScript**，每个都练手后再学框架（React / Vue / Svelte）。
>
> 上一篇：[[爬虫基础与进阶篇]]
> 下一篇推荐：[[Vue入门到进阶]] 或 [[React入门到进阶]]
