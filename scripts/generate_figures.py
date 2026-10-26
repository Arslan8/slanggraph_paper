"""Generate the evaluation figures used by the slangGraph paper."""

from __future__ import annotations

import hashlib
import io
import json
import os
import tempfile
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch


ROOT = Path(__file__).resolve().parents[1]
FIGURES = ROOT / "figures"


def _configure() -> None:
    """Configure deterministic, grayscale, publication-sized figures."""
    mpl.rcParams.update(
        {
            "font.family": "serif",
            "font.serif": ["STIXGeneral"],
            "mathtext.fontset": "stix",
            "font.size": 8,
            "axes.labelsize": 8,
            "axes.titlesize": 9,
            "xtick.labelsize": 7,
            "ytick.labelsize": 7,
            "legend.fontsize": 7,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "savefig.bbox": "tight",
            "savefig.pad_inches": 0.02,
        }
    )


def _save(fig: plt.Figure, name: str) -> None:
    """Publish a complete vector PDF before LaTeX can read the destination."""
    FIGURES.mkdir(parents=True, exist_ok=True)
    buffer = io.BytesIO()
    fig.savefig(buffer, format="pdf")
    plt.close(fig)
    payload = buffer.getvalue()
    if not payload.endswith(b"%%EOF\n"):
        raise ValueError(f"Incomplete generated PDF: {name}")
    with tempfile.NamedTemporaryFile(dir=FIGURES, suffix=".tmp", delete=False) as handle:
        temporary = Path(handle.name)
        handle.write(payload)
        handle.flush()
        os.fsync(handle.fileno())
    try:
        temporary.replace(FIGURES / name)
    finally:
        temporary.unlink(missing_ok=True)


def _box(
    ax: plt.Axes,
    xy: tuple[float, float],
    width: float,
    height: float,
    text: str,
    *,
    facecolor: str = "white",
    edgecolor: str = "#202020",
    fontsize: float = 7.2,
    linestyle: str = "-",
) -> None:
    """Draw a compact rounded box used by the system diagrams."""
    patch = FancyBboxPatch(
        xy,
        width,
        height,
        boxstyle="round,pad=0.025,rounding_size=0.035",
        facecolor=facecolor,
        edgecolor=edgecolor,
        linewidth=0.8,
        linestyle=linestyle,
    )
    ax.add_patch(patch)
    ax.text(
        xy[0] + width / 2,
        xy[1] + height / 2,
        text,
        ha="center",
        va="center",
        fontsize=fontsize,
        linespacing=1.15,
    )


def _arrow(
    ax: plt.Axes,
    start: tuple[float, float],
    end: tuple[float, float],
    *,
    color: str = "#202020",
    linestyle: str = "-",
) -> None:
    """Draw an arrow used by the system diagrams."""
    ax.add_patch(
        FancyArrowPatch(
            start,
            end,
            arrowstyle="-|>",
            mutation_scale=8,
            linewidth=0.8,
            color=color,
            linestyle=linestyle,
        )
    )


def motivation() -> None:
    """Show why authorizing a call is weaker than constraining its effects."""
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.35))
    for ax in axes:
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 6)
        ax.axis("off")

    left, right = axes
    left.set_title("(a) Call-boundary authorization", fontweight="bold", pad=4)
    _box(left, (0.2, 3.9), 2.2, 1.0, "Call\nread(q3)", facecolor="#f2f2f2")
    _box(left, (3.5, 3.9), 2.2, 1.0, "Call guard\nALLOW", facecolor="#d9d9d9")
    _box(
        left,
        (6.5, 3.9),
        3.2,
        1.0,
        "Tool\nimplementation",
        facecolor="#f2f2f2",
        fontsize=6.6,
    )
    _arrow(left, (2.4, 4.4), (3.5, 4.4))
    _arrow(left, (5.7, 4.4), (6.5, 4.4))
    _box(left, (4.65, 1.1), 2.5, 0.9, "payroll.csv\nREAD", edgecolor="#8c1d18", fontsize=6.6)
    _box(left, (7.4, 1.1), 2.5, 0.9, "attacker.net\nSEND", edgecolor="#8c1d18", fontsize=6.6)
    _arrow(left, (7.75, 3.9), (5.9, 2.0), color="#8c1d18")
    _arrow(left, (8.45, 3.9), (8.65, 2.0), color="#8c1d18")
    left.text(7.8, 0.35, "effects occur below the check", ha="center", color="#8c1d18", fontsize=7.2)

    right.set_title("(b) Layered reference monitoring", fontweight="bold", pad=4)
    _box(right, (0.2, 3.9), 2.2, 1.0, "Call\nread(q3)", facecolor="#f2f2f2")
    _box(
        right,
        (3.5, 3.9),
        2.2,
        1.0,
        "HostRouter\nframework",
        facecolor="#d9d9d9",
        fontsize=6.5,
    )
    _box(
        right,
        (6.5, 3.9),
        3.2,
        1.0,
        "Confined worker\nhost",
        facecolor="#bdbdbd",
        fontsize=6.5,
    )
    _arrow(right, (2.4, 4.4), (3.5, 4.4))
    _arrow(right, (5.7, 4.4), (6.5, 4.4))
    _box(right, (4.85, 1.1), 2.3, 0.9, "report/q3\nREAD", edgecolor="#1f5d3a", fontsize=6.8)
    _box(right, (7.55, 1.1), 2.3, 0.9, "all other\nauthority", edgecolor="#8c1d18", fontsize=6.8)
    _arrow(right, (7.75, 3.9), (6.0, 2.0), color="#1f5d3a")
    _arrow(right, (8.45, 3.9), (8.7, 2.0), color="#8c1d18")
    right.text(6.0, 0.35, "grant", ha="center", color="#1f5d3a", fontsize=7.2)
    right.text(8.7, 0.35, "DENY", ha="center", color="#8c1d18", fontsize=7.2, fontweight="bold")

    fig.subplots_adjust(wspace=0.16)
    _save(fig, "motivation.pdf")


def architecture() -> None:
    """Show requirements, fixed policy, and distinct enforcement contracts."""
    fig, ax = plt.subplots(figsize=(7.0, 3.35))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8.5)
    ax.axis("off")
    _box(ax, (0.2, 7.0), 3.1, 1.0, "Requirement producer\nresource manifest", facecolor="#f2f2f2")
    _box(ax, (5.0, 7.0), 3.6, 1.0, "Authorization\nprincipal DAC + operator MAC", facecolor="#d2d2d2", fontsize=6.3)
    _box(ax, (10.2, 7.0), 3.5, 1.0, "Invocation grant\nresources + baseline", facecolor="#d2d2d2")
    _arrow(ax, (3.3, 7.5), (5.0, 7.5))
    _arrow(ax, (8.6, 7.5), (10.2, 7.5))
    _box(ax, (0.2, 4.7), 3.5, 1.2, "Trusted analyzers\nfindings + provenance\nno policy updates", facecolor="#f2f2f2")
    _box(ax, (5.0, 4.7), 3.6, 1.2, "Fixed security modules\nrequired analysis barriers\nfresh attempt snapshot", facecolor="#e4e4e4")
    _box(ax, (10.2, 4.7), 3.5, 1.2, "Framework mediation\nstate / model / output\nexplicit coverage contracts", facecolor="#e4e4e4")
    _arrow(ax, (3.7, 5.3), (5.0, 5.3))
    _arrow(ax, (6.8, 5.9), (6.8, 7.0))
    _arrow(ax, (11.95, 7.0), (11.95, 5.9))
    _arrow(ax, (8.6, 5.3), (10.2, 5.3))
    boxes = [
        (0.2, "Restricted in-process APIs\nsource-body admission\nactive-grant checks"),
        (4.9, "Resource mediators\npump / SQLite / custom\nper-request grant checks"),
        (9.6, "Host-confined workers\nLandlock / seccomp\nactivation before import"),
    ]
    for x, label in boxes:
        _box(ax, (x, 1.6), 4.0, 1.35, label, facecolor="#f2f2f2", fontsize=7.1)
    # One grant fans out to alternative/cooperating enforcement paths.
    ax.plot([13.9, 13.9, 2.2], [7.5, 3.6, 3.6], color="#4a4a4a", linewidth=0.8)
    ax.plot([13.7, 13.9], [7.5, 7.5], color="#4a4a4a", linewidth=0.8)
    for x in (2.2, 6.9, 11.6):
        _arrow(ax, (x, 3.6), (x, 2.95))
    ax.text(7.0, 0.65, "Unsupported routes deny under runtime MAC; trusted adapters must preserve the grant",
            ha="center", fontsize=7.1, fontweight="bold")
    _save(fig, "architecture.pdf")


def overhead() -> None:
    """Plot policy-path overhead relative to security-disabled execution."""
    labels = ["Security\ndisabled", "DAC + cap", "Five modules"]
    medians_us = np.array([593.701, 672.212, 884.800])
    overhead_pct = (medians_us / medians_us[0] - 1.0) * 100.0

    fig, ax = plt.subplots(figsize=(3.35, 2.35))
    bars = ax.bar(
        np.arange(len(labels)),
        overhead_pct,
        color=["white", "#8f8f8f", "#303030"],
        edgecolor="black",
        linewidth=0.7,
        width=0.62,
    )
    ax.set_xticks(np.arange(len(labels)), labels=labels)
    ax.set_ylabel("Overhead vs. disabled (%)")
    ax.set_ylim(0, 58)
    ax.set_yticks(np.arange(0, 51, 10))
    ax.grid(axis="y", color="#d0d0d0", linewidth=0.5)
    ax.set_axisbelow(True)
    ax.spines[["top", "right"]].set_visible(False)
    for bar, value in zip(bars, overhead_pct, strict=True):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + 1.3,
            f"{value:.1f}%",
            ha="center",
            va="bottom",
            fontweight="bold",
        )
    _save(fig, "overhead.pdf")


def _application_metrics() -> dict:
    """Load reported aggregates and verify their archived source identity."""
    evidence = ROOT / "evidence"
    data = json.loads((evidence / "application_macrobenchmarks_summary.json").read_text())
    digest = hashlib.sha256((evidence / data["source_file"]).read_bytes()).hexdigest()
    if digest != data["source_sha256"]:
        raise ValueError("The application report changed; review plotted aggregates.")
    return data


def _backend_metrics() -> dict:
    evidence = ROOT / "evidence"
    data = json.loads((evidence / "backend_evaluation_summary.json").read_text())
    digest = hashlib.sha256((evidence / data["source_file"]).read_bytes()).hexdigest()
    if digest != data["source_sha256"]:
        raise ValueError("Backend report changed; review and reimport its aggregates.")
    return data


def application_effects(data: dict, backend: dict) -> None:
    """Keep application and backend case denominators visibly separate."""
    effects = data["controlled_effects"]
    security = backend["security"]
    labels = [f"{c}  {d}" for c, d in zip(
        data["configurations"], data["configuration_descriptions"], strict=True)]
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 1.95))
    panels = [
        (effects["forbidden_effects_reached"],
         effects["supported_forbidden_probes_per_configuration"], labels,
         "(a) Pandas computation", [0, 1, 2, 3]),
        (security["reached_cases"], security["forbidden_cases"],
         security["conditions"], "(b) Synthetic backend census", [0, 10, 20, 30, 40, 49]),
    ]
    for ax, (values, denominator, names, title, ticks) in zip(axes, panels, strict=True):
        bars = ax.barh(range(len(values)), values, height=0.58,
                       color=["#cfcfcf", "#8f8f8f", "#303030", "#303030"][:len(values)],
                       edgecolor="black", linewidth=0.6)
        ax.set_xlim(0, denominator * 1.07)
        ax.set_xticks(ticks)
        ax.set_xlabel("Forbidden effects reached (distinct cases)")
        ax.set_title(title, fontweight="bold", pad=7)
        ax.set_yticks(range(len(values)), names)
        ax.grid(axis="x", color="#d0d0d0", linewidth=0.45)
        ax.set_axisbelow(True)
        ax.spines[["top", "right"]].set_visible(False)
        for bar, value in zip(bars, values, strict=True):
            ax.text(value - denominator * 0.025 if value else denominator * 0.025,
                    bar.get_y() + bar.get_height() / 2,
                    f"{value}/{denominator}", va="center",
                    ha="right" if value else "left", fontweight="bold")
        ax.invert_yaxis()
    fig.tight_layout(w_pad=2.2)
    _save(fig, "application-effects.pdf")


def application_runtime(data: dict) -> None:
    """Normalize means and SDs by each cohort's fixed upstream mean."""
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.15))
    panels = [
        (data["local_replay"], "(a) Computation replay, 100 calls/config.",
         "Runtime relative to A", 4.2, 2),
        (data["full_workflow"], "(b) Full workflow, 5 runs/config.",
         "Runtime relative to A", 1.5, 3),
    ]
    for ax, (cohort, title, ylabel, ymax, decimals) in zip(axes, panels, strict=True):
        baseline = cohort["mean"][0]
        means = [v / baseline for v in cohort["mean"]]
        scaled_sd = [v / baseline for v in cohort["sd"]]
        bars = ax.bar(range(3), means, yerr=scaled_sd,
                      capsize=3, width=0.57,
                      color=["#cfcfcf", "#8f8f8f", "#303030"],
                      edgecolor="black", linewidth=0.6,
                      error_kw={"elinewidth": 0.8, "capthick": 0.8})
        ax.set_xticks(range(3), data["configurations"])
        ax.set_ylim(0, ymax)
        ax.yaxis.set_major_formatter(mpl.ticker.FuncFormatter(lambda v, _: f"{v:g}×"))
        ax.axhline(1, color="#505050", linewidth=0.65, linestyle="--")
        ax.set_ylabel(ylabel)
        ax.set_title(title, fontweight="bold", pad=8)
        ax.grid(axis="y", color="#d0d0d0", linewidth=0.45)
        ax.set_axisbelow(True)
        ax.spines[["top", "right"]].set_visible(False)
        for bar, mean, sd in zip(bars, means, scaled_sd, strict=True):
            ax.text(bar.get_x() + bar.get_width() / 2,
                    mean + sd + 0.025 * ymax, f"{mean:.{decimals}f}×",
                    ha="center", va="bottom", fontsize=8, fontweight="bold")
    fig.tight_layout(w_pad=2.1)
    _save(fig, "application-runtime.pdf")


def audit_breakdown(data: dict, backend: dict) -> None:
    """Show two measured bottlenecks without pooling their denominators."""
    cohort = data["audit_diagnostic_b"]
    extra = cohort["mean_total"] - cohort["mean_subprocess"]
    audit_pct = 100 * cohort["mean_audit"] / extra
    other_pct = 100 - audit_pct
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.45))
    ax = axes[0]
    ax.barh(0, audit_pct, height=0.5, color="#303030", edgecolor="black", linewidth=0.6)
    ax.barh(0, other_pct, left=audit_pct, height=0.5, color="white", edgecolor="black", linewidth=0.6)
    ax.text(audit_pct / 2, 0, f"Audit persistence: {audit_pct:.1f}%",
            ha="center", va="center", fontsize=7.5, color="white")
    ax.annotate(f"Other: {other_pct:.1f}%", xy=(100 - other_pct / 2, 0.26),
                xytext=(100, 0.64), ha="right", va="center", fontsize=7,
                arrowprops={"arrowstyle": "-", "lw": 0.6})
    ax.set_title("(a) Application B diagnostic, n=20", fontweight="bold", fontsize=8.5)
    ax.set_ylim(-0.5, 0.9)
    ax.set_yticks([])
    ax.set_xlabel("Share of time outside subprocess (%)")

    ax = axes[1]
    workloads = ["arithmetic", "allowed_read", "allowed_small_file"]
    stage_rows = backend["host_stages"]
    groups = [(["policy"], "Policy", "#303030", None),
              (["worker"], "Worker", "#b0b0b0", None),
              (["negotiate"], "Negotiation", "white", "///"),
              (["attest", "grant", "other_invoke", "outside_invoke"],
               "Other prep./dispatch", "white", None)]
    for i, workload in enumerate(workloads):
        rows = {r["stage"]: r["mean"] for r in stage_rows if r["workload"] == workload}
        total = sum(rows.values())
        left = 0.0
        for stages, label, color, hatch in groups:
            value = 100 * sum(rows[k] for k in stages) / total
            ax.barh(i, value, left=left, height=0.54, color=color,
                    edgecolor="black", hatch=hatch, linewidth=0.55,
                    label=label if i == 0 else None)
            if stages in [["policy"], ["worker"]]:
                ax.text(left + value / 2, i, f"{value:.1f}%", ha="center", va="center",
                        fontsize=6.8, color="white" if stages == ["policy"] else "black")
            left += value
    ax.set_yticks(range(3), ["Arithmetic", "Read", "Write 4 KiB"])
    ax.invert_yaxis()
    ax.set_xlabel("Share of total dispatch (%)")
    ax.set_title("(b) Synthetic host, n=100/workload", fontweight="bold", fontsize=8.5)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.32), ncol=2,
              fontsize=6.5, frameon=False, handlelength=1.8, columnspacing=1)
    for ax in axes:
        ax.set_xlim(0, 102)
        ax.set_xticks([0, 25, 50, 75, 100])
        ax.spines[["top", "right", "left"]].set_visible(False)
        ax.tick_params(axis="y", length=0)
    fig.tight_layout(w_pad=2.5)
    _save(fig, "audit-breakdown.pdf")


def backend_runtime(data: dict) -> None:
    """Plot only reported mean ratios; paired dispersion stays in the appendix."""
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.45))
    ax = axes[0]
    workloads = ["arithmetic", "allowed_read", "allowed_small_file"]
    contrasts = [("host-trusted", "Host / trusted", "#303030", -0.18),
                 ("host_language_helper-language_helper", "Host + helper / helper", "#b0b0b0", 0.18)]
    for contrast, label, color, offset in contrasts:
        values = [next(r["overhead_pct"] for r in data["paired_runtime"]
                       if r["workload"] == w and r["contrast"] == contrast) / 100 + 1
                  for w in workloads]
        bars = ax.bar(np.arange(3) + offset, values, width=0.34, color=color,
                      edgecolor="black", linewidth=0.6, label=label)
        for bar, value in zip(bars, values, strict=True):
            ax.text(bar.get_x() + bar.get_width()/2, value + 0.3, f"{value:.1f}×",
                    ha="center", va="bottom", fontsize=6.5, fontweight="bold")
    ax.set_xticks(range(3), ["Arithmetic", "Read", "Write 4 KiB"])
    ax.set_title("(a) Synthetic backends, n=100", fontweight="bold")
    ax.legend(loc="upper center", fontsize=6.2, frameon=False, handlelength=1.6)
    ax = axes[1]
    ratios = [r["ratio"] for r in data["verified"]]
    bars = ax.bar(range(5), ratios, width=0.58, color="#303030", edgecolor="black", linewidth=0.6)
    for bar, value in zip(bars, ratios, strict=True):
        ax.text(bar.get_x() + bar.get_width()/2, value + 0.35, f"{value:.2f}×",
                ha="center", va="bottom", fontsize=6.8, fontweight="bold")
    ax.set_xticks(range(5), ["Constant", "Read\n32 B", "Read\n4 KiB", "Read\n64 KiB", "Two reads\n32 B"])
    ax.set_title("(b) Linux / verified mode, n=50", fontweight="bold")
    for ax in axes:
        ax.set_ylim(0, 21)
        ax.set_yticks([0, 5, 10, 15, 20])
        ax.yaxis.set_major_formatter(mpl.ticker.FuncFormatter(lambda v, _: f"{v:g}×"))
        ax.axhline(1, color="#505050", linewidth=0.65, linestyle="--")
        ax.set_ylabel("Runtime relative to stated baseline")
        ax.grid(axis="y", color="#d0d0d0", linewidth=0.45)
        ax.set_axisbelow(True)
        ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout(w_pad=2.2)
    _save(fig, "backend-runtime.pdf")


def operation_overhead(data: dict) -> None:
    """Show successful whole-call overhead and scaled paired-difference SD."""
    rows = data["operations"]
    values = [100 * (r["ratio"] - 1) for r in rows]
    errors = [100 * r["increment_sd"] / r["baseline_mean"] for r in rows]
    fig, ax = plt.subplots(figsize=(7.0, 3.7))
    bars = ax.barh(range(len(rows)), values, xerr=errors, height=0.65,
                   color="#b0b0b0", edgecolor="black", linewidth=0.5,
                   capsize=2, error_kw={"elinewidth": 0.7, "capthick": 0.7})
    ax.set_yticks(range(len(rows)), [r["operation"] for r in rows])
    ax.invert_yaxis()
    ax.set_xlim(0, 1850)
    ax.set_xticks([0, 500, 1000, 1500])
    ax.xaxis.set_major_formatter(mpl.ticker.FuncFormatter(lambda v, _: f"{v:g}%"))
    ax.set_xlabel("Added whole-call time relative to plain Python subprocess")
    ax.set_title("Successful operation/API variants, 50 matched pairs each", fontweight="bold")
    ax.grid(axis="x", color="#d0d0d0", linewidth=0.45)
    ax.set_axisbelow(True)
    ax.spines[["top", "right"]].set_visible(False)
    for bar, value, error in zip(bars, values, errors, strict=True):
        ax.text(value + error + 16, bar.get_y() + bar.get_height()/2,
                f"{value:.0f}%", ha="left", va="center", fontsize=6.8)
    fig.tight_layout()
    _save(fig, "operation-overhead.pdf")



def _alternative_metrics() -> dict:
    data = json.loads((ROOT / "evidence/alternative_backends_summary.json").read_text())
    digest = hashlib.sha256((ROOT / data["source"]).read_bytes()).hexdigest()
    if digest != data["source_sha256"]:
        raise ValueError("Alternative-backend summary does not match its source report")
    return data


def _paired_panels(rows: list[dict], workloads: list[str], labels: list[str],
                   titles: tuple[str, str], name: str, *, height: float = 2.7,
                   ratio_digits: int = 2) -> None:
    """Keep ratios and paired-difference confidence intervals on separate axes."""
    fig, axes = plt.subplots(1, 2, figsize=(7.0, height), gridspec_kw={"width_ratios": [1, 1.12]})
    for mode, label, color, marker, offset in [
        ("landlock", "Landlock", "#202020", "o", -0.13),
        ("container", "Container", "#707070", "s", 0.13),
    ]:
        selected = [next(r for r in rows if r["workload"] == w and r["mode"] == mode) for w in workloads]
        y = np.arange(len(workloads)) + offset
        ratios = [r["ratio_of_reported_means"] for r in selected]
        axes[0].plot(ratios, y, linestyle="", marker=marker, color=color, markersize=4, label=label)
        for x, yy in zip(ratios, y, strict=True):
            axes[0].annotate(f"{x:.{ratio_digits}f}×", (x, yy), xytext=(5, 0), textcoords="offset points",
                             va="center", fontsize=7)
        increments = np.array([r["added_ms"] for r in selected])
        bounds = np.array([r["session_ci_ms"] for r in selected])
        axes[1].errorbar(increments, y, xerr=np.array([increments - bounds[:, 0], bounds[:, 1] - increments]),
                         fmt=marker, color=color, markersize=4, capsize=2, elinewidth=0.8, label=label)
    axes[0].axvline(1, color="#888888", linestyle="--", linewidth=0.7)
    axes[1].axvline(0, color="#888888", linestyle="--", linewidth=0.7)
    axes[0].set_xlabel("Runtime / baseline (ratio of means)")
    axes[1].set_xlabel("Added time (ms), session 95% CI")
    axes[0].xaxis.set_major_formatter(mpl.ticker.FuncFormatter(lambda v, _: f"{v:g}×"))
    max_ratio = max(r["ratio_of_reported_means"] for r in rows)
    axes[0].set_xlim(0.85 if max_ratio < 3 else 0, max_ratio * 1.22)
    for i, ax in enumerate(axes):
        ax.set_yticks(range(len(labels)), labels if i == 0 else [""] * len(labels))
        ax.set_ylim(len(labels) - 0.5, -0.5)
        ax.set_title(titles[i], fontweight="bold")
        ax.grid(axis="x", color="#dddddd", linewidth=0.5)
        ax.spines[["top", "right", "left"]].set_visible(False)
        ax.tick_params(axis="y", length=0)
    handles, legend_labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, legend_labels, loc="lower center", ncol=2, frameon=False, bbox_to_anchor=(0.55, -0.02))
    fig.tight_layout(w_pad=2.0, rect=(0, 0.11, 1, 1))
    _save(fig, name)


def current_backend_runtime(data: dict) -> None:
    _paired_panels(data["comparison"],
                   ["constant_control", "read_32b", "read_4kib", "read_64kib", "two_reads_32b"],
                   ["Constant", "Read 32 B", "Read 4 KiB", "Read 64 KiB", "Two reads 32 B"],
                   ("(a) Relative to verified mode", "(b) Added to verified mode"),
                   "backend-runtime.pdf", height=2.8)


def execution_cost(data: dict) -> None:
    _paired_panels(data["application"] + data["native_chain"],
                   ["pandas_february", "env_to_cat"],
                   ["Pandas replay", "Native chain"],
                   ("(a) Relative to plain process", "(b) Added to plain process"),
                   "execution-cost.pdf", height=2.15, ratio_digits=4)


def current_operation_overhead(data: dict) -> None:
    rows = data["operations"]
    operations = list(dict.fromkeys(r["workload"] for r in rows))
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 4.3), sharey=True)
    for ax, mode, title in zip(axes, ["landlock", "container"], ["Landlock", "Container"], strict=True):
        selected = [next(r for r in rows if r["workload"] == w and r["mode"] == mode) for w in operations]
        means = np.array([r["added_ms"] for r in selected])
        ci = np.array([r["session_ci_ms"] for r in selected])
        ax.errorbar(means, range(len(operations)), xerr=[means-ci[:, 0], ci[:, 1]-means],
                    fmt="o", color="#202020", markersize=3.5, capsize=2, elinewidth=0.8)
        ax.axvline(0, color="#999999", linestyle="--", linewidth=0.6)
        ax.set_title(title, fontweight="bold")
        ax.set_xlabel("Added whole-call time (ms), 95% CI")
        ax.grid(axis="x", color="#dddddd", linewidth=0.5)
        ax.spines[["top", "right"]].set_visible(False)
    axes[0].set_yticks(range(len(operations)), [w.replace("_", " ") for w in operations])
    axes[0].invert_yaxis()
    axes[0].set_xlim(-3, 6)
    axes[1].set_xlim(44, 57)
    fig.tight_layout(w_pad=2)
    _save(fig, "operation-overhead.pdf")

def main() -> None:
    """Generate every paper figure from the recorded evaluation values."""
    _configure()
    motivation()
    architecture()
    overhead()
    data = _application_metrics()
    backend = _backend_metrics()
    application_runtime(data)
    audit_breakdown(data, backend)
    current = _alternative_metrics()
    current_backend_runtime(current)
    execution_cost(current)
    current_operation_overhead(current)


if __name__ == "__main__":
    main()

