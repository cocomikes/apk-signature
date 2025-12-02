# 快速入门指南

5 分钟快速上手 `apk-signature` 工具。

## 1. 安装 (30 秒)

```bash
# 确保 Python 3.7+
python3 --version

# 安装工具
pip install apk-signature

# 验证安装
apk-signature --version
```

## 2. 基本使用 (1 分钟)

### 查看 APK 签名

```bash
apk-signature myapp.apk
```

输出所有格式的指纹（MD5/SHA1/SHA256）。

### 仅获取 MD5（微信/支付宝常用）

```bash
apk-signature myapp.apk --only md5
```

输出：`cde9f6208d672b54b1dacc0b7029f5eb`

## 3. 常用场景 (3 分钟)

### 场景 1: 微信支付接入

```bash
# 获取 MD5 签名
MD5=$(apk-signature myapp.apk --only md5)
echo "微信支付平台填入: $MD5"
```

### 场景 2: 查看证书详情

```bash
apk-signature myapp.apk --verbose
```

显示证书主题、颁发者、有效期等信息。

### 场景 3: 验证签名有效性

```bash
apk-signature myapp.apk --verify
```

检查证书是否过期或使用不安全算法。

### 场景 4: 比较两个 APK

```bash
apk-signature --compare app1.apk app2.apk
```

快速判断两个 APK 签名是否相同。

### 场景 5: JSON 格式输出

```bash
apk-signature myapp.apk --format json > signature.json
```

适合程序化处理。

## 4. 脚本集成 (1 分钟)

### Bash 脚本

```bash
#!/bin/bash

# 获取 MD5
MD5=$(apk-signature myapp.apk --only md5)

# 验证签名
if apk-signature myapp.apk --verify > /dev/null 2>&1; then
    echo "✓ 签名有效: $MD5"
else
    echo "✗ 签名无效"
    exit 1
fi
```

### Python 脚本

```python
from apk_signature.apk_parser import APKParser

# 解析 APK
parser = APKParser('myapp.apk')
info = parser.parse()

# 获取 MD5
md5 = info['fingerprints']['md5']
print(f"MD5: {md5}")

# 验证签名
is_valid, message = parser.verify_signature()
print(f"验证: {message}")
```

## 5. 完整示例

```bash
# 1. 查看基本信息
apk-signature myapp.apk

# 2. 查看详细信息
apk-signature myapp.apk --verbose

# 3. 验证签名
apk-signature myapp.apk --verify

# 4. 获取 MD5（用于第三方平台）
apk-signature myapp.apk --only md5

# 5. JSON 格式（用于程序处理）
apk-signature myapp.apk --format json

# 6. 比较签名（验证渠道包）
apk-signature --compare master.apk channel.apk
```

## 下一步

- 查看 [README.zh.md](README.zh.md) 了解完整功能
- 查看 [EXAMPLES.md](EXAMPLES.md) 了解更多使用示例
- 查看 [CHANGELOG.md](CHANGELOG.md) 了解版本更新

## 常见问题

**Q: 为什么需要 MD5？**  
A: 虽然 MD5 不够安全，但微信支付、支付宝等平台仍使用 MD5 作为应用标识。

**Q: 支持哪些签名方案？**  
A: 完整支持 v1 (JAR) 签名，v2/v3 识别功能开发中。

**Q: 需要安装 OpenSSL 吗？**  
A: 不需要！v2.0 使用纯 Python 实现，无需外部依赖。

**Q: 会修改 APK 文件吗？**  
A: 不会，工具仅读取文件，不做任何修改。

## 获取帮助

```bash
# 查看帮助
apk-signature --help

# 查看版本
apk-signature --version
```

## 反馈

遇到问题？欢迎提交 [Issue](https://github.com/floatinghotpot/apk-signature/issues)！

---

**开始使用吧！** 🚀
