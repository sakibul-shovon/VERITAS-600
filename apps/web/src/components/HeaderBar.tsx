"use client";

import React from "react";
import Link from "next/link";
import { ShieldAlert, Database, Zap, Clock, Cpu, BarChart3, ChevronDown, FilePlus2, Moon, Sun } from "lucide-react";
import { LCScenarioSummary } from "@/lib/types";

interface HeaderBarProps {
  scenarios: LCScenarioSummary[];
  selectedLcId: string;
  onSelectScenario: (lcId: string) => void;
  sponsorHealth: any;
  onToggleSqlDrawer: () => void;
  sqlDrawerOpen: boolean;
  darkMode: boolean;
  onToggleTheme: () => void;
  onNewCase: () => void;
}

export default function HeaderBar({
  scenarios,
  selectedLcId,
  onSelectScenario,
  sponsorHealth,
  onToggleSqlDrawer,
  sqlDrawerOpen,
  darkMode,
  onToggleTheme,
  onNewCase,
}: HeaderBarProps) {
  return (
    <header className="exam-header border-b border-card-border bg-[#0B0F19]/90 backdrop-blur sticky top-0 z-40 px-4 py-2.5">
      <div className="flex flex-wrap items-center justify-between gap-3">
        {/* Left: Brand & Navigation */}
        <div className="flex items-center gap-4">
          <Link href="/" className="flex items-center gap-2" aria-label="Return to VERITAS-600 product overview">
            <div className="h-8 w-8 rounded-lg bg-gradient-to-tr from-blue-600 to-indigo-500 flex items-center justify-center shadow-lg shadow-blue-500/20">
              <ShieldAlert className="h-4 w-4 text-white" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="font-bold text-sm tracking-wider text-slate-100">VERITAS-600</span>
                <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-blue-500/10 text-blue-400 border border-blue-500/20">
                  UCP 600 ADJUDICATOR
                </span>
              </div>
              <p className="text-[11px] text-slate-400">Examining Bank Trade Finance Terminal</p>
            </div>
          </Link>

          <div className="h-5 w-px bg-card-border hidden sm:block" />

          {/* Scenario Selector */}
          <div className="relative">
            <select
              value={selectedLcId}
              onChange={(e) => onSelectScenario(e.target.value)}
              disabled={scenarios.length === 0}
              className="bg-card hover:bg-slate-800 text-slate-200 text-xs font-mono font-medium rounded-md px-3 py-1.5 pr-8 border border-card-border focus:outline-none focus:ring-1 focus:ring-blue-500 appearance-none cursor-pointer"
            >
              <option value="">Choose an existing case…</option>
              {scenarios.map((scenario) => <option key={scenario.lc_id} value={scenario.lc_id}>{scenario.case_source === "SAMPLE_CASE" ? "SAMPLE · " : ""}{scenario.lc_id}: {scenario.applicant} → {scenario.beneficiary} ({scenario.currency} {scenario.amount.toLocaleString()})</option>)}
            </select>
            <ChevronDown className="h-3.5 w-3.5 text-slate-400 absolute right-2.5 top-2.5 pointer-events-none" />
          </div>
        </div>

        {/* Center: 5-Day Preclusion Clock */}
        <div className="hidden lg:flex items-center gap-2 bg-amber-500/10 border border-amber-500/20 rounded-md px-3 py-1 text-xs">
          <Clock className="h-3.5 w-3.5 text-amber-400 animate-pulse" />
          <span className="text-amber-300 font-medium">UCP 600 Art. 14(b) examination clock:</span>
          <span className="font-mono font-bold text-amber-200">starts from recorded presentation receipt</span>
        </div>

        {/* Right: Telemetry Badges & Links */}
        <div className="flex items-center gap-2">
          <button type="button" className="header-action header-new-case" onClick={onNewCase}>
            <FilePlus2 aria-hidden="true" />
            <span>New case</span>
          </button>

          <button type="button" className="header-action header-theme" onClick={onToggleTheme} aria-label={darkMode ? "Switch examination to light theme" : "Switch examination to dark theme"}>
            {darkMode ? <Sun aria-hidden="true" /> : <Moon aria-hidden="true" />}
            <span>{darkMode ? "Light" : "Dark"}</span>
          </button>

          {/* Zetaris Badge */}
          <button
            onClick={onToggleSqlDrawer}
            className={`flex items-center gap-1.5 px-2.5 py-1 rounded text-[11px] font-mono border transition ${
              sqlDrawerOpen
                ? "bg-blue-600/20 border-blue-500 text-blue-300"
                : "bg-slate-900 border-card-border text-slate-300 hover:border-slate-600"
            }`}
            title="Click to inspect Zetaris 3-Silo In-Situ SQL Query"
          >
            <Database className="h-3 w-3 text-cyan-400" />
            <span>Zetaris:</span>
            <span className="text-emerald-400 font-semibold">
              {sponsorHealth?.sponsors?.zetaris?.telemetry === "LIVE_ZETARIS" ? "LIVE CLOUD" : "LOCAL DUCKDB"}
            </span>
          </button>

          {/* Meterless Badge */}
          <div className="hidden sm:flex items-center gap-1.5 px-2 py-1 rounded bg-slate-900 border border-card-border text-[11px] font-mono text-slate-300">
            <Zap className="h-3 w-3 text-amber-400" />
            <span>Meterless:</span>
            <span className="text-amber-300 font-semibold">MEASURED PER RUN</span>
          </div>

          {/* NVIDIA NIM Badge */}
          <div className="flex items-center gap-1.5 px-2 py-1 rounded bg-slate-900 border border-card-border text-[11px] font-mono text-slate-300">
            <Cpu className="h-3 w-3 text-emerald-400" />
            <span>NIM:</span>
            <span className="text-emerald-400 font-semibold">
              {sponsorHealth?.sponsors?.nvidia_nim?.telemetry === "LIVE_UNCACHED" ? "LIVE" : "CACHED REPLAY"}
            </span>
          </div>

          {/* Evals Link */}
          <Link
            href="/evals"
            className="flex items-center gap-1 px-2.5 py-1 rounded bg-indigo-600/20 border border-indigo-500/30 text-indigo-300 hover:bg-indigo-600/30 text-xs font-medium transition"
          >
            <BarChart3 className="h-3.5 w-3.5" />
            <span>Evals</span>
          </Link>
        </div>
      </div>
    </header>
  );
}
