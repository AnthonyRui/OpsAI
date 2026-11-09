import io
import unittest

from examples.cpu_baseline import SAMPLE, detect, read_intervals


class CpuBaselineTests(unittest.TestCase):
    def test_sample_events_include_only_sustained_load(self):
        with SAMPLE.open(encoding="utf-8") as source:
            self.assertEqual(detect(read_intervals(source)), [{
                "server_id": "demo-a", "start": "2026-11-02T12:05:00+00:00",
                "end": "2026-11-02T12:20:00+00:00", "minutes": 15,
                "peak_cpu_pct": 92,
            }])

    def test_out_of_order_run_extends_to_last_interval(self):
        csv = "timestamp,server_id,cpu_pct\n" + "".join(
            f"2026-11-02T12:{minute:02}:00Z,A,85\n" for minute in (15, 0, 10, 5)
        )
        self.assertEqual([e["minutes"] for e in detect(read_intervals(io.StringIO(csv)))], [20])

    def test_reject_invalid_inputs(self):
        row = "2026-11-02T12:00:00Z,A,90\n"
        for payload in ("", row * 2, row.replace("90", "nan"), row.replace("90", "101"),
                        row.replace(",A,", ",,"), row.replace("Z", ""), row.replace(":00Z", ":01Z")):
            with self.subTest(payload=payload), self.assertRaises(ValueError):
                read_intervals(io.StringIO("timestamp,server_id,cpu_pct\n" + payload))
