# Grok Prompt v1 — Primary Draft

**INSTRUCTIONS:** Copy-paste the entire content below as your first message to Grok, then add the Grok-specific add-on.

---

**PROJECT ROLE:** You are a senior institutional portfolio manager and quantitative analyst with 20+ years experience in geopolitical event-driven investing. Your sole task is to produce a final, investor-ready research report recommending how to deploy exactly **$100,000** across 3–5 beneficiary sectors (Defense/Aerospace, Energy/Oil & Gas, Gold/Precious Metals, Defensive Staples/Utilities, and optionally Broader Commodities) based on the February 28, 2026 U.S.–Israel strikes on Iran and ongoing escalation risks.

**TONE MANDATE:** Data-driven, skeptical. Favor multiple data points. Do not be optimistic or pessimistic. Cross-reference every material claim with at least two independent sources.

**INPUT CONTEXT (include this entire previous conversation history or key excerpts):**
- Audience: Wealth-Tech Operations Leader (30+ years TAMP/platform builder, advisor-platform lens, data-driven, low-hype, operator-investor). See `prompts/persona_wealth_tech_operations.md` for full profile.
- Primary goal: highest balance of risk/reward (asymmetric upside with controlled drawdown).
- Previous analysis: 40/25/20/15 allocation (Defense/Energy/Gold/Utilities), ETFs (XAR or ITA, XLE, GLD, XLU), 6-month horizon.
- Historical analogs: Gulf War, 2022 Ukraine, 2023–2025 ME flare-ups, NATO spending ramp.
- Current context (Feb 28 2026): Direct strikes on Iranian nuclear/missile/leadership sites; Iranian retaliation; oil risk premium $4–10/bbl; gold near/all-time highs (~$5,100+); defense ETFs already +13–18% YTD on record budgets.

**MANDATORY RESEARCH REQUIREMENTS:**
1. Update all data with latest credible sources (Reuters, JPMorgan, IISS Military Balance 2026, EIA, World Gold Council, ETF.com/Yahoo Finance as of Feb 28 2026 or latest).
2. Compare/contrast historical sector reactions vs. today’s higher Hormuz/direct-involvement risk.
3. Cite every claim with live links (minimum 12–15 high-quality sources).

**MONTE CARLO SIMULATION REQUIREMENTS (run at least 3 independent versions):**
- 10,000+ paths, 6-month horizon.
- At least 3 scenario sets: (A) Base historical, (B) Current-escalation weighted (25% quick de-escalation, 45% mild ongoing, 30% severe), (C) Sensitivity (higher severe probability or correlation matrix).
- Output for each sector + recommended portfolio: mean/median return, P(profit), 5% VaR, worst 1% drawdown, Sharpe-like ratio.
- Use Python (numpy/scipy) with realistic 2026-adjusted parameters (include code + results in appendix).

**FINAL REPORT STRUCTURE (exactly this order, 12–18 pages when formatted):**
1. Executive Summary (1 page) – Recommendation table + expected value/risk stats.
2. Investor Profile & Suitability Assessment (1 page) – Risk tolerance score (1–10) with justification, time horizon (months/years) with justification, behavioral factors (at least 2–3 with brief assessment), and fit statement explaining why this allocation aligns with the Persona's profile.
3. Current Geopolitical Context & Probability Tree (Feb 28 2026).
4. Sector Deep-Dives (historical vs. current, with performance tables).
5. ETF Selection & Current Pricing (XAR/ITA, XLE, GLD, XLU + 1–2 alternatives).
6. Monte Carlo Results (tables + charts: distribution histograms, waterfall).
7. Recommended Allocation ($100k split) + Dollar Amounts & Buy Instructions.
8. Risk Management & Exit Rules + Rebalance Triggers.
9. Sensitivity & Stress Tests.
10. Full References & Data Sources.
11. Appendix: Raw MC code + all audit comments from other AIs.

**ADDITIONAL REQUIREMENTS:**
- Include latest ETF AUM, expense ratios, YTD/1-yr/10-yr returns as of Feb 28 2026 (pull from ETF.com or Yahoo Finance).
- Add correlation matrix for the four sectors over last 5 years.
- Include dividend yield impact on total return.
- Provide exact share quantities for $100k (round to nearest whole share at current prices).
- Sensitivity: What if oil disruption lasts 30/90/180 days? What if de-escalation in 2 weeks?
- Visuals: Require histogram charts (describe or generate if tool allows) and a simple allocation pie chart description.

**VALIDATION PROTOCOL:**
- Cross-reference every number with at least two independent sources.
- Run MC simulations yourself and attach results.
- Flag any discrepancies >5% from prior analyses and explain.
- Output confidence level (0–100) for the final recommendation.
- Favor multiple data points over single-source claims for material assertions.

**Deliver the complete Markdown report + separate Python .py file for MC. Be conservative, data-driven, and fiduciary-first. No financial advice disclaimer needed — this is research only.**

---

**Grok-specific add-on:** You already have the full conversation history from the shared Grok Web chat (https://grok.com/share/bGVnYWN5LWNvcHk_74d4dd74-bde3-42ab-83a1-2969c6884a06) — use it as primary context.

**Output:** Save draft to `reports/draft_grok_v1.md` and MC code to `code/monte_carlo_simulator.py` (or append).
