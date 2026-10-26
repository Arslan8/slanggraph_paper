# Submission evidence checklist

Target: USENIX Security '27 Cycle 2. Registration is due January 19, 2027;
submission is due January 26, 2027 (Anywhere on Earth). The submission permits
13 pages of body text, unlimited references and appendices, and requires an Open
Science appendix.

## Current design alignment

Design snapshot: `40e24e978f9ec2e8f061abb21077e2251583f5e5` (WIP, October 25, 2026).

- Implemented open resource classes, typed mediator contracts, pump and SQLite
  record mediation; these are no longer merely proposed.
- Sealed operator runtime MAC, rejection of unsupported execution paths and
  waivers, and mandatory restricted in-process source admission.
- Replaceable analyzers, immutable policies, per-attempt snapshots, provenance
  propagation, scoped developer access, and tool/model/output policy integration.
- Analysis validation reported separately: 42 analysis tests and 123 regressions
  passed; full prebuilt run 3,701 passed, 58 host-unavailable failures, four skipped.
  This revision of the paper did not rerun those implementation tests.

## Application evidence incorporated

- The supplied report is archived in `evidence/application_macrobenchmarks_source.md`.
  Its experiments use WIP plus a frozen working-tree overlay. This editorial
  revision did not rerun the experiments or inspect the referenced raw samples.
- Eight applications screened from seven repositories; three local baselines
  from two repositories; only Pandas has a protected computation integration.
- A/B/C separates the upstream subprocess sandbox, added authorization, and
  authorization plus the bubblewrap executor. It is not a Landlock evaluation.
- The three supported forbidden probes succeed in A/B and are prevented in C;
  all 15 controlled-effect runs retain the legitimate result. Private `/tmp`
  writes are permitted, so a strict output-only guest-write policy is unsupported.
- Deterministic dispatch: 4/4 checks in B and C. One fixed model-driven injection:
  zero forbidden attempts in every configuration, not enforcement success.
- Initial utility: 1/3 tasks in every configuration. Later selected-task repeats:
  5/5 per configuration. Do not pool these cohorts.
- Replay: 100 measured calls each; B/A 2.04x (+104.2%), C/A 3.48x (+248.4%).
  The separate 20-call audit diagnostic identifies synchronous persistence cost.
  Five-run full-workflow C/A is 1.202x (+20.2%), including model and runner costs.

## Expanded backend evidence incorporated

- `evidence/paper_evaluation_source.md` preserves the new report. Its aggregate
  tables are imported into `evidence/backend_evaluation_summary.json`; source
  hashes are checked when generating figures. The archived report and JSON are
  not substitutes for raw samples, source archives, or admission diagnostics.
- E6 fixed census: 49/49 effects in both synthetic baselines across three repeats;
  0/49 in both host conditions, each retaining 30/30 positive-control trials.
  Of 147 forbidden trials per host condition, 135 show explicit denial, six a
  generic SQLite error, and six an empty/absent result. Only 45/49 cases support
  explicit blocking. Zero observed effect is not automatically an explicit denial.
- The synthetic direct-language frontend rejects 27/30 controls. It is distinct
  from the actual production verified mode; do not equate them or pool their data.
- Matched backend timings: three successful workloads, four conditions, ten
  warmups and 100 measured calls each. Host/trusted is 15.30-15.63x. No model or
  durable audit sink; fresh workers; construction/preflight excluded and separate.
- Exclusive backend stages: Cedar filtering 65.8-66.2%, worker 24.4-24.9% of total
  host dispatch. Temporary policy files, validation, and per-rule Cedar CLI
  subprocesses are confirmed in WIP code. Timings remain supplied measurements.
- Sixteen successful operation/API variants, five warmups and 50 matched pairs
  each: host/plain-Python whole-call ratios 12.53-15.88x. No per-syscall tax claim.
- Production verified-v2: five constant/read workloads, five warmups and 50
  paired samples; host/verified 11.60-17.31x. Both use real Cedar with different
  frontends; reused executors, fresh host workers. Broad API and application
  coverage cannot be inferred from these five workloads.
- E1 projections of 8 -> 4 -> 0 exposed sinks are static 50%/100% reductions;
  the host model is broader than the measured filesystem adapter.

## Historical evidence retained

- Earlier layered reference-monitor evidence at revision `53c5d317`, including the
  target ten-class object inventory, shared `HostRouter`, Cedar policy
  partitions, and separate Landlock and bubblewrap execution paths.
- Optional OSTree tool/runtime selection on the bubblewrap path, plus separately
  labeled development observations. Fake-OSTree tests and reported real-OSTree
  runs are not interchangeable evidence.
- Router certificate: 21 discovered, 21 obligated, and 21 verified entries under
  the checker's documented contracts.
- Tool API conformance: 15,744 passing cases in the checked-in report.
- Linux integration evidence for descriptor-bound Landlock rules, second-file
  denial, raw `open(2)`, descendants, `openat2` magic links, seccomp classes,
  activation receipts, and resource-control fallbacks.
- Historical frozen Linux milestone: 518 full-suite and 55 focused tests. The
  manuscript labels these as evidence for that revision, not the current
  Landlock backend.
- E0 released-artifact checks: CaMeL 126/126, Progent parity 3/3, plus recorded
  package-import checks.
- E1 static sink census over eight deliberately vulnerable tools.
- E2 deterministic local canaries for no defense, Progent, Eydii, Forge,
  Nuggets, and the scoped CaMeL post-validation case.
- Matched hot-path benchmark on October 7, 2026: 593.701 us disabled,
  672.212 us cap-only (13.2% overhead), and 884.800 us with five no-op modules
  (49.0% overhead).

## Required before submission

- Add the application study's exact source archive, working-tree hashes,
  manifests, policies, environment freezes, model digests, scripts, and raw
  samples to the reproducible artifact. The named application records are not
  in the reviewed public WIP tree; the source commit alone is insufficient.
- Archive and independently check the report builder's recomputation from raw
  application and backend traces. Preserve the failed launch
  cohort and corrected outside-fixture-write oracle, and link each table cell
  to its run IDs. Keep replay, audit diagnostic, workflow, and startup scopes
  separate. Do not reconstruct paired SDs or box plots from marginal summaries.
- Expand beyond one protected computation and the known-working February task:
  complete the frozen multi-task workload, resolve the initial utility failures,
  probe additional adversarial channels and host-capability degradation, and
  mediate SQL query/metadata and Notebook server/storage paths before counting
  them as protected ports. Add across-task uncertainty once tasks are available.
- Profile or optimize synchronous audit persistence and the repeated Cedar CLI
  policy path while preserving their contracts, then rerun the same successful
  workloads. No SSD, caching, embedded-engine, or uninstrumented speedup follows
  from the current measurements. Keep the two measured bottlenecks separate.
- Release the exact E6 source archives and map each host condition to its concrete
  executor, policy frontend, revision, and activation evidence. Include all stage
  samples, setup/static-admission costs, verifier rejection diagnostics, and
  operation-body timings; the supplied report references but does not include
  those raw records. Add multi-host and multi-task measurements and race tests.

- Create a claim ledger mapping each manuscript claim to a source revision,
  symbol or result file, backend, command, evidence type, and remaining
  assumptions. Historical test totals require their original collected command
  and snapshot; presence in the current tree is not a new execution result.
- Repair the recorded SGV107 backing-store read mediation and SGV108 checkpoint
  history authentication findings, including sync and async paths. Regenerate
  their evidence; source-pattern diagnostics are not executed bypass results.
- Resolve or explicitly scope the SGV901--SGV903 placement, adapter-composition,
  and host/isolation proof gaps. Do not claim whole-framework complete mediation
  from a passing router certificate or test count.
- Enforce disjoint release and channel identities in both deployment update
  APIs; reject attempts to overwrite published release names through a channel
  operation. Add tool and runtime regressions.
- Test real OSTree pruning with a commit retained only by an invocation or
  execution lease. Make durable retention visible to object pruning before
  claiming recovery survives cleanup. Cover retire/rebind/cleanup and races.
- Require a deployment manager for automatic lifecycle guarantees, or document
  and test a separate operator-retention contract for static specifications.
- Add a reproducible real-OSTree integration harness covering helper shadowing,
  runtime A/B/A, authenticated restart, signed and unsigned pulls, and cleanup.
  Report every host-dependent skip; the fake command's no-op prune cannot
  validate real object retention.
- Keep Landlock deployment support unimplemented in the capability matrix until
  selection, launch inputs, receipts, and lifetime management are connected and
  tested. A recorded digest alone is insufficient.
- Re-run `make security-verify` and the full `libs/prebuilt` format, lint, and
  test gates on the release revision; update the checked-in layered report.
- Validate the new frozen backend latency cohorts against their exact executor
  sources and repeat them on the release revision. Throughput remains unmeasured.
  Do not transfer a Linux-labeled result to Landlock, bubblewrap deployment, or
  object-broker paths without establishing the actual implementation identity.
- Add dynamic slangGraph rows to E2. The current paper deliberately reports the
  existing third-party canaries, router evidence, and Linux tests separately.
- Complete AgentDojo, InjecAgent, and ASB parity runs or remove the prospective
  benchmark discussion. Never report unexecuted runs.
- Freeze and rerun the implemented resource API and broker evidence. Cover
  parser/registry support, resume reauthorization, effective-object binding,
  protected-path overlap and aliases, exact per-request grants, cancellation, and
  unsupported requirements. Runtime MAC rejects enforcement waivers; keep that
  contract distinct from lower-level APIs that allow explicit degradation.
- Hold one mandatory rule fixed and test native tool reads, child execution,
  local overrides, broker substitutions, and alternate graph entry points. Include
  properly configured sandbox/broker baselines; document who can change policy.
- Evaluate the sealed runtime MAC path and analysis runtime together on supported
  graph shapes. Separate refusal of unsupported execution from useful support.
- Add held-out classifier accuracy, provenance propagation, failure/deadline, and
  public/internal destination experiments. Do not infer classifier soundness from
  scripted detections or full CaMeL/Progent compatibility from finite fixtures.
- Keep historical E2 `langchain-forge==0.2.0` (with `veritera==0.4.0`)
  distinct from the separately reviewed FORGE/SASY framework. `eval/PINS.md`
  records the package hashes; no FORGE/SASY execution result is claimed.
- Preserve explicit policies and host-dependent outcomes. Distinguish valid
  tightening from an eligible obligation waiver; static-analysis waivers are
  not runtime permission to disable confinement.
- Replace the historical policy plot's hard-coded medians with versioned raw
  measurement inputs. Application and backend figures read source-hash-bound
  reported aggregates, but raw traces still require artifact validation. Carry
  backend, source revision, host, sample count, and dispersion, and keep
  publication/checkout, preparation, launch, and tool execution costs separate.
- Check page limits and anonymity independently of `make check`, which verifies
  only basic PDF integrity and embedded fonts.
- Re-run all numbers from a signed release tag and update the artifact revision.
- Produce a history-free anonymous artifact with a stable SEC27 URL.
- Add author names, affiliations, ORCIDs, acknowledgments, and the stable public
  artifact URL only for the camera-ready version.

