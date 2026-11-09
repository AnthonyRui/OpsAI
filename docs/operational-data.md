# CPU demo data contract

The bundled data are hand-authored, synthetic five-minute interval averages.
They describe no real machines. Each row represents the interval **starting**
at the timestamp, ending five minutes later (exclusive); an instantaneous
sample must not be passed off as an interval average.

| CSV field | Meaning | Validation |
| --- | --- | --- |
| timestamp | ISO timestamp with UTC offset, normalized to UTC | on a five-minute boundary |
| server_id | server identifier | nonblank |
| cpu_pct | average CPU utilization during this interval, percent | finite, 0–100 inclusive |

The example accepts these three columns, one record per server and timestamp.
Records can arrive out of order; duplicate keys and invalid rows are rejected.
Missing intervals are unknown and break continuity. The default demo rule is
three adjacent qualifying intervals (15 minutes), including equality at 85%.
Report one event per uninterrupted run: server, inclusive start, exclusive
end, minutes and peak interval average. Do not interpret peaks as instantaneous
maxima or a high-load event as a confirmed incident.
