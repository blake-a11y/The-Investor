# Gemini Prompt — Phase 3: Company Universe Screen & Market Data
**Agent:** Gemini (Google)
**Project:** Homeland Security Investment Research 2026
**Output file:** `reports/draft_company_universe.md`

---

## Your Role
You are the market intelligence agent. Your job is to build a comprehensive, investment-ready profile of the publicly traded homeland security supply chain — covering market data, analyst sentiment, contract wins, and event sensitivity for each company in the universe.

---

## Company Universe to Cover

### Tier 1 — Direct DHS/FBI Contract Holders
| Ticker | Company | Primary Thesis |
|--------|---------|----------------|
| AXON | Axon Enterprise | Body cameras, Tasers, law enforcement software |
| MSI | Motorola Solutions | Public safety comms, CAD systems, dispatch |
| PLTR | Palantir Technologies | Intelligence analytics, federal AI contracts |
| LDOS | Leidos Holdings | DHS/FBI IT systems integration |
| BAH | Booz Allen Hamilton | Intelligence community consulting + tech |
| SAIC | Science Applications International | Federal systems integration |

### Tier 2 — First Responder & Physical Security
| Ticker | Company | Primary Thesis |
|--------|---------|----------------|
| MSA | MSA Safety | SCBA, protective gear, first responder equipment |
| PSN | Parsons Corporation | Federal infrastructure + security programs |
| INVE | Identiv | Physical access control, credentials |

### Tier 3 — Communications & Cyber
| Ticker | Company | Primary Thesis |
|--------|---------|----------------|
| LHX | L3Harris Technologies | Federal comms, surveillance, ISR |
| CRWD | CrowdStrike Holdings | Endpoint security, federal cyber |
| PANW | Palo Alto Networks | Federal network security |
| T | AT&T / FirstNet | First responder broadband network |

---

## For Each Company, Pull and Report:

### Market Data (as of most recent available)
- Current stock price
- Market cap
- 52-week range
- YTD performance vs S&P 500
- Average daily volume

### Analyst Consensus
- Buy / Hold / Sell breakdown
- Consensus price target
- Implied upside from current price
- Most recent rating changes (last 90 days)

### Revenue & Contract Profile
- TTM revenue
- % from U.S. government (federal)
- % from DHS/DOJ/FBI specifically (if disclosed)
- Contract backlog ($M and months of coverage)
- Most significant contract wins in last 12 months (press releases + USASpending.gov verification)

### Event Sensitivity (Historical)
Research and report actual stock performance during:
- **9/11 aftermath (Sep–Dec 2001):** If company existed, what happened?
- **Post-Soleimani (Jan 2020):** +30 day performance
- **COVID-19 federal spending surge (2020–2021):** Revenue impact
- **Ukraine invasion defense spending surge (Feb 2022):** Performance

### Competitive Position
- Primary competitors (public and private)
- Key contract vehicles held (IDIQ names, GSA schedules)
- Any contract loss risks (rebid timelines)
- Organic vs. acquisition growth profile

---

## Additional Research Tasks

### 1. ETF Universe
Identify all ETFs with >5% weight in homeland security / public safety:
- ITA (iShares U.S. Aerospace & Defense)
- CEFA (any dedicated homeland security ETF?)
- XAR (confirmed from Iran report)
- Any pure-play HomeSec ETF (research if one exists — HOMS was delisted, find current alternatives)

For each ETF: AUM, ER, top 10 holdings, YTD performance, 1-year performance.

### 2. Recent Sector News (Last 90 Days)
Pull major contract announcements, earnings surprises, and analyst upgrades in the homeland security sector. Flag anything material.

### 3. Valuation Context
- Where does each company trade vs. its defense/government IT peer group?
- What is the sector average P/E and EV/EBITDA?
- Which companies look cheap vs. peers on a contract-backlog-adjusted basis?

---

## Source Priority
1. SEC EDGAR (edgar.sec.gov) — official filings
2. USASpending.gov — contract verification
3. Company investor relations pages — earnings transcripts
4. Bloomberg / Reuters / WSJ for analyst consensus
5. Morningstar / ETF.com for ETF data
6. Defense News / FCW / GovExec for contract reporting

**Minimum: ≥2 independent sources per material data point. No Wikipedia.**

---

## Output Format
`reports/draft_company_universe.md`:

```markdown
# Company Universe — Homeland Security Supply Chain
**Agent:** Gemini | **Date:** [date] | **Status:** Draft — Pending Audit

## 1. Executive Summary — Investment Universe Overview
## 2. Tier 1 Company Profiles (full detail each)
## 3. Tier 2 Company Profiles
## 4. Tier 3 Company Profiles
## 5. ETF Options
## 6. Sector Valuation Context
## 7. Recent Material News
## 8. Source List
```

Commit with message: `"Phase 3 complete: Gemini company universe screen"`
