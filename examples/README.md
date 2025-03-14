# Pixivtools Examples

[中文文档](README_zh.md)

This directory contains various examples demonstrating how to use the pixivtools package.

## Setup

1. Install pixivtools:
```bash
pip install pixivtools --upgrade
```

2. Configure your environment:
   - Edit `config.yaml` and replace `YOUR_PHPSESSID` with your actual Pixiv PHPSESSID
   - Adjust proxy settings if needed
   - Configure database settings according to your needs

## Available Examples

1. `constructor_example.py` - Shows how to create a crawler using the constructor approach
2. `config_file_example.py` - Demonstrates configuration using a YAML file
3. `batch_processing_example.py` - Shows how to process multiple artworks/users/tags in batch

## Running the Examples

Each example can be run independently:

```bash
python examples/constructor_example.py
python examples/config_file_example.py
python examples/batch_processing_example.py
```

## Important Notes

- Always replace `YOUR_PHPSESSID` with your actual Pixiv PHPSESSID
- Make sure to configure your proxy settings if needed
- Database credentials in examples should be replaced with your actual credentials
- The examples use some sample artwork IDs, user IDs, and tags - feel free to modify them according to your needs 