#!/usr/bin/env python3
"""
Setup script cho Hello World Desktop App
"""

from setuptools import setup, find_packages
from pathlib import Path

# Đọc README
this_directory = Path(__file__).parent
long_description = (this_directory / "docs" / "README.md").read_text(encoding="utf-8")

# Đọc requirements
requirements = []
requirements_file = this_directory / "requirements.txt"
if requirements_file.exists():
    with open(requirements_file, 'r') as f:
        requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name="hello-world-app",
    version="1.0.0",
    author="Hello World Team",
    author_email="team@helloworld.app",
    description="A simple desktop application for Fedora with system tray support",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/hello-world-app",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Desktop Environment",
        "Topic :: System :: System Shells",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-gtk",
            "black",
            "flake8",
            "mypy",
        ],
    },
    entry_points={
        "console_scripts": [
            "hello-world-app=hello_world_app.main:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords="desktop gtk fedora linux system-tray",
    project_urls={
        "Bug Reports": "https://github.com/your-username/hello-world-app/issues",
        "Source": "https://github.com/your-username/hello-world-app",
        "Documentation": "https://github.com/your-username/hello-world-app/blob/main/docs/README.md",
    },
) 