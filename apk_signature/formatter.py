#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
输出格式化器
"""
import json
from typing import Dict


class Formatter:
    """输出格式化器"""
    
    @staticmethod
    def format_text(info: Dict, verbose: bool = False) -> str:
        """文本格式输出"""
        lines = []
        
        # 签名方案
        lines.append(f"签名方案: {info.get('scheme_version', 'unknown')}")
        if 'v2_signature' in info:
            lines.append(f"V2/V3 签名: {info['v2_signature']}")
        
        lines.append("")
        
        # 指纹信息
        fp = info['fingerprints']
        lines.append("=== 签名指纹 (十六进制-冒号-大写) ===")
        lines.append(f"MD5:    {Formatter._format_fingerprint(fp['md5'], 'colon-upper')}")
        lines.append(f"SHA1:   {Formatter._format_fingerprint(fp['sha1'], 'colon-upper')}")
        lines.append(f"SHA256: {Formatter._format_fingerprint(fp['sha256'], 'colon-upper')}")
        
        lines.append("")
        lines.append("=== 签名指纹 (十六进制-大写) ===")
        lines.append(f"MD5:    {fp['md5'].upper()}")
        lines.append(f"SHA1:   {fp['sha1'].upper()}")
        lines.append(f"SHA256: {fp['sha256'].upper()}")
        
        lines.append("")
        lines.append("=== 签名指纹 (十六进制-小写) ===")
        lines.append(f"MD5:    {fp['md5'].lower()}")
        lines.append(f"SHA1:   {fp['sha1'].lower()}")
        lines.append(f"SHA256: {fp['sha256'].lower()}")
        
        # 详细信息
        if verbose and 'certificate' in info:
            cert = info['certificate']
            lines.append("")
            lines.append("=== 证书详细信息 ===")
            lines.append(f"主题 (Subject):")
            for key, value in cert['subject'].items():
                if value != "N/A":
                    lines.append(f"  {key}: {value}")
            
            lines.append(f"颁发者 (Issuer):")
            for key, value in cert['issuer'].items():
                if value != "N/A":
                    lines.append(f"  {key}: {value}")
            
            lines.append(f"序列号: {cert['serial_number']}")
            lines.append(f"有效期从: {cert['valid_from']}")
            lines.append(f"有效期至: {cert['valid_to']}")
            lines.append(f"是否过期: {'是' if cert['is_expired'] else '否'}")
            lines.append(f"签名算法: {cert['signature_algorithm']}")
        
        return '\n'.join(lines)
    
    @staticmethod
    def format_json(info: Dict, pretty: bool = True) -> str:
        """JSON 格式输出"""
        if pretty:
            return json.dumps(info, indent=2, ensure_ascii=False)
        return json.dumps(info, ensure_ascii=False)
    
    @staticmethod
    def format_simple(info: Dict, hash_type: str = 'md5') -> str:
        """简单格式输出（仅指纹）"""
        fp = info['fingerprints']
        return fp.get(hash_type.lower(), '')
    
    @staticmethod
    def format_comparison(result: Dict) -> str:
        """格式化签名比较结果"""
        lines = []
        lines.append("=== APK 签名比较 ===")
        lines.append(f"APK 1: {result['apk1']}")
        lines.append(f"APK 2: {result['apk2']}")
        lines.append("")
        
        lines.append(f"签名是否相同: {'✓ 是' if result['identical'] else '✗ 否'}")
        lines.append("")
        
        lines.append("指纹对比:")
        lines.append(f"  MD5:    {'✓ 相同' if result['md5_match'] else '✗ 不同'}")
        lines.append(f"  SHA1:   {'✓ 相同' if result['sha1_match'] else '✗ 不同'}")
        lines.append(f"  SHA256: {'✓ 相同' if result['sha256_match'] else '✗ 不同'}")
        
        lines.append("")
        lines.append("APK 1 指纹:")
        fp1 = result['fingerprints1']
        lines.append(f"  MD5:    {fp1['md5']}")
        lines.append(f"  SHA1:   {fp1['sha1']}")
        lines.append(f"  SHA256: {fp1['sha256']}")
        
        lines.append("")
        lines.append("APK 2 指纹:")
        fp2 = result['fingerprints2']
        lines.append(f"  MD5:    {fp2['md5']}")
        lines.append(f"  SHA1:   {fp2['sha1']}")
        lines.append(f"  SHA256: {fp2['sha256']}")
        
        return '\n'.join(lines)
    
    @staticmethod
    def _format_fingerprint(fp: str, style: str) -> str:
        """格式化指纹"""
        if style == 'colon-upper':
            # 转换为大写并添加冒号分隔
            fp = fp.upper()
            return ':'.join([fp[i:i+2] for i in range(0, len(fp), 2)])
        elif style == 'colon-lower':
            fp = fp.lower()
            return ':'.join([fp[i:i+2] for i in range(0, len(fp), 2)])
        elif style == 'upper':
            return fp.upper()
        elif style == 'lower':
            return fp.lower()
        return fp
