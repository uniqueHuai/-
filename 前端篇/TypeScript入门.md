# TypeScript 入门

## 一、TypeScript 概述

### 什么是 TypeScript

**TypeScript（TS）** 是微软开发的开源编程语言，是 **JavaScript 的超集**，在 JS 基础上添加了**静态类型系统**。

```
JavaScript（弱类型、动态）
     │ 加类型
     ▼
TypeScript（强类型、静态）——编译——► JavaScript（浏览器/Node 运行）
```

| 特性 | 说明 |
|:----:|------|
| **类型安全** | 在编译阶段发现类型错误，减少运行时 bug |
| **增强 IDE** | 自动补全、重构、跳转定义、错误提示 |
| **渐进采用** | 现有 JS 项目可以逐步迁移 |
| **社区生态** | 主流框架（React、Vue、Angular）都支持 TS |
| **标准兼容** | 遵循 ECMAScript 标准，支持最新 JS 特性 |

### 快速开始

```bash
# 1. 全局安装 TypeScript
npm install -g typescript

# 2. 查看版本
tsc --version

# 3. 编译 TS 文件
tsc hello.ts    # 生成 hello.js

# 4. 监听模式（自动编译）
tsc hello.ts --watch
```

### 项目配置 tsconfig.json ⭐

```bash
# 生成 tsconfig.json
tsc --init
```

```json
{
    "compilerOptions": {
        /* 目标与模块 */
        "target": "ES2020",           // 编译目标版本
        "module": "ESNext",           // 模块系统
        "moduleResolution": "bundler", // 模块解析策略

        /* 严格模式（⭐ 推荐启用） */
        "strict": true,               // 启用所有严格检查
        "noImplicitAny": true,        // 禁止隐式 any
        "strictNullChecks": true,     // 严格的 null 检查
        "noUnusedLocals": true,       // 未使用的局部变量报错

        /* 输出 */
        "outDir": "./dist",           // 输出目录
        "rootDir": "./src",           // 源码目录
        "sourceMap": true,            // 生成 source map

        /* 其他 */
        "esModuleInterop": true,      // 兼容 CommonJS 模块
        "skipLibCheck": true,         // 跳过声明文件检查
        "forceConsistentCasingInFileNames": true
    },
    "include": ["src/**/*"],          // 包含的文件
    "exclude": ["node_modules"]       // 排除的文件
}
```

### 使用项目

```bash
# 编译整个项目
tsc

# 监听模式
tsc --watch
```

---

## 二、基础类型

### 原始类型

```typescript
// ⭐ 基本类型（小写）
let name: string = "张三";
let age: number = 25;
let isDone: boolean = false;
let big: bigint = 100n;
let sym: symbol = Symbol("unique");

// ⭐ 类型推断（TS 会自动推断类型）
let message = "Hello";  // message 被推断为 string 类型
// message = 123;       // ❌ 错误！不能将 number 赋值给 string

// ⭐ 空值
let u: undefined = undefined;
let n: null = null;
let v: void = undefined;  // void 表示没有返回值
```

### 数组和元组

```typescript
// ⭐ 数组
let list1: number[] = [1, 2, 3];
let list2: Array<string> = ["a", "b", "c"];  // 泛型写法

// 只读数组
let readonlyList: ReadonlyArray<number> = [1, 2, 3];
// readonlyList.push(4);  // ❌ 只读，不能修改

// ⭐ 元组（Tuple）：固定长度和类型的数组
let tuple: [string, number, boolean] = ["张三", 25, true];
// let wrong: [string, number] = ["张三", 25, true];  // ❌ 长度不对

// 可选元素
let optionalTuple: [string, number?] = ["张三"];
optionalTuple = ["张三", 25];  // ✅

// 命名元组（TS 4.0+）
let namedTuple: [name: string, age: number] = ["张三", 25];
```

### any / unknown / never

```typescript
// ⚠️ any：关闭类型检查（尽量少用）
let value: any = 42;
value = "hello";   // ✅
value = true;      // ✅
value.foo();       // ✅ 运行时可能报错，但 TS 不检查

// ⭐ unknown：安全的 any（使用前必须进行类型检查）
let unknownValue: unknown = 42;
unknownValue = "hello";         // ✅
// unknownValue.toUpperCase();  // ❌ 无法直接调用方法

// 必须先进行类型检查才能操作
if (typeof unknownValue === "string") {
    unknownValue.toUpperCase();  // ✅ 类型收窄后可以调用
}

// ⭐ never：永不存在的值
function throwError(message: string): never {
    throw new Error(message);
}

function infiniteLoop(): never {
    while (true) {}
}

// never 在 exhaustiveness check 中的应用
type Shape = "circle" | "square" | "triangle";

function getArea(shape: Shape): number {
    switch (shape) {
        case "circle": return 1;
        case "square": return 2;
        case "triangle": return 3;
        default:
            // 如果 Shape 新增了类型但没加 case，这里会报错
            const exhaustive: never = shape;
            return exhaustive;
    }
}
```

> [!tip] **类型使用优先级**
> ```
> ✅ 明确类型（string, number, interface...）
> ✅ unknown（不确定但有类型安全）
> ⚠️ any（不得已时使用）
> ```

---

## 三、接口（interface）

### 基本用法

```typescript
// ⭐ interface：定义对象的结构
interface User {
    readonly id: number;          // 只读属性（只能在创建时赋值）
    name: string;
    age: number;
    email?: string;               // 可选属性
    readonly createdAt: Date;     // 只读
}

function greet(user: User): string {
    return `Hello, ${user.name}!`;
}

const user: User = {
    id: 1,
    name: "张三",
    age: 25,
    createdAt: new Date(),
};

// user.id = 2;  // ❌ 只读属性不能修改
```

### 接口继承

```typescript
interface Animal {
    name: string;
    speak(): void;
}

// ⭐ 接口可以继承多个
interface Dog extends Animal {
    breed: string;
    wagTail(): void;
}

interface Pet extends Animal {
    owner: string;
}

// 多继承
interface FamilyDog extends Dog, Pet {
    favoriteToy: string;
}

// 使用
const myDog: FamilyDog = {
    name: "旺财",
    breed: "金毛",
    owner: "张三",
    favoriteToy: "飞盘",
    speak() {
        console.log("汪汪！");
    },
    wagTail() {
        console.log("摇尾巴...");
    },
};
```

### 接口合并（Declaration Merging）

```typescript
// ⭐ 同名接口会自动合并
interface User {
    name: string;
}

interface User {
    age: number;  // 合并后 User 有 name 和 age
}

const user: User = { name: "张三", age: 25 };  // ✅
```

### 函数类型接口

```typescript
// ⭐ 定义函数类型
interface SearchFn {
    (source: string, subString: string): boolean;
}

let search: SearchFn = function (src, sub) {
    return src.includes(sub);
};

// 等价写法：类型别名
type SearchFnType = (source: string, subString: string) => boolean;
```

### 索引签名

```typescript
// ⭐ 索引签名：定义动态属性的类型
interface StringDictionary {
    [key: string]: string;
}

interface Dictionary<T> {
    [key: string]: T;
}

// 混合类型
interface Config {
    name: string;
    [key: string]: unknown;  // 允许其他任意属性
}

const config: Config = {
    name: "app",
    version: "1.0",
    debug: true,
};
```

---

## 四、类型别名（type）

### 基本用法

```typescript
// ⭐ type vs interface
type User = {
    name: string;
    age: number;
};

// type 可以为原始类型创建别名
type ID = string | number;
type Status = "active" | "inactive" | "pending";
type Point = [number, number];  // 元组类型

// 使用
let userId: ID = "abc123";
userId = 456;  // ✅ string | number 都行
```

### type 与 interface 的区别 ⭐

| 对比项 | interface | type |
|:------:|:---------:|:----:|
| **对象类型** | ✅ | ✅ |
| **联合类型** | ❌ | ✅ `type A = string \| number` |
| **交叉类型** | ❌ | ✅ `type A = B & C` |
| **元组类型** | ❌ | ✅ `type Point = [number, number]` |
| **映射类型** | ❌ | ✅ `type Readonly<T> = { readonly [K in keyof T]: T[K] }` |
| **声明合并** | ✅（同名自动合并） | ❌（同名报错） |
| **继承** | `extends` | 交叉类型 `&` |
| **实现** | `implements` | `implements` |

> [!tip] **选择建议**：定义对象类型时优先用 `interface`，需要联合/交叉/工具类型时用 `type`。

### 交叉类型（Intersection）

```typescript
interface Person {
    name: string;
    age: number;
}

interface Contact {
    email: string;
    phone: string;
}

// ⭐ 交叉类型：合并所有属性
type Employee = Person & Contact;

const emp: Employee = {
    name: "张三",
    age: 25,
    email: "zhangsan@example.com",
    phone: "13800138000",
};
```

---

## 五、联合类型与类型收窄

### 联合类型

```typescript
// ⭐ 联合类型：值可以是几种类型之一
type Status = "success" | "error" | "loading";
type Result = string | number | boolean;
type Shape = Circle | Square | Triangle;

function printId(id: number | string) {
    // 这里还不能直接调用 string 或 number 特有的方法
    // id.toUpperCase();   // ❌
    // id.toFixed();       // ❌
}
```

### 类型收窄（Narrowing）⭐

```typescript
// ⭐ 1. typeof 收窄
function printId(id: number | string) {
    if (typeof id === "string") {
        // 在这个分支中，id 被收窄为 string
        console.log(id.toUpperCase());
    } else {
        // 在这里，id 被收窄为 number
        console.log(id.toFixed(2));
    }
}

// ⭐ 2. 真值收窄
function getFirst(arr?: string[]) {
    if (arr && arr.length > 0) {
        return arr[0];
    }
    return undefined;
}

// ⭐ 3. 等值收窄
function checkStatus(status: "success" | "error" | "loading") {
    if (status === "success") {
        console.log("成功！");
    } else if (status === "error") {
        console.log("失败！");
    }
}

// ⭐ 4. in 操作符收窄
interface Fish { swim(): void; }
interface Bird { fly(): void; }

function move(animal: Fish | Bird) {
    if ("swim" in animal) {
        animal.swim();  // 收窄为 Fish
    } else {
        animal.fly();   // 收窄为 Bird
    }
}

// ⭐ 5. instanceof 收窄
function logValue(x: Date | string) {
    if (x instanceof Date) {
        console.log(x.toISOString());  // Date
    } else {
        console.log(x.toUpperCase());  // string
    }
}

// ⭐ 6. 可区分联合（Discriminated Unions）
interface Circle {
    kind: "circle";
    radius: number;
}

interface Square {
    kind: "square";
    sideLength: number;
}

interface Triangle {
    kind: "triangle";
    base: number;
    height: number;
}

type Shape = Circle | Square | Triangle;

function getArea(shape: Shape): number {
    switch (shape.kind) {
        // ⭐ TS 会根据 kind 字段自动收窄
        case "circle":
            return Math.PI * shape.radius ** 2;
        case "square":
            return shape.sideLength ** 2;
        case "triangle":
            return (shape.base * shape.height) / 2;
        default:
            // 确保所有类型都被处理
            const exhaustive: never = shape;
            return exhaustive;
    }
}
```

---

## 六、函数类型

### 函数声明

```typescript
// ⭐ 完整的函数类型注解
function add(x: number, y: number): number {
    return x + y;
}

// 箭头函数
const multiply = (x: number, y: number): number => {
    return x * y;
};

// 可选参数（必须放在必选参数之后）
function greet(name: string, greeting?: string): string {
    return `${greeting || "Hello"}, ${name}!`;
}

// 默认参数
function createUser(name: string, age: number = 18): User {
    return { name, age };
}

// 剩余参数
function sum(...numbers: number[]): number {
    return numbers.reduce((acc, curr) => acc + curr, 0);
}
```

### 函数重载

```typescript
// ⭐ 函数重载：同一个函数有不同的参数类型组合
// 1. 重载签名
function reverse(x: string): string;
function reverse(x: number): number;

// 2. 实现签名（兼容所有重载）
function reverse(x: string | number): string | number {
    if (typeof x === "string") {
        return x.split("").reverse().join("");
    }
    return Number(x.toString().split("").reverse().join(""));
}

// 使用
reverse("hello");  // "olleh"
reverse(12345);    // 54321
// reverse(true);  // ❌ 不匹配任何重载
```

### this 类型

```typescript
// ⭐ 指定 this 的类型
interface User {
    name: string;
    age: number;
}

function greetUser(this: User, greeting: string): string {
    return `${greeting}, ${this.name}!`;
}

const user = { name: "张三", age: 25 };
greetUser.call(user, "你好");  // "你好, 张三!"

// ⭐ 在对象方法中使用
const calculator = {
    value: 0,
    add(this: { value: number }, x: number) {
        this.value += x;
        return this;
    },
    subtract(this: { value: number }, x: number) {
        this.value -= x;
        return this;
    },
};
```

---

## 七、类（Class）

### 基本语法

```typescript
// ⭐ TypeScript 中的类
class Animal {
    // 属性声明（需要显式声明）
    readonly id: number;        // 只读
    protected name: string;     // 受保护（子类可访问）
    private age: number;        // 私有的（仅当前类可访问）
    public species: string;     // 公开的（默认）

    // 静态属性
    static category = "动物";

    // 构造函数
    constructor(name: string, age: number, species: string) {
        this.id = Date.now();
        this.name = name;
        this.age = age;
        this.species = species;
    }

    // 方法
    public speak(): void {
        console.log(`${this.name} 在叫`);
    }

    // 静态方法
    static isAnimal(obj: unknown): boolean {
        return obj instanceof Animal;
    }

    // getter / setter
    get ageInHumanYears(): number {
        return this.age * 7;
    }

    set ageInHumanYears(years: number) {
        this.age = Math.floor(years / 7);
    }
}

const dog = new Animal("旺财", 3, "狗");
// dog.id = 2;       // ❌ 只读
// dog.name;         // ❌ 受保护，外部不可访问
// dog.age;          // ❌ 私有，外部不可访问
console.log(dog.species);  // ✅ "狗"
```

### 简洁语法 ⭐

```typescript
// ⭐ 参数属性简写（直接在构造函数中声明）
class Person {
    constructor(
        public name: string,        // 自动创建并初始化 this.name
        private age: number,        // 自动创建并初始化 this.age
        readonly id: number = Date.now()  // 自动创建并初始化
    ) {}

    greet(): void {
        console.log(`你好，我是${this.name}，今年${this.age}岁`);
    }
}

const p = new Person("张三", 25);
console.log(p.name);   // ✅ "张三"
// console.log(p.age); // ❌ 私有
```

### 继承

```typescript
class Dog extends Animal {
    constructor(
        name: string,
        age: number,
        public breed: string  // 新增属性
    ) {
        super(name, age, "狗");  // ⭐ 必须调用 super()
    }

    // ⭐ 重写方法
    speak(): void {
        super.speak();       // 调用父类方法
        console.log("汪汪！");
    }
}
```

### 抽象类

```typescript
// ⭐ 抽象类：不能被实例化，只能被继承
abstract class Shape {
    abstract getArea(): number;  // 抽象方法，子类必须实现

    // 普通方法
    describe(): string {
        return `面积是 ${this.getArea()}`;
    }
}

class Circle extends Shape {
    constructor(private radius: number) {
        super();
    }

    // 必须实现抽象方法
    getArea(): number {
        return Math.PI * this.radius ** 2;
    }
}

// const shape = new Shape();  // ❌ 不能实例化抽象类
const circle = new Circle(5);
console.log(circle.describe());  // ✅
```

### 类实现接口

```typescript
interface Flyable {
    fly(): void;
    land(): void;
}

interface Swimmable {
    swim(): void;
}

// ⭐ 类实现多个接口
class Duck implements Flyable, Swimmable {
    fly(): void {
        console.log("鸭子飞");
    }

    land(): void {
        console.log("鸭子降落");
    }

    swim(): void {
        console.log("鸭子游泳");
    }
}
```

---

## 八、泛型（Generics）⭐

> [!info] 泛型是 TypeScript 最核心的功能之一，它让类型可以像参数一样"传参"，实现 **类型安全 + 复用**。

### 泛型函数

```typescript
// ⭐ 泛型函数：不指定具体类型，而是由调用时决定
function identity<T>(arg: T): T {
    return arg;
}

// 使用（类型推断）
const result1 = identity("hello");    // T 推断为 string
const result2 = identity(42);         // T 推断为 number

// 显式指定类型
const result3 = identity<boolean>(true);

// ⭐ 多个泛型参数
function pair<T, U>(first: T, second: U): [T, U] {
    return [first, second];
}

const p = pair("张三", 25);  // [string, number]
```

### 泛型约束

```typescript
// ⭐ 使用 extends 约束泛型
interface HasLength {
    length: number;
}

function logLength<T extends HasLength>(arg: T): T {
    console.log(arg.length);  // 确保 T 一定有 length 属性
    return arg;
}

logLength("hello");     // ✅ string 有 length
logLength([1, 2, 3]);   // ✅ array 有 length
// logLength(123);      // ❌ number 没有 length

// ⭐ keyof 约束
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
    return obj[key];
}

const user = { name: "张三", age: 25, email: "test@example.com" };
getProperty(user, "name");   // ✅ string
getProperty(user, "age");    // ✅ number
// getProperty(user, "xxx"); // ❌ "xxx" 不在 keyof User 中
```

### 泛型接口

```typescript
// ⭐ 泛型接口
interface ApiResponse<T> {
    code: number;
    message: string;
    data: T;
}

interface User {
    id: number;
    name: string;
}

interface Product {
    id: number;
    title: string;
    price: number;
}

// 使用
const userResponse: ApiResponse<User> = {
    code: 200,
    message: "成功",
    data: { id: 1, name: "张三" },
};

const productResponse: ApiResponse<Product[]> = {
    code: 200,
    message: "成功",
    data: [{ id: 1, title: "商品1", price: 100 }],
};
```

### 泛型类

```typescript
// ⭐ 泛型类
class Stack<T> {
    private items: T[] = [];

    push(item: T): void {
        this.items.push(item);
    }

    pop(): T | undefined {
        return this.items.pop();
    }

    peek(): T | undefined {
        return this.items[this.items.length - 1];
    }

    get size(): number {
        return this.items.length;
    }
}

const numberStack = new Stack<number>();
numberStack.push(1);
numberStack.push(2);
console.log(numberStack.pop());  // 2

const stringStack = new Stack<string>();
stringStack.push("hello");
stringStack.push("world");
```

### 泛型工具类型 ⭐

```typescript
// ⭐ Partial<T>：所有属性变为可选
interface Todo {
    title: string;
    description: string;
    completed: boolean;
}

function updateTodo(todo: Todo, fieldsToUpdate: Partial<Todo>) {
    return { ...todo, ...fieldsToUpdate };
}

// ⭐ Required<T>：所有属性变为必选
type RequiredTodo = Required<Partial<Todo>>;

// ⭐ Readonly<T>：所有属性变为只读
type ReadonlyTodo = Readonly<Todo>;

// ⭐ Pick<T, K>：从 T 中选取部分属性
type TodoPreview = Pick<Todo, "title" | "completed">;

// ⭐ Omit<T, K>：从 T 中排除部分属性
type TodoWithoutDesc = Omit<Todo, "description">;

// ⭐ Record<K, T>：创建键值类型
type PageInfo = Record<string, { title: string; url: string }>;
const pages: PageInfo = {
    home: { title: "首页", url: "/" },
    about: { title: "关于", url: "/about" },
};

// ⭐ Exclude<T, U>：从联合类型中排除
type T0 = Exclude<"a" | "b" | "c", "a">;  // "b" | "c"

// ⭐ Extract<T, U>：从联合类型中提取
type T1 = Extract<"a" | "b" | "c", "a" | "f">;  // "a"

// ⭐ NonNullable<T>：排除 null 和 undefined
type T2 = NonNullable<string | number | null | undefined>;  // string | number

// ⭐ ReturnType<T>：获取函数返回类型
type Fn = (x: number) => string;
type T3 = ReturnType<Fn>;  // string

// ⭐ Parameters<T>：获取函数参数类型
type T4 = Parameters<Fn>;  // [x: number]
```

### 条件类型 ⭐

```typescript
// ⭐ 条件类型：根据条件返回不同的类型
type IsString<T> = T extends string ? "yes" : "no";

type A = IsString<string>;   // "yes"
type B = IsString<number>;   // "no"

// ⭐ infer：在条件类型中推断类型
type ReturnType2<T> = T extends (...args: unknown[]) => infer R ? R : never;

type FnType = (x: number) => string;
type R = ReturnType2<FnType>;  // string

// ⭐ 实际应用：提取 Promise 值类型
type Unwrap<T> = T extends Promise<infer U> ? U : T;
type PromiseValue = Unwrap<Promise<string>>;  // string
type NormalValue = Unwrap<number>;             // number

// ⭐ 实际应用：联合类型转交叉类型
type UnionToIntersection<U> = (U extends unknown ? (k: U) => void : never) extends (
    k: infer I
) => void
    ? I
    : never;
```

---

## 九、类型断言

```typescript
// ⭐ 类型断言：告诉 TS "我知道这个值的类型"

// 方式一：as 语法（推荐）
const someValue: unknown = "hello";
const strLength = (someValue as string).length;

// 方式二：尖括号语法（不推荐，会和 JSX 冲突）
const len = (<string>someValue).length;

// ⭐ 非空断言（!）
function processUser(user?: User | null) {
    // 确定 user 不为 null/undefined 时使用
    const name = user!.name;
}

// ⭐ const 断言
const config = {
    server: "localhost",
    port: 3000,
} as const;
// config.port = 4000;  // ❌ 所有属性变为 readonly

// as const 在数组中的使用
const colors = ["red", "green", "blue"] as const;
// colors.push("yellow");  // ❌ 只读
type Color = (typeof colors)[number];  // "red" | "green" | "blue"

// ⭐ 双重断言（谨慎使用）
const exp: string = "hello";
// 先断言为 unknown，再断言为目标类型
const num = exp as unknown as number;  // ⚠️ 可能会在运行时出错
```

> [!warning] **类型断言不是类型转换**。它不会在运行时改变值的类型，只是在编译时告诉 TS 信任你。如果断言错误，运行时可能会出现 TypeError。

---

## 十、枚举（Enum）

### 数字枚举

```typescript
// ⭐ 数字枚举（默认从 0 递增）
enum Direction {
    Up,      // 0
    Down,    // 1
    Left,    // 2
    Right,   // 3
}

const dir: Direction = Direction.Up;

// ⭐ 自定义初始值
enum Status {
    Active = 1,
    Inactive,    // 2（自动递增）
    Pending,     // 3
    Archived = 10,
    Deleted,     // 11
}

// ⭐ 反向映射
console.log(Direction[0]);     // "Up"
console.log(Direction.Up);     // 0
```

### 字符串枚举

```typescript
// ⭐ 字符串枚举（每个成员必须有初始值）
enum HttpMethod {
    GET = "GET",
    POST = "POST",
    PUT = "PUT",
    DELETE = "DELETE",
}

function makeRequest(url: string, method: HttpMethod) {
    fetch(url, { method });
}

makeRequest("/api/users", HttpMethod.GET);
// makeRequest("/api/users", "GET");  // ❌ 类型不匹配
```

### const 枚举

```typescript
// ⭐ const 枚举：编译时会被完全抹除，提升性能
const enum Size {
    Small = "S",
    Medium = "M",
    Large = "L",
}

const mySize = Size.Medium;  // 编译后直接变成 "M"
```

---

## 十一、模块与命名空间

### 模块（ES Modules）

```typescript
// ⭐ 模块：推荐使用 ES Module 语法

// utils/math.ts
export function add(x: number, y: number): number {
    return x + y;
}

export const PI = 3.14159;

export interface Result {
    sum: number;
    average: number;
}

// 默认导出
export default class Calculator {
    add(x: number, y: number): number {
        return x + y;
    }
}

// 导入
import Calculator, { add, PI, type Result } from "./utils/math";

// ⭐ 类型导入（type 关键字，编译时会被移除）
import type { User } from "./types";
import { type ApiResponse, fetchData } from "./api";
```

### 命名空间（namespace）

```typescript
// ⭐ namespace（不推荐在新项目中使用，了解即可）
namespace Validation {
    export interface StringValidator {
        isValid(s: string): boolean;
    }

    export class EmailValidator implements StringValidator {
        isValid(s: string): boolean {
            return s.includes("@");
        }
    }

    export class PhoneValidator implements StringValidator {
        isValid(s: string): boolean {
            return /^\d{11}$/.test(s);
        }
    }
}

// 使用
const emailValidator = new Validation.EmailValidator();
console.log(emailValidator.isValid("test@example.com"));
```

---

## 十二、声明文件（.d.ts）

### 什么是声明文件

```typescript
// ⭐ .d.ts 文件用于描述已有 JavaScript 库的类型信息
// 它们不会被编译成 JS，仅用于类型检查

// 常见的声明文件：
// - 库自带的：lodash、axios、react 自带 .d.ts
// - DefinitelyTyped：@types/react、@types/node
// - 自己写的：为纯 JS 库编写
```

### 安装类型声明

```bash
# 大部分库有类型声明
npm install typescript

# 有些需要从 DefinitelyTyped 安装
npm install -D @types/react
npm install -D @types/node
npm install -D @types/lodash
```

### 编写声明文件

```typescript
// globals.d.ts
// ⭐ 声明全局变量
declare const API_BASE_URL: string;

// 声明全局函数
declare function $(selector: string): HTMLElement | null;

// 声明全局类型
declare global {
    interface Window {
        __INITIAL_STATE__: Record<string, unknown>;
    }
}

// ⭐ 声明模块
declare module "*.vue" {
    import type { DefineComponent } from "vue";
    const component: DefineComponent<{}, {}, any>;
    export default component;
}

declare module "*.module.css" {
    const classes: { readonly [key: string]: string };
    export default classes;
}

// ⭐ 为现有模块添加类型（模块扩展）
import "axios";

declare module "axios" {
    interface AxiosRequestConfig {
        /** 请求重试次数 */
        retry?: number;
    }
}
```

---

## 十三、高级类型技巧

### 映射类型（Mapped Types）⭐

```typescript
// ⭐ 映射类型：基于已有类型创建新类型
type Readonly2<T> = {
    readonly [P in keyof T]: T[P];
};

type Optional<T> = {
    [P in keyof T]?: T[P];
};

type Nullable<T> = {
    [P in keyof T]: T[P] | null;
};

// 使用
interface Person {
    name: string;
    age: number;
}

type ReadonlyPerson = Readonly2<Person>;
type OptionalPerson = Optional<Person>;

// ⭐ 键名重映射（TS 4.1+）
type Getters<T> = {
    [K in keyof T as `get${Capitalize<string & K>}`]: () => T[K];
};

type PersonGetters = Getters<Person>;
// { getName: () => string; getAge: () => number }

// ⭐ 过滤属性
type Methods<T> = {
    [K in keyof T as T[K] extends Function ? K : never]: T[K];
};

interface UserService {
    name: string;
    age: number;
    getName(): string;
    setName(name: string): void;
}

type UserMethods = Methods<UserService>;
// { getName: () => string; setName: (name: string) => void }
```

### 模板字面量类型 ⭐

```typescript
// ⭐ 模板字面量类型（TS 4.1+）
type EventName = "click" | "focus" | "blur";
type HandlerName = `on${Capitalize<EventName>}`;
// "onClick" | "onFocus" | "onBlur"

// ⭐ 实际应用：事件监听器
type EventHandlers = {
    [K in EventName as `on${Capitalize<K>}`]: (event: Event) => void;
};

// ⭐ 字符串操作类型
type UppercaseName = Uppercase<"hello">;      // "HELLO"
type LowercaseName = Lowercase<"HELLO">;      // "hello"
type CapitalizeName = Capitalize<"hello">;    // "Hello"
type UncapitalizeName = Uncapitalize<"Hello">; // "hello"
```

### 实用工具类型实现

```typescript
// ⭐ 深度 Partial
type DeepPartial<T> = T extends object
    ? { [P in keyof T]?: DeepPartial<T[P]> }
    : T;

// ⭐ 深度 Readonly
type DeepReadonly<T> = T extends object
    ? { readonly [P in keyof T]: DeepReadonly<T[P]> }
    : T;

// ⭐ 函数类型提取
type FnReturnType<T> = T extends (...args: any[]) => infer R ? R : never;
type FnParams<T> = T extends (...args: infer P) => any ? P : never;

// ⭐ 联合类型转交叉类型
type UnionToIntersection2<U> = (
    U extends any ? (k: U) => void : never
) extends (k: infer I) => void
    ? I
    : never;

// ⭐ 非空值提取
type NonNull<T> = T extends null | undefined ? never : T;
```

---

## 十四、TypeScript 配置实战

### 不同项目的 tsconfig

```json
// ⭐ React 项目 tsconfig.json
{
    "compilerOptions": {
        "target": "ES2020",
        "jsx": "react-jsx",
        "module": "ESNext",
        "moduleResolution": "bundler",
        "strict": true,
        "esModuleInterop": true,
        "skipLibCheck": true,
        "forceConsistentCasingInFileNames": true,
        "resolveJsonModule": true,
        "isolatedModules": true,
        "noEmit": true,
        "baseUrl": ".",
        "paths": {
            "@/*": ["src/*"]
        }
    },
    "include": ["src"]
}
```

```json
// ⭐ Node.js 项目 tsconfig.json
{
    "compilerOptions": {
        "target": "ES2022",
        "module": "NodeNext",
        "moduleResolution": "NodeNext",
        "outDir": "./dist",
        "rootDir": "./src",
        "strict": true,
        "esModuleInterop": true,
        "skipLibCheck": true,
        "declaration": true,
        "sourceMap": true
    },
    "include": ["src"]
}
```

### 常见配置项说明

| 配置项 | 说明 | 推荐值 |
|:------:|:----:|:------:|
| `target` | 编译到哪个 JS 版本 | `ES2020` 或更高 |
| `module` | 模块系统 | `ESNext`、`NodeNext` |
| `strict` | 启用所有严格检查 | `true` |
| `strictNullChecks` | 严格的 null 检查 | `true` |
| `jsx` | JSX 支持 | `react-jsx`（React 17+） |
| `declaration` | 生成 .d.ts 文件 | 库项目用 `true` |
| `sourceMap` | 生成 source map | 调试用 `true` |
| `outDir` | 编译输出目录 | `./dist` |
| `rootDir` | 源码目录 | `./src` |
| `paths` | 路径别名 | React 项目常用 |

---

## 十五、React + TypeScript 实战 ⭐

### 组件定义

```tsx
// ⭐ Props 类型
interface ButtonProps {
    label: string;
    variant?: "primary" | "secondary" | "danger";
    size?: "sm" | "md" | "lg";
    disabled?: boolean;
    onClick?: (event: React.MouseEvent<HTMLButtonElement>) => void;
    children?: React.ReactNode;
}

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
```

### useState 泛型

```tsx
interface User {
    id: number;
    name: string;
    email: string;
}

function UserProfile() {
    // ⭐ 显式指定泛型
    const [user, setUser] = useState<User | null>(null);
    const [users, setUsers] = useState<User[]>([]);
    const [count, setCount] = useState(0);  // 推断为 number

    // ⭐ 复杂状态
    const [form, setForm] = useState({
        name: "",
        email: "",
        age: 0,
    });

    const updateField = (field: keyof typeof form, value: string | number) => {
        setForm((prev) => ({ ...prev, [field]: value }));
    };

    return <div>{/* ... */}</div>;
}
```

### useRef 泛型

```tsx
function Form() {
    // ⭐ DOM 元素引用
    const inputRef = useRef<HTMLInputElement>(null);
    const divRef = useRef<HTMLDivElement>(null);
    const formRef = useRef<HTMLFormElement>(null);

    // ⭐ 非 DOM 值（不需要初始值）
    const countRef = useRef<number>(0);

    const focusInput = () => {
        inputRef.current?.focus();  // ?. 可选链
    };

    return (
        <div ref={divRef}>
            <input ref={inputRef} type="text" />
            <button onClick={focusInput}>聚焦</button>
        </div>
    );
}
```

### 事件类型

```tsx
function EventDemo() {
    // ⭐ 常见事件类型
    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        console.log(e.target.value);
    };

    const handleClick = (e: React.MouseEvent<HTMLButtonElement>) => {
        console.log(e.clientX, e.clientY);
    };

    const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
    };

    const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
        if (e.key === "Enter") {
            console.log("按下了回车");
        }
    };

    const handleDrag = (e: React.DragEvent<HTMLDivElement>) => {
        console.log(e.dataTransfer);
    };

    return <>{/* ... */}</>;
}
```

### 自定义 Hook 泛型

```tsx
// ⭐ 泛型自定义 Hook
function useLocalStorage<T>(key: string, initialValue: T): [T, (value: T | ((prev: T) => T)) => void] {
    const [storedValue, setStoredValue] = useState<T>(() => {
        try {
            const item = window.localStorage.getItem(key);
            return item ? (JSON.parse(item) as T) : initialValue;
        } catch {
            return initialValue;
        }
    });

    const setValue = (value: T | ((prev: T) => T)) => {
        try {
            const valueToStore = value instanceof Function ? value(storedValue) : value;
            setStoredValue(valueToStore);
            window.localStorage.setItem(key, JSON.stringify(valueToStore));
        } catch (error) {
            console.error("保存失败：", error);
        }
    };

    return [storedValue, setValue];
}

// 使用
interface Settings {
    theme: "light" | "dark";
    fontSize: number;
}

const [settings, setSettings] = useLocalStorage<Settings>("settings", {
    theme: "light",
    fontSize: 14,
});
```

### 类型安全的 API 请求 ⭐

```tsx
// api/types.ts
interface ApiResponse<T> {
    code: number;
    message: string;
    data: T;
}

interface User {
    id: number;
    name: string;
    email: string;
}

interface Product {
    id: number;
    title: string;
    price: number;
}

// api/request.ts
async function fetchApi<T>(url: string, options?: RequestInit): Promise<T> {
    const response = await fetch(url, options);
    if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
    }
    return response.json();
}

// 使用
async function getUsers(): Promise<User[]> {
    const res = await fetchApi<ApiResponse<User[]>>("/api/users");
    return res.data;
}

async function getProduct(id: number): Promise<Product> {
    const res = await fetchApi<ApiResponse<Product>>(`/api/products/${id}`);
    return res.data;
}
```

---

## 十六、常见错误与最佳实践

### 常见错误及解决

```typescript
// 1. Object is possibly 'null' / 'undefined'
// ❌ 错误
function getName(user: User | null) {
    return user.name;  // Object is possibly 'null'
}

// ✅ 解决
function getName(user: User | null) {
    return user?.name;          // 可选链
    // return user!.name;       // 非空断言（确定不为 null 时）
    // return user ? user.name : "匿名";  // 三元运算符
    // if (user) return user.name;        // 类型收窄
}

// 2. Type 'X' is not assignable to type 'Y'
// ❌ 错误
const num: number = "hello";

// ✅ 解决：检查类型是否正确

// 3. Property 'X' does not exist on type 'Y'
// ❌ 错误
const obj = { name: "张三" };
// console.log(obj.age);  // 不存在 age 属性

// ✅ 解决：添加到 interface 或使用索引签名

// 4. Cannot find module 'X' or its corresponding type declarations
// ✅ 解决：安装 @types/包名 或创建 .d.ts 声明文件

// 5. Binding element 'X' implicitly has an 'any' type
// ✅ 解决：启用 strict 模式，或显式注解类型
```

### 最佳实践 ⭐

```typescript
// ⭐ 1. 优先用 interface 定义对象类型
interface User {
    name: string;
    age: number;
}

// ⭐ 2. 避免 any，用 unknown 代替
// ❌
function process(data: any) {
    data.name;  // 无类型安全
}
// ✅
function process(data: unknown) {
    if (data && typeof data === "object" && "name" in data) {
        console.log((data as { name: string }).name);
    }
}

// ⭐ 3. 使用 readonly 防止意外修改
interface Config {
    readonly apiKey: string;
    readonly endpoints: readonly string[];
}

// ⭐ 4. 使用 const 断言
const COLORS = ["red", "green", "blue"] as const;

// ⭐ 5. 使用 satisfies 操作符（TS 4.9+）
const palette = {
    red: [255, 0, 0],
    green: "#00ff00",
    blue: [0, 0, 255],
} satisfies Record<string, string | number[]>;

// palette.green 被推断为 string，而非 string | number[]

// ⭐ 6. 使用枚举还是联合类型？
// 需要反向映射 → 枚举
// 只是几个字符串 → 联合类型更简单
type Status = "active" | "inactive" | "pending";

// ⭐ 7. 明确导入类型（编译优化）
import type { User } from "./types";
import { fetchUsers, type ApiResponse } from "./api";

// ⭐ 8. 使用 satisfies 做类型验证
type Person = { name: string; age: number };

const person = {
    name: "张三",
    age: 25,
    // extraProp: "test"  // ❌ satisfies 会报多余属性
} satisfies Person;
```

---

## 十七、TypeScript 面试常见问题

### 1. TypeScript 和 JavaScript 的区别？

> TypeScript 是 JavaScript 的超集，在 JS 基础上增加了静态类型系统。TS 代码需要编译成 JS 才能运行。主要优势：**编译时发现类型错误**、更好的 IDE 支持（自动补全、重构）、更强的代码可读性和可维护性。

### 2. any、unknown、never 的区别？

> `any` 关闭类型检查，可以调用任何方法，没有类型安全。`unknown` 是类型安全的"未知类型"，使用前必须进行类型收窄。`never` 表示永远不会发生的值，常用于函数返回值（throw、无限循环）和 exhaustive check。

### 3. interface 和 type 的区别？

> `interface` 可以声明合并、只能定义对象类型。`type` 可以定义联合类型、交叉类型、元组、映射类型等。**定义对象类型时优先用 interface**，需要联合类型或复杂类型操作时用 type。

### 4. 什么是泛型约束？

> 使用 `extends` 关键字限制泛型可以接受的类型范围。例如 `<T extends HasLength>` 表示 T 必须有 length 属性。配合 `keyof` 可以约束属性名，确保类型安全地访问对象属性。

### 5. 什么是可区分联合（Discriminated Unions）？

> 当一个值是多个类型的联合时，通过一个公共的、字面量类型的属性（如 `kind`）来区分具体是哪个类型。TS 可以根据这个属性自动收窄类型，常用于处理复杂的联合类型场景。

### 6. 映射类型是什么？

> 映射类型可以基于已有类型的属性创建新类型。例如 `Partial<T>`、`Readonly<T>`、`Pick<T, K>` 等都是内置的映射类型。使用 `[P in keyof T]` 语法遍历属性。

### 7. 什么是条件类型？

> 条件类型根据条件返回不同的类型：`T extends U ? X : Y`。结合 `infer` 关键字可以从类型中推断类型变量，例如提取 Promise 的值类型、函数的返回值类型等。

### 8. declare 关键字的作用？

> `declare` 用于**声明**类型而不提供实现。常用于编写 `.d.ts` 声明文件，描述已有 JavaScript 库的类型信息，或声明全局变量/模块的类型。

### 9. 什么是模块增强（Module Augmentation）？

> 模块增强可以**扩展已有模块的类型定义**。例如在 axios 中添加自定义的请求配置选项 `AxiosRequestConfig.retry`，或在 vue 中添加全局属性 `$store`。

### 10. 如何处理第三方库没有类型声明？

> 1. 安装 `@types/库名`（如果 DefinitelyTyped 有）
> 2. 在 `.d.ts` 文件中使用 `declare module '库名'` 手动声明
> 3. 在 `tsconfig.json` 中设置 `"noImplicitAny": false`（不推荐）

---

> [!tip] **学习路径建议**
> 1. **入门**：基础类型 → 接口 → 类型别名 → 函数类型 → 类
> 2. **进阶**：泛型 → 类型收窄 → 联合/交叉类型 → 类型断言
> 3. **深入**：映射类型 → 条件类型 → 模板字面量类型 → 工具类型
> 4. **实战**：React + TypeScript → 自定义 Hook 泛型 → 项目配置
> 5. **补充**：声明文件 → 模块增强 → 类型体操挑战
