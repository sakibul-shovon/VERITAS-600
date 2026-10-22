"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import {
  AlertTriangle,
  ArrowRight,
  CheckCircle2,
  ChevronRight,
  Cpu,
  Database,
  Eye,
  FileText,
  Fingerprint,
  Landmark,
  Lock,
  Menu,
  Moon,
  Scale,
  ShieldCheck,
  X,
  Sun,
} from "lucide-react";

type DemoStage = 0 | 1 | 2 | 3 | 4;

const stages = [
  {
    label: "Active terms",
    owner: "METERLESS / MEMORY",
    title: "Establish the terms that govern",
    detail: "Accepted amendments become active terms. Pending amendments remain quarantined under UCP 600 Art. 10(c) and 10(e).",
    output: "Active term snapshot",
  },
  {
    label: "Federated evidence",
    owner: "ZETARIS",
    title: "Bring external context to the evidence",
    detail: "Operational records, customs benchmarks, and watchlist context are queried as separate sources with a receipt.",
    output: "One-row federation receipt",
  },
  {
    label: "Deterministic rules",
    owner: "PYTHON",
    title: "Lock the calculation",
    detail: "Insurance is 108%. The UCP 600 Art. 28(f)(ii) minimum is 110%. The $9,600 shortfall is a locked discrepancy.",
    output: "DISCREPANT · immutable",
  },
  {
    label: "Semantic review",
    owner: "NEMOTRON",
    title: "Interpret language inside a boundary",
    detail: "Semantic findings can explain a typographical difference or general description. They cannot change a failed calculation.",
    output: "Bounded legal finding",
  },
  {
    label: "Human action",
    owner: "POLICY ENGINE → HUMAN",
    title: "Recommend, then require authority",
    detail: "The system recommends a refusal. A bank examiner must explicitly sign off before any action is dispatched.",
    output: "PENDING HUMAN SIGN-OFF",
  },
] as const;

const outcomeCards = [
  {
    caseId: "LC-2026-8841",
    title: "Approve honour",
    tone: "success",
    detail: "Accepted amendment context, a protected typo, and a non-conflicting general description lead to a complying presentation.",
  },
  {
    caseId: "LC-2026-9104",
    title: "Issue MT734 refusal",
    tone: "danger",
    detail: "Insurance coverage is 108%, below the 110% requirement. The calculation stays discrepant.",
  },
  {
    caseId: "LC-2026-9920",
    title: "Place compliance hold",
    tone: "warning",
    detail: "Facially compliant documents can still require AML review when federated risk signals demand it.",
  },
] as const;

export default function LandingPage() {
  const [menuOpen, setMenuOpen] = useState(false);
  const [activeStage, setActiveStage] = useState<DemoStage>(0);
  const [showOverride, setShowOverride] = useState(false);
  const [activeOutcome, setActiveOutcome] = useState(1);
  const [dark, setDark] = useState(false);
  const [motionReady, setMotionReady] = useState(false);

  const currentStage = stages[activeStage];

  useEffect(() => {
    const nodes = Array.from(document.querySelectorAll<HTMLElement>("[data-reveal]"));
    const revealVisibleNodes = () => {
      nodes.forEach((node) => {
        if (node.getBoundingClientRect().top < window.innerHeight * 0.88) node.classList.add("revealed");
      });
    };
    revealVisibleNodes();
    const observer = new IntersectionObserver(
      (entries) => entries.forEach((entry) => entry.isIntersecting && entry.target.classList.add("revealed")),
      { threshold: 0.12 }
    );
    nodes.forEach((node) => observer.observe(node));
    requestAnimationFrame(() => setMotionReady(true));
    return () => observer.disconnect();
  }, []);

  return (
    <main id="main-content" className={`landing-shell${dark ? " landing-dark" : ""}${motionReady ? " landing-motion" : ""}`}>
      <a className="landing-skip" href="#main-story">Skip to main content</a>

      <header className="landing-nav">
        <Link className="landing-brand" href="/" aria-label="VERITAS-600 home">
          <span className="brand-mark" aria-hidden="true"><i /><i /><i /></span>
          <span>VERITAS<span>—</span>600</span>
        </Link>

        <nav className="landing-nav-links" aria-label="Landing page">
          <a href="#why">Why</a>
          <a href="#trace">Trace a decision</a>
          <a href="#architecture">Architecture</a>
          <a href="#proof">Proof</a>
          <Link href="/evals">Benchmark</Link>
        </nav>

        <div className="landing-nav-action">
          <button className="landing-theme-button" onClick={() => setDark((value) => !value)} aria-label={dark ? "Use light theme" : "Use dark theme"}>
            {dark ? <Sun aria-hidden="true" /> : <Moon aria-hidden="true" />}
          </button>
          <Link className="landing-cta landing-cta-small" href="/examine">
            Open examination <ArrowRight aria-hidden="true" />
          </Link>
          <button className="landing-menu-button" onClick={() => setMenuOpen(true)} aria-label="Open navigation menu">
            <Menu aria-hidden="true" />
          </button>
        </div>
      </header>

      {menuOpen && (
        <div className="landing-menu-overlay" role="dialog" aria-modal="true" aria-label="Landing navigation">
          <div className="landing-menu-panel">
            <button className="landing-menu-close" onClick={() => setMenuOpen(false)} aria-label="Close navigation menu"><X /></button>
            <a href="#why" onClick={() => setMenuOpen(false)}>Why VERITAS</a>
            <a href="#trace" onClick={() => setMenuOpen(false)}>Trace a decision</a>
            <a href="#architecture" onClick={() => setMenuOpen(false)}>Architecture</a>
            <a href="#proof" onClick={() => setMenuOpen(false)}>Proof</a>
            <Link href="/evals" onClick={() => setMenuOpen(false)}>Architecture benchmark</Link>
            <Link className="landing-cta" href="/examine" onClick={() => setMenuOpen(false)}>Open examination <ArrowRight /></Link>
          </div>
        </div>
      )}

      <section className="landing-hero" id="main-story">
        <div className="landing-hero-copy">
          <p className="landing-eyebrow hero-animate hero-1"><span /> DOCUMENTARY CREDIT EXAMINATION · UCP 600</p>
          <h1 className="hero-animate hero-2">Every document.<br />Every rule.<br /><em>One defensible decision.</em></h1>
          <p className="landing-lead hero-animate hero-3">VERITAS-600 turns documentary-credit evidence into a traceable bank action—locking objective UCP 600 checks, constraining semantic AI, and requiring human authorization.</p>
          <div className="landing-hero-actions hero-animate hero-4">
            <Link className="landing-cta" href="/examine?case=LC-2026-9104">
              Open examination <ArrowRight aria-hidden="true" />
            </Link>
            <a className="landing-text-link" href="#trace">Trace a decision <ChevronRight aria-hidden="true" /></a>
          </div>
          <p className="landing-proof-line hero-animate hero-5"><Lock aria-hidden="true" /> Deterministic checks locked <span>·</span> Semantic review bounded <span>·</span> Human sign-off required</p>
        </div>

        <div className="evidence-gate hero-animate hero-gate" aria-label="Guided predefined evidence preview">
          <div className="gate-topline">
            <span>GUIDED PREVIEW</span>
            <span>PREDEFINED CASE</span>
          </div>
          <button className="gate-evidence gate-node active" onClick={() => setActiveStage(2)}>
            <span className="gate-node-label">INSURANCE CERTIFICATE</span>
            <strong>108<span>%</span></strong>
            <small>Observed cover</small>
          </button>
          <div className="gate-rail" aria-hidden="true"><span /></div>
          <button className="gate-rule gate-node" onClick={() => setShowOverride((visible) => !visible)}>
            <span className="gate-node-label">PYTHON REQUIRES</span>
            <strong>≥ 110<span>%</span></strong>
            <small>UCP 600 Art. 28(f)(ii)</small>
          </button>
          <div className="gate-docket">
            <div className="docket-top"><AlertTriangle aria-hidden="true" /><span>RECOMMENDED ACTION</span></div>
            <strong>ISSUE MT734<br />REFUSAL</strong>
            <p>Insurance shortfall <b>$9,600</b></p>
            <div className="docket-human"><Lock aria-hidden="true" /> HUMAN AUTHORIZATION REQUIRED</div>
          </div>
          {showOverride && (
            <div className="override-note" role="status">
              <Cpu aria-hidden="true" /> Semantic review may add context. It cannot overwrite this deterministic discrepancy.
            </div>
          )}
          <p className="gate-caption">LC-2026-9104 · predefined evidence · not a live run</p>
        </div>
      </section>

      <div className="landing-rule" aria-hidden="true"><span /></div>

      <section className="landing-section landing-problem reveal" id="why" data-reveal>
        <div className="section-kicker">01 / THE PROBLEM</div>
        <div className="problem-headline">Trade documents do not fail in only one way.</div>
        <div className="problem-list">
          <article><span>01</span><div><h2>Strict text can wrongfully refuse.</h2><p>A harmless typo or general non-conflicting description is not necessarily a discrepancy.</p></div><FileText aria-hidden="true" /></article>
          <article><span>02</span><div><h2>AI cannot waive an objective fact.</h2><p>A fluent explanation cannot make 108% insurance satisfy a 110% threshold.</p></div><Scale aria-hidden="true" /></article>
          <article><span>03</span><div><h2>Documents alone can miss external risk.</h2><p>Documentary compliance and regulatory exposure are distinct decisions that need distinct evidence.</p></div><Database aria-hidden="true" /></article>
        </div>
      </section>

      <section className="landing-section landing-invariant reveal" aria-labelledby="invariant-title" data-reveal>
        <div className="section-kicker">02 / THE HARD INVARIANT</div>
        <div className="invariant-grid">
          <div>
            <h2 id="invariant-title">Interpretation may add context.<br /><em>It cannot erase a failed calculation.</em></h2>
            <p>Objective UCP 600 checks are calculated in Python. Nemotron is used for bounded semantic and lexical reasoning, never to override a locked discrepancy.</p>
            <button className="landing-outline-button" onClick={() => setShowOverride(true)}>Show attempted override <ArrowRight aria-hidden="true" /></button>
          </div>
          <div className="invariant-calculation">
            <div><span>OBSERVED COVER</span><strong>108%</strong></div>
            <div className="calc-divider"><span>LOCKED RULE</span></div>
            <div><span>REQUIRED MINIMUM</span><strong>110%</strong></div>
            <div className="calc-result"><AlertTriangle aria-hidden="true" /><span>DISCREPANT · $9,600 SHORTFALL</span></div>
          </div>
        </div>
      </section>

      <section className="landing-section landing-trace reveal" id="trace" data-reveal>
        <div className="trace-heading">
          <div><div className="section-kicker">03 / TRACE ONE DECISION</div><h2>Follow one evidence chain.<br /><em>Nothing is hidden.</em></h2></div>
          <p>Guided demonstration · predefined LC-2026-9104 evidence · not a live examination.</p>
        </div>
        <div className="trace-workbench">
          <div className="trace-steps" role="tablist" aria-label="Guided decision stages">
            {stages.map((stage, index) => (
              <button
                key={stage.label}
                role="tab"
                aria-selected={activeStage === index}
                className={activeStage === index ? "selected" : ""}
                onClick={() => setActiveStage(index as DemoStage)}
              >
                <span>{String(index + 1).padStart(2, "0")}</span>{stage.label}
              </button>
            ))}
          </div>
          <article className="trace-detail" role="tabpanel" key={activeStage}>
            <span className="trace-owner">{currentStage.owner}</span>
            <h3>{currentStage.title}</h3>
            <p>{currentStage.detail}</p>
            <div className="trace-output"><span>OUTPUT</span><strong>{currentStage.output}</strong></div>
            <div className="trace-nav">
              <button onClick={() => setActiveStage((Math.max(0, activeStage - 1)) as DemoStage)} disabled={activeStage === 0}>Previous</button>
              {activeStage < 4 ? <button onClick={() => setActiveStage((activeStage + 1) as DemoStage)}>Next evidence <ArrowRight aria-hidden="true" /></button> : <Link className="landing-cta" href="/examine?case=LC-2026-9104&tour=1">Open this case <ArrowRight aria-hidden="true" /></Link>}
            </div>
          </article>
          <aside className="trace-visual" aria-label="Evidence lineage diagram">
            <div className="folio-card"><span>FIELD</span><strong>{activeStage === 2 ? "Coverage: 108%" : activeStage === 1 ? "Three source silos" : "LC-2026-9104"}</strong><small>Evidence anchor</small></div>
            <div className="trace-line" aria-hidden="true"><i /><i /><i /><i /></div>
            <div className="folio-card folio-card-bottom"><span>DECISION</span><strong>{activeStage === 4 ? "Human sign-off" : "Evidence bounded"}</strong><small>Traceable outcome</small></div>
          </aside>
        </div>
      </section>

      <section className="landing-section landing-architecture reveal" id="architecture" data-reveal>
        <div className="architecture-intro"><div className="section-kicker">04 / ACCOUNTABLE ARCHITECTURE</div><h2>Five owners.<br /><em>One chain of custody.</em></h2><p>Each stage has a distinct responsibility, output, and execution mode. The system does not collapse them into a single opaque “AI decision.”</p></div>
        <div className="architecture-list">
          <article><span>01</span><div><b>Meterless / Memory</b><p>Resolves active terms and routes scoped context.</p></div><ArrowRight aria-hidden="true" /></article>
          <article><span>02</span><div><b>Zetaris</b><p>Federates operational, customs, and watchlist evidence without ETL.</p></div><ArrowRight aria-hidden="true" /></article>
          <article><span>03</span><div><b>Python</b><p>Calculates dates, thresholds, amounts, and locked failures.</p></div><ArrowRight aria-hidden="true" /></article>
          <article><span>04</span><div><b>Nemotron</b><p>Assesses bounded semantic questions with legal citations.</p></div><ArrowRight aria-hidden="true" /></article>
          <article><span>05</span><div><b>Policy engine → Human</b><p>Assembles a recommendation, then requires examiner sign-off.</p></div><ArrowRight aria-hidden="true" /></article>
        </div>
      </section>

      <section className="landing-section landing-outcomes reveal" data-reveal>
        <div className="outcomes-intro"><div className="section-kicker">05 / THREE POSSIBLE ACTIONS</div><h2>Honour. Refuse. Hold.</h2><p>Every recommendation stays pending until a human examiner authorizes the consequence.</p></div>
        <div className="outcomes-list">
          {outcomeCards.map((outcome, index) => (
            <button key={outcome.caseId} className={`outcome-card ${outcome.tone} ${activeOutcome === index ? "open" : ""}`} onClick={() => setActiveOutcome(index)} aria-expanded={activeOutcome === index}>
              <span>{outcome.caseId}</span><strong>{outcome.title}</strong><ChevronRight aria-hidden="true" />
              {activeOutcome === index && <p>{outcome.detail}</p>}
              <small><Lock aria-hidden="true" /> Human sign-off required</small>
            </button>
          ))}
        </div>
      </section>

      <section className="landing-section landing-proof reveal" id="proof" data-reveal>
        <div className="section-kicker">06 / INSPECTABLE PROOF</div>
        <div className="proof-layout">
          <div><h2>Evidence does not disappear<br />when the decision arrives.</h2><p>VERITAS keeps the chain visible from source record to examiner receipt, including execution provenance when the real terminal runs.</p></div>
          <ol className="proof-chain">
            <li><Fingerprint aria-hidden="true" /><span>Source digest</span></li>
            <li><CheckCircle2 aria-hidden="true" /><span>Active-term hash</span></li>
            <li><Database aria-hidden="true" /><span>Federation receipt</span></li>
            <li><ShieldCheck aria-hidden="true" /><span>Decision digest</span></li>
            <li><Landmark aria-hidden="true" /><span>Examiner receipt</span></li>
          </ol>
        </div>
      </section>

      <section className="landing-section landing-benchmark reveal" data-reveal>
        <div><div className="section-kicker">07 / ARCHITECTURE BENCHMARK</div><h2>Safer reasoning is not a style choice.</h2><p>Compare the strict rule baseline, a single-prompt model, and the hybrid system across the evaluation suite.</p></div>
        <div className="benchmark-table" role="table" aria-label="Architecture comparison">
          <div role="row"><span role="cell">Strict rules</span><b role="cell">Rigid text</b><small role="cell">Misses semantic tolerance</small></div>
          <div role="row"><span role="cell">Single-prompt model</span><b role="cell">Fluent reasoning</b><small role="cell">Can waive objective facts</small></div>
          <div className="hybrid" role="row"><span role="cell">VERITAS hybrid</span><b role="cell">Bounded authority</b><small role="cell">Evidence, rules, semantics, human gate</small></div>
        </div>
        <Link className="landing-text-link" href="/evals">View architecture benchmark <ArrowRight aria-hidden="true" /></Link>
      </section>

      <section className="landing-final reveal" data-reveal>
        <div className="receipt-mark" aria-hidden="true"><Fingerprint /></div>
        <p className="landing-eyebrow">VERITAS—600</p>
        <h2>Inspect the evidence.<br /><em>Then make the call.</em></h2>
        <p>Decision support prepares the case. Human authority releases the action.</p>
        <div className="landing-hero-actions"><Link className="landing-cta" href="/examine">Open examination <ArrowRight aria-hidden="true" /></Link><Link className="landing-text-link" href="/evals">View benchmark <ArrowRight aria-hidden="true" /></Link></div>
      </section>

      <footer className="landing-footer"><span>VERITAS—600 · Documentary Credit Examination</span><span>Evidence-led UCP 600 adjudication</span></footer>
    </main>
  );
}
