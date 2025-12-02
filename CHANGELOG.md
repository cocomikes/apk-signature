# 更新日志

本文档记录了 apk-signature 项目的所有重要变更。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [2.0.0] - 2024-12-02

### 🎉 重大更新 - 完全重写

这是一个重大版本更新，完全重写了核心代码，提供了更强大的功能和更好的性能。

### 新增 (Added)

- ✨ **APK v1/v2/v3 签名方案支持**: 自动识别不同版本的 Android 签名方案
- ✨ **多种输出格式**: 支持 text、json、simple 三种输出格式
- ✨ **证书详细信息**: 使用 `--verbose` 查看完整的证书信息
  - 证书主题（Subject）
  - 证书颁发者（Issuer）
  - 序列号
  - 有效期（起始/结束时间）
  - 是否过期
  - 签名算法
- ✨ **签名验证功能**: 使用 `--verify` 检查证书有效性
  - 检查证书是否过期
  - 检查是否使用不安全的签名算法
- ✨ **签名比较功能**: 使用 `--compare` 对比两个 APK 的签名
  - 快速判断签名是否相同
  - 显示详细的对比结果
- ✨ **纯 Python 实现**: 不再依赖外部命令
  - 使用 `cryptography` 库解析证书
  - 使用 `zipfile` 直接读取 APK
- ✨ **完善的错误处理**: 友好的错误提示和异常处理
  - 文件不存在提示
  - 损坏的 APK 文件提示
  - 未签名的 APK 提示
- ✨ **Python API**: 可以在 Python 代码中直接使用
  - `APKParser` 类用于解析 APK
  - `Formatter` 类用于格式化输出
- ✨ **详细文档**: 新增多个文档文件
  - `EXAMPLES.md`: 详细的使用示例
  - `CHANGELOG.md`: 更新日志
  - 更新的 `README.md` 和 `README.zh.md`

### 改进 (Changed)

- ⚡ **性能优化**: 无需创建临时文件
  - 直接解析 ZIP 文件
  - 内存占用更低
  - 处理速度更快
- 🔧 **命令行参数**: 使用 `argparse` 提供更好的参数解析
  - 更清晰的帮助信息
  - 更灵活的参数组合
- 📝 **输出格式**: 改进了输出格式的可读性
  - 更清晰的分组
  - 更友好的提示信息
  - 支持 Unicode 符号（✓ ✗）

### 移除 (Removed)

- ❌ **OpenSSL 依赖**: 不再需要安装 OpenSSL
- ❌ **unzip 依赖**: 不再需要 unzip 命令
- ❌ **临时文件**: 不再创建 `./tmp` 目录
- ❌ **Shell 命令**: 不再使用 `subprocess` 执行外部命令

### 依赖变更 (Dependencies)

- ➕ 新增: `cryptography >= 3.4.8`
- ➖ 移除: 对 OpenSSL 的依赖
- ➖ 移除: 对 unzip 的依赖

### 破坏性变更 (Breaking Changes)

- 命令行参数格式有所变化
  - 旧版: `apk-signature myapp.apk`（仅此一种用法）
  - 新版: 支持多种参数组合（`--verbose`, `--format`, `--only`, `--compare`, `--verify`）
- 输出格式有所变化
  - 旧版: 使用 echo 输出简单文本
  - 新版: 使用结构化的格式化输出
- Python 版本要求
  - 旧版: Python 3.7+
  - 新版: Python 3.7+（保持不变，但推荐 3.8+）

### 迁移指南

如果你从 v1.x 升级到 v2.0，请注意以下变化：

#### 1. 基本用法保持兼容

```bash
# v1.x 和 v2.0 都支持
apk-signature myapp.apk
```

#### 2. 输出格式变化

v1.x 输出：
```
Extracting APK: /path/to/myapp.apk ...
--- Signature in upper case ---
md5 Fingerprint=CD:E9:F6:20:8D:67:2B:54:B1:DA:CC:0B:70:29:F5:EB
...
```

v2.0 输出：
```
签名方案: v1

=== 签名指纹 (十六进制-冒号-大写) ===
MD5:    CD:E9:F6:20:8D:67:2B:54:B1:DA:CC:0B:70:29:F5:EB
...
```

#### 3. 获取特定指纹

v1.x: 需要解析输出文本
```bash
apk-signature myapp.apk | grep "MD5(stdin)" | cut -d'=' -f2
```

v2.0: 使用 `--only` 参数
```bash
apk-signature myapp.apk --only md5
```

#### 4. 不再需要安装 OpenSSL

v1.x: 需要先安装 OpenSSL
```bash
brew install openssl  # macOS
```

v2.0: 只需要 Python 和 pip
```bash
pip install apk-signature
```

## [1.2.0] - 2022

### 新增

- 支持加固包签名提取
  - 自动处理 `META-INF/*.RSA` 文件
- 添加多种格式输出
  - 大写带冒号格式
  - 大写纯十六进制格式
  - 小写纯十六进制格式

### 改进

- 改进了错误处理
- 优化了命令执行流程

## [1.0.0] - 2022

### 新增

- 🎉 初始版本发布
- 基于 OpenSSL 命令实现
- 支持提取 MD5/SHA1/SHA256 指纹
- 支持 v1 (JAR) 签名方案
- 命令行工具
- 发布到 PyPI

### 功能

- 从 APK 提取签名证书
- 计算 MD5/SHA1/SHA256 指纹
- 多种格式输出
- 简单易用的命令行界面

---

## 版本说明

### 版本号规则

本项目遵循 [语义化版本 2.0.0](https://semver.org/lang/zh-CN/)：

- **主版本号 (MAJOR)**: 不兼容的 API 变更
- **次版本号 (MINOR)**: 向下兼容的功能性新增
- **修订号 (PATCH)**: 向下兼容的问题修正

### 版本状态

- **2.0.0**: 当前稳定版本 ✅
- **1.2.0**: 旧版本（不再维护）
- **1.0.0**: 旧版本（不再维护）

### 升级建议

- 从 v1.x 升级到 v2.0: **强烈推荐**
  - 更好的性能
  - 更多的功能
  - 更好的错误处理
  - 不依赖外部命令
  
- 如果你依赖 v1.x 的输出格式，可以：
  - 使用 v2.0 的 `--only` 参数获取纯指纹
  - 使用 v2.0 的 `--format json` 进行程序化处理

## 未来计划

### v2.1.0 (计划中)

- [ ] 完整的 v2/v3 签名解析
- [ ] 批量处理多个 APK
- [ ] 性能进一步优化
- [ ] 更多的输出格式选项

### v2.2.0 (计划中)

- [ ] GUI 图形界面
- [ ] Web API 服务
- [ ] 插件系统

### v3.0.0 (未来)

- [ ] iOS IPA 签名支持
- [ ] AAB (Android App Bundle) 支持
- [ ] 签名修改功能
- [ ] 证书生成功能

## 贡献

欢迎提交 Issue 和 Pull Request！

如果你发现了 bug 或有功能建议，请在 [GitHub Issues](https://github.com/floatinghotpot/apk-signature/issues) 中提出。

## 许可证

本项目采用 GPLv3+ 许可证。详见 [LICENSE](LICENSE) 文件。
