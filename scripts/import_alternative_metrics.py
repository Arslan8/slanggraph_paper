"""Import reported aggregates without reconstructing unavailable raw samples."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "evidence/alternative_backends_source.md"
EXPECTED_SHA256 = "a4068963b3ebb56c84ec7ce25cc77155989fec812cbdf2033d95a64bd595aa8f"


def tables(text: str) -> list[list[list[str]]]:
    result, rows = [], []
    for line in text.splitlines() + ["END"]:
        if line.startswith("|"):
            cells = [s.strip() for s in line.strip().strip("|").split("|")]
            if all(re.fullmatch(r":?-+:?", s) for s in cells):
                if len(rows) > 1:
                    result.append(rows[:-1])
                    rows = rows[-1:]
            else:
                rows.append(cells)
        elif line.strip() and rows:
            result.append(rows)
            rows = []
    return result


def numeric(cell: str):
    if cell == "—":
        return None
    if cell.startswith("["):
        return json.loads(cell)
    return float(cell)


def main() -> None:
    payload = SOURCE.read_bytes()
    digest = hashlib.sha256(payload).hexdigest()
    if digest != EXPECTED_SHA256:
        raise ValueError("Review changed source before importing another cohort")
    text = re.sub(r"\\([#|*`\[\]().:_-])", r"\1", payload.decode())
    out = {
        "source": SOURCE.relative_to(ROOT).as_posix(),
        "source_sha256": digest,
        "provenance": "Reported rounded aggregates; raw archives not supplied with report",
        "protocol": {"sessions": 5, "measured_per_session": 20,
                     "warmup_per_session": 10, "separate_first_use_per_session": 1,
                     "ci": "Student t, df=4, on five session mean paired differences (ms)"},
        "comparison": [], "operations": [], "application": [], "native_chain": [],
        "stages": [], "admission": [], "operation_bodies_us": [],
        "application_stages": [], "lifecycle": [], "security": [],
    }
    keys = ["mean_ms", "sd_ms", "median_ms", "p95_ms", "added_ms", "paired_sd_ms", "session_ci_ms"]
    for table in tables(text):
        header, *rows = table
        if header[0] == "Workload / mode" and header[1] == "Mean ms":
            for row in rows:
                workload, mode = row[0].split(" / ")
                group = ("comparison" if workload in ["constant_control", "read_32b", "read_4kib", "read_64kib", "two_reads_32b"] else
                         "application" if workload == "pandas_february" else
                         "native_chain" if workload == "env_to_cat" else "operations")
                out[group].append({"workload": workload, "mode": mode,
                                   **dict(zip(keys, map(numeric, row[1:]), strict=True))})
        elif header[0] == "Workload / mode":
            for row in rows:
                workload, mode = row[0].split(" / ")
                out["stages"].append({"workload": workload, "mode": mode,
                                      "policy_ms": float(row[1]), "execution_ms": float(row[2])})
        elif header[0] == "Tool workload":
            out["admission"] = [{"workload": r[0], "n": int(r[1]), "mean_ms": float(r[2]), "sd_ms": float(r[3])} for r in rows]
        elif header[0] == "Operation":
            out["operation_bodies_us"] = [{"operation": r[0], **dict(zip(["plain", "landlock", "container"], map(float, r[1:]), strict=True))} for r in rows]
        elif header[0] == "Application mode":
            out["application_stages"] = [{"mode": r[0], **dict(zip(["activation_ms", "body_ms", "residual_ms"], map(float, r[1:]), strict=True))} for r in rows]
        elif header[0] == "Experiment":
            out["lifecycle"] = [{"experiment": r[0], "containers": int(r[1]), "setup_mean_ms": float(r[2]), "setup_sd_ms": float(r[3]), "teardown_mean_ms": float(r[4])} for r in rows]
        elif header[0] == "Mode":
            out["security"] = [{"mode": r[0], "effect_cases": int(r[1].split('/')[0]), "forbidden_cases": 49,
                                "allowed_successes": 30, "allowed_trials": 30,
                                "reduction_pct": float(r[3].strip('%'))} for r in rows]
    out["forbidden_trial_outcomes"] = {
        "landlock": {"effect_observed": 3, "no_effect_observed": 6, "operation_denied": 132, "operation_error": 6},
        "container": {"effect_observed": 0, "no_effect_observed": 9, "operation_denied": 132, "operation_error": 6},
    }
    out["verified_controls"] = {"reported": "12/12 controls, each repeated three times",
                                "counting_ambiguity": "Raw evidence needed to distinguish cases from trials"}
    out["native_security"] = {"checks_per_mode": 15, "plain_disclosures": 15,
                               "landlock_disclosures": 0, "container_disclosures": 0,
                               "profile": "Separate exec-enabled profile; no Landlock process-count quota"}
    for group, expected in [("comparison", 15), ("operations", 48), ("application", 3), ("native_chain", 3)]:
        if len(out[group]) != expected:
            raise ValueError(f"Unexpected {group} row count: {len(out[group])}")
        baseline = "verified" if group == "comparison" else "plain"
        bases = {r["workload"]: r["mean_ms"] for r in out[group] if r["mode"] == baseline}
        for row in out[group]:
            row["ratio_of_reported_means"] = row["mean_ms"] / bases[row["workload"]]
            row["overhead_pct"] = 100 * (row["ratio_of_reported_means"] - 1)
            if row["added_ms"] is not None and abs(row["mean_ms"] - bases[row["workload"]] - row["added_ms"]) > 0.002:
                raise ValueError(f"Paired increment differs beyond report rounding: {row}")
    for outcomes in out["forbidden_trial_outcomes"].values():
        assert sum(outcomes.values()) == 147
    target = ROOT / "evidence/alternative_backends_summary.json"
    target.write_text(json.dumps(out, indent=2) + "\n")
    print(f"Imported {sum(len(out[g]) for g in ['comparison', 'operations', 'application', 'native_chain'])} timing rows; source {digest}")


if __name__ == "__main__":
    main()
