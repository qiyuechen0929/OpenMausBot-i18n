# OpenMausBot i18n / 本地化工具

将 [OpenMausBot](https://github.com/milind-soni/OpenMausBot)（Electron 桌面应用）的界面文案替换为任意支持的语言。

## 原理

OpenMausBot 是一个 Electron 应用，其 UI 由 Next.js 编译为静态资源。本工具直接改写已安装应用 `resources/ui` 目录下的编译产物（纯前端静态 JS/HTML 文件），不改动 `app.asar` 主程序逻辑。

**优势：**
- 风险低：不触碰应用核心逻辑
- 可逆：随时可还原为英文
- 无依赖：纯 Python 实现，无需 Node.js 或 npm

## 支持的语言

| 代码 | 语言 | 说明 |
|------|------|------|
| `zh-CN` | 简体中文 | 内置语言，由项目维护 |
| `zh-TW` | 繁體中文 | 社區維護 |
| `ja-JP` | 日本語 | コミュニティ翻訳 |
| `ko-KR` | 한국어 | 커뮤니티 번역 |
| `es-ES` | Español | Traducción de la comunidad |
| `fr-FR` | Français | Traduction de la communauté |
| `de-DE` | Deutsch | Community-Übersetzung |
| `ru-RU` | Русский | Перевод сообщества |

## 环境要求

- Python 3.8+（无第三方依赖）
- OpenMausBot 桌面应用已安装
- 可选：Node.js（用于 `--check` 语法自检）

## 快速开始

### Windows

双击 `localize.bat`，使用编号菜单操作：
- **1** → 本地化（选择语言）
- **2** → 还原英文
- **3** → 列出可用语言
- **4** → 退出

或直接命令行：
```bash
# 运行并弹出语言选择菜单
python hanhua.py

# 直接指定语言
python hanhua.py --lang zh-CN
python hanhua.py --lang ja-JP
python hanhua.py --lang ru-RU

# 列出所有可用语言
python hanhua.py --list
```

### macOS / Linux

```bash
python3 hanhua.py --dry-run --lang zh-TW   # 先预览
python3 hanhua.py --lang zh-TW             # 再应用
python3 hanhua.py --restore                # 还原英文
```

## 高级用法

### 指定安装目录
```bash
python hanhua.py --path "D:\Programs\openmausbot" --lang fr-FR
```

### 预览模式
```bash
# 只预览，不写入
python hanhua.py --dry-run --lang de-DE

# 预览 + 用 node 校验生成的 JS 语法
python hanhua.py --dry-run --check --lang ru-RU
```

### 还原操作
```bash
# 还原为英文（默认用最早的原始备份）
python hanhua.py --restore

# 从指定备份还原
python hanhua.py --restore --backup 0.1.25-20260820-172245
```

### 不创建备份
```bash
python hanhua.py --no-backup --lang ko-KR
```

## 添加新语言

1. 复制 `locales/zh-CN.json` 为 `locales/<code>.json`（例如 `pt-BR.json`）
2. 填写 `_meta`（`code` / `flag` / `name` / `name_en` / `note`），并翻译所有 value
3. **key 必须与 zh-CN 完全一致**——包括前导空格、弯引号、省略号等字符
4. 校验：
   ```bash
   python hanhua.py --list                    # 确认出现新语言
   python hanhua.py --dry-run --check --lang <code>  # 预览并自检语法
   python tools/validate_dict.py              # 全量校验
   ```

## 工作原理

1. **发现语言**：扫描 `locales/*.json`，读取 `_meta` 生成语言列表
2. **定位应用**：自动检测安装路径（Windows / macOS / Linux），或用 `--path` 手动指定
3. **备份**：复制 `resources/ui` 下待改文件到 `backups/<版本>-<时间戳>/`
4. **替换**：对每个 UI 文件做正则扫描——仅在字符串字面量内替换，边界检查确保不误伤代码
5. **注入**：修改 `index.html` 的 `<html lang>` 属性为目标语言
6. **自检（可选）**：`--check` 调用 `node --check` 验证产物语法

## 安全说明

- 仅改动 `resources/ui` 下的静态 JS/HTML，不触碰 `app.asar`
- 所有 key 在写入前经 `tools/validate_dict.py` 校验为原包子串
- 关键逻辑串（键盘键名、比较常量、JS 类型名等）在词典生成阶段即被排除
- 文件以 UTF-8 无 BOM 写回；每处替换均按原引号类型转义

## 重新生成词典（新版本适配）

当 OpenMausBot 更新版本时，需要重新提取候选字符串：

1. `tools/extract_strings.py`：从 UI 主包提取候选字符串 → `candidates.json`
2. 人工筛选出可翻译 UI 文案，写入 `locales/zh-CN.json`
3. `tools/validate_dict.py`：校验所有语言文件的 key 集与 zh-CN 一致
4. `tools/check_keys.py`：扫描 key 是否以危险方式出现，命中则剔除
5. `tools/verify_lang.py <code>`：对已安装 UI 做幂等性校验

## 目录结构

```
OpenMausBot-i18n/
├── hanhua.py              # 主脚本（多语言，含交互式选择器）
├── localize.bat           # Windows 批处理脚本
├── locales/               # 语言词典目录
│   ├── zh-CN.json         # 基准词典（key 以此为准）
│   ├── zh-TW.json
│   ├── ja-JP.json
│   ├── ko-KR.json
│   ├── es-ES.json
│   ├── fr-FR.json
│   ├── de-DE.json
│   └── ru-RU.json
├── tools/                 # 提取与校验工具
│   ├── extract_strings.py
│   ├── validate_dict.py
│   ├── check_keys.py
│   └── verify_lang.py
├── backups/               # （运行时生成）备份
├── LICENSE
└── README.md
```

## 常见问题

| 问题 | 解决 |
|------|------|
| `OpenMausBot not found` | 用 `--path` 指定安装目录 |
| `Cannot write ...` | 应用正在运行，先退出 OpenMausBot 再执行 |
| 替换数量为 0 | 应用可能已被汉化，或版本不匹配需重新生成词典 |
| `--check` 显示需 node | 安装 Node.js 后重试，或省略 `--check` |
| 想恢复英文 | `python hanhua.py --restore`，重启应用 |
| 换语言时旧译文残留 | 先 `--restore` 还原英文，再 `--lang <code>` 应用新语言 |

## 当前版本

- 支持 OpenMausBot **v0.1.29**
- 886 个翻译键
- 1225 个替换点

## License

MIT
