# Claude Sonnet Prompt — Phase 3B: Fundamental Analysis
**Agent:** Claude Sonnet (Anthropic, in Cursor)
**Project:** Homeland Security Investment Research 2026
**Input:** `data/company_fundamentals/` (from Codex) + `reports/draft_company_universe.md` (from Gemini)
**Output file:** `reports/draft_earnings_assessment.md`

---

## Your Role
You are the fundamental analysis agent. Your job is to synthesize the earnings model data (from Codex) and market data (from Gemini) into investment-grade fundamental assessments for each company. This is the layer that separates this report from a pure event-driven trade — you are building a **durable earnings thesis** for each company regardless of the trigger event.

---

## Read First
Before writing anything, read:
1. `data/company_fundamentals/master_fundamentals.csv`
2. `data/company_fundamentals/historical_event_returns.csv`
3. `reports/draft_company_universe.md`

---

## Task 1 — Fundamental Scorecard (Each Company)

For each company, produce a structured assessment:

### A. Business Quality Score (1–10)
Rate on:
- **Revenue visibility** (backlog coverage ratio)
- **Contract concentration risk** (single-agency dependency)
- **Margin durability** (gross margin trend, FCF conversion)
- **Competitive moat** (switching costs, certification requirements, incumbency)
- **Management execution** (organic growth rate, M&A discipline)

### B. Earnings Trajectory
- 3-year revenue CAGR (from Codex data)
- Consensus next-12-month revenue growth estimate
- EPS growth rate vs. peer average
- FCF yield vs. 10-year treasury (spread analysis)
- How does contract backlog translate to revenue recognition? (timing analysis)

### C. Event Sensitivity Rating (1–5)
- 1 = Minimal direct exposure to homeland security spending surge
- 5 = Near-total revenue dependent on DHS/FBI/law enforcement spending
- For each rating, cite the specific contract relationships that drive it

### D. Valuation Assessment
- Is the stock cheap, fair, or expensive vs. its own history?
- What growth rate is implied by the current multiple?
- At what price does the stock become a "buy" on fundamentals alone (ex-event)?
- What is the additional upside from a Scenario B event?

---

## Task 2 — Investment Thesis Construction (Each Tier 1 Company)

For each Tier 1 company, write a concise investment thesis in this structure:

```
COMPANY: [Name] ([Ticker])
ONE-LINE THESIS: [Why own this stock in this environment]

BULL CASE:
- Fundamental driver 1 (earnings-based)
- Event-driven catalyst
- Upside target and timeline

BASE CASE:
- Expected return without a major event
- Key earnings drivers
- Price target (12-month fundamental)

BEAR CASE:
- Contract loss risk
- Budget continuing resolution risk
- Valuation compression scenario

KEY METRICS TO MONITOR:
- [Specific data points from earnings calls/USASpending]
```

---

## Task 3 — Portfolio Construction Recommendation

Given the full universe, recommend an allocation across Tier 1, 2, and 3:

- What weight to Tier 1 vs. Tier 2 vs. Tier 3?
- Is there an ETF option that provides better risk-adjusted exposure than individual stocks?
- How does this integrate with the existing Iran report allocation (35% XAR already covers some defense)?
- What is the overlap risk between the two portfolios?

Model two portfolio options:
1. **ETF-first:** Minimize single-stock risk, use ETFs where available
2. **Concentrated:** 4–6 highest-conviction individual names

For each portfolio: expected return, VaR, correlation to broader market.

---

## Task 4 — Risks to Fundamental Thesis

Document the risks that are specific to **earnings** (not event-driven):
- **Continuing resolution risk:** Congress fails to pass full appropriations; agencies can't award new contracts
- **DOGE / budget cut risk:** Federal IT and consulting spending under pressure
- **Contract rebid risk:** Which major contracts come up for rebid in 2026–2027?
- **Margin compression:** Cost-plus vs. fixed-price contract mix shifts
- **Cybersecurity commodity risk:** Cloud providers eating into pure-play cyber

---

## Output Format
`reports/draft_earnings_assessment.md`:

```markdown
# Earnings-Based Fundamental Assessment
**Agent:** Claude Sonnet | **Date:** [date] | **Status:** Draft — Pending Audit

## 1. Methodology Note
## 2. Fundamental Scorecards — All Companies
## 3. Investment Theses — Tier 1 (Full Detail)
## 4. Investment Theses — Tier 2 & 3 (Summary)
## 5. Portfolio Construction Options
## 6. Risks to Earnings Thesis
## 7. Integration with Iran Event-Driven Report
```

Commit with message: `"Phase 3B complete: Claude Sonnet fundamental analysis"`
