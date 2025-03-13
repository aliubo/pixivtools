from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pixivtools",
    version="0.0.5",
    author="aliubo",
    author_email="liubo@aliubo.com",
    description="A Python module for Pixiv crawling and interaction",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aliubo/pixivtools",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "requests",
        "parsel",
        "pillow",
        "pyyaml",
        "sqlalchemy",
    ],
)
