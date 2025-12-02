#!/bin/sh
# 开发模式安装，会创建.egg-info目录，用于开发测试。
# python3 -m pip install -e . --quiet
# 发布模式并上传到pip
# python3 setup.py bdist_wheel --universal upload -r pypi
# 本地安装
# pip install --force-reinstall ./dist/apk_signature-1.0.0-py3-none-any.whl
python3 setup.py bdist_wheel