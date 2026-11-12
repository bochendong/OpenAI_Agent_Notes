#!/usr/bin/env python3
"""
Environment configuration checker.
Checks whether the project environment is configured correctly.
"""

import sys
import os
from pathlib import Path

# Terminal output colors
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
    """Check the Python version."""
    print(f"\n{Colors.BOLD}Checking the Python version...{Colors.END}")
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    
    if version.major == 3 and version.minor >= 9:
        print_success(f"Python version: {version_str} (meets the >= 3.9 requirement)")
        return True
    else:
        print_error(f"Python version: {version_str} (requires >= 3.9)")
        return False

def check_venv():
    """Check whether a virtual environment is active."""
    print(f"\n{Colors.BOLD}Checking the active virtual environment...{Colors.END}")
    
    # Check whether Python is running in a virtual environment.
    in_venv = hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )
    
    if in_venv:
        venv_path = sys.prefix
        print_success(f"Virtual environment is active: {venv_path}")
        return True
    else:
        print_warning("No active virtual environment detected")
        print_info("To create a virtual environment, run: python3 -m venv venv")
        return False

def check_venv_directory():
    """Check whether the venv directory exists."""
    print(f"\n{Colors.BOLD}Checking for the venv directory...{Colors.END}")
    venv_dir = Path("venv")
    
    if venv_dir.exists():
        print_success(f"venv directory exists: {venv_dir.absolute()}")
        return True
    else:
        print_warning("venv directory does not exist")
        print_info("Create a virtual environment: python3 -m venv venv")
        return False

def check_dependencies():
    """Check whether the dependencies are installed."""
    print(f"\n{Colors.BOLD}Checking dependencies...{Colors.END}")
    
    # Map pip package names to import names.
    required_packages = {
        'openai': 'openai',
        'openai-agents': 'agents',
        'pydantic': 'pydantic',
        'python-dotenv': 'dotenv',
        'jupyter': 'jupyter',
        'httpx': 'httpx',
    }
    
    missing_packages = []
    installed_packages = []
    
    for package_name, import_name in required_packages.items():
        try:
            __import__(import_name)
            installed_packages.append(package_name)
            print_success(f"{package_name} is installed")
        except ImportError:
            missing_packages.append(package_name)
            print_error(f"{package_name} is missing")
    
    if missing_packages:
        print_warning(f"Missing packages: {', '.join(missing_packages)}")
        print_info("Install dependencies: pip install -r requirements.txt")
        return False
    else:
        print_success("All required packages are installed")
        return True

def check_env_file():
    """Check whether the .env file exists."""
    print(f"\n{Colors.BOLD}Checking for the .env file...{Colors.END}")
    env_file = Path(".env")
    
    if env_file.exists():
        print_success(f".env file exists: {env_file.absolute()}")
        return True
    else:
        print_error(".env file does not exist")
        print_info("Create a .env file and add: OPENAI_API_KEY=your_api_key_here")
        return False

def check_api_key():
    """Check whether the API key is configured."""
    print(f"\n{Colors.BOLD}Checking the API key...{Colors.END}")
    
    # Try to read the API key from the environment.
    api_key = os.environ.get("OPENAI_API_KEY")
    
    # Fall back to the .env file if the environment variable is missing.
    if not api_key:
        env_file = Path(".env")
        if env_file.exists():
            try:
                from dotenv import load_dotenv
                load_dotenv()
                api_key = os.environ.get("OPENAI_API_KEY")
            except ImportError:
                print_warning("Install python-dotenv to read the .env file")
    
    if api_key:
        # Show the first eight and last four characters, with asterisks in between.
        masked_key = f"{api_key[:8]}...{api_key[-4:]}" if len(api_key) > 12 else "***"
        print_success(f"API key is configured: {masked_key}")
        return True
    else:
        print_error("API key is missing")
        print_info("Add this line to .env: OPENAI_API_KEY=your_api_key_here")
        return False

def check_optional_packages():
    """Check optional dependencies."""
    print(f"\n{Colors.BOLD}Checking optional dependencies...{Colors.END}")
    
    optional_packages = {
        'fastapi': 'FastAPI',
        'uvicorn': 'Uvicorn',
        'eval_type_backport': 'eval_type_backport (Python 3.9 type annotation support)',
    }
    
    for package, description in optional_packages.items():
        try:
            import_name = package.replace('-', '_')
            __import__(import_name)
            print_success(f"{description} is installed")
        except ImportError:
            print_info(f"{description} is missing (optional)")

def main():
    """Run the environment checks and report the results."""
    print(f"\n{Colors.BOLD}{'='*50}{Colors.END}")
    print(f"{Colors.BOLD}OpenAI Agent Notes - Environment Check{Colors.END}")
    print(f"{Colors.BOLD}{'='*50}{Colors.END}")
    
    results = []
    
    # Run the checks.
    results.append(("Python version", check_python_version()))
    results.append(("Virtual environment directory", check_venv_directory()))
    results.append(("Active virtual environment", check_venv()))
    results.append(("Dependencies", check_dependencies()))
    results.append((".env file", check_env_file()))
    results.append(("API Key", check_api_key()))
    
    # Check optional packages.
    check_optional_packages()
    
    # Summarize the results.
    print(f"\n{Colors.BOLD}{'='*50}{Colors.END}")
    print(f"{Colors.BOLD}Check Results{Colors.END}")
    print(f"{Colors.BOLD}{'='*50}{Colors.END}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = f"{Colors.GREEN}PASS{Colors.END}" if result else f"{Colors.RED}FAIL{Colors.END}"
        print(f"{name}: {status}")
    
    print(f"\nPassed: {passed}/{total}")
    
    if passed == total:
        print(f"\n{Colors.GREEN}{Colors.BOLD}✓ All checks passed. The environment is ready.{Colors.END}")
        return 0
    else:
        print(f"\n{Colors.YELLOW}{Colors.BOLD}⚠ Some checks failed. Follow the instructions above to fix them.{Colors.END}")
        return 1

if __name__ == "__main__":
    sys.exit(main())

