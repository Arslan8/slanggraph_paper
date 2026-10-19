# Submission evidence checklist

Target: USENIX Security '27 Cycle 2. Registration is due January 19, 2027;
submission is due January 26, 2027 (Anywhere on Earth). The submission permits
13 pages of body text, unlimited references and appendices, and requires an Open
Science appendix.

## Evidence already incorporated

- Layered reference-monitor architecture at revision `53c5d317`, including the
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
- Run and report Landlock fresh-worker end-to-end latency and throughput on the
  accepted evaluation host. Do not extrapolate it from policy-only benchmarks or
  the separately implemented bubblewrap deployment path.
- Add dynamic slangGraph rows to E2. The current paper deliberately reports the
  existing third-party canaries, router evidence, and Linux tests separately.
- Complete AgentDojo, InjecAgent, and ASB parity runs or remove the prospective
  benchmark discussion. Never report unexecuted runs.
- Implement, freeze, and test the proposed open object-class API before reporting
  it as shipped. Cover parser/registry support, resume reauthorization,
  effective-object binding, evidence cardinality, and scoped runtime waivers.
- Preserve explicit policies and host-dependent outcomes. Distinguish valid
  tightening from an eligible obligation waiver; static-analysis waivers are
  not runtime permission to disable confinement.
- Replace hard-coded plotted medians with versioned measurement inputs carrying
  their backend, source revision, host, sample count, and dispersion. Keep
  publication/checkout, preparation, launch, and tool execution costs separate.
- Check page limits and anonymity independently of `make check`, which verifies
  only basic PDF integrity and embedded fonts.
- Re-run all numbers from a signed release tag and update the artifact revision.
- Produce a history-free anonymous artifact with a stable SEC27 URL.
- Add author names, affiliations, ORCIDs, acknowledgments, and the stable public
  artifact URL only for the camera-ready version.
