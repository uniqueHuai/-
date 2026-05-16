分布式基础内容大纲：

![](https://cdn.nlark.com/yuque/0/2025/png/52814014/1752828439300-29cbe7a1-91ab-432c-992d-65624460ef37.png)

---

Nacos

Nacos注册中心：

服务注册：微服务启动时将自己的网络地址、元数据等信息注册到Nacos

![](https://cdn.nlark.com/yuque/0/2025/png/52814014/1752828599216-4567caac-ebd0-4a9e-b6bd-d5fb2af07b6d.png)

服务发现：服务消费者能够查询和发现可用的服务实例（返回访问的地址）

使用方法在springboot启动类上面加上@EnableDiscoveryClient注解

![](https://cdn.nlark.com/yuque/0/2025/png/52814014/1752828879314-3473cc51-da17-452d-b642-7c0973e55c09.png)

远程调用（编程式）：

基础实现：使用RestTemplate实例（springboot-web-start依赖），配合服务发现中的访问地址，发送请求，返回数据。

负载均衡实现：

步骤四是另一种方法，在RestTemplate的bean对象下使用@LoadBalanced注解，对用访问url地址写为对方微服务名字。

![](https://cdn.nlark.com/yuque/0/2025/png/52814014/1752830837408-34f7a6c2-bce9-48b7-8695-5333c6284c6d.png)

Nacos注册中心注意点，当Nacos宕机时：

![](https://cdn.nlark.com/yuque/0/2025/png/52814014/1752831559756-71f11aa9-aec9-4260-ab8b-d58e817ef3e7.png)

---

Nacos配置中心：

动态更新项目里面的配置信息：

![](https://cdn.nlark.com/yuque/0/2025/png/52814014/1752832464890-799625c7-237a-4353-9d00-a1ccdf8f2364.png)

三种方式（推荐二）

![](https://cdn.nlark.com/yuque/0/2025/png/52814014/1752832505173-12dfe20d-5fd3-4533-a149-9df3ad02fa37.png)

数据隔离（不同环境使用不同的配置文件）：

使用到Nacos中的名称空间

![](https://cdn.nlark.com/yuque/0/2025/png/52814014/1752833444432-1dc8e9ea-254c-44b6-95ae-1faf390fa844.png)

Nacos小结：

![](https://cdn.nlark.com/yuque/0/2025/png/52814014/1752833521074-6a92b17c-a718-4f36-9e42-89655fe9c820.png)

---

OpenFeign

远程调用（声明式）：

![](https://cdn.nlark.com/yuque/0/2025/png/52814014/1752890960509-b3cd8609-5307-41a8-ab0e-c2a5768da6d3.png)

![](https://cdn.nlark.com/yuque/0/2025/png/52814014/1752891026456-ade08a99-b886-438e-9a93-65f9af1b01a2.png)

进阶配置：

配置日志

![](https://cdn.nlark.com/yuque/0/2025/png/52814014/1752892027261-cfff101d-6cfb-4377-a619-00b037bffbe8.png)

超时控制

默认下

![](https://cdn.nlark.com/yuque/0/2025/png/52814014/1752892254227-328a581e-d7b6-4228-93ab-65feeb4c9043.png)

精确设置在配置文件里面进行配置信息

重试机制

默认不开启，两种方法开启（配置文件和bean重试器）

![](https://cdn.nlark.com/yuque/0/2025/png/52814014/1752892647415-17df755f-0bd5-406b-99cf-2f9065a4c8b1.png)

拦截器

请求拦截器和响应拦截器，两种方法（配置文件和拦截器类，bean拦截器类）

兜底返回Fallback

编写兜底返回bean，继承ProductFeignClient

总结

![](https://cdn.nlark.com/yuque/0/2025/png/52814014/1752893470698-09cc9766-cd41-4b44-88ab-bdcbece7d721.png)

---

Sentinel（用户访问资源的规则）

异常处理

使用：引入依赖，配置Sentinel地址信息，再进入控制台即可

异常处理：

继承BlockException，编写异常处理

![](https://cdn.nlark.com/yuque/0/2025/png/52814014/1752941580580-efc3ca4d-92e2-456a-933d-63aa77918f91.png)

流控规则（限制多于请求，保护资源不被耗尽，防止雪崩）

![](https://cdn.nlark.com/yuque/0/2025/png/52814014/1752982391838-cbc4d9b9-789b-443b-9423-edc1e72095e1.png)![](https://cdn.nlark.com/yuque/0/2025/png/52814014/1752982402749-195b770b-0eea-4dce-92b1-40b995751da3.png)

熔断降级规则

开启熔断规则后，当请求错误到达一定次数，将会自动fallback（兜底数据），在设置的一定时间内不会再请求B。

![](https://cdn.nlark.com/yuque/0/2025/png/52814014/1753069428814-b8046434-347b-4a71-8a17-7887e23dea98.png)

---

Gateway（转发前端请求路由）

使用引入依赖，配置信息

![](https://cdn.nlark.com/yuque/0/2025/png/52814014/1753089362343-6eda5a72-7841-4a84-a2f2-129be11a529f.png)

URI目的地

Predicate断言

![](https://cdn.nlark.com/yuque/0/2025/png/52814014/1753089495143-abb654f5-d596-46da-8931-008538331190.png)

Filter过滤器

![](https://cdn.nlark.com/yuque/0/2025/png/52814014/1753089509979-991b3e79-9552-4bae-beb8-f19716278dbc.png)

---

Seata（解决分布式事务问题）

使用引入依赖，编写file.conf配置文件

原理

![](https://cdn.nlark.com/yuque/0/2025/png/52814014/1753089790964-e2c3f67b-bd03-4cc3-88b0-a587e51476a0.png)

二阶提交协议和undo_log

![](https://cdn.nlark.com/yuque/0/2025/png/52814014/1753089804716-725ed0fd-891e-41d6-aa48-820c64059a6b.png)