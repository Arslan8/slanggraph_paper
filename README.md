# slangGraph paper

USENIX Security '27 paper source for slangGraph. The manuscript uses the
official USENIX LaTeX style and is anonymous by default.

```bash
make
make check
```

`make` regenerates the vector evaluation figures with Matplotlib before building
the paper. The plotting source and recorded inputs live in
`scripts/generate_figures.py`.

The paper's current architecture is grounded in slangGraph revision `53c5d317`
and the accompanying object-class design work. Quantitative claims retain their
own recorded implementation revisions; the manuscript does not attribute an
older bubblewrap measurement to the current Landlock backend. Static capability
projections and incomplete framework placement are labeled explicitly rather
than presented as runtime enforcement or whole-system results.

Before submission, create a history-free anonymous artifact snapshot and replace
the placeholder Open Science URL. Do not put author names or affiliations in
`main.tex` while the submission is under double-blind review.
