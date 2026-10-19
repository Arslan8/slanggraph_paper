"""Generate the evaluation figures used by the slangGraph paper."""

from __future__ import annotations

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
        (6.8, 3.9),
        2.6,
        1.0,
        "Tool\nimplementation",
        facecolor="#f2f2f2",
        fontsize=6.6,
    )
    _arrow(left, (2.4, 4.4), (3.5, 4.4))
    _arrow(left, (5.7, 4.4), (6.8, 4.4))
    _box(left, (5.8, 1.1), 1.9, 0.9, "payroll.csv\nREAD", edgecolor="#8c1d18")
    _box(left, (8.0, 1.1), 1.8, 0.9, "attacker.net\nSEND", edgecolor="#8c1d18")
    _arrow(left, (7.75, 3.9), (6.8, 2.0), color="#8c1d18")
    _arrow(left, (8.45, 3.9), (8.9, 2.0), color="#8c1d18")
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
        (6.8, 3.9),
        2.6,
        1.0,
        "Confined worker\nhost",
        facecolor="#bdbdbd",
        fontsize=6.5,
    )
    _arrow(right, (2.4, 4.4), (3.5, 4.4))
    _arrow(right, (5.7, 4.4), (6.8, 4.4))
    _box(right, (5.6, 1.1), 1.9, 0.9, "report/q3\nREAD", edgecolor="#1f5d3a")
    _box(right, (7.9, 1.1), 1.8, 0.9, "all other\nauthority", edgecolor="#8c1d18")
    _arrow(right, (7.75, 3.9), (6.55, 2.0), color="#1f5d3a")
    _arrow(right, (8.45, 3.9), (8.8, 2.0), color="#8c1d18")
    right.text(6.55, 0.35, "grant", ha="center", color="#1f5d3a", fontsize=7.2)
    right.text(8.8, 0.35, "DENY", ha="center", color="#8c1d18", fontsize=7.2, fontweight="bold")

    fig.subplots_adjust(wspace=0.16)
    _save(fig, "motivation.pdf")


def architecture() -> None:
    """Draw the layered slangGraph reference-monitor architecture."""
    fig, ax = plt.subplots(figsize=(7.0, 3.05))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8)
    ax.axis("off")

    _box(ax, (0.3, 6.3), 2.4, 0.9, "Model / subagent\n(untrusted intent)", facecolor="#f2f2f2")
    _box(ax, (3.25, 6.3), 3.0, 0.9, "HostRouter\nsingle refusing path", facecolor="#bdbdbd")
    _box(ax, (7.0, 6.3), 2.6, 0.9, "Policy\nDAC then forbids", facecolor="#e4e4e4")
    _box(ax, (10.4, 6.3), 3.1, 0.9, "Exact grant\n+ baseline authority", facecolor="#d2d2d2")
    _arrow(ax, (2.7, 6.75), (3.25, 6.75))
    _arrow(ax, (6.25, 6.75), (7.0, 6.75))
    _arrow(ax, (9.6, 6.75), (10.4, 6.75))

    framework_band = FancyBboxPatch(
        (0.3, 3.9),
        13.2,
        1.45,
        boxstyle="round,pad=0.025,rounding_size=0.035",
        facecolor="#f7f7f7",
        edgecolor="#5a5a5a",
        linewidth=0.8,
    )
    ax.add_patch(framework_band)
    ax.text(0.5, 5.02, "FRAMEWORK OBJECT MANAGER", fontsize=7.2, fontweight="bold", color="#4a4a4a")
    framework = ["dispatch", "registry", "state/store", "checkpoint", "model input", "output"]
    for index, label in enumerate(framework):
        x = 0.5 + index * 2.17
        _box(ax, (x, 4.15), 1.75, 0.62, label, facecolor="white", fontsize=6.6)
    _arrow(ax, (4.75, 6.3), (4.75, 5.35), color="#4a4a4a")

    host_band = FancyBboxPatch(
        (0.3, 1.15),
        13.2,
        1.75,
        boxstyle="round,pad=0.025,rounding_size=0.035",
        facecolor="#f7f7f7",
        edgecolor="#5a5a5a",
        linewidth=0.8,
    )
    ax.add_patch(host_band)
    ax.text(0.5, 2.57, "HOST ENFORCEMENT", fontsize=7.2, fontweight="bold", color="#4a4a4a")
    _box(ax, (0.5, 1.4), 2.35, 0.8, "Trusted parent\nresolve + lower", facecolor="#e4e4e4")
    _box(ax, (3.25, 1.4), 2.25, 0.8, "Fresh worker\nrelease barrier", facecolor="#bdbdbd")
    _box(ax, (5.9, 1.4), 2.05, 0.8, "Landlock\nobjects", facecolor="white")
    _box(ax, (8.35, 1.4), 2.05, 0.8, "seccomp\nsyscalls", facecolor="white")
    _box(ax, (10.8, 1.4), 2.35, 0.8, "cgroup / rlimit\nresources", facecolor="white")
    _arrow(ax, (11.95, 6.3), (11.95, 2.9), color="#4a4a4a")
    _arrow(ax, (2.85, 1.8), (3.25, 1.8))
    _arrow(ax, (5.5, 1.8), (5.9, 1.8))
    _arrow(ax, (7.95, 1.8), (8.35, 1.8))
    _arrow(ax, (10.4, 1.8), (10.8, 1.8))
    ax.text(
        7.0,
        0.45,
        "Activation receipt binds principal, request, grant, lowering, worker, and mechanisms before release",
        ha="center",
        fontsize=7.2,
        fontweight="bold",
    )
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
    ax.set_ylabel("Overhead vs. security disabled (%)")
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


def main() -> None:
    """Generate every paper figure from the recorded evaluation values."""
    _configure()
    motivation()
    architecture()
    overhead()


if __name__ == "__main__":
    main()
