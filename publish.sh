#!/bin/bash

# 清理之前的构建文件
rm -rf dist/ *.egg-info/

# 安装/更新构建工具
python -m pip install --upgrade pip
python -m pip install --upgrade build twine

# 构建包
python -m build

# 检查分发包
twine check dist/*

# 上传到 PyPI
echo "Uploading to PyPI..."
twine upload dist/*

echo "Done! Package published to PyPI successfully."