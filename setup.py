from setuptools import setup, find_packages

setup(
    name="llm-noise-filter",
    version="0.1.0",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        "requests>=2.31.0",
        "python-dotenv>=1.0.0",
        "pyyaml>=6.0",
        "tenacity>=8.2.0"
    ],
    entry_points={
        "console_scripts": [
            "noise-filter=main:main"
        ]
    }
)