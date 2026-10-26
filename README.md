# slangGraph paper

Anonymous USENIX-style manuscript for slangGraph.

```bash
make
make check
```

`make` regenerates the vector figures with Matplotlib and builds the paper.
Set `PYTHON=/path/to/python` to select an interpreter. `make check` checks PDF
readability and font embedding, not venue compliance or evidence completeness.

The current design baseline is `Arslan8/slanggraph:wip` at
`40e24e978f9ec2e8f061abb21077e2251583f5e5` (October 25, 2026).
The introduction follows EC's progression from cited applications and concrete
failures to existing defenses, their enforcement boundaries, and the missing
system contract. Runtime functions, Chrome companion processes, and MCP servers
motivate three requirements: unified policy, host- and configuration-dependent
lowering, and composite distributed reference monitoring. The design uses Flask's
security-server/object-manager separation, with independent inference and
enforcement interfaces. The contributions are the common grant contract, host
adapters and composite lowering, and implementation and evaluation.

The motivation develops these requirements through one record-reporting example.
The manuscript covers sealed runtime MAC, restricted in-process admission, typed
domain mediators, SQLite record mediation, and the fixed-policy analysis/provenance
runtime. Table 1 is a capability matrix organized by policy/requirements, execution
enforcement, and composition. Prior systems receive credit for the boundaries they
actually enforce. Chrome and remote MCP illustrate deployment requirements, not
additional completed ports or experimental results.
Trust assumptions and coverage limits remain in the security model and evaluation.

Table 1 separately identifies language-based sandboxing. CaMeL receives credit
for its restricted orchestration interpreter; slangGraph receives credit for
admitted tool bodies using monitored APIs. The caption states those scopes.
Host lowering and dual execution paths remain separate capabilities.

The evaluation combines one protected Pandas computation integration, two
additional baseline adaptations, a 49-case backend operation census, and three
separate backend timing studies. The production verified-language comparison is
distinct from the synthetic helper condition. All timing comparisons lead with
percentages or runtime multiples, with absolute statistics in the appendices.

Evidence is archived without changing the supplied files:

- `evidence/application_macrobenchmarks_source.md` retains the original
  application study, including its oracle correction and separate cohorts.
- `evidence/paper_evaluation_source.md` adds the expanded report: 49-case census,
  100-call matched backend timings, an exclusive stage partition, 16 operation/API
  variants, and five production verified-versus-Linux workloads.
- The corresponding summary JSON files contain reported aggregates, not raw
  samples. Figure generation checks each report's SHA-256. To reimport a revised
  backend report after review, run `python3 scripts/import_backend_metrics.py`.

The source archives, raw samples, admission diagnostics, and body-timing records
referenced by these reports are not included in this paper repository or present
in the reviewed public WIP tree. No experiment was rerun during this manuscript
edit. The source commit alone does not identify the application working-tree
changes or substitute for the backend cohorts' frozen sources. Cedar CLI process
and serialization behavior was checked against the WIP implementation.

`sections/evaluation.tex` contains the main study, with environment and exact
application results in `sections/evaluation_appendix.tex` and backend protocol,
paired statistics, production-mode results, and the operation-overhead plot in
`sections/backend_evaluation.tex`. Historical component checks and policy-only
measurements remain in `sections/component_evidence.tex` at their original
snapshots. E1 exposure reductions are static projections, not executed blocking.

Five main figures and two tables cover the architecture, finite probe counts,
application runtime, backend and production-mode runtime, and measured cost
sources. Application replay costs are 2.04x for B/A and 3.48x for C/A; observed
full-workflow C/A is 1.202x, including model and runner effects. Synthetic host
cost is 15.30-15.63x its trusted baseline, and Linux is 11.60-17.31x the actual
verified mode on the five measured workloads. Different policy frontends prevent
interpreting the latter as a pure kernel-isolation tax.

Cost profiles keep their denominators separate: audit is 98.1% of application B's
non-subprocess time in the 20-call diagnostic; Cedar filtering is 65.8-66.2% of
total synthetic host dispatch without a durable audit sink. No cross-cohort
subtraction or unmeasured optimization speedup is claimed. Normalized whiskers
show SDs scaled by a fixed baseline, not confidence intervals. No raw distribution
is reconstructed. See `SUBMISSION_CHECKLIST.md` for the remaining evidence.

The low-level Landlock executor, object-broker worker, and deployment-backed
bubblewrap executor have different integration coverage. Do not transfer
activation, lifecycle, or performance claims between them. Source-body admission
does not certify imports or arbitrary Python, and runtime MAC is per interpreter
under trusted bootstrap. Policy and analysis extensions remain trusted.

Before submission, prepare a history-free anonymous artifact and replace the
placeholder Open Science URL. Keep author identity out of `main.tex`; preserve
ordinary attribution to prior work. Avoid em dashes in manuscript prose.
