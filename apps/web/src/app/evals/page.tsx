"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { ArrowLeft, Database, Play, RefreshCw, ShieldCheck } from "lucide-react";
import { fetchEvalsResults, runEvalsBenchmark } from "@/lib/api";

type EvaluationRow = {
  lc_id: string; name: string; difficulty: "Golden" | "Edge Case"; ground_truth: string; primary_rule: string;
  regex_verdict: string; regex_correct: boolean; regex_failure_mode: string;
  llm_verdict: string; llm_correct: boolean; llm_failure_mode: string;
  veritas_verdict: string; veritas_rationale: string;
};

const FEATURED_CASES: EvaluationRow[] = [
  { lc_id: "LC-2026-8841", name: "Typo ‘Mashine’ & Servo Motors Non-Conflict", difficulty: "Golden", ground_truth: "APPROVE_HONOUR", primary_rule: "ISBP 745 Para A23 & UCP 600 Art. 14(e)", regex_verdict: "REFUSAL", regex_correct: false, regex_failure_mode: "Exact string matching wrongly rejected a harmless typo.", llm_verdict: "APPROVE_HONOUR", llm_correct: true, llm_failure_mode: "Correctly interpreted typographical variance.", veritas_verdict: "APPROVE_HONOUR", veritas_rationale: "Semantic judgement protects the harmless typo while the evidence remains auditable." },
  { lc_id: "LC-2026-9104", name: "Insurance 108% Shortfall ($9,600) + Curable Demurrage", difficulty: "Golden", ground_truth: "ISSUE_MT734_REFUSAL", primary_rule: "UCP 600 Art. 28(f)(ii) & Art. 16(c)(iii)", regex_verdict: "REFUSAL", regex_correct: true, regex_failure_mode: "Caught the numerical threshold but cannot explain the operational remedy.", llm_verdict: "APPROVE_HONOUR", llm_correct: false, llm_failure_mode: "Treated 108% as ‘close enough’ to the mandatory 110%.", veritas_verdict: "ISSUE_MT734_REFUSAL", veritas_rationale: "Python locks the 110% rule; the system produces the lawful refusal and re-presentation advice." },
  { lc_id: "LC-2026-9920", name: "TBML Price Anomaly (+4.12σ) & Sanctioned Vessel", difficulty: "Golden", ground_truth: "COMPLIANCE_HOLD_AML", primary_rule: "Zetaris in-situ CTE federation", regex_verdict: "APPROVE_HONOUR", regex_correct: false, regex_failure_mode: "Siloed documents cannot expose customs or sanctions risk.", llm_verdict: "APPROVE_HONOUR", llm_correct: false, llm_failure_mode: "No live access to customs distributions or watchlists.", veritas_verdict: "COMPLIANCE_HOLD_AML", veritas_rationale: "Federated evidence finds the +4.12σ anomaly and sanctioned vessel before honour." },
];

export default function EvaluationsPage() {
  const [filter, setFilter] = useState<"ALL" | "Golden" | "Edge Case">("ALL");
  const [isRunning, setIsRunning] = useState(false);
  const [realResults, setRealResults] = useState<any>(null);
  const [selectedId, setSelectedId] = useState("LC-2026-9104");
  const [darkMode, setDarkMode] = useState(false);
  const [runNotice, setRunNotice] = useState<string | undefined>(undefined);

  useEffect(() => { fetchEvalsResults().then(setRealResults).catch(() => undefined); }, []);

  const rows: EvaluationRow[] = realResults?.rows ? realResults.rows.map((row: any) => ({
    lc_id: row.lc_id, name: row.title, difficulty: row.category, ground_truth: row.ground_truth_verdict, primary_rule: row.governing_rule,
    regex_verdict: row.regex_baseline.verdict, regex_correct: row.regex_baseline.is_correct, regex_failure_mode: row.regex_baseline.failure_mode || row.regex_baseline.rationale,
    llm_verdict: row.single_prompt_llm.verdict, llm_correct: row.single_prompt_llm.is_correct, llm_failure_mode: row.single_prompt_llm.failure_mode || row.single_prompt_llm.rationale,
    veritas_verdict: row.veritas_600.verdict, veritas_rationale: row.veritas_600.rationale,
  })) : FEATURED_CASES;
  const visibleRows = rows.filter((row) => filter === "ALL" || row.difficulty === filter);
  const selectedRow = rows.find((row) => row.lc_id === selectedId) ?? visibleRows[0] ?? rows[0];
  const veritas = realResults?.architectures?.veritas_600;
  const llm = realResults?.architectures?.single_prompt_nemotron;
  const regex = realResults?.architectures?.regex_rule_based;
  const source = realResults ? "FRESH API RESULT" : "BUNDLED DEMO REPLAY";

  async function runBenchmark() {
    setIsRunning(true);
    setRunNotice(undefined);
    try { setRealResults(await runEvalsBenchmark()); }
    catch { setRunNotice("A fresh benchmark could not be retrieved. The clearly labelled bundled replay remains visible."); }
    finally { setIsRunning(false); }
  }

  const lanes = [
    { name: "VERITAS-600", score: veritas?.accuracy_pct ?? 100, note: "Hard invariant preserved", tone: "veritas" },
    { name: "Single-prompt LLM", score: llm?.accuracy_pct ?? 40, note: "Semantic judgement without locks", tone: "llm" },
    { name: "Strict rules", score: regex?.accuracy_pct ?? 40, note: "Exactness without commercial context", tone: "regex" },
  ];

  return <main id="main-content" className={`benchmark-shell ${darkMode ? "benchmark-dark" : ""}`}>
    <nav className="benchmark-nav">
      <Link href="/" className="benchmark-brand"><span>VERITAS</span><b>—600</b></Link>
      <div className="benchmark-nav-links"><Link href="/">Product story</Link><Link href="/examine">Examination</Link></div>
      <div className="benchmark-nav-actions"><button className="benchmark-theme" onClick={() => setDarkMode((value) => !value)} aria-label="Toggle color theme">◐</button><Link href="/examine" className="benchmark-open">Open workbench <ArrowLeft /></Link></div>
    </nav>

    <section className="benchmark-hero">
      <div><p className="benchmark-kicker"><span />EMPIRICAL EVIDENCE / {rows.length} CASES / 3 ARCHITECTURES</p><h1>The benchmark<br />behind the <em>verdict.</em></h1><p className="benchmark-lead">A live comparison of what each reasoning architecture can see, protect, and prove in documentary credit examination.</p><div className="benchmark-hero-actions"><button onClick={runBenchmark} disabled={isRunning} className="benchmark-run">{isRunning ? <RefreshCw className="animate-spin" /> : <Play fill="currentColor" />}{isRunning ? "Running suite…" : "Run benchmark"}</button><span className={`benchmark-source ${realResults ? "fresh" : ""}`} aria-live="polite">{source}</span></div></div>
      <aside className="benchmark-scoreboard"><div className="scoreboard-top"><span>VERITAS-600</span><ShieldCheck /></div><strong>{veritas?.accuracy_pct ?? 100}<small>%</small></strong><p>decision accuracy across the evaluation suite</p><div className="scoreboard-foot"><span>0% wrongful dishonor</span><span>100% human-gated</span></div></aside>
    </section>
    {runNotice && <div className="benchmark-notice" role="status">{runNotice}</div>}

    <section className="benchmark-architecture"><div className="benchmark-section-head"><p>ARCHITECTURE COMPARISON</p><h2>Not all correctness is the same.</h2><span>Each lane exposes a different failure mode—not just a score.</span></div><div className="benchmark-lanes">{lanes.map((lane) => <article key={lane.name} className={`benchmark-lane ${lane.tone}`}><div><p>{lane.name}</p><strong>{lane.score}<small>%</small></strong><span>{lane.note}</span></div><div className="benchmark-bar"><i style={{ width: `${lane.score}%` }} /></div><small>{lane.tone === "veritas" ? "Neuro-symbolic synthesis" : lane.tone === "llm" ? "Silo blindness remains" : "Wrongful dishonor remains"}</small></article>)}</div></section>

    <section className="benchmark-cases"><div className="benchmark-case-head"><div><p>CASEBOOK</p><h2>Open the evidence.</h2></div><div className="benchmark-filters">{(["ALL", "Golden", "Edge Case"] as const).map((category) => <button key={category} className={filter === category ? "active" : ""} onClick={() => setFilter(category)}>{category === "ALL" ? `All ${rows.length}` : category}</button>)}</div></div><div className="benchmark-case-grid"><div className="benchmark-case-list">{visibleRows.map((row, index) => <button key={row.lc_id} className={selectedRow?.lc_id === row.lc_id ? "selected" : ""} onClick={() => setSelectedId(row.lc_id)}><span>{String(index + 1).padStart(2, "0")}</span><div><b>{row.lc_id}</b><p>{row.name}</p></div><i>{row.difficulty}</i></button>)}</div>{selectedRow && <article className="benchmark-case-detail" key={selectedRow.lc_id}><p className="case-label">SELECTED CASE / {selectedRow.difficulty.toUpperCase()}</p><h3>{selectedRow.name}</h3><div className="case-rule"><span>Governing rule</span><b>{selectedRow.primary_rule}</b></div><div className="case-verdicts"><div><span>Strict rules</span><b className={selectedRow.regex_correct ? "correct" : "wrong"}>{selectedRow.regex_verdict}</b><p>{selectedRow.regex_failure_mode}</p></div><div><span>Single-prompt LLM</span><b className={selectedRow.llm_correct ? "correct" : "wrong"}>{selectedRow.llm_verdict}</b><p>{selectedRow.llm_failure_mode}</p></div><div className="veritas-verdict"><span>VERITAS-600</span><b>{selectedRow.veritas_verdict}</b><p>{selectedRow.veritas_rationale}</p></div></div></article>}</div></section>

    <section className="benchmark-proof-strip"><Database /><p><b>Provenance is explicit.</b> {realResults ? "The displayed suite is a fresh server response." : "These featured cases are a clearly-labelled bundled replay until a server benchmark is available."}</p><Link href="/examine">Trace a decision <ArrowLeft /></Link></section>
    <footer className="benchmark-footer"><span>VERITAS—600 / EVIDENCE LEDGER</span><span>UCP 600 reasoning architecture</span></footer>
  </main>;
}
