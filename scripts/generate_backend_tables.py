from pathlib import Path
import hashlib
import json
root=Path(__file__).resolve().parents[1]
d=json.loads((root/'evidence/alternative_backends_summary.json').read_text())
if hashlib.sha256((root / d['source']).read_bytes()).hexdigest() != d['source_sha256']:
    raise ValueError('Alternative-backend source does not match its summary')
s=r'''\section{Alternative Backend Details}
\label{app:backend-details}

Tables~\ref{tab:common-authorizer} and~\ref{tab:execution-ablation} retain the
reported rounded timing aggregates. Each workload/mode has 100 measured calls
in five sessions. Added time and its 95\% interval use paired differences;
rounding can make the difference of displayed means differ by 0.001~ms.
Intervals use five session means, not individual calls. The mean ratio is a
point estimate; no ratio confidence interval is inferred.

The container image digest, source archives, and per-session observations are
named in the supplied report. The paper repository preserves that report
byte-for-byte and checks its hash before generating figures. Raw archives have
not yet been incorporated into the paper artifact; the tabulated intervals are
reported values, not independently recomputed intervals. Docker cpuset was
unavailable: taskset ran before Python startup and every worker's reported
CPU-0 affinity was checked. Container and host Python environments differ as
documented in the source report.

'''
labels={'constant_control':'Constant','read_32b':'Read 32 B','read_4kib':'Read 4 KiB','read_64kib':'Read 64 KiB','two_reads_32b':'Two reads','pandas_february':'Pandas replay','env_to_cat':'Native chain'}
def table(rows,label,caption):
    t=r'''\begin{table*}[t]
\centering
\small
\setlength{\tabcolsep}{3pt}
\begin{tabular*}{\textwidth}{@{\extracolsep{\fill}}llrrrrrrl@{}}
\toprule
Workload & Mode & Mean & SD & Median & P95 & Ratio & Added & Session 95\% CI \\
\midrule
'''
    previous=None
    for r in rows:
        if previous and previous!=r['workload']:t+=r'\addlinespace'+'\n'
        previous=r['workload']
        ci=r['session_ci_ms'];ci='n/a' if ci is None else f"[{ci[0]:.3f}, {ci[1]:.3f}]"
        delta='n/a' if r['added_ms'] is None else f"{r['added_ms']:.3f}"
        ratio='$'+f"{r['ratio_of_reported_means']:.3f}"+r'\times$'
        t+=f"{labels[r['workload']]} & {r['mode'].capitalize()} & {r['mean_ms']:.3f} & {r['sd_ms']:.3f} & {r['median_ms']:.3f} & {r['p95_ms']:.3f} & {ratio} & {delta} & {ci} \\\\\n"
    t+=r'\bottomrule'+'\n'+r'\end{tabular*}'+'\n'+f"\\caption{{{caption}}}\n\\label{{{label}}}\n"+r'\end{table*}'+'\n\n'
    return t
s+=table(d['comparison'],'tab:common-authorizer','Common production authorizer with different execution paths. All durations are milliseconds; ratios use the verified mean for the same workload. Static admission and container lifecycle are excluded.')
s+=table(d['application']+d['native_chain'],'tab:execution-ablation','Execution-only workloads. All durations are milliseconds; ratios use the plain-process mean. Neither workload includes Cedar, durable audit, or model calls. The native chain uses its separate exec-enabled profile.')
s+=r'''\paragraph{Operation variants.}
Figure~\ref{fig:operation-overhead} shows all 16 successful raw-API variants.
Compared with a fresh plain Python child, Landlock mean ratios range from
$0.998$ to $1.025\times$ and container ratios from $1.824$ to $1.894\times$.
All programs are rejected by the actual source-admission checker; rejected
programs are not given useful-operation timing results. The separately reported
body times include Python/API wrappers and open/close work, so are not pure
syscall overheads.

\begin{figure*}[t]
  \centering
  \includegraphics[width=\textwidth]{figures/operation-overhead.pdf}
  \caption{Added whole-call time for raw-operation variants, without Cedar or
  durable audit. Each mode/variant has 100 measured calls in five sessions.
  Whiskers are reported session-level 95\% intervals for paired increments.
  Panels use different x-axis ranges to expose Landlock's intervals around zero.}
  \label{fig:operation-overhead}
\end{figure*}

\paragraph{Lifecycle.}
The common-authorizer cohort creates ten containers: setup mean 1302.591~ms
(SD 70.392), teardown 1037.445~ms. The operation cohort creates five:
1197.466~ms (SD 74.900), teardown 1539.833~ms. The application cohort creates
five: 1720.825~ms (SD 1021.362), teardown 1501.668~ms. These are separate
lifecycle observations, not 100 invocation measurements or a measured cold-start
latency for every workload.

\paragraph{Verified controls.}
The report describes four control categories and 12/12 controls, each repeated
three times. Pending the raw ledger, we report the categories rather than
treating twelve as either distinct cases or a uniquely determined trial count.
Admission, binding, and allowed-read checks cover a different boundary from
the 49 forbidden host cases.

\paragraph{Historical cohorts.}
The earlier backend census found 0/49 effects for its two host conditions:
135 explicit denials, six generic SQLite errors, and six empty/absent results
per 147 trials. It is not the new Landlock/container census, which has 132
explicit-denial trials per adapter and a Landlock metadata effect.
Earlier synthetic host/trusted timings were $15.30$--$15.63\times$; the
production Linux/verified comparison ranged from $11.60\times$ to
$17.31\times$ but used
different policy frontends. The new common-authorizer experiment replaces that
comparison in the main argument. Historical source reports and aggregate JSON
remain archived; their absolute values, profiles, and sample counts are not
pooled with the new cohorts.
'''
(root/'sections/backend_evaluation.tex').write_text(s)
print('Backend appendix generated')

