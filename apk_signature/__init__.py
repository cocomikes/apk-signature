#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
APK Signature - Android APK 签名指纹提取工具
"""
from __future__ import (absolute_import, division, print_function, unicode_literals)

import sys
import os
import argparse
from typing import List

from .version import __version__
from .apk_parser import APKParser, APKSignatureError
from .formatter import Formatter


def cli_main():
    """命令行主入口"""
    parser = argparse.ArgumentParser(
        prog='apk-signature',
        description='Android APK 签名指纹提取工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  %(prog)s app.apk                          # 查看签名
  %(prog)s app.apk --verbose                # 查看详细信息
  %(prog)s app.apk --format json            # JSON 格式输出
  %(prog)s app.apk --only md5               # 仅显示 MD5
  %(prog)s --compare app1.apk app2.apk      # 比较两个 APK 签名
  %(prog)s app.apk --verify                 # 验证签名有效性
        '''
    )
    
    parser.add_argument('apk_file', nargs='?', help='APK 文件路径')
    parser.add_argument('-v', '--version', action='version', version=f'%(prog)s {__version__}')
    parser.add_argument('--verbose', action='store_true', help='显示详细证书信息')
    parser.add_argument('--format', choices=['text', 'json', 'simple'], 
                       default='text', help='输出格式 (默认: text)')
    parser.add_argument('--only', choices=['md5', 'sha1', 'sha256'],
                       help='仅显示指定类型的指纹')
    parser.add_argument('--compare', nargs=2, metavar=('APK1', 'APK2'),
                       help='比较两个 APK 的签名')
    parser.add_argument('--verify', action='store_true', help='验证签名有效性')
    
    args = parser.parse_args()
    
    try:
        # 比较模式
        if args.compare:
            handle_compare(args.compare[0], args.compare[1])
            return 0
        
        # 需要 APK 文件
        if not args.apk_file:
            parser.print_help()
            return 1
        
        # 检查文件是否存在
        if not os.path.exists(args.apk_file):
            print(f"错误: 文件不存在: {args.apk_file}", file=sys.stderr)
            return 1
        
        # 解析 APK
        parser_obj = APKParser(args.apk_file)
        info = parser_obj.parse()
        
        # 验证签名
        if args.verify:
            is_valid, message = parser_obj.verify_signature()
            print(f"\n签名验证: {'✓ ' if is_valid else '✗ '}{message}\n")
        
        # 格式化输出
        if args.format == 'json':
            output = Formatter.format_json(info)
        elif args.format == 'simple' or args.only:
            hash_type = args.only if args.only else 'md5'
            output = Formatter.format_simple(info, hash_type)
        else:
            output = Formatter.format_text(info, args.verbose)
        
        print(output)
        return 0
        
    except APKSignatureError as e:
        print(f"错误: {e}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\n已取消", file=sys.stderr)
        return 130
    except Exception as e:
        print(f"未预期的错误: {e}", file=sys.stderr)
        if '--debug' in sys.argv:
            import traceback
            traceback.print_exc()
        return 1


def handle_compare(apk1: str, apk2: str):
    """处理签名比较"""
    # 检查文件
    for apk in [apk1, apk2]:
        if not os.path.exists(apk):
            print(f"错误: 文件不存在: {apk}", file=sys.stderr)
            sys.exit(1)
    
    try:
        result = APKParser.compare_signatures(apk1, apk2)
        output = Formatter.format_comparison(result)
        print(output)
        
        # 返回码：相同返回 0，不同返回 1
        sys.exit(0 if result['identical'] else 1)
        
    except APKSignatureError as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    sys.exit(cli_main())
