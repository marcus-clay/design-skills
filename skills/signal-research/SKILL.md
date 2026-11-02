---
name: signal-research
description: >
  Scans current signals across UI/UX, product design, design strategy, AI-assisted workflows, the design toolchain, B2B/B2G/SaaS design, AI regulation and process automation, then generates content angles calibrated to the user's own positioning. Use when the user asks for content ideas, wants to know what is trending or debated in design, product or AI, needs an editorial plan, or names a topic to write about (search first, then differentiate).
compatibility: "Requires web_search tool"
---

# Signal Research Skill

Research and content ideation system for designers, product people and consultants. It finds signal across the design, AI, product and regulation space and turns it into content angles calibrated to the user's positioning and credibility map.

## What this skill produces

A **Research Brief** structured as:
1. 3-5 **Trend Clusters** (each with signals, discourse summary, tension points)
2. 2-3 **Content Angles** per cluster (format, hook, stance)
3. An optional **7-day editorial skeleton** if the user asks for a posting plan

---

## Step 0: Load the positioning brief

Content angles only work when they fit the person who will publish them. Before any search:

1. Look for the user's positioning brief (see `references/positioning-brief.md` for the template). Check the project files, memory or any file the user points to.
2. If a brief exists, read it and use it for every angle.
3. If none exists, build it first with these 5 short questions, then write the answers into a copy of the template and save it where the user prefers:
   - Who are you, and what is your role or practice?
   - On which 3 to 5 topics can you speak from direct experience, and what is the evidence (projects, tools, results you can share)?
   - Who do you want to reach (roles, seniority, sectors, language)?
   - What posture and tone do you want (analytical, builder, teacher, contrarian)?
   - Which topics, formats or claims should never appear in your content?
4. Only then start scanning.

---

## Step 1: Clarify scope (if needed)

If the request is open-ended (no specific domain or time frame), run the **Full Scan** (all 9 domains, see `references/domains.md`).

If the user names a specific domain or topic, run a **Focused Scan** on that area only.

Start without asking for clarification. Make a judgment call and state it at the top of the brief.

---

## Step 2: Search protocol

### Full Scan (9 searches, one per domain cluster)

Run one search per domain. Use the queries in `references/domains.md` as starting points. Adapt queries with recency signals: append the current year. After each search, fetch 1-2 of the highest-signal results with `web_fetch` to extract substance.

**Signal sources to prioritize (in order):**
1. Substack and independent newsletters (UX Collective, Dive Club, Dense Discovery, Every, Lenny's Newsletter)
2. LinkedIn posts with high engagement from known practitioners
3. Industry publications: Nielsen Norman Group, Baymard, Smashing Magazine, A List Apart
4. Conference proceedings: Config, NN/g UX Conference, UX London and similar
5. GitHub, Vercel, Linear and Notion changelogs (for tool-layer signals)
6. Official regulator and institution sources for regulatory signals (European Commission, ENISA, national data protection authorities)
7. Academic preprints on HCI (ACM CHI) when surfaced

**Sources to deprioritize:**
- Generic "Top 10 UX trends" listicles from SEO farms
- Agency blog posts without a named author
- Content older than 6 months unless it is a foundational piece still driving discourse

### Focused Scan (2-4 searches)

Go deeper on fewer queries. Fetch at least 2 full articles. Extract direct quotes, named practitioners, and specific tool or method names: these become angle anchors.

---

## Step 3: Identify Trend Clusters

From search results, group findings into 3-5 clusters. Each cluster must have:
- A **tension or contradiction** at its core (a debate, a shift, a disappearing assumption, beyond a plain topic)
- At least 2 distinct practitioner positions (beyond consensus)
- A clear signal of why it matters *now* (timing hook)

Name clusters with a short phrase that captures the tension, in place of a topic label.

**Examples of good cluster names:**
- "Figma is a drawing tool in an agentic world"
- "The PM-designer role boundary is dissolving"
- "Accessibility compliance is becoming a procurement condition in the public sector"
- "AI prompting is the new wireframing"
- "AI regulation turns UX patterns into legal liabilities"

**Examples of bad cluster names:**
- "AI in UX"
- "Design trends this year"
- "New tools"

---

## Step 4: Generate Content Angles

For each cluster, produce 2-3 content angles. Each angle is defined by:

| Field | Description |
|---|---|
| **Format** | One of: Opinion post, Case breakdown, Myth debunking, Observation + question, Tool review, Process documentation, Contrarian take, Data point + implication, Framework reveal, Before/after workflow |
| **Hook** | The opening move. Concrete and specific, with a first line that avoids stock openers like "Have you ever wondered..." |
| **Stance** | The user's position. Opinionated, and more than a summary of "both sides". |
| **Audience trigger** | Who this will resonate with (Head of Design, CPO, B2B SaaS PM, public sector design lead, etc.) |
| **Tension used** | Which cluster tension this angle exploits |
| **Differentiation check** | What makes this angle different from what is already in the discourse |
| **Angle risk** | What could make this post fall flat or feel obvious |

### Positioning constraints (always apply)

Apply the user's positioning brief to every angle:
- Match the credibility map: write only on topics where the user has direct experience or evidence.
- Match the target audience and the stated tone.
- Respect the "angles to avoid" list without exception.
- Favor the formats and recurring themes the brief marks as high fit.

### Angle quality test (all 4 must pass)

Before outputting an angle, test it against:
1. Would the target reader named in the brief stop scrolling for this?
2. Does it require the user's specific experience to write credibly?
3. Does it have a position, beyond an observation?
4. Is there something in the current discourse this angle contradicts, sharpens or adds to, as opposed to restating what everyone already knows?

If any answer is no, revise or discard.

---

## Step 5: Output format

```
# Research Brief | [Date] | [Scan type: Full / Focused: topic]

## Scan summary
[2-3 sentences on what the search found overall. Flag any surprising absences or dominant narratives.]

---

## Cluster 1: [Tension name]

**What's moving:** [3-5 sentences. Concrete, named. Cite sources inline.]
**Key practitioners in this discourse:** [Names, companies or publications if found]
**Why now:** [Timing signal: conference, product launch, policy change, etc.]

### Content Angles

**Angle A | [Format]**
- Hook: [Opening line or move]
- Stance: [The user's position]
- Audience trigger: [Who this lands with]
- Differentiation: [What makes this non-obvious]
- Risk: [What could make it miss]

**Angle B | [Format]**
...

---

## Cluster 2: ...

---

## 7-day editorial skeleton (optional, include only if requested)

| Day | Cluster | Format | Hook summary |
|---|---|---|---|
| Mon | | | |
...
```

---

## Edge cases

**If search results are thin on a domain:** Note it explicitly and leave out generic filler. Suggest a better search strategy or a primary source to check manually.

**If two clusters are too similar:** Merge them. Fewer sharper clusters beat more vague ones.

**If the user names a topic they want to write about:** Reverse the process. Search for the current discourse on that topic first, then generate angles that differentiate the user's take from what is already out there.

**If the user asks for a post draft:** Confirm the angle first, then draft in the voice described in the positioning brief.

**If the user writes in another language:** Deliver the brief in that language. Cluster names and angle fields follow the user's language. Source titles can remain in their original language.

---

## Reference files

- `references/domains.md`: the 9 domain clusters with seed queries and signal sources
- `references/positioning-brief.md`: template for the user's positioning, credibility map and angle constraints
