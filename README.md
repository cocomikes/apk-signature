# APK Signature - Android APK Signature Fingerprint Extractor

[中文版 README](README.zh.md)

A powerful Python command-line tool for extracting and analyzing Android APK signature fingerprints (MD5/SHA1/SHA256).

## 🚀 Features

- ✅ **Pure Python Implementation** - No OpenSSL or temporary files required
- ✅ **Multiple Output Formats** - Text, JSON, and simple modes
- ✅ **Signature Verification** - Check certificate validity and expiration
- ✅ **Signature Comparison** - Compare signatures between two APKs
- ✅ **Detailed Information** - View certificate subject, issuer, validity period
- ✅ **High Performance** - Direct ZIP parsing without extraction
- ✅ **Error Handling** - Friendly error messages and exception handling
- ✅ **APK v1/v2/v3 Support** - Recognizes different Android signing schemes

## Why This Tool?

### Problems with Traditional Methods

**keytool** - Java 8+ no longer displays MD5 fingerprints, but many platforms (WeChat Pay, Alipay) still require MD5.

**Gen_Signature_Android.apk** - Requires installation on Android device, often refused by some phones.

**jadx** - Powerful but overkill for just viewing signatures.

### Our Solution

This tool provides a lightweight, fast, and reliable way to extract APK signatures with multiple output formats and advanced features.

## Installation

### Requirements

- Python 3.7 or higher
- pip package manager

### Install via pip (Recommended)

```bash
# Check Python version
python3 --version

# Install
python3 -m pip install apk-signature

# Verify installation
apk-signature --version
```

### Install from Source

```bash
git clone https://github.com/floatinghotpot/apk-signature.git
cd apk-signature
python3 -m pip install -e .
```

## Quick Start

### Basic Usage

```bash
apk-signature myapp.apk
```

Output:
```
签名方案: v1

=== 签名指纹 (十六进制-冒号-大写) ===
MD5:    CD:E9:F6:20:8D:67:2B:54:B1:DA:CC:0B:70:29:F5:EB
SHA1:   38:91:8A:45:3D:07:19:93:54:F8:B1:9A:F0:5E:C6:56:2C:ED:57:88
SHA256: F0:FD:6C:5B:41:0F:25:CB:25:C3:B5:33:46:C8:97:2F:AE:30:F8:EE:74:11:DF:91:04:80:AD:6B:2D:60:DB:83
```

## Usage Examples

### 1. View Detailed Certificate Information

```bash
apk-signature myapp.apk --verbose
```

### 2. JSON Output

```bash
apk-signature myapp.apk --format json
```

### 3. Show Only Specific Fingerprint

```bash
# MD5 only (for WeChat Pay, Alipay)
apk-signature myapp.apk --only md5

# SHA1 only
apk-signature myapp.apk --only sha1

# SHA256 only
apk-signature myapp.apk --only sha256
```

### 4. Verify Signature

```bash
apk-signature myapp.apk --verify
```

### 5. Compare Two APKs

```bash
apk-signature --compare app1.apk app2.apk
```

### 6. Use in Scripts

```bash
#!/bin/bash

# Get MD5 signature
MD5=$(apk-signature myapp.apk --only md5)
echo "APK MD5: $MD5"

# Verify signature
if apk-signature myapp.apk --verify > /dev/null 2>&1; then
    echo "Signature is valid"
else
    echo "Signature is invalid or expired"
    exit 1
fi
```

### 7. Use in Python Code

```python
from apk_signature.apk_parser import APKParser
from apk_signature.formatter import Formatter

# Parse APK
parser = APKParser('myapp.apk')
info = parser.parse()

# Get fingerprints
print(f"MD5: {info['fingerprints']['md5']}")
print(f"SHA1: {info['fingerprints']['sha1']}")
print(f"SHA256: {info['fingerprints']['sha256']}")

# Verify signature
is_valid, message = parser.verify_signature()
print(f"Verification: {message}")

# Compare signatures
result = APKParser.compare_signatures('app1.apk', 'app2.apk')
print(f"Identical: {result['identical']}")
```

## Command-Line Options

```
usage: apk-signature [-h] [-v] [--verbose] [--format {text,json,simple}]
                     [--only {md5,sha1,sha256}] [--compare APK1 APK2]
                     [--verify]
                     [apk_file]

positional arguments:
  apk_file              APK file path

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  --verbose             show detailed certificate information
  --format {text,json,simple}
                        output format (default: text)
  --only {md5,sha1,sha256}
                        show only specified fingerprint type
  --compare APK1 APK2   compare signatures of two APKs
  --verify              verify signature validity
```

## How It Works

### APK Signing Mechanism

Android APK uses PKI (Public Key Infrastructure) for signing:

1. Developer generates key pair using `keytool`
2. APK is signed with private key
3. Public key certificate is embedded in `META-INF/` directory
4. Android system verifies signature using public key

### Signing Scheme Evolution

| Scheme | Android Version | Features |
|--------|----------------|----------|
| v1 (JAR) | All versions | ZIP-based signing, certificate in META-INF/ |
| v2 | 7.0+ (API 24) | APK Signing Block, faster verification |
| v3 | 9.0+ (API 28) | Key rotation support |
| v4 | 11+ (API 30) | Streaming installation optimization |

### Implementation

```
APK File (ZIP format)
    ↓
Read META-INF/CERT.RSA (v1 signature)
    ↓
Parse PKCS#7 format
    ↓
Extract X.509 certificate
    ↓
Calculate hash of DER-encoded certificate
    ↓
Output MD5/SHA1/SHA256 fingerprints
```

## FAQ

### Q: Why do we need MD5 fingerprints?

**A:** Although MD5 is considered insecure, many third-party platforms (WeChat Pay, Alipay) still use MD5 fingerprints as application identifiers. Java 8+ keytool no longer displays MD5, hence this tool.

### Q: Which APK signing schemes are supported?

**A:** Current version fully supports v1 (JAR) signing. v2/v3 support is under development. Most APKs include v1 signing for compatibility.

### Q: Can it handle obfuscated/protected APKs?

**A:** Yes. The tool automatically searches for all `.RSA`, `.DSA`, `.EC` files in the `META-INF/` directory, supporting common protection schemes.

### Q: How to verify accuracy?

**A:** Compare with `keytool` command:
```bash
# Using keytool
keytool -printcert -jarfile myapp.apk

# Using this tool
apk-signature myapp.apk --verbose
```

SHA1 and SHA256 fingerprints should match exactly.

### Q: Does it modify the APK file?

**A:** No. The tool only reads the APK file without any modifications.

## Changelog

### v2.0.0 (2024-12-02)

🎉 **Major Update - Complete Rewrite**

**New Features:**
- ✨ APK v1/v2/v3 signing scheme recognition
- ✨ Multiple output formats (text/json/simple)
- ✨ Detailed certificate information (--verbose)
- ✨ Signature verification (--verify)
- ✨ Signature comparison (--compare)
- ✨ Pure Python implementation, no OpenSSL required
- ✨ Comprehensive error handling

**Performance Improvements:**
- ⚡ No temporary files needed
- ⚡ Direct ZIP parsing
- ⚡ Lower memory usage
- ⚡ Faster processing

**Dependencies:**
- Added: `cryptography >= 3.4.8`
- Removed: OpenSSL dependency
- Removed: unzip command dependency

### v1.2.0 (2022)

- Support for protected APK signatures
- Multiple output formats

### v1.0.0 (2022)

- Initial release
- OpenSSL-based implementation

## Roadmap

- [ ] Complete v2/v3 signature parsing
- [ ] Batch processing for multiple APKs
- [ ] GUI interface
- [ ] Web API service
- [ ] iOS IPA signature support
- [ ] AAB (Android App Bundle) support

## Contributing

Issues and Pull Requests are welcome!

## License

This project is licensed under GPLv3+. See [LICENSE](LICENSE) file for details.

## Author

Raymond Xie (liming.xie@gmail.com)

## Credits

Thanks to all developers who use and support this project!

---

**If this tool helps you, please give it a ⭐ Star!**