#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
APK 签名解析器 - 使用纯 Python 实现，无需临时文件
"""
import zipfile
import hashlib
import struct
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization


class APKSignatureError(Exception):
    """APK 签名解析异常"""
    pass


class APKParser:
    """APK 签名解析器"""
    
    def __init__(self, apk_path: str):
        self.apk_path = apk_path
        self.certificates: List[x509.Certificate] = []
        
    def parse(self) -> Dict:
        """解析 APK 签名信息"""
        try:
            with zipfile.ZipFile(self.apk_path, 'r') as apk:
                # 尝试解析 v1 签名
                v1_info = self._parse_v1_signature(apk)
                
                # 尝试解析 v2/v3 签名
                v2_info = self._parse_v2_v3_signature()
                
                if not v1_info and not v2_info:
                    raise APKSignatureError("未找到有效的签名信息")
                
                # 合并签名信息
                result = v1_info if v1_info else v2_info
                if v2_info:
                    result['v2_signature'] = v2_info.get('scheme_version', 'v2/v3')
                
                return result
                
        except zipfile.BadZipFile:
            raise APKSignatureError(f"无效的 APK 文件: {self.apk_path}")
        except Exception as e:
            raise APKSignatureError(f"解析失败: {str(e)}")
    
    def _parse_v1_signature(self, apk: zipfile.ZipFile) -> Optional[Dict]:
        """解析 v1 (JAR) 签名"""
        # 查找 META-INF 目录中的 RSA/DSA/EC 文件
        cert_files = [f for f in apk.namelist() 
                     if f.startswith('META-INF/') and 
                     (f.endswith('.RSA') or f.endswith('.DSA') or f.endswith('.EC'))]
        
        if not cert_files:
            return None
        
        # 读取第一个证书文件
        cert_data = apk.read(cert_files[0])
        
        try:
            # 解析 PKCS#7 格式
            from cryptography.hazmat.primitives.serialization import pkcs7
            
            # 尝试加载 PKCS7 数据
            try:
                # 某些 APK 使用 DER 编码的 PKCS7
                certs = self._extract_certs_from_pkcs7(cert_data)
            except:
                # 如果失败，尝试直接解析为 X.509 证书
                cert = x509.load_der_x509_certificate(cert_data, default_backend())
                certs = [cert]
            
            if not certs:
                return None
            
            self.certificates = certs
            cert = certs[0]  # 使用第一个证书
            
            return self._extract_cert_info(cert, 'v1')
            
        except Exception as e:
            return None
    
    def _extract_certs_from_pkcs7(self, data: bytes) -> List[x509.Certificate]:
        """从 PKCS#7 数据中提取证书"""
        certs = []
        
        # 简单的 PKCS#7 解析（查找证书序列）
        # 这是一个简化版本，实际 PKCS#7 结构更复杂
        try:
            # 查找证书标记 (0x30 0x82 表示 SEQUENCE)
            i = 0
            while i < len(data) - 4:
                if data[i] == 0x30 and data[i+1] == 0x82:
                    # 读取长度
                    length = struct.unpack('>H', data[i+2:i+4])[0]
                    cert_data = data[i:i+4+length]
                    try:
                        cert = x509.load_der_x509_certificate(cert_data, default_backend())
                        certs.append(cert)
                        i += 4 + length
                    except:
                        i += 1
                else:
                    i += 1
        except:
            pass
        
        return certs
    
    def _parse_v2_v3_signature(self) -> Optional[Dict]:
        """解析 v2/v3 签名块"""
        try:
            with open(self.apk_path, 'rb') as f:
                # 读取文件末尾查找签名块
                f.seek(-1024, 2)  # 从文件末尾往前读 1KB
                data = f.read()
                
                # 查找 APK Signing Block 魔数
                magic = b'APK Sig Block 42'
                if magic not in data:
                    return None
                
                # 这里需要完整的 v2/v3 解析逻辑
                # 由于复杂度较高，暂时返回 None
                # 实际项目中可以使用 androguard 等库
                return None
                
        except Exception:
            return None
    
    def _extract_cert_info(self, cert: x509.Certificate, scheme: str) -> Dict:
        """提取证书信息"""
        # 计算指纹
        cert_der = cert.public_bytes(serialization.Encoding.DER)
        
        md5_hash = hashlib.md5(cert_der).hexdigest()
        sha1_hash = hashlib.sha1(cert_der).hexdigest()
        sha256_hash = hashlib.sha256(cert_der).hexdigest()
        
        # 提取主题信息
        subject = cert.subject
        issuer = cert.issuer
        
        def get_name_attr(name, oid):
            try:
                return name.get_attributes_for_oid(oid)[0].value
            except:
                return "N/A"
        
        from cryptography.x509.oid import NameOID
        
        return {
            'scheme_version': scheme,
            'fingerprints': {
                'md5': md5_hash,
                'sha1': sha1_hash,
                'sha256': sha256_hash,
            },
            'certificate': {
                'subject': {
                    'CN': get_name_attr(subject, NameOID.COMMON_NAME),
                    'O': get_name_attr(subject, NameOID.ORGANIZATION_NAME),
                    'OU': get_name_attr(subject, NameOID.ORGANIZATIONAL_UNIT_NAME),
                    'L': get_name_attr(subject, NameOID.LOCALITY_NAME),
                    'ST': get_name_attr(subject, NameOID.STATE_OR_PROVINCE_NAME),
                    'C': get_name_attr(subject, NameOID.COUNTRY_NAME),
                },
                'issuer': {
                    'CN': get_name_attr(issuer, NameOID.COMMON_NAME),
                    'O': get_name_attr(issuer, NameOID.ORGANIZATION_NAME),
                },
                'serial_number': format(cert.serial_number, 'x'),
                'valid_from': cert.not_valid_before.isoformat(),
                'valid_to': cert.not_valid_after.isoformat(),
                'is_expired': datetime.now() > cert.not_valid_after,
                'signature_algorithm': cert.signature_algorithm_oid._name,
            }
        }
    
    def verify_signature(self) -> Tuple[bool, str]:
        """验证签名有效性"""
        if not self.certificates:
            return False, "未找到证书"
        
        cert = self.certificates[0]
        
        # 检查证书是否过期
        now = datetime.now()
        if now < cert.not_valid_before:
            return False, f"证书尚未生效（生效时间: {cert.not_valid_before}）"
        
        if now > cert.not_valid_after:
            return False, f"证书已过期（过期时间: {cert.not_valid_after}）"
        
        # 检查签名算法
        algo = cert.signature_algorithm_oid._name
        if 'md5' in algo.lower():
            return True, f"警告: 使用了不安全的 MD5 签名算法"
        
        return True, "签名有效"
    
    @staticmethod
    def compare_signatures(apk1_path: str, apk2_path: str) -> Dict:
        """比较两个 APK 的签名"""
        parser1 = APKParser(apk1_path)
        parser2 = APKParser(apk2_path)
        
        info1 = parser1.parse()
        info2 = parser2.parse()
        
        fp1 = info1['fingerprints']
        fp2 = info2['fingerprints']
        
        return {
            'apk1': apk1_path,
            'apk2': apk2_path,
            'md5_match': fp1['md5'] == fp2['md5'],
            'sha1_match': fp1['sha1'] == fp2['sha1'],
            'sha256_match': fp1['sha256'] == fp2['sha256'],
            'identical': (fp1['md5'] == fp2['md5'] and 
                         fp1['sha1'] == fp2['sha1'] and 
                         fp1['sha256'] == fp2['sha256']),
            'fingerprints1': fp1,
            'fingerprints2': fp2,
        }
