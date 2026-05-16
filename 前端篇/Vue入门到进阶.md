# Vue 入门到进阶

## 一、Vue 概述

### 什么是 Vue

**Vue（读音 /vjuː/，类似 view）** 是一款用于构建用户界面的**渐进式框架**。与 React、Angular 并称前端三大框架。

| 特性 | 说明 |
|:----:|------|
| **渐进式** | 可以从一个 CDN 标签开始，逐步引入路由、状态管理等 |
| **响应式** | 数据变化自动更新视图，无需手动操作 DOM |
| **组件化** | 页面由独立、可复用的组件构成 |
| **声明式** | 只需描述数据和 UI 的关系，无需关心如何操作 DOM |

### 版本简史

|    版本     |  发布时间   | 说明                                      |
| :-------: | :-----: | --------------------------------------- |
| **Vue 2** |  2016   | ❌ 2023.12 已停止维护                         |
| **Vue 3** | 2020.9  | ✅ **当前标准**，Composition API + TypeScript |
|  Vue 3.3  | 2023.5  | 泛型组件、defineOptions                      |
|  Vue 3.4  | 2023.12 | 响应式系统重写（性能提升）                           |
|  Vue 3.5  |  2024   | 进一步优化                                   |

> [!warning] **新项目请直接使用 Vue 3**，Vue 2 已停止维护，不再有新功能和安全更新。

### 快速开始

```bash
# 方式一：Vite 创建项目（⭐ 推荐）
npm create vue@latest      # 或
npm create vite@latest my-app -- --template vue
# 然后选择需要的功能（TypeScript、Router、Pinia 等）

cd my-app
npm install
npm run dev

# 方式二：CDN 直接使用（快速体验）
# <script src="https://unpkg.com/vue@3/dist/vue.global.prod.js"></script>
```

### 项目结构

```
my-app/
├── src/
│   ├── App.vue                # 根组件
│   ├── main.js                # 入口文件
│   ├── components/            # 组件
│   ├── views/                 # 页面（路由视图）
│   ├── router/                # 路由配置
│   ├── stores/                # 状态管理（Pinia）
│   ├── composables/           # 组合式函数
│   ├── assets/                # 静态资源
│   └── styles/                # 全局样式
├── public/
├── index.html                 # HTML 入口
├── vite.config.js             # Vite 配置
└── package.json
```

### 创建一个 Vue 应用

```javascript
// main.js
import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import { createPinia } from "pinia";

const app = createApp(App);

app.use(router);        // 注册路由
app.use(createPinia()); // 注册状态管理
app.mount("#app");      // 挂载到 HTML 元素
```

### Vue 单文件组件（SFC）⭐

```vue
<!-- ⭐ 单文件组件 (Single File Component) 是 Vue 的核心开发方式 -->
<script setup>
// 组合式 API（推荐）
import { ref, onMounted } from "vue";

const count = ref(0);

function increment() {
    count.value++;
}

onMounted(() => {
    console.log("组件已挂载");
});
</script>

<template>
    <button @click="increment">
        点击了 {{ count }} 次
    </button>
</template>

<style scoped>
/* scoped 表示样式仅作用于当前组件，不影响全局 */
button {
    padding: 8px 16px;
    background: #42b883;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}
</style>
```

> [!tip] **推荐**：新项目一律使用 `<script setup>` + 组合式 API，这是 Vue 3 的官方推荐写法。

---

## 二、模板语法

### 文本插值

```vue
<script setup>
const msg = "Hello, Vue!";
const html = "<strong>粗体文本</strong>";
const number = 42;
const isActive = true;
</script>

<template>
    <!-- ⭐ 双大括号：文本插值 -->
    <p>{{ msg }}</p>

    <!-- 支持任意 JavaScript 表达式 -->
    <p>{{ number + 1 }}</p>
    <p>{{ isActive ? "激活" : "未激活" }}</p>
    <p>{{ msg.split("").reverse().join("") }}</p>

    <!-- ⚠️ 只能写表达式，不能写语句 -->
    <!-- ❌ {{ if (ok) { return msg } }} -->

    <!-- v-html 输出原始 HTML（⚠️ XSS 风险，不要用用户输入） -->
    <div v-html="html"></div>
</template>
```

### 指令（Directives）一览

| 指令 | 缩写 | 作用 |
|:----:|:----:|------|
| `v-bind` | `:` | 动态绑定属性 |
| `v-on` | `@` | 绑定事件 |
| `v-if` / `v-else-if` / `v-else` | — | 条件渲染 |
| `v-show` | — | 条件显示（CSS display 切换） |
| `v-for` | — | 列表渲染 |
| `v-model` | — | 双向绑定 |
| `v-html` | — | 输出 HTML |
| `v-text` | — | 输出纯文本 |
| `v-once` | — | 只渲染一次 |
| `v-cloak` | — | 防止闪烁 |
| `v-pre` | — | 跳过编译（显示原始标签） |

### v-bind（属性绑定）⭐

```vue
<script setup>
import { ref } from "vue";

const url = ref("https://vuejs.org");
const imageUrl = ref("https://via.placeholder.com/200");
const className = ref("active");
const isDisabled = ref(true);
const style = ref({ color: "red", fontSize: "20px" });
</script>

<template>
    <!-- ⭐ 完整写法 -->
    <a v-bind:href="url">Vue 官网</a>

    <!-- ⭐ 缩写（推荐） -->
    <a :href="url">Vue 官网</a>
    <img :src="imageUrl" :alt="description">

    <!-- 动态绑定 class ⭐ -->
    <div :class="className">动态类名</div>
    <div :class="{ active: isActive, disabled: isDisabled }">对象语法</div>
    <div :class="['base', isActive ? 'active' : '']">数组语法</div>

    <!-- 动态绑定 style -->
    <div :style="style">动态样式</div>
    <div :style="{ color: activeColor, fontSize: size + 'px' }">对象样式</div>

    <!-- 动态绑定布尔属性 -->
    <button :disabled="isDisabled">禁用按钮</button>

    <!-- 动态绑定多个属性 -->
    <div v-bind="{ id: 'app', class: 'container', 'data-id': 123 }"></div>
</template>
```

### v-on（事件绑定）⭐

```vue
<script setup>
import { ref } from "vue";

const count = ref(0);
const name = ref("");

function greet(msg) {
    alert(msg);
}

function handleKeydown(e) {
    console.log(e.key);
}

function onSubmit() {
    console.log("提交");
}
</script>

<template>
    <!-- ⭐ 完整写法 -->
    <button v-on:click="count++">+1</button>

    <!-- ⭐ 缩写 @（推荐） -->
    <button @click="count++">+1</button>
    <button @click="greet('你好')">带参数</button>

    <!-- 事件对象 $event -->
    <button @click="greet($event)">传递事件对象</button>

    <!-- ⭐ 事件修饰符（链式调用） -->
    <!-- .stop    阻止冒泡 -->
    <!-- .prevent 阻止默认行为 -->
    <!-- .once    只触发一次 -->
    <!-- .capture 捕获阶段触发 -->
    <!-- .self    只有 event.target 是自身时触发 -->
    <!-- .passive 不调用 preventDefault -->

    <form @submit.prevent="onSubmit">          <!-- 阻止表单提交刷新 -->
        <a @click.stop="handleClick">阻止冒泡</a>
        <button @click.once="handleOnce">只执行一次</button>
    </form>

    <!-- ⭐ 按键修饰符 -->
    <input @keyup.enter="submit">              <!-- 回车触发 -->
    <input @keyup.esc="cancel">                <!-- ESC -->
    <input @keyup.ctrl.enter="submit">         <!-- Ctrl + Enter -->
    <input @keyup.alt.s="/">                   <!-- Alt + / -->

    <!-- ⭐ 鼠标修饰符 -->
    <div @click.left="leftClick">左键</div>
    <div @click.middle="middleClick">中键</div>
    <div @click.right.prevent="rightClick">右键（阻止菜单）</div>
</template>
```

### 双向绑定（v-model）⭐

```vue
<script setup>
import { ref } from "vue";

const name = ref("");
const email = ref("");
const gender = ref("");
const agree = ref(false);
const city = ref("");
const intro = ref("");
const count = ref(0);
</script>

<template>
    <!-- ⭐ 文本输入 -->
    <input v-model="name" placeholder="请输入姓名">
    <p>你好，{{ name }}</p>

    <!-- v-model 等价于：-->
    <input :value="name" @input="name = $event.target.value">

    <!-- 多行文本 -->
    <textarea v-model="intro"></textarea>

    <!-- ⭐ 复选框 -->
    <input type="checkbox" v-model="agree" id="agree">
    <label for="agree">同意条款</label>

    <!-- ⭐ 单选 -->
    <input type="radio" value="male" v-model="gender"> 男
    <input type="radio" value="female" v-model="gender"> 女

    <!-- ⭐ 下拉框 -->
    <select v-model="city">
        <option value="">请选择城市</option>
        <option value="beijing">北京</option>
        <option value="shanghai">上海</option>
    </select>

    <!-- ⭐ v-model 修饰符 -->
    <input v-model.trim="name">           <!-- 自动去除首尾空格 -->
    <input v-model.number="count">        <!-- 自动转为数字类型 -->
    <input v-model.lazy="email">          <!-- 懒同步（change 事件触发，不是 input）-->
</template>
```

> [!tip] **模板语法要点**
> - `{{ }}` 只能写表达式，不能写语句
> - 缩写 `@click` = `v-on:click`，`:src` = `v-bind:src`
> - 事件修饰符可链式：`@click.stop.prevent`
> - `v-model` 本质是语法糖：`:value` + `@input`

---

## 三、响应式数据

### ref / reactive / computed / watch ⭐

```vue
<script setup>
import { ref, reactive, computed, watch, watchEffect } from "vue";

// ============ ref（基本类型 + 对象）============
const count = ref(0);                    // 基本类型
const user = ref({ name: "Alice" });     // 对象也可用 ref

console.log(count.value);  // 访问 ref 需要 .value（模板中不需要）

function increment() {
    count.value++;
    user.value.name = "Bob";
}

// ============ reactive（仅限对象，自动深层响应）============
const state = reactive({
    user: { name: "Alice", age: 25 },
    items: [1, 2, 3],
});

// reactive 不用 .value，直接访问
state.user.name = "Bob";
state.items.push(4);

// ============ ref vs reactive 选型 ============
// ⭐ 推荐统一用 ref（Vue 官方推荐）
// 优点：类型友好、可解构不丢失响应性、心智模型统一
// reactive 的限制：不能重新赋值、不能解构、不能用于基本类型

// ============ computed（计算属性）⭐ ============
const firstName = ref("张");
const lastName = ref("三");

// 只读计算属性
const fullName = computed(() => {
    return `${firstName.value}${lastName.value}`;
});

// 可写计算属性（少用）
const fullNameWritable = computed({
    get() { return `${firstName.value}${lastName.value}`; },
    set(val) {
        [firstName.value, lastName.value] = [val[0], val.slice(1)];
    },
});

// ============ watch（监听）⭐ ============
// 监听单个 ref
watch(count, (newVal, oldVal) => {
    console.log(`count 从 ${oldVal} 变为 ${newVal}`);
});

// 监听多个
watch([count, firstName], ([newCount, newName], [oldCount, oldName]) => {
    console.log("多个值变化了");
});

// ⭐ watch 选项
watch(
    () => state.user,           // 监听 reactive 的某个属性
    (newVal, oldVal) => {
        console.log("user 变化:", newVal);
    },
    {
        deep: true,             // ⭐ 深度监听（嵌套对象变化也能检测）
        immediate: true,        // ⭐ 立即执行一次（初始时）
        flush: "post",          // DOM 更新后执行（默认 pre）
    }
);

// ⭐ watchEffect（自动收集依赖，无需指定监听目标）
watchEffect(() => {
    // 在此函数中使用的响应式数据变化时会自动重新执行
    console.log("count 或 name 变化了:", count.value, firstName.value);
});
</script>

<template>
    <p>count: {{ count }}</p>       <!-- 模板中不需要 .value -->
    <p>姓名: {{ fullName }}</p>
    <button @click="increment">+1</button>
</template>
```

### 响应式原理（浅谈）

```
ref/reactive 通过 Proxy 拦截对数据的读写操作

读取属性 → 收集依赖（谁在用它）
修改属性 → 触发依赖（通知所有用到的地方更新）

Vue 3 的 Proxy 相比 Vue 2 的 defineProperty：
  ✅ 可以检测数组索引/长度的变化
  ✅ 可以检测对象新增/删除属性
  ❌ 不需要 Vue.set / Vue.delete
  ❌ 不需要 this.$set
```

---

## 四、条件与列表渲染

### v-if / v-show

```vue
<script setup>
import { ref } from "vue";

const show = ref(true);
const status = ref("success");
</script>

<template>
    <!-- ⭐ v-if / v-else-if / v-else（真正的条件渲染，DOM 会被销毁/重建）-->
    <div v-if="status === 'success'">✅ 操作成功</div>
    <div v-else-if="status === 'error'">❌ 操作失败</div>
    <div v-else>⏳ 处理中...</div>

    <!-- ⭐ v-show（CSS display 切换，元素始终存在）-->
    <div v-show="show">这个元素始终在 DOM 中</div>

    <!-- ⭐ v-if 和 v-show 的选择 -->
    <!-- v-if：适合运行时很少切换的场景 -->
    <!-- v-show：适合频繁切换的场景（如 Tabs、折叠面板）-->
</template>
```

### v-for（列表渲染）⭐

```vue
<script setup>
import { ref } from "vue";

const items = ref([
    { id: 1, name: "苹果", price: 5 },
    { id: 2, name: "香蕉", price: 3 },
    { id: 3, name: "橘子", price: 4 },
]);

const newItem = ref({ name: "", price: 0 });

// 对象数据
const user = ref({ name: "Alice", age: 25, role: "admin" });

function addItem() {
    items.value.push({ ...newItem.value, id: Date.now() });
}

function removeItem(id) {
    items.value = items.value.filter(item => item.id !== id);
}
</script>

<template>
    <!-- ⭐ v-for="(item, index) in array" :key 必须加！-->
    <ul>
        <li v-for="(item, index) in items" :key="item.id">
            {{ index + 1 }}. {{ item.name }} - ¥{{ item.price }}
            <button @click="removeItem(item.id)">删除</button>
        </li>
    </ul>

    <!-- 遍历对象 -->
    <div v-for="(value, key, index) in user" :key="key">
        {{ index }}. {{ key }}: {{ value }}
    </div>

    <!-- 遍历数字范围 -->
    <span v-for="n in 5" :key="n">{{ n }}</span>

    <!-- ⭐ v-for 与 v-if 同时使用 -->
    <!-- ❌ 不要同时用在同一元素上（v-if 优先级更高，无法访问 v-for 变量）-->
    <!-- ✅ 方案一：用 template 包装 -->
    <template v-for="item in items" :key="item.id">
        <li v-if="item.price > 3">{{ item.name }}</li>
    </template>
    <!-- ✅ 方案二：用计算属性过滤 -->
    <!-- const expensiveItems = computed(() => items.value.filter(i => i.price > 3)) -->
</template>
```

> [!warning] **`:key` 的重要性**
> - Vue 通过 `:key` 来追踪每个节点的身份，优化 DOM 复用
> - 最好用**唯一 ID** 而不是数组索引（除非列表是静态的）
> - 不加 `:key` 或使用索引作为 key，在列表增删时会导致渲染 Bug

---

## 五、组件基础

### 组件定义与使用

```vue
<!-- MyButton.vue -->
<script setup>
// 组件可以有 props、事件、插槽等
</script>

<template>
    <button class="my-btn">
        <slot />   <!-- ⭐ 插槽：接收父组件传入的内容 -->
    </button>
</template>

<style scoped>
.my-btn {
    padding: 8px 20px;
    background: #42b883;
    color: white;
    border: none;
    border-radius: 6px;
    cursor: pointer;
}
</style>
```

```vue
<!-- 使用组件 -->
<script setup>
import MyButton from "./MyButton.vue";
import MyCard from "./MyCard.vue";   // 自动注册
</script>

<template>
    <MyButton> 点击我 </MyButton>
    <my-button> 也可以 kebab-case </my-button>
</template>
```

### Props（父传子）⭐

```vue
<!-- ChildComponent.vue -->
<script setup>
// ⭐ 方式一：简单声明
defineProps(["title", "count", "items"]);

// ⭐ 方式二：类型声明（推荐）
defineProps({
    title: {
        type: String,
        required: true,            // 必填
    },
    count: {
        type: Number,
        default: 0,                // 默认值
        validator: (val) => val >= 0,  // 自定义校验
    },
    items: {
        type: Array,
        default: () => [],         // ⚠️ 对象/数组默认值要用工厂函数
    },
    status: {
        type: String,
        default: "info",
    },
    // 多种类型
    value: [String, Number],
});

// ⭐ 方式三：TypeScript 泛型（推荐）
// defineProps<{
//     title: string
//     count?: number
//     items: string[]
// }>()
</script>

<template>
    <div class="card">
        <h3>{{ title }}</h3>
        <p>数量: {{ count }}</p>
        <ul>
            <li v-for="item in items" :key="item">{{ item }}</li>
        </ul>
    </div>
</template>
```

```vue
<!-- 父组件传递 props -->
<script setup>
import ChildComponent from "./ChildComponent.vue";

const userItems = ["苹果", "香蕉", "橘子"];
</script>

<template>
    <!-- 传递静态值 -->
    <ChildComponent title="水果列表" count="5" />

    <!-- 传递动态值（: 绑定）-->
    <ChildComponent
        :title="'水果列表'"
        :count="userItems.length"
        :items="userItems"
        :status="someVariable"
    />

    <!-- 展开对象传递 -->
    <ChildComponent v-bind="{ title: '标题', count: 3, items: userItems }" />
</template>
```

### Emit（子传父）⭐

```vue
<!-- ChildComponent.vue -->
<script setup>
// ⭐ 声明事件
const emit = defineEmits(["update", "delete"]);

function handleUpdate() {
    emit("update", { id: 1, name: "新数据" });  // 传递数据
}

function handleDelete(id) {
    emit("delete", id);
}

// TypeScript 版本
// const emit = defineEmits<{
//     update: [data: { id: number; name: string }]
//     delete: [id: number]
// }>()
</script>

<template>
    <button @click="handleUpdate">更新</button>
    <button @click="handleDelete(1)">删除</button>
</template>
```

```vue
<!-- 父组件监听事件 -->
<script setup>
import ChildComponent from "./ChildComponent.vue";

function onUpdate(data) {
    console.log("收到更新:", data);
}

function onDelete(id) {
    console.log("删除:", id);
}
</script>

<template>
    <ChildComponent @update="onUpdate" @delete="onDelete" />
</template>
```

### v-model 组件

```vue
<!-- InputWrapper.vue（自定义 v-model 组件）-->
<script setup>
defineProps({
    modelValue: String,              // v-model 默认属性名
});

const emit = defineEmits(["update:modelValue"]);

function onInput(e) {
    emit("update:modelValue", e.target.value);
}

// ⭐ 多个 v-model 绑定
// defineProps({ firstName: String, lastName: String })
// const emit = defineEmits(["update:firstName", "update:lastName"])
</script>

<template>
    <div class="input-group">
        <label>自定义输入</label>
        <input
            :value="modelValue"
            @input="onInput"
            class="custom-input"
        >
    </div>
</template>
```

```vue
<!-- 使用 -->
<script setup>
import { ref } from "vue";
import InputWrapper from "./InputWrapper.vue";

const text = ref("");

// 多个 v-model
// const firstName = ref("")
// const lastName = ref("")
</script>

<template>
    <!-- 等价于 :modelValue="text" + @update:modelValue="text = $event" -->
    <InputWrapper v-model="text" />
    <p>输入内容: {{ text }}</p>

    <!-- 多个 v-model -->
    <!-- <UserForm v-model:firstName="firstName" v-model:lastName="lastName" /> -->
</template>
```

### 插槽（Slot）⭐

```vue
<!-- Card.vue -->
<script setup>
defineProps({ title: String });
</script>

<template>
    <div class="card">
        <div class="card-header">
            <!-- ⭐ 具名插槽 -->
            <slot name="header" :defaultTitle="title">
                默认标题（没有传入 header 时显示）
            </slot>
        </div>

        <div class="card-body">
            <!-- ⭐ 默认插槽 -->
            <slot :data="items">没有内容</slot>
        </div>

        <div class="card-footer">
            <slot name="footer" />
        </div>
    </div>
</template>
```

```vue
<!-- 使用插槽 -->
<script setup>
import Card from "./Card.vue";
</script>

<template>
    <Card title="用户信息">
        <!-- 默认插槽 -->
        <p>这是卡片主体内容</p>

        <!-- ⭐ 具名插槽 -->
        <template #header="slotProps">
            <h2>{{ slotProps.defaultTitle }}</h2>
        </template>

        <!-- 简写 # -->
        <template #footer>
            <button>确定</button>
            <button>取消</button>
        </template>
    </Card>
</template>
```

> [!info] **组件通信方式**
>
> | 方式 | 场景 | 方向 |
> |:----:|------|:----:|
> | **`props`** | 父传子 | 父 → 子 |
> | **`emit`** | 子传父 | 子 → 父 |
> | **`v-model`** | 双向绑定 | 父 ↔ 子 |
> | **`provide/inject`** | 深层传递 | 祖先 → 后代 |
> | **Pinia** | 全局状态 | 任意组件 |
> | **`slot`** | 父传模板内容 | 父 → 子（结构） |

---

## 六、组件进阶

### provide / inject

```vue
<!-- 祖先组件（App.vue 或任意父组件）-->
<script setup>
import { provide, ref } from "vue";

const theme = ref("light");
const user = ref({ name: "Alice" });

// ⭐ 提供数据给所有后代
provide("theme", theme);
provide("user", user);
// provide("key", "value")  — key 用 Symbol 避免命名冲突

// ⭐ 提供方法
const updateTheme = (newTheme) => { theme.value = newTheme; };
provide("updateTheme", updateTheme);
</script>
```

```vue
<!-- 任意后代组件（深层嵌套也能用）-->
<script setup>
import { inject } from "vue";

// ⭐ 注入祖先提供的数据
const theme = inject("theme", "light");         // 第二个参数是默认值
const user = inject("user");
const updateTheme = inject("updateTheme");

// ⚠️ inject 的数据是响应式的（祖先修改了，后代也会更新）
</script>

<template>
    <div :class="`app-${theme}`">
        <p>当前用户: {{ user.name }}</p>
        <button @click="updateTheme('dark')">切换暗色主题</button>
    </div>
</template>
```

### 动态组件

```vue
<script setup>
import { ref } from "vue";
import TabA from "./TabA.vue";
import TabB from "./TabB.vue";
import TabC from "./TabC.vue";

const currentTab = ref("TabA");
const tabs = {
    TabA, TabB, TabC,
};
</script>

<template>
    <!-- ⭐ :is 动态切换组件 -->
    <component :is="tabs[currentTab]"></component>

    <button @click="currentTab = 'TabA'">Tab A</button>
    <button @click="currentTab = 'TabB'">Tab B</button>
</template>
```

### 异步组件

```vue
<script setup>
import { defineAsyncComponent } from "vue";

// ⭐ 异步加载组件（只在需要时才加载）
const HeavyComponent = defineAsyncComponent(() =>
    import("./HeavyComponent.vue")
);

// ⭐ 带加载状态
const AsyncComponent = defineAsyncComponent({
    loader: () => import("./HeavyComponent.vue"),
    loadingComponent: () => import("./Loading.vue"),     // 加载中
    errorComponent: () => import("./Error.vue"),         // 加载失败
    delay: 200,             // 延迟 200ms 显示 loading
    timeout: 30000,         // 30s 超时
});
</script>

<template>
    <HeavyComponent />
    <AsyncComponent />
</template>
```

### keep-alive（缓存组件）

```vue
<script setup>
import { ref } from "vue";

const currentView = ref("Home");
</script>

<template>
    <!-- ⭐ keep-alive：切换时缓存组件状态，不销毁 -->
    <KeepAlive :max="10">    <!-- 最多缓存 10 个 -->
        <component :is="currentView" />
    </KeepAlive>

    <!-- 条件缓存 -->
    <KeepAlive :include="["Home", "About"]">
        <component :is="currentView" />
    </KeepAlive>

    <button @click="currentView = 'Home'">首页</button>
    <button @click="currentView = 'About'">关于</button>
</template>
```

### Teleport（传送门）

```vue
<script setup>
const modalOpen = ref(false);
</script>

<template>
    <!-- ⭐ Teleport 将子元素渲染到指定 DOM 位置（如 body 下）-->
    <Teleport to="body">
        <div v-if="modalOpen" class="modal-overlay">
            <div class="modal-content">
                <p>这个弹窗渲染在 body 下</p>
                <button @click="modalOpen = false">关闭</button>
            </div>
        </div>
    </Teleport>

    <!-- Teleport 到 CSS 选择器目标 -->
    <Teleport to="#app-header">
        <span>显示在页头区域</span>
    </Teleport>
</template>
```

---

## 七、Composition API（组合式 API）

### Options API vs Composition API

```vue
<!-- ⭐ 选项式 API（Options API）— Vue 2 风格 -->
<script>
export default {
    data() {
        return { count: 0, name: "Alice" };
    },
    computed: {
        double() { return this.count * 2; },
    },
    watch: {
        count(newVal) { console.log(newVal); },
    },
    methods: {
        increment() { this.count++; },
    },
    mounted() { console.log("mounted"); },
};
</script>
```

```vue
<!-- ⭐ 组合式 API（Composition API）— Vue 3 推荐 ⭐ -->
<script setup>
import { ref, computed, watch, onMounted } from "vue";

const count = ref(0);
const name = ref("Alice");

const double = computed(() => count.value * 2);

watch(count, (newVal) => console.log(newVal));

function increment() { count.value++; }

onMounted(() => console.log("mounted"));
</script>
```

| 对比 | Options API | Composition API |
|:----:|:-----------:|:---------------:|
| **代码组织** | 按选项分散（data、methods、computed） | 按功能聚合 |
| **逻辑复用** | mixins（不清晰） | **composables**（清晰） |
| **TypeScript** | 支持一般 | **支持优秀** |
| **this** | 依赖 this（指向实例） | 不依赖 this |
| **推荐** | 简单组件/已有项目 | **新项目/复杂组件** ⭐ |

### 组合式 API 的核心优势：逻辑复用 ⭐

```vue
<!-- 选项式 API：逻辑分散在多个选项中 -->
<script>
export default {
    data() { return { x: 0, y: 0, count: 0 }; },
    mounted() { window.addEventListener("mousemove", this.handler); },
    beforeUnmount() { window.removeEventListener("mousemove", this.handler); },
    methods: {
        handler(e) { this.x = e.clientX; this.y = e.clientY; },
    },
};
</script>
```

```vue
<!-- 组合式 API：按功能提取为 composable -->
<script setup>
import { useMouse } from "./composables/useMouse";
import { useCounter } from "./composables/useCounter";

// ⭐ 逻辑被封装到独立的 composable 函数中
const { x, y } = useMouse();       // 鼠标位置逻辑
const { count, increment } = useCounter();  // 计数逻辑
</script>
```

```javascript
// composables/useMouse.js — 可复用的组合式函数 ⭐
import { ref, onMounted, onUnmounted } from "vue";

export function useMouse() {
    const x = ref(0);
    const y = ref(0);
    const position = ref({ x: 0, y: 0 });

    function update(e) {
        x.value = e.clientX;
        y.value = e.clientY;
        position.value = { x: e.clientX, y: e.clientY };
    }

    onMounted(() => window.addEventListener("mousemove", update));
    onUnmounted(() => window.removeEventListener("mousemove", update));

    // 返回响应式数据
    return { x, y, position };
}
```

```javascript
// composables/useFetch.js — 数据请求 ⭐
import { ref, watchEffect, toValue } from "vue";

export function useFetch(url) {
    const data = ref(null);
    const error = ref(null);
    const loading = ref(true);

    async function fetchData() {
        loading.value = true;
        error.value = null;

        try {
            const response = await fetch(toValue(url));  // toValue 支持 ref 和普通值
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            data.value = await response.json();
        } catch (e) {
            error.value = e.message;
        } finally {
            loading.value = false;
        }
    }

    // url 变化时自动重新请求
    watchEffect(() => {
        if (toValue(url)) fetchData();
    });

    return { data, error, loading, refresh: fetchData };
}

// 使用
// const { data, error, loading } = useFetch("/api/users");
```

---

## 八、生命周期

### 生命周期图示

```
创建
  setup() / <script setup>         ← 组件创建前
      │
  beforeCreate (Options API only)  ← 实例初始化前
      │
  created (Options API only)       ← 实例创建完成
      │
  beforeMount                      ← 挂载前
      │
  mounted                          ← ⭐ 挂载完成（DOM 可用）
      │
  运行中...
  （数据变化时）                    ← 组件更新
  beforeUpdate                     ← 更新前
  updated                          ← 更新完成
      │
  卸载时
  beforeUnmount                    ← 卸载前（清理定时器）
      │
  unmounted                        ← 卸载完成
```

### 生命周期钩子

```vue
<script setup>
import { ref, onMounted, onBeforeMount, onBeforeUpdate, onUpdated,
         onBeforeUnmount, onUnmounted, onActivated, onDeactivated } from "vue";

const count = ref(0);
let timer = null;

// ⭐ mounted — DOM 已挂载，可访问元素、发请求
onMounted(() => {
    console.log("组件已挂载");
    timer = setInterval(() => {
        console.log("定时器运行中...");
    }, 1000);
});

// 更新前
onBeforeUpdate(() => {
    console.log("组件即将更新");
});

// 更新后
onUpdated(() => {
    console.log("组件已更新");
});

// ⭐ beforeUnmount — 清理工作（清除定时器、取消订阅）
onBeforeUnmount(() => {
    console.log("组件即将卸载");
    if (timer) {
        clearInterval(timer);   // 防止内存泄漏
    }
});

onUnmounted(() => {
    console.log("组件已卸载");
});

// keep-alive 专用
onActivated(() => console.log("组件被激活"));
onDeactivated(() => console.log("组件被停用"));
</script>
```

### 常见错误：生命周期中的异步

```javascript
// ❌ 错误：在 setup 中直接使用 await（会导致组件先挂载再执行）
const data = await fetchData();
onMounted(() => {
    // 此时组件可能已经挂载了
});

// ✅ 正确：在 onMounted 中执行异步操作
onMounted(async () => {
    const data = await fetchData();
    // 处理数据
});
```

> [!tip] **`<script setup>` 中的生命周期钩子**
> ```javascript
> // Options API         → Composition API
// beforeCreate        → setup() / <script setup>
// created             → setup() / <script setup>
// beforeMount         → onBeforeMount
// mounted             → onMounted
// beforeUpdate        → onBeforeUpdate
// updated             → onUpdated
// beforeUnmount       → onBeforeUnmount
// unmounted           → onUnmounted
// errorCaptured       → onErrorCaptured
// activated           → onActivated (keep-alive)
// deactivated         → onDeactivated (keep-alive)
> ```

---

## 九、Vue Router

### 安装与配置

```bash
npm install vue-router@4
```

```javascript
// router/index.js
import { createRouter, createWebHistory } from "vue-router";
import Home from "../views/Home.vue";
import About from "../views/About.vue";

// ⭐ 路由配置
const routes = [
    {
        path: "/",
        name: "home",
        component: Home,
    },
    {
        path: "/about",
        name: "about",
        component: About,
        meta: { title: "关于我们" },         // 路由元信息
    },
    {
        path: "/users",
        name: "users",
        // ⭐ 路由级代码分割（懒加载）
        component: () => import("../views/Users.vue"),
    },
    {
        // ⭐ 动态路由参数
        path: "/users/:id",
        name: "user-detail",
        component: () => import("../views/UserDetail.vue"),
        props: true,          // 将 params 作为 props 传入组件
    },
    {
        // ⭐ 嵌套路由
        path: "/dashboard",
        component: () => import("../views/Dashboard.vue"),
        children: [
            { path: "", redirect: { name: "dashboard-overview" } },
            { path: "overview", name: "dashboard-overview", component: () => import("../views/Overview.vue") },
            { path: "settings", name: "dashboard-settings", component: () => import("../views/Settings.vue") },
        ],
    },
    {
        // 404 页面
        path: "/:pathMatch(.*)*",
        name: "not-found",
        component: () => import("../views/NotFound.vue"),
    },
];

const router = createRouter({
    history: createWebHistory(),     // HTML5 历史模式（需要服务器支持）
    // history: createWebHashHistory(),  // Hash 模式（不用服务器配置）
    routes,
    scrollBehavior(to, from, savedPosition) {
        // 路由跳转时滚动到顶部
        if (savedPosition) return savedPosition;
        return { top: 0 };
    },
});

// ⭐ 导航守卫
router.beforeEach((to, from) => {
    // 页面标题
    document.title = to.meta.title || "My App";

    // 认证检查
    if (to.meta.requiresAuth && !isLoggedIn()) {
        return { name: "login", query: { redirect: to.fullPath } };
    }
});

router.afterEach((to, from) => {
    // 分析/统计
});

export default router;
```

### 在组件中使用

```vue
<script setup>
import { useRoute, useRouter } from "vue-router";
import { ref, watch } from "vue";

const route = useRoute();
const router = useRouter();

const userId = ref(route.params.id);      // 当前路由参数

// 监听路由参数变化（用户从 /users/1 导航到 /users/2）
watch(() => route.params.id, (newId) => {
    userId.value = newId;
    fetchUser(newId);
});

function goBack() {
    router.back();
}

function goToUser(id) {
    // ⭐ 编程式导航
    router.push({ name: "user-detail", params: { id } });
    // router.push("/users/123")
    // router.replace("/users/123")     // 替换当前历史记录
}

function goWithQuery() {
    router.push({ path: "/users", query: { page: 2, size: 20 } });
}
</script>

<template>
    <!-- ⭐ <router-link> 声明式导航 -->
    <nav>
        <router-link to="/">首页</router-link>
        <router-link :to="{ name: 'about' }">关于</router-link>
        <router-link :to="{ name: 'users' }">用户列表</router-link>
        <router-link
            :to="{ name: 'user-detail', params: { id: 1 } }"
        >用户 1</router-link>

        <!-- active class 加粗 -->
        <router-link to="/" active-class="active" exact>首页</router-link>
    </nav>

    <!-- ⭐ 路由出口 -->
    <router-view />

    <!-- 命名视图 -->
    <!-- <router-view name="sidebar" /> -->

    <button @click="goBack">返回</button>
    <button @click="goToUser(5)">跳转到用户 5</button>
</template>
```

### 导航守卫总结

| 守卫 | 作用 | 类型 |
|:----:|------|:----:|
| `beforeEach` | 全局前置守卫（认证、标题） | 全局 |
| `beforeResolve` | 全局解析守卫（数据预取后） | 全局 |
| `afterEach` | 全局后置钩子（分析） | 全局 |
| `beforeEnter` | 路由独享守卫 | 路由级 |
| `onBeforeRouteLeave` | 组件内离开守卫（未保存提醒） | 组件级 |
| `onBeforeRouteUpdate` | 组件内更新守卫 | 组件级 |

---

## 十、Pinia（状态管理）

### 安装与配置

```bash
npm install pinia
```

```javascript
// main.js
import { createPinia } from "pinia";
app.use(createPinia());
```

### 创建 Store ⭐

```javascript
// stores/counter.js
import { ref, computed } from "vue";
import { defineStore } from "pinia";

// ⭐ defineStore 定义状态仓库
// 第一个参数是 store 的唯一 ID
export const useCounterStore = defineStore("counter", () => {
    // ============ state（状态）============
    const count = ref(0);
    const name = ref("计数器");

    // ============ getters（计算属性）============
    const doubleCount = computed(() => count.value * 2);

    // ============ actions（方法）============
    function increment() {
        count.value++;
    }

    function decrement() {
        count.value--;
    }

    function reset() {
        count.value = 0;
    }

    // 异步 action
    async function fetchAndSet() {
        const data = await fetch("/api/count");
        count.value = data.count;
    }

    // ⭐ 返回需要暴露的内容
    return { count, name, doubleCount, increment, decrement, reset, fetchAndSet };
});
```

```javascript
// stores/user.js
import { ref, computed } from "vue";
import { defineStore } from "pinia";
import { loginAPI, logoutAPI } from "@/api/auth";

export const useUserStore = defineStore("user", () => {
    const token = ref(localStorage.getItem("token") || "");
    const userInfo = ref(null);

    const isLoggedIn = computed(() => !!token.value);

    async function login(username, password) {
        const res = await loginAPI({ username, password });
        token.value = res.token;
        userInfo.value = res.user;
        localStorage.setItem("token", res.token);
    }

    function logout() {
        token.value = "";
        userInfo.value = null;
        localStorage.removeItem("token");
    }

    return { token, userInfo, isLoggedIn, login, logout };
});
```

### 在组件中使用

```vue
<script setup>
import { useCounterStore } from "@/stores/counter";
import { useUserStore } from "@/stores/user";
import { storeToRefs } from "pinia";

const counter = useCounterStore();
const user = useUserStore();

// ⭐ 解构并保持响应性（必须用 storeToRefs）
const { count, doubleCount, name } = storeToRefs(counter);
// 普通方法可以直接解构
const { increment, decrement } = counter;

// 直接修改 state（灵活）
function directUpdate() {
    counter.count = 100;               // ✅ 直接修改
    counter.$patch({ count: 200 });    // ✅ 批量修改
    counter.$reset();                  // ✅ 重置为初始值
}
</script>

<template>
    <div>
        <h2>{{ name }}</h2>
        <p>count: {{ count }}</p>
        <p>double: {{ doubleCount }}</p>
        <button @click="increment">+1</button>
        <button @click="counter.decrement()">-1</button>
        <button @click="counter.reset()">重置</button>
    </div>

    <div v-if="user.isLoggedIn">
        <p>欢迎, {{ user.userInfo?.name }}</p>
        <button @click="user.logout()">退出</button>
    </div>
</template>
```

### Pinia vs Vuex

| 对比 | Vuex 4 | Pinia ⭐ |
|:----:|:------:|:--------:|
| **Vue 版本** | Vue 3 | Vue 3 |
| **TypeScript** | 支持一般 | **完美支持** |
| **代码体积** | 较大 | 极小（~1KB） |
| **DevTools** | 支持 | **支持更好** |
| **模块嵌套** | 模块嵌套复杂 | **扁平化，无嵌套** |
| **语法** | mutations + actions | 只有 actions |
| **状态重置** | 需要手写 | **内置 `$reset()`** |
| **推荐** | 不推荐新项目 | **新项目首选** ⭐ |

---

## 十一、自定义指令

```javascript
// ⭐ 全局自定义指令
// main.js 或 directives/index.js
import { createApp } from "vue";

const app = createApp(App);

app.directive("focus", {
    mounted(el) {
        el.focus();
    },
});

app.directive("highlight", {
    mounted(el, binding) {
        el.style.backgroundColor = binding.value || "yellow";
    },
    updated(el, binding) {
        el.style.backgroundColor = binding.value;
    },
});
```

```vue
<!-- 使用 -->
<script setup>
import { ref } from "vue";

// ⭐ 局部自定义指令
const vColor = {
    mounted(el, binding) {
        el.style.color = binding.value;
        // binding.value     → 指令的值
        // binding.arg       → 指令参数（v-color:red 的 arg 是 "red"）
        // binding.modifiers → 修饰符对象
    },
};

const highlightColor = ref("yellow");
</script>

<template>
    <input v-focus placeholder="自动获得焦点">
    <p v-highlight="'lightblue'">高亮文本</p>

    <!-- 带参数的指令 -->
    <p v-color="'red'">红色文字</p>

    <!-- 动态绑定 -->
    <p v-highlight="highlightColor">可改变的高亮</p>
</template>
```

### 自定义指令生命周期

```javascript
app.directive("my-directive", {
    // 绑定元素的父组件挂载时调用
    created(el, binding, vnode) {},
    // 在元素被插入到 DOM 前调用
    beforeMount(el, binding, vnode) {},
    // ⭐ 绑定元素的父组件及自身所有子节点都挂载后调用
    mounted(el, binding, vnode) {},
    // 绑定元素的父组件更新前调用
    beforeUpdate(el, binding, vnode) {},
    // 绑定元素的父组件及自身所有子节点都更新后调用
    updated(el, binding, vnode) {},
    // 绑定元素的父组件卸载前调用
    beforeUnmount(el, binding, vnode) {},
    // 绑定元素的父组件卸载后调用
    unmounted(el, binding, vnode) {},
});
```

---

## 十二、混入（Mixin）与插件

### Mixin（组合式 API 下不推荐）

```javascript
// mixins/userMixin.js — Vue 2 风格，Vue 3 推荐用 composables 替代
export const userMixin = {
    data() {
        return { user: null, loading: false };
    },
    mounted() {
        this.fetchUser();
    },
    methods: {
        async fetchUser() {
            this.loading = true;
            this.user = await fetch("/api/user").then(r => r.json());
            this.loading = false;
        },
    },
};
```

> [!warning] **Vue 3 中不推荐用 Mixin**，原因：命名冲突、来源不清晰、逻辑复用不灵活。改用 **Composables**（组合式函数）替代。

### 插件

```javascript
// plugins/toast.js — 插件示例
export default {
    install(app, options) {
        // ⭐ 全局方法
        app.config.globalProperties.$toast = (msg) => {
            // 显示一个 toast
            console.log("Toast:", msg);
        };

        // 全局指令
        app.directive("tooltip", {
            mounted(el, binding) {
                el.setAttribute("title", binding.value);
            },
        });

        // 全局组件
        app.component("ToastContainer", {
            template: "<div class='toast-container'><slot/></div>",
        });

        // provide 全局数据
        app.provide("toast", {
            show: (msg) => console.log(msg),
        });
    },
};

// main.js 注册
import ToastPlugin from "./plugins/toast";
app.use(ToastPlugin, { duration: 3000 });  // 传入选项
```

---

## 十三、TypeScript 集成

```vue
<script setup lang="ts">
// ⭐ TypeScript 与 Vue 3 是天作之合

import { ref, reactive, computed } from "vue";
import type { Ref } from "vue";

// 类型推断
const count = ref(0);               // Ref<number>
const name = ref("Alice");          // Ref<string>
const items = ref([1, 2, 3]);       // Ref<number[]>

// 显式类型
const data = ref<number | null>(null);
const list = ref<Array<{ id: number; name: string }>>([]);

// reactive
const state = reactive({
    user: { id: 1, name: "Alice" } as { id: number; name: string },
});

// computed 类型
const double: Ref<number> = computed(() => count.value * 2);

// ⭐ Props 类型
interface Props {
    title: string;
    count?: number;
    items: string[];
    status?: "success" | "error" | "warning";
    onChange?: (id: number) => void;
}

const props = defineProps<Props>();
// 带默认值
// const props = withDefaults(defineProps<Props>(), {
//     count: 0,
//     status: "success",
// });

// ⭐ Emit 类型
const emit = defineEmits<{
    update: [data: { id: number; name: string }];
    delete: [id: number];
    change: [value: string];
}>();

// ⭐ ref 模板引用
const inputRef = ref<HTMLInputElement | null>(null);
onMounted(() => {
    inputRef.value?.focus();
});

// ⭐ 异步组件
const HeavyComponent = defineAsyncComponent<typeof import("./Heavy.vue").default>(
    () => import("./Heavy.vue")
);
</script>

<template>
    <input ref="inputRef" />
    <p>{{ props.title }}: {{ count }}</p>
</template>
```

---

## 十四、Vite 配置与项目工程化

### vite.config.js

```javascript
import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import { resolve } from "path";

export default defineConfig({
    plugins: [vue()],

    // ⭐ 路径别名
    resolve: {
        alias: {
            "@": resolve(__dirname, "src"),
            "@comps": resolve(__dirname, "src/components"),
        },
    },

    // ⭐ 开发服务器
    server: {
        port: 3000,
        open: true,
        // 代理 API 请求（解决跨域）
        proxy: {
            "/api": {
                target: "http://localhost:8080",
                changeOrigin: true,
                // rewrite: (path) => path.replace(/^\/api/, ""),
            },
        },
    },

    // ⭐ 构建配置
    build: {
        outDir: "dist",
        assetsDir: "assets",
        sourcemap: false,         // 生产环境关闭 sourcemap
        chunkSizeWarningLimit: 500,

        rollupOptions: {
            output: {
                // ⭐ 代码分割
                manualChunks: {
                    vendor: ["vue", "vue-router", "pinia"],
                    ui: ["element-plus", "ant-design-vue"],
                },
            },
        },
    },
});
```

### 环境变量

```bash
# .env（所有环境）
VITE_APP_TITLE=My App

# .env.development（开发环境）
VITE_API_BASE_URL=http://localhost:8080/api

# .env.production（生产环境）
VITE_API_BASE_URL=https://api.example.com

# ⚠️ 只有 VITE_ 开头的变量会暴露给前端
```

```javascript
// 在代码中使用
const apiBase = import.meta.env.VITE_API_BASE_URL;
const isDev = import.meta.env.DEV;          // 是否为开发环境
const isProd = import.meta.env.PROD;        // 是否为生产环境
const mode = import.meta.env.MODE;          // "development" / "production"
```

### 常用工具集成

```bash
# 安装 UI 库
npm install element-plus
npm install ant-design-vue
npm install vant                          # 移动端

# 安装请求库
npm install axios

# 安装工具库
npm install dayjs                         # 日期处理
npm install lodash-es                     # 工具函数（按需导入）
npm install zustand                       # 量子状态（可选）

# 安装图标库
npm install @iconify/vue                  # 图标框架
npm install lucide-vue-next               # 简洁图标

# 安装表单验证
npm install vee-validate
npm install @vee-validate/rules
npm install zod                           # 类型验证（与 TS 搭配）
```

### 项目规范

```bash
# 代码格式化
npm install -D prettier

# 代码检查
npm install -D eslint eslint-plugin-vue

# Git 提交规范
npm install -D commitizen cz-conventional-changelog
npm install -D husky lint-staged
```

---

## 十五、完整实战：Todo 应用

```vue
<!-- App.vue — 完整的 Todo 应用 -->
<script setup lang="ts">
import { ref, computed } from "vue";
import type { Ref } from "vue";

interface Todo {
    id: number;
    text: string;
    done: boolean;
    createdAt: Date;
}

// 状态
const todos: Ref<Todo[]> = ref(loadTodos());
const input = ref("");
const filter = ref<"all" | "active" | "completed">("all");

// 计算属性
const filteredTodos = computed(() => {
    switch (filter.value) {
        case "active": return todos.value.filter(t => !t.done);
        case "completed": return todos.value.filter(t => t.done);
        default: return todos.value;
    }
});

const activeCount = computed(() => todos.value.filter(t => !t.done).length);
const completedCount = computed(() => todos.value.filter(t => t.done).length);

// 方法
function addTodo() {
    const text = input.value.trim();
    if (!text) return;
    todos.value.push({
        id: Date.now(),
        text,
        done: false,
        createdAt: new Date(),
    });
    input.value = "";
    saveTodos();
}

function toggleTodo(id: number) {
    const todo = todos.value.find(t => t.id === id);
    if (todo) todo.done = !todo.done;
    saveTodos();
}

function removeTodo(id: number) {
    todos.value = todos.value.filter(t => t.id !== id);
    saveTodos();
}

function clearCompleted() {
    todos.value = todos.value.filter(t => !t.done);
    saveTodos();
}

// 持久化
function saveTodos() {
    localStorage.setItem("todos", JSON.stringify(todos.value));
}

function loadTodos(): Todo[] {
    const stored = localStorage.getItem("todos");
    return stored ? JSON.parse(stored) : [];
}
</script>

<template>
    <div class="todo-app">
        <h1>Todo List</h1>

        <!-- 输入区域 -->
        <div class="input-group">
            <input
                v-model.trim="input"
                @keyup.enter="addTodo"
                placeholder="输入新的待办事项..."
                class="input"
            >
            <button @click="addTodo" class="add-btn" :disabled="!input.trim()">
                添加
            </button>
        </div>

        <!-- 过滤 -->
        <div class="filters">
            <button
                v-for="f in (['all', 'active', 'completed'] as const)"
                :key="f"
                @click="filter = f"
                :class="['filter-btn', { active: filter === f }]"
            >
                {{ { all: "全部", active: "进行中", completed: "已完成" }[f] }}
            </button>
        </div>

        <!-- 统计 -->
        <div class="stats">
            <span>总计: <strong>{{ todos.length }}</strong></span>
            <span>待完成: <strong>{{ activeCount }}</strong></span>
            <span>已完成: <strong>{{ completedCount }}</strong></span>
        </div>

        <!-- 列表 -->
        <ul class="todo-list" v-if="filteredTodos.length">
            <li
                v-for="todo in filteredTodos"
                :key="todo.id"
                :class="['todo-item', { completed: todo.done }]"
            >
                <input
                    type="checkbox"
                    :checked="todo.done"
                    @change="toggleTodo(todo.id)"
                    class="checkbox"
                >
                <span class="todo-text" @dblclick="toggleTodo(todo.id)">
                    {{ todo.text }}
                </span>
                <button @click="removeTodo(todo.id)" class="delete-btn">✕</button>
            </li>
        </ul>

        <div v-else class="empty">
            <p>{{ todos.length === 0 ? "还没有待办事项，添加一个吧" : "没有符合条件的待办" }}</p>
        </div>

        <button
            v-if="completedCount > 0"
            @click="clearCompleted"
            class="clear-btn"
        >
            清除所有已完成 ({{ completedCount }})
        </button>
    </div>
</template>

<style scoped>
.todo-app {
    max-width: 500px;
    margin: 40px auto;
    padding: 24px;
    background: white;
    border-radius: 12px;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
    font-family: -apple-system, "Microsoft YaHei", sans-serif;
}

h1 {
    text-align: center;
    color: #333;
    margin-bottom: 20px;
    font-size: 24px;
}

.input-group {
    display: flex;
    gap: 8px;
    margin-bottom: 16px;
}

.input {
    flex: 1;
    padding: 10px 12px;
    border: 2px solid #e0e0e0;
    border-radius: 8px;
    font-size: 14px;
    outline: none;
    transition: border-color 0.2s;
}

.input:focus { border-color: #42b883; }

.add-btn {
    padding: 10px 20px;
    background: #42b883;
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-size: 14px;
    transition: background 0.2s;
}

.add-btn:hover { background: #38a375; }
.add-btn:disabled { background: #ccc; cursor: not-allowed; }

.filters {
    display: flex;
    gap: 8px;
    margin-bottom: 12px;
}

.filter-btn {
    flex: 1;
    padding: 6px;
    border: 1px solid #e0e0e0;
    background: white;
    border-radius: 6px;
    cursor: pointer;
    transition: all 0.2s;
}

.filter-btn.active {
    background: #42b883;
    color: white;
    border-color: #42b883;
}

.stats {
    display: flex;
    justify-content: space-around;
    margin-bottom: 12px;
    padding-bottom: 12px;
    border-bottom: 1px solid #f0f0f0;
    font-size: 13px;
    color: #666;
}

.todo-list { list-style: none; padding: 0; }

.todo-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 8px;
    border-radius: 6px;
    transition: background 0.2s;
}

.todo-item:hover { background: #f9f9f9; }
.todo-item.completed .todo-text {
    text-decoration: line-through;
    color: #999;
}

.todo-text { flex: 1; cursor: pointer; }

.checkbox { width: 18px; height: 18px; cursor: pointer; }

.delete-btn {
    background: none;
    border: none;
    color: #ccc;
    cursor: pointer;
    font-size: 18px;
    padding: 0 6px;
    transition: color 0.2s;
}

.delete-btn:hover { color: #ff4d4f; }

.empty {
    text-align: center;
    color: #999;
    padding: 30px 0;
}

.clear-btn {
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
```

---

## 十六、Vue 3 面试高频题

| 问题 | 答案要点 |
|:----:|----------|
| **Vue 3 比 Vue 2 有哪些改进？** | Proxy 替代 defineProperty、Composition API、TypeScript 支持、Tree-shaking、Fragments、Teleport、Suspense |
| **computed 和 watch 的区别？** | computed 有缓存，依赖变化才重新计算；watch 执行副作用，支持 deep/immediate |
| **v-if 和 v-show 的区别？** | v-if 条件渲染（DOM 销毁/重建），v-show CSS 切换；v-if 有更高的切换开销，v-show 有更高的初始渲染开销 |
| **ref 和 reactive 的区别？** | ref 可处理所有类型（含基本类型），需 .value；reactive 仅对象，无需 .value，不能解构 |
| **nextTick 的作用？** | 等待 DOM 更新完成后执行回调，用于获取更新后的 DOM 状态 |
| **Vue 3 生命周期变化？** | beforeDestroy → beforeUnmount，destroyed → unmounted，新增 setup 代替 beforeCreate/created |
| **为什么 v-for 需要 key？** | 帮助 Vue 追踪节点身份，优化虚拟 DOM diff，提高列表更新性能 |
| **组件通信方式有哪些？** | props/emit、v-model、provide/inject、Pinia、slot、$parent/$refs（少用） |
| **什么是单向数据流？** | props 是父→子的单向数据流，子组件不应直接修改 props，应通过 emit 通知父组件修改 |
| **Vue 3 的响应式原理？** | 使用 Proxy 拦截 get/set，get 时收集依赖，set 时触发更新 |

> [!tip] **Vue 学习路径**
>
> **第一阶段**：模板语法 + ref/reactive + 条件/列表渲染
> **第二阶段**：组件（props/emit/slot）+ 生命周期 + computed/watch
> **第三阶段**：Vue Router + Pinia + Composables
> **第四阶段**：TypeScript + 工程化 + 测试 + 实战项目
>
> 上一篇：[[前端篇/HTML、CSS、JS]]
> 下一篇推荐：[[前端篇/React入门到进阶]]
