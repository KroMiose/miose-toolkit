# Miose Toolkit 工具箱

## 介绍

Miose Toolkit 是一个基于 Python 的个人工具箱，收集了一些个人常用的小工具，方便快速开发。为了提高工具库可用性，大部分工具都包含了自动化测试用例，包含 Windows, Linux, MacOS 的多平台一致性测试。

## 工具列表

- [common](./common/README.md) - 通用工具集
- [db](./db/README.md) - 数据库工具集 (支持 MySQL, PostgreSQL, SQLite)
- [logger](./logger/README.md) - 日志工具 (一个基于 loguru 的日志工具)

## 安装 (以 logger 为例)

```bash
pip install miose-toolkit-logger  # 安装日志工具
```

## 使用

```python
from miose_toolkit_logger import logger

logger.info('Hello Miose Toolkit !')
```

## 开发指南

如果你想为 Miose Toolkit 贡献代码，可以参考以下步骤：

### 1. 克隆代码

```bash
git clone https://github.com/KroMiose/miose-toolkit.git
```

### 2. 安装开发环境依赖

```bash
poetry install --dev
```

### 3. 安装子项目依赖

```bash
poetry run install  # 安装所有子项目依赖
poetry run install common  # 安装 common 子项目依赖
```

### 4. 运行测试

```bash
poetry run test # 运行所有测试
poetry run test common # 运行 common 子项目测试
```

### 5. 调试代码 (推荐使用 VSCode)

项目中包含了 VSCode 的调试配置，可以直接使用 VSCode 选择对应的包以调试模式运行测试用例。

### 6. 清理环境

如果你在开发过程中遇到了问题，例如依赖包冲突等，可以尝试清理环境后重新安装依赖。

```bash
poetry run clean # 清理所有子项目环境
poetry run clean common # 清理 common 子项目环境
```

如果运行以上代码时因为权限问题导致失败，可以尝试直接到对应子项目目录下删除 `.venv` 文件夹。

## 🤝 贡献列表

感谢以下开发者对本项目做出的贡献

<a href="https://github.com/KroMiose/miose-toolkit/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=KroMiose/miose-toolkit&max=1000" />
</a>
