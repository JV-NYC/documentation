# Portfolio Production Log

This is a public-readable record of the portfolio being made, including the experiments, revisions, failures, decisions, and milestones that turn an idea into something that has to work on a page. Each entry is an abbreviated case study: a question, the constraints around it, the evidence, the direction now in play, and whatever remains unsettled. Production rarely supplies those pieces in a clean order, but the record should make the reasoning legible.

> **Historical record note:** Entries through 2026-08-19 were reconstructed from contemporaneous Portfolio project conversations when this log was established. Dates reflect the original work where they can be established. Later entries are recorded as the project develops.

## 2026-08-19

### Moving from design-system critique to page proof

**Item:** Portfolio proof set  
**Type:** Review, Milestone  
**Theme:** Design-system validation  
**Tools:** Claude, Framer  
**Status:** In progress

#### Question

Can the emerging design system support real portfolio pages, or does it only appear coherent while it remains an object of abstract review?

#### Context

I used Claude to pressure-test color, typography, spacing, layout, component consistency, unsupported decisions, and Framer compatibility through Critics A through D, a Step 15 adversarial review, and a Step 16 handoff that passed with reservations. That work surfaced real inconsistencies and tightened the system, but another review pass risks improving the appearance of the rules while revealing little about whether they can carry real content.

I considered continuing to refine the system before implementation, then reduced the first proof set to three representative pages instead:

- Landing, renamed from `Home`
- one project or case-study page
- Bio

The first case-study candidate is shifting away from Packs toward either the powerlifting data-visualization project or Toyota. The choice remains unresolved because the next useful evidence is not another abstract comparison. It is the act of placing real content into the three-page set.

#### Experiment and direction

Claude has been more useful as a critic of the system as a whole than as a generator of isolated visual ideas, so the next test is deliberately concrete: build the proof set in the Lab/Sandbox and see where the rules require exceptions. On August 19, implementation became the next source of evidence. The Lab/Sandbox now holds those pages while assumptions either survive contact with real content or fail there without destabilizing the production site.

#### Why this is enough

A small set of real pages can expose problems in both the system and the content without introducing so many page types that it becomes difficult to tell which one causes the problem. The immediate scope is therefore Landing, one case-study page, and Bio, which shifts the project away from extending the system in the abstract and toward learning whether actual pages can use it without constant exception-making.

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

#### Question

How much of the design system can move into Framer through a deterministic, repeatable workflow before that workflow becomes larger than the design problem itself?

#### Context and evidence

Framer compatibility is a hard requirement, and the original standard leans toward direct programmatic ingestion. Across August 18 and 19, however, the automation exercise began to acquire its own gravity. I tested ways to move tokens and related design-system artifacts into Framer, and the resulting acceptance criterion now includes reliable, low-friction ingestion through practical intermediate steps as well as direct writes. Plugins, generated artifacts, and small manual adjustments are acceptable when they make the process dependable.

The remaining comparison was concrete: ten minutes of manual radius adjustment against another twenty prompts intended to eliminate that adjustment. Once framed that way, perfect automation stopped being a requirement. I now accept a small amount of manual finishing when more automation costs more than the problem it removes.

#### Decision and rationale

The purpose of the workflow is to get the design system into Framer reliably, not to demonstrate that every property can arrive without human adjustment. Direct writes are therefore no longer the only acceptable path. A deterministic process may include plugins, generated artifacts, intermediate steps, and trivial manual finishing, provided the handoff remains dependable.

#### What I learned

Automation can become its own form of scope creep. The useful threshold remains a workflow reliable enough that the remaining work is trivial.

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

#### Question

Can AI-assisted work inspect and modify the actual local portfolio files, then preserve those changes through Git?

#### Context and outcome

The existing Portfolio project holds substantial design and ideation context but lacks the filesystem access needed to change the actual work. The local portfolio is a single HTML file, and conversational context cannot substitute for access to it. A conversation can describe a file accurately. That does not make it editable.

I established a separate project with local file access, confirmed read and write access to the relevant files, and connected the work to the Git repository. The HTML file is in place, the local development server does not need to remain running, and AI-assisted changes can operate directly on local files while participating in the Git workflow.

#### What I learned

Conversational context and filesystem access are different capabilities. Important context needs durable files that can travel between environments instead of relying on every AI session to share the same history.

### Creating durable records of the project

**Item:** Portfolio documentation  
**Type:** Setup  
**Theme:** Project memory  
**Status:** Complete

#### Question

How can the portfolio's thinking and production history survive beyond individual AI conversations?

#### Context and outcome

Important context is distributed across conversations and project memory, while different environments can have different access to both. The records also need to remain understandable if they eventually become public, so I created three Markdown files with distinct responsibilities:

- `portfolio-ideation-log.md` for evolving ideas, references, experiments, questions, and creative directions
- `portfolio-production-diary.md` for the actual making of the portfolio through abbreviated case studies
- `portfolio-change-log.md` for pushed updates after the site is live

I also created `portfolio-production-diary-instructions.md` to define the production record's structure and formatting, and `agents.md` to govern voice, writing, Git, and other operating instructions. The project now has a documentation structure that can persist across tools, sessions, and AI systems.

#### Why it matters

Memory is useful, but it should not be the only archive. Markdown files can act as the shared record that different tools read instead of asking each environment to reconstruct the project from scratch.

## 2026-08-18

### Selecting Framer as the production platform

**Item:** Portfolio platform  
**Type:** Decision  
**Theme:** Platform selection  
**Status:** Complete

#### Question

Which production platform can support the portfolio as both a CMS-driven site and a more interactive visual environment?

#### Context, alternatives, and decision

The platform needs a real CMS, SEO strong enough for a portfolio, reusable components, layered 2D animation, environmental interaction, and a practical production path that does not split the site across too many systems. I prefer to stay within one design ecosystem if the remaining tool can actually carry the project.

I compared the practical roles of Notion, Figma Sites, and Framer. Figma Sites is attractive because it keeps more work inside the Figma ecosystem, but further research indicates that Framer has stronger CMS and SEO capabilities for this project and better matches the interaction and animation needs emerging from the visual-world work. Framer is therefore the production platform and CMS, holding the site, CMS, components, animation, and interaction, while Figma remains useful for assets and discrete elements.

#### Rationale

Reducing the number of tools only helps when the remaining tool can carry the project. A single ecosystem looks simpler in theory, but Figma Sites imposes larger constraints elsewhere.

### Separating production from experimentation

**Item:** Framer workspace  
**Type:** Setup  
**Theme:** Experimentation workflow  
**Status:** Complete

#### Question

How can I test uncertain interactions, animations, components, CMS patterns, and layouts without turning every experiment into a production decision?

#### Context and approach

Aggressive experiments can destabilize the production portfolio, while protecting production too carefully can make it difficult to test ideas honestly. I separated the Framer workspace into:

- `Portfolio 2026` for production
- `Lab/Sandbox` for experiments
- Tutorial space for learning and reference

A working rule governs the separation:

> Sandbox proves it. Portfolio 2026 ships it.

The Sandbox is the proving ground for components, layouts, animation ideas, and CMS patterns before they move into production. That separation reduces pressure on experiments because a failed idea can still be useful without damaging the production site or quietly becoming a production commitment. Experimental evidence belongs in the Sandbox first; movement into `Portfolio 2026` marks a separate production choice.

### Building the CMS around artifacts

**Item:** Framer CMS and Artifact Card  
**Type:** Design, Build  
**Theme:** Content architecture  
**Status:** In progress

#### Question

Can one flexible content model support case studies, essays, research, prototypes, simulations, and other portfolio work, while one reusable card represents that work across filtered views?

#### Context and alternatives

The content types differ in presentation, but a separate collection for each type would duplicate structure and increase maintenance. The card also needs enough variation to express hierarchy without becoming several unrelated components.

The main alternative is to split site sections and content types into separate CMS collections with page-specific cards. I tested a single collection named `Artifacts` instead, where one record represents one work item:

Packs. Glaciers. Toyota. Montage. A paper. A simulation. A prototype.

The fields under test are:

- Title
- Status
- Slug
- Content
- Test Content
- Image
- Case Study / Essay toggle

Site sections can then become filtered views of the same collection rather than separate data models.

#### Evidence and direction

I built an `Artifact Card` with Primary and Featured variants, hover and pressed states, and variable bindings for title, summary, and image. The component now shows that CMS content can feed reusable visual patterns across views without requiring page-specific cards, so the single `Artifacts` collection is the working CMS model, with Index and Detail pages. The artifact, rather than the page section, is the useful content unit.

#### Rationale and current position

The content types are not structurally different enough to justify separate data models. Filtering one collection appears cleaner than multiplying collections around the site's sections, while card variants can carry the needed visual hierarchy. The model still needs to prove itself through production, so it remains a working direction rather than a finished architecture.
