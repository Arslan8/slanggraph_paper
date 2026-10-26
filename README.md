# slangGraph paper

Anonymous USENIX-style manuscript for slangGraph.

Run `make check` to regenerate vector figures, compile LaTeX, and check PDF
readability and embedded fonts. Set `PYTHON=/path/to/python` if needed.
Manuscript checks do not execute framework experiments or establish venue compliance.

## Current framing

The paper centers the authority contract connecting fallible requirement proposals
to actual tool effects. Principal authorization and sealed operator MAC cap an
invocation grant; runtime APIs, semantic mediators, and host adapters enforce its
obligations. Exact, tightened, and unsupported lowering outcomes are explicit.
Requirement output may be untrusted data. Installed analyzer code, policy engines,
normalizers, mediators, and bootstrap remain trusted.

The paper proceeds from Introduction to Background and Threat Model, Motivation,
and Overview, followed by the detailed design. Background introduces LangGraph
execution and the adversary/TCB before the concrete motivation examples. The
overview states EC-grounded reference-monitor requirements (R1-R3), additional
design goals (D1-D4), the authority invariant, and cooperating component roles.
The introduction retains cited applications, incidents, runtime/companion/MCP
deployment forms, EC's separation of identification and enforcement, and Flask's
architecture.

| Design goal | Where the design addresses it | Evaluation scope |
| --- | --- | --- |
| D1: Unified policy across distributed enforcers | Shared dispatch, principal/MAC construction, sealed operator policy, and activation bound to the invocation grant | Controlled effect checks and component evidence; full composition remains conditional |
| D2: Flexible and faithful lowering | Runtime versus native paths, semantic mediators, capability assessment, explicit lowering outcomes, and Linux adapters | Admitted APIs, opaque native chain, and backend census; host-change and broker-composition ablations remain pending |
| D3: Low enforcement overhead | Language-based admission avoids worker launch/transport for supported tools while retaining authorization | Same-authorizer comparison on five constant/read workloads, complete application costs, and separately labeled execution-only costs |
| D4: Extensible enforcement | Requirement interface, analysis registry under fixed policy, typed resource classes, and adapter contracts | Implemented mechanisms; end-to-end independent-producer reuse remains unevaluated |

Goal references are stable LaTeX labels, used at the corresponding mechanisms,
in the security argument, and in evaluation. Low overhead is a design goal, not
a claim that every workload has low total cost. The language path remains
limited to admitted source bodies and monitored APIs.

The author will supply the overview figure. Add it as `figures/overview.pdf`;
the manuscript automatically prefers that file, and the generator does not
overwrite it. Until then, `figures/architecture.pdf` remains a provisional
diagram. Review the caption against the supplied figure before submission.

Table 1 credits IsolateGPT's process isolation and FIDES/CaMeL's precise flow
tracking. slangGraph's IFC cell is a half circle for instrumented/coarse coverage.
Related work also covers Conseca, AgentSpec, Capsicum, gVisor, and Firecracker.
APF receives credit for programmable grants, mandatory forbids, and extensible
policy projection. Its documented bundle-load projection is distinguished from
invocation-specific semantic/host obligations. The motivation uses APF's
documented missing-middleware-route condition, not a reproduced APF exploit.

## Evidence and reproducibility

The implementation design pin remains
`Arslan8/slanggraph:wip@40e24e978f9ec2e8f061abb21077e2251583f5e5`.
It does not by itself reproduce the evaluation overlays.

Three source reports are preserved byte-for-byte:

- `evidence/application_macrobenchmarks_source.md`: original protected Pandas
  study, baseline adaptations, corrected oracles, and separate cohorts.
- `evidence/paper_evaluation_source.md`: historical backend census, synthetic
  cost profiles, and the earlier comparison with different policy frontends.
- `evidence/alternative_backends_source.md`: new common-authorizer comparison,
  16 raw-operation variants, execution-only Pandas replay, Landlock/container
  census, container lifecycle, and a separate opaque native-chain profile.
  The two latest uploads were identical and count as one report.

The new summary is imported with
`python3 scripts/import_alternative_metrics.py`. Its source SHA-256 is
`a4068963b3ebb56c84ec7ce25cc77155989fec812cbdf2033d95a64bd595aa8f`.
The importer checks row counts, paired-increment rounding consistency, and trial
denominators. `python3 scripts/generate_backend_tables.py` regenerates the
new appendix tables. Figure generation checks source hashes and publishes PDFs
atomically. Text uses Times-compatible STIX fonts.

The new timing protocol has 100 calls per workload/mode: five sessions of 20,
with ten warmups and a separate first-use call per session. Confidence intervals
are reported Student-t intervals over five session mean paired differences.
Ratios use rounded reported means, not reconstructed raw measurements.

The Landlock and rootless-container adapters are evaluation implementations.
Their telemetry is not production activation evidence. Both use the same
production Cedar authorizer in the constant/read comparison: 3.62-4.92x and
5.98-8.37x verified-mode runtime. The raw-operation and application ablations
exclude Cedar and durable audit. The new Pandas Landlock point estimate is
+0.34%, with an increment interval that includes zero; this is not full-framework
overhead. The earlier complete replay remains 3.48x upstream and the observed
full workflow 1.202x, including model and runner effects.

The new census retains Landlock's metadata exposure: 1/49 forbidden cases,
versus 0/49 for the container, with 30/30 allowed trials per adapter. Each has
132 explicit-denial trials; generic errors and no-effect outcomes remain separate.
The old census's 135 explicit denials belong only to its historical cohort.
Native-chain checks use a distinct exec-enabled profile and do not establish
arbitrary-binary coverage or a Landlock process-count quota.

No experiment was rerun during this manuscript revision. Referenced raw samples,
source archives, full-precision CSVs, and a frozen release covering all claims
remain required artifact inputs. The student brief requests the missing
semantic/MAC/lowering/reuse experiments and additional protected workloads.

## Submission work

The current draft separates mechanism implementation, finite measurements,
source findings, and outstanding validation. General framework placement,
SQLite's fixed schema, per-interpreter MAC, trusted setup, and local receipt
assumptions remain explicit. See `SUBMISSION_CHECKLIST.md` for the remaining
release and artifact work and `DESIGN_ALIGNMENT.md` for the claim history.

Create the history-free anonymous artifact before replacing the Open Science
placeholder. Keep ordinary prior-work attribution; remove author-identifying
artifact history for submission. Avoid em dashes in manuscript prose.
