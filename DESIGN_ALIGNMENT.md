# Manuscript alignment: October 25, 2026

Paper base: `0be042f8f80ee842ffe85cd8a034f0b2b80bd040`.
Implementation baseline: `Arslan8/slanggraph:wip`,
`40e24e978f9ec2e8f061abb21077e2251583f5e5`.

## Claims changed

- Motivation now connects a concrete SQLite record violation to three boundaries:
  native tool effects, resource semantics, and mandatory restrictions across local
  configuration and execution routes. The comparison is about enforcement scope,
  not a blanket claim that competitors lack MAC or cannot be extended.
- Resource classes and pump/SQLite/custom mediators are implemented, not proposed.
  SQLite supports a fixed record schema, not arbitrary SQL. Resource backends and
  protected-path configuration remain trusted.
- Runtime MAC is installed once or loaded from a protected directory and sealed.
  It rejects unsupported graph bodies, dispatchers, wrappers, and waivers. Scope
  is the configured interpreter under trusted bootstrap, not machine-wide MAC.
- In-process admission checks supported source bodies against manifests and
  approved monitored APIs. Imports and setup are trusted; arbitrary Python is
  unsupported. Confined workers retain a separate execution contract.
- Analysis provides immutable evidence, provenance, barriers, and scoped access.
  Policy is loaded before execution and does not change in response to findings.
  Conservative tracking does not establish classifier soundness or full coverage.
- Historical evaluation results retain their snapshots. New validation records
  are reported separately and include unavailable-host failures. The historical
  `langchain-forge` baseline is not the FORGE/SASY framework in the source review.

## Implementation evidence

All paths below are relative to the pinned implementation baseline:

| Claim | Evidence |
| --- | --- |
| Runtime MAC loading and sealing | `libs/langgraph/langgraph/_internal/_runtime_policy.py` |
| Boundary rejection and operator forbids | `libs/prebuilt/langgraph/prebuilt/security/mac.py`, `object_policy.py` |
| Runtime MAC regressions | `libs/prebuilt/tests/security/test_runtime_mac.py` |
| Source-body admission | `docs/security/manifest-consistency.md` |
| Resource classes, broker, SQLite contract | `docs/security/object-classes.md`, `workspace/README.md` |
| Analysis ownership and policy invariant | `docs/security/analysis/architecture.md`, `extension-contracts.md` |
| Flow propagation | `docs/security/analysis/information-flow.md` |
| Coverage and recorded validation | `docs/security/analysis/coverage.md`, `validation.md` |
| Historical wrapper identities | `eval/PINS.md` |
| Historical router/composition evidence | `docs/security/host-routing-completeness.md` |

## Comparison snapshots

- APF: `NVIDIA/agent-policy-fabric@77f5a23902fa5b47a059293c5a0074dfc3159690`.
- nono: `nolabs-ai/nono@8db15c939053374d9c6c6ad12365e25ee0552e95`,
  `docs/cli/features/tool-sandbox.mdx`.
- Sandlock: `multikernel/sandlock@620b2decd826d915edd818187244bf62ae25fe5d`.
- Progent source review: `lindsey98/progent@07eb84451d4a2ccff1643b6b50216c7e3c868584`,
  `secagent/progent_proxy.py`, lines 293–308. This is distinct from the historical
  canary source revision in `eval/PINS.md`.
- CaMeL: `google-research/camel-prompt-injection@f083b6b396399d3b3c7f2ddaf613a5945eaf32d8`,
  `src/camel/pipeline_elements/agentdojo_function.py`, lines 229–238.
- FORGE/SASY: `sasy-labs/sasy@7dc9e524c5b1979b91d16b9d573219e358a6c332`,
  `sdk/python/sasy/instrumentation/langchain.py`, lines 793–828.
- SEAgent: arXiv:2601.11893v1, trusted SDK threat model.

## Manuscript checks

Run `make` and `make check`. Inspect the rendered pages and architecture diagram.
Check the LaTeX source and extracted PDF text for em dashes, unresolved references,
and overflow. These are manuscript checks, not new implementation experiments.
The implementation's historical numerical results were not rerun for this edit.


## Motivation rewrite

The merged paper at `46fba24ee4a8f19f3f589ccff7629f05a01e648d` supplied the
unchanged design/evaluation baseline for this editorial revision.

The abstract, introduction, motivation, related-work framing, and conclusion now
center the missing reusable enforcement framework. Table 1 adapts the existing
motivation/literature ledger's feature matrix, including the same implementation
scope for grants/controls, invocation grants, dual tool paths, and independent
requirement producers. Column labels are written out instead of relying on ten
abbreviations. Configured sandbox boundaries are distinguished from grants derived
from manifest requirements and principal authorization.

The argument progresses through four requirements: bound effects inside tools;
mediate domain operations finer than host objects; retain mandatory restrictions
across local configurations; and allow new analyses to reuse those enforcers.
The reporting/database example connects each missing mechanism to a concrete
operation. The earlier audit-style escape-point table and proposed comparative
experiment were removed from the motivation. Their substantive scope constraints
remain in the security model, design, limitations, and submission checklist.

Writing references reread for structure, not additional novelty claims:

- [EC](https://arslan8.github.io/publications/ec.pdf): distinguish identifying
  protection domains from enforcing them, compare concrete capabilities, and
  derive design requirements from what the combination lacks.
- [Stateful Least Privilege Authorization for the Cloud, USENIX Security 2024](https://www.usenix.org/system/files/usenixsecurity24-cao-leo.pdf):
  connect an application need to missing authorization mechanisms and explain the
  benefit to the developer.
- [Endokernel, USENIX Security 2024](https://www.usenix.org/system/files/usenixsecurity24-yang-fangfei.pdf):
  connect concrete enforcement omissions to design requirements and a capability
  comparison. No security results from that paper are attributed to slangGraph.

No new security experiments or benchmark results were added by this rewrite.

## Reference-monitor grounding

The security model now follows EC Kernel (ECK), Section VI-B1, in presenting
complete mediation, tamperproofness, and verifiability as G1-G3. The citations
trace these requirements to Anderson's 1972 report and Jaeger's 2011
"Reference Monitor" entry, which EC itself cites. The additional monotonic
composition requirement is identified separately.

The discussion maps those obligations to tool effects, framework operations,
protected policy/grant/provenance state, and execution configuration. Verifiability
means assurance about the enforcement implementation. A runtime activation
receipt alone does not establish it. ECK's formal verification is attributed
only to ECK; slangGraph retains its reported component evidence and conditional
security argument.

Related work now cites EC's separation of compiler-driven compartment
identification from protected runtime enforcement. The analogy concerns
architecture, not reuse of ECK's hardware mechanism or verification results.

Sources checked:

- [EC, IEEE S&P 2023, Sections VI-B and VI-C](https://www.cs.purdue.edu/homes/dxu/pubs/SP23_EC.pdf).
- [Anderson, Computer Security Technology Planning Study, Volume II, Sections 3.4 and 4.1.1](https://csrc.nist.gov/files/pubs/conference/1998/10/08/proceedings-of-the-21st-nissc-1998/final/docs/early-cs-papers/ande72.pdf).
- [Jaeger, Reference Monitor, 2011](https://doi.org/10.1007/978-1-4419-5906-5_646).

## Application evaluation revision

The supplied application report is preserved byte-for-byte at
`evidence/application_macrobenchmarks_source.md` (SHA-256
`2126874e8a11cdddcdd8ac5125197788d6f21e7559f77d6567e3f9dc343afd7c`).
The source states WIP `40e24e9` plus working-tree modifications. The public WIP
tree does not contain the named application scripts/results or that source
archive. This manuscript revision transcribes the reported evidence; it does not
claim independent execution or raw-sample verification. The referenced archive,
hashes, policies, traces, and samples remain artifact-delivery requirements.

The main evaluation now answers containment, utility/integration, and runtime
questions through the Pandas A/B/C study. The prior component evaluation remains
in an appendix, with a short main-text synthesis. Abstract and limitations now
reflect the application results rather than presenting the historical 13.2%
policy-only result as the main performance finding.

Interpretation constraints preserved:

- Eight applications were screened, three baselines reproduced, one protected
  computation integration completed. Pandas and SQL share a repository.
- A keeps the upstream subprocess sandbox on the shared overlay; B adds a
  dispatch boundary; C adds the bubblewrap executor. This is not a native
  tool-dispatch ablation, a published-defense reproduction, or a Landlock result.
- Forbidden effects are reached in 3/3 supported probes in A/B and 0/3 in C.
  All 15 controlled-effect executions return the intended result. Private `/tmp`
  writes are allowed and excluded from that denominator; host containment does
  not establish output-directory-only guest writes.
- The initial three-task clean workload is 1/3 in every configuration. Later 5/5
  repeats select the known-working task and are not pooled with the original
  workload. The model-driven attack has zero eligible forbidden attempts in all
  configurations. Infrastructure failures are retained as a separate cohort.
- The 100-call replay, 20-call audit diagnostic, five-run workflow cohort, and
  single-observation startup values have distinct scopes. Paired SDs are taken
  from the supplied report, not reconstructed from marginal summaries.
- No box plot or distribution was synthesized from aggregate statistics. The
  attachment references runtime images and raw samples that were not attached;
  the manuscript plots reported counts and relative means with scaled SDs,
  with exact absolute summary tables retained in the appendix.
- New application citations identify upstream sources and revisions. Their
  commit identities were checked through GitHub, not used as evidence for
  experiments performed on the unavailable overlay.

Arithmetic checks confirm the reported mean differences and rounded ratios:
278.35 ms B-A, 663.74 ms C-A, 385.39 ms C-B; C/A = 3.48 in replay;
2.577 s C-A and 20.2% in the recorded full workflow; audit writes account for
98.1% of the diagnostic B remainder. No new performance/security result is
claimed from editing or building the paper.

## Language boundary and evaluation figures

Table 1 adds an independent language-sandbox column under execution enforcement.
Its definition is a restricted language and API set constraining executable agent
code, distinct from host lowering, policy-language evaluation, and having two
tool execution paths. CaMeL and slangGraph are both marked as implemented, with
different scopes stated in the caption:

- CaMeL's restricted interpreter executes orchestration code. Its AgentDojo
  adapter invokes the native tool through `runtime.run_function`, outside that
  interpreter. Evidence: the CaMeL paper Section 4.4 and pinned source
  `src/camel/interpreter/interpreter.py` and
  `src/camel/pipeline_elements/agentdojo_function.py` at `f083b6b`.
- slangGraph checks supported tool bodies against manifests and the approved
  monitored API vocabulary, then rechecks bindings at dispatch. Trusted setup,
  imports, and resource mediators remain outside the body certificate. Evidence:
  `docs/security/manifest-consistency.md` at WIP `40e24e9`.
- Other rows retain their reviewed integration scopes. A policy DSL is not an
  application-code sandbox. In particular, FORGE/SASY's `sasy-policy` compile
  and evaluator sandboxes isolate policy evaluation, not agent tool bodies;
  these are also OS-level mechanisms, not a restricted agent language.

Before the expanded backend report, the main paper had four figures and two tables.
Three evaluation figures
replace the main result tables: controlled-effect counts and retained computation,
two separately normalized runtime panels, and the separately measured B audit-cost
diagnostic. Detailed tables move to the application appendix. All plots read
`evidence/application_macrobenchmarks_summary.json`, whose source SHA-256 is
checked by the figure generator. Counts retain their distinct denominators.
Within each runtime panel, means and SDs are divided by the fixed upstream A
mean for that cohort. Error bars show scaled SDs, not ratio confidence intervals.
Replay ratios are B/A 2.04x, C/A 3.48x, and C/B 1.71x (104.2%, 248.4%, and
70.6% increases). Full-workflow C/A is 1.202x (20.2% increase), with its model,
startup, and tracing confounds preserved. Absolute timings and paired differences
remain in the appendix. The audit residual is computed as
544.34 - 265.09 - 273.94 = 5.31 ms; the plot shows audit/residual shares of
98.1%/1.9% of time outside B's subprocess. No nested span or separate cohort
is added to the replay totals. The historical deployment observation now also
states its relative cost, 1.47x (47.1%), alongside absolute means.

## Expanded evaluation report incorporated

The second supplied report is preserved byte-for-byte as
`evidence/paper_evaluation_source.md`, SHA-256
`4b993da71c49fdc1e9ac3cbc8062a0ddab066f56731731756d2d21593cdd9930`.
It extends, rather than replaces, the original application's numerical record.
`python3 scripts/import_backend_metrics.py` extracts its tables into
`evidence/backend_evaluation_summary.json`; the generator verifies the source
hash. Raw samples, linked images, sources.tar.gz, detailed admission diagnostics,
and inner-body timings were referenced but not supplied or found in public WIP.
No experimental rerun or raw-distribution reconstruction is claimed.

The main paper now has five figures and two tables. The security figure separates
Pandas's three distinct probes from E6's 49 operation/surface cases. The latter
reproduces all 49 effects in three repeats in the synthetic trusted/helper modes;
no forbidden effect appears in either host condition. Each host condition has
135 explicit denials, six generic SQLite errors, and six empty/absent results
across 147 trials, plus 30/30 positive-control trials. Only 45/49 cases establish
explicit denial. The synthetic direct-language frontend's 27/30 control
rejections are not attributed to production verified mode.

Three new runtime scopes remain separate:

- E6 runtime-v1: three successful workloads, four conditions, ten warmups and
  100 measured calls each; no model or durable audit, fresh workers, setup excluded.
  Host/trusted is 15.30-15.63x; paired differences and their SDs are retained.
- E6 operations-v1: 16 successful operation/API variants, five warmups and 50
  matched pairs each. Plain Python subprocess is the baseline. Whole-call cost
  is 12.53-15.88x, not per-syscall overhead. Whiskers use the paired-increment SD
  divided by the same fixed baseline mean; they are not ratio confidence intervals.
- E6 verified-v2: production cedar_security admission, binding validation and
  grant-checked read_text versus Linux execution. Both use real Cedar but have
  different policy frontends. Five warmups and 50 pairs per workload; reused
  executors, fresh host workers, separately timed setup. Ratios 11.60-17.31x
  apply only to the constant/read workloads; read sizes are not distinct APIs.

The exclusive backend partition identifies Cedar filtering as 65.8-66.2% of
host dispatch and worker execution/supervision as 24.4-24.9%. Public WIP source
`libs/prebuilt/langgraph/prebuilt/security/cedar.py` at `40e24e9` confirms temporary
policy/request files, CLI validation and per-rule authorization subprocesses.
This supports the mechanism description, not the reported timings. Other-invoke
remains a residual; stage variances are not summed. The application audit result
has a different denominator and cohort and is not added to this partition.

E1's 8 -> 4 -> 0 sink projection is included as projected 50%/100% reductions,
with its broader host model explicitly distinguished from the measured adapter.
The zero-attempt model-driven injection batch still has undefined enforcement
success and relative reduction. One protected application and two baselines
remain the port count. Artifact requirements now include backend source identity,
raw samples, setup/admission costs, capability degradation, races, and multi-host
and multi-task repetitions. The timing comparisons cannot be transferred between
Landlock, bubblewrap, object brokers, or an unmeasured release revision.
