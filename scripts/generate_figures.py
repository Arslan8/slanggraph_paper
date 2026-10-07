"""Generate the evaluation figures used by the slangGraph paper."""

from __future__ import annotations

from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch, Rectangle


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


def expressiveness() -> None:
    """Plot the qualitative feature matrix from the published designs."""
    systems = ["Progent", "SEAgent", "CaMeL", "slangGraph"]
    features = [
        "Tool\nDAC",
        "Argument\nrules",
        "History /\nflow",
        "Restrictive\nstack",
        "Monotonic\nnarrowing",
        "Delegation",
        "Hostile-tool\nconfinement",
        "Portable\nadapters",
        "Activation\nevidence",
    ]
    # 0 = absent, 0.5 = narrower/partial model, 1 = provided.
    values = np.array(
        [
            [0, 1, 0.5, 0, 1, 0.5, 0, 0, 0],
            [0, 1, 1, 0, 0, 1, 0, 0, 0],
            [0, 1, 1, 0, 0.5, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 1, 1],
        ],
        dtype=float,
    )

    fig, ax = plt.subplots(figsize=(7.0, 2.15))
    fills = {0.0: "white", 0.5: "#a6a6a6", 1.0: "#202020"}
    ax.set_xlim(-0.5, len(features) - 0.5)
    ax.set_ylim(len(systems) - 0.5, -0.5)
    ax.set_xticks(np.arange(len(features)), labels=features)
    ax.set_yticks(np.arange(len(systems)), labels=systems)
    ax.tick_params(top=True, bottom=False, labeltop=True, labelbottom=False, length=0)

    for row in range(values.shape[0]):
        for column in range(values.shape[1]):
            value = values[row, column]
            ax.add_patch(
                Rectangle(
                    (column - 0.5, row - 0.5),
                    1,
                    1,
                    facecolor=fills[value],
                    edgecolor="black",
                    linewidth=0.45,
                )
            )
            label = "Y" if value == 1 else "P" if value == 0.5 else "--"
            color = "white" if value == 1 else "black"
            ax.text(column, row, label, ha="center", va="center", color=color)

    for spine in ax.spines.values():
        spine.set_linewidth(0.6)

    legend = [
        Patch(facecolor="#202020", edgecolor="black", label="Y: provided"),
        Patch(facecolor="#a6a6a6", edgecolor="black", label="P: narrower model"),
        Patch(facecolor="white", edgecolor="black", label="--: not provided"),
    ]
    ax.legend(handles=legend, loc="upper center", bbox_to_anchor=(0.5, -0.17), ncol=3)
    _save(fig, "expressiveness.pdf")


def exposure() -> None:
    """Plot exposed sinks for the E1 static mediation models."""
    labels = [
        "None",
        "Three LangChain wrappers",
        "Progent",
        "CaMeL (generous tag model)",
        "slangGraph policy only",
        "slangGraph host adapter",
        "slangGraph composed adapters",
    ]
    exposed = [8, 8, 7, 0, 8, 4, 0]
    projected = [False, False, False, False, False, True, True]
    y = np.arange(len(labels))

    fig, ax = plt.subplots(figsize=(3.35, 2.65))
    bars = ax.barh(
        y,
        exposed,
        color=["#303030" if not item else "#bdbdbd" for item in projected],
        edgecolor="black",
        linewidth=0.6,
        hatch=["" if not item else "///" for item in projected],
        height=0.68,
    )
    ax.set_yticks(y, labels=labels)
    ax.invert_yaxis()
    ax.set_xlim(0, 8.8)
    ax.set_xticks(range(0, 9, 2))
    ax.set_xlabel("Exposed implementation sinks (of 8)")
    ax.grid(axis="x", color="#d0d0d0", linewidth=0.5)
    ax.set_axisbelow(True)
    ax.spines[["top", "right"]].set_visible(False)
    for bar, value in zip(bars, exposed, strict=True):
        ax.text(max(value, 0) + 0.15, bar.get_y() + bar.get_height() / 2, str(value), va="center")

    legend = [
        Patch(facecolor="#303030", edgecolor="black", label="Static mediation model"),
        Patch(facecolor="#bdbdbd", edgecolor="black", hatch="///", label="Adapter projection"),
    ]
    ax.legend(handles=legend, loc="lower right", frameon=False)
    _save(fig, "exposure.pdf")


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
    expressiveness()
    exposure()
    overhead()


if __name__ == "__main__":
    main()
