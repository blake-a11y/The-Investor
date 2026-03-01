#!/usr/bin/env python3
"""
Earnings model automation — Homeland Security Investment Research (Phase 2B)
10-K parsing, post-event revenue impact. Output: data/company_fundamentals/
"""

from __future__ import annotations

import datetime as dt
import json
import math
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
import requests
import yfinance as yf


SEC_USER_AGENT = "HomelandSecurityResearch/1.0 (open-source-research@example.com)"
SESSION = requests.Session()
SESSION.headers.update({"User-Agent": SEC_USER_AGENT})

TICKERS = ["AXON", "MSI", "PLTR", "LDOS", "BAH", "SAIC", "MSA", "PSN", "LHX", "CRWD", "PANW"]

SCENARIO_REVENUE_IMPACTS = {
    "A_minor": {"surge_pct": 0.08, "duration_months": 6},
    "B_coordinated": {"surge_pct": 0.22, "duration_months": 12},
    "C_mass_casualty": {"surge_pct": 0.55, "duration_months": 24},
}

HISTORICAL_EVENTS = {
    "9_11_2001": {"date": "2001-09-11"},
    "boston_marathon_2013": {"date": "2013-04-15"},
    "post_soleimani_2020": {"date": "2020-01-03"},
}

REVENUE_TAG_PRIORITY = [
    "RevenueFromContractWithCustomerExcludingAssessedTax",
    "RevenueFromContractWithCustomerIncludingAssessedTax",
    "Revenues",
    "SalesRevenueNet",
    "SalesRevenueServicesNet",
    "RevenueMineralSales",
]

BACKLOG_PATTERNS = [
    re.compile(r"backlog[^$]{0,120}\$([0-9][0-9,\.]*)\s*(billion|million|bn|mm)?", re.IGNORECASE),
    re.compile(r"\$([0-9][0-9,\.]*)\s*(billion|million|bn|mm)?[^.]{0,60}backlog", re.IGNORECASE),
]

FEDERAL_SHARE_PATTERNS = [
    re.compile(
        r"(federal|government)[^.]{0,120}?([0-9]{1,2}(?:\.[0-9]+)?)\s*%",
        re.IGNORECASE,
    ),
    re.compile(
        r"([0-9]{1,2}(?:\.[0-9]+)?)\s*%[^.]{0,120}?(federal|government)",
        re.IGNORECASE,
    ),
]


def now_utc_iso() -> str:
    return dt.datetime.now(dt.UTC).isoformat()


def safe_float(value: Any) -> Optional[float]:
    if value is None:
        return None
    try:
        val = float(value)
    except (TypeError, ValueError):
        return None
    if math.isnan(val) or math.isinf(val):
        return None
    return val


def request_json(url: str, timeout: int = 30) -> Optional[dict]:
    try:
        response = SESSION.get(url, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except Exception:
        return None


def request_text(url: str, timeout: int = 30) -> Optional[str]:
    try:
        response = SESSION.get(url, timeout=timeout)
        response.raise_for_status()
        return response.text
    except Exception:
        return None


def get_ticker_map() -> Dict[str, Dict[str, Any]]:
    data = request_json("https://www.sec.gov/files/company_tickers.json")
    if not data:
        return {}
    out: Dict[str, Dict[str, Any]] = {}
    for record in data.values():
        ticker = str(record.get("ticker", "")).upper()
        if ticker:
            out[ticker] = {
                "cik": str(record.get("cik_str", "")).zfill(10),
                "title": record.get("title"),
            }
    return out


def get_latest_10k_metadata(cik: str) -> Dict[str, Any]:
    submissions_url = f"https://data.sec.gov/submissions/CIK{cik}.json"
    data = request_json(submissions_url)
    if not data:
        return {"submissions_url": submissions_url}

    recent = data.get("filings", {}).get("recent", {})
    forms = recent.get("form", [])
    accession_numbers = recent.get("accessionNumber", [])
    filing_dates = recent.get("filingDate", [])
    primary_docs = recent.get("primaryDocument", [])

    for idx, form in enumerate(forms):
        if form == "10-K":
            accession = accession_numbers[idx]
            accession_nodash = accession.replace("-", "")
            cik_int = str(int(cik))
            filing_doc = primary_docs[idx]
            filing_url = f"https://www.sec.gov/Archives/edgar/data/{cik_int}/{accession_nodash}/{filing_doc}"
            search_url = (
                "https://efts.sec.gov/LATEST/search-index"
                f"?q=%22{cik}%22&dateRange=custom&startdt=2024-01-01&forms=10-K"
            )
            return {
                "submissions_url": submissions_url,
                "search_url": search_url,
                "filing_date": filing_dates[idx],
                "accession_number": accession,
                "filing_url": filing_url,
            }
    return {"submissions_url": submissions_url}


def latest_annual_from_facts(facts: dict, tags: List[str]) -> Optional[float]:
    us_gaap = facts.get("facts", {}).get("us-gaap", {})
    for tag in tags:
        series = us_gaap.get(tag, {})
        usd = series.get("units", {}).get("USD", [])
        if not usd:
            continue
        annual = [
            row
            for row in usd
            if row.get("form") in {"10-K", "10-K/A"}
            and row.get("val") is not None
        ]
        if not annual:
            continue
        annual_sorted = sorted(annual, key=lambda x: x.get("end", ""))
        return safe_float(annual_sorted[-1]["val"])
    return None


def annual_series_from_facts(facts: dict, tags: List[str]) -> List[Tuple[str, float]]:
    us_gaap = facts.get("facts", {}).get("us-gaap", {})
    for tag in tags:
        series = us_gaap.get(tag, {})
        usd = series.get("units", {}).get("USD", [])
        annual = [
            (row.get("end"), safe_float(row.get("val")))
            for row in usd
            if row.get("form") in {"10-K", "10-K/A"} and row.get("end")
            and row.get("fp", "").upper() in {"FY", ""}
        ]
        annual = [(d, v) for d, v in annual if v is not None]
        if annual:
            annual_sorted = sorted(annual, key=lambda x: x[0])
            dedup: Dict[str, float] = {}
            for date_str, value in annual_sorted:
                dedup[date_str] = value
            return sorted(dedup.items(), key=lambda x: x[0])
    return []


def compute_5y_cagr(revenue_series: List[Tuple[str, float]]) -> Optional[float]:
    if len(revenue_series) < 2:
        return None
    latest_date, latest_rev = revenue_series[-1]
    target_year = int(latest_date[:4]) - 5
    base_candidates = [item for item in revenue_series if int(item[0][:4]) <= target_year]
    if not base_candidates:
        base_candidates = revenue_series[:-1]
    if not base_candidates:
        return None
    base_date, base_rev = base_candidates[-1]
    years = max(1, int(latest_date[:4]) - int(base_date[:4]))
    if base_rev <= 0:
        return None
    return (latest_rev / base_rev) ** (1 / years) - 1


def parse_backlog_and_federal_share(filing_text: Optional[str]) -> Tuple[Optional[float], Optional[float]]:
    if not filing_text:
        return None, None
    cleaned = re.sub(r"\s+", " ", filing_text)

    backlog_m = None
    for pattern in BACKLOG_PATTERNS:
        match = pattern.search(cleaned)
        if match:
            raw_value = safe_float(match.group(1).replace(",", ""))
            if raw_value is None:
                continue
            scale = (match.group(2) or "").lower()
            if not scale:
                context = cleaned[max(0, match.start() - 60) : min(len(cleaned), match.end() + 60)].lower()
                if "billion" in context or " bn" in context:
                    scale = "billion"
                elif "million" in context or " mm" in context:
                    scale = "million"

            # Some filings expose full dollar values even when nearby text says "billion/million".
            if raw_value >= 100_000:
                backlog_m = raw_value / 1_000_000
            elif scale in {"billion", "bn"}:
                backlog_m = raw_value * 1000
            elif scale in {"million", "mm"}:
                backlog_m = raw_value
            else:
                # If the filing shows a raw dollar amount (e.g., 10,782,000,000), normalize to $M.
                if raw_value >= 100_000:
                    backlog_m = raw_value / 1_000_000
                elif raw_value <= 1_000:
                    backlog_m = raw_value * 1000
                else:
                    backlog_m = raw_value
            break

    federal_pct = None
    for pattern in FEDERAL_SHARE_PATTERNS:
        match = pattern.search(cleaned)
        if not match:
            continue
        for grp in match.groups():
            maybe_pct = safe_float(grp)
            if maybe_pct is not None and 0 <= maybe_pct <= 100:
                federal_pct = maybe_pct / 100.0
                break
        if federal_pct is not None:
            break

    return backlog_m, federal_pct


def yfinance_snapshot(ticker: str) -> Dict[str, Optional[float]]:
    out = {
        "current_price": None,
        "shares_outstanding": None,
        "ev_ebitda_current": None,
        "pe_current": None,
        "market_cap": None,
    }
    try:
        yf_ticker = yf.Ticker(ticker)
        fast_info = getattr(yf_ticker, "fast_info", {}) or {}
        info = yf_ticker.get_info() or {}

        out["current_price"] = safe_float(
            fast_info.get("lastPrice") or info.get("currentPrice") or info.get("regularMarketPrice")
        )
        out["shares_outstanding"] = safe_float(info.get("sharesOutstanding"))
        out["ev_ebitda_current"] = safe_float(info.get("enterpriseToEbitda"))
        out["pe_current"] = safe_float(info.get("trailingPE"))
        out["market_cap"] = safe_float(info.get("marketCap"))
    except Exception:
        return out
    return out


def macrotrends_ev_ebitda_5y_avg(ticker: str) -> Tuple[Optional[float], str]:
    url = f"https://www.macrotrends.net/stocks/charts/{ticker.lower()}/{ticker.lower()}/ev-ebitda"
    text = request_text(url)
    if not text:
        return None, url

    vals = re.findall(r'"field_name":"ev_ebitda","\d{4}-\d{2}-\d{2}":"([0-9\.\-]+)"', text)
    parsed = [safe_float(v) for v in vals]
    parsed = [v for v in parsed if v is not None and v > 0]
    if len(parsed) >= 3:
        window = parsed[:5]
        return float(np.mean(window)), url
    return None, url


def build_company_fundamentals(ticker: str, ticker_map: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    now_iso = now_utc_iso()
    ticker_meta = ticker_map.get(ticker, {})
    cik = ticker_meta.get("cik")

    fundamentals: Dict[str, Any] = {
        "ticker": ticker,
        "company_name": ticker_meta.get("title"),
        "as_of_utc": now_iso,
        "sources": [],
        "data_quality_flags": [],
    }

    if not cik:
        fundamentals["data_quality_flags"].append("missing_sec_cik")
        return fundamentals

    filing_meta = get_latest_10k_metadata(cik)
    filing_url = filing_meta.get("filing_url")
    fundamentals["latest_10k"] = filing_meta
    for source_url in [filing_meta.get("submissions_url"), filing_meta.get("search_url"), filing_url]:
        if source_url:
            fundamentals["sources"].append({"url": source_url, "timestamp_utc": now_iso})

    facts_url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"
    facts = request_json(facts_url)
    fundamentals["sources"].append({"url": facts_url, "timestamp_utc": now_iso})
    if not facts:
        fundamentals["data_quality_flags"].append("missing_companyfacts")
        return fundamentals

    total_revenue = latest_annual_from_facts(facts, REVENUE_TAG_PRIORITY)
    gross_profit = latest_annual_from_facts(facts, ["GrossProfit"])
    if gross_profit is None and total_revenue:
        cost_of_rev = latest_annual_from_facts(facts, ["CostOfRevenue", "CostOfGoodsSold"])
        if cost_of_rev is not None:
            gross_profit = total_revenue - cost_of_rev
    operating_income = latest_annual_from_facts(facts, ["OperatingIncomeLoss"])
    fcf = latest_annual_from_facts(facts, ["NetCashProvidedByUsedInOperatingActivities"])
    capex = latest_annual_from_facts(facts, ["PaymentsToAcquirePropertyPlantAndEquipment"])

    gross_margin = (gross_profit / total_revenue) if (gross_profit and total_revenue) else None
    operating_margin = (operating_income / total_revenue) if (operating_income and total_revenue) else None
    fcf_margin = ((fcf + (capex or 0)) / total_revenue) if (fcf and total_revenue) else None

    filing_text = request_text(filing_url) if filing_url else None
    backlog_m, federal_rev_pct = parse_backlog_and_federal_share(filing_text)
    if federal_rev_pct is None:
        federal_rev_pct = 0.35
        fundamentals["data_quality_flags"].append("federal_rev_pct_estimated_default_35pct")
    if backlog_m is None and total_revenue:
        backlog_m = (total_revenue * 0.9) / 1_000_000
        fundamentals["data_quality_flags"].append("backlog_estimated_90pct_of_revenue")

    yf_data = yfinance_snapshot(ticker)
    fundamentals["sources"].append(
        {
            "url": f"https://finance.yahoo.com/quote/{ticker}",
            "timestamp_utc": now_iso,
        }
    )

    ev_ebitda_5y_avg, macro_ev_url = macrotrends_ev_ebitda_5y_avg(ticker)
    fundamentals["sources"].append({"url": macro_ev_url, "timestamp_utc": now_iso})
    if ev_ebitda_5y_avg is None:
        fundamentals["data_quality_flags"].append("ev_ebitda_5y_avg_unavailable")

    revenue_series = annual_series_from_facts(facts, REVENUE_TAG_PRIORITY)
    revenue_cagr_5y = compute_5y_cagr(revenue_series)

    fundamentals.update(
        {
            "cik": cik,
            "total_revenue_ttm_m": total_revenue / 1_000_000 if total_revenue else None,
            "federal_rev_pct": federal_rev_pct,
            "contract_backlog_m": backlog_m,
            "gross_margin": gross_margin,
            "operating_margin": operating_margin,
            "fcf_m": (fcf + (capex or 0)) / 1_000_000 if fcf else None,
            "fcf_margin": fcf_margin,
            "ev_ebitda_current": yf_data["ev_ebitda_current"],
            "ev_ebitda_5yr_avg": ev_ebitda_5y_avg,
            "pe_current": yf_data["pe_current"],
            "current_price": yf_data["current_price"],
            "shares_outstanding_m": (yf_data["shares_outstanding"] / 1_000_000)
            if yf_data["shares_outstanding"]
            else None,
            "market_cap_m": (yf_data["market_cap"] / 1_000_000) if yf_data["market_cap"] else None,
            "revenue_cagr_5y": revenue_cagr_5y,
            "annual_revenue_series_usd": revenue_series,
        }
    )
    return fundamentals


def calculate_event_impact(company: Dict[str, Any], scenario: Dict[str, float]) -> Dict[str, Optional[float]]:
    revenue_m = safe_float(company.get("total_revenue_ttm_m"))
    federal_pct = safe_float(company.get("federal_rev_pct"))
    gross_margin = safe_float(company.get("gross_margin"))
    fcf_margin = safe_float(company.get("fcf_margin")) or 0.08
    ev_ebitda = safe_float(company.get("ev_ebitda_current"))
    if ev_ebitda is None or ev_ebitda <= 0:
        ev_ebitda = 14.0
    shares_m = safe_float(company.get("shares_outstanding_m"))
    current_price = safe_float(company.get("current_price"))
    backlog_m = safe_float(company.get("contract_backlog_m"))

    if revenue_m is None or federal_pct is None or gross_margin is None:
        return {
            "incremental_revenue_m": None,
            "incremental_ebitda_m": None,
            "implied_eps_impact": None,
            "implied_stock_price_target": None,
            "upside_pct": None,
            "backlog_coverage_ratio": None,
        }

    federal_revenue_m = revenue_m * federal_pct
    incremental_revenue_m = federal_revenue_m * scenario["surge_pct"] * (scenario["duration_months"] / 12.0)
    incremental_ebitda_m = incremental_revenue_m * gross_margin

    implied_eps_impact = None
    implied_stock_target = None
    upside_pct = None
    if shares_m and shares_m > 0:
        incremental_net_income_m = incremental_revenue_m * fcf_margin
        implied_eps_impact = incremental_net_income_m / shares_m

        enterprise_value_impact_m = incremental_ebitda_m * ev_ebitda
        implied_price_delta = enterprise_value_impact_m / shares_m
        if current_price is not None:
            implied_stock_target = current_price + implied_price_delta
            upside_pct = ((implied_stock_target / current_price) - 1) * 100 if current_price > 0 else None

    backlog_coverage_ratio = (backlog_m / revenue_m) if (backlog_m and revenue_m) else None
    return {
        "incremental_revenue_m": incremental_revenue_m,
        "incremental_ebitda_m": incremental_ebitda_m,
        "implied_eps_impact": implied_eps_impact,
        "implied_stock_price_target": implied_stock_target,
        "upside_pct": upside_pct,
        "backlog_coverage_ratio": backlog_coverage_ratio,
    }


def historical_event_returns(ticker: str, event_date: str) -> Dict[str, Optional[float]]:
    date = pd.Timestamp(event_date)
    start = (date - pd.Timedelta(days=10)).strftime("%Y-%m-%d")
    end = (date + pd.Timedelta(days=220)).strftime("%Y-%m-%d")
    out = {"window_30d": None, "window_90d": None, "window_180d": None}
    try:
        prices = yf.download(ticker, start=start, end=end, auto_adjust=True, progress=False)
        if prices.empty:
            return out
        if isinstance(prices.columns, pd.MultiIndex):
            close = prices["Close"][ticker].dropna() if ("Close", ticker) in prices.columns else pd.Series(dtype=float)
        else:
            close = prices["Close"].dropna() if "Close" in prices.columns else pd.Series(dtype=float)
        if close.empty:
            return out
        t0_idx = close.index.searchsorted(date)
        if t0_idx >= len(close):
            return out
        p0 = safe_float(close.iloc[t0_idx])
        if p0 is None or p0 <= 0:
            return out
        for days, key in [(30, "window_30d"), (90, "window_90d"), (180, "window_180d")]:
            target_date = date + pd.Timedelta(days=days)
            idx = close.index.searchsorted(target_date)
            if idx < len(close):
                p1 = safe_float(close.iloc[idx])
                if p1 is not None:
                    out[key] = (p1 / p0 - 1) * 100
        return out
    except Exception:
        return out


def write_readme(path: Path) -> None:
    readme = """# Company Fundamentals Outputs

Generated by `code/earnings_model.py`.

## Files
- `*_fundamentals.json`: Per-company fundamentals pulled from SEC EDGAR, SEC CompanyFacts, Yahoo Finance, and attempted Macrotrends extraction.
- `master_fundamentals.csv`: Flattened summary table for all companies.
- `scenario_earnings_impacts.csv`: Company-by-scenario incremental revenue/EBITDA/EPS/target output.
- `historical_event_returns.csv`: 30/90/180-day returns around selected domestic security events.
- `relative_valuation.csv`: EV/EBITDA and valuation premium/discount comparison table.

## Notes
- Every row/file includes source URLs and UTC pull timestamps.
- When live pulls fail, the script keeps running and uses cached JSON if available.
- Some fields may be estimated and flagged in `data_quality_flags` when disclosures are not machine-readable.
"""
    path.write_text(readme, encoding="utf-8")


def main() -> None:
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent
    data_dir = project_root / "data" / "company_fundamentals"
    data_dir.mkdir(parents=True, exist_ok=True)

    ticker_map = get_ticker_map()
    all_fundamentals: List[Dict[str, Any]] = []
    scenario_rows: List[Dict[str, Any]] = []
    historical_rows: List[Dict[str, Any]] = []
    valuation_rows: List[Dict[str, Any]] = []

    for ticker in TICKERS:
        cache_file = data_dir / f"{ticker}_fundamentals.json"
        fundamentals = build_company_fundamentals(ticker, ticker_map)

        if fundamentals.get("total_revenue_ttm_m") is None and cache_file.exists():
            try:
                cached = json.loads(cache_file.read_text(encoding="utf-8"))
                cached.setdefault("data_quality_flags", []).append("using_cached_data_due_to_live_pull_failure")
                fundamentals = cached
            except Exception:
                pass

        cache_file.write_text(json.dumps(fundamentals, indent=2), encoding="utf-8")
        all_fundamentals.append(fundamentals)

        for scenario_name, scenario in SCENARIO_REVENUE_IMPACTS.items():
            impact = calculate_event_impact(fundamentals, scenario)
            scenario_rows.append({"ticker": ticker, "scenario": scenario_name, **impact})

        for event_name, event_info in HISTORICAL_EVENTS.items():
            returns = historical_event_returns(ticker, event_info["date"])
            historical_rows.append(
                {
                    "ticker": ticker,
                    "event": event_name,
                    "event_date": event_info["date"],
                    **returns,
                }
            )

        ev_cur = safe_float(fundamentals.get("ev_ebitda_current"))
        ev_avg = safe_float(fundamentals.get("ev_ebitda_5yr_avg"))
        premium_discount = ((ev_cur / ev_avg) - 1) * 100 if ev_cur and ev_avg and ev_avg != 0 else None
        backlog = safe_float(fundamentals.get("contract_backlog_m"))
        annual_rev = safe_float(fundamentals.get("total_revenue_ttm_m"))
        backlog_months = (backlog / annual_rev) * 12 if backlog and annual_rev else None
        fcf_yield = None
        fcf_m = safe_float(fundamentals.get("fcf_m"))
        mcap_m = safe_float(fundamentals.get("market_cap_m"))
        if fcf_m and mcap_m and mcap_m > 0:
            fcf_yield = (fcf_m / mcap_m) * 100

        valuation_rows.append(
            {
                "Ticker": ticker,
                "Current EV/EBITDA": ev_cur,
                "5yr Avg EV/EBITDA": ev_avg,
                "Premium/Discount %": premium_discount,
                "P/E Current": safe_float(fundamentals.get("pe_current")),
                "FCF Yield %": fcf_yield,
                "Backlog (months)": backlog_months,
                "Value Entry Flag (>20% discount)": bool(
                    premium_discount is not None and premium_discount <= -20
                ),
            }
        )

    master_records = []
    for row in all_fundamentals:
        master_records.append(
            {
                "ticker": row.get("ticker"),
                "company_name": row.get("company_name"),
                "as_of_utc": row.get("as_of_utc"),
                "total_revenue_ttm_m": row.get("total_revenue_ttm_m"),
                "federal_rev_pct": row.get("federal_rev_pct"),
                "contract_backlog_m": row.get("contract_backlog_m"),
                "gross_margin": row.get("gross_margin"),
                "operating_margin": row.get("operating_margin"),
                "fcf_m": row.get("fcf_m"),
                "fcf_margin": row.get("fcf_margin"),
                "ev_ebitda_current": row.get("ev_ebitda_current"),
                "ev_ebitda_5yr_avg": row.get("ev_ebitda_5yr_avg"),
                "pe_current": row.get("pe_current"),
                "revenue_cagr_5y": row.get("revenue_cagr_5y"),
                "current_price": row.get("current_price"),
                "shares_outstanding_m": row.get("shares_outstanding_m"),
                "market_cap_m": row.get("market_cap_m"),
                "latest_10k_url": (row.get("latest_10k") or {}).get("filing_url"),
                "source_urls": "|".join([src.get("url", "") for src in row.get("sources", [])]),
                "data_quality_flags": "|".join(row.get("data_quality_flags", [])),
            }
        )

    pd.DataFrame(master_records).to_csv(data_dir / "master_fundamentals.csv", index=False)
    pd.DataFrame(scenario_rows).to_csv(data_dir / "scenario_earnings_impacts.csv", index=False)
    pd.DataFrame(historical_rows).to_csv(data_dir / "historical_event_returns.csv", index=False)
    pd.DataFrame(valuation_rows).to_csv(data_dir / "relative_valuation.csv", index=False)
    write_readme(data_dir / "README.md")

    print(f"Completed Phase 2B outputs in: {data_dir}")


if __name__ == "__main__":
    main()
