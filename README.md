# slangGraph paper

USENIX Security '27 paper source for slangGraph. The manuscript uses the
official USENIX LaTeX style and is anonymous by default.

```bash
make
make check
```

`make` regenerates the three vector figures with Matplotlib before building
the paper. The plotting source and currently hard-coded benchmark medians live
in `scripts/generate_figures.py`. Set `PYTHON=/path/to/python` to choose the
interpreter. `make check` verifies basic PDF readability and font embedding;
it does not certify venue page limits, anonymity, or evidence completeness.

The paper's implementation baseline is slangGraph revision `53c5d317`.
It distinguishes the namespace-free Landlock executor from the bubblewrap
executor that integrates OSTree tool/runtime deployments. General open object
classes remain a proposed language extension. Quantitative claims retain their
own recorded implementation revisions; policy-only and bubblewrap measurements
must not be attributed to Landlock. Static projections, fake-OSTree regression
tests, recorded development observations, and incomplete framework placement
are identified separately.

The first alignment revision also identifies deployment lifecycle work and the
recorded SGV107/SGV108 adapter findings. The router certificate and finite API
matrix do not establish a complete system verification pass. See
`SUBMISSION_CHECKLIST.md` for the code fixes and experiments still required.

Before submission, create a history-free anonymous artifact snapshot and replace
the placeholder Open Science URL. Do not put author names or affiliations in
`main.tex` while the submission is under double-blind review.
