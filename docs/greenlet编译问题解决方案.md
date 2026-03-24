# 解决 pip install sqlalchemy 时 greenlet 编译失败的问题

## 问题描述

在执行 `pip install sqlalchemy` 时，安装过程因 greenlet 包编译失败而中断，错误信息如下：

```text
Building wheel for greenlet (pyproject.toml) ... error
...
error: Unable to find a compatible Visual Studio installation.
```

## 原因分析

sqlalchemy 依赖 greenlet，而 greenlet 包含 C 扩展代码。

当使用 pip 从 PyPI 安装时，如果找不到对应平台的预编译 wheel（或 pip 被配置为强制从源码构建），pip 会尝试在本地编译该扩展。

编译需要 Windows 平台上的 Visual C++ 编译器（Visual Studio 工具链），而你的系统中缺少这一组件，导致编译失败。

## 解决方案

### 推荐：使用 Conda 安装（无需编译器）

由于你正在使用 Miniforge3（或 Anaconda）的 Conda 环境，可以直接利用 Conda 的预编译二进制包，完全避免本地编译：

```bash
conda install sqlalchemy
```

Conda 会自动从 Anaconda 仓库下载适合你系统和 Python 版本的 sqlalchemy 及依赖（包括预编译好的 greenlet），安装过程快速且无编译错误。

### 备选：安装 Visual C++ 编译器（继续使用 pip）

如果你坚持使用 pip，需要安装 Windows 上的 C++ 编译工具：

1. 下载并安装 [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)（免费）。
2. 安装时，在 **工作负载** 选项卡中勾选 **C++ 桌面开发**，确保包含 Windows 10/11 SDK 和 MSVC v142 工具集。
3. 安装完成后，重启终端（或重启电脑），然后重新运行：

```bash
pip install sqlalchemy
```

## 验证安装

无论使用哪种方式，安装成功后，可以通过以下命令验证：

```bash
# 检查已安装的包
conda list sqlalchemy   # 如果用 conda 安装
pip show sqlalchemy     # 如果用 pip 安装
```

或者在 Python 中测试导入：

```python
import sqlalchemy
print(sqlalchemy.__version__)
```

若无错误输出，说明安装成功。
