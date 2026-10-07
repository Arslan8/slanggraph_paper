# Submission evidence checklist

Target: USENIX Security '27 Cycle 2. Registration is due January 19, 2027;
submission is due January 26, 2027 (Anywhere on Earth). The submission permits
13 pages of body text, unlimited references and appendices, and requires an Open
Science appendix.

## Evidence already incorporated

- Frozen Linux contract and A1--A8 acceptance evidence at implementation commit
  `96ef1df9`; documentation commit `c9164220`.
- Full `langgraph-prebuilt` suite: 518 passed on the accepted Linux host.
- Focused Linux and flow suite: 55 passed using real kernel integration where
  the claim depends on kernel behavior.
- E0 released-artifact checks: CaMeL 126/126, Progent parity 3/3, plus recorded
  package-import checks.
- E1 static sink census over eight deliberately vulnerable tools.
- E2 deterministic local canaries for no defense, Progent, Eydii, Forge,
  Nuggets, and the scoped CaMeL post-validation case.
- Matched hot-path benchmark on October 7, 2026: 593.701 us disabled,
  672.212 us cap-only, and 884.800 us with five no-op modules.

## Required before submission

- Run and report fresh-worker Linux end-to-end latency and throughput on the
  accepted evaluation host. Do not extrapolate it from policy-only benchmarks.
- Add dynamic slangGraph rows to E2. The current paper deliberately reports the
  existing third-party canaries and Linux contract tests separately.
- Complete AgentDojo, InjecAgent, and ASB parity runs or remove the prospective
  benchmark discussion. Never report unexecuted runs.
- Decide whether Cedar is part of the submitted implementation. The current
  manuscript accurately describes the shipped typed forbid backend and treats
  Cedar as a replaceable policy backend, not as shipped code.
- Re-run all numbers from a signed release tag and update the artifact revision.
- Produce a history-free anonymous artifact with a stable SEC27 URL.
- Add author names, affiliations, ORCIDs, acknowledgments, and the stable public
  artifact URL only for the camera-ready version.

