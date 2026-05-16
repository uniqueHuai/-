# CSS 预处理器

## 一、CSS 预处理器概述

### 什么是 CSS 预处理器

**CSS 预处理器** 是一种在原生 CSS 之上添加了**编程能力**的扩展语言，通过编译生成标准 CSS 文件。它让 CSS 代码更可维护、更高效、更具模块化。

```
┌──────────────────┐    编译/转译    ┌───────────────────┐
│  Sass / SCSS     │                │                   │
│  Less            │ ────────────►   │   原生 CSS         │
│  Stylus          │                │  (浏览器可解析)     │
│  PostCSS 插件    │                │                   │
└──────────────────┘                └───────────────────┘
```

### 为什么需要预处理器

| 原生 CSS 的问题 | 预处理器解决方式 |
|:---------------:|:----------------:|
| ❌ 没有变量，重复的颜色/尺寸值到处写 | ✅ 变量定义，一处修改全局生效 |
| ❌ 没有嵌套，选择器层级必须重复写 | ✅ 嵌套语法，结构清晰 |
| ❌ 没有复用机制，相同代码到处复制 | ✅ 混入（Mixin）和继承（Extend） |
| ❌ 没有逻辑，不能写条件/循环 | ✅ 支持条件判断、循环、函数 |
| ❌ 模块化困难，一个大文件难以拆分 | ✅ `@import` 合并，按需拆分 |

### 主流预处理器对比

| 特性 | Sass/SCSS | Less | Stylus | PostCSS |
|:----:|:---------:|:----:|:------:|:-------:|
| **诞生时间** | 2006 | 2009 | 2010 | 2013 |
| **运行环境** | Node (Dart) | Node | Node | Node |
| **语法风格** | 两种语法（SCSS/Sass） | 接近 CSS | 极简灵活 | 插件化 |
| **学习曲线** | 中等 | 较低 | 较高 | 取决于插件 |
| **社区生态** | ⭐⭐⭐ | ⭐⭐ | ⭐ | ⭐⭐⭐ (插件) |
| **框架支持** | Bootstrap 5、Tailwind | Bootstrap 4、Ant Design | — | Autoprefixer 必用 |
| **当前趋势** | **行业标准** | 较少新项目用 | 小众 | **现代 CSS 核心工具** |

> [!tip] **推荐**：新项目首选 **SCSS（Sass）** 作为预处理器，配合 **PostCSS**（Autoprefixer）处理兼容性和未来 CSS 特性。

### 快速开始

```bash
# Sass / SCSS
npm install -D sass

# Less
npm install -D less

# Stylus
npm install -D stylus

# PostCSS（常用插件）
npm install -D postcss autoprefixer postcss-preset-env
```

---

## 二、Sass / SCSS ⭐

### SCSS vs Sass

Sass 有两种语法：

```scss
// ⭐ SCSS（Sassy CSS）—— 推荐！语法和 CSS 完全兼容
$primary-color: #3498db;

.button {
    background-color: $primary-color;
    &:hover {
        background-color: darken($primary-color, 10%);
    }
}
```

```sass
// Sass（缩进语法）—— 了解即可，不用缩进代替花括号
$primary-color: #3498db

.button
    background-color: $primary-color
    &:hover
        background-color: darken($primary-color, 10%)
```

> [!warning] **推荐使用 SCSS**（`.scss` 文件），因为：
> - 完全兼容原生 CSS（把 `.css` 改成 `.scss` 就能用）
> - 更接近主流写法，团队接受度高
> - IDE 支持更好

### 变量（Variables）⭐

```scss
// ⭐ 变量以 $ 开头
$primary-color: #3498db;
$secondary-color: #2ecc71;
$font-stack: "Helvetica Neue", Arial, sans-serif;
$base-font-size: 16px;
$border-radius: 4px;
$spacing-unit: 8px;

// ⭐ 作用域
$global-var: 10px; // 全局变量

.container {
    $local-var: 20px; // 局部变量（仅在此块内有效）
    font-size: $local-var;
}

// ⭐ !default：设置默认值（可被覆盖）
$primary-color: #3498db !default; // 如果没有定义，则使用此值

// ⭐ !global：强制设为全局变量
.box {
    $theme-color: #e74c3c !global;
}

.other {
    color: $theme-color; // ✅ 因为 !global 声明
}
```

### 嵌套（Nesting）⭐

```scss
// ⭐ 嵌套——预处理器最直观的特性
nav {
    background: #333;
    padding: 10px;

    // 嵌套选择器
    ul {
        list-style: none;
        margin: 0;
        padding: 0;

        li {
            display: inline-block;
            margin: 0 5px;

            a {
                color: white;
                text-decoration: none;

                &:hover {
                    color: $primary-color;
                }
            }
        }
    }

    // ⭐ & 引用父选择器
    &-header { font-size: 20px; }    // nav-header
    &-footer { font-size: 12px; }    // nav-footer
}
```

编译后：
```css
nav { background: #333; padding: 10px; }
nav ul { list-style: none; margin: 0; padding: 0; }
nav ul li { display: inline-block; margin: 0 5px; }
nav ul li a { color: white; text-decoration: none; }
nav ul li a:hover { color: #3498db; }
nav-header { font-size: 20px; }
nav-footer { font-size: 12px; }
```

> [!warning] **嵌套不要超过 3 层**，过深嵌套会导致 CSS 选择器冗长，降低可读性和性能。

### `&` 父选择器引用 ⭐

```scss
.button {
    padding: 8px 16px;
    border: none;

    // & 代表父选择器 .button
    &:hover {
        opacity: 0.8;
    }

    &--primary {
        background: $primary-color;

        // 多层 & 拼接
        &--large {
            font-size: 20px;  // .button--primary--large
        }
    }

    // & 也可以放在后面
    .dark-mode & {
        background: #555;
    }
}
```

### 混入（Mixin）⭐

```scss
// ⭐ 定义混入：@mixin + 名称
@mixin flex-center {
    display: flex;
    justify-content: center;
    align-items: center;
}

@mixin box-shadow($x: 2px, $y: 2px, $blur: 4px, $color: rgba(0, 0, 0, 0.2)) {
    -webkit-box-shadow: $x $y $blur $color;
    box-shadow: $x $y $blur $color;
}

@mixin responsive($breakpoint) {
    @if $breakpoint == "mobile" {
        @media (max-width: 768px) { @content; }
    } @else if $breakpoint == "tablet" {
        @media (max-width: 1024px) { @content; }
    } @else if $breakpoint == "desktop" {
        @media (min-width: 1025px) { @content; }
    }
}

// ⭐ 使用混入：@include
.card {
    @include flex-center;
    @include box-shadow;
    padding: 20px;

    // @content：传递内容块
    @include responsive("mobile") {
        flex-direction: column;
    }
}

.card--elevated {
    @include box-shadow(0, 8px, 16px, rgba(0, 0, 0, 0.3));
}
```

编译后：
```css
.card {
    display: flex;
    justify-content: center;
    align-items: center;
    -webkit-box-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    box-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    padding: 20px;
}

@media (max-width: 768px) {
    .card { flex-direction: column; }
}

.card--elevated {
    -webkit-box-shadow: 0 8px 16px rgba(0,0,0,0.3);
    box-shadow: 0 8px 16px rgba(0,0,0,0.3);
}
```

### 继承（@extend）⭐

```scss
// ⭐ @extend：让一个选择器继承另一个选择器的样式
// 适用于样式完全相同的元素

%button-base {               // % 定义占位符选择器（不会编译到 CSS 中）
    padding: 8px 16px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;
}

.btn-primary {
    @extend %button-base;    // 继承所有样式
    background: $primary-color;
    color: white;
}

.btn-danger {
    @extend %button-base;
    background: #e74c3c;
    color: white;
}

.btn-large {
    @extend %button-base;
    @extend .btn-primary;    // 也可以继承普通选择器
    font-size: 18px;
    padding: 12px 24px;
}
```

编译后：
```css
.btn-primary, .btn-danger, .btn-large {
    padding: 8px 16px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;
}

.btn-primary, .btn-large { background: #3498db; color: white; }
.btn-danger { background: #e74c3c; color: white; }
.btn-large { font-size: 18px; padding: 12px 24px; }
```

> [!tip] **Mixin vs @extend**
> | 对比 | @include (Mixin) | @extend |
> |:----:|:----------------:|:-------:|
> | 编译方式 | 复制样式到每个调用处 | 合并选择器（逗号分隔） |
> | 输出体积 | 较大（重复代码） | 较小（分组选择器） |
> | 传参 | ✅ 可传参 | ❌ 不能传参 |
> | 适用场景 | 需要参数、内容块 | 样式完全相同 |
> | **推荐** | ⭐ **优先用 Mixin** | 慎用（@extend 有副作用） |

### 函数与运算 ⭐

```scss
// ⭐ 内置函数
$base-color: #3498db;

// 颜色函数
.lighter { background: lighten($base-color, 20%); }   // 变亮
.darker { background: darken($base-color, 10%); }     // 变暗
.saturate { background: saturate($base-color, 30%); } // 增加饱和度
.desaturate { background: desaturate($base-color, 30%); } // 降低饱和度
.transparent { background: rgba($base-color, 0.5); }  // 透明度

// ⭐ 数学运算
$base-width: 100px;

.box {
    width: $base-width * 2;           // 200px
    height: $base-width + 50;         // 150px
    margin: ($base-width / 4);        // 25px
    font-size: $base-font-size * 1.2; // 19.2px
}

// ⭐ 自定义函数
@function px-to-rem($px, $base: 16px) {
    @return ($px / $base) * 1rem;
}

h1 { font-size: px-to-rem(32px); }  // 2rem
h2 { font-size: px-to-rem(24px); }  // 1.5rem

// ⭐ 字符串函数
@function str-replace($string, $search, $replace: "") {
    $index: str-index($string, $search);
    @if $index {
        @return str-slice($string, 1, $index - 1) + $replace +
            str-replace(str-slice($string, $index + str-length($search)), $search, $replace);
    }
    @return $string;
}
```

### 逻辑控制 ⭐

```scss
// ⭐ @if / @else if / @else
@mixin theme($theme) {
    background: if($theme == "dark", #333, #fff);
    color: if($theme == "dark", #fff, #333);

    @if $theme == "dark" {
        border-color: #555;
    } @else if $theme == "light" {
        border-color: #ddd;
    } @else {
        border-color: transparent;
    }
}

// ⭐ @for 循环
@for $i from 1 through 4 {
    .col-#{$i} {
        width: percentage($i / 4);
    }
}

// ⭐ @each 循环
$sizes: ("sm": 8px, "md": 16px, "lg": 24px);

@each $name, $size in $sizes {
    .padding-#{$name} {
        padding: $size;
    }
}

// ⭐ @while 循环
$column: 12;
@while $column > 0 {
    .col-#{$column} {
        width: percentage($column / 12);
    }
    $column: $column - 1;
}
```

### 模块化（@use / @forward）⭐

```scss
// ⭐ 旧语法 @import（已弃用，不再推荐）
// @import "variables";
// @import "mixins";

// ⭐ 新语法 @use（创建命名空间，避免变量冲突）

// _variables.scss
$primary-color: #3498db !default;
$secondary-color: #2ecc71 !default;

// _mixins.scss
@use "variables" as v;  // 引入并使用命名空间 v.

@mixin primary-button {
    background: v.$primary-color;
    color: white;
}

// main.scss
@use "variables";
@use "mixins";

.button {
    @include mixins.primary-button;
    color: variables.$primary-color;  // 通过命名空间访问
}

// ⭐ 重命名命名空间
@use "variables" as vars;
// vars.$primary-color

// ⭐ 无命名空间
@use "variables" as *;
// 直接 $primary-color

// ⭐ @forward：透传（一个文件重新导出多个模块）
// _index.scss
@forward "variables";
@forward "mixins";

// 使用
@use "index" as *;
// 可以访问 index 中 @forward 的所有变量和 mixin
```

### 媒体查询最佳实践

```scss
// _breakpoints.scss
$breakpoints: (
    "xs": 0,
    "sm": 576px,
    "md": 768px,
    "lg": 992px,
    "xl": 1200px,
    "xxl": 1400px,
);

// ⭐ 响应式混入
@mixin respond-up($breakpoint) {
    $min: map-get($breakpoints, $breakpoint);

    @if $min {
        @media (min-width: $min) {
            @content;
        }
    }
}

@mixin respond-down($breakpoint) {
    $max: map-get($breakpoints, $breakpoint);

    @if $max {
        @media (max-width: ($max - 0.02px)) {
            @content;
        }
    }
}

@mixin respond-between($lower, $upper) {
    $min: map-get($breakpoints, $lower);
    $max: map-get($breakpoints, $upper);

    @if $min and $max {
        @media (min-width: $min) and (max-width: ($max - 0.02px)) {
            @content;
        }
    }
}

// 使用
.card {
    display: grid;
    grid-template-columns: 1fr;

    @include respond-up("md") {
        grid-template-columns: 1fr 1fr;
    }

    @include respond-up("lg") {
        grid-template-columns: 1fr 1fr 1fr;
    }
}
```

---

## 三、Less

### 基本语法

```less
// ⭐ Less 变量用 @
@primary-color: #3498db;
@secondary-color: #2ecc71;
@base-font-size: 16px;
@spacing: 8px;

// ⭐ 嵌套（和 SCSS 相同）
nav {
    ul {
        margin: 0;
        li {
            display: inline-block;

            a {
                color: @primary-color;

                &:hover {
                    text-decoration: underline;
                }
            }
        }
    }
}
```

### Mixin

```less
// ⭐ Less 的 Mixin 更简洁——直接复用类选择器
.flex-center() {
    display: flex;
    justify-content: center;
    align-items: center;
}

.border-radius(@radius: 4px) {
    -webkit-border-radius: @radius;
    border-radius: @radius;
}

.card {
    .flex-center();       // 调用无参 mixin
    .border-radius(8px);
    padding: @spacing * 2;
}
```

### 变量插值与懒加载

```less
// ⭐ 变量插值（Selector Interpolation）
@prefix: "app";

.@{prefix}-header {
    background: #333;
}

.@{prefix}-footer {
    background: #222;
}

// ⭐ 懒加载（Less 变量的值是最后定义的）
@var: "before";

.value-before {
    content: @var;  // "after"
}

@var: "after";
```

### 运算

```less
// ⭐ Less 的运算与 SCSS 类似
@base: 16px;

h1 { font-size: @base * 2; }        // 32px
h2 { font-size: @base * 1.5; }      // 24px
.container { width: 100% - 40px; }   // ⚠️ Less 中单位和值都要运算
.margin { margin: @base / 2; }       // 8px
```

### 内置函数

```less
// ⭐ 颜色函数
lighten(@color, 20%);
darken(@color, 10%);
saturate(@color, 20%);
desaturate(@color, 20%);
fade(@color, 50%);        // 透明度

// ⭐ 其他常用
round(3.14);              // 3
ceil(3.14);               // 4
floor(3.14);              // 3
percentage(0.5);          // 50%
```

### Less vs SCSS

| 对比 | Less | SCSS |
|:----:|:----:|:----:|
| 变量符号 | `@` | `$` |
| Mixin 传参 | `.mixin(@param)` | `@mixin mixin($param)` |
| 条件判断 | `when` | `@if` |
| 循环 | 递归 mixin + `when` | `@for` / `@each` / `@while` |
| 内置函数 | 较少 | 丰富（颜色、数学、字符串） |
| 生态 | Bootstrap 4、Ant Design | Bootstrap 5、主流 |

> [!info] Less 目前的使用场景主要是维护旧项目（如 Ant Design 早期版本、Bootstrap 4），新项目建议使用 SCSS。

---

## 四、Stylus

### 极简语法

```stylus
// ⭐ Stylus 语法极为灵活——可以省略冒号、分号、花括号
primary-color = #3498db
secondary-color = #2ecc71

// 方式一：标准 CSS 语法 ✅
.button {
    background: primary-color;
    color: white;
}

// 方式二：省略花括号 ✅
.button
    background: primary-color
    color: white

// 方式三：再省略冒号 ✅
.button
    background primary-color
    color white
```

### Mixin 与函数

```stylus
// ⭐ Stylus 中 mixin 和函数没有区别
border-radius(n = 4px)
    -webkit-border-radius n
    border-radius n

flex-center()
    display flex
    justify-content center
    align-items center

// 使用
.card
    flex-center()
    border-radius(8px)

// ⭐ 返回值函数
px-to-rem(px, base = 16)
    (px / base) rem
```

### 逻辑控制

```stylus
// ⭐ 条件
theme-color(theme)
    if theme == "dark"
        #333
    else if theme == "light"
        #fff
    else
        #999

// ⭐ 循环
for i in (1..4)
    .col-{i}
        width (i / 4 * 100)%
```

> [!info] Stylus 以极简和灵活著称，但由于可选语法太多导致团队风格难以统一，目前使用率较低。

---

## 五、PostCSS ⭐

### 什么是 PostCSS

**PostCSS** 严格来说**不是 CSS 预处理器**，而是一个 **CSS 处理引擎**，通过插件系统转换 CSS。它可以在预处理器之前或之后使用。

```
PostCSS 生态（插件系统）
│
├── ⭐ Autoprefixer       —— 自动添加浏览器前缀
├── ⭐ postcss-preset-env —— 使用未来的 CSS 语法
├── postcss-nesting       —— CSS 原生嵌套支持
├── postcss-custom-media  —— 自定义媒体查询
├── Tailwind CSS          —— 基于 PostCSS 的工具类框架
├── postcss-modules       —— CSS Modules 支持
└── 2000+ 其他插件
```

### 配置方式

```bash
npm install -D postcss autoprefixer postcss-preset-env
```

```js
// postcss.config.js
module.exports = {
    plugins: [
        require("autoprefixer")({
            overrideBrowserslist: [
                "> 1%",
                "last 2 versions",
                "not dead",
            ],
        }),
        require("postcss-preset-env")({
            stage: 2, // 使用处于 stage 2+ 的 CSS 特性
            features: {
                "nesting-rules": true, // 启用原生嵌套
                "custom-properties": true, // CSS 变量
            },
        }),
    ],
};
```

### Vite 集成

```js
// vite.config.js
export default {
    css: {
        postcss: "./postcss.config.js",
    },
};
```

```scss
// ⭐ 现代 CSS 结合 PostCSS 的写法
:root {
    --primary: #3498db;
    --surface: #ffffff;
    --text: #333333;
}

.card {
    background: var(--surface);
    color: var(--text);
    border-radius: 8px;

    // 原生嵌套（postcss-nesting）
    &__title {
        font-size: 1.5rem;
        color: var(--primary);
    }
}
```

### Autoprefixer ⭐

```css
/* ⭐ 输入（不加前缀） */
.card {
    display: flex;
    user-select: none;
    backdrop-filter: blur(10px);
}

/* ⭐ 输出（自动加前缀） */
.card {
    display: -webkit-box;
    display: -ms-flexbox;
    display: flex;
    -webkit-user-select: none;
    -moz-user-select: none;
    user-select: none;
    -webkit-backdrop-filter: blur(10px);
    backdrop-filter: blur(10px);
}
```

---

## 六、核心特性对比实战

### 变量定义与使用

```scss
// SCSS
$primary: #3498db;
$padding: 16px;
```

```less
// Less
@primary: #3498db;
@padding: 16px;
```

```stylus
// Stylus
primary = #3498db
padding = 16px
```

```css
/* 原生 CSS（CSS Custom Properties） */
:root {
    --primary: #3498db;
    --padding: 16px;
}

.card {
    color: var(--primary);
    padding: var(--padding);
}
```

> [!tip] **CSS 变量 vs 预处理器变量**
> - 预处理器变量：编译时替换，不能动态改变
> - CSS 变量：运行时生效，可用 JS 修改、支持媒体查询
> - **最佳实践**：用 CSS 变量定义主题（可动态切换），用 SCSS 变量定义构建时的值

### 嵌套

```scss
// SCSS
.card {
    padding: 16px;

    &__title { font-size: 1.25rem; }
    &__body { font-size: 1rem; }

    &--featured {
        border: 2px solid $primary;

        .card__title { color: $primary; }
    }
}
```

```css
/* 原生 CSS 嵌套（2023+ 标准） */
.card {
    padding: 16px;

    &__title { font-size: 1.25rem; }
    &__body { font-size: 1rem; }

    &--featured {
        border: 2px solid var(--primary);

        & .card__title { color: var(--primary); }
    }
}
```

### Mixin

```scss
// SCSS
@mixin center-content {
    display: flex;
    justify-content: center;
    align-items: center;
}
```

```less
// Less
.center-content() {
    display: flex;
    justify-content: center;
    align-items: center;
}
```

```stylus
// Stylus
center-content()
    display flex
    justify-content center
    align-items center
```

### 条件

```scss
// SCSS
@if $theme == "dark" { background: #333; }
@else { background: #fff; }
```

```less
// Less
& when (@theme = dark) { background: #333; }
& when not (@theme = dark) { background: #fff; }
```

```stylus
// Stylus
if theme == "dark"
    background #333
else
    background #fff
```

### 循环

```scss
// SCSS
@for $i from 1 through 3 {
    .item-#{$i} { width: 100px * $i; }
}

$colors: (primary, #3498db), (success, #2ecc71);
@each $name, $color in $colors {
    .text-#{$name} { color: $color; }
}
```

```less
// Less（递归 mixin 模拟循环）
.gen-col(@n, @i: 1) when (@i <= @n) {
    .item-@{i} { width: 100px * @i; }
    .gen-col(@n, @i + 1);
}
.gen-col(3);
```

```stylus
// Stylus
for i in 1..3
    .item-{i}
        width 100px * i
```

---

## 七、BEM 命名 + 预处理器最佳实践 ⭐

### BEM 快速回顾

```css
/* Block__Element--Modifier */
.block                { /* 独立组件 */ }
.block__element       { /* 组件内部的元素 */ }
.block--modifier      { /* 组件的变体 */ }
.block__element--modifier { /* 元素的变体 */ }
```

### SCSS 实现 BEM ⭐

```scss
// ⭐ BEM + SCSS 完美搭配
.card {
    $block: &; // 保存当前选择器引用

    padding: 16px;
    background: #fff;
    border-radius: 8px;

    // 元素
    &__title {
        font-size: 1.25rem;
        font-weight: bold;
    }

    &__body {
        font-size: 1rem;
        color: #666;
    }

    &__footer {
        margin-top: 12px;
        padding-top: 12px;
        border-top: 1px solid #eee;
    }

    // 修饰符——利用 & 拼接
    &--featured {
        border: 2px solid $primary;

        // 修饰符下的元素
        #{$block}__title {
            color: $primary;
        }
    }

    &--compact {
        padding: 8px;

        #{$block}__title {
            font-size: 1rem;
        }
    }
}
```

编译后：
```css
.card { padding: 16px; background: #fff; border-radius: 8px; }
.card__title { font-size: 1.25rem; font-weight: bold; }
.card__body { font-size: 1rem; color: #666; }
.card__footer { margin-top: 12px; padding-top: 12px; border-top: 1px solid #eee; }
.card--featured { border: 2px solid #3498db; }
.card--featured .card__title { color: #3498db; }
.card--compact { padding: 8px; }
.card--compact .card__title { font-size: 1rem; }
```

### 主题系统

```scss
// _themes.scss
// ⭐ 主题变量定义
$themes: (
    light: (
        bg: #ffffff,
        text: #333333,
        primary: #3498db,
        surface: #f8f9fa,
        border: #dee2e6,
    ),
    dark: (
        bg: #1a1a2e,
        text: #e0e0e0,
        primary: #64b5f6,
        surface: #16213e,
        border: #2a2a4a,
    ),
);

// ⭐ 主题混入
@mixin themify() {
    @each $theme-name, $theme-vars in $themes {
        $current-theme: $theme-name !global;

        [data-theme="#{$theme-name}"] &,
        .theme-#{$theme-name} & {
            @content;
        }
    }

    $current-theme: null !global;
}

// ⭐ 获取主题变量
@function theme-var($key) {
    @return map-get(map-get($themes, $current-theme), $key);
}
```

```scss
// main.scss
@use "themes" as *;

.card {
    background: #fff;
    color: #333;

    @include themify {
        background: theme-var(bg);
        color: theme-var(text);
        border-color: theme-var(border);
    }
}

.button {
    background: $primary;

    @include themify {
        background: theme-var(primary);
    }
}
```

### 设计 Token 系统 ⭐

```scss
// ⭐ 设计 Token 让样式一致且可维护

// _tokens.scss

// —— 颜色 ——
$colors: (
    // 品牌色
    brand-50: #ebf5fb,
    brand-100: #cfe8fc,
    brand-200: #a0d0f5,
    brand-300: #6cb5ed,
    brand-400: #419ae0,
    brand-500: #3498db,    // 主色
    brand-600: #2980b9,
    brand-700: #1c6ea4,
    brand-800: #155d8c,

    // 中性色
    neutral-50: #f8f9fa,
    neutral-100: #f0f0f0,
    neutral-200: #e0e0e0,
    neutral-300: #bdbdbd,
    neutral-400: #9e9e9e,
    neutral-500: #757575,
    neutral-600: #616161,
    neutral-700: #424242,
    neutral-800: #212121,
    neutral-900: #121212,

    // 语义色
    success: #2ecc71,
    warning: #f39c12,
    error: #e74c3c,
    info: #3498db,
);

// —— 间距 ——
$spacing: (
    0: 0,
    1: 4px,
    2: 8px,
    3: 12px,
    4: 16px,
    5: 20px,
    6: 24px,
    8: 32px,
    10: 40px,
    12: 48px,
    16: 64px,
);

// —— 字体大小 ——
$font-sizes: (
    xs: 12px,
    sm: 14px,
    base: 16px,
    lg: 18px,
    xl: 20px,
    2xl: 24px,
    3xl: 30px,
    4xl: 36px,
    5xl: 48px,
);

// —— 圆角 ——
$radii: (
    none: 0,
    sm: 4px,
    md: 8px,
    lg: 12px,
    xl: 16px,
    full: 9999px,
);

// —— 阴影 ——
$shadows: (
    sm: 0 1px 2px rgba(0, 0, 0, 0.05),
    md: 0 4px 6px rgba(0, 0, 0, 0.1),
    lg: 0 10px 15px rgba(0, 0, 0, 0.1),
    xl: 0 20px 25px rgba(0, 0, 0, 0.15),
);

// —— 断点 ——
$breakpoints: (
    sm: 640px,
    md: 768px,
    lg: 1024px,
    xl: 1280px,
    xxl: 1536px,
);

// —— 获取 Token 函数 ——
@function color($key) { @return map-get($colors, $key); }
@function spacing($key) { @return map-get($spacing, $key); }
@function font-size($key) { @return map-get($font-sizes, $key); }
@function radius($key) { @return map-get($radii, $key); }
@function shadow($key) { @return map-get($shadows, $key); }
@function bp($key) { @return map-get($breakpoints, $key); }

// —— 响应式 Mixin ——
@mixin respond($breakpoint) {
    @if map-has-key($breakpoints, $breakpoint) {
        @media (min-width: map-get($breakpoints, $breakpoint)) {
            @content;
        }
    }
}
```

```scss
// 使用设计 Token
@use "tokens" as *;

.card {
    background: color(neutral-50);
    border: 1px solid color(neutral-200);
    border-radius: radius(md);
    padding: spacing(6);
    box-shadow: shadow(md);

    &__title {
        font-size: font-size(xl);
        color: color(neutral-900);
        margin-bottom: spacing(2);
    }

    &__body {
        font-size: font-size(base);
        color: color(neutral-600);
    }

    &--featured {
        border-color: color(brand-500);
        background: color(brand-50);

        .card__title { color: color(brand-700); }
    }

    @include respond(md) {
        padding: spacing(8);
    }
}
```

---

## 八、工程化集成

### Vite + SCSS ⭐

```js
// vite.config.js
import { defineConfig } from "vite";

export default defineConfig({
    css: {
        // ⭐ 预处理器配置
        preprocessorOptions: {
            scss: {
                // 全局注入变量和 mixin（避免每个文件都 @import）
                additionalData: `
                    @use "@/styles/variables" as *;
                    @use "@/styles/mixins" as *;
                `,
            },
        },
    },
    resolve: {
        alias: {
            "@": "/src",
        },
    },
});
```

```scss
// 组件中无需手动导入变量和 mixin
.card {
    padding: spacing(4);         // 直接使用
    background: color(surface);
    border-radius: radius(md);

    @include respond(md) {
        padding: spacing(6);
    }
}
```

### Webpack + SCSS

```js
// webpack.config.js
module.exports = {
    module: {
        rules: [
            {
                test: /\.scss$/,
                use: [
                    "style-loader",   // 将 CSS 注入到 DOM
                    "css-loader",     // 解析 CSS 中的 @import/url()
                    {
                        loader: "sass-loader",
                        options: {
                            additionalData: `
                                @use "@/styles/variables" as *;
                                @use "@/styles/mixins" as *;
                            `,
                        },
                    },
                ],
            },
        ],
    },
};
```

### CSS Modules + SCSS

```scss
// Button.module.scss
.button {
    padding: 8px 16px;
    background: $primary;
    border: none;
    border-radius: 4px;
    color: white;
    cursor: pointer;

    &:hover {
        opacity: 0.9;
    }
}

.primary {
    background: $primary;
}

.danger {
    background: color(error);
}
```

```tsx
// 使用（React）
import styles from "./Button.module.scss";

function Button({ variant = "primary", children }) {
    return (
        <button
            className={`${styles.button} ${styles[variant]}`}
        >
            {children}
        </button>
    );
}
```

### Tailwind CSS + SCSS 共存

```scss
// ⭐ Tailwind 的自定义层 + SCSS 变量
@use "tokens" as *;

@tailwind base;
@tailwind components;
@tailwind utilities;

// ⭐ 自定义组件层
@layer components {
    .btn {
        @apply px-4 py-2 rounded font-medium transition-colors;
    }

    .btn-primary {
        @apply btn;
        background: color(brand-500);
        color: white;

        &:hover {
            background: color(brand-600);
        }
    }
}

// ⭐ 自定义工具层
@layer utilities {
    .text-balance {
        text-wrap: balance;
    }
}
```

---

## 九、迁移策略：原生 CSS → 预处理器

### 渐进迁移路线

```
阶段一：原生 CSS
├── 使用 CSS 变量（--primary, --spacing）
├── 使用 calc() 运算
├── 使用新的选择器（:has(), :where()）

阶段二：引入 PostCSS
├── Autoprefixer 自动加前缀
├── postcss-preset-env 使用未来特性
├── postcss-nesting（原生嵌套）

阶段三：引入 SCSS
├── 变量 + 嵌套（最小改动）
├── Mixin 抽取重复代码
├── @use 模块化管理

阶段四：全面工程化
├── 设计 Token 系统
├── BEM + 嵌套命名规范
├── CSS Modules + SCSS
├── 构建时全局注入变量
```

### 何时不需要预处理器

```css
/* ⭐ 现代原生 CSS 已经能解决很多问题 */

/* 1. CSS 变量解决主题问题 */
:root {
    --primary: #3498db;
    --spacing: 16px;
}

.card {
    color: var(--primary);
    padding: var(--spacing);
}

/* 2. calc() 解决运算问题 */
.container {
    width: calc(100% - 40px);
}

/* 3. 原生嵌套（2023+ 标准）*/
.card {
    &__title { font-weight: bold; }
    &:hover { opacity: 0.9; }
}

/* 4. :where() / :is() 降低优先级 */
:where(.card) {
    border-radius: 8px;
}
```

> [!tip] **选择建议**
> | 场景 | 推荐方案 |
> |:-----|:---------|
> | 个人小项目 | 原生 CSS + CSS 变量 |
> | 需要兼容旧浏览器 | 原生 CSS + PostCSS |
> | 中大型项目 | **SCSS + PostCSS** |
> | React 组件项目 | CSS Modules + SCSS |
> | 工具类优先 | Tailwind CSS |
> | 维护旧项目 | 保持已有方案 |

---

## 十、面试常见问题

### 1. CSS 预处理器解决了什么问题？

> 预处理器给 CSS 带来了编程能力：**变量**统一管理值、**嵌套**反映 HTML 结构、**Mixin** 复用代码片段、**函数与运算**动态计算值、**模块化**拆分管理。核心目标是提升 CSS 的可维护性和开发效率。

### 2. SCSS 中的 @mixin 和 @extend 有什么区别？

> `@mixin` 将样式复制到每个 `@include` 的位置，支持传参和 `@content`，输出体积较大但灵活。`@extend` 将选择器合并到一组，减少重复代码但不支持传参。**推荐优先使用 Mixin**，因为 extend 可能导致意外的选择器组合和样式污染。

### 3. CSS 变量和 SCSS 变量有什么区别？

> SCSS 变量在**编译时**替换，不能动态改变。CSS 变量在**运行时**生效，可通过 JS 修改，支持媒体查询。**最佳实践**：用 CSS 变量管理主题（`--primary`），用 SCSS 变量管理构建时的值（间距、断点）。

### 4. PostCSS 和 Sass 是什么关系？

> 它们不是竞争关系而是**互补关系**。Sass 提供嵌套、Mixin 等编程能力，PostCSS 通过插件处理兼容性和未来特性。通常一起使用：**Sass 写源码 → PostCSS 处理前缀 → 产出原生 CSS**。

### 5. @import 和 @use 的区别？

> Sass 旧版的 `@import` 会污染全局命名空间，已被**废弃**。`@use` 创建独立的命名空间，避免变量冲突，且只引入一次。新项目应该全部使用 `@use` / `@forward`。

### 6. Scss 中 & 代表什么？

> `&` 代表**当前父选择器的引用**。常用于：`:hover` 伪类（`&:hover`）、BEM 修饰符（`&--primary`）、父选择器拼接（`&-title`）、修改上下文（`.dark-mode &`）。

### 7. 什么是设计 Token？和预处理器如何结合？

> 设计 Token 是设计系统中所有可复用值的集合（颜色、间距、字体等），用 `map` 存储，配合 Sass 函数取值。好处是保证设计一致性，修改 Token 值全局生效。

### 8. 如何组织大型项目的 SCSS？

> ```
> styles/
> ├── _tokens.scss        # 设计 Token（变量）
> ├── _mixins.scss        # 混入
> ├── _functions.scss     # 函数
> ├── _reset.scss         # 重置样式
> ├── _typography.scss    # 排版
> ├── _grid.scss          # 网格系统
> ├── components/         # 组件样式
> │   ├── _button.scss
> │   └── _card.scss
> ├── pages/              # 页面样式
> │   ├── _home.scss
> │   └── _about.scss
> └── main.scss           # 入口（@use 所有模块）
> ```

### 9. 团队中如何统一预处理器风格？

> - 统一使用 SCSS 语法
> - 使用 `stylelint` 自动检查
> - 嵌套不超过 3 层
> - BEM 命名规范
> - 使用 `@use` 而非 `@import`
> - 全局变量和 Mixin 集中管理
> - 代码审查关注样式质量

### 10. 现代 CSS 已经支持嵌套，是否还需要预处理器？

> 原生 CSS 嵌套（2023+）解决了嵌套问题，但变量、Mixin、函数、循环、模块系统等仍然是预处理器的优势。对于复杂项目，**SCSS + PostCSS** 的组合仍然是行业的最佳实践。简单项目可以只用原生 CSS + CSS 变量。

---

> [!tip] **学习路径建议**
> 1. **入门**：理解预处理器概念 → 变量 → 嵌套 → Mixin
> 2. **进阶**：@extend → 函数 → 条件/循环 → 模块化 @use
> 3. **深入**：BEM + 预处理器 → 设计 Token 系统 → 主题系统
> 4. **工程化**：Vite/Webpack 集成 → PostCSS 插件 → CSS Modules
> 5. **拓展**：对比熟悉 Less/Stylus → 理解 CSS 原生 vs 预处理器边界
