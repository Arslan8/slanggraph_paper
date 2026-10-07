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

The paper is grounded in slangGraph revision
`c9164220c436be8a2e92cde3db19a2d3fcbadd7e`. Quantitative claims come from the
versioned evaluation artifact or from commands recorded in
`SUBMISSION_CHECKLIST.md`. Static capability projections are labeled as such;
they are not presented as runtime enforcement results.

Before submission, create a history-free anonymous artifact snapshot and replace
the placeholder Open Science URL. Do not put author names or affiliations in
`main.tex` while the submission is under double-blind review.
