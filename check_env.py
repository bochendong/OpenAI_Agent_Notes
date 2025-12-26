#!/usr/bin/env python3
"""
环境配置检测脚本
检查项目环境是否正确配置
"""

import sys
import os
from pathlib import Path

# 颜色输出
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_success(message):
    print(f"{Colors.GREEN}✓{Colors.END} {message}")

def print_error(message):
    print(f"{Colors.RED}✗{Colors.END} {message}")

def print_warning(message):
    print(f"{Colors.YELLOW}⚠{Colors.END} {message}")

def print_info(message):
    print(f"{Colors.BLUE}ℹ{Colors.END} {message}")

def check_python_version():
    """检查 Python 版本"""
    print(f"\n{Colors.BOLD}检查 Python 版本...{Colors.END}")
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    
    if version.major == 3 and version.minor >= 9:
        print_success(f"Python 版本: {version_str} (符合要求 >= 3.9)")
        return True
    else:
        print_error(f"Python 版本: {version_str} (需要 >= 3.9)")
        return False

def check_venv():
    """检查虚拟环境"""
    print(f"\n{Colors.BOLD}检查虚拟环境...{Colors.END}")
    
    # 检查是否在虚拟环境中
    in_venv = hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )
    
    if in_venv:
        venv_path = sys.prefix
        print_success(f"虚拟环境已激活: {venv_path}")
        return True
    else:
        print_warning("未检测到虚拟环境")
        print_info("建议使用虚拟环境，运行: python3 -m venv venv")
        return False

def check_venv_directory():
    """检查 venv 目录是否存在"""
    print(f"\n{Colors.BOLD}检查 venv 目录...{Colors.END}")
    venv_dir = Path("venv")
    
    if venv_dir.exists():
        print_success(f"venv 目录存在: {venv_dir.absolute()}")
        return True
    else:
        print_warning("venv 目录不存在")
        print_info("创建虚拟环境: python3 -m venv venv")
        return False

def check_dependencies():
    """检查依赖包是否安装"""
    print(f"\n{Colors.BOLD}检查依赖包...{Colors.END}")
    
    # 包名映射：pip 包名 -> 导入名
    required_packages = {
        'openai': 'openai',
        'openai-agents': 'agents',  # openai-agents 包的导入名是 agents
        'pydantic': 'pydantic',
        'python-dotenv': 'dotenv',  # python-dotenv 包的导入名是 dotenv
        'jupyter': 'jupyter',
        'httpx': 'httpx',
    }
    
    missing_packages = []
    installed_packages = []
    
    for package_name, import_name in required_packages.items():
        try:
            __import__(import_name)
            installed_packages.append(package_name)
            print_success(f"{package_name} 已安装")
        except ImportError:
            missing_packages.append(package_name)
            print_error(f"{package_name} 未安装")
    
    if missing_packages:
        print_warning(f"缺少以下包: {', '.join(missing_packages)}")
        print_info("安装依赖: pip install -r requirements.txt")
        return False
    else:
        print_success("所有必需依赖包已安装")
        return True

def check_env_file():
    """检查 .env 文件"""
    print(f"\n{Colors.BOLD}检查 .env 文件...{Colors.END}")
    env_file = Path(".env")
    
    if env_file.exists():
        print_success(f".env 文件存在: {env_file.absolute()}")
        return True
    else:
        print_error(".env 文件不存在")
        print_info("创建 .env 文件并添加: OPENAI_API_KEY=your_api_key_here")
        return False

def check_api_key():
    """检查 API Key 是否配置"""
    print(f"\n{Colors.BOLD}检查 API Key...{Colors.END}")
    
    # 尝试从环境变量读取
    api_key = os.environ.get("OPENAI_API_KEY")
    
    # 如果环境变量中没有，尝试从 .env 文件读取
    if not api_key:
        env_file = Path(".env")
        if env_file.exists():
            try:
                from dotenv import load_dotenv
                load_dotenv()
                api_key = os.environ.get("OPENAI_API_KEY")
            except ImportError:
                print_warning("python-dotenv 未安装，无法读取 .env 文件")
    
    if api_key:
        # 只显示前8个字符和后4个字符，中间用*代替
        masked_key = f"{api_key[:8]}...{api_key[-4:]}" if len(api_key) > 12 else "***"
        print_success(f"API Key 已配置: {masked_key}")
        return True
    else:
        print_error("API Key 未配置")
        print_info("在 .env 文件中添加: OPENAI_API_KEY=your_api_key_here")
        return False

def check_optional_packages():
    """检查可选依赖包"""
    print(f"\n{Colors.BOLD}检查可选依赖包...{Colors.END}")
    
    optional_packages = {
        'fastapi': 'FastAPI',
        'uvicorn': 'Uvicorn',
        'eval_type_backport': 'eval_type_backport (Python 3.9 类型注解支持)',
    }
    
    for package, description in optional_packages.items():
        try:
            import_name = package.replace('-', '_')
            __import__(import_name)
            print_success(f"{description} 已安装")
        except ImportError:
            print_info(f"{description} 未安装（可选）")

def main():
    """主函数"""
    print(f"\n{Colors.BOLD}{'='*50}{Colors.END}")
    print(f"{Colors.BOLD}OpenAI Agent Notes - 环境配置检测{Colors.END}")
    print(f"{Colors.BOLD}{'='*50}{Colors.END}")
    
    results = []
    
    # 执行各项检查
    results.append(("Python 版本", check_python_version()))
    results.append(("虚拟环境目录", check_venv_directory()))
    results.append(("虚拟环境激活", check_venv()))
    results.append(("依赖包", check_dependencies()))
    results.append((".env 文件", check_env_file()))
    results.append(("API Key", check_api_key()))
    
    # 检查可选包
    check_optional_packages()
    
    # 总结
    print(f"\n{Colors.BOLD}{'='*50}{Colors.END}")
    print(f"{Colors.BOLD}检测结果总结{Colors.END}")
    print(f"{Colors.BOLD}{'='*50}{Colors.END}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = f"{Colors.GREEN}通过{Colors.END}" if result else f"{Colors.RED}失败{Colors.END}"
        print(f"{name}: {status}")
    
    print(f"\n通过: {passed}/{total}")
    
    if passed == total:
        print(f"\n{Colors.GREEN}{Colors.BOLD}✓ 所有检查通过！环境配置正确。{Colors.END}")
        return 0
    else:
        print(f"\n{Colors.YELLOW}{Colors.BOLD}⚠ 部分检查未通过，请根据上述提示进行修复。{Colors.END}")
        return 1

if __name__ == "__main__":
    sys.exit(main())

