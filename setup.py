"""A minimal setup.py for Langroid
"""

from setuptools import setup, find_packages

setup(
    name="langroid-slim",
    version="0.1.255",
    description="Harness LLMs with Multi-Agent Programming",
    author="Prasad Chalasani",
    author_email="pchalasani@gmail.com",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "onnxruntime==1.16.1",
        "fire>=0.5.0",
        "bs4>=0.0.1",
        "python-dotenv>=1.0.0",
        "wget>=3.2",
        "rich>=13.3.4",
        "requests-oauthlib>=1.3.1",
        "halo>=0.0.31",
        "typer>=0.9.0",
        "colorlog>=6.7.0",
        "openai>=1.14.0",
        "tiktoken>=0.7.0",
        "pygithub>=1.58.1",
        "pygments>=2.15.1",
        "redis>=5.0.1",
        "fakeredis>=2.12.1",
        "requests>=2.31.0",
        "types-redis>=4.5.5.2",
        "types-requests>=2.31.0.1",
        "pyparsing>=3.0.9",
        "nltk>=3.8.1",
        "qdrant-client>=1.8.0",
        "pydantic==1.10.13",
        "pandas>=2.1.3",
        "pyyaml>=6.0",
        "rank-bm25>=0.2.2",
        "groq>=0.5.0",
        "jinja2>=3.1.2",
        "docstring-parser>=0.15",
        "faker>=18.9.0",
        "thefuzz==0.20.0",
        "aiohttp>=3.9.1"
    ],
    python_requires=">=3.10, <3.12",
    extras_require={
        "extra":[
            "ruff>=0.2.2",
            "pre-commit>=3.3.2",
            "flake8>=6.0.0",
            "mypy>=1.7.0",
            "black[jupyter]>=24.3.0",
            "autopep8>=2.0.2",
        ],
        "docs": [
            "mkdocs>=1.4.2",
            "mkdocs-material>=9.1.5",
            "mkdocstrings[python]>=0.21.2",
            "mkdocs-awesome-pages-plugin>=2.8.0",
            "mkdocs-rss-plugin>=1.8.0",
            "mkdocs-gen-files>=0.4.0",
            "mkdocs-literate-nav>=0.6.0",
            "mkdocs-section-index>=0.3.5",
            "mkdocs-jupyter>=0.24.1",
            "chromadb>=0.4.21,<=0.4.23",
        ]
    }
)


