# Cursor Orchestration Guide

Peer-reviewed, multi-AI audited, Monte Carlo–validated research workflow for Wealth-Tech Operations Leader Persona.

## Audience & Report Requirements

**Persona:** Wealth-Tech Operations Leader (30+ years TAMP/platform builder, advisor-platform lens, data-driven, low-hype, operator-investor). See `prompts/persona_wealth_tech_operations.md` for full profile.

**Key Report Addition:** Section 2 "Investor Profile & Suitability Assessment" must include:
- Risk tolerance score (1–10) with justification
- Time horizon (months/years) with justification
- Behavioral factors (at least 2–3 with brief assessment)
- Fit statement: why this allocation aligns with the Persona's profile

**Tone:** Data-driven, skeptical. Favor multiple data points. No optimism or pessimism. Cross-reference every material claim with at least two independent sources.

---

## Orchestration Plan (Day 1 → Day 2)

| Phase | Action |
|-------|--------|
| **Day 1 – Primary Draft** | Paste `prompts/master_instructions.md` to **Grok** (+ "You already have the full conversation history — use it.") → receive full report + MC code. Save to `reports/draft_grok_v1.md`. |
| **Day 1–2 – Parallel Audits** | Paste Grok draft + audit prompts to **Claude**, **Gemini**, **ChatGPT-4o** in parallel. Save to `reports/audit_claude.md`, `audit_gemini.md`, `audit_chatgpt.md`. |
| **Day 2 – Reconciliation** | Paste all three audits to Grok: *"Incorporate all valid audit feedback, resolve discrepancies, and produce FINAL version 1.0 with change log."* |
| **Final Sign-Off** | Run `.\code\run_mc.ps1` locally, attach MC output to report. Document: *"Audited & validated by Grok + Claude + Gemini + ChatGPT + independent Python execution."* |

---

## Using Cursor

- **Composer + @ codebase** for all AI work. Reference `@ prompts/master_instructions.md`, `@ reports/draft_grok_v1.md`, etc.
- **Version control:** Run `.\code\commit_audit_round.ps1 -Message "Audit round N"` after each audit.
- **Monte Carlo:** One click → `.\code\run_mc.ps1` in Cursor terminal.
- **Export PDF:** `.\code\export_to_pdf.ps1` (Pandoc). **Zero install:** Open `reports/final_validated_report.md` → Ctrl+K → "Markdown: Open Preview" → Ctrl+P → Save as PDF.
- **Share repo:** GitHub Settings → Private → Collaborators → Add advisor/family.

## Cursor Bot Setup Instructions

All research bots run inside Cursor with `@codebase` access to the same repo. Each bot is a **Composer session** (or Chat session) with a different model selected.

### Prerequisites
- Cursor installed with the workspace open at `geopolitical-investment-research-2026` (or the parent folder containing it)
- Cursor Pro or equivalent for access to Claude, GPT, Gemini (model availability depends on your subscription)
- Ensure `geopolitical-investment-research-2026` is the active workspace or a subfolder thereof so `@codebase` indexes the correct files

### Model Availability (Cursor)
| Model | Cursor Name / How to Select |
|-------|-----------------------------|
| Claude 4.6 | Composer → Model selector → Claude Opus 4.5 / Claude 4 (or nearest available) |
| ChatGPT 5.2/3 | Composer → Model selector → GPT-4o / o1 (Cursor labels may differ; use latest GPT) |
| Gemini 3.5 | Composer → Model selector → Gemini (if integrated); otherwise use via API or external app |
| Composer (default) | Default Composer agent — use as orchestrator or as an additional audit bot with any selected model |

*Note: Exact model names in Cursor's UI may vary. Use the closest available (e.g., Claude Opus 4, GPT-4o).*

### Setup Steps for Each Research Bot

**For Claude (Audit):**
1. Open Cursor, ensure workspace = `The Investor` (or `geopolitical-investment-research-2026`)
2. Open Composer (Cmd+I / Ctrl+I) or New Chat (Cmd+L / Ctrl+L)
3. Select model: Claude (Opus 4 or best available)
4. Type `@codebase` to attach full codebase
5. Paste the contents of `prompts/claude_audit_prompt.md`
6. Attach/reference `reports/draft_grok_v1.md` (e.g., "Attach reports/draft_grok_v1.md" or paste its contents)
7. Run the audit; copy output to `reports/audit_claude.md`

**For ChatGPT (Audit):**
1. New Composer or Chat session
2. Select model: GPT-4o (or o1 if available)
3. `@codebase` + paste `prompts/chatgpt_audit_prompt.md` + attach `reports/draft_grok_v1.md`
4. Run; save output to `reports/audit_chatgpt.md`

**For Gemini (Audit):**
1. New Composer or Chat session
2. Select model: Gemini (if shown in Cursor)
3. If Gemini is not in Cursor: run audit in browser (Gemini app), paste same prompt + draft, copy output to `reports/audit_gemini.md`
4. `@codebase` equivalent: manually paste key repo paths or attach the draft + persona + master instructions

**For Composer as Orchestrator:**
- The current session (this one) = Orchestrator
- Use for: creating/editing prompts, organizing files, running MC script, reconciling audit feedback, exporting PDF
- Can also run a fourth audit by starting a new Composer tab with a different model if desired

---

## Audit Prompts

| AI | Prompt file | Output |
|----|-------------|--------|
| Claude | `prompts/claude_audit_prompt.md` | `reports/audit_claude.md` |
| Gemini | `prompts/gemini_audit_prompt.md` | `reports/audit_gemini.md` |
| ChatGPT | `prompts/chatgpt_audit_prompt.md` | `reports/audit_chatgpt.md` |

**Base prompt:** *"Audit the attached Grok report for factual accuracy, logical gaps, and MC validity. Mark every claim that needs verification."*  
**ChatGPT add-on:** *"Suggest any stronger recent sources from 2025–2026."*

---

## Composer: "Your Actions"

A Cursor rule (`.cursor/rules/your-actions.mdc`) ensures **every Composer Agent response ends with a "Your actions" section** — a numbered list of next steps for you. No config needed; it applies to all sessions.

## Quick Commands

| Task | Command |
|------|---------|
| Run MC | `.\code\run_mc.ps1` |
| Commit audit | `.\code\commit_audit_round.ps1 -Message "Round N"` |
| Export PDF | `.\code\export_to_pdf.ps1` |

---

## Repo Structure

```
geopolitical-investment-research-2026/
├── prompts/
│   ├── master_instructions.md          ← Copy-paste to Grok/Claude/Gemini/ChatGPT
│   ├── persona_wealth_tech_operations.md ← Wealth-Tech Operations Leader profile
│   ├── grok_prompt_v1.md
│   ├── claude_audit_prompt.md
│   ├── gemini_audit_prompt.md
│   ├── chatgpt_audit_prompt.md
│   └── reconciliation_prompt.md
├── data/
├── code/
│   ├── monte_carlo_simulator.py        ← 3 scenarios (A/B/C), 10k paths
│   ├── run_mc.ps1
│   ├── commit_audit_round.ps1
│   └── export_to_pdf.ps1
├── reports/
│   ├── draft_grok_v1.md
│   ├── audit_claude.md
│   ├── audit_gemini.md
│   ├── audit_chatgpt.md
│   └── final_validated_report.md       ← TARGET OUTPUT (includes Investor Profile section)
└── audits/feedback_round1/
```

---

## Your Actions

| # | Action | Status |
|---|--------|--------|
| 1 | Create GitHub repo in Cursor | Done (https://github.com/blake-a11y/The-Investor) |
| 2 | Copy Master Instructions → paste to Grok → get Draft 1 | You do |
| 3 | Run Claude, Gemini, ChatGPT audits in parallel | You do |
| 4 | Reconcile in Grok with reconciliation prompt | You do |
| 5 | Run `.\code\run_mc.ps1` locally, attach output to report | You do |
| 6 | Export to PDF, share repo privately with advisor/family | You do |

**Optional:** Install [Pandoc](https://pandoc.org/installing.html) for script-based PDF export. Else use Cursor preview → Print to PDF.
