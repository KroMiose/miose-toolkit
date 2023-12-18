# Miose Toolkit 工具箱: Common 子项目

## 介绍

Common 子项目包含了 Miose Toolkit 中所有子项目都会用到的公共代码和一些只依赖于一些通用库的常用工具。

## 测试用例库 -> [用例库](./src/tests)

测试用例库中包含了所有模块的测试用例，可以参考其中的代码来使用模块。

## 功能列表

### 1. 配置文件工具 [测试用例](./src/tests/test_config.py)

配置文件工具可以帮助你快速 读取/导出 yaml 配置文件中的配置项，并支持类型注解。基本使用如下:

```python
from miose_toolkit_common import Config, Env

# 定义配置模板
class MyConfigTemplate(Config):
    MYSQL_HOST: str = "localhost"
    MYSQL_PORT: int = 3306

# 加载配置
config = MyConfigTemplate.load_config()

# 使用配置
print(config.MYSQL_HOST)

# 导出当前配置
config.dump_config()

# 导出多个环境配置
config.dump_env_config(envs=[Env.Dev.value, Env.Prod.value])

# 重载配置
config.reload_config()

# 生成配置结构
print(config.gen_config_schema())
```

指定环境: 在运行项目时，可以通过运行参数 `env=xxx` 来指定环境，例如：`python main.py env=dev`，如果不指定环境，则默认为 `dev` 环境。

### 2. 指令解析工具 [测试用例](./src/tests/test_command.py)

指令解析工具可以帮助你快速构建自定义指令，支持指令 参数/选项 解析，基本使用如下:

```python
from miose_toolkit_common import CmdOpt, CommandMaster

cm = CommandMaster()  # 创建指令解析器

# 注册指令选项
opt_page: CmdOpt = cm.reg_option(
    full_name="page", # 选项全名
    short_name="p", # 选项简写名
    info="Page number", # 选项描述
    Type=int, # 选项类型
    default=1,  # 选项默认值
)

# 注册指令
@cm.reg_command(route="help", info="Show help info.", options=["page"])
def _(_options, command_name: str = "help"):
    # ...  # 执行指令实现
    return # 返回指令执行结果

# 执行指令
cm.exec(command_text="help test -p 1")

# 生成指令帮助信息
print(cm.gen_desc())

# 生成指令简短帮助信息
print(cm.gen_short_desc())
```

### 3. 重试工具

重试工具可以帮助你快速构建重试逻辑，只需要在需要重试的函数上添加装饰器即可，基本使用如下:

```python
from miose_toolkit_common import retry, async_retry

# 同步重试
@retry(retry_times=3, delay=1, ignore_exception=False)
def your_func():
    # ...  # 执行函数实现
    return # 返回函数执行结果

# 异步重试
@async_retry(retry_times=3, delay=1, ignore_exception=False)
async def your_func():
    # ...  # 执行函数实现
    return # 返回函数执行结果
```

其中 `ignore_exception` 参数用于控制是否忽略异常，如果设置为 `True`，则会在重试次数用尽后抛出最后一次异常，否则会直接忽略重试过程中的所有异常。

### 4. 简易 同步/异步 请求工具

请求工具可以帮助你快速构建发起 同步/异步 HTTP 请求，基本使用如下:

```python
from miose_toolkit_common import Mfetch

# 同步请求
res = Mfetch.fetch(
    url="https://www.baidu.com", # 请求地址
    method="get", # 请求方法
    params={}, # 请求参数
    data={}, # 请求数据
    headers={}, # 请求头
    proxy_server="", # 代理服务器地址，例如：http://127.0.0.1:7890
    timeout=10, # 请求超时时间
)

# 异步请求
res = await Mfetch.async_fetch(
    url="https://www.baidu.com", # 请求地址
    method="get", # 请求方法
    params={}, # 请求参数
    data={}, # 请求数据
    headers={}, # 请求头
    proxy_server="", # 代理服务器地址，例如：http://
```

### 5. 字典操作

一些常用的字典操作，例如：字典合并等

```python
from miose_toolkit_common import MDict

# 字典合并
dict1 = {"a": 1}
dict2 = {"b": 2}
dict3 = MDict.merge_dicts(dict1, dict2) # 后面的字典会覆盖前面的字典
```

### 6. Url 操作

一些常用的 Url 操作，例如：获取 Url 参数等

```python
from miose_toolkit_common import MUrl

# 获取 Url 参数
params = MUrl.get_url_params("http://example.com?a=1&b=2")

# 获取 Url 域名
domain = MUrl.get_url_domain("http://example.com")

# 获取 Url 路径
path = MUrl.get_url_path("http://example.com/path/to")

# 去除 Url 锚点
url = MUrl.drop_url_anchor("http://example.com#anchor")

# 判断 Url 是否为相对路径
is_relative_url = MUrl.is_relative_url("/path/to")
```
