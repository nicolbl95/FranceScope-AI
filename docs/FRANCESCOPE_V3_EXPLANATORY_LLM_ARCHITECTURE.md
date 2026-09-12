# FranceScope V3 — Explanatory LLM Architecture

Date: 2026-08-24. Explanation-only layer over frozen V3 presentation artifacts.

## 1. Route / API architecture

- **Next.js Route Handler**: `src/app/api/explain/route.ts` (Node runtime).
- Single POST endpoint accepting `{ question: string }`, returning:
  `{ answer, sources, answer_scope }` on success, or `{ error }` with an
  appropriate HTTP status on failure.
- The page `src/app/ask/page.tsx` is a client component that POSTs only the
  user's question. No system prompt, context, or API key is ever sent from the
  browser. The client cannot override server-side instructions.

Input safety enforced server-side: non-empty check, max length 2000 characters,
no client-supplied context field.

## 2. Provider abstraction — `src/lib/llm.ts`

One module, one function: `generateExplanation(systemPrompt, userPrompt)`.
- Uses the **OpenAI-compatible** `/v1/chat/completions` contract via native
  `fetch` (no SDK dependency added).
- Configured entirely by environment variables (see §7).
- Throws `LLMNotConfiguredError` when no key is present, which the route maps
  to a 503 with a developer-friendly message. No fake answer is ever produced.

This keeps provider choice replaceable: change `FRANCESCOPE_LLM_BASE_URL` /
`FRANCESCOPE_LLM_MODEL` without touching UI or prompt logic.

## 3. Deterministic grounding — `src/lib/grounding.ts`

- Loads the four authoritative presentation artifacts from `public/data` via the
  existing server-side `fs` loader (`@/lib/data`):
  - `historical_index.json`
  - `distributions.json`
  - `scenarios.json`
  - `methodology.json`
- A lightweight **keyword classifier** maps each question to a scope
  (`historical | distribution | scenario | methodology | mixed`) and selects only
  the relevant compact JSON blocks (methodology is always included; others are
  added per scope). This is deliberate deterministic routing — **no embeddings,
  no RAG, no vector DB**.
- Assembles a strict **system prompt** containing permanent FranceScope facts
  and guard rails, plus a **user prompt** carrying the selected JSON context and
  the question. The route returns `answer_scope` and `sources` for provenance.

## 4. Authoritative context sources

Only the four JSON files above are used. The assistant never reasons over raw
MC1000 parquet, the 24,000 raw path rows, or arbitrary repository source files.

## 5. Causal & factual restrictions (encoded in system prompt)

Allowed causal language is limited to links the implemented model supports
(e.g. AI productivity → structural GDP; GDP → unemployment recurrence; debt →
sovereign premium → fiscal stress/adjustment; climate amplitude → structural
drag; GFC → external shock / regime effects). Speculative statements (e.g.
"France will raise taxes because…") are forbidden unless represented in context.

Permanent scenario facts: P10=path 856, P50=path 524, P90=path 367 — real
selected simulation paths, not synthetic combinations or worst/base/best cases;
all three contain **zero GFC events**.

Counterintuitive AI guard: the P10 path (AI amplitude ≈1.497) is NOT worse
because of AI; other stochastic conditions (external environment, climate drag,
regime history) dominate. Debt is explicitly **not** an Index component; the
Index = GDPpc + median living + (reversed) unemployment, equal 1/3, fixed
2010–2019 normalization, base 100, 10 pts/SD, RAW, no clipping. P10/P50/P90 are
distribution percentiles, never "90% confidence interval" or "worst/best case".

## 6. Unsupported-question behavior

If the context does not support an answer, the model is instructed to state that
it is "not represented in the current FranceScope model or published outputs"
rather than answer from general knowledge. Out-of-scope examples (elections,
foreign invasions, house prices) are answered as not modeled. Only relevant
limitations are surfaced per question.

## 7. Environment setup (server-side only)

`frontend/.env.example` declares (no real values committed):
- `FRANCESCOPE_LLM_API_KEY` (required)
- `FRANCESCOPE_LLM_BASE_URL` (default `https://api.openai.com/v1`)
- `FRANCESCOPE_LLM_MODEL` (default `gpt-4o-mini`)

Copy to `.env.local`; never expose via `NEXT_PUBLIC_*`. The key is read only in
the server route and provider module.

## 8. Source-chip behavior

Each response returns a `sources` array of `{ label, artifact }` with friendly
labels (Historical V3 Index, Official MC1000 distributions, Coherent scenario
paths, FranceScope methodology). The `/ask` UI renders them as small chips under
the answer; only friendly labels are shown (no filesystem paths exposed).

## 9. MVP scope

- Single-turn Q&A; no conversation memory, accounts, or database.
- No RAG, embeddings, vector DB, authentication, or streaming infrastructure.
- Graceful fallback when unconfigured (page renders; submit shows the
  configuration message; app does not crash).
- Loading state, disabled submit, Enter/Ctrl+Enter submit, suggested-question
  chips.

## 10. Future extension points

- Swap providers by changing env vars; no code change.
- Add multi-turn grounding by re-sending the same deterministic context per turn.
- Extend the classifier or add per-topic prompt templates without altering the
  UI. A vector/RAG layer is **not** required and is not mandated as a next step.
