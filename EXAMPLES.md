# APK Signature 使用示例

本文档提供了 `apk-signature` 工具的详细使用示例。

## 目录

- [基础用法](#基础用法)
- [高级功能](#高级功能)
- [脚本集成](#脚本集成)
- [Python API](#python-api)
- [实际场景](#实际场景)

## 基础用法

### 1. 查看 APK 签名

最简单的用法，显示所有格式的指纹：

```bash
apk-signature myapp.apk
```

输出：
```
签名方案: v1

=== 签名指纹 (十六进制-冒号-大写) ===
MD5:    CD:E9:F6:20:8D:67:2B:54:B1:DA:CC:0B:70:29:F5:EB
SHA1:   38:91:8A:45:3D:07:19:93:54:F8:B1:9A:F0:5E:C6:56:2C:ED:57:88
SHA256: F0:FD:6C:5B:41:0F:25:CB:25:C3:B5:33:46:C8:97:2F:AE:30:F8:EE:74:11:DF:91:04:80:AD:6B:2D:60:DB:83

=== 签名指纹 (十六进制-大写) ===
MD5:    CDE9F6208D672B54B1DACC0B7029F5EB
SHA1:   38918A453D07199354F8B19AF05EC6562CED5788
SHA256: F0FD6C5B410F25CB25C3B53346C8972FAE30F8EE7411DF910480AD6B2D60DB83

=== 签名指纹 (十六进制-小写) ===
MD5:    cde9f6208d672b54b1dacc0b7029f5eb
SHA1:   38918a453d07199354f8b19af05ec6562ced5788
SHA256: f0fd6c5b410f25cb25c3b53346c8972fae30f8ee7411df910480ad6b2d60db83
```

### 2. 查看版本

```bash
apk-signature --version
```

输出：
```
apk-signature 2.0.0
```

### 3. 查看帮助

```bash
apk-signature --help
```

## 高级功能

### 1. 详细证书信息

使用 `--verbose` 参数查看完整的证书信息：

```bash
apk-signature myapp.apk --verbose
```

输出：
```
签名方案: v1

=== 签名指纹 (十六进制-冒号-大写) ===
MD5:    CD:E9:F6:20:8D:67:2B:54:B1:DA:CC:0B:70:29:F5:EB
SHA1:   38:91:8A:45:3D:07:19:93:54:F8:B1:9A:F0:5E:C6:56:2C:ED:57:88
SHA256: F0:FD:6C:5B:41:0F:25:CB:25:C3:B5:33:46:C8:97:2F:AE:30:F8:EE:74:11:DF:91:04:80:AD:6B:2D:60:DB:83

=== 签名指纹 (十六进制-大写) ===
MD5:    CDE9F6208D672B54B1DACC0B7029F5EB
SHA1:   38918A453D07199354F8B19AF05EC6562CED5788
SHA256: F0FD6C5B410F25CB25C3B53346C8972FAE30F8EE7411DF910480AD6B2D60DB83

=== 签名指纹 (十六进制-小写) ===
MD5:    cde9f6208d672b54b1dacc0b7029f5eb
SHA1:   38918a453d07199354f8b19af05ec6562ced5788
SHA256: f0fd6c5b410f25cb25c3b53346c8972fae30f8ee7411df910480ad6b2d60db83

=== 证书详细信息 ===
主题 (Subject):
  CN: Android
  O: Google Inc.
  OU: Android
  L: Mountain View
  ST: California
  C: US
颁发者 (Issuer):
  CN: Android
  O: Google Inc.
序列号: c2e08746644a308d
有效期从: 2008-08-22T07:13:34
有效期至: 2036-01-08T07:13:34
是否过期: 否
签名算法: sha1WithRSAEncryption
```

### 2. JSON 格式输出

适合程序化处理：

```bash
apk-signature myapp.apk --format json
```

输出：
```json
{
  "scheme_version": "v1",
  "fingerprints": {
    "md5": "cde9f6208d672b54b1dacc0b7029f5eb",
    "sha1": "38918a453d07199354f8b19af05ec6562ced5788",
    "sha256": "f0fd6c5b410f25cb25c3b53346c8972fae30f8ee7411df910480ad6b2d60db83"
  },
  "certificate": {
    "subject": {
      "CN": "Android",
      "O": "Google Inc.",
      "OU": "Android",
      "L": "Mountain View",
      "ST": "California",
      "C": "US"
    },
    "issuer": {
      "CN": "Android",
      "O": "Google Inc."
    },
    "serial_number": "c2e08746644a308d",
    "valid_from": "2008-08-22T07:13:34",
    "valid_to": "2036-01-08T07:13:34",
    "is_expired": false,
    "signature_algorithm": "sha1WithRSAEncryption"
  }
}
```

### 3. 仅显示特定指纹

#### 仅显示 MD5（微信支付、支付宝常用）

```bash
apk-signature myapp.apk --only md5
```

输出：
```
cde9f6208d672b54b1dacc0b7029f5eb
```

#### 仅显示 SHA1

```bash
apk-signature myapp.apk --only sha1
```

输出：
```
38918a453d07199354f8b19af05ec6562ced5788
```

#### 仅显示 SHA256

```bash
apk-signature myapp.apk --only sha256
```

输出：
```
f0fd6c5b410f25cb25c3b53346c8972fae30f8ee7411df910480ad6b2d60db83
```

### 4. 验证签名有效性

```bash
apk-signature myapp.apk --verify
```

**签名有效时：**
```
签名验证: ✓ 签名有效

签名方案: v1
...
```

**证书过期时：**
```
签名验证: ✗ 证书已过期（过期时间: 2020-01-01T00:00:00）

签名方案: v1
...
```

**使用不安全算法时：**
```
签名验证: ✓ 警告: 使用了不安全的 MD5 签名算法

签名方案: v1
...
```

### 5. 比较两个 APK 签名

```bash
apk-signature --compare app1.apk app2.apk
```

**签名相同时：**
```
=== APK 签名比较 ===
APK 1: app1.apk
APK 2: app2.apk

签名是否相同: ✓ 是

指纹对比:
  MD5:    ✓ 相同
  SHA1:   ✓ 相同
  SHA256: ✓ 相同

APK 1 指纹:
  MD5:    cde9f6208d672b54b1dacc0b7029f5eb
  SHA1:   38918a453d07199354f8b19af05ec6562ced5788
  SHA256: f0fd6c5b410f25cb25c3b53346c8972fae30f8ee7411df910480ad6b2d60db83

APK 2 指纹:
  MD5:    cde9f6208d672b54b1dacc0b7029f5eb
  SHA1:   38918a453d07199354f8b19af05ec6562ced5788
  SHA256: f0fd6c5b410f25cb25c3b53346c8972fae30f8ee7411df910480ad6b2d60db83
```

**签名不同时：**
```
=== APK 签名比较 ===
APK 1: app1.apk
APK 2: app2.apk

签名是否相同: ✗ 否

指纹对比:
  MD5:    ✗ 不同
  SHA1:   ✗ 不同
  SHA256: ✗ 不同

APK 1 指纹:
  MD5:    cde9f6208d672b54b1dacc0b7029f5eb
  SHA1:   38918a453d07199354f8b19af05ec6562ced5788
  SHA256: f0fd6c5b410f25cb25c3b53346c8972fae30f8ee7411df910480ad6b2d60db83

APK 2 指纹:
  MD5:    abc123def456789012345678901234ef
  SHA1:   1234567890abcdef1234567890abcdef12345678
  SHA256: 1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef
```

## 脚本集成

### Bash 脚本示例

#### 1. 获取并使用 MD5 签名

```bash
#!/bin/bash

APK_FILE="myapp.apk"

# 获取 MD5 签名
MD5=$(apk-signature "$APK_FILE" --only md5)

echo "APK 文件: $APK_FILE"
echo "MD5 签名: $MD5"

# 将签名写入配置文件
echo "app_signature=$MD5" > config.properties
```

#### 2. 验证签名并处理结果

```bash
#!/bin/bash

APK_FILE="myapp.apk"

# 验证签名
if apk-signature "$APK_FILE" --verify > /dev/null 2>&1; then
    echo "✓ 签名验证通过"
    exit 0
else
    echo "✗ 签名验证失败"
    exit 1
fi
```

#### 3. 批量处理多个 APK

```bash
#!/bin/bash

# 处理当前目录下所有 APK 文件
for apk in *.apk; do
    echo "========================================="
    echo "处理: $apk"
    echo "========================================="
    
    # 获取 MD5
    MD5=$(apk-signature "$apk" --only md5)
    echo "MD5: $MD5"
    
    # 验证签名
    if apk-signature "$apk" --verify > /dev/null 2>&1; then
        echo "状态: ✓ 有效"
    else
        echo "状态: ✗ 无效或过期"
    fi
    
    echo ""
done
```

#### 4. 比较渠道包签名

```bash
#!/bin/bash

MASTER_APK="app-master.apk"
CHANNEL_DIR="channels"

echo "主包: $MASTER_APK"
echo ""

# 遍历所有渠道包
for channel_apk in "$CHANNEL_DIR"/*.apk; do
    echo "检查: $(basename "$channel_apk")"
    
    if apk-signature --compare "$MASTER_APK" "$channel_apk" > /dev/null 2>&1; then
        echo "  ✓ 签名一致"
    else
        echo "  ✗ 签名不一致 - 警告！"
    fi
done
```

#### 5. 生成签名报告

```bash
#!/bin/bash

APK_FILE="myapp.apk"
REPORT_FILE="signature_report.txt"

{
    echo "APK 签名报告"
    echo "============================================"
    echo "文件: $APK_FILE"
    echo "生成时间: $(date)"
    echo ""
    
    apk-signature "$APK_FILE" --verbose
    
    echo ""
    echo "============================================"
    
    if apk-signature "$APK_FILE" --verify > /dev/null 2>&1; then
        echo "验证结果: ✓ 签名有效"
    else
        echo "验证结果: ✗ 签名无效或过期"
    fi
    
} > "$REPORT_FILE"

echo "报告已生成: $REPORT_FILE"
```

### Python 脚本示例

#### 1. 基本使用

```python
#!/usr/bin/env python3
from apk_signature.apk_parser import APKParser

# 解析 APK
parser = APKParser('myapp.apk')
info = parser.parse()

# 打印指纹
print(f"MD5:    {info['fingerprints']['md5']}")
print(f"SHA1:   {info['fingerprints']['sha1']}")
print(f"SHA256: {info['fingerprints']['sha256']}")
```

#### 2. 验证签名

```python
#!/usr/bin/env python3
from apk_signature.apk_parser import APKParser

parser = APKParser('myapp.apk')
info = parser.parse()

# 验证签名
is_valid, message = parser.verify_signature()

if is_valid:
    print(f"✓ {message}")
else:
    print(f"✗ {message}")
    exit(1)
```

#### 3. 批量处理

```python
#!/usr/bin/env python3
import os
import sys
from apk_signature.apk_parser import APKParser

def process_apk(apk_path):
    """处理单个 APK"""
    try:
        parser = APKParser(apk_path)
        info = parser.parse()
        
        return {
            'file': apk_path,
            'md5': info['fingerprints']['md5'],
            'valid': parser.verify_signature()[0]
        }
    except Exception as e:
        return {
            'file': apk_path,
            'error': str(e)
        }

# 处理目录下所有 APK
apk_dir = sys.argv[1] if len(sys.argv) > 1 else '.'

results = []
for filename in os.listdir(apk_dir):
    if filename.endswith('.apk'):
        apk_path = os.path.join(apk_dir, filename)
        result = process_apk(apk_path)
        results.append(result)

# 打印结果
for result in results:
    if 'error' in result:
        print(f"✗ {result['file']}: {result['error']}")
    else:
        status = '✓' if result['valid'] else '✗'
        print(f"{status} {result['file']}: {result['md5']}")
```

#### 4. 生成 JSON 报告

```python
#!/usr/bin/env python3
import json
from apk_signature.apk_parser import APKParser

apk_file = 'myapp.apk'

# 解析 APK
parser = APKParser(apk_file)
info = parser.parse()

# 添加验证信息
is_valid, message = parser.verify_signature()
info['verification'] = {
    'is_valid': is_valid,
    'message': message
}

# 保存为 JSON
with open('signature_report.json', 'w', encoding='utf-8') as f:
    json.dump(info, f, indent=2, ensure_ascii=False)

print("报告已生成: signature_report.json")
```

#### 5. 比较签名并生成报告

```python
#!/usr/bin/env python3
import sys
from apk_signature.apk_parser import APKParser
from apk_signature.formatter import Formatter

if len(sys.argv) != 3:
    print("用法: python compare.py <apk1> <apk2>")
    sys.exit(1)

apk1 = sys.argv[1]
apk2 = sys.argv[2]

# 比较签名
result = APKParser.compare_signatures(apk1, apk2)

# 格式化输出
output = Formatter.format_comparison(result)
print(output)

# 返回码
sys.exit(0 if result['identical'] else 1)
```

## 实际场景

### 场景 1: 微信支付接入

微信支付需要提交应用的 MD5 签名：

```bash
# 获取 MD5 签名（小写，无冒号）
apk-signature myapp.apk --only md5
```

将输出的 MD5 值填入微信支付商户平台。

### 场景 2: 支付宝接入

支付宝同样需要 MD5 签名：

```bash
# 获取 MD5 签名
MD5=$(apk-signature myapp.apk --only md5)
echo "请在支付宝开放平台填入: $MD5"
```

### 场景 3: 多渠道包验证

确保所有渠道包使用相同的签名：

```bash
#!/bin/bash

MASTER="app-master.apk"
FAILED=0

for channel in channels/*.apk; do
    if ! apk-signature --compare "$MASTER" "$channel" > /dev/null 2>&1; then
        echo "✗ 签名不一致: $channel"
        FAILED=1
    fi
done

if [ $FAILED -eq 0 ]; then
    echo "✓ 所有渠道包签名一致"
else
    echo "✗ 发现签名不一致的渠道包"
    exit 1
fi
```

### 场景 4: CI/CD 集成

在持续集成流程中验证签名：

```yaml
# .gitlab-ci.yml
verify_signature:
  stage: test
  script:
    - pip install apk-signature
    - apk-signature app-release.apk --verify
    - |
      EXPECTED_MD5="cde9f6208d672b54b1dacc0b7029f5eb"
      ACTUAL_MD5=$(apk-signature app-release.apk --only md5)
      if [ "$EXPECTED_MD5" != "$ACTUAL_MD5" ]; then
        echo "签名不匹配！"
        exit 1
      fi
```

### 场景 5: 自动化测试

在测试脚本中验证 APK 签名：

```python
import unittest
from apk_signature.apk_parser import APKParser

class TestAPKSignature(unittest.TestCase):
    
    def test_signature_valid(self):
        """测试签名是否有效"""
        parser = APKParser('app-release.apk')
        info = parser.parse()
        is_valid, _ = parser.verify_signature()
        self.assertTrue(is_valid)
    
    def test_expected_md5(self):
        """测试 MD5 是否符合预期"""
        parser = APKParser('app-release.apk')
        info = parser.parse()
        expected_md5 = "cde9f6208d672b54b1dacc0b7029f5eb"
        actual_md5 = info['fingerprints']['md5']
        self.assertEqual(expected_md5, actual_md5)
    
    def test_debug_release_different(self):
        """测试 debug 和 release 签名不同"""
        result = APKParser.compare_signatures(
            'app-debug.apk',
            'app-release.apk'
        )
        self.assertFalse(result['identical'])

if __name__ == '__main__':
    unittest.main()
```

## 总结

`apk-signature` 工具提供了灵活强大的 APK 签名分析功能，适用于：

- 第三方平台接入（微信、支付宝等）
- 多渠道包管理
- CI/CD 流程集成
- 自动化测试
- 签名验证和比较

通过命令行和 Python API 两种方式，可以轻松集成到各种工作流程中。
