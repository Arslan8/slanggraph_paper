"""Generate the evaluation figures used by the slangGraph paper."""

from __future__ import annotations

import hashlib
import json
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
    """Save one vector figure and close it."""
    FIGURES.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIGURES / name)
    plt.close(fig)


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


def application_effects(data: dict) -> None:
    """Contrast reached forbidden effects with retained legitimate computation."""
    effects = data["controlled_effects"]
    configs = data["configurations"]
    descriptions = data["configuration_descriptions"]
    labels = [f"{c}  {d}" for c, d in zip(configs, descriptions, strict=True)]
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 1.9), sharey=True)
    panels = [
        (effects["forbidden_effects_reached"],
         effects["supported_forbidden_probes_per_configuration"],
         "(a) Forbidden effects reached", "Supported probes (count)"),
        (effects["correct_computations"],
         effects["case_profile_executions_per_configuration"],
         "(b) Correct computation results", "Controlled case/profile runs (count)"),
    ]
    for ax, (values, denominator, title, xlabel) in zip(axes, panels, strict=True):
        bars = ax.barh(range(3), values, height=0.58,
                       color=["#cfcfcf", "#8f8f8f", "#303030"],
                       edgecolor="black", linewidth=0.6)
        ax.set_xlim(0, denominator + 0.2)
        ax.set_xticks(range(denominator + 1))
        ax.set_xlabel(xlabel)
        ax.set_title(title, fontweight="bold", pad=7)
        ax.set_yticks(range(3), labels)
        ax.grid(axis="x", color="#d0d0d0", linewidth=0.45)
        ax.set_axisbelow(True)
        ax.spines[["top", "right"]].set_visible(False)
        for i, (bar, value) in enumerate(zip(bars, values, strict=True)):
            inside = value > 0
            ax.text(value - 0.12 if inside else 0.07,
                    bar.get_y() + bar.get_height() / 2,
                    f"{value}/{denominator}", va="center",
                    ha="right" if inside else "left", fontweight="bold",
                    color="white" if inside and i == 2 else "black")
    axes[0].invert_yaxis()
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


def audit_breakdown(data: dict) -> None:
    """Attribute time outside computation in the separate 20-call diagnostic."""
    cohort = data["audit_diagnostic_b"]
    computation = cohort["mean_subprocess"]
    audit = cohort["mean_audit"]
    other = cohort["mean_total"] - computation - audit
    if other < 0:
        raise ValueError("Audit diagnostic components exceed the reported total.")
    fig, ax = plt.subplots(figsize=(3.35, 1.8))
    extra = cohort["mean_total"] - computation
    audit_pct = 100 * audit / extra
    other_pct = 100 * other / extra
    left = 0.0
    for value, shade in zip([audit_pct, other_pct],
                            ["#303030", "white"], strict=True):
        ax.barh(0, value, left=left, height=0.52,
                color=shade, edgecolor="black", linewidth=0.6)
        left += value
    ax.text(audit_pct / 2, 0, f"Audit persistence: {audit_pct:.1f}%",
            ha="center", va="center", fontsize=7.5, color="white")
    ax.annotate(f"Other: {other_pct:.1f}%", xy=(left - other_pct / 2, 0.28),
                xytext=(100, 0.65), ha="right", va="center", fontsize=7.5,
                arrowprops={"arrowstyle": "-", "lw": 0.6,
                            "connectionstyle": "angle,angleA=0,angleB=90"})
    ax.set_title("B cost beyond computation (20-call diagnostic)",
                 fontsize=8.5, fontweight="bold", pad=7)
    ax.set_xlim(0, 102)
    ax.set_ylim(-0.52, 0.92)
    ax.set_yticks([])
    ax.set_xlabel("Share of time outside the subprocess (%)")
    ax.set_xticks([0, 25, 50, 75, 100])
    ax.spines[["top", "right", "left"]].set_visible(False)
    fig.tight_layout()
    _save(fig, "audit-breakdown.pdf")


def main() -> None:
    """Generate every paper figure from the recorded evaluation values."""
    _configure()
    motivation()
    architecture()
    overhead()
    data = _application_metrics()
    application_effects(data)
    application_runtime(data)
    audit_breakdown(data)


if __name__ == "__main__":
    main()

