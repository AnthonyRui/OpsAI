# OpsAI

**OpsAI helps data-center operators decide which servers need attention and what evidence to check next.** The project spans two semesters: first a monitoring and explanation application, then an agent that investigates incidents using controlled diagnostic tools.

OpsAI 面向数据中心运维人员。第一学期回答“哪台服务器需要关注，依据是什么？”；第二学期回答“还应检查哪些指标、事件和文档，才能缩小可能原因的范围？”已有 GPU 容量规划模块独立回答“给定设施功率和设备配置，能部署多少 GPU？”

## Project roadmap / 项目总计划

**当前阶段（2026-11-09）：** 已有本地可运行的 CPU 规则示例和容量规划工具。年底目标是交付可公开演示、可复现的 Project 1；这是开发目标，目前尚无已部署的运维网页。Project 2 是第二学期计划。

### Semester 1 · Project 1 — 服务器运行分析与 AI 辅助解释

目标流程：运维人员导入数据 → 查看服务器趋势 → 定位持续高负载时段 → 查看触发依据和 AI 解释 → 导出调查摘要。没有密钥或 AI 服务不可用时，基础分析仍应可用。

| 阶段 | 状态 | 交付物与验收方法 |
| --- | --- | --- |
| 1. 确定问题与基线 | 本地示例完成 | [提案](project-1/proposal.md)、[架构图](docs/architecture.md)、[数据约定](docs/operational-data.md)、模拟 CSV、规则与趋势图。用已知案例验证持续高负载、短尖峰和数据缺口。 |
| 2. 数据导入与网页 | 已有本地 CSV 校验；网页待开发 | 支持示例和用户 CSV；检查时间、单位、缺失与重复记录。用户能从服务器列表找到被标记的时段、持续时间和原始读数；错误输入得到具体提示。 |
| 3. AI 解释与效果比较 | 待开发 | 将规则输出作为证据，解释为什么需要关注、还有哪些信息不足。对同一组固定案例比较“只看规则”和“规则加 AI”：检查服务器和时间定位、无依据说法、调查用时及失败案例。 |
| 4. 演示、部署与交付 | 待开发 | 发布可访问的演示网址、示例报告、安装说明、截图、测试和评估记录、稳定版本及两分钟演示。让另一位使用者从示例数据独立复现结果。 |

第一版只选择 CPU 时序数据。当前示例把连续三个五分钟区间的平均 CPU 使用率均达到 85% 标为持续高负载；这是演示规则，不是通用故障标准。后续选取来源和使用权限明确的运营数据，再评估误报与漏报。没有可靠标签时，不报告真实故障识别率。

### Semester 2 · Project 2 — 可调用诊断工具的事件调查 Agent

目标流程：收到事件 → Agent 选择允许使用的只读工具 → 查询相关时间段的指标与事件记录 → 检索技术文档 → 返回可能原因、对应证据和下一步检查建议，交由运维人员判断。

| 阶段 | 状态 | 交付物与验收方法 |
| --- | --- | --- |
| 1. 复盘并确定调查场景 | 计划中 | 保持 Project 1 可用，记录其失败案例、技术债和数据缺口；选定一个可取得指标、事件记录和文档的场景，补齐[第二项目提案](project-2/proposal.md)。 |
| 2. 实现受控调查 | 计划中 | 为每个工具定义输入、输出、权限和错误处理。Agent 返回结构化结果，区分观测事实、可能原因和建议；查询失败、无文档或证据矛盾时明确说明。 |
| 3. 部署与端到端演示 | 计划中 | 用完整案例展示输入、工具调用、检索证据和建议。提供公开演示、自动测试、CI、部署说明及可复现的案例记录。 |
| 4. 评估与发布 | 计划中 | 同时复查两个项目；记录检索失败、错误归因、无依据结论、响应时间、估算调用成本及失败率。检查密钥、输入校验和工具权限，修复关键问题后发布。 |

### Capacity planning / 已有容量模块如何接入

保留当前 Python 计算、CLI、图表和原始 baseline。计划在网页中设独立的“容量规划”入口，复用已有接口，在相同输入下返回与独立工具一致的结果。运营分析发现 CPU 高负载时，不自动推断需要多少 GPU，也不自动修改服务器。预留功率、部分 Pod 和机架约束属于容量模块的后续候选项，不阻塞上述运维演示。

## Current status / 当前进度

The reusable capacity module is implemented: deterministic power calculations, scenario comparison,
PUE sensitivity, validated plots, a conversational CLI and sourced local knowledge retrieval.
A local CPU baseline now reads five-minute interval data and flags sustained high load.
The bundled example is synthetic; there is no live telemetry, deployed dashboard or incident diagnosis.

项目第一阶段：[一页提案](project-1/proposal.md) · [架构图](docs/architecture.md) ·
[数据说明](docs/operational-data.md) · [验收与任务清单](eval/README.md)。
安装依赖后运行：

```sh
python examples/cpu_baseline.py --plot generated/cpu_baseline.png
```

示例应仅标记 demo-a 在 12:05–12:20 UTC 的持续高负载；图中空白表示缺少读数。

![Synthetic CPU interval averages and the sustained-load event](docs/assets/cpu-baseline-demo.png)

## Quick start

Python 3.12 is the tested version. From this repository root on Windows PowerShell:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-agent-lock.txt
.\.venv\Scripts\python.exe examples/opsai_capacity.py
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

On macOS/Linux use `python3.12 -m venv .venv` and `.venv/bin/python` for the same commands.
The capacity example needs no API key. Optional live conversation setup:

```powershell
.\.venv\Scripts\python.exe run_agent.py --configure
.\.venv\Scripts\python.exe run_agent.py
```

Credentials belong in your local `.env`, never in Git. See [CLI setup](docs/agent_cli.md).

## Structure

| Path | Status and purpose |
| --- | --- |
| `src/` | Existing deterministic capacity model |
| `agent/` | Existing tool wrappers, LLM integration and local retrieval |
| `data/`, `knowledge/` | Capacity scenario inputs, synthetic CPU demo data and curated knowledge; no live telemetry |
| `examples/`, `tests/` | Runnable examples and existing automated tests |
| `figures/`, `results/`, `notebooks/` | Reference capacity analysis artifacts |
| `app/` | Documentation placeholders for future application components |
| `eval/` | Baseline acceptance cases and future evaluation criteria |
| `project-1/`, `project-2/` | First project proposal and future second-project placeholder |
| `docs/` | Existing module guides plus architecture and source provenance |
| `.github/workflows/` | Automated capacity checks inherited from the source |

## Documentation

- [Source provenance and migration validation](docs/source-provenance.md)
- [Architecture](docs/architecture.md)
- [Application integration](docs/opsai-integration.md)
- [Original capacity module README](CAPACITY_README.md) (historical roadmap, not an OpsAI delivery commitment)

The capacity baseline is 221 whole pods, 7,072 racks and 226,304 GPUs for the documented
500 MW / PUE 1.2 scenario. This is a conceptual power budget, not a validated physical installation.
CPU utilization does not directly establish GPU expansion requirements.

No open-source license is granted by this initialization; the owner has not selected a license.
