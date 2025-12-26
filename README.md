# OpenAI Agent Notes

这个仓库包含了使用 OpenAI Agents SDK 的学习笔记和示例代码。

## 📁 项目结构

```
.
├── notebooks/              # Jupyter Notebook 示例文件
│   ├── basicCommuation.ipynb          # 基础通信示例
│   ├── functionTool.ipynb             # 函数工具示例
│   ├── handOff.ipynb                  # 代理交接示例
│   ├── openai-agent-use-examples.ipynb # OpenAI Agent 使用示例集合
│   └── sourceCommunication.ipynb     # 源通信示例
├── requirements.txt       # Python 依赖包列表
├── check_env.py          # 环境配置检测脚本
├── venv/                  # Python 虚拟环境
└── README.md              # 项目说明文档
```

## 🚀 快速开始

### 1. 环境要求

- Python 3.9+
- pip

### 2. 创建虚拟环境

如果还没有虚拟环境，需要先创建一个：

```bash
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
# macOS/Linux:
source venv/bin/activate

# Windows:
# venv\Scripts\activate
```

激活成功后，命令行提示符前会显示 `(venv)`。

### 3. 安装依赖

```bash
# 确保虚拟环境已激活
# 安装依赖包
pip install -r requirements.txt
```

### 4. 配置 API Key

#### 创建 .env 文件

在项目根目录下创建 `.env` 文件（注意文件名以点开头）：

**方法一：使用命令行创建**

```bash
# macOS/Linux
echo "OPENAI_API_KEY=your_api_key_here" > .env

# Windows (PowerShell)
echo "OPENAI_API_KEY=your_api_key_here" | Out-File -Encoding utf8 .env
```

**方法二：手动创建**

1. 在项目根目录创建一个新文件，命名为 `.env`（注意文件名以点开头）
2. 在文件中添加以下内容：

```bash
OPENAI_API_KEY=your_api_key_here
```

**重要提示：**
- 将 `your_api_key_here` 替换为你的实际 OpenAI API Key
- `.env` 文件通常会被 `.gitignore` 忽略，不会提交到版本控制系统
- 不要将 API Key 分享给他人或提交到公共仓库

#### 获取 OpenAI API Key

1. 访问 [OpenAI Platform](https://platform.openai.com/)
2. 登录或注册账号
3. 进入 API Keys 页面
4. 创建新的 API Key
5. 复制 Key 并粘贴到 `.env` 文件中

### 5. 检查环境配置

运行环境检测脚本，检查所有配置是否正确：

```bash
# 确保虚拟环境已激活
python check_env.py
```

脚本会检查：
- Python 版本是否符合要求
- 虚拟环境是否激活
- 依赖包是否已安装
- .env 文件是否存在
- API Key 是否已配置

## 📚 Notebook 说明

### `basicCommuation.ipynb`
基础通信示例，包括：
- 基本 Agent 使用
- 结构化输出（使用 Pydantic 模型）
- 会话管理（SQLiteSession）

### `functionTool.ipynb`
函数工具示例，展示：
- 自定义函数工具（使用 `@function_tool` 装饰器）
- 内置工具（WebSearchTool）
- 函数调用和链式调用

### `handOff.ipynb`
代理交接示例，演示：
- 多个 Agent 的创建
- Agent 之间的交接（handoff）
- 路由 Agent 的使用

### `openai-agent-use-examples.ipynb`
OpenAI Agent SDK 的综合使用示例集合。

### `sourceCommunication.ipynb`
源通信相关示例。

## 📦 主要依赖

- `openai` - OpenAI Python SDK
- `openai-agents` - OpenAI Agents SDK
- `pydantic` - 数据验证库
- `python-dotenv` - 环境变量管理
- `jupyter` - Jupyter Notebook 环境
- `httpx` - HTTP 客户端
- `fastapi` - Web 框架（可选）

完整依赖列表请查看 `requirements.txt`。

## 🔧 常见问题

### Python 3.9 类型注解问题

如果遇到 `TypeError: Unable to evaluate type annotation 'float | None'` 错误，请安装 `eval_type_backport`：

```bash
pip install eval_type_backport
```

### 异步函数使用

注意 `Runner.run()` 是异步函数，需要使用 `await`：

```python
result = await Runner.run(agent, "Hello!")
```

## 📝 注意事项

- 确保已正确配置 OpenAI API Key
- 某些功能可能需要付费的 OpenAI API 访问权限
- 建议在虚拟环境中运行代码

## 📄 许可证

本项目仅用于学习和研究目的。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

