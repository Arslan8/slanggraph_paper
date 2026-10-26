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
