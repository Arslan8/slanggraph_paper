# Submission evidence checklist

Target: USENIX Security '27 Cycle 2. Registration is due January 19, 2027;
submission is due January 26, 2027 (Anywhere on Earth). The submission permits
13 pages of body text, unlimited references and appendices, and requires an Open
Science appendix.

## Evidence already incorporated

- Layered reference-monitor architecture at revision `53c5d317`, including the
  ten-class object inventory, single `HostRouter`, Cedar policy partitions, and
  namespace-free Landlock/seccomp/cgroup host design.
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

- Close or explicitly disposition the six implementation-review obligations in
  `docs/security/host-routing-completeness.md`. Do not claim whole-framework
  complete mediation while placement remains partial.
- Re-run `make security-verify` and the full `libs/prebuilt` format, lint, and
  test gates on the release revision; update the checked-in layered report.
- Run and report Landlock fresh-worker end-to-end latency and throughput on the
  accepted evaluation host. Do not extrapolate it from policy-only benchmarks or
  the retired bubblewrap path.
- Add dynamic slangGraph rows to E2. The current paper deliberately reports the
  existing third-party canaries, router evidence, and Linux tests separately.
- Complete AgentDojo, InjecAgent, and ASB parity runs or remove the prospective
  benchmark discussion. Never report unexecuted runs.
- Freeze and test the open object-class API, including resume reauthorization,
  effective-object binding, evidence cardinality, and waiver semantics.
- Re-run all numbers from a signed release tag and update the artifact revision.
- Produce a history-free anonymous artifact with a stable SEC27 URL.
- Add author names, affiliations, ORCIDs, acknowledgments, and the stable public
  artifact URL only for the camera-ready version.
