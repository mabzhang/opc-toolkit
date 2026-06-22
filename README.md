# OPC Toolkit

一套可移植的中文品牌营销 Agent Skills 工具包。

[![Validate](https://github.com/mabzhang/opc-toolkit/actions/workflows/validate.yml/badge.svg)](https://github.com/mabzhang/opc-toolkit/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

OPC Toolkit 使用 1 个智能路由器和 10 个专业技能，把零散营销需求转化为需求卡、研究洞察、Campaign、内容方案、客户提案和执行任务单。

## 它解决什么问题

- 把 Brief、聊天记录和会议纪要整理为统一需求。
- 根据任务自动选择最合适的营销工作流。
- 研究竞品、消费者、内容、渠道和平台要求。
- 生成客户可读的正式营销方案。
- 把策略继续拆成负责人、排期、依赖和验收标准。
- 区分事实、推断、假设和待验证信息。

## 包含的技能

| Skill | 用途 |
|---|---|
| `$opc-toolkit` | 智能总入口与工作流路由 |
| `$opc-proposal` | 完整品牌营销全案编排 |
| `$brief-analysis` | Brief、聊天和会议纪要归一 |
| `$competitor-analysis` | 竞品定位、内容、渠道和机会研究 |
| `$consumer-insight` | 人群、购买障碍和内容触发洞察 |
| `$campaign-planning` | Campaign 策略、主题和传播节奏 |
| `$social-media-plan` | 多平台内容矩阵与内容日历 |
| `$platform-adaptation` | 抖音、小红书、微信等平台原生改写 |
| `$platform-specs` | 当前素材尺寸、格式和安全区核验 |
| `$marketing-proposal` | 客户可读的正式营销提案 |
| `$task-decomposition` | 任务、负责人、依赖、排期和验收 |

## 典型工作流

```text
完整全案：
brief-analysis
  → competitor-analysis + consumer-insight
  → campaign-planning
  → marketing-proposal
  → task-decomposition

社媒运营：
brief-analysis
  → consumer-insight
  → social-media-plan
  → platform-adaptation
```

单一明确任务只调用对应技能，不会被强制扩张为完整全案。

## 安装

推荐从 [Releases](https://github.com/mabzhang/opc-toolkit/releases) 下载最新安装包。

也可以直接克隆仓库：

```bash
git clone https://github.com/mabzhang/opc-toolkit.git
cd opc-toolkit
```

### macOS / Linux

```bash
# Codex
./install.sh --agent codex --global

# Claude Code
./install.sh --agent claude --global

# Cursor
./install.sh --agent cursor --global

# GitHub Copilot
./install.sh --agent copilot --global

# Gemini CLI
./install.sh --agent gemini --global

# 通用 Agent Skills
./install.sh --agent agents --global
```

### Windows 或没有 Bash 的环境

```powershell
python install.py --agent codex --global
python install.py --agent cursor --project C:\path\to\project
python install.py --target C:\path\to\agent\skills
```

安装到项目而不是全局环境：

```bash
./install.sh --agent cursor --project /path/to/project
```

安装后请新开一个 Agent 会话，让宿主重新加载技能。

## 第一次使用

```text
用 $opc-toolkit 处理下面这项营销任务。
请先判断正确的工作流，再完成交付；
事实、假设和待确认项要分开。
```

任务明确时可以直接点名：

```text
用 $competitor-analysis 分析三个竞品的定位、价格带、
抖音/小红书内容与 KOL 生态，并给出可攻击的市场空白。
```

## 安全更新和诊断

```bash
./install.sh --list
./install.sh --dry-run --agent codex
./install.sh --doctor --agent codex
python install.py --doctor --agent codex
```

安装器会先验证包结构，再暂存和替换文件。更新已有 Skill 时默认保留备份；重复安装相同版本会自动跳过。

## 支持的 Agent 目录

| Agent | 全局目录 | 项目目录 |
|---|---|---|
| Codex | `~/.codex/skills` | `<project>/.codex/skills` |
| Claude Code | `~/.claude/skills` | `<project>/.claude/skills` |
| Cursor | `~/.cursor/skills` | `<project>/.cursor/skills` |
| GitHub Copilot | `~/.copilot/skills` | `<project>/.github/skills` |
| Gemini CLI | `~/.gemini/skills` | `<project>/.gemini/skills` |
| 通用 Agent Skills | `~/.agents/skills` | `<project>/.agents/skills` |

项目同时包含 Codex 和 Claude Code 插件清单。跨 Agent 分发时，推荐使用安装器。

## 开发和验证

```bash
python3 scripts/validate_bundle.py
bash scripts/smoke_test.sh
python3 scripts/build_release.py --output-dir dist
```

GitHub Actions 会在每次 Push 和 Pull Request 时自动运行结构校验与安装冒烟测试。

## 隐私与内容边界

不要把以下内容提交到公开仓库、Issue 或 Pull Request：

- API Key、Token、密码和私钥；
- 客户 Brief、聊天记录、会议纪要和未公开方案；
- 个人信息、用户数据和付费报告原文；
- 未经授权的品牌案例、图片、字体和第三方素材。

涉及价格、平台规则、达人、政策、合规和竞品近期动作时，应在实际使用时重新核验，不要把旧信息当成永久事实。

## 参与贡献

请阅读 [CONTRIBUTING.md](CONTRIBUTING.md) 和 [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)。

发现安全或隐私问题时，请先阅读 [SECURITY.md](SECURITY.md)，不要直接在公开 Issue 中粘贴敏感信息。

## License

本项目采用 [MIT License](LICENSE) 开源。

你可以学习、修改、分发和商用，但需要保留版权与许可证声明。项目按现状提供，不承诺适用于任何特定用途。
