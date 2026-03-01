# Claude Code Prompt — Phase 2A: Agency Budget & Contract Flow
**Agent:** Claude Code (Anthropic)
**Project:** Homeland Security Investment Research 2026
**Output files:** `data/usaspending_raw/` + `reports/draft_agency_mapping.md`

---

## Your Role
You are the data engineering agent. Your job is to pull structured contract and budget data from public government APIs and databases, then map the agency → contract vehicle → publicly traded prime contractor chain for the homeland security supply chain.

---

## Task 1 — USASpending.gov API Pull

Use the USASpending.gov public API (no key required) to extract:

```python
# Base URL: https://api.usaspending.gov/api/v2/

# Pull 1: DHS total contract obligations FY2022–2025
GET /agency/070/budgetary_resources/  # DHS agency code: 070

# Pull 2: Top 50 DHS contractors by total obligation FY2022–2025
GET /search/spending_by_award/
  filters:
    agencies: [DHS, FBI/DOJ, FEMA, TSA, CBP, Secret Service]
    award_type_codes: [A, B, C, D]  # contracts only
    time_period: FY2022–FY2025

# Pull 3: Contract surge analysis — compare FY2001 vs FY2002 (9/11 analog)
# Use historical data endpoint

# Pull 4: IDIQ vehicles held by top contractors
GET /search/spending_by_award/
  filters: award_type_codes: [IDV_A, IDV_B]
```

Save raw JSON responses to `data/usaspending_raw/`:
- `dhs_obligations_fy22_25.json`
- `top_contractors_dhs.json`
- `911_surge_analog.json`
- `idiq_vehicles.json`

Also pull from **SAM.gov** (System for Award Management):
- Active IDIQ vehicles in homeland security NAICS codes
- GSA Schedule holders in security/law enforcement categories

---

## Task 2 — Agency Response Mapping

For each of these agencies, document the standard emergency procurement mechanism:
- **DHS** — Primary coordinator; Emergency Support Function (ESF) #13
- **FBI** — Crisis response, evidence, counterterrorism
- **FEMA** — Disaster response; Public Assistance program
- **TSA** — Aviation/transit security surge
- **CBP** — Border surge, ports of entry
- **NORTHCOM/National Guard** — Domestic military support
- **CISA** — Critical infrastructure protection
- **Secret Service** — VIP protection surge

For each agency output:
```markdown
| Agency | Primary Contract Vehicle | Typical Surge Trigger | Historical Surge Multiplier | Top 5 Prime Contractors (publicly traded only) |
```

Use GAO reports (gao.gov) and CRS reports to source surge multipliers.
Post-9/11 DHS budget went from ~$0 to $40B+ — document the ramp rate.

---

## Task 3 — Publicly Traded Prime Contractor Identification

Cross-reference your USASpending data against publicly traded companies:

For each company identified as a top contractor, pull from SEC EDGAR:
```
https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&company=[name]&type=10-K

From 10-K filings extract:
- % revenue from U.S. government contracts
- Specific agency relationships mentioned
- Contract backlog dollar amount
- Backlog as months of revenue
- Any IDIQ ceiling amounts disclosed
```

Target companies to verify (add any discovered via USASpending):
AXON, MSI, PLTR, LDOS, BAH, SAIC, MSA, PSN, LHX, CRWD, PANW

---

## Task 4 — Surge Multiplier Model

Build `code/usaspending_pull.py` that:
1. Hits the USASpending API for the agencies above
2. Calculates YoY contract growth rate for each agency FY2022–2025
3. Applies a post-event surge multiplier (source from GAO/CRS)
4. Outputs: projected contract award increase per agency per scenario

```python
# Scenario multipliers to model (source from GAO post-9/11 analysis):
scenario_multipliers = {
    'A_minor':      1.15,   # 15% surge
    'B_coordinated': 1.45,  # 45% surge  
    'C_mass_casualty': 2.10 # 110% surge (9/11 analog)
}
```

---

## Output Format
`reports/draft_agency_mapping.md`:

```markdown
# Agency Budget & Contract Flow Analysis
**Agent:** Claude Code | **Date:** [date] | **Status:** Draft — Pending Audit

## 1. Agency Response Chain (Event → Agency → Contract)
## 2. Top Publicly Traded Prime Contractors by Agency
## 3. Contract Vehicle Analysis (IDIQ ceilings, GSA schedules)
## 4. Historical Surge Multipliers (sourced from GAO/CRS)
## 5. Projected Contract Award Surge by Scenario
## 6. Data Sources & API References
```

Commit with message: `"Phase 2A complete: Agency mapping and USASpending data"`
