"""Setup configuration for transitions_reactflow package."""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file for long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(
    encoding="utf-8") if readme_file.exists() else ""

# Read version from __init__.py
version = "0.1.0"

setup(
    name="transitions-rf",
    version=version,
    author="transitions_rf contributors",
    description="React Flow graph engine for pytransitions state machines",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/transitions-rf",  # Update with actual URL
    packages=find_packages(
        exclude=["tests", "tests.*", "examples", "react_app"]),
    python_requires=">=3.7",
    install_requires=[
        "transitions>=0.8.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=3.0.0",
            "black>=22.0.0",
            "mypy>=0.950",
            "flake8>=4.0.0",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Visualization",
    ],
    keywords="state-machine transitions visualization react-flow",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/transitions-rf/issues",
        "Source": "https://github.com/yourusername/transitions-rf",
    },
)
