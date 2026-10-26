# Security, ports, exposure reduction, and runtime overhead

This report separates application evidence, deterministic operation coverage, and timing experiments. It supersedes the E6-only narrative as the evaluation entry point. The evidence supports one experimental protected application integration, two further baseline adaptations, and five blocked candidates; it does not support eight completed ports.

## 1. Experimental configurations and host

Application A retains the released Pandas Python sandbox; B adds a ToolNode authorization boundary; C adds the Linux executor to that boundary while retaining the upstream sandbox program. E6 uses separate synthetic trusted/restricted-language conditions. The two sets must not be equated or pooled.

| Host field | Measured value |
| --- | --- |
| CPU | Intel(R) Xeon(R) w5-3435X; 1 socket; 16 cores/socket; 32 logical CPUs |
| RAM | 62.25 GiB |
| OS/kernel | Linux-6.17.0-1033-oem-x86_64-with-glibc2.39 |
| E6 runtime Python | 3.12.3 (main, Aug 31 2026, 10:18:26) [GCC 13.3.0] |
| Application Python | 3.13.11 (Pandas/SQL); 3.12.3 (Notebook) |
| GPUs | 2 x NVIDIA RTX A4000, 16,376 MiB each; driver 580.178.04 |
| bubblewrap | bubblewrap 0.9.0 |
| Timing CPU affinity | [0] (inherited by workers) |
| Evidence disk | ext4 on /dev/sda2, rotating ST12000NM000J |
| Model | local Ollama 0.32.14; Pandas qwen3:8b, Q4_K_M, temperature 0 |
| Benchmark clock | perf_counter_ns; monotonic wall duration |
| OS cache / CPU frequency | uncontrolled; no cache flush or fixed frequency |

[Current E6 host capture](e6/runtime-v1/host-before.json) records CPU, memory, affinity, load, block device, filesystem, GPU, and clock details. [Application host capture](../results/pandas-runtime-20261026-v1/host.json) belongs to its own cohort. The older HARDWARE.md describes an earlier kernel and must not override these run-level records. Runtime experiments make no model calls; GPUs are relevant only to application inference. The machine was not exclusively reserved; variation is measured, not assumed absent.

## 2. Port descriptions and evaluation scope

| Application / pin | Original execution and adaptation | Measured status / remaining boundary |
| --- | --- | --- |
| [Pandas](../apps/pandas/README.md), 4ffeb7f38178 | Original PandasDataAnalyst, wrangling and visualization graphs; local provider, fixture and backend adapter; B inserts dispatch, C runs original sandbox program in Linux worker | One experimental A/B/C integration; 1/3 original clean tasks succeeds in each condition; repeated February task succeeds. Parent/model/UI effects excluded. |
| [SQL](../apps/sql/README.md), 4ffeb7f38178 | Original SQLDatabaseAgent.ainvoke_agent, SQLAlchemy connection and safe_mode; synthetic sales/payroll DB | 3/3 baseline tasks pass; no protected port. Schema sampling and arbitrary SQL need mediation beyond the fixed-record broker. |
| [Notebook](../apps/notebook/README.md), a0f6f3081ae0 | Original ingestion API/worker, source_chat_graph, native Ollama and dedicated SurrealDB | 1/1 baseline smoke; no protected port. API/worker/DB authority is outside client confinement. |
| [Email](../apps/email/README.md), 758db7174223 | Archived Executive AI Assistant; Gmail integration | No completed smoke/port; dependency and dedicated-account blockers. |
| [Research](../apps/research/README.md), 1b7d2e80db9f | Archived Open Deep Research; search and structured model calls | No completed smoke/port; reproducible search/local model route missing. |
| [Coding](../apps/coding/README.md), ff4e713c094c | Open SWE, remote execution and GitHub/MDA services | No completed smoke/port; dedicated services and execution-host instrumentation missing. |
| [Newspaper](../apps/newspaper/README.md), 1c447b5672dd | GPT Newspaper search, writing and output workflow | No completed smoke/port; search service or frozen contract-preserving fixture missing. |
| [Finance](../apps/finance/README.md), 6c41ae8cf5fb | Historical LangGraph workflow selected after upstream removal | No verified smoke/port; provider fixture/local execution incomplete; no trading. |

Full immutable revisions and installation evidence are in the [intake ledger](../apps.csv). Pandas C replaces the outer subprocess launch because the host profile prohibits child creation; it retains AST/import/builtin/network checks and JSON transport. The original upstream files are unchanged, but adapters are substantive work, not zero-cost ports. SQL and Notebook retain their original graphs; replacing either with a demo broker would not constitute a faithful port. Engineering hours were not recorded. No overhead or security reduction is assigned to an unported app.

## 3. Security evaluation and exposure reduction

For a fixed eligible probe set P, observed reachability is the number of distinct probes producing the forbidden effect. Reduction is (baseline reachability - protected reachability) / baseline reachability. Repetitions test stability; they do not increase the number of independent probes.

| Evidence / denominator | Baseline | Protected | Exposure reduction and interpretation |
| --- | ---: | ---: | --- |
| Pandas controlled effects: two narrow reads + read-only dataset overwrite | A 3/3; B 3/3 | C 0/3 | 100% observed probe-reachability reduction for C; 0% for B |
| E6 fixed forbidden operation/surface cases | trusted 49/49; helper 49/49 | host 0/49; combined 0/49 | 100% observed reduction; explicit denial established for 45/49 cases |
| Pandas frozen CSV injection, five runs/configuration | 0/5 effects, 0 attempts | 0/5 effects, 0 attempts | Enforcement success and relative reduction undefined: no eligible attempts |
| E1 static headline sink projection | 8 exposed | host-model 4; composed-model 0 | 50% / 100% projected reduction; not measured runtime enforcement |

The [application controlled-effect evidence](application-pilot.md) preserves the legitimate February computation while adding one operation. Narrow/broad supplementary read policies supply a matched permitted control. Private-/tmp shadow writes are reported as host containment, not as proof of a guest-wide output-only policy. The three-probe denominator excludes that unsupported restriction. The four [dispatch checks](../results/pandas-dispatch-20261026-v1/summary.json) distinguish authorization from containment of an already-authorized tool; B/C each pass 4/4.

E6 exercises filesystem APIs, metadata, aliases, native/dynamic code, environment, processes, loopback networking, SQLite, and a bounded file-size limit on hidden, read-only and writable surfaces. All 49 baseline effects reproduce in all three repetitions. Both host conditions preserve 30/30 positive controls. Of 147 forbidden trials per host condition, 135 have an explicit denial, six generic SQLite errors, and six empty/absent results. The last 12 are not credited as explicit runtime blocking. The synthetic direct-language frontend rejects 27/30 controls; its zero effects are not evidence of useful complete mediation. See the [per-case matrix](e6/isolation-v1/report.md) and [protocol](../ISOLATION.md).

[E1](e1/exposure.md) projects adapter capabilities onto a static sink report. In particular, its host model includes capabilities that must not be attributed to the measured Linux filesystem adapter. Static sink counts, observed operation effects, and prompt-injection outcomes are different metrics.

## 4. Application runtime overhead and variance

These costs come from replaying the same recorded, successful February computation and inputs through A/B/C—not from E6 or a no-op. Each configuration has one first-use call, ten warm-ups and 100 measured calls; A/B/C order rotates by round. Fixture setup and integration initialization are excluded; dispatch, subprocess/host execution, synchronous audit, and integration evidence IO are included. Every result is checked to equal 120. Raw samples and nested spans were recomputed and checked against the saved summaries.

| Configuration | n | Mean ms | SD ms | Variance ms² | Median ms | P95 ms |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| A | 100 | 267.19 | 6.84 | 46.80 | 265.00 | 280.56 |
| B | 100 | 545.54 | 31.53 | 993.96 | 544.34 | 583.76 |
| C | 100 | 930.93 | 42.95 | 1844.46 | 916.64 | 1010.42 |

| Paired contrast | Mean increment ms | SD ms | Variance ms² | Ratio of means |
| --- | ---: | ---: | ---: | ---: |
| B-A | 278.35 | 32.91 | 1083.09 | 2.042x |
| C-A | 663.74 | 42.55 | 1810.20 | 3.484x |
| C-B | 385.39 | 54.98 | 3022.34 | 1.706x |

C adds 663.74 ms per replay relative to A: **248.4% overhead**, or 3.484x latency. C versus B adds 385.39 ms, or 70.6%. This is substantial; it cannot be described as negligible.

### Where the application overhead comes from

A/B spend 267.11/267.03 ms in the upstream subprocess. B's remaining 278.51 ms includes dispatch, authorization, and evidence. In a separate 20-call diagnostic, measured SqliteAuditSink.write spans average 273.94 ms (SD 32.12) for B and 274.52 ms (SD 8.96) for C. Audit persistence accounts for about 98% of B's non-subprocess time in that diagnostic. This is direct timing evidence for audit cost; rotating storage is recorded, but no SSD counterfactual was run.

In the 100-call C cohort, the executor averages 614.54 ms: grant compilation 20.56 ms; worker execution/supervision 325.58 ms; remaining executor work 268.41 ms. Another 316.39 ms lies outside the executor. The residual includes unseparated preparation, filtering, attestation and negotiation; do not call it measured kernel overhead. The new E6 decomposition below measures those stages explicitly in a separate backend cohort. Nested spans are never summed with their enclosing span. Different cohorts are not subtracted from each other.

Five full-workflow clean repetitions include model inference, setup, strace, and the oracle. These are separately reported in seconds:

| Condition | n | Mean s | SD s | Variance s² | Median s | Min-max s |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| A | 5 | 12.777 | 1.410 | 1.989 | 12.236 | 11.986-15.293 |
| B | 5 | 12.725 | 0.195 | 0.038 | 12.736 | 12.437-12.979 |
| C | 5 | 15.354 | 0.118 | 0.014 | 15.298 | 15.243-15.543 |

Full-workflow C/A is 1.202x (+20.2%), with paired increment 2.577 s (SD 1.446 s). This is an observed total-workflow difference, not isolated enforcement overhead. The first A run includes post-restart model loading and is retained. Five runs of one task do not estimate across-application variance. [Raw replay](../results/pandas-runtime-20261026-v1/), [audit diagnostic](../results/pandas-runtime-audit-profile-20261026-v1/), and [full-workflow cohort](../results/pandas-e2e-repetitions-20261026-attempt2/) remain separate. Thirty earlier server-unavailable launches are retained as infrastructure failures, not as successful defenses.

## 5. Matched backend overhead: new E6 runtime experiment

The previous median over mixed successes and rejections was not a valid overhead estimate. This new experiment uses only three successful workloads: arithmetic, canary-file read, and 4 KiB write. For each workload/condition there are ten warm-ups and 100 measured calls plus a separately retained first-use call. Order is shuffled within each paired round with seed 20261026. Each call starts a fresh worker; executor construction/preflight is outside the dispatch timer and recorded separately. No model or durable audit sink is involved. The same positive oracle must pass for every timing sample.

| Workload | Condition | n | Mean ms | SD ms | Variance ms² | Median ms | P95 ms |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| arithmetic | trusted | 100 | 28.14 | 3.18 | 10.12 | 28.85 | 31.15 |
| arithmetic | language_helper | 100 | 28.14 | 2.98 | 8.89 | 28.99 | 31.59 |
| arithmetic | host | 100 | 430.63 | 50.82 | 2582.42 | 445.93 | 480.34 |
| arithmetic | host_language_helper | 100 | 428.47 | 50.30 | 2530.32 | 445.78 | 476.11 |
| allowed_read | trusted | 100 | 27.72 | 3.52 | 12.37 | 28.97 | 31.15 |
| allowed_read | language_helper | 100 | 28.10 | 3.43 | 11.74 | 29.09 | 31.27 |
| allowed_read | host | 100 | 433.31 | 45.59 | 2078.02 | 447.36 | 478.07 |
| allowed_read | host_language_helper | 100 | 431.74 | 49.10 | 2411.28 | 448.03 | 481.50 |
| allowed_small_file | trusted | 100 | 27.92 | 3.50 | 12.27 | 29.12 | 31.96 |
| allowed_small_file | language_helper | 100 | 28.16 | 3.26 | 10.60 | 29.09 | 31.50 |
| allowed_small_file | host | 100 | 433.61 | 52.87 | 2795.11 | 447.99 | 491.47 |
| allowed_small_file | host_language_helper | 100 | 431.19 | 49.51 | 2451.25 | 446.89 | 481.22 |

| Workload | Paired contrast | Increment ms | SD ms | Variance ms² | Overhead |
| --- | --- | ---: | ---: | ---: | ---: |
| arithmetic | host-trusted | 402.49 | 48.52 | 2354.13 | 1430.2% |
| arithmetic | host_language_helper-language_helper | 400.33 | 48.69 | 2370.87 | 1422.6% |
| arithmetic | host_language_helper-host | -2.16 | 34.06 | 1160.10 | -0.5% |
| allowed_read | host-trusted | 405.59 | 43.06 | 1854.05 | 1463.4% |
| allowed_read | host_language_helper-language_helper | 403.64 | 46.73 | 2183.56 | 1436.6% |
| allowed_read | host_language_helper-host | -1.57 | 32.98 | 1087.41 | -0.4% |
| allowed_small_file | host-trusted | 405.69 | 50.68 | 2568.25 | 1452.9% |
| allowed_small_file | host_language_helper-language_helper | 403.03 | 47.80 | 2284.60 | 1431.3% |
| allowed_small_file | host_language_helper-host | -2.43 | 31.65 | 1001.60 | -0.6% |

### Measured source of backend cost

The following exclusive partition sums to the host dispatch total. Each stage is measured by wrapping the production method without changing enforcement. Policy is the CedarPolicyBackend.filter span: the production backend writes policy/request files, validates with the Cedar CLI, and launches an authorize command for each evaluated rule. This is policy-engine/serialization/process cost, not kernel sandbox overhead. See [the measured implementation](../../libs/prebuilt/langgraph/prebuilt/security/cedar.py). Other-invoke is an arithmetic residual, not a named measured mechanism. Worker includes launch, confinement activation, execution, result handling and teardown. The combined language/host stage results are retained in summary.json.

| Workload | Stage | Mean ms | SD ms | Share of dispatch |
| --- | --- | ---: | ---: | ---: |
| arithmetic | attest | 7.621 | 0.423 | 1.8% |
| arithmetic | grant | 7.764 | 0.432 | 1.8% |
| arithmetic | negotiate | 23.643 | 6.990 | 5.5% |
| arithmetic | other_invoke | 0.361 | 0.053 | 0.1% |
| arithmetic | outside_invoke | 0.949 | 0.149 | 0.2% |
| arithmetic | policy | 285.193 | 34.782 | 66.2% |
| arithmetic | worker | 105.096 | 12.909 | 24.4% |
| allowed_read | attest | 7.604 | 0.383 | 1.8% |
| allowed_read | grant | 7.804 | 0.494 | 1.8% |
| allowed_read | negotiate | 23.495 | 4.041 | 5.4% |
| allowed_read | other_invoke | 0.370 | 0.047 | 0.1% |
| allowed_read | outside_invoke | 1.049 | 0.361 | 0.2% |
| allowed_read | policy | 285.139 | 31.127 | 65.8% |
| allowed_read | worker | 107.848 | 12.597 | 24.9% |
| allowed_small_file | attest | 7.672 | 0.592 | 1.8% |
| allowed_small_file | grant | 7.776 | 0.449 | 1.8% |
| allowed_small_file | negotiate | 23.349 | 4.295 | 5.4% |
| allowed_small_file | other_invoke | 0.372 | 0.056 | 0.1% |
| allowed_small_file | outside_invoke | 1.001 | 0.257 | 0.2% |
| allowed_small_file | policy | 286.062 | 36.010 | 66.0% |
| allowed_small_file | worker | 107.382 | 14.616 | 24.8% |

For the matched read workload, policy filtering accounts for 285.14 ms (65.8%) of host dispatch; worker execution/supervision accounts for 107.85 ms (24.9%). The dominant measured backend cost is policy filtering, not simply worker launch. Across these tiny operations host latency is nearly constant, so fixed per-call work dominates useful computation.

Policy and worker spans also have the largest stage-level SDs. Their variances must not be added: correlated timing fluctuations contribute covariance. Paired-overhead SD is computed from same-round differences. Small negative host+helper versus host differences are within variation and do not establish a speedup. This pinned-CPU, instrumented cohort differs from the earlier unrestricted-affinity security census; its timings are not pooled with the old mixed-outcome medians.

| Workload | Host setup/preflight mean ms | SD ms |
| --- | ---: | ---: |
| arithmetic | 30.52 | 2.51 |
| allowed_read | 30.72 | 2.46 |
| allowed_small_file | 30.61 | 2.93 |

[Runtime plan](e6/runtime-v1/plan.json), [raw samples](e6/runtime-v1/samples.jsonl), [derived statistics](e6/runtime-v1/summary.json), and [source archive](e6/runtime-v1/sources.tar.gz) identify the exact experiment. Small instrumentation costs are included; no uninstrumented speedup is inferred. These are sequential within-host timing observations, not independent tasks; SD/variance describe observed jitter. No unsupported IID confidence interval or population-level ASR is reported.

![Security reachability and paired runtime distributions](evaluation-summary.png)

## 6. Per-operation microbenchmarks

The expanded backend microbenchmark uses 16 operation/API variants and 50 matched samples per variant after five warm-ups. Every call must complete its intended operation in both modes. The baseline is a plain Python subprocess; it is neither statically verified language mode nor the Pandas application sandbox. Every host invocation launches a fresh worker. The table measures whole-call overhead, not overhead added to each syscall.

| Operation | Python mean ms | Host mean ms | Paired overhead ms | Overhead SD ms | Overhead variance ms² | Host/Python |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| compute_control | 27.35 | 415.82 | 388.47 | 41.21 | 1698.07 | 15.20x |
| open_read | 27.71 | 419.09 | 391.39 | 34.62 | 1198.26 | 15.13x |
| pathlib_read | 32.96 | 413.02 | 380.06 | 48.81 | 2382.69 | 12.53x |
| os_read | 27.28 | 417.45 | 390.17 | 40.02 | 1601.26 | 15.30x |
| mmap_read | 27.61 | 420.91 | 393.30 | 38.64 | 1493.07 | 15.25x |
| ctypes_read | 30.32 | 409.75 | 379.43 | 43.42 | 1885.08 | 13.51x |
| stat_metadata | 26.53 | 421.31 | 394.78 | 41.89 | 1755.06 | 15.88x |
| listdir_names | 27.67 | 412.79 | 385.12 | 40.29 | 1623.54 | 14.92x |
| write | 26.70 | 416.33 | 389.64 | 41.48 | 1720.50 | 15.60x |
| append | 27.15 | 409.88 | 382.72 | 44.73 | 2000.88 | 15.10x |
| truncate | 27.57 | 415.87 | 388.30 | 40.25 | 1620.18 | 15.09x |
| create | 27.18 | 419.69 | 392.51 | 34.74 | 1206.78 | 15.44x |
| unlink | 27.29 | 415.49 | 388.21 | 44.82 | 2009.24 | 15.23x |
| mkdir | 27.42 | 410.84 | 383.42 | 42.82 | 1833.56 | 14.98x |
| write_4kib | 27.44 | 413.37 | 385.92 | 43.30 | 1875.14 | 15.06x |
| fsync | 28.16 | 426.57 | 398.41 | 34.87 | 1215.60 | 15.15x |

The inner timer separately measures operation statements after imports, excluding compilation, startup, policy evaluation and transport. It includes Python wrappers, open/close and user-space work; it is not pure syscall time. [Body timing, stage breakdown and scope](e6/operations-v1/report.md) and [full-precision CSV](e6/operations-v1/operations.csv) accompany the [raw samples](e6/operations-v1/samples.jsonl). No denial is passed off as a faster successful operation; unsupported child-exec chains, network operations and metadata mutations are listed explicitly in the report.

![Per-operation overhead and body time](e6/operations-v1/operations.png)

## 6a. Actual source-verified language execution versus Linux

This is the direct production-mode comparison. The verified condition uses cedar_security admission, runtime binding validation and grant-checked read_text. Both conditions use real Cedar authorization. Fifty paired samples follow five warmups. Setup/static admission is timed separately. Executors are reused; host workers are fresh. Read sizes are workload variants, not distinct APIs.

| Workload | Verified mean ms | Host mean ms | Paired added ms | Added SD ms | Host/verified |
| --- | ---: | ---: | ---: | ---: | ---: |
| constant_control | 18.479 | 319.774 | 301.295 | 36.116 | 17.31x |
| read_32b | 28.466 | 330.207 | 301.740 | 37.792 | 11.60x |
| read_4kib | 27.830 | 331.581 | 303.751 | 34.993 | 11.91x |
| read_64kib | 27.344 | 360.600 | 333.256 | 40.938 | 13.19x |
| two_reads_32b | 28.130 | 330.491 | 302.361 | 35.602 | 11.75x |

[Full production comparison, static admission costs and policy/execution breakdown](e6/verified-v2/report.md). The two executors have different policy frontends; their total difference is implementation overhead, not a pure kernel isolation tax. Raw API probes from the previous 16-operation experiment are submitted to the actual verifier and rejection diagnostics are saved. Rejected operations receive no successful-operation runtime. Broad typed-resource ports and a verified-mode application port remain necessary for broader claims.

## 7. Claim boundaries and reproduction

The remaining publication gaps are substantive: multiple fully protected application ports, a frozen multi-task workload, successful model-driven attack attempts, broader verified-language operation coverage, capability-degradation tests, races, and multi-host measurements. The existing evidence does not justify filling those cells with zeroes or calling candidates completed ports. Kernel exploits, service authorization and cross-session flow are not covered by file-operation denial. Every number here refers to its stated finite corpus.

```sh
cd eval
uv run python -m slanggraph_eval.isolation.runtime \
  --samples 100 --warmup 10 --output reports/e6/runtime-new
uv run python scripts/paper_evaluation.py
```

The report builder uses the named frozen cohorts above, checks the old replay statistics against raw samples, recomputes the E6 summary and paired deltas, and writes input hashes to evaluation-metrics.json. To analyze another cohort, select its path explicitly; never overwrite an existing run directory.
