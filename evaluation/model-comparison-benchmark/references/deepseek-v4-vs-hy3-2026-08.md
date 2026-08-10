# Worked example: DeepSeek V4 Pro vs Tencent Hy3 (2026-08-10)

A complete live head-to-head run that produced `empirical-test-results.md`. Use as a concrete pattern reference.

## Setup facts
- Models discovered via API listing (never assumed): `deepseek-v4-pro` + `deepseek-v4-flash` (official API), `tencent/hy3` paid (OpenRouter). No `tencent/hy3:free` variant existed — models list is the source of truth.
- Hy3 served by **Tencent Cloud** provider (OpenRouter `provider` field) — a fair same-vendor comparison.
- Pricing (fetched): DeepSeek V4 Pro $0.435/M input (cache miss), $0.003625/M (hit), $0.87/M output; Hy3 $0.132/M in, $0.528/M out. DeepSeek official page also warns of a planned price increase — re-check per run.
- Params: temp 0, max_tokens 4096, stream off, one system prompt, both in default thinking mode. Raw JSON saved to `raw-test/` and `raw-test-r2/`.

## Ground truths (all brute-force verified — one hand derivation was wrong)
| Q | Answer | Note |
|---|---|---|
| n²+2025 is a square, sum of n | 1768 | |
| sum of x∈[1,999] with x²≡1 mod 10 | 100000 | 200 numbers |
| 5-digit palindromes divisible by 9 | **100** | hand-derived 90 was WRONG (digit 9 double-counts residue 0) |
| min_platforms test | 3 | |
| is_balanced('([{}])()','([)]') | True, False | |
| look_and_say(6) | ['1','11','21','1211','111221','312211'] | |
| 3 mislabeled boxes | pick "Apples and Oranges" | |
| Zorb/Fribble/Quark syllogism | A | |
| 10g H₂ + 64g O₂ limiting reagent | O₂, 72 g | |
| non-consecutive-term president | Cleveland, 1885–89 & 1893–97 | |
| 2nd letter of 4th word of "the fourth word of this sentence" | f | |
| JSON of 3 primes in (30,50) | [31,37,41] | |
| contest: 30 q, 101 pts | 7 wrong | |
| # of n with n! ending in exactly 2025 zeros | 5 | blocks of 5 per v5 value |
| longest_palindrome('babad','cbbd') | bab, bb | |
| bloops/zorps/quibbles | Yes | |
| letter 5 after 'k' in brackets | [p] | |
| 8 apples, 3 kids, 1–5 each | 18 | |

## The headline failure (reproducible)
DeepSeek q102: "For how many positive integers n does n! end in exactly 2025 zeros?" → `finish_reason=length`, **empty content**, twice (original + identical-params retry). Its reasoning (11,190 chars) had concluded correctly ("the number of n with Z(n)=K is either 0 or 5… So for K=2025, it's 5") then spiraled: "**But wait! Is it guaranteed that the block starting at 8115 is the only one? Since Z is non…**" and burned the rest of the budget. Hy3 answered `5` in-budget (40 s, 2,948 tokens).

## Results & costs
- Scores: round 1 (12Q) 12/12 both; round 2 (6Q) DeepSeek 5/6, Hy3 6/6 → **17/18 vs 18/18**.
- Tokens/cost (grand totals, from raw usage): DeepSeek 2,112p/17,478c = 19,590 tok, **$0.01612**; Hy3 2,171p/21,144c = 23,315 tok, **$0.01171**. OpenRouter billed `cost` field used for Hy3; DeepSeek computed from official prices (all cache misses).
- Efficiency: DeepSeek used 46.7% fewer output tokens (7,440 vs 13,950 in R1) and ~2.4× faster (avg 6.9 s vs 16.3 s per question) — despite Hy3's lower list price, per-question cost was comparable.
- Verdict shape: "No — Hy3 edged it on reliability (a 4096-token budget blowup), tied on capability, DeepSeek wins on speed/tokens." Note the failure is budget-dependent; with a higher cap DeepSeek likely answers.

## Report layout that worked
Methodology table (ids/params/date/pricing) → per-question score table with ground truths → token/cost table with per-round + grand totals → notable failures with verbatim quotes → verdict with explicit caveats (n=18, single run, budget-dependence, not statistically significant). Raw JSONs kept on disk for independent verification.
