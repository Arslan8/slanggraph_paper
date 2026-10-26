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

Historical canaries, router/API certificates, Linux tests, and benchmark medians
retain their original source snapshots. They are not measurements of the latest
analysis runtime or object broker. The analysis validation record is reported
separately, including its unavailable-host failures. See
`SUBMISSION_CHECKLIST.md` for evidence still required. The plotted performance
medians remain historical hard-coded data, not a fresh experiment.

The low-level Landlock executor, object-broker worker, and deployment-backed
bubblewrap executor have different integration coverage. Do not transfer
activation, lifecycle, or performance claims between them. Source-body admission
does not certify imports or arbitrary Python, and runtime MAC is per interpreter
under trusted bootstrap. Policy and analysis extensions remain trusted.

Before submission, prepare a history-free anonymous artifact and replace the
placeholder Open Science URL. Keep author identity out of `main.tex`; preserve
ordinary attribution to prior work. Avoid em dashes in manuscript prose.
