# FastAPI 篇

## 一、FastAPI 概述

FastAPI 是一个 **高性能**、**易学习**、**适合生产** 的 Python Web 框架，基于 Python 类型注解自动生成 OpenAPI 文档。

### 核心特点

| 特性 | 说明 |
|:----:|------|
| **高性能** | 性能媲美 Node.js 和 Go（基于 Starlette + Uvicorn） |
| **自动生成文档** | 内置 Swagger UI 和 ReDoc，零配置 |
| **类型安全** | 基于 Python 类型注解，自动校验和转换 |
| **异步原生** | 支持 `async/await`，也可以同步运行 |
| **依赖注入** | 强大的 DI 系统，代码解耦 |
| **生产就绪** | 自动验证、序列化、文档、安全 |

### 底层架构

```
FastAPI
  └── Starlette（Web 框架核心）
        ├── 路由、中间件、请求/响应
        ├── WebSocket、Server-Sent Events
        └── 后台任务、测试客户端
  └── Pydantic（数据校验）
        ├── BaseModel / Field 校验
        ├── JSON Schema 生成
        └── 序列化与反序列化
```

### 环境搭建

```bash
# 安装
pip install fastapi                    # FastAPI 本身
pip install uvicorn                    # ASGI 服务器（推荐）
pip install uvicorn[standard]          # 带性能增强

# 可选扩展
pip install python-multipart           # 表单/文件上传
pip install aiofiles                   # 异步文件操作
pip install httpx                      # TestClient 需要
pip install sqlalchemy asyncmy         # 数据库
pip install python-jose[cryptography]  # JWT 认证
pip install python-multipart           # OAuth2 表单
```

### Hello World

```python
from fastapi import FastAPI

app = FastAPI(title="我的第一个 API", version="1.0.0")

@app.get("/")
async def root():
    return {"message": "Hello, FastAPI!"}

@app.get("/health")
async def health():
    return {"status": "ok", "version": "1.0.0"}
```

```bash
# 启动服务
uvicorn main:app --reload     # 开发模式（热重载）
uvicorn main:app --port 8000  # 指定端口
```

启动后访问：
- API 交互文档：http://127.0.0.1:8000/docs（Swagger UI）
- 替代文档：http://127.0.0.1:8000/redoc（ReDoc）
- OpenAPI JSON：http://127.0.0.1:8000/openapi.json

> [!tip] `--reload` 会在代码变更时自动重启，**仅用于开发**，生产环境不要加。

---

## 二、路由与路径参数

### 基本路由

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/items")            # GET 请求
async def list_items():
    return [{"id": 1, "name": "Foo"}]

@app.post("/items")           # POST 请求
async def create_item():
    return {"message": "created"}

@app.put("/items/{item_id}")  # PUT 请求
async def update_item(item_id: int):
    return {"item_id": item_id}

@app.delete("/items/{item_id}")  # DELETE 请求
async def delete_item(item_id: int):
    return {"message": "deleted"}

@app.patch("/items/{item_id}")   # PATCH 请求
async def patch_item(item_id: int):
    return {"item_id": item_id}
```

### 路径参数（Path Parameters）

```python
from fastapi import FastAPI

app = FastAPI()

# 路径参数 — 类型自动转换
@app.get("/users/{user_id}")
async def get_user(user_id: int):          # 自动验证是否为 int
    return {"user_id": user_id}

# 多个路径参数
@app.get("/groups/{group_id}/users/{user_id}")
async def get_group_user(group_id: int, user_id: int):
    return {"group_id": group_id, "user_id": user_id}

# 路径枚举限制
from enum import Enum

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    vgg = "vgg"

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "深度学习先锋"}
    return {"model_name": model_name}

# 路径转换器（捕获完整路径）
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):       # :path 允许包含 /
    return {"file_path": file_path}
```

### 路由顺序

```python
# FastAPI 按定义顺序匹配路由
@app.get("/users/me")           # ① 特定路由放前面
async def get_current_user():
    return {"user": "current"}

@app.get("/users/{user_id}")    # ② 参数化路由放后面
async def get_user(user_id: int):
    return {"user_id": user_id}
```

> [!warning] **路由顺序很重要！** 如果 `{user_id}` 写在 `/me` 前面，`/me` 会被 `user_id="me"` 匹配到。

---

## 三、请求参数

### 查询参数（Query Parameters）

```python
from fastapi import FastAPI, Query

app = FastAPI()

# 基础查询参数（函数参数 = 查询参数）
@app.get("/items")
async def list_items(
    skip: int = 0,         # 有默认值 → 可选
    limit: int = 10,       # 有默认值 → 可选
    q: str | None = None,  # None → 可选参数
    active: bool = True,   # 布尔参数
):
    return {"skip": skip, "limit": limit, "q": q, "active": active}

# 必填查询参数（没有默认值）
@app.get("/items/search")
async def search_items(keyword: str):   # 没有默认值 → 必填
    return {"keyword": keyword}

# Query 高级校验 ⭐
@app.get("/products")
async def list_products(
    q: str | None = Query(
        default=None,
        min_length=3,
        max_length=50,
        pattern=r"^[a-zA-Z]+$",
        description="搜索关键词",
        deprecated=False,
    ),
    page: int = Query(default=1, ge=1, description="页码"),
    size: int = Query(default=20, ge=1, le=100, description="每页数量"),
    tags: list[str] = Query(default=[]),      # 多值参数: ?tags=a&tags=b
):
    return {"q": q, "page": page, "size": size, "tags": tags}

# 用 Pydantic 模型声明查询参数（FastAPI 0.115+）
from pydantic import BaseModel, Field

class FilterParams(BaseModel):
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []

@app.get("/items-v2/")
async def read_items(filter_query: Annotated[FilterParams, Query()]):
    return filter_query
```

### 请求体（Request Body）

```python
from fastapi import FastAPI, Body
from pydantic import BaseModel, Field

app = FastAPI()

class Item(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="商品名称")
    price: float = Field(..., gt=0, description="价格")
    description: str | None = Field(None, max_length=500)
    tags: list[str] = []

# 自动解析 JSON 请求体
@app.post("/items")
async def create_item(item: Item):
    return {"item": item, "price_with_tax": item.price * 1.1}

# 同时使用路径参数 + 查询参数 + 请求体
@app.put("/items/{item_id}")
async def update_item(
    item_id: int,                     # 路径参数
    item: Item,                       # 请求体 (JSON)
    q: str | None = None,             # 查询参数
    authorization: str | None = None, # 请求头（见下文）
):
    return {"item_id": item_id, **item.model_dump(), "q": q}

# 多个请求体参数
class User(BaseModel):
    username: str
    email: str

class Order(BaseModel):
    product: str
    quantity: int

@app.post("/purchase")
async def purchase(
    user: User,       # 第一个 Pydantic → 请求体
    order: Order,     # 第二个 Pydantic → 请求体（嵌套）
):
    return {"user": user, "order": order}

# 嵌入 Body（将单个字段包装在 JSON key 中）
@app.post("/items/embed")
async def create_item_with_embed(
    item: Item = Body(embed=True),  # 请求体: {"item": {...}}
): ...
# 无 embed: {"name": "...", "price": ...}
# 有 embed: {"item": {"name": "...", "price": ...}}
```

### 请求头（Header）

```python
from fastapi import FastAPI, Header

app = FastAPI()

@app.get("/protected")
async def protected_route(
    authorization: str = Header(..., description="Bearer token"),
    user_agent: str | None = Header(default=None),
    x_client_id: str | None = Header(default=None, alias="X-Client-ID"),
):
    return {"auth": authorization, "ua": user_agent}
```

### Cookie

```python
from fastapi import FastAPI, Cookie

app = FastAPI()

@app.get("/cart")
async def read_cart(
    session_id: str | None = Cookie(default=None),
):
    return {"session_id": session_id}
```

### 表单与文件上传

```python
from fastapi import FastAPI, Form, File, UploadFile

app = FastAPI()

# 表单数据（需安装 python-multipart）
@app.post("/login")
async def login(
    username: str = Form(...),       # Form() 而不是 Body()
    password: str = Form(...),
):
    return {"username": username}

# 文件上传 ⭐
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()                               # 读取全部
    # 或逐块读取大文件
    # while chunk := await file.read(1024):
    #     process(chunk)
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": len(content),
    }

# 多个文件
@app.post("/upload-multiple")
async def upload_multiple(files: list[UploadFile] = File(...)):
    return [{"filename": f.filename, "size": await f.seek(0, 2)} for f in files]

# 文件 + 表单混合
@app.post("/create-item")
async def create_item(
    name: str = Form(...),
    price: float = Form(...),
    image: UploadFile | None = File(default=None),
):
    return {"name": name, "price": price}
```

### 合并参数顺序规则

```python
# 如果参数名冲突，FastAPI 按以下规则推断来源：
# 1. 路径参数 → 路径中已声明
# 2. 查询参数 → 其他单一类型参数（int, str, bool 等）
# 3. 请求体 → Pydantic model

# ⭐ 也可以显式指定
from fastapi import Path, Query, Body

@app.put("/items/{item_id}")
async def update_item(
    item_id: int = Path(..., ge=1),           # 显式路径参数
    q: str | None = Query(default=None),       # 显式查询参数
    body: dict = Body(...),                     # 显式请求体
):
    return {"item_id": item_id, "q": q, "body": body}
```

> [!info] FastAPI 使用**声明式参数**风格，一个函数参数列表即可搞定路径参数、查询参数、请求体、请求头、Cookie、表单和文件，非常优雅。

---

## 四、响应模型

### response_model

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class ItemIn(BaseModel):
    name: str
    price: float
    description: str | None = None
    password: str           # 输入有 password

class ItemOut(BaseModel):
    name: str
    price: float
    description: str | None = None
    # 注意：没有 password 字段 → 自动过滤！

@app.post("/items", response_model=ItemOut)  # ⭐ 自动过滤输出
async def create_item(item: ItemIn):
    return item   # password 字段会被自动移除

# response_model_exclude_unset
@app.get("/items/{item_id}", response_model=ItemOut)
async def get_item(item_id: int):
    return {"name": "Foo", "price": 10.5}    # description=None 会被省略
    # 除非设置 response_model_exclude_unset=False
```

### 状态码

```python
from fastapi import FastAPI, status

app = FastAPI()

# 使用 HTTP 状态码常量（推荐）
@app.post("/items", status_code=status.HTTP_201_CREATED)
async def create_item():
    return {"message": "created"}

@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int):
    return None  # 204 响应不能有 body

# 动态状态码
from fastapi.responses import JSONResponse

@app.post("/items/custom")
async def custom_status():
    content = {"message": "处理中"}
    return JSONResponse(content=content, status_code=202)
```

### Response 类型

```python
from fastapi.responses import (
    JSONResponse,      # JSON（默认）
    HTMLResponse,      # HTML
    PlainTextResponse, # 纯文本
    FileResponse,      # 文件
    StreamingResponse, # 流式
    RedirectResponse,  # 重定向
)
from fastapi import FastAPI

app = FastAPI()

@app.get("/html")
async def get_html():
    html_content = """
    <h1>Hello, FastAPI!</h1>
    """
    return HTMLResponse(content=html_content)

@app.get("/download")
async def download_file():
    return FileResponse("path/to/file.pdf", filename="report.pdf")

@app.get("/redirect")
async def redirect():
    return RedirectResponse(url="/docs")

# 流式响应（大文件/SSE）
from fastapi.responses import StreamingResponse
import asyncio

async def generate_numbers():
    for i in range(10):
        yield f"data: {i}\n\n"
        await asyncio.sleep(0.5)

@app.get("/stream")
async def stream():
    return StreamingResponse(generate_numbers(), media_type="text/event-stream")
```

---

## 五、Pydantic 模型

### 基础模型

```python
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional
from decimal import Decimal

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    age: int = Field(ge=0, le=150, default=18)

class UserCreate(UserBase):             # 继承复用
    password: str = Field(..., min_length=6)

class UserResponse(UserBase):
    id: int
    created_at: datetime
    is_active: bool = True

    model_config = {"from_attributes": True}   # ⭐ ORM 模式（从 SQLAlchemy 等创建）
```

### Field 校验 ⭐

```python
from pydantic import BaseModel, Field
from typing import Annotated

class Product(BaseModel):
    # 基本校验
    name: str = Field(..., min_length=1, max_length=200, description="商品名称")

    # 数值限制
    price: float = Field(gt=0, le=999999.99)    # > 0, ≤ 999999.99
    quantity: int = Field(ge=0, default=0)       # ≥ 0

    # 默认值与别名
    category: str = Field(default="未分类", alias="category_name")

    # 正则校验
    sku: str = Field(pattern=r"^SKU-\d{6}$")     # 格式: SKU-123456

    # 列表约束
    tags: list[str] = Field(default=[], max_length=10)

product = Product(
    name="测试商品",
    price=99.9,
    sku="SKU-123456",
    category_name="电子产品",  # 用别名传入
)
print(product.model_dump(by_alias=True))  # 别名模式导出
```

### 嵌套模型

```python
from pydantic import BaseModel
from datetime import datetime

class Address(BaseModel):
    city: str
    street: str
    zip_code: str

class OrderItem(BaseModel):
    product_id: int
    quantity: int = 1

class Order(BaseModel):
    id: int
    user_id: int
    address: Address                      # 嵌套模型
    items: list[OrderItem]               # 模型列表
    created_at: datetime
    total: float | None = None

    model_config = {"from_attributes": True}

# 使用
order_data = {
    "id": 1,
    "user_id": 123,
    "address": {
        "city": "北京",
        "street": "长安街 1 号",
        "zip_code": "100000",
    },
    "items": [
        {"product_id": 1, "quantity": 2},
        {"product_id": 2, "quantity": 1},
    ],
    "created_at": "2025-01-15T14:30:00",
}

order = Order(**order_data)
print(order.model_dump_json(indent=2))  # 序列化为 JSON
```

### 高级配置

```python
from pydantic import BaseModel, ConfigDict

class Config(BaseModel):
    # Pydantic v2 配置语法
    model_config = ConfigDict(
        from_attributes=True,       # 支持从 ORM 对象创建
        populate_by_name=True,      # 允许用字段名或别名访问
        extra="forbid",             # 禁止额外字段（默认 ignore）
        frozen=True,                # 不可变（类似 dataclass frozen=True）
        str_strip_whitespace=True,  # 自动去除字符串首尾空格
        validate_default=True,      # 验证默认值
    )

    name: str
    value: int
```

###  validator（自定义校验）

```python
from pydantic import BaseModel, field_validator, model_validator

class OrderCreate(BaseModel):
    items: list[dict]
    coupon_code: str | None = None

    # ⭐ 字段级校验器
    @field_validator("coupon_code")
    @classmethod
    def validate_coupon(cls, v: str | None) -> str | None:
        if v and not v.startswith("COUPON-"):
            raise ValueError("优惠券格式错误，必须以 COUPON- 开头")
        return v.upper() if v else v

    # 模型级校验器（依赖多个字段）
    @model_validator(mode="after")
    def check_items_not_empty(self) -> "OrderCreate":
        if not self.items:
            raise ValueError("订单至少需要一个商品")
        return self
```

> [!tip] **Pydantic v1 vs v2**
> - FastAPI 已全面支持 Pydantic v2（推荐）
> - `model_dump()` 替代 v1 的 `dict()`
> - `model_dump_json()` 替代 `json()`
> - `from_attributes=True` 替代 `orm_mode=True`
> - `@field_validator` 替代 `@validator`
> - `ConfigDict` 替代 `class Config`

---

## 六、依赖注入

依赖注入（DI）是 FastAPI 最强大的特性之一，用于**解耦、复用、测试**。

### Depends（函数依赖）⭐

```python
from fastapi import FastAPI, Depends, Query

app = FastAPI()

# 定义依赖（就是一个普通函数）
async def pagination(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
):
    return {"skip": skip, "limit": limit}

# 注入依赖
@app.get("/items")
async def list_items(page: dict = Depends(pagination)):  # Depends 注入
    skip, limit = page["skip"], page["limit"]
    return {"skip": skip, "limit": limit}

# 更简洁的写法：直接解包
@app.get("/users")
async def list_users(params: dict = Depends(pagination)):
    return params
```

### 可复用依赖（类）⭐

```python
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# 数据库会话依赖
async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 认证依赖
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    user = verify_token(token, db)    # 解析 JWT
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的认证凭据",
        )
    return user

# 权限依赖
def require_admin(user: User = Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="需要管理员权限")
    return user

# 路由中使用
@app.get("/me")
async def read_me(user: User = Depends(get_current_user)):
    return user

@app.get("/admin/dashboard")
async def dashboard(admin: User = Depends(require_admin)):
    return {"message": f"欢迎管理员 {admin.username}"}

# 多个依赖
@app.get("/protected-items")
async def protected_items(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    pagination: dict = Depends(pagination),
):
    items = db.query(Item).offset(pagination["skip"]).limit(pagination["limit"]).all()
    return items
```

### 依赖的作用域

```python
from fastapi import FastAPI, Depends

app = FastAPI()

# 依赖可以返回任何值（不仅是函数）
# 依赖可以依赖其他依赖（链式注入）
# 每个请求独立计算一次依赖（即使被多个路由使用）

# 缓存：默认 Depends 在每个请求中只调用一次
async def common_params(q: str | None = None):
    return {"q": q}

@app.get("/items")
async def items(params: dict = Depends(common_params)):
    return params

@app.get("/users")
async def users(params: dict = Depends(common_params)):  # 同一个依赖被复用
    return params
# common_params 在每个请求中只执行一次
```

### 用 `yield` 管理资源

```python
from fastapi import FastAPI, Depends

app = FastAPI()

# yield 之前的代码在请求开始前执行
# yield 之后的代码在请求结束后执行（即使是异常也会执行）
async def get_db():
    db = SessionLocal()
    try:
        yield db              # 注入给路由
    finally:
        db.close()            # 请求结束后自动关闭

@app.get("/users/{user_id}")
async def get_user(user_id: int, db: Session = Depends(get_db)):
    return db.query(User).filter(User.id == user_id).first()
```

> [!info] **依赖注入的优势**
> - **解耦**：认证、数据库、分页等逻辑可以独立维护
> - **复用**：同一依赖可在多个路由中共享
> - **测试**：可以轻松 Mock 依赖进行单元测试
> - **缓存**：同一依赖在同一请求中只计算一次

---

## 七、中间件与 CORS

### 自定义中间件

```python
from fastapi import FastAPI, Request
import time

app = FastAPI()

# 基础中间件
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()

    response = await call_next(request)       # 执行请求

    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

# 日志中间件
@app.middleware("http")
async def log_requests(request: Request, call_next):
    print(f"→ {request.method} {request.url.path}")
    response = await call_next(request)
    print(f"← {response.status_code}")
    return response
```

### CORS（跨域）⭐

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[                          # 允许的源
        "http://localhost:3000",
        "https://myfrontend.com",
    ],
    allow_origin_regex=r"https://.*\.example\.com",  # 或正则
    allow_credentials=True,                   # 允许 Cookie
    allow_methods=["*"],                      # 允许的方法
    allow_headers=["*"],                      # 允许的请求头
)

# 开发阶段（放开所有限制）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],                     # ⚠️ 生产环境不要用 *
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 信任代理（Nginx 反向代理时）

```python
from fastapi import FastAPI
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware

app = FastAPI()

# 当 Nginx 等反向代理在前端时
# 确保获取真实的客户端 IP 和协议
```

---

## 八、异常处理

### HTTPException

```python
from fastapi import FastAPI, HTTPException, status

app = FastAPI()

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    if user_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户 ID 必须为正数",
        )

    if user_id > 1000:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"用户 {user_id} 不存在",
            headers={"X-Error": "User not found"},  # 自定义响应头
        )

    return {"user_id": user_id, "name": "Alice"}
```

### 自定义异常处理器

```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

# 自定义异常类
class InsufficientBalanceError(Exception):
    def __init__(self, balance: float, amount: float):
        self.balance = balance
        self.amount = amount

# 注册异常处理器
@app.exception_handler(InsufficientBalanceError)
async def insufficient_balance_handler(request: Request, exc: InsufficientBalanceError):
    return JSONResponse(
        status_code=402,
        content={
            "message": "余额不足",
            "balance": exc.balance,
            "required": exc.amount - exc.balance,
            "code": "INSUFFICIENT_BALANCE",
        },
    )

@app.get("/pay")
async def pay(balance: float, amount: float):
    if balance < amount:
        raise InsufficientBalanceError(balance=balance, amount=amount)
    return {"message": "支付成功"}

# 重写默认的 HTTPException 处理器
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

@app.exception_handler(StarletteHTTPException)
async def custom_http_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "code": "HTTP_ERROR",
            "message": exc.detail,
            "path": request.url.path,
        },
    )

# 重写请求参数校验错误处理器
@app.exception_handler(RequestValidationError)
async def validation_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "code": "VALIDATION_ERROR",
            "message": "请求参数校验失败",
            "errors": exc.errors(),   # 详细的错误字段信息
        },
    )
```

---

## 九、安全与认证

### OAuth2 密码流 + JWT ⭐

```python
from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

# ============ 配置 ============
SECRET_KEY = "your-secret-key-here-change-in-production"  # ⚠️ 生产环境用环境变量
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# ============ 模型 ============
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: str | None = None

class User(BaseModel):
    username: str
    email: str | None = None
    disabled: bool | None = None

class UserInDB(User):
    hashed_password: str

# ============ 工具 ============
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

app = FastAPI()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# ============ 模拟数据库 ============
fake_users_db = {
    "alice": {
        "username": "alice",
        "email": "alice@example.com",
        "hashed_password": get_password_hash("secret123"),
        "disabled": False,
    },
}

# ============ 依赖 ============
def get_user(db, username: str) -> UserInDB | None:
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
    return None

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    """验证 JWT token 并返回当前用户"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
) -> User:
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="用户已禁用")
    return current_user

# ============ 路由 ============
@app.post("/auth/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    """登录获取 JWT token"""
    user = get_user(fake_users_db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return Token(access_token=access_token)

@app.get("/users/me", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    """获取当前用户信息"""
    return current_user
```

### HTTP Basic Auth

```python
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

app = FastAPI()
security = HTTPBasic()

@app.get("/basic-auth")
async def basic_auth(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    # 防止时序攻击
    is_correct_username = secrets.compare_digest(credentials.username, "admin")
    is_correct_password = secrets.compare_digest(credentials.password, "admin123")

    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
        )
    return {"username": credentials.username}
```

> [!tip] **JWT 认证完整流程**
> 1. 用户 POST `/auth/token` 提交用户名密码 → 返回 `access_token`
> 2. 客户端在请求头加 `Authorization: Bearer <token>`
> 3. 路由通过 `Depends(get_current_active_user)` 自动验证
> 4. 验证通过 → 正常返回；验证失败 → 401

---

## 十、数据库操作

### SQLAlchemy 集成 ⭐

```python
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker, relationship
from datetime import datetime, timezone

# ============ 数据库配置 ============
SQLALCHEMY_DATABASE_URL = "sqlite:///./data.db"
# PostgreSQL: "postgresql://user:pass@localhost/dbname"
# MySQL:      "mysql+asyncmy://user:pass@localhost/dbname"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ============ ORM 模型 ============
class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    is_active = Column(Integer, default=1)

    items = relationship("Item", back_populates="owner")  # 关联

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(String(500))
    price = Column(Float, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    owner = relationship("User", back_populates="items")

# 创建表
Base.metadata.create_all(bind=engine)
```

### CRUD 操作

```python
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel

app = FastAPI()

# 依赖：获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ============ Pydantic Schema ============
class ItemCreate(BaseModel):
    title: str
    description: str | None = None
    price: float

class ItemResponse(ItemCreate):
    id: int
    owner_id: int

    model_config = {"from_attributes": True}

# ============ CRUD 路由 ============
@app.post("/items", response_model=ItemResponse, status_code=201)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    """创建商品"""
    db_item = Item(**item.model_dump(), owner_id=1)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.get("/items", response_model=list[ItemResponse])
def list_items(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    """分页查询商品列表"""
    return db.query(Item).offset(skip).limit(limit).all()

@app.get("/items/{item_id}", response_model=ItemResponse)
def get_item(item_id: int, db: Session = Depends(get_db)):
    """查询单个商品"""
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="商品不存在")
    return item

@app.put("/items/{item_id}", response_model=ItemResponse)
def update_item(
    item_id: int,
    item_data: ItemCreate,
    db: Session = Depends(get_db),
):
    """更新商品"""
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="商品不存在")

    for key, value in item_data.model_dump().items():
        setattr(item, key, value)

    db.commit()
    db.refresh(item)
    return item

@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    """删除商品"""
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="商品不存在")
    db.delete(item)
    db.commit()
    return None
```

### 异步数据库

```python
# 使用 async SQLAlchemy + async driver
# pip install sqlalchemy asyncmy

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

ASYNC_DATABASE_URL = "mysql+asyncmy://user:pass@localhost/dbname"
async_engine = create_async_engine(ASYNC_DATABASE_URL)
AsyncSessionLocal = async_sessionmaker(async_engine, class_=AsyncSession)

async def get_async_db():
    async with AsyncSessionLocal() as db:
        yield db

# 路由中使用
@app.get("/async-items")
async def get_async_items(db: AsyncSession = Depends(get_async_db)):
    result = await db.execute(select(Item))
    return result.scalars().all()
```

> [!tip] **同步 vs 异步数据库**
> - 同步 SQLAlchemy：简单、稳定，配合多线程（uvicorn workers）足够
> - 异步 SQLAlchemy：适合高并发 IO 场景，但代码更复杂
> - **小项目用同步即可**，FastAPI 的异步路由也可以调用同步 DB（FastAPI 会自动在线程池中执行）

---

## 十一、APIRouter 与项目结构

### 大型项目组织

```
project/
├── app/
│   ├── __init__.py
│   ├── main.py               # 应用入口
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py          # 配置（settings）
│   │   ├── security.py        # 认证/密码工具
│   │   └── database.py        # 数据库引擎/会话
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py            # SQLAlchemy ORM 模型
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── user.py            # Pydantic Schema
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── users.py           # 用户相关路由
│   │   └── items.py           # 商品相关路由
│   ├── services/
│   │   ├── __init__.py
│   │   └── user_service.py    # 业务逻辑层
│   └── utils/
│       ├── __init__.py
│       └── helpers.py         # 工具函数
├── tests/
│   ├── __init__.py
│   ├── conftest.py            # pytest 共享 fixture
│   └── test_users.py
├── requirements.txt
└── .env
```

### APIRouter 使用 ⭐

```python
# app/routers/users.py
from fastapi import APIRouter, Depends, HTTPException
from app.core.database import get_db
from app.schemas.user import UserCreate, UserResponse
from app.services import user_service
from app.core.security import get_current_user

router = APIRouter(
    prefix="/users",             # ⭐ 统一前缀
    tags=["用户管理"],            # ⭐ OpenAPI 标签分组
    responses={404: {"description": "用户不存在"}},
)

@router.get("/", response_model=list[UserResponse])
async def list_users(db=Depends(get_db)):
    return user_service.get_all(db)

@router.post("/", response_model=UserResponse, status_code=201)
async def create_user(user: UserCreate, db=Depends(get_db)):
    return user_service.create(db, user)

@router.get("/me", response_model=UserResponse)
async def get_me(current_user=Depends(get_current_user)):
    """获取当前用户信息"""
    return current_user

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db=Depends(get_db)):
    user = user_service.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user
```

```python
# app/routers/items.py
from fastapi import APIRouter

router = APIRouter(
    prefix="/items",
    tags=["商品管理"],
)

@router.get("/")
async def list_items():
    pass

@router.post("/")
async def create_item():
    pass
```

```python
# app/main.py — 注册所有路由
from fastapi import FastAPI
from app.routers import users, items

app = FastAPI(title="My API", version="1.0.0")

# 注册路由
app.include_router(users.router)
app.include_router(items.router)

# 或给路由再加一层前缀
# app.include_router(users.router, prefix="/api/v1")
```

### 配置管理

```python
# app/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # ⭐ 从环境变量或 .env 文件读取
    app_name: str = "My API"
    debug: bool = False

    database_url: str = "sqlite:///./data.db"
    secret_key: str = "change-me"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # 允许跨域的源
    cors_origins: list[str] = ["http://localhost:3000"]

    class Config:
        env_file = ".env"         # 从 .env 文件加载
        env_file_encoding = "utf-8"

settings = Settings()
```

```python
# 在 main.py 中使用
from app.core.config import settings

app = FastAPI(title=settings.app_name, debug=settings.debug)
```

> [!tip] **项目结构原则**
> - `routers/`：只管路由定义（URL 映射）
> - `services/`：业务逻辑（可测试）
> - `schemas/`：Pydantic 模型（请求/响应定义）
> - `models/`：ORM 模型（数据库表映射）
> - 不要直接在路由函数里写数据库操作——抽到 service 层

---

## 十二、后台任务与生命周期

### BackgroundTasks

```python
from fastapi import FastAPI, BackgroundTasks

app = FastAPI()

# 后台任务函数
def write_log(message: str):
    with open("app.log", "a") as f:
        f.write(f"{message}\n")

def send_email(to: str, subject: str, body: str):
    # 模拟发送邮件
    import time
    time.sleep(5)
    print(f"邮件已发送到 {to}: {subject}")

@app.post("/register")
async def register(username: str, background_tasks: BackgroundTasks):
    # 立即返回响应
    background_tasks.add_task(write_log, f"用户 {username} 注册成功")
    background_tasks.add_task(send_email, f"{username}@example.com", "欢迎", "...")

    return {"message": "注册成功，邮件将在后台发送"}

# 后台任务中还可以引用依赖
from fastapi import Depends

def email_report(db: Session = Depends(get_db)):
    users = db.query(User).all()
    # 发邮件...

@app.post("/reports")
async def trigger_report(background_tasks: BackgroundTasks):
    background_tasks.add_task(email_report)  # 依赖会在后台任务中解析
    return {"message": "报表生成中"}
```

> [!warning] `BackgroundTasks` 适合轻量任务，**重任务用 Celery**。

### 生命周期事件（lifespan）⭐

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI

# ⭐ FastAPI 推荐用法（替代废弃的 on_event）
@asynccontextmanager
async def lifespan(app: FastAPI):
    # ──────── 启动时执行 ────────
    print("应用启动...")
    app.state.db_engine = create_engine(DATABASE_URL)   # 初始化数据库
    app.state.redis_client = await redis.connect()      # 连接 Redis
    print("应用已就绪")

    yield   # ← 应用在此运行

    # ──────── 关闭时执行 ────────
    print("应用关闭中...")
    app.state.db_engine.dispose()                       # 关闭数据库
    await app.state.redis_client.close()                # 关闭 Redis
    print("应用已关闭")

app = FastAPI(lifespan=lifespan)

# 在路由中访问
@app.get("/health")
async def health(request: Request):
    return {
        "status": "ok",
        "db": request.app.state.db_engine is not None,
    }
```

---

## 十三、WebSocket

### 基本使用

```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()               # 接受连接
    try:
        while True:
            data = await websocket.receive_text()   # 接收消息
            await websocket.send_text(f"回声: {data}")  # 发送消息
    except WebSocketDisconnect:
        print("客户端断开连接")
```

### 连接管理器

```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()

class ConnectionManager:
    """管理多个 WebSocket 连接"""
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        """广播消息给所有客户端"""
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception:
                self.disconnect(connection)

manager = ConnectionManager()

@app.websocket("/ws/chat")
async def chat(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"用户说: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast("有用户离开了聊天室")
```

---

## 十四、测试

### TestClient

```python
from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

@app.get("/")
async def read_root():
    return {"hello": "world"}

# ⭐ pytest 测试
from fastapi.testclient import TestClient

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"hello": "world"}

# 测试 POST
def test_create_item():
    response = client.post(
        "/items",
        json={"name": "Foo", "price": 10.5},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Foo"

# 测试认证
def test_auth():
    response = client.post(
        "/auth/token",
        data={"username": "alice", "password": "secret123"},  # 表单格式
    )
    assert response.status_code == 200
    token = response.json()["access_token"]

    # 使用 token 访问受保护路由
    response = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200

# 测试文件上传
def test_upload():
    response = client.post(
        "/upload",
        files={"file": ("test.txt", b"Hello, World!", "text/plain")},
    )
    assert response.status_code == 200
```

### conftest.py（共享 fixture）

```python
# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.core.database import Base, get_db

# 测试用内存数据库
TEST_DATABASE_URL = "sqlite:///./test.db"
test_engine = create_engine(TEST_DATABASE_URL)
TestSessionLocal = sessionmaker(bind=test_engine)

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)

@pytest.fixture
def db_session():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client(db_session):
    """用测试数据库覆盖依赖"""
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()   # 清理覆盖

# 测试中使用
def test_list_items(client: TestClient):
    response = client.get("/items")
    assert response.status_code == 200
```

> [!info] **`app.dependency_overrides`** 是 FastAPI 测试的秘密武器：无需修改源代码，直接替换任何依赖，非常适合测试 Mock。

---

## 十五、部署

### Uvicorn 生产配置

```bash
# 基础运行
uvicorn app.main:app --host 0.0.0.0 --port 8000

# 生产运行（多 workers）
uvicorn app.main:app \
  --host 0.0.0.0 \
  --port 8000 \
  --workers 4 \               # worker 进程数（通常 = CPU 核心数）
  --loop uvloop \             # 性能更好（Linux）
  --http httptools            # 性能更好
```

### Gunicorn + Uvicorn（推荐）

```bash
# 安装
pip install gunicorn uvicorn[standard]

# 启动（gunicorn 管理 worker 进程，uvicorn 处理 ASGI）
gunicorn app.main:app \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --workers 4 \
  --timeout 120 \
  --access-logfile - \
  --error-logfile -
```

### Docker 部署 ⭐

```dockerfile
# Dockerfile
FROM python:3.12-slim

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制代码
COPY . .

# 暴露端口
EXPOSE 8000

# 启动
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```yaml
# docker-compose.yml
version: "3.8"

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/mydb
      - SECRET_KEY=${SECRET_KEY}
    depends_on:
      - db
    restart: unless-stopped

  db:
    image: postgres:16
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=mydb
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

volumes:
  postgres_data:
```

### 环境变量管理

```bash
# .env 文件（不要提交到 git！）
DATABASE_URL=postgresql://user:pass@localhost:5432/mydb
SECRET_KEY=your-256-bit-secret
DEBUG=false
CORS_ORIGINS=["https://myapp.com"]
```

```python
# app/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    debug: bool = False
    cors_origins: list[str] = ["http://localhost:3000"]

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}

settings = Settings()  # 自动从环境变量或 .env 加载
```

### 生产检查清单

| 项目 | 检查 |
|:----:|------|
| **SECRET_KEY** | 使用强随机密钥，从环境变量读取 |
| **CORS** | 生产环境限制 `allow_origins` |
| **HTTPS** | 用 Nginx/Traefik 做 TLS 终止 |
| **数据库** | 使用连接池，设置连接数上限 |
| **日志** | 用 logging 替代 print，结构化日志 |
| **限流** | 使用 slowapi 或网关限流 |
| **健康检查** | 暴露 `/health` 端点给负载均衡器 |
| **文档** | 生产环境关闭 `/docs`（debug=False） |
| **Graceful Shutdown** | 使用 lifespan 正确处理关闭 |

> [!tip] **快速上手总结**
>
> ```
> 1. 安装：pip install fastapi uvicorn
> 2. 写一个 main.py（Hello World）
> 3. 运行：uvicorn main:app --reload
> 4. 访问 /docs 看 API 文档
> 5. 加 Pydantic 模型 → 自动校验
> 6. 加 Depends → 依赖注入
> 7. 加 router → 分模块
> 8. 加数据库 → CRUD
> 9. 加认证 → JWT
> 10. 部署 → Docker + Gunicorn
> ```
>
> 上一篇：[[Python基础与进阶篇]]
> 下一篇推荐：[[python学习篇/面向对象与设计模式篇|面向对象与设计模式篇]]
