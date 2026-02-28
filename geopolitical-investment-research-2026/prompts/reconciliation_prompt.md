# Grok Reconciliation Prompt

Use this after receiving all three audits (Claude, Gemini, ChatGPT).

**Prompt:**
> Incorporate all valid audit feedback, resolve discrepancies, and produce FINAL version 1.0 with change log.
> Ensure Investor Profile/Suitability section is complete and justified.
> Resolve any audit flags on single-source claims by adding citations or softening language.
> Preserve data-driven, skeptical tone. No optimism or pessimism creep.

**Input:** Attach `reports/draft_grok_v1.md` + `reports/audit_claude.md` + `reports/audit_gemini.md` + `reports/audit_chatgpt.md`

**Output:** Save to `reports/final_validated_report.md`
