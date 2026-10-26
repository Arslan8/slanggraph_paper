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
The motivation centers on preserving mandatory restrictions from manifest
requirements through invocation grants to actual effects. The manuscript now
covers sealed runtime MAC, restricted in-process admission, typed domain
mediators, SQLite record mediation, and the fixed-policy analysis/provenance
runtime. Table 1 is a capability matrix organized by policy/requirements, execution
enforcement, and composition. The motivation explains why call authorization,
process confinement, and flow policies need a shared invocation-grant contract;
it then identifies the independent analysis and resource extension interfaces.
Trust assumptions and coverage limits remain in the security model and evaluation.

Table 1 separately identifies language-based sandboxing. CaMeL receives credit
for its restricted orchestration interpreter; slangGraph receives credit for
admitted tool bodies using monitored APIs. The caption states those scopes.
Host lowering and dual execution paths remain separate capabilities.

The evaluation now centers on the supplied application study: one protected
Pandas computation integration, with SQL and Open Notebook baseline reproductions.
It compares the original subprocess sandbox, added authorization, and authorization
plus the bubblewrap executor. It separates controlled effects, deterministic
dispatch checks, model-driven injections, utility, 100-call computation replays,
a 20-call audit diagnostic, and five-run workflow observations.

The application source is WIP plus an archived working-tree overlay, not the WIP
commit alone. `evidence/application_macrobenchmarks_source.md` preserves the
supplied report byte-for-byte. Its raw samples, scripts, and source archive are
referenced by that report but are not included in this paper repository or present
at the reviewed WIP commit. No application experiment was rerun during this edit.

`sections/evaluation.tex` contains the main study, while
`sections/evaluation_appendix.tex` holds environment and reproduction details.
Historical canaries, router/API checks, Linux tests, and policy-only measurements
remain in `sections/component_evidence.tex` with their original snapshots.
The policy-overhead figure is historical, not the source of the application
timings. See `SUBMISSION_CHECKLIST.md` for remaining evidence requirements.

The main evaluation uses figures for containment, runtime, and the audit-cost
breakdown. Detailed outcome and latency tables remain in the appendix. The new
figures read `evidence/application_macrobenchmarks_summary.json`, which records
the source report's hash, cohort sizes, timer scopes, means, and SDs. The generator
checks that source hash. Runtime plots show ratios to upstream A within each
cohort, with SDs scaled by that same fixed baseline, not ratio confidence
intervals. The prose also reports percentage increases: B/A 104.2% and C/A
248.4% in replay; C/A 20.2% in the observed full workflow. The latter includes
model and runner effects and is not isolated enforcement overhead. No box plots
or raw distributions are inferred from the aggregates. The 20-call diagnostic
shows the percentage of B's non-computation time spent in audit writes and is
kept separate from the 100-call replay and five-run workflow cohorts.

The low-level Landlock executor, object-broker worker, and deployment-backed
bubblewrap executor have different integration coverage. Do not transfer
activation, lifecycle, or performance claims between them. Source-body admission
does not certify imports or arbitrary Python, and runtime MAC is per interpreter
under trusted bootstrap. Policy and analysis extensions remain trusted.

Before submission, prepare a history-free anonymous artifact and replace the
placeholder Open Science URL. Keep author identity out of `main.tex`; preserve
ordinary attribution to prior work. Avoid em dashes in manuscript prose.
