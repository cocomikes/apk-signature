# APK Signature - Android APK 签名指纹提取工具

[English README](README.md)

一个强大的 Python 命令行工具，用于提取和分析 Android APK 包的签名指纹（MD5/SHA1/SHA256）。

## 📋 目录

- [为什么需要这个工具](#为什么需要这个工具)
- [核心特性](#核心特性)
- [安装](#安装)
- [快速开始](#快速开始)
- [使用指南](#使用指南)
- [技术原理](#技术原理)
- [常见问题](#常见问题)
- [更新日志](#更新日志)

## 为什么需要这个工具？

在申请微信支付、支付宝支付等第三方服务时，通常需要提交 APK 的签名指纹。获取签名的传统方法存在诸多不便：

### 传统方法的问题

1. **Gen_Signature_Android.apk**
   - 需要安装到 Android 设备
   - 部分手机（如小米）拒绝安装
   - 操作繁琐，不适合批量处理

2. **keytool 命令**
   - Java 8+ 版本不再显示 MD5 指纹
   - 输出格式不够灵活
   - 无法直接比较签名

3. **jadx 反编译工具**
   - 功能过于强大，安装包体积大
   - 仅为查看签名而安装显得"杀鸡用牛刀"

### 本工具的优势

✅ **纯 Python 实现** - 无需 OpenSSL、无需临时文件  
✅ **多种输出格式** - 支持文本、JSON、简洁模式  
✅ **签名验证** - 检查证书有效期和签名算法  
✅ **签名比较** - 快速对比两个 APK 的签名  
✅ **详细信息** - 显示证书主题、颁发者、有效期等  
✅ **高性能** - 直接解析 ZIP 文件，无需解压  
✅ **错误处理** - 友好的错误提示和异常处理  

## 核心特性

### 🎯 功能 1: 支持 APK v1/v2/v3 签名方案

自动识别并解析不同版本的 Android 签名方案：
- **v1 (JAR 签名)**: 传统的 META-INF 签名
- **v2/v3 签名**: Android 7.0+ 引入的 APK Signing Block

### 📊 功能 2: 多种输出格式

```bash
# 文本格式（默认）
apk-signature app.apk

# JSON 格式（便于程序处理）
apk-signature app.apk --format json

# 简洁模式（仅输出指纹）
apk-signature app.apk --only md5
```

### 🔍 功能 3: 证书详细信息

```bash
apk-signature app.apk --verbose
```

显示内容包括：
- 证书主题（Subject）：CN, O, OU, L, ST, C
- 证书颁发者（Issuer）
- 序列号
- 有效期（起始/结束时间）
- 是否过期
- 签名算法

### ✅ 功能 4: 签名验证

```bash
apk-signature app.apk --verify
```

自动检查：
- 证书是否在有效期内
- 是否使用了不安全的签名算法（如 MD5withRSA）
- 签名完整性

### 🔄 功能 5: 签名比较

```bash
apk-signature --compare app1.apk app2.apk
```

快速对比两个 APK 的签名是否相同，适用于：
- 验证不同渠道包的签名一致性
- 检查重新签名后的 APK
- 确认 APK 来源

### ⚡ 功能 6: 无需临时文件

使用 Python 的 `zipfile` 和 `cryptography` 库直接解析：
- 不创建临时目录
- 不依赖外部命令（OpenSSL、unzip）
- 更快、更安全、更可靠

### 🛡️ 功能 7: 完善的错误处理

- 文件不存在时给出明确提示
- 损坏的 APK 文件友好报错
- 未签名的 APK 清晰说明
- 支持 `--debug` 模式查看详细错误

### 🚀 功能 8: 性能优化

- 流式读取 ZIP 文件，支持大文件
- 仅解析必要的证书数据
- 内存占用低
- 处理速度快

## 安装

### 系统要求

- Python 3.7 或更高版本
- pip 包管理器

### 使用 pip 安装（推荐）

```bash
# 检查 Python 版本
python3 --version

# 安装
python3 -m pip install apk-signature

# 验证安装
apk-signature --version
```

### 从源码安装

```bash
# 克隆仓库
git clone https://github.com/floatinghotpot/apk-signature.git
cd apk-signature

# 安装依赖
python3 -m pip install -r requirements.txt

# 开发模式安装
python3 -m pip install -e .
```

## 快速开始

### 基本用法

```bash
# 查看 APK 签名
apk-signature myapp.apk
```

输出示例：
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

## 使用指南

### 1. 查看详细证书信息

```bash
apk-signature myapp.apk --verbose
```

输出包含：
```
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

```bash
apk-signature myapp.apk --format json
```

适合程序化处理：
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
      ...
    },
    ...
  }
}
```

### 3. 仅显示特定指纹

```bash
# 仅显示 MD5（微信支付、支付宝常用）
apk-signature myapp.apk --only md5

# 仅显示 SHA1
apk-signature myapp.apk --only sha1

# 仅显示 SHA256
apk-signature myapp.apk --only sha256
```

### 4. 验证签名有效性

```bash
apk-signature myapp.apk --verify
```

输出示例：
```
签名验证: ✓ 签名有效
```

或：
```
签名验证: ✗ 证书已过期（过期时间: 2020-01-01T00:00:00）
```

### 5. 比较两个 APK 签名

```bash
apk-signature --compare app1.apk app2.apk
```

输出示例：
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

### 6. 在脚本中使用

```bash
#!/bin/bash

# 获取 MD5 签名
MD5=$(apk-signature myapp.apk --only md5)
echo "APK MD5: $MD5"

# 验证签名并检查返回码
if apk-signature myapp.apk --verify > /dev/null 2>&1; then
    echo "签名有效"
else
    echo "签名无效或已过期"
    exit 1
fi

# 比较签名
if apk-signature --compare app1.apk app2.apk > /dev/null 2>&1; then
    echo "签名相同"
else
    echo "签名不同"
    exit 1
fi
```

### 7. Python 代码中使用

```python
from apk_signature.apk_parser import APKParser
from apk_signature.formatter import Formatter

# 解析 APK
parser = APKParser('myapp.apk')
info = parser.parse()

# 获取指纹
print(f"MD5: {info['fingerprints']['md5']}")
print(f"SHA1: {info['fingerprints']['sha1']}")
print(f"SHA256: {info['fingerprints']['sha256']}")

# 验证签名
is_valid, message = parser.verify_signature()
print(f"签名验证: {message}")

# 比较签名
result = APKParser.compare_signatures('app1.apk', 'app2.apk')
print(f"签名相同: {result['identical']}")

# 格式化输出
text_output = Formatter.format_text(info, verbose=True)
json_output = Formatter.format_json(info)
```

## 技术原理

### APK 签名机制

Android APK 使用 PKI（公钥基础设施）进行签名：

1. **开发者生成密钥对**：使用 `keytool` 创建 keystore
2. **签名 APK**：使用私钥对 APK 进行签名
3. **证书嵌入**：公钥证书嵌入到 APK 的 `META-INF/` 目录
4. **验证**：Android 系统使用公钥验证签名

### 签名方案演进

| 方案 | Android 版本 | 特点 |
|------|-------------|------|
| v1 (JAR) | 所有版本 | 基于 ZIP 文件签名，证书在 META-INF/ |
| v2 | 7.0+ (API 24) | APK Signing Block，更快的验证 |
| v3 | 9.0+ (API 28) | 支持密钥轮换 |
| v4 | 11+ (API 30) | 流式安装优化 |

### 本工具的实现

```
APK 文件 (ZIP 格式)
    ↓
读取 META-INF/CERT.RSA (v1 签名)
    ↓
解析 PKCS#7 格式
    ↓
提取 X.509 证书
    ↓
计算 DER 编码的哈希值
    ↓
输出 MD5/SHA1/SHA256 指纹
```

### 为什么不需要 OpenSSL？

旧版本使用 shell 命令调用 OpenSSL：
```bash
openssl pkcs7 -inform DER -in CERT.RSA -print_certs -out CERT.cert
openssl x509 -in CERT.cert -fingerprint -noout -md5
```

新版本使用 Python `cryptography` 库：
```python
from cryptography import x509
from cryptography.hazmat.backends import default_backend

cert = x509.load_der_x509_certificate(cert_data, default_backend())
cert_der = cert.public_bytes(serialization.Encoding.DER)
md5_hash = hashlib.md5(cert_der).hexdigest()
```

优势：
- 跨平台兼容性更好
- 不依赖外部命令
- 更容易处理错误
- 性能更高

## 常见问题

### Q1: 为什么需要 MD5 指纹？

**A:** 虽然 MD5 算法已被认为不够安全，但许多第三方平台（如微信支付、支付宝）仍然使用 MD5 指纹作为应用标识。Java 8+ 的 keytool 不再显示 MD5，因此需要专门的工具。

### Q2: 支持哪些 APK 签名方案？

**A:** 当前版本完整支持 v1 (JAR) 签名，v2/v3 签名的支持正在开发中。大多数 APK 都包含 v1 签名以保持兼容性。

### Q3: 可以处理加固后的 APK 吗？

**A:** 可以。工具会自动查找 `META-INF/` 目录下的所有 `.RSA`、`.DSA`、`.EC` 文件，支持常见的加固方案。

### Q4: 如何验证工具的准确性？

**A:** 可以与 `keytool` 命令对比：
```bash
# 使用 keytool
keytool -printcert -jarfile myapp.apk

# 使用本工具
apk-signature myapp.apk --verbose
```

SHA1 和 SHA256 指纹应该完全一致。

### Q5: 为什么有多种格式的指纹？

**A:** 不同平台要求不同格式：
- **冒号分隔大写** (AA:BB:CC): keytool 默认格式
- **纯大写** (AABBCC): 部分 API 要求
- **纯小写** (aabbcc): 微信、支付宝等平台

### Q6: 工具是否会修改 APK 文件？

**A:** 不会。工具仅读取 APK 文件，不会进行任何修改。

### Q7: 支持批量处理吗？

**A:** 当前版本不直接支持，但可以通过 shell 脚本实现：
```bash
for apk in *.apk; do
    echo "处理: $apk"
    apk-signature "$apk" --only md5
done
```

### Q8: 遇到错误怎么办？

**A:** 使用 `--debug` 参数查看详细错误信息：
```bash
apk-signature myapp.apk --debug
```

常见错误：
- `无效的 APK 文件`: 文件损坏或不是有效的 ZIP
- `未找到有效的签名信息`: APK 未签名或签名格式不支持
- `解析失败`: 证书格式异常

## 更新日志

### v2.0.0 (2024-12-02)

🎉 **重大更新 - 完全重写**

**新增功能：**
- ✨ 支持 APK v1/v2/v3 签名方案识别
- ✨ 多种输出格式（text/json/simple）
- ✨ 证书详细信息显示（--verbose）
- ✨ 签名验证功能（--verify）
- ✨ 签名比较功能（--compare）
- ✨ 纯 Python 实现，无需 OpenSSL
- ✨ 完善的错误处理和提示

**性能优化：**
- ⚡ 无需创建临时文件
- ⚡ 直接解析 ZIP 文件
- ⚡ 内存占用更低
- ⚡ 处理速度更快

**依赖变更：**
- 新增：`cryptography >= 3.4.8`
- 移除：对 OpenSSL 的依赖
- 移除：对 unzip 命令的依赖

### v1.2.0 (2022)

- 支持加固包签名提取
- 添加多种格式输出

### v1.0.0 (2022)

- 初始版本
- 基于 OpenSSL 命令实现

## 开发计划

- [ ] 完整的 v2/v3 签名解析
- [ ] 批量处理多个 APK
- [ ] GUI 图形界面
- [ ] Web API 服务
- [ ] iOS IPA 签名支持
- [ ] AAB (Android App Bundle) 支持

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

本项目采用 GPLv3+ 许可证。详见 [LICENSE](LICENSE) 文件。

## 作者

Raymond Xie (liming.xie@gmail.com)

## 致谢

感谢所有使用和支持本项目的开发者！

---

**如果这个工具对你有帮助，请给个 ⭐ Star！**