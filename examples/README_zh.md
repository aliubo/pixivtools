# Pixivtools 示例

本目录包含了多个展示如何使用 pixivtools 包的示例。

## 环境配置

1. 安装 pixivtools：
```bash
pip install pixivtools --upgrade
```

2. 配置环境：
   - 编辑 `config.yaml` 并将 `YOUR_PHPSESSID` 替换为你的 Pixiv PHPSESSID
   - 根据需要调整代理设置
   - 根据需要配置数据库设置

## 可用示例

1. `constructor_example.py` - 展示如何使用构造器方式创建爬虫
2. `config_file_example.py` - 演示如何使用 YAML 文件配置
4. `batch_processing_example.py` - 展示如何批量处理多个作品/用户/标签

## 运行示例

每个示例都可以独立运行：

```bash
python examples/constructor_example.py
python examples/config_file_example.py
python examples/batch_processing_example.py
```

## 重要说明

- 务必将 `YOUR_PHPSESSID` 替换为你的实际 Pixiv PHPSESSID
- 确保根据需要正确配置代理设置
- 数据库凭据需要替换为你的实际凭据
- 示例中使用的作品ID、用户ID和标签仅供参考，可以根据需要自行修改 