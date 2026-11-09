"""Small, offline operations demo; each reading represents a five-minute interval."""

import argparse
import csv
import json
import math
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

STEP = timedelta(minutes=5)
SAMPLE = Path(__file__).resolve().parents[1] / "data/demo/cpu_synthetic.csv"


def read_intervals(source):
    reader = csv.DictReader(source)
    if sorted(reader.fieldnames or []) != ["cpu_pct", "server_id", "timestamp"]:
        raise ValueError("Expected timestamp,server_id,cpu_pct columns")
    servers = defaultdict(dict)
    for row in reader:
        try:
            if None in row:
                raise ValueError("extra column")
            server = (row["server_id"] or "").strip()
            stamp = datetime.fromisoformat(row["timestamp"])
            pct = float(row["cpu_pct"])
            if not server or stamp.tzinfo is None:
                raise ValueError("server and timezone are required")
            stamp = stamp.astimezone(timezone.utc)
            if stamp.minute % 5 or stamp.second or stamp.microsecond:
                raise ValueError("timestamp must start a five-minute interval")
            if not math.isfinite(pct) or not 0 <= pct <= 100:
                raise ValueError("cpu_pct must be between 0 and 100")
            if stamp in servers[server]:
                raise ValueError("duplicate interval")
            servers[server][stamp] = pct
        except (TypeError, ValueError) as exc:
            raise ValueError(f"CSV line {reader.line_num}: {exc}") from exc
    if not servers:
        raise ValueError("No interval records")
    return servers


def detect(servers):
    events = []
    for server, readings in sorted(servers.items()):
        start = previous = None
        peak = 0
        for stamp, pct in sorted(readings.items()):
            if start is not None and (stamp != previous + STEP or pct < 85):
                _finish(events, server, start, previous + STEP, peak)
                start, peak = None, 0
            if pct >= 85:
                start = start or stamp
                peak = max(peak, pct)
            previous = stamp
        if start is not None:
            _finish(events, server, start, previous + STEP, peak)
    return events


def _finish(events, server, start, end, peak):
    minutes = (end - start) // timedelta(minutes=1)
    if minutes >= 15:
        events.append(dict(server_id=server, start=start.isoformat(), end=end.isoformat(),
                           minutes=minutes, peak_cpu_pct=peak))


def plot(servers, events, path):
    import matplotlib
    matplotlib.use("Agg")
    from matplotlib import pyplot as plt

    fig, axes = plt.subplots(len(servers), 1, sharex=True, squeeze=False,
                             figsize=(8, 2.3 * len(servers)))
    for ax, (server, readings) in zip(axes[:, 0], sorted(servers.items())):
        for stamp, pct in readings.items():
            ax.hlines(pct, stamp, stamp + STEP, linewidth=3)
        for event in events:
            if event["server_id"] == server:
                ax.axvspan(datetime.fromisoformat(event["start"]),
                           datetime.fromisoformat(event["end"]), alpha=.2, color="orange")
        ax.axhline(85, linestyle="--", linewidth=.8)
        ax.set(ylabel="CPU (%)", title=server, ylim=(0, 105))
    axes[-1, 0].set_xlabel("Interval time (UTC); shading = sustained high load")
    fig.autofmt_xdate()
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path)
    plt.close(fig)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv", nargs="?", default=SAMPLE, type=Path)
    parser.add_argument("--plot", type=Path)
    args = parser.parse_args()
    try:
        with args.csv.open(encoding="utf-8-sig", newline="") as source:
            servers = read_intervals(source)
        events = detect(servers)
        if args.plot:
            plot(servers, events, args.plot)
        print(json.dumps(events, indent=2))
    except (ValueError, OSError) as exc:
        parser.exit(2, f"CPU demo: {exc}\n")
