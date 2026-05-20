# React 入门到进阶

## 一、React 概述

### 什么是 React

**React** 是由 Meta（Facebook）开发和维护的用于构建用户界面的 **UI 库**。与 Vue、Angular 并称前端三大框架。

| 特性 | 说明 |
|:----:|------|
| **声明式** | 只需描述 UI 应该是什么样子，React 负责操作 DOM |
| **组件化** | 页面由独立、可复用的组件构成 |
| **单向数据流** | 数据从父组件流向子组件，数据变化可预测 |
| **虚拟 DOM** | 通过 Virtual DOM 减少真实 DOM 操作，提升性能 |

### 版本简史

|      版本      |   发布时间   | 说明                                                |
| :----------: | :--------: | ------------------------------------------------- |
|  React 0.3   |   2013.5   | 首次开源                                              |
| **React 16** |   2017.9   | Fiber 架构重写、Portal、Error Boundaries                |
|  React 16.8  |   2019.2   | ⭐ **Hooks 发布**（函数组件革命）                            |
| **React 17** |  2020.10   | 渐进升级、无新特性                                         |
| **React 18** |   2022.3   | ⭐ Concurrent Mode、`useId`、自动 batching、Suspense    |
| **React 19** |  2024.12   | ⭐ Actions、`use()`、`useOptimistic`、Server Components |
|  React 19.1  |   2025.3   | ref 作为常规 prop、类型改进、性能优化                          |
|  React 19.2  |  2025.10   | 并发特性增强、SSR 改进                                    |
|  React 19.2.6|   2026.5   | ⭐ **最新稳定版**（持续修复）                                 |
| **React 19.3**| 2026~  | 🔶 **Canary 阶段**，新 API 正在开发中                       |

> [!tip] 目前 **React 19.2.x** 是生产稳定版，React 19.3 正在 canary 阶段。React 19 的 Server Components 和 Actions 已进入生产可用。

### 核心思想：虚拟 DOM

```
数据（State）变化
       │
       ▼
生成新的 Virtual DOM（JS 对象树）
       │
       ▼
Diff 对比新旧 Virtual DOM（Reconciliation）
       │
       ▼
计算最小更新量（Diff 算法）
       │
       ▼
批量更新真实 DOM
```

> [!tip] **为什么用虚拟 DOM？**
> - 真实 DOM 操作很慢（重排/重绘代价高）
> - JS 对象操作很快（内存中比较差异）
> - 批量更新减少浏览器重排次数

### 快速开始

```bash
# ⭐ 推荐：Vite 创建 React 项目
npm create vite@latest my-app -- --template react
# 或者 TypeScript 版本
npm create vite@latest my-app -- --template react-ts

cd my-app
npm install
npm run dev
```

### 项目结构

```
my-app/
├── src/
│   ├── App.jsx                # 根组件
│   ├── main.jsx               # 入口文件
│   ├── components/            # 公共组件
│   ├── pages/                 # 页面组件
│   ├── hooks/                 # 自定义 Hooks
│   ├── context/               # Context 定义
│   ├── utils/                 # 工具函数
│   ├── styles/                # 全局样式
│   └── api/                   # API 请求
├── public/
├── index.html
├── vite.config.js
└── package.json
```

### Hello World

```jsx
// main.jsx
import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";

ReactDOM.createRoot(document.getElementById("root")).render(
    <React.StrictMode>
        <App />
    </React.StrictMode>
);
```

```jsx
// App.jsx
function App() {
    return <h1>Hello, React!</h1>;
}

export default App;
```

---

## 二、JSX 语法

### JSX 是什么

**JSX（JavaScript XML）** 是 JavaScript 的语法扩展，允许在 JS 中写类似 HTML 的标记。

```jsx
const element = <h1>Hello, World!</h1>;
```

> [!info] JSX 会被 Babel 编译为 `React.createElement()` 调用：
> ```jsx
> // JSX 写法
> const el = <h1 className="title">Hello</h1>;
>
> // 编译后
> const el = React.createElement("h1", { className: "title" }, "Hello");
> ```

### JSX 规则

```jsx
function App() {
    const name = "React";
    const isLoggedIn = true;
    const items = ["A", "B", "C"];

    return (
        // ⭐ 必须有且只有一个根元素（可以用 Fragment <>...</> 包裹）
        <>
            {/* 1. 花括号 {} 嵌入 JavaScript 表达式 */}
            <h1>Hello, {name}!</h1>
            <p>{isLoggedIn ? "已登录" : "未登录"}</p>

            {/* 2. class → className，for → htmlFor */}
            <div className="container">
                <label htmlFor="email">邮箱</label>
            </div>

            {/* 3. 内联样式用对象（驼峰命名） */}
            <div style={{ color: "red", fontSize: "16px", backgroundColor: "#f0f0f0" }}>
                内联样式
            </div>

            {/* 4. 自闭和标签必须使用 /> */}
            <input type="text" />
            <br />
            <img src="logo.png" alt="logo" />

            {/* 5. 列表渲染需要 key */}
            <ul>
                {items.map((item, index) => (
                    <li key={index}>{item}</li>
                ))}
            </ul>
        </>
    );
}
```

### JSX 中的条件渲染

```jsx
function Greeting({ user }) {
    // 方式一：与运算符 &&
    return <div>{user && <h1>欢迎回来，{user.name}！</h1>}</div>;

    // 方式二：三元运算符
    // return <div>{user ? <h1>欢迎回来，{user.name}！</h1> : <h1>请登录</h1>}</div>;

    // 方式三：if/else 变量赋值
    // let content;
    // if (user) {
    //     content = <h1>欢迎回来，{user.name}！</h1>;
    // } else {
    //     content = <h1>请登录</h1>;
    // }
    // return <div>{content}</div>;
}
```

---

## 三、组件

### 函数组件（⭐ 推荐）

```jsx
// ⭐ React 18+ 推荐：函数组件 + Hooks
function Welcome(props) {
    return <h1>Hello, {props.name}!</h1>;
}

// 箭头函数写法
const Welcome = ({ name }) => {
    return <h1>Hello, {name}!</h1>;
};
```

### 类组件

```jsx
import React, { Component } from "react";

// 了解即可，新项目不再使用
class Welcome extends Component {
    render() {
        return <h1>Hello, {this.props.name}!</h1>;
    }
}
```

> [!tip] **函数组件 vs 类组件**
> | 对比项 | 函数组件 | 类组件 |
> |:------:|:--------:|:------:|
> | 定义方式 | 纯函数 | ES6 Class |
> | 状态管理 | `useState` Hook | `this.state` |
> | 生命周期 | `useEffect` Hook | `componentDidMount` 等 |
> | `this` | 无 | 需要绑定 |
> | 代码量 | 少，简洁 | 多，样板代码 |
> | **推荐度** | ⭐ **推荐** | ❌ 已不推荐 |

### 组件通信

```jsx
// 1. 父传子：Props
function Child({ message }) {
    return <p>{message}</p>;
}

function Parent() {
    return <Child message="来自父组件的数据" />;
}

// 2. 子传父：回调函数
function Child({ onSend }) {
    return <button onClick={() => onSend("子组件的数据")}>发送</button>;
}

function Parent() {
    const handleReceive = (data) => console.log("收到：", data);
    return <Child onSend={handleReceive} />;
}

// 3. 兄弟组件通信：通过共同父组件中转
// 4. 跨层级通信：Context（后面会讲）
```

### Props 默认值与类型

```jsx
// 默认值（推荐写法）
function Button({ text = "点击", color = "blue" }) {
    return <button style={{ backgroundColor: color }}>{text}</button>;
}

// children：组件内嵌的内容
function Card({ title, children }) {
    return (
        <div className="card">
            <h3>{title}</h3>
            <div>{children}</div>
        </div>
    );
}

// 使用
<Card title="标题">
    <p>这是卡片内容</p>
</Card>;
```

---

## 四、State（状态管理）

### useState ⭐

```jsx
import { useState } from "react";

function Counter() {
    // 数组解构：[当前状态, 更新函数]
    const [count, setCount] = useState(0);
    const [user, setUser] = useState({ name: "张三", age: 25 });

    return (
        <>
            <p>计数：{count}</p>
            {/* 直接设置新值 */}
            <button onClick={() => setCount(count + 1)}>+1</button>

            {/* 函数式更新（推荐：依赖前值） */}
            <button onClick={() => setCount((prev) => prev + 1)}>+1</button>

            {/* ⚠️ 对象/数组必须创建新引用才能触发更新 */}
            <button
                onClick={() => setUser({ ...user, age: user.age + 1 })}
            >
                年龄 +1
            </button>
        </>
    );
}
```

> [!warning] **State 更新的重要规则**
> 1. **不可直接修改 state**：`count = 5` ❌，必须用 `setCount(5)` ✅
> 2. **更新是异步的**：多次 `setCount` 会批量合并
> 3. **对象/数组要创建新引用**：`setUser({...user, name: "李四"})` ✅
> 4. **React 18 自动批处理**：多个 setState 只触发一次重渲染

### useState 使用技巧

```jsx
// 1. 惰性初始化（适合计算量大的场景）
const [data, setData] = useState(() => {
    // 这个函数只会在初始渲染时执行一次
    const initial = expensiveComputation();
    return initial;
});

// 2. 存储上一次的值（自定义 Hook）
function usePrevious(value) {
    const ref = useRef();
    useEffect(() => {
        ref.current = value;
    }, [value]);
    return ref.current;
}

// 3. 多个状态 vs 单个对象
const [name, setName] = useState("");
const [age, setAge] = useState(0); // ✅ 独立状态，更新互不影响

const [form, setForm] = useState({ name: "", age: 0 }); // ⚠️ 对象需要展开
```

### useReducer（复杂状态逻辑）⭐

```jsx
import { useReducer } from "react";

// 定义 reducer（纯函数）
function counterReducer(state, action) {
    switch (action.type) {
        case "INCREMENT":
            return { count: state.count + 1 };
        case "DECREMENT":
            return { count: state.count - 1 };
        case "ADD":
            return { count: state.count + action.payload };
        case "RESET":
            return { count: 0 };
        default:
            return state;
    }
}

function Counter() {
    const [state, dispatch] = useReducer(counterReducer, { count: 0 });

    return (
        <>
            <p>计数：{state.count}</p>
            <button onClick={() => dispatch({ type: "INCREMENT" })}>+1</button>
            <button onClick={() => dispatch({ type: "DECREMENT" })}>-1</button>
            <button onClick={() => dispatch({ type: "ADD", payload: 5 })}>+5</button>
            <button onClick={() => dispatch({ type: "RESET" })}>重置</button>
        </>
    );
}
```

> [!tip] **useState vs useReducer**
> | 场景 | 用 useState | 用 useReducer |
> |:----:|:-----------:|:-------------:|
> | 状态类型 | 简单值（数字、字符串、布尔） | 复杂对象 |
> | 更新逻辑 | 简单，独立的更新 | 涉及多个子值的联动 |
> | 状态依赖 | 下一个状态依赖前一个 | 复杂的状态转换 |
> | 可读性 | 逻辑就在组件内 | 逻辑集中在 reducer 中 |

---

## 五、事件处理

```jsx
function EventDemo() {
    // ⭐ 事件命名：驼峰命名（onClick、onChange、onSubmit）
    const handleClick = (event) => {
        console.log("被点击了", event);
    };

    const handleChange = (event) => {
        // event.target.value 获取输入值
        console.log("输入内容：", event.target.value);
    };

    const handleSubmit = (event) => {
        event.preventDefault(); // 阻止默认行为
        console.log("表单提交");
    };

    // 传参
    const handleDelete = (id, event) => {
        console.log("删除：", id);
    };

    return (
        <>
            {/* 基本事件 */}
            <button onClick={handleClick}>点击</button>

            {/* 行内箭头函数 */}
            <button onClick={() => console.log("点击")}>点击</button>

            {/* ⚠️ 传参时注意 */}
            <button onClick={(e) => handleDelete(1, e)}>删除</button>

            {/* 表单事件 */}
            <input type="text" onChange={handleChange} />
            <form onSubmit={handleSubmit}>
                <button type="submit">提交</button>
            </form>
        </>
    );
}
```

### 常见事件

| 事件 | 触发时机 | 常用属性 |
|:----:|:--------:|:--------:|
| `onClick` | 元素被点击 | — |
| `onChange` | 输入框内容变化 | `event.target.value` |
| `onSubmit` | 表单提交 | `event.preventDefault()` |
| `onFocus` | 元素获得焦点 | — |
| `onBlur` | 元素失去焦点 | — |
| `onKeyDown` | 键盘按下 | `event.key` |
| `onMouseEnter` | 鼠标移入 | — |
| `onMouseLeave` | 鼠标移出 | — |
| `onScroll` | 滚动 | `event.scrollTop` |

---

## 六、Hooks 详解

> [!info] **Hooks 规则**
> 1. **只在最顶层使用 Hook**：不要在循环、条件、嵌套函数中调用
> 2. **只在 React 函数组件或自定义 Hook 中调用**
> 3. 可以用 ESLint 插件 `eslint-plugin-react-hooks` 自动检查

### useState — 状态管理

（已在第四章详细讲解）

### useEffect — 副作用 ⭐

```jsx
import { useState, useEffect } from "react";

function Timer() {
    const [count, setCount] = useState(0);

    // 1. 无依赖：每次渲染都执行（慎用！）
    useEffect(() => {
        console.log("组件渲染了");
    });

    // 2. 空数组 []：只在挂载时执行一次（相当于 componentDidMount）
    useEffect(() => {
        console.log("组件挂载了");
    }, []);

    // 3. 有依赖：依赖变化时执行
    useEffect(() => {
        console.log("count 变化了：", count);

        // 4. ⭐ 清理函数（cleanup）：组件卸载或重新执行前调用
        const timer = setInterval(() => {
            console.log("定时器执行中...");
        }, 1000);

        return () => {
            console.log("清理定时器");
            clearInterval(timer);
        };
    }, [count]);

    return (
        <div>
            <p>计数：{count}</p>
            <button onClick={() => setCount((c) => c + 1)}>+1</button>
        </div>
    );
}
```

> [!tip] **useEffect 生命周期映射**
> | 类组件生命周期 | useEffect 等效写法 |
> |:--------------:|:------------------:|
> | `componentDidMount` | `useEffect(() => {}, [])` |
> | `componentDidUpdate` | `useEffect(() => {}, [dep])` |
> | `componentWillUnmount` | `useEffect(() => { return cleanup }, [])` |

### useRef — 引用 DOM / 保存可变值 ⭐

```jsx
import { useRef, useEffect } from "react";

function Form() {
    // 1. 引用 DOM 元素
    const inputRef = useRef(null);

    // 2. 保存任意可变值（不会触发重渲染）
    const renderCount = useRef(0);

    useEffect(() => {
        // 自动聚焦输入框
        inputRef.current.focus();
    }, []);

    useEffect(() => {
        renderCount.current += 1;
        console.log("渲染次数：", renderCount.current);
    });

    const handleClick = () => {
        console.log("输入框的值：", inputRef.current.value);
    };

    return (
        <>
            <input ref={inputRef} type="text" />
            <button onClick={handleClick}>获取值</button>
        </>
    );
}
```

> [!tip] **useRef 的特点**
> - `ref.current` 变化**不会**触发重新渲染
> - 在组件的整个生命周期内保持不变（除了你手动修改）
> - 常用于：DOM 引用、保存定时器 ID、记录前一个值、保存不需要渲染的数据

### useContext — 跨层级传递数据 ⭐

```jsx
import { createContext, useContext, useState } from "react";

// 1. 创建 Context
const ThemeContext = createContext("light");

// 2. Provider 提供数据
function App() {
    const [theme, setTheme] = useState("light");

    return (
        <ThemeContext.Provider value={{ theme, setTheme }}>
            <Toolbar />
        </ThemeContext.Provider>
    );
}

// 3. 任意后代组件消费数据
function Toolbar() {
    return <Button />;
}

function Button() {
    // ⭐  useContext 访问 Context 值
    const { theme, setTheme } = useContext(ThemeContext);

    return (
        <button
            onClick={() => setTheme(theme === "light" ? "dark" : "light")}
            style={{
                background: theme === "light" ? "#fff" : "#333",
                color: theme === "light" ? "#333" : "#fff",
            }}
        >
            当前主题：{theme}
        </button>
    );
}
```

### useMemo — 记忆化计算值 ⭐

```jsx
import { useMemo, useState } from "react";

function ExpensiveList({ items, filter }) {
    // ⭐ 只在 items 或 filter 变化时才重新计算
    const filteredItems = useMemo(() => {
        console.log("执行昂贵计算...");
        return items.filter((item) => item.includes(filter));
    }, [items, filter]);

    // 如果没有 useMemo，每次渲染都会重新过滤
    // const filteredItems = items.filter((item) => item.includes(filter));

    return (
        <ul>
            {filteredItems.map((item, i) => (
                <li key={i}>{item}</li>
            ))}
        </ul>
    );
}
```

### useCallback — 记忆化函数 ⭐

```jsx
import { useCallback, useState } from "react";
import ChildButton from "./ChildButton";

function Parent() {
    const [count, setCount] = useState(0);

    // ⭐ 只有依赖变化时才创建新函数引用
    // 避免子组件因函数引用变化而重复渲染
    const handleClick = useCallback(() => {
        console.log("点击了", count);
    }, [count]); // 如果依赖是空数组，函数始终是同一个引用

    // 对比：不使用 useCallback，每次渲染都创建新函数
    // const handleClick = () => console.log("点击了", count);

    return (
        <>
            <p>计数：{count}</p>
            <button onClick={() => setCount((c) => c + 1)}>+1</button>
            {/* ChildButton 使用 React.memo 包装 */}
            <ChildButton onClick={handleClick} />
        </>
    );
}
```

> [!tip] **useMemo vs useCallback**
> | Hook | 返回值 | 使用场景 |
> |:----:|:------:|:---------|
> | `useMemo` | 记忆化**值** | 昂贵的计算结果 |
> | `useCallback` | 记忆化**函数** | 传给子组件的回调 |

### React.memo — 组件记忆化

```jsx
import { memo } from "react";

// ⭐ React.memo 包裹的组件：只有当 props 变化时才重新渲染
const ChildButton = memo(function ChildButton({ onClick, label = "点击" }) {
    console.log("ChildButton 重新渲染了");
    return <button onClick={onClick}>{label}</button>;
});

export default ChildButton;
```

### useTransition — 过渡更新（React 18+）⭐

```jsx
import { useState, useTransition } from "react";

function SearchPage() {
    const [query, setQuery] = useState("");
    const [searchResults, setSearchResults] = useState([]);
    // 标记非紧急更新
    const [isPending, startTransition] = useTransition();

    const handleChange = (e) => {
        // 紧急更新：更新输入框
        setQuery(e.target.value);

        // 过渡更新：搜索结果可以延迟
        startTransition(() => {
            const results = heavySearch(e.target.value);
            setSearchResults(results);
        });
    };

    return (
        <div>
            <input value={query} onChange={handleChange} />
            {isPending ? <p>搜索中...</p> : <SearchList results={searchResults} />}
        </div>
    );
}
```

### useDeferredValue — 延迟更新（React 18+）

```jsx
import { useState, useDeferredValue, useMemo } from "react";

function SearchPage() {
    const [query, setQuery] = useState("");
    // 延迟值：当有更高优先级更新时，该值会"落后"
    const deferredQuery = useDeferredValue(query);
    const isStale = query !== deferredQuery;

    const searchResults = useMemo(() => {
        return heavySearch(deferredQuery);
    }, [deferredQuery]);

    return (
        <div>
            <input value={query} onChange={(e) => setQuery(e.target.value)} />
            <div style={{ opacity: isStale ? 0.5 : 1 }}>
                <SearchList results={searchResults} />
            </div>
        </div>
    );
}
```

### useId — 生成唯一 ID（React 18+）

```jsx
import { useId } from "react";

function FormField({ label }) {
    const id = useId(); // ⭐ 生成唯一 ID，服务端渲染时也保持一致性

    return (
        <div>
            <label htmlFor={id}>{label}</label>
            <input id={id} type="text" />
        </div>
    );
}
```

---

## 七、自定义 Hooks ⭐

> [!info] 自定义 Hook 是 React 中**复用逻辑**的核心方式，本质是一个以 `use` 开头的函数，内部可以调用其他 Hook。

### useMouse — 鼠标位置跟踪

```jsx
import { useState, useEffect } from "react";

function useMouse() {
    const [mouse, setMouse] = useState({ x: 0, y: 0 });

    useEffect(() => {
        const handleMove = (e) => {
            setMouse({ x: e.clientX, y: e.clientY });
        };

        window.addEventListener("mousemove", handleMove);
        return () => window.removeEventListener("mousemove", handleMove);
    }, []);

    return mouse;
}

// 使用
function MouseTracker() {
    const { x, y } = useMouse();
    return <p>鼠标位置：({x}, {y})</p>;
}
```

### useFetch — 数据请求 ⭐

```jsx
import { useState, useEffect } from "react";

function useFetch(url, options = {}) {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        let cancelled = false;

        async function fetchData() {
            try {
                setLoading(true);
                const response = await fetch(url, options);
                if (!response.ok) throw new Error(`HTTP ${response.status}`);
                const result = await response.json();

                if (!cancelled) {
                    setData(result);
                    setError(null);
                }
            } catch (err) {
                if (!cancelled) setError(err.message);
            } finally {
                if (!cancelled) setLoading(false);
            }
        }

        fetchData();

        // ⭐ 清理函数：防止组件卸载后更新状态
        return () => {
            cancelled = true;
        };
    }, [url]); // 依赖 url

    return { data, loading, error };
}

// 使用
function UserList() {
    const { data: users, loading, error } = useFetch(
        "https://jsonplaceholder.typicode.com/users"
    );

    if (loading) return <p>加载中...</p>;
    if (error) return <p>错误：{error}</p>;

    return (
        <ul>
            {users?.map((user) => (
                <li key={user.id}>{user.name}</li>
            ))}
        </ul>
    );
}
```

### useLocalStorage — 本地存储

```jsx
import { useState, useCallback } from "react";

function useLocalStorage(key, initialValue) {
    // 惰性初始化：从 localStorage 读取
    const [storedValue, setStoredValue] = useState(() => {
        try {
            const item = window.localStorage.getItem(key);
            return item ? JSON.parse(item) : initialValue;
        } catch {
            return initialValue;
        }
    });

    const setValue = useCallback(
        (value) => {
            try {
                const valueToStore =
                    value instanceof Function ? value(storedValue) : value;
                setStoredValue(valueToStore);
                window.localStorage.setItem(key, JSON.stringify(valueToStore));
            } catch (error) {
                console.error("保存到 localStorage 失败：", error);
            }
        },
        [key, storedValue]
    );

    return [storedValue, setValue];
}

// 使用
function Settings() {
    const [theme, setTheme] = useLocalStorage("theme", "light");
    const [user, setUser] = useLocalStorage("user", null);

    return (
        <button onClick={() => setTheme(theme === "light" ? "dark" : "light")}>
            切换主题（当前：{theme}）
        </button>
    );
}
```

### useToggle

```jsx
import { useState, useCallback } from "react";

function useToggle(initialValue = false) {
    const [value, setValue] = useState(initialValue);

    const toggle = useCallback(() => {
        setValue((prev) => !prev);
    }, []);

    const setTrue = useCallback(() => setValue(true), []);
    const setFalse = useCallback(() => setValue(false), []);

    return [value, toggle, { setTrue, setFalse }];
}

// 使用
function Modal() {
    const [isOpen, toggleModal, { setTrue, setFalse }] = useToggle();

    return (
        <>
            <button onClick={toggleModal}>切换弹窗</button>
            {isOpen && <div className="modal">弹窗内容</div>}
        </>
    );
}
```

---

## 八、表单处理

### 受控组件 ⭐

```jsx
import { useState } from "react";

function LoginForm() {
    // ⭐ 受控组件：表单数据由 React 状态管理
    const [form, setForm] = useState({
        username: "",
        password: "",
        remember: false,
        gender: "",
    });

    const handleChange = (e) => {
        const { name, value, type, checked } = e.target;
        // ⭐ 统一处理多种输入类型
        setForm({
            ...form,
            [name]: type === "checkbox" ? checked : value,
        });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        console.log("提交的数据：", form);
    };

    return (
        <form onSubmit={handleSubmit}>
            {/* 文本输入 */}
            <input name="username" value={form.username} onChange={handleChange} placeholder="用户名" />

            {/* 密码 */}
            <input name="password" type="password" value={form.password} onChange={handleChange} placeholder="密码" />

            {/* 复选框 */}
            <label>
                <input name="remember" type="checkbox" checked={form.remember} onChange={handleChange} />
                记住我
            </label>

            {/* 单选框 */}
            <label>
                <input name="gender" type="radio" value="male" checked={form.gender === "male"} onChange={handleChange} />
                男
            </label>
            <label>
                <input name="gender" type="radio" value="female" checked={form.gender === "female"} onChange={handleChange} />
                女
            </label>

            <button type="submit">登录</button>
        </form>
    );
}
```

### 非受控组件（useRef）

```jsx
import { useRef } from "react";

function UncontrolledForm() {
    // useRef 读取 DOM 值
    const nameRef = useRef(null);
    const emailRef = useRef(null);

    const handleSubmit = (e) => {
        e.preventDefault();
        console.log("姓名：", nameRef.current.value);
        console.log("邮箱：", emailRef.current.value);
    };

    return (
        <form onSubmit={handleSubmit}>
            <input ref={nameRef} placeholder="姓名" defaultValue="默认值" />
            <input ref={emailRef} type="email" placeholder="邮箱" />
            <button type="submit">提交</button>
        </form>
    );
}
```

> [!tip] **受控 vs 非受控**
> | 对比 | 受控组件 | 非受控组件 |
> |:----:|:--------:|:-----------:|
> | 数据源 | React state | DOM 自身 |
> | 读取时机 | 任何时候 | 使用时（提交等） |
> | 实时校验 | ✅ 方便 | ❌ 不方便 |
> | 代码量 | 较多 | 较少 |
> | **推荐** | ⭐ **推荐** | 简单表单场景 |

---

## 九、Context API + useReducer（全局状态管理）

### 实现简单状态管理 ⭐

```jsx
// store/AppContext.jsx
import { createContext, useContext, useReducer } from "react";

// 1. 创建 Context
const AppContext = createContext(null);
const AppDispatchContext = createContext(null);

// 2. Reducer
function appReducer(state, action) {
    switch (action.type) {
        case "SET_USER":
            return { ...state, user: action.payload };
        case "LOGOUT":
            return { ...state, user: null };
        case "SET_THEME":
            return { ...state, theme: action.payload };
        default:
            return state;
    }
}

// 3. Provider 组件
const initialState = {
    user: null,
    theme: "light",
};

export function AppProvider({ children }) {
    const [state, dispatch] = useReducer(appReducer, initialState);

    return (
        <AppContext.Provider value={state}>
            <AppDispatchContext.Provider value={dispatch}>
                {children}
            </AppDispatchContext.Provider>
        </AppContext.Provider>
    );
}

// 4. 自定义 Hooks（方便使用）
export function useAppState() {
    return useContext(AppContext);
}

export function useAppDispatch() {
    return useContext(AppDispatchContext);
}
```

```jsx
// 使用
import { AppProvider, useAppState, useAppDispatch } from "./store/AppContext";

function App() {
    return (
        <AppProvider>
            <Navbar />
            <Profile />
        </AppProvider>
    );
}

function Navbar() {
    const { user, theme } = useAppState();
    const dispatch = useAppDispatch();

    return (
        <nav style={{ background: theme === "dark" ? "#333" : "#fff" }}>
            {user ? (
                <>
                    <span>欢迎，{user.name}</span>
                    <button onClick={() => dispatch({ type: "LOGOUT" })}>退出</button>
                </>
            ) : (
                <button onClick={() => dispatch({ type: "SET_USER", payload: { name: "张三" } })}>
                    登录
                </button>
            )}
            <button onClick={() => dispatch({ type: "SET_THEME", payload: theme === "dark" ? "light" : "dark" })}>
                切换主题
            </button>
        </nav>
    );
}

function Profile() {
    const { user } = useAppState();
    return <div>{user ? <p>个人信息：{user.name}</p> : <p>请登录</p>}</div>;
}
```

---

## 十、React Router ⭐

### 安装

```bash
npm install react-router-dom
```

### 基本路由

```jsx
// main.jsx
import { BrowserRouter } from "react-router-dom";
import App from "./App";

ReactDOM.createRoot(document.getElementById("root")).render(
    <BrowserRouter>
        <App />
    </BrowserRouter>
);
```

```jsx
// App.jsx
import { Routes, Route, Link, NavLink, Navigate } from "react-router-dom";
import Home from "./pages/Home";
import About from "./pages/About";
import User from "./pages/User";
import NotFound from "./pages/NotFound";

function App() {
    return (
        <div>
            {/* 导航链接 */}
            <nav>
                <Link to="/">首页</Link>
                <Link to="/about">关于</Link>
                <Link to="/user/123">用户</Link>

                {/* ⭐ NavLink：带激活状态 */}
                <NavLink to="/" className={({ isActive }) => (isActive ? "active" : "")}>
                    首页
                </NavLink>
            </nav>

            {/* 路由出口 */}
            <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/about" element={<About />} />
                {/* 动态路由参数 */}
                <Route path="/user/:id" element={<User />} />
                {/* 重定向 */}
                <Route path="/old-path" element={<Navigate to="/new-path" />} />
                {/* 404 */}
                <Route path="*" element={<NotFound />} />
            </Routes>
        </div>
    );
}
```

### 嵌套路由

```jsx
function App() {
    return (
        <Routes>
            <Route path="/" element={<Layout />}>
                {/* index 路由：默认子路由 */}
                <Route index element={<Home />} />
                <Route path="about" element={<About />} />
                <Route path="dashboard" element={<Dashboard />}>
                    {/* ⭐ 嵌套的子路由 */}
                    <Route index element={<Overview />} />
                    <Route path="settings" element={<Settings />} />
                    <Route path="profile" element={<Profile />} />
                </Route>
            </Route>
        </Routes>
    );
}

// Layout 使用 <Outlet /> 渲染子路由
import { Outlet } from "react-router-dom";

function Layout() {
    return (
        <div className="layout">
            <Header />
            <main>
                <Outlet /> {/* 子路由内容在这里渲染 */}
            </main>
            <Footer />
        </div>
    );
}
```

### 路由 Hooks ⭐

```jsx
import { useParams, useNavigate, useLocation, useSearchParams } from "react-router-dom";

function User() {
    // 1. 获取动态路由参数
    const { id } = useParams();

    // 2. 编程式导航
    const navigate = useNavigate();

    // 3. 获取当前路径信息
    const location = useLocation();

    // 4. 查询参数
    const [searchParams, setSearchParams] = useSearchParams();
    const page = searchParams.get("page") || "1";

    return (
        <div>
            <p>用户 ID：{id}</p>
            <p>当前路径：{location.pathname}</p>
            <p>当前页：{page}</p>

            <button onClick={() => navigate("/")}>返回首页</button>
            <button onClick={() => navigate(-1)}>后退</button>
            <button onClick={() => navigate("/about", { state: { from: "user" } })}>
                跳转并传递状态
            </button>
            <button onClick={() => setSearchParams({ page: "2" })}>下一页</button>
        </div>
    );
}
```

### 路由守卫 ⭐

```jsx
import { Navigate, useLocation } from "react-router-dom";

// 需要登录的路由
function RequireAuth({ children }) {
    const isLoggedIn = !!localStorage.getItem("token");
    const location = useLocation();

    if (!isLoggedIn) {
        // 重定向到登录页，保留来源地址
        return <Navigate to="/login" state={{ from: location }} replace />;
    }

    return children;
}

// 使用
<Routes>
    <Route
        path="/dashboard"
        element={
            <RequireAuth>
                <Dashboard />
            </RequireAuth>
        }
    />
    <Route path="/login" element={<Login />} />
</Routes>;
```

---

## 十一、状态管理（Zustand）⭐

> [!info] 除了 Context + useReducer，社区主流状态管理库有 **Redux Toolkit** 和 **Zustand**。Zustand 更轻量、更易用，是目前增长最快的状态管理方案。

### 安装

```bash
npm install zustand
```

### 创建 Store

```jsx
// store/useUserStore.js
import { create } from "zustand";
import { persist } from "zustand/middleware";

// ⭐ 创建 store
const useUserStore = create(
    // persist 中间件：持久化到 localStorage
    persist(
        (set, get) => ({
            // 状态
            user: null,
            token: null,
            theme: "light",

            // ⭐ 操作（直接修改状态）
            login: (userData) =>
                set({ user: userData.user, token: userData.token }),

            logout: () => set({ user: null, token: null }),

            setTheme: (theme) => set({ theme }),

            // ⭐ get() 获取当前状态
            isLoggedIn: () => !!get().token,
        }),
        {
            name: "user-storage", // localStorage key
        }
    )
);

export default useUserStore;
```

### 在组件中使用

```jsx
import useUserStore from "./store/useUserStore";

function Navbar() {
    // ⭐ 选择需要的状态（组件只会在选择的状态变化时重渲染）
    const user = useUserStore((state) => state.user);
    const theme = useUserStore((state) => state.theme);
    const login = useUserStore((state) => state.login);
    const logout = useUserStore((state) => state.logout);

    return (
        <nav style={{ background: theme === "dark" ? "#333" : "#fff" }}>
            {user ? (
                <>
                    <span>欢迎，{user.name}</span>
                    <button onClick={logout}>退出</button>
                </>
            ) : (
                <button onClick={() => login({ user: { name: "张三" }, token: "xxx" })}>
                    登录
                </button>
            )}
        </nav>
    );
}

// 组件外使用
// const state = useUserStore.getState();
// useUserStore.getState().logout();
// useUserStore.subscribe((state) => console.log("状态变化", state));
```

---

## 十二、性能优化

### React.memo — 避免不必要的重渲染

```jsx
import { memo } from "react";

// ⭐ 只有 props 变化时才重新渲染
const ExpensiveComponent = memo(function ExpensiveComponent({ data }) {
    console.log("ExpensiveComponent 渲染");
    return <div>{/* 渲染大量数据 */}</div>;
});
```

### useMemo — 缓存计算结果

```jsx
const sortedList = useMemo(() => {
    return items.sort((a, b) => a.name.localeCompare(b.name));
}, [items]); // items 没变就不重新排序
```

### useCallback — 缓存函数引用

```jsx
const handleClick = useCallback((id) => {
    console.log("点击了", id);
}, []); // 函数引用不变，子组件不会因为函数而重渲染
```

### lazy + Suspense — 代码分割 ⭐

```jsx
import { lazy, Suspense } from "react";

// ⭐ 动态导入：该组件会在需要时才加载
const HeavyComponent = lazy(() => import("./HeavyComponent"));
const UserProfile = lazy(() => import("./pages/UserProfile"));

function App() {
    return (
        <Suspense fallback={<div>加载中...</div>}>
            <HeavyComponent />
            {/* 多个 lazy 组件可以放在同一个 Suspense 中 */}
            <UserProfile />
        </Suspense>
    );
}
```

### 虚拟列表（react-window）

```bash
npm install react-window
```

```jsx
import { FixedSizeList } from "react-window";

// ⭐ 只渲染可见区域的内容（10 万条数据也不卡）
function VirtualList({ items }) {
    const Row = ({ index, style }) => (
        <div style={style}>
            {index + 1}. {items[index].name}
        </div>
    );

    return (
        <FixedSizeList
            height={400}      // 可视区域高度
            itemCount={items.length}
            itemSize={35}      // 每行高度
            width="100%"
        >
            {Row}
        </FixedSizeList>
    );
}
```

### 性能优化检查清单

| 优化手段 | 解决什么问题 | 使用场景 |
|:--------:|:-----------:|:---------|
| `React.memo` | 组件不必要的重渲染 | 纯展示组件 |
| `useMemo` | 昂贵的计算重复执行 | 过滤、排序、大数据处理 |
| `useCallback` | 函数引用变化导致子组件重渲染 | 传给子组件的回调函数 |
| `lazy` + `Suspense` | 首屏包体积过大 | 路由级别的代码分割 |
| 虚拟列表 | 大量列表项渲染 | 聊天记录、长列表 |
| 图片懒加载 | 太多图片加载 | 图片列表、瀑布流 |

---

## 十三、错误边界（Error Boundaries）

```jsx
import React from "react";

// ⭐ 错误边界必须用类组件（目前 Hooks 还不支持）
class ErrorBoundary extends React.Component {
    constructor(props) {
        super(props);
        this.state = { hasError: false, error: null };
    }

    static getDerivedStateFromError(error) {
        // 更新 state，下次渲染显示 fallback UI
        return { hasError: true, error };
    }

    componentDidCatch(error, errorInfo) {
        // 记录错误日志
        console.error("捕获到错误：", error, errorInfo);
    }

    render() {
        if (this.state.hasError) {
            // 自定义错误 UI
            return (
                <div className="error-boundary">
                    <h2>出错了！</h2>
                    <p>{this.state.error?.message}</p>
                    <button onClick={() => this.setState({ hasError: false, error: null })}>
                        重试
                    </button>
                </div>
            );
        }

        return this.props.children;
    }
}

// 使用
<ErrorBoundary>
    <UserProfile userId={userId} />
</ErrorBoundary>;
```

---

## 十四、与后端通信

### fetch（原生）⭐

```jsx
// api/user.js
const API_BASE = "https://api.example.com";

export async function getUsers() {
    const res = await fetch(`${API_BASE}/users`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return res.json();
}

export async function createUser(data) {
    const res = await fetch(`${API_BASE}/users`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return res.json();
}
```

### axios

```bash
npm install axios
```

```jsx
// api/request.js
import axios from "axios";

// ⭐ 创建实例
const request = axios.create({
    baseURL: "https://api.example.com",
    timeout: 10000,
    headers: { "Content-Type": "application/json" },
});

// 请求拦截器（添加 Token）
request.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem("token");
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

// 响应拦截器（统一处理错误）
request.interceptors.response.use(
    (response) => response.data, // 直接返回数据
    (error) => {
        if (error.response?.status === 401) {
            // Token 过期，跳转登录
            localStorage.removeItem("token");
            window.location.href = "/login";
        }
        return Promise.reject(error);
    }
);

export default request;
```

```jsx
// 使用
import request from "./api/request";

function UserList() {
    const [users, setUsers] = useState([]);

    useEffect(() => {
        request.get("/users").then(setUsers);
        // request.post("/users", { name: "张三" });
        // request.put("/users/1", { name: "李四" });
        // request.delete("/users/1");
    }, []);

    return <div>{/* 渲染用户列表 */}</div>;
}
```

---

## 十五、TypeScript 集成 ⭐

```tsx
// ⭐ Props 类型定义
interface ButtonProps {
    label: string;
    variant?: "primary" | "secondary" | "danger";
    size?: "sm" | "md" | "lg";
    disabled?: boolean;
    onClick?: (event: React.MouseEvent<HTMLButtonElement>) => void;
    children?: React.ReactNode;
}

// ⭐ 函数组件 + 泛型
function Button({
    label,
    variant = "primary",
    size = "md",
    disabled = false,
    onClick,
    children,
}: ButtonProps) {
    return (
        <button
            className={`btn btn-${variant} btn-${size}`}
            disabled={disabled}
            onClick={onClick}
        >
            {label}
            {children}
        </button>
    );
}

// ⭐ useState 泛型
const [user, setUser] = useState<User | null>(null);
const [items, setItems] = useState<string[]>([]);
const [form, setForm] = useState<FormData>({ name: "", email: "" });

// ⭐ useRef 泛型
const inputRef = useRef<HTMLInputElement>(null);
const divRef = useRef<HTMLDivElement>(null);

// ⭐ 事件类型
const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    console.log(e.target.value);
};

const handleClick = (e: React.MouseEvent<HTMLButtonElement>) => {
    console.log(e.clientX, e.clientY);
};

// ⭐ 自定义 Hook 泛型
function useLocalStorage<T>(key: string, initialValue: T): [T, (value: T | ((prev: T) => T)) => void] {
    const [storedValue, setStoredValue] = useState<T>(() => {
        const item = window.localStorage.getItem(key);
        return item ? JSON.parse(item) : initialValue;
    });

    const setValue = (value: T | ((prev: T) => T)) => {
        const valueToStore = value instanceof Function ? value(storedValue) : value;
        setStoredValue(valueToStore);
        window.localStorage.setItem(key, JSON.stringify(valueToStore));
    };

    return [storedValue, setValue];
}
```

---

## 十六、测试

### 安装

```bash
npm install vitest @testing-library/react @testing-library/jest-dom jsdom
```

### vitest 配置

```js
// vite.config.js
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
    plugins: [react()],
    test: {
        environment: "jsdom",
        globals: true,
        setupFiles: "./src/test/setup.js",
    },
});
```

### 组件测试

```jsx
// src/test/setup.js
import "@testing-library/jest-dom";
```

```jsx
// Counter.test.jsx
import { render, screen, fireEvent } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import Counter from "./Counter";

describe("Counter 组件", () => {
    it("应该渲染初始计数", () => {
        render(<Counter />);
        expect(screen.getByText("计数：0")).toBeInTheDocument();
    });

    it("点击按钮应该增加计数", () => {
        render(<Counter />);
        const button = screen.getByRole("button", { name: /\+1/ });
        fireEvent.click(button);
        expect(screen.getByText("计数：1")).toBeInTheDocument();
    });

    it("应该调用 onClick 回调", () => {
        const handleClick = vi.fn();
        render(<Button onClick={handleClick}>点击</Button>);
        fireEvent.click(screen.getByText("点击"));
        expect(handleClick).toHaveBeenCalledTimes(1);
    });
});
```

---

## 十七、React 19 新特性（了解）

> [!info] React 19 于 2024 年底发布，以下是一些重要新特性。

### use() — 直接在渲染阶段读取 Promise 或 Context

```jsx
import { use, Suspense } from "react";

// ⭐ use() 可以直接在组件中使用 Promise
function UserData({ userPromise }) {
    const user = use(userPromise); // 会"挂起"组件直到 Promise resolve
    return <div>{user.name}</div>;
}

function UserPage({ userId }) {
    const userPromise = fetchUser(userId);

    return (
        <Suspense fallback={<div>加载中...</div>}>
            <UserData userPromise={userPromise} />
        </Suspense>
    );
}
```

### Actions（表单处理）

```jsx
function AddTodo() {
    // ⭐ form action：自动管理 pending 状态
    const [error, submitAction, isPending] = useActionState(async (previousState, formData) => {
        const title = formData.get("title");
        const res = await fetch("/api/todos", {
            method: "POST",
            body: JSON.stringify({ title }),
        });
        if (!res.ok) return { error: "添加失败" };
        return { success: true };
    }, null);

    return (
        <form action={submitAction}>
            <input name="title" required />
            {error && <p>{error}</p>}
            <button type="submit" disabled={isPending}>
                {isPending ? "添加中..." : "添加"}
            </button>
        </form>
    );
}
```

### useOptimistic — 乐观更新

```jsx
import { useOptimistic, useRef } from "react";

function MessageList({ messages, sendMessage }) {
    const [optimisticMessages, addOptimisticMessage] = useOptimistic(
        messages,
        (state, newMessage) => [...state, { text: newMessage, sending: true }]
    );

    const formRef = useRef(null);

    async function formAction(formData) {
        const text = formData.get("message");
        // ⭐ 立即在 UI 中显示，不需要等服务器响应
        addOptimisticMessage(text);
        formRef.current.reset();
        await sendMessage(text); // 实际发送
    }

    return (
        <form ref={formRef} action={formAction}>
            <input name="message" required />
            <button type="submit">发送</button>
            <ul>
                {optimisticMessages.map((msg, i) => (
                    <li key={i} className={msg.sending ? "sending" : ""}>
                        {msg.text} {msg.sending && "⏳"}
                    </li>
                ))}
            </ul>
        </form>
    );
}
```

---

## 十八、完整实战：Todo List ⭐

### 项目结构

```
src/
├── components/
│   ├── TodoInput.jsx
│   ├── TodoList.jsx
│   └── TodoItem.jsx
├── hooks/
│   └── useLocalStorage.js
├── App.jsx
└── main.jsx
```

### App.jsx

```jsx
import { useState, useCallback } from "react";
import TodoInput from "./components/TodoInput";
import TodoList from "./components/TodoList";

// 过滤类型
const FILTERS = ["全部", "待完成", "已完成"];

export default function App() {
    const [todos, setTodos] = useState(() => {
        const saved = localStorage.getItem("todos");
        return saved ? JSON.parse(saved) : [];
    });
    const [filter, setFilter] = useState("全部");

    // 保存到 localStorage
    const saveTodos = useCallback((newTodos) => {
        setTodos(newTodos);
        localStorage.setItem("todos", JSON.stringify(newTodos));
    }, []);

    // 添加待办
    const addTodo = useCallback(
        (text) => {
            const newTodo = {
                id: Date.now(),
                text,
                completed: false,
                createdAt: new Date().toISOString(),
            };
            saveTodos([...todos, newTodo]);
        },
        [todos, saveTodos]
    );

    // 切换完成状态
    const toggleTodo = useCallback(
        (id) => {
            saveTodos(
                todos.map((todo) =>
                    todo.id === id ? { ...todo, completed: !todo.completed } : todo
                )
            );
        },
        [todos, saveTodos]
    );

    // 删除待办
    const deleteTodo = useCallback(
        (id) => {
            saveTodos(todos.filter((todo) => todo.id !== id));
        },
        [todos, saveTodos]
    );

    // 过滤
    const filteredTodos = todos.filter((todo) => {
        if (filter === "待完成") return !todo.completed;
        if (filter === "已完成") return todo.completed;
        return true;
    });

    return (
        <div className="app">
            <h1>Todo List</h1>
            <TodoInput onAdd={addTodo} />

            <div className="filters">
                {FILTERS.map((f) => (
                    <button
                        key={f}
                        className={filter === f ? "active" : ""}
                        onClick={() => setFilter(f)}
                    >
                        {f}
                    </button>
                ))}
            </div>

            <TodoList todos={filteredTodos} onToggle={toggleTodo} onDelete={deleteTodo} />

            <div className="stats">
                <span>总计：{todos.length}</span>
                <span>已完成：{todos.filter((t) => t.completed).length}</span>
                <span>待完成：{todos.filter((t) => !t.completed).length}</span>
            </div>
        </div>
    );
}
```

### TodoInput.jsx

```jsx
import { useState } from "react";

export default function TodoInput({ onAdd }) {
    const [text, setText] = useState("");

    const handleSubmit = (e) => {
        e.preventDefault();
        if (!text.trim()) return;
        onAdd(text.trim());
        setText("");
    };

    return (
        <form onSubmit={handleSubmit} className="todo-input">
            <input
                type="text"
                value={text}
                onChange={(e) => setText(e.target.value)}
                placeholder="输入待办事项..."
            />
            <button type="submit" disabled={!text.trim()}>
                添加
            </button>
        </form>
    );
}
```

### TodoList.jsx

```jsx
import TodoItem from "./TodoItem";

export default function TodoList({ todos, onToggle, onDelete }) {
    if (todos.length === 0) {
        return <p className="empty">暂无待办事项</p>;
    }

    return (
        <ul className="todo-list">
            {todos.map((todo) => (
                <TodoItem key={todo.id} todo={todo} onToggle={onToggle} onDelete={onDelete} />
            ))}
        </ul>
    );
}
```

### TodoItem.jsx

```jsx
import { memo } from "react";

const TodoItem = memo(function TodoItem({ todo, onToggle, onDelete }) {
    return (
        <li className={`todo-item ${todo.completed ? "completed" : ""}`}>
            <input
                type="checkbox"
                checked={todo.completed}
                onChange={() => onToggle(todo.id)}
            />
            <span>{todo.text}</span>
            <button onClick={() => onDelete(todo.id)} className="delete">
                删除
            </button>
        </li>
    );
});

export default TodoItem;
```

### 样式

```css
/* App.css */
.app {
    max-width: 500px;
    margin: 50px auto;
    font-family: Arial, sans-serif;
}

.todo-input {
    display: flex;
    gap: 8px;
    margin-bottom: 20px;
}

.todo-input input {
    flex: 1;
    padding: 8px 12px;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 16px;
}

.todo-input button {
    padding: 8px 16px;
    background: #646cff;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

.todo-input button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.filters {
    display: flex;
    gap: 8px;
    margin-bottom: 16px;
}

.filters button {
    padding: 4px 12px;
    border: 1px solid #ddd;
    border-radius: 4px;
    background: white;
    cursor: pointer;
}

.filters button.active {
    background: #646cff;
    color: white;
    border-color: #646cff;
}

.todo-list {
    list-style: none;
    padding: 0;
}

.todo-item {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 10px;
    border-bottom: 1px solid #eee;
}

.todo-item.completed span {
    text-decoration: line-through;
    color: #999;
}

.todo-item span {
    flex: 1;
}

.delete {
    background: none;
    border: none;
    color: #ff4444;
    cursor: pointer;
    opacity: 0;
    transition: opacity 0.2s;
}

.todo-item:hover .delete {
    opacity: 1;
}

.empty {
    text-align: center;
    color: #999;
    padding: 40px;
}

.stats {
    display: flex;
    gap: 16px;
    justify-content: center;
    margin-top: 20px;
    font-size: 14px;
    color: #666;
}
```

---

## 十九、React 面试常见问题

### 1. 虚拟 DOM 的原理是什么？

> **虚拟 DOM（Virtual DOM）** 是真实 DOM 的 JavaScript 对象表示。当数据变化时，React 先用新数据生成新的 Virtual DOM 树，然后通过 Diff 算法对比新旧两棵树的差异，最后只将差异部分批量更新到真实 DOM 上。这样做避免了频繁操作真实 DOM 带来的性能开销。

### 2. React 中的 key 有什么作用？

> `key` 帮助 React 识别哪些元素发生了变化（增删改）。在 Diff 过程中，React 通过 `key` 来判断一个元素是"移动"了还是"新建"了。**不支持用索引（index）作为 key**，因为索引会随列表变化，导致性能问题和状态错乱。

### 3. useEffect 和 useLayoutEffect 的区别？

> `useEffect` 是**异步**执行（在浏览器绘制之后），不会阻塞视觉更新，适合数据请求、事件绑定等。`useLayoutEffect` 是**同步**执行（在浏览器绘制之前），会阻塞视觉更新，适合 DOM 测量、读取布局等需要在绘制前完成的操作。

### 4. 什么是闭包陷阱？如何避免？

> 在 Hooks 中，由于闭包捕获了旧的 state 值，导致回调中访问的是"过时"的数据。例如 `useEffect` 中调用了 `setTimeout`，在定时器回调中访问 state，得到的是创建定时器时的值。
>
> **解决方法**：使用函数式更新 `setCount(prev => prev + 1)`、添加正确的依赖数组、或使用 `useRef` 保存最新值。

### 5. React 18 的自动批处理是什么？

> 在 React 18 之前，只有 React 事件处理函数中的 setState 会被批量合并。React 18 将批处理扩展到所有场景（Promise、setTimeout、原生事件等）。这意味着在一个异步回调中多次调用 `setState`，组件只会重渲染一次。

### 6. 受控组件和非受控组件的区别？

> **受控组件**：表单数据由 React state 控制，输入变化通过 `onChange` 更新 state，state 是"唯一数据源"。**非受控组件**：表单数据由 DOM 自身管理，通过 `ref` 获取值。推荐使用受控组件，因为它更符合 React 的单向数据流理念，且便于实时校验。

### 7. React.memo 和 useMemo 的区别？

> `React.memo` 是一个高阶组件，用来包裹组件，当 props 没有变化时跳过组件渲染。`useMemo` 是一个 Hook，用来缓存计算结果，只有依赖变化时才重新计算。两者都用于性能优化，但作用对象不同：`React.memo` 针对组件，`useMemo` 针对值。

### 8. 什么是状态提升（Lifting State Up）？

> 当多个组件需要共享同一份状态时，将状态提升到它们最近的共同父组件中管理，然后通过 props 传递给子组件。这是 React 中最基本的共享状态模式。

### 9. 如何实现代码分割？

> 使用 `React.lazy()` 动态导入组件，配合 `Suspense` 组件提供加载状态。`React.lazy(() => import('./MyComponent'))` 会在组件首次渲染时才加载对应的 JavaScript 包。通常结合路由实现页面级别的代码分割。

### 10. Fiber 架构是什么？

> React 16 引入的新的协调引擎。Fiber 将渲染工作分解为小的"工作单元"，允许**中断和恢复**渲染过程，从而实现**并发模式**。这样 React 可以优先处理高优先级的更新（如用户输入），延迟低优先级的更新（如数据加载）。

---

> [!tip] **学习路径建议**
> 1. **入门**：JSX → 组件 → Props → State → 事件处理
> 2. **进阶**：useEffect → useRef → 自定义 Hooks → Context
> 3. **深入**：useReducer → React.memo → useMemo/useCallback → 代码分割
> 4. **生态系统**：React Router → Zustand → 测试 → TypeScript
> 5. **实战**：完成 Todo List → 仿写常见页面 → 参与开源项目
