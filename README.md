# Download Organizer (Python 下载文件夹自动整理工具)

简体中文版本在后面

A lightweight Python tool to automatically organize your **Downloads** folder using **configurable rules** (YAML).  
Supports **one-shot organizing** and a **watch mode** that runs in the background and avoids moving files that are still downloading.

## Features

- Rule-based organization via **YAML config**
- **Watch mode** (`--watch`) to organize automatically when files change
- Avoids moving unfinished downloads:
  - Ignores common temporary extensions (e.g. `.crdownload`, `.part`, `.tmp`, `.aria2`)
  - Optional **file stability check** (size + mtime unchanged for N seconds)
- **Dry run** (`--dry-run`) to preview actions without moving files
- Automatic handling of name conflicts (adds ` (1)`, ` (2)` ... suffix)
- Optional logging to file (`--log-file`) — recommended when running with `pythonw.exe` / background

## Requirements

- Python 3.10+ (recommended)
- Windows/macOS/Linux
- Dependencies:
  - `PyYAML`
  - `watchdog` (only required for `--watch` mode)

## Installation

### 1) Clone

```bash
git clone https://github.com/<your-username>/Download_Organizer.git
cd Download_Organizer
```

### 2) Create a virtual environment

**Windows (PowerShell):**
```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3) Install dependencies

```bash
pip install -r requirements.txt
```

If you don't have a `requirements.txt` yet, install manually:
```bash
pip install pyyaml watchdog
```

## Configuration (YAML)

Create a config file, for example: `configs/rules.yaml`

Example:

```yaml
download_dir: "your_path/Downloads"
destination_root: "your_path/Downloads/Sorted"

ignore_extensions:
  - ".crdownload"
  - ".part"
  - ".tmp"
  - ".download"
  - ".opdownload"
  - ".!qB"
  - ".aria2"

rules:
  - name: "Images"
    extensions: [".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp"]
    target: "Images"

  - name: "Videos"
    extensions: [".mp4", ".mkv", ".mov", ".avi", ".webm"]
    target: "Videos"

  - name: "Documents"
    extensions: [".pdf", ".docx", ".doc", ".pptx", ".xlsx", ".md", ".txt"]
    target: "Documents"

  - name: "Archives"
    extensions: [".zip", ".rar", ".7z", ".tar", ".gz"]
    target: "Archives"

  - name: "Installers"
    extensions: [".exe", ".msi"]
    target: "Installers"

  - name: "CatchAll"
    extensions: ["*"]
    target: "Others"
```

### Notes

- Rules are matched top-to-bottom; the **first match wins**
- `extensions: ["*"]` is a catch-all fallback
- Prefer forward slashes (`C:/...`) on Windows to avoid escaping issues

## Usage

### One-shot organize (recommended first run)

Preview actions:
```bash
python -m organizer.cli --config configs/rules.yaml --dry-run --verbose
```

Apply changes:
```bash
python -m organizer.cli --config configs/rules.yaml --verbose
```

### Watch mode (auto-organize)

Dry run watch:
```bash
python -m organizer.cli --config configs/rules.yaml --watch --dry-run --verbose
```

Actual watch:
```bash
python -m organizer.cli --config configs/rules.yaml --watch --verbose
```

### Stability tuning (avoid moving files still being written)

- `--stable-seconds`: how long the file must remain unchanged before moving
- `--debounce-seconds`: reduce repeated triggers during heavy download activity

Example:
```bash
python -m organizer.cli --config configs/rules.yaml --watch --stable-seconds 4 --debounce-seconds 2 --verbose
```

### Logging to file (useful for background mode)

```bash
python -m organizer.cli --config configs/rules.yaml --watch --log-file logs/watcher.log --verbose
```

## Run silently on Windows at login (Task Scheduler + pythonw.exe)

If you want the organizer to run in the background **without a console window**:

1. Open **Task Scheduler** → **Create Task...**
2. **General**:
   - Select **Run only when user is logged on**
   - (Optional) check **Run with highest privileges**
3. **Triggers**:
   - **At log on** (optionally delay 30 seconds)
4. **Actions** → **Start a program**:
   - Program/script:
     - `your_path\Download_Organizer\.venv\Scripts\pythonw.exe`
   - Add arguments:
     - `-m organizer.cli --config "your_path\1AMainProjects\Download_Organizer\configs\rules.yaml" --watch --log-file "your_path\Download_Organizer\logs\watcher.log" --verbose`
   - Start in:
     - `your_path\Download_Organizer`

Check logs at:
- `logs/watcher.log`

## Project Structure

```text
Download_Organizer/
  organizer/
    cli.py
    config.py
    organizer.py
    rules.py
    utils.py
    watch.py
  configs/
    rules.example.yaml
```

## Roadmap ideas

- More match types (regex filename, min/max size, date ranges)
- "Move only when download finished" integration for specific browsers/download managers
- Packaging as a standalone executable (PyInstaller)
- GUI configuration editor

## Contributing

PRs and issues are welcome!  
If you report a bug, please include:

- your OS + Python version
- your config file (remove sensitive paths if needed)
- relevant log output (`--log-file`)

---

## 简体中文版本

一个轻量的 Python 工具，用**可配置规则（YAML）**自动整理 **Downloads/下载** 文件夹。  
支持**单次整理**与**监听模式（watch）**，并尽量避免移动“仍在下载/写入中”的文件。

## 功能特性

- 使用 **YAML 配置**自定义整理规则
- **监听模式**（`--watch`）：文件夹有变化就自动整理
- 避免移动未完成下载：
  - 忽略常见临时扩展名（如 `.crdownload`、`.part`、`.tmp`、`.aria2` 等）
  - 可选 **文件稳定性检测**（大小 + 修改时间在 N 秒内不变才移动）
- **干跑预览**（`--dry-run`）：只打印将执行的操作，不实际移动
- 同名冲突自动处理：自动加 ` (1)`、` (2)`… 后缀
- 支持写入日志文件（`--log-file`）——配合 `pythonw.exe` 后台运行尤其推荐

## 环境要求

- Python 3.10+（推荐）
- Windows/macOS/Linux
- 依赖：
  - `PyYAML`
  - `watchdog`（仅 `--watch` 监听模式需要）

## 安装

### 1) 克隆仓库

```bash
git clone https://github.com/<your-username>/Download_Organizer.git
cd Download_Organizer
```

### 2) 创建虚拟环境

**Windows（PowerShell）：**

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS/Linux：**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3) 安装依赖

```bash
pip install -r requirements.txt
```

如果你还没有 `requirements.txt`，也可以手动安装：
```bash
pip install pyyaml watchdog
```

## 配置说明（YAML）

创建配置文件，例如：`configs/rules.yaml`

示例：

```yaml
download_dir: "your_path/Downloads"
destination_root: "your_path/Downloads/Sorted"

ignore_extensions:
  - ".crdownload"
  - ".part"
  - ".tmp"
  - ".download"
  - ".opdownload"
  - ".!qB"
  - ".aria2"

rules:
  - name: "Images"
    extensions: [".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp"]
    target: "Images"

  - name: "Videos"
    extensions: [".mp4", ".mkv", ".mov", ".avi", ".webm"]
    target: "Videos"

  - name: "Documents"
    extensions: [".pdf", ".docx", ".doc", ".pptx", ".xlsx", ".md", ".txt"]
    target: "Documents"

  - name: "Archives"
    extensions: [".zip", ".rar", ".7z", ".tar", ".gz"]
    target: "Archives"

  - name: "Installers"
    extensions: [".exe", ".msi"]
    target: "Installers"

  - name: "CatchAll"
    extensions: ["*"]
    target: "Others"
```

### 配置要点

- 规则从上到下匹配：**命中第一条规则就执行**
- `extensions: ["*"]` 表示兜底规则（建议保留）
- Windows 路径建议用正斜杠 `C:/...`，减少转义问题

## 使用方法

### 单次整理（建议首次先 dry-run）

预览将要执行的移动操作：
```bash
python -m organizer.cli --config configs/rules.yaml --dry-run --verbose
```

确认无误后执行移动：
```bash
python -m organizer.cli --config configs/rules.yaml --verbose
```

### 监听模式（自动整理）

监听模式（先 dry-run 观察）：
```bash
python -m organizer.cli --config configs/rules.yaml --watch --dry-run --verbose
```

实际运行：
```bash
python -m organizer.cli --config configs/rules.yaml --watch --verbose
```

### 稳定性参数调优（避免移动仍在写入中的文件）

- `--stable-seconds`：文件必须“稳定不变”的秒数（越大越稳，越小越快）
- `--debounce-seconds`：事件防抖（下载器频繁触发变更时建议调大）

示例：
```bash
python -m organizer.cli --config configs/rules.yaml --watch --stable-seconds 4 --debounce-seconds 2 --verbose
```

### 写日志到文件（后台运行必备）

```bash
python -m organizer.cli --config configs/rules.yaml --watch --log-file logs/watcher.log --verbose
```

日志默认追加写入，方便排查问题。

## Windows：登录后静默后台运行（任务计划程序 + pythonw.exe）

想要“登录后自动运行、且不弹黑色控制台窗口”，推荐用 `pythonw.exe`：

1. 打开 **任务计划程序** → **创建任务…**
2. **常规**：
   - 选择 **仅当用户登录时运行**
   -（可选）勾选 **使用最高权限运行**
3. **触发器**：
   - **登录时**
   -（可选）延迟 30 秒
4. **操作** → **启动程序**：
   - 程序或脚本：
     - `your_path\Download_Organizer\.venv\Scripts\pythonw.exe`
   - 添加参数：
     - `-m organizer.cli --config "your_path\Download_Organizer\configs\rules.yaml" --watch --log-file "your_path\Download_Organizer\logs\watcher.log" --verbose`
   - 起始于：
     - `your_path\Download_Organizer`

运行后查看日志：
- `logs/watcher.log`

## 项目结构

```text
Download_Organizer/
  organizer/
    cli.py
    config.py
    organizer.py
    rules.py
    utils.py
    watch.py
  configs/
    rules.example.yaml
```

## 后续可扩展方向（Roadmap）

- 更多匹配条件（文件名正则、大小范围、时间范围等）
- 针对特定浏览器/下载器的“下载完成检测”更深度适配
- 打包成可执行文件（PyInstaller）
- GUI 配置编辑器

## 贡献方式

欢迎提 Issue / PR。提交 Bug 时建议附上：

- 操作系统与 Python 版本
- 你的配置文件（可删减/脱敏路径）
- 相关日志（建议使用 `--log-file` 输出）
