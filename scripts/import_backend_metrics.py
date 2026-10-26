"""Extract reported aggregates, not raw samples, from the archived evaluation."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "evidence/paper_evaluation_source.md"
OUTPUT = ROOT / "evidence/backend_evaluation_summary.json"


def main() -> None:
    raw = SOURCE.read_bytes()
    text = raw.decode("utf-8")
    tables = []
    for block in re.findall(r"(?m)^\|.*(?:\n\|.*)+", text):
        rows = [[cell.strip() for cell in line.strip("|").split("|")]
                for line in block.splitlines()]
        tables.append([dict(zip(rows[0], row, strict=True)) for row in rows[2:]])
    if len(tables) != 12:
        raise ValueError("Report layout changed; review table mappings before import.")

    def records(index: int, fields: dict[str, str]) -> list[dict]:
        result = []
        for row in tables[index]:
            item = {}
            for key, heading in fields.items():
                value = row[heading]
                if key not in {"workload", "condition", "contrast", "stage", "operation"}:
                    value = float(value.rstrip("%x"))
                item[key] = value
            result.append(item)
        return result

    # These prose counts are checked against literal statements in the frozen source.
    for statement in ["trusted 49/49; helper 49/49", "host 0/49; combined 0/49",
                      "30/30 positive controls", "135 have an explicit denial",
                      "six generic SQLite errors", "six empty/absent results",
                      "rejects 27/30 controls"]:
        if statement not in text:
            raise ValueError(f"Review changed security count: {statement}")
    data = {
        "source_file": SOURCE.name,
        "source_sha256": hashlib.sha256(raw).hexdigest(),
        "evidence_type": "Reported aggregates; referenced raw samples and source archives were not supplied",
        "security": {
            "conditions": ["Trusted", "Helper", "Host", "Host + helper"],
            "forbidden_cases": 49,
            "reached_cases": [49, 49, 0, 0],
            "repetitions_per_case": 3,
            "host_trials": 147,
            "host_explicit_denials": 135,
            "host_sqlite_errors": 6,
            "host_empty_or_absent": 6,
            "host_positive_controls_passed": 30,
            "host_positive_control_trials": 30,
            "direct_language_controls_rejected": 27,
            "direct_language_control_trials": 30,
            "scope": "Counts apply separately to each host condition. Synthetic helper and direct-language conditions are not the production verified mode."
        },
        "runtime": records(6, {"workload":"Workload", "condition":"Condition", "n":"n", "mean":"Mean ms", "sd":"SD ms", "variance":"Variance ms²", "median":"Median ms", "p95":"P95 ms"}),
        "paired_runtime": records(7, {"workload":"Workload", "contrast":"Paired contrast", "increment":"Increment ms", "sd":"SD ms", "variance":"Variance ms²", "overhead_pct":"Overhead"}),
        "host_stages": records(8, {"workload":"Workload", "stage":"Stage", "mean":"Mean ms", "sd":"SD ms", "share_pct":"Share of dispatch"}),
        "setup": records(9, {"workload":"Workload", "mean":"Host setup/preflight mean ms", "sd":"SD ms"}),
        "operations": records(10, {"operation":"Operation", "baseline_mean":"Python mean ms", "host_mean":"Host mean ms", "increment":"Paired overhead ms", "increment_sd":"Overhead SD ms", "increment_variance":"Overhead variance ms²", "ratio":"Host/Python"}),
        "verified": records(11, {"workload":"Workload", "verified_mean":"Verified mean ms", "host_mean":"Host mean ms", "increment":"Paired added ms", "increment_sd":"Added SD ms", "ratio":"Host/verified"}),
        "scopes": {
            "runtime": "10 warmups, 100 measured calls per condition/workload, separately retained first call; fresh worker each call; construction/preflight outside timer; no model or durable audit sink; shuffled paired rounds, seed 20261026.",
            "stages": "Exclusive partition of host dispatch. Other-invoke is a residual. Policy includes Cedar serialization, CLI validation and per-rule authorization processes. Worker includes launch, confinement, execution and teardown. Do not sum stage variances.",
            "operations": "5 warmups, 50 matched samples per variant. Plain Python subprocess baseline; fresh host worker; successful whole calls, not syscall overhead. Inner-body timings are referenced but not present in this supplied report.",
            "verified": "5 warmups, 50 paired samples. Production source admission, binding validation and grant-checked read_text versus Linux execution. Both use real Cedar, with different policy frontends. Executors reused; host workers fresh; setup/static admission excluded and referenced separately.",
            "dispersion": "Reported SDs describe sequential within-host jitter, not task variation. Ratios may use greater precision than the rounded means; paired SDs are not reconstructed from marginal statistics."
        }
    }
    OUTPUT.write_text(json.dumps(data, indent=2) + "\n")
    print(f"Imported {len(data['runtime'])} runtime, {len(data['operations'])} operation, "
          f"and {len(data['verified'])} production-mode rows from {SOURCE.name}.")


if __name__ == "__main__":
    main()
