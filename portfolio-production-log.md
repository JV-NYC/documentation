# Portfolio Production Log

This log is a chronological, public-readable record of how the portfolio is being made. Each entry is an abbreviated case study of meaningful production work: experiments, tests, revisions, failures, decisions, and milestones.

The basic sequence is:

**Question or opportunity → Context and constraints → Exploration and evidence → Decision, direction, or unresolved position → Rationale → Implications and learning**

> **Historical record note:** Entries through 2026-08-19 were reconstructed from contemporaneous Portfolio project conversations when this log was established. Dates reflect the original work where they can be established. Later entries are recorded as the project develops.

## 2026-08-19

### Moving from design-system critique to page proof

**Item:** Portfolio proof set  
**Type:** Review, Milestone  
**Theme:** Design-system validation  
**Tools:** Claude, Framer  
**Status:** In progress  

#### Question or opportunity

I needed to know whether the emerging design system could support real portfolio pages, not merely remain coherent under another round of abstract review.

#### Context

Across August 18 and 19, I used Claude to pressure-test color, typography, spacing, layout, component consistency, unsupported decisions, and Framer compatibility. The process included Critics A through D, a Step 15 adversarial review, and a Step 16 handoff that passed with reservations. The work surfaced useful inconsistencies and tightened the system, but further critique risked solving hypothetical problems instead of production problems.

#### Exploration and alternatives

I considered continuing to refine the system before implementation. Instead, I reduced the first proof set to three representative pages:

- Landing, renamed from `Home`
- one project or case-study page
- Bio

The first case-study candidate also shifted away from Packs toward either the powerlifting data-visualization project or Toyota. That choice remained unresolved.

#### Experiment or evidence

Claude was more useful as a critic of the whole system than as a generator of isolated visual ideas. The next test would be more concrete: place real content into the three-page proof set in the Lab/Sandbox and see where the rules required exceptions.

#### Direction

On August 19, implementation became the next source of evidence. The Lab/Sandbox would hold the proof set so design assumptions could survive contact with real content or fail without destabilizing the production site.

#### Rationale

A small set of real pages can expose problems in both the system and the content without introducing enough page types to obscure which one is responsible. Another review pass could make the rules look tidier while revealing little about whether they work.

#### Implications

The immediate production scope became Landing, one case-study page, and Bio. The project moved away from extending the design system in the abstract and toward testing whether real pages could use it without constant exception-making.

#### Open questions

- Should the first case study use the powerlifting data-visualization project or Toyota?
- Which design-system assumptions will fail when the proof set uses real content?

#### AI process note

**Role:** Design-system critique and adversarial review  

**Prompt sketch**

```text
Review the design system as a whole.

Look critically at:
- typography
- color
- spacing
- layout
- component consistency
- unsupported decisions
- Framer compatibility

Push on real weaknesses rather than expanding the system for its own sake.
```

### Finding the practical limit of Framer automation

**Item:** Framer token ingestion  
**Type:** Experiment  
**Theme:** Design-system implementation  
**Tools:** Framer, Claude  
**Status:** Complete  

#### Question or opportunity

I wanted to determine how much of the design system could move into Framer through a deterministic, repeatable workflow.

#### Context

Framer compatibility was a hard requirement. The original standard leaned toward direct programmatic ingestion, but the automation exercise was beginning to grow larger than the design problem.

#### Exploration and alternatives

Across August 18 and 19, I tested ways to move tokens and related design-system artifacts into Framer. The acceptance criterion gradually broadened from direct writes to reliable, low-friction ingestion through practical intermediate steps. Plugins, generated artifacts, and small manual adjustments became acceptable when they made the workflow dependable.

#### Experiment or evidence

The remaining work offered a useful comparison: ten minutes of manual radius adjustment against another twenty prompts intended to eliminate that manual step.

#### Decision

Perfect automation stopped being a requirement. I accepted a small amount of manual finishing when further automation cost more than the problem it removed.

#### Rationale

The purpose of the workflow is to get the design system into Framer reliably, not to prove that every property can be transferred without human adjustment.

#### Implications

Direct writes are no longer the only acceptable path. A deterministic process may include plugins, generated artifacts, intermediate steps, and trivial manual finishing.

#### What I learned

Automation can become its own form of scope creep. The useful threshold is a workflow reliable enough that the remaining work is trivial.

#### AI process note

**Role:** Implementation exploration and critique  

**Prompt sketch**

```text
Test how reliably the design system can move into Framer.

Prefer deterministic and repeatable ingestion.

Do not assume direct API or programmatic writes are required.

Identify the point where more automation costs more than a small amount of manual finishing.
```

### Establishing a local and Git-backed workflow

**Item:** Local development workflow  
**Type:** Setup  
**Theme:** Development infrastructure  
**Status:** Complete  

#### Question or opportunity

I needed AI-assisted work to inspect and modify the actual local portfolio files, then maintain those changes through Git.

#### Context

The existing Portfolio project contained substantial design and ideation context but lacked the needed filesystem access. The local portfolio was a single HTML file. Conversational context alone could not substitute for access to the files being changed.

#### What I did

I established a separate project with local file access, confirmed read and write access to the relevant files, and connected the work to the Git repository. Once the HTML file was confirmed in place, the local development server no longer needed to remain running.

#### Outcome

AI-assisted changes could now operate directly on local files and participate in the Git workflow.

#### What I learned

Conversational context and filesystem access are different capabilities. Important context needs durable files that can travel between environments instead of relying on every AI session to share the same history.

### Creating durable records of the project

**Item:** Portfolio documentation  
**Type:** Setup  
**Theme:** Project memory  
**Status:** Complete  

#### Question or opportunity

I needed to preserve the portfolio's thinking and production history beyond individual AI conversations.

#### Context

Important context was distributed across conversations and project memory, while different environments could have different access to both. The records also needed to remain understandable if they eventually became public.

#### What I did

I created three Markdown records and separated their responsibilities:

- `portfolio-ideation-log.md` for evolving ideas, references, experiments, questions, and creative directions
- `portfolio-production-diary.md` for the actual making of the portfolio through abbreviated case studies
- `portfolio-change-log.md` for pushed updates after the site is live

I also created `portfolio-production-diary-instructions.md` to define the production record's structure and formatting, and `agents.md` to govern voice, writing, Git, and other operating instructions.

#### Outcome

The project gained a documentation structure that could persist across tools, sessions, and AI systems.

#### Rationale

Memory is useful, but it should not be the only archive. Markdown files can act as the shared record that different tools read instead of asking each environment to reconstruct the project from scratch.

## 2026-08-18

### Selecting Framer as the production platform

**Item:** Portfolio platform  
**Type:** Decision  
**Theme:** Platform selection  
**Status:** Complete  

#### Question or opportunity

I needed a production platform that could support the portfolio as both a CMS-driven site and a more interactive visual environment.

#### Context and constraints

The platform needed a real CMS, strong enough SEO for a portfolio, reusable components, layered 2D animation, environmental interaction, and a practical production path that did not split the site across too many systems. I preferred to stay within one design ecosystem if the remaining tool could carry the project.

#### Exploration and alternatives

I compared the practical roles of Notion, Figma Sites, and Framer. Figma Sites was attractive because it kept more work inside the Figma ecosystem. Further research indicated that Framer had stronger CMS and SEO capabilities for this project and better matched the interaction and animation needs emerging from the visual-world work.

#### Decision

Framer became the production platform and CMS. It would own the site, CMS, components, animation, and interaction. Figma would remain useful selectively for designing assets and discrete elements.

#### Rationale

Reducing the number of tools helps only when the remaining tool can carry the project. A single ecosystem looked simpler in theory, but Figma Sites would have imposed larger constraints elsewhere.

#### Implications

Production would center on Framer, while Figma would support rather than contain the site.

### Separating production from experimentation

**Item:** Framer workspace  
**Type:** Setup  
**Theme:** Experimentation workflow  
**Status:** Complete  

#### Question or opportunity

I needed room to test uncertain interactions, animations, components, CMS patterns, and layouts without turning every experiment into a production decision.

#### Context and constraints

Aggressive experiments could destabilize the production portfolio. At the same time, protecting production too carefully could make it difficult to test ideas honestly.

#### What I did

I separated the Framer workspace into:

- `Portfolio 2026` for production
- `Lab/Sandbox` for experiments
- Tutorial space for learning and reference

A working rule emerged:

> Sandbox proves it. Portfolio 2026 ships it.

#### Outcome

The Sandbox became the proving ground for components, layouts, animation ideas, and CMS patterns before they moved into production.

#### Rationale

The separation reduces pressure on experiments. A failed idea can still be useful because it does not damage the production site or quietly become a production commitment.

#### Implications

Experimental evidence belongs in the Sandbox first. Movement into `Portfolio 2026` marks a separate production choice.

### Building the CMS around artifacts

**Item:** Framer CMS and Artifact Card  
**Type:** Design, Build  
**Theme:** Content architecture  
**Status:** In progress  

#### Question or opportunity

Could one flexible content model support case studies, essays, research, prototypes, simulations, and other portfolio work, while one reusable card represented that work across filtered views?

#### Context and constraints

The content types differ in presentation, but a separate collection for each type would duplicate structure and increase maintenance. The card also needed enough variation to express hierarchy without becoming several unrelated components.

#### Exploration and alternatives

The main alternative was to split site sections and content types into separate CMS collections with page-specific cards. I instead tested a single collection named `Artifacts`, where one record represents one work item. Examples included Packs, Glaciers, Toyota, Montage, a paper, a simulation, and a prototype.

Tested fields included:

- Title
- Status
- Slug
- Content
- Test Content
- Image
- Case Study / Essay toggle

Site sections could then become filtered views of the same collection rather than separate data models.

#### Experiment or evidence

I built an `Artifact Card` with Primary and Featured variants, hover and pressed states, and variable bindings for title, summary, and image. The component showed that CMS content could feed reusable visual patterns across views instead of requiring page-specific cards.

#### Direction

The single `Artifacts` collection became the working CMS model, with Index and Detail pages. The artifact, rather than the page section, became the useful content unit.

#### Rationale

The content types were not structurally different enough to justify separate data models. Filtering one collection appeared cleaner than multiplying collections around the site's sections, while card variants could carry the needed visual hierarchy.

#### Implications

Content remains unified while presentation can vary. The model still needs to prove itself through production, so it remains a working direction rather than a finished architecture.
