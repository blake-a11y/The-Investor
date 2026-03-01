# Homeland Security Investment Research — Project Scope
**Project:** Domestic Sleeper Cell Risk & Homeland Security Supply Chain Analysis
**Initiated:** March 1, 2026
**Trigger Event:** Confirmed death of senior Iranian leadership + U.S.–Israel strike scenario (Feb 28, 2026)
**Repository:** blake-a11y/The-Investor · branch: master
**Orchestrator:** Cursor Composer
**Final Reconciliation:** Claude (External) via GitHub

---

## Research Mandate

Following the Iran strike report (see `geopolitical-investment-research-2026/`), investor feedback identified a critical unmodeled risk: **domestic sleeper cell activation** following confirmed Iranian leadership death. This project answers three questions:

1. **How real is the risk?** — Probability assessment using publicly available intelligence, historical analogs, and academic terrorism databases
2. **Who responds?** — Federal agency budget flows, contract surge patterns, and procurement vehicles
3. **Who profits?** — Publicly traded homeland security supply chain with earnings-based AND event-driven valuation

This report adds a **fundamental/earnings-based layer** not present in the Iran event-driven report — making it suitable for longer-horizon investment theses, not just tactical positioning.

---

## Agent Assignments & Workflow

### Phase 1 — Threat Assessment
**Agent: Grok (xAI)**
**Prompt file:** `prompts/grok_threat_assessment.md`
**Output:** `reports/draft_threat_assessment.md`
**Estimated time:** 2–3 hours
**What Grok produces:** Probability tree, historical analogs, source-verified threat landscape

### Phase 2A — Agency Budget & Contract Flow
**Agent: Claude Code (Anthropic)**
**Prompt file:** `prompts/claude_code_usaspending.md`
**Output:** `data/usaspending_raw/` + `reports/draft_agency_mapping.md`
**Estimated time:** 2–4 hours
**What Claude Code produces:** USASpending.gov data pull, agency contract vehicle mapping, surge multiplier analysis

### Phase 2B — Earnings Model Automation
**Agent: ChatGPT 5.3 Codex (OpenAI)**
**Prompt file:** `prompts/chatgpt_codex_earnings_model.md`
**Output:** `code/earnings_model.py` + `data/company_fundamentals/`
**Estimated time:** 2–3 hours
**What Codex produces:** Automated earnings extraction, 10-K parsing, post-event revenue impact modeling

### Phase 3 — Company Universe & Market Data
**Agent: Gemini (Google)**
**Prompt file:** `prompts/gemini_company_screen.md`
**Output:** `reports/draft_company_universe.md`
**Estimated time:** 2–3 hours
**What Gemini produces:** Tiered company universe with market data, analyst ratings, contract backlog, event sensitivity

### Phase 3B — Fundamental Analysis
**Agent: Claude Sonnet (Anthropic, in Cursor)**
**Prompt file:** `prompts/claude_sonnet_fundamentals.md`
**Output:** `reports/draft_earnings_assessment.md`
**Estimated time:** 3–4 hours
**What Claude Sonnet produces:** EV/EBITDA comps, FCF analysis, contract concentration risk, valuation vs. peers

### Phase 4 — Monte Carlo Simulation
**Agent: Claude Code (Anthropic)**
**Prompt file:** `prompts/claude_code_monte_carlo.md`
**Output:** `code/monte_carlo_homesec.py` + `reports/mc_summary_homesec.csv`
**Estimated time:** 1–2 hours
**What Claude Code produces:** 10k-path simulation across 3 domestic scenarios, sector weights, risk metrics

### Phase 5 — Audit & Reconciliation
**Agent: Claude External (this instance)**
**Input:** All committed drafts from phases 1–4
**Prompt file:** `prompts/reconciliation_prompt.md`
**Output:** `reports/final_validated_report.md` + `reports/investment_report_homesec.html`
**Process:** Parallel audits (Claude, Gemini, ChatGPT) → flag resolution → final report production

---

## Scenario Framework

| Scenario | Event | Probability | Portfolio Thesis |
|----------|-------|-------------|-----------------|
| **A** | Minor domestic incident — IED, cyber attack, infrastructure sabotage | 40% | Moderate HomeSec spending surge; targeted contract awards |
| **B** | Coordinated multi-city attack — simultaneous targets | 35% | Major emergency appropriations; full supply chain activation |
| **C** | Mass casualty event — stadium, transit, infrastructure | 25% | Black swan; all-asset correlation spike then HomeSec supercycle |

---

## Company Universe — Tiered

### Tier 1 — Direct DHS/FBI Contract Holders (Highest Event Sensitivity)
- AXON Enterprise (AXON) — Law enforcement tech, body cameras, Tasers
- Motorola Solutions (MSI) — Public safety communications, dispatch systems
- Palantir Technologies (PLTR) — Intelligence analytics, federal contracts
- Leidos Holdings (LDOS) — Federal IT, DHS/FBI prime contractor
- Booz Allen Hamilton (BAH) — Intelligence community consulting + tech
- Science Applications International (SAIC) — Federal systems integration

### Tier 2 — First Responder & Physical Security Supply Chain
- MSA Safety (MSA) — First responder protective equipment
- Axon (overlaps Tier 1)
- Identiv (INVE) — Physical security, access control
- Avon Protection (AVON.L) — CBRN protective gear (note: London-listed)
- Parsons Corporation (PSN) — Federal infrastructure + security

### Tier 3 — Communications & Cyber Infrastructure
- L3Harris Technologies (LHX) — Federal communications, surveillance
- CrowdStrike Holdings (CRWD) — Cyber, federal endpoint protection
- Palo Alto Networks (PANW) — Federal cybersecurity
- FirstNet/AT&T (T) — First responder communications network

---

## Repo File Structure

```
homeland-security-research-2026/
├── PROJECT_SCOPE.md              ← This file
├── METHODOLOGY.md                ← To be created post-reconciliation
├── prompts/
│   ├── grok_threat_assessment.md
│   ├── claude_code_usaspending.md
│   ├── claude_code_monte_carlo.md
│   ├── claude_sonnet_fundamentals.md
│   ├── chatgpt_codex_earnings_model.md
│   ├── gemini_company_screen.md
│   └── reconciliation_prompt.md
├── data/
│   ├── usaspending_raw/          ← Claude Code outputs
│   ├── company_fundamentals/     ← Codex outputs
│   └── threat_sources/           ← Grok source citations
├── reports/
│   ├── draft_threat_assessment.md
│   ├── draft_agency_mapping.md
│   ├── draft_company_universe.md
│   ├── draft_earnings_assessment.md
│   └── final_validated_report.md
├── code/
│   ├── monte_carlo_homesec.py
│   ├── usaspending_pull.py
│   └── earnings_model.py
└── audits/
    ├── audit_claude.md
    ├── audit_gemini.md
    └── audit_chatgpt.md
```

---

## Sequencing

```
DAY 1 — MORNING (Parallel)
  → Grok:        Phase 1  — Threat assessment
  → Claude Code: Phase 2A — USASpending data pull
  → Gemini:      Phase 3  — Company universe screen

DAY 1 — AFTERNOON (Parallel)
  → ChatGPT Codex:  Phase 2B — Earnings model automation
  → Claude Sonnet:  Phase 3B — Fundamental analysis

DAY 2 — MORNING
  → Claude Code: Phase 4 — Monte Carlo runs
  → All agents:  Commit drafts to repo

DAY 2 — AFTERNOON
  → Push all drafts to GitHub master
  → Claude External: Phase 5 — Audit + reconciliation + final report
```

---

## Quality Standards (Inherited from Iran Report)
- All material claims: ≥2 independent sources
- No Wikipedia as primary source
- All MC parameters (μ/σ) fully disclosed
- Earnings data: sourced from 10-K / earnings call transcripts only
- Confidence score target: ≥80/100 post-reconciliation
- Output format: Print-optimized HTML → PDF (same template as Iran report)

---

*Project initiated by: blake-a11y · Research Only — Not Investment Advice*
