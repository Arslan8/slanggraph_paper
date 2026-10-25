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
