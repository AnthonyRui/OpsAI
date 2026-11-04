# Architecture

Current implemented path:

```text
Python caller or existing CLI
  -> agent validated tools
  -> src deterministic capacity calculations
  -> results with units, sources and scope
```

Optional LLM orchestration and local knowledge retrieval reuse the existing agent/ code.
The new app/ directories are placeholders only. No web API or Dashboard is deployed.
Future telemetry analysis must be explicitly scoped and evaluated separately from capacity calculations.
Existing entry points and resource paths are preserved to avoid breaking tests and notebooks.
