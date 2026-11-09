# Project 1 acceptance and task board

| Done | Next | Later |
| --- | --- | --- |
| Proposal, architecture, data contract, synthetic CSV, offline CPU rule and plot | Generalize the import workflow and collect representative cases | Dashboard, evidence-grounded explanations, public demo and independent evaluation |

Run `python -m unittest discover -s tests -p test_cpu_baseline.py -v`.
The synthetic acceptance oracle is defined independently of the detector:

| Case | Expected |
| --- | --- |
| demo-a: three adjacent intervals at 85, 92, 89 | Exactly one event: 12:05–12:20 UTC, 15 minutes, peak 92% |
| demo-b: one spike above 85 | No event |
| demo-c: high readings separated by missing interval | No event spanning the gap |
| Invalid, duplicate or missing input | Reject input; never present it as healthy |

These checks verify the rule implementation. They do not measure production accuracy.
Later, on held-out labelled incidents, report event precision and recall with a
predefined server/time matching rule. Separately compare rule-only evidence against
AI-assisted investigation on identical cases: correct server/time, unsupported
claims, time taken, and failure examples. Do not use synthetic acceptance results
as evidence that AI improves operator performance.
