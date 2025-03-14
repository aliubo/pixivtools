from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="pixivtools",
    version="0.0.6",
    author="aliubo",
    author_email="liubo@aliubo.com",
    description="A Python module for Pixiv crawling and interaction",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aliubo/pixivtools",
    packages=find_packages(exclude=["tests*", "examples*"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="pixiv, crawler, downloader, artwork, illustration",
    python_requires=">=3.6",
    install_requires=requirements,
    include_package_data=True,
    package_data={
        "pixivtools": ["*.yaml", "*.yml"],
    },
    entry_points={
        "console_scripts": [
            "pixivtools=pixivtools.cli:main",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/aliubo/pixivtools/issues",
        "Source": "https://github.com/aliubo/pixivtools",
    },
)
