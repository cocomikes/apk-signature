#!/bin/sh
#
# Generate pypi wheels universal package and upload
# pip install --force-reinstall ./dist/apk_signature-1.0.0-py3-none-any.whl
#
# python3 setup.py bdist_wheel --universal upload -r pypi
python3 setup.py bdist_wheel