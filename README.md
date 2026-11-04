# OpsAI

Data-center operations project foundation, initialized from an existing capacity-planning AI agent.

## Current status / 当前进度

The reusable capacity module is implemented: deterministic power calculations, scenario comparison,
PUE sensitivity, validated plots, a conversational CLI and sourced local knowledge retrieval.
Operational telemetry ingestion, high-load detection, an operations Dashboard and incident investigation
are **not implemented**. Development is awaiting the owner's next scope decision.

本仓库先保留已验证的容量规划能力，准备后续运营分析扩展。当前没有上线网页、运营异常检测或事件调查系统。

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
| `data/`, `knowledge/` | Capacity scenario inputs and curated knowledge; not live operational telemetry |
| `examples/`, `tests/` | Runnable examples and existing automated tests |
| `figures/`, `results/`, `notebooks/` | Reference capacity analysis artifacts |
| `app/` | Documentation placeholders for future application components |
| `eval/` | Planned operational evaluation; no fabricated evaluation scores |
| `project-1/`, `project-2/` | Proposal and release-note placeholders awaiting scope definition |
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
