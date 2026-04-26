"""
Packaging configuration for LLM-Noise-Filtering-System.
Why: Enables pip install, CLI entry points, dependency resolution, and distribution.
     Modern Python (3.10+) prefers pyproject.toml, but setup.py remains fully supported
     and is easier to read for GSoC reviewers learning packaging fundamentals.
"""
from setuptools import setup, find_packages

# Read README for PyPI/GitHub integration
with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    # 📦 Basic Metadata
    name="llm-noise-filtering-system",
    version="0.1.0",
    author="mUchiha26",
    author_email="RAHAL.Mohamed-Yassine@tek-up.de",
    description="Hybrid rule-based + LLM pipeline for cleaning noisy security reconnaissance data (e.g., SpiderFoot).",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mUchiha26/LLM-Noise-Filtering-System",
    license="Apache-2.0",

    # 🐍 Python & Package Discovery
    python_requires=">=3.10",
    package_dir={"": "src"},
    # Finds subpackages (e.g., src/core/)
    packages=find_packages(where="src"),
    # Handles flat modules in src/ (main.py, config_loader.py, orchestrator.py)
    py_modules=["main", "config_loader", "orchestrator"],

    # 📦 Dependencies (split for clean env management)
    install_requires=[
        "PyYAML>=6.0.1",
        "python-dotenv>=1.0.0",
        "pydantic>=2.0.0",
        "httpx>=0.27.0",
        "rich>=13.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "pytest-mock>=3.12.0",
            "ruff>=0.3.0",
        ],
        # Optional: pull in OpenAI SDK if you ever switch from raw httpx
        "llm-openai": ["openai>=1.30.0"],
    },

    # 🖥️ CLI Entry Point (allows running `llm-filter` anywhere after install)
    entry_points={
        "console_scripts": [
            "llm-filter=main:main",
        ],
    },

    # 🏷️ PyPI Classifiers & Keywords (helps with discoverability & GSoC alignment)
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Security",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Filters",
    ],
    keywords="osint, security, llm, filtering, spiderfoot, reconnaissance, noise-reduction, hybrid-pipeline",

    # 📁 Data & Config Inclusion
    include_package_data=True,
)