Sponte AI - Business Plan
0) One‑liner & Promise
Sponte — “Set it up once. Local SEO forever.”
 A multi‑agent system that runs local SEO (GBP, NAP, on‑site, posts, social) on autopilot with user‑selectable autonomy: Draft‑only → Approve‑to‑publish → Full autopilot.

1) Onboarding — the exact inputs you need (10‑minute flow)
Goal: everything the agents need to run without asking again.
A. Business Profile
Legal/brand name


Primary domain (+ CMS type if known)


Primary phone (tracking number optional)


Physical address or service area (zip/city list)


Primary category + 3–5 services (free‑text OK)


Weekly hours + holiday hours


Coverage radius (mi/km)


Competitors (up to 5 URLs or GBP names) (optional but useful)
B. Connections (OAuth / API keys)
Google Business Profile (Business Profile + Performance scopes)


Google Search Console (site verified)


Google Analytics 4 (read)


CMS: WordPress (App Password or OAuth), Webflow, Shopify, or “manual publish”


Social (optional for MVP v1.1): Meta (FB/IG), TikTok Business, LinkedIn Pages


SERP provider: DataForSEO (API key) (you already prefer this)


C. Content & brand
Tone presets (professional / friendly / witty / luxury / clinical)


Forbidden claims/words (compliance)


Visuals source (brand folder URL or upload)


Posting cadence preference:


Blog: off / monthly / 2× / weekly


GBP Posts: off / weekly / 2× / 3×


Social: off / 3× / 5× / 7× per week (per network)


D. Autonomy & guardrails
Global autonomy: Draft-only | Approve-to-publish | Full autopilot


Per‑surface overrides (GBP, Blog, Social)


“No publish” blackout hours (optional)


Monthly content budget cap (e.g., words/images/render credits)


E. Goals & reporting
Primary goal: calls | form fills | bookings | direction requests


UTM scheme (campaign/source/medium templates)


Report frequency: weekly summary + monthly deep‑dive


Email(s) to receive reports



2) Agents — who they are & what they do (MVP → V1 → V2)
Multi‑agent with job titles. One Orchestrator assigns, sequences, and checks.
0. Orchestrator (always on)
Reads settings & autonomy level


Pulls fresh data, assembles weekly plan


Assigns tasks to domain agents, enforces guardrails, creates report


1. GBP Agent (MVP – Must Have)
Syncs hours, NAP, description, categories (suggests safe secondary categories)


Writes & schedules GBP posts (offers, updates, events) with UTM links


Monitors Insights/Performance (queries, calls, dir requests) → feeds Reporting Agent


Notes: posting via API varies by account—fallbacks: manual push queue or partner integrations.


2. NAP Agent (MVP – Must Have)
Checks site footer, Contact page, schema.org LocalBusiness, GBP, and top citations


Flags inconsistencies; if autopilot, updates site + GBP (citations: propose tickets/links)


Exports a “fix list” for platforms that don’t allow programmatic updates


3. Keyword & Category Agent (MVP – Must Have)
Uses DataForSEO/Ahrefs/SEMrush API → seed → cluster → target list per service+city


Recommends GBP categories (safe adds/removals) and blog/topic ideas


Keeps a rolling opportunities queue


4. Reporting Agent (MVP – Must Have)
Compiles weekly digest + monthly narrative: movement in local pack, calls, top queries


Explains work done, upcoming items, and wins/gaps in plain English


5. On‑Page SEO Agent (V1)
Generates meta titles/descriptions, H1/H2 suggestions, internal link targets


Drafts changes via CMS API; respect no‑index/canonical; ships on autopilot if allowed


6. Blog Content Agent (V1)
Creates localized posts per service area (“{Service} in {City}”) with FAQs and schema block


Drafts in CMS, requests approval or publishes based on autonomy


Interlinks service pages ↔ blog


7. Social Agent (V1.1 – your request)
Turns blog/GBP updates into FB/IG/LinkedIn posts; supports TikTok captions/outlines


Schedules via Meta Graph / LinkedIn / TikTok Business APIs (where allowed)


Optional: pulls 1–2 “raw” videos from user and produces captions & hooks


8. Technical SEO Agent (V2)
Lightweight crawl (site map + BFS to depth N), 404/500, basic Core Web Vitals pull, schema checks


Files actionable tickets (or auto‑fix simple items on CMS)


9. Reputation Agent (V2)
Monitors new Google reviews; drafts tone‑matched replies; auto‑responds if enabled


Surfaces negative trends


(Ads, Email, Branding, Ops = later or separate product lines.)

3) System architecture (fast to build, easy to extend)
Stack suggestion (ship fast + stable):
Backend: Python FastAPI or Node NestJS


Queue/Scheduler: BullMQ (Redis) or Temporal (durable workflows)


DB: Postgres (+ pgvector if you add embeddings)


Object storage: S3-compatible (images, exports)


Auth: Clerk/Auth0/Supabase Auth


Frontend: Next.js (app router)


Vector store (optional V1+): pgvector or Pinecone for RAG over site content


Logging/Obs: OpenTelemetry + Logtail/Datadog; Sentry for exceptions


Service diagram (conceptual):
API (FastAPI/Nest)  <->  Redis Queue   <->  Worker(s): [GBP Agent, NAP Agent, Keyword Agent, ...]
        |                       |                  |
   Postgres --------------------+------------------+
        |
   Frontend (Next.js)  -->  Orchestrator plan view, approvals, reports

Core worker contract
// TypeScript types, language-agnostic idea
type Autonomy = 'DRAFT_ONLY' | 'APPROVE_TO_PUBLISH' | 'FULL_AUTOPILOT';

interface AgentTask {
  id: string;
  agent: 'GBP'|'NAP'|'KEYWORD'|'REPORT'|'ONPAGE'|'BLOG'|'SOCIAL';
  businessId: string;
  payload: Record<string, any>;
  autonomy: Autonomy;
}

interface AgentResult {
  taskId: string;
  status: 'DRAFTED'|'PUBLISHED'|'DECLINED'|'ERROR';
  artifacts?: { type: 'POST'|'META'|'DOC'|'IMAGE'|'LINK'; url?: string; body?: string };
  notes?: string;
}


4) Data model (minimum tables)
businesses: id, owner_user_id, name, domain, phone, address, geo, primary_category


connections: business_id, provider (GBP/GSC/GA4/CMS/META/LINKEDIN/TIKTOK/DFS), auth_blob, scopes


preferences: business_id, autonomy_global, per_surface_overrides JSON, cadence JSON


keywords: business_id, term, cluster, intent, priority, location


plans: business_id, week/month, items JSON (planned tasks)


tasks: id, business_id, agent, payload JSON, status, scheduled_at, executed_at


content_items: id, type (blog/gbp_post/social), status (draft/published), cms_id/url, body, meta JSON


reports: business_id, period, metrics JSON, narrative TEXT, url_pdf


events (audit log): business_id, actor (agent/user), action, details JSON, ts



5) Integrations to wire first (endpoints you’ll call)
Google Business Profile
OAuth scopes for Locations/Performance


Read/write: locations (hours, description, links), (posts if your account is allowed; otherwise store as “to publish”)


Reviews read for future Reputation Agent


Google Search Console
searchanalytics.query → queries, clicks, impressions by page


sitemaps.list (basic health)


GA4
Reports API for conversions / events tied to UTM’d links


CMS
WordPress: /wp-json/wp/v2/posts, media upload, Yoast/RankMath fields if present


Webflow/Shopify: posts/collections create/update


Fallback: export HTML/markdown for manual publish


Social
Meta Graph (Pages + IG), LinkedIn Pages, TikTok Business


Post scheduling endpoints; media upload; page/org IDs storage


SERP
DataForSEO: keywords suggestions, rank tracking (Local Pack & organic), “near me” patterns



6) Workflows (what runs when)
Weekly (cron / Temporal workflow)
Pull fresh GSC/GBP/DFSEO data


Keyword & Category Agent: refresh opportunities


GBP Agent: next 1–3 GBP posts (offers/updates)


On‑Page Agent: 3–5 title/meta fixes (draft)


Blog Agent (if enabled): draft next post


Social Agent: schedule 3–5 repurposed posts


Reporting Agent: weekly digest email


Monthly
Deeper report (movement per keyword cluster, calls, dir requests, top pages)


NAP re‑audit + Category review


Backlog grooming for next month


Safety rails
Max X publishes per week per surface


Blacklist phrases / claims


Kill‑switch per surface + global



7) MVP scope (what to ship first)
Must‑have for Day‑1
Auth + multi‑tenant businesses


Onboarding flow (inputs above)


Connections: GBP (OAuth), GSC, GA4, CMS (WordPress is enough), DataForSEO


Orchestrator + Redis queue


GBP Agent, NAP Agent, Keyword & Category Agent, Reporting Agent


Approvals UI (Draft → Approve/Reject → Publish)


Weekly cron + email summary


V1 (fast follow)
On‑Page SEO Agent (titles/meta/internal links drafts)


Blog Content Agent (1 post/mo default, drafts)


Basic Social Agent (repurpose blog/GBP → FB/IG/LinkedIn)


V2
Technical SEO Agent


Reputation Agent (review reply drafts)


Deeper multi‑location controls



8) 30 / 60 / 90 build plan
Days 1–30 (MVP running for first beta user)
Project scaffold (API + Next.js + Postgres + Redis)


Auth, business creation, connections (GBP/GSC/GA4/WP/DFSEO)


Task queue + Orchestrator skeleton


Implement GBP Agent + NAP Agent + Keyword Agent + Reporting Agent


Approvals UI + weekly digest email


Launch to 3–5 pilot users


Days 31–60 (V1)
On‑Page SEO Agent + CMS draft pipeline


Blog Agent (templates + outlines → draft + internal links)


Social Agent (FB/IG/LinkedIn) basic scheduling


Monthly report PDF export


Harden error handling, retries, idempotency


Days 61–90 (V2 prep)
Technical SEO Agent (crawl lite)


Reputation Agent (reply drafts)


Multi‑location dashboard


Usage metering + billing hooks (Stripe)



9) Pricing (50% of agency cost, simple & scalable)
Starter (1 location) – $149/mo (founding promo $99)
Autonomy: Draft or Approve-to-publish


GBP Agent, NAP Agent, Keyword Agent, Reporting


1 GBP post/week


1 on‑page fix/week


Pro (up to 3 locations) – $299/mo
Everything in Starter


Blog Agent: 1 post/mo/location


Social Agent: 3 posts/week (FB/IG/LinkedIn)


On‑Page batch fixes (up to 10/mo)


Agency (10 locations) – $799/mo + $40/add’l location
Multi‑location view, white‑label reports


Custom cadences & bulk approvals


Slack/Webhooks


Setup: $0–$299 (waive during beta for faster adoption).
 Add‑ons: Extra blog posts, review reply autopilot, TikTok scheduling.
(These hit your “~50% of agency” promise and let you land + expand.)

10) GTM: cold email / ads / phone
Cold email (local owners)
 Subject: Your Google ranking, done for you (no agency)
 Body (short):
Hey {{first}},

Saw {{business}} in {{city}}. Quick Q: if your Google Business Profile,
posts, and local SEO ran themselves—would that help?

Sponte is an AI agent that keeps your GBP updated, fixes NAP drift,
and posts weekly—no meetings, no retainers.

We set it up once (10 minutes). You pick: draft-only, approve-to-publish,
or full autopilot.

Want me to run a free audit and send a 1‑page plan?

— Jakob

Paid ad angles
“Set SEO. Forget SEO.”


“10‑minute setup → local SEO forever.”


“Autopilot GBP posts + NAP fixes. No agency.”


Cold call opener (20 seconds)
“Calling about your Google listing—if we could keep it updated and post for you automatically so you rank for {service} in {city}, is that worth a quick audit? It’s software, not an agency—10‑minute setup, then hands‑off.”

11) Product copy & UX notes (based on your mock)
The hero is strong. Consider:
Add 3 check‑icons under subhead: GBP ✓ / NAP ✓ / Posts ✓


Replace “10K+ Businesses Optimized” with credible early‑access language until you have it


Above the fold: a small toggle UI (“Draft‑only / Approve / Autopilot”) to reinforce control


“Start Your Agent” form: collect at least name, email, business name, site URL, city/zip, phone; defer everything else until OAuth



12) Risks & mitigations
GBP write limits / posting availability varies → gracefully fall back to: create draft, request approval, or push via partner integrations; never hard‑fail.


Content quality / hallucinations → use site crawl + FAQs as context, enforce length/tone, rule‑based checkers (no medical/legal claims).


Citations → programmatic updates are limited; deliver monitoring + link-out “fix” tasks and one-click verify flow.


Multi‑location complexity → always attach tasks to location_id.



13) What to code first (issue checklist)
FastAPI/NestJS scaffold + Postgres + Redis


Auth + Business create


OAuth: GBP, GSC, GA4; API key input: DataForSEO; CMS: WordPress creds


Tables (see §4) + migrations


Queue + Orchestrator


GBP Agent: read/write hours/desc/links; draft post object


NAP Agent: extract site NAP (footer, /contact, schema), compare with GBP, propose fix


Keyword Agent: seed → cluster → opportunity list


Reporting Agent: weekly email (GSC + GBP metrics)


Approvals UI (table of drafts → approve/publish)


Weekly cron + error handling



14) Prompting & templates (copy/paste starters)
GBP Post (Offer)
Goal: local conversions. Tone: {brand_tone}. Location: {city}.
Include: concise hook (<=12 words), 1-line benefit, CTA + UTM link.
Avoid: medical/financial claims, discounts without terms.

Input: service, city, offer details (optional).
Output: title (<=58 chars), body (80–150 words), alt text, 3 hashtags.

Blog Outline → Draft
Topic: {service} in {city}
Sources: {service_page_url}, GBP Q&A, top SERP H2s (paraphrase only)
Sections: Intro, What it includes, Costs/estimates, How to choose a provider,
FAQ(3–5 local), CTA with phone + map link.
Schema: Article + LocalBusiness FAQ snippet.

Title/Meta Fix
Given page content and target keyword cluster, produce:
- Title (<=58 chars, brand at end)
- Meta description (<=150 chars, benefit + city)
- H1/H2 suggestion, 2 internal link targets with anchor variants.


15) Your next actions in Cursor today
Scaffold API + DB + Redis


Build OAuth for GBP/GSC/GA4


Implement POST /businesses/:id/plan/weekly → generates tasks from agents


Build Approvals UI + publish handlers for GBP & CMS


Send first weekly email report to yourself from a demo business



