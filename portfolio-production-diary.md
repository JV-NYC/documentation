# Portfolio Production Diary

This diary is a chronological, public-readable record of how the portfolio is being made. Each entry is an abbreviated case study of meaningful production work: experiments, tests, revisions, failures, decisions, and milestones.

The basic sequence is:

**Problem / Goal → Constraint → What I did → Outcome → What I learned**

> **Historical record note:** Entries through 2026-08-19 were reconstructed from contemporaneous Portfolio project conversations when this diary was established. Dates reflect the original work where they can be established. Later entries are recorded as the project develops.

## Historical entries

### 2026-08-18 | Selecting Framer as the production platform

**Item:** Portfolio platform  
**Type:** Decision  

#### Problem / Goal

I needed a production platform that could support the portfolio as both a CMS-driven site and a more interactive visual environment. The options included Framer, Notion, and Figma Sites.

#### Constraint

The platform needed to support:

- a real CMS
- strong enough SEO for a portfolio site
- reusable components
- layered 2D animation
- environmental interaction
- practical production without splitting the site across too many systems

I also preferred to stay within one design ecosystem if possible.

#### What I did

I compared the practical roles of Notion, Figma Sites, and Framer. Figma Sites was attractive because it could keep more of the work inside the Figma ecosystem. Further research showed that Framer had stronger CMS and SEO capabilities for this project. It also better matched the interaction and animation needs emerging from the visual-world work.

#### Outcome

Framer became the production platform and CMS. Figma remains useful selectively for designing assets and discrete elements.

Framer owns:

- the site
- CMS
- components
- animation
- interaction

#### What I learned

Reducing the number of tools is useful only when the remaining tool can carry the project. Keeping everything inside one ecosystem would have been simpler in theory, but it would have imposed larger constraints elsewhere.

### 2026-08-18 | Separating production from experimentation

**Item:** Framer workspace  
**Type:** Setup  

#### Problem / Goal

I needed a way to experiment aggressively without destabilizing the production portfolio.

#### Constraint

The project needs room for uncertain interaction, animation, component, and layout experiments. Those experiments should not automatically become production decisions.

#### What I did

I separated the Framer work into:

- `Portfolio 2026` for production
- `Lab/Sandbox` for experiments
- Tutorial space for learning and reference

A simple working rule emerged:

> Sandbox proves it. Portfolio 2026 ships it.

#### Outcome

The Sandbox became the proving ground for components, layouts, animation ideas, and CMS patterns before they move into production.

#### What I learned

The separation reduces pressure on experiments. An idea can be useful even when it fails, because failure in the Sandbox does not damage the production site.

### 2026-08-18 | Simplifying the CMS around Artifacts

**Item:** Framer CMS  
**Type:** Design  

#### Problem / Goal

I wanted a CMS structure that could support case studies, essays, research, prototypes, simulations, and other portfolio work without creating unnecessary collections.

#### Constraint

The portfolio contains different kinds of work, but splitting every content type into its own CMS collection would create duplicated structure and more maintenance.

#### What I did

I tested a single collection named `Artifacts`. One artifact represents one work item, such as:

- Packs
- Glaciers
- Toyota
- Montage
- a paper
- a simulation
- a prototype

Tested fields included:

- Title
- Status
- Slug
- Content
- Test Content
- Image
- Case Study / Essay toggle

Sections of the site would become filtered views rather than separate collections.

#### Outcome

The single `Artifacts` collection became the working CMS model. CMS pages included Index and Detail.

#### What I learned

The content types are different in presentation, but not different enough structurally to justify separate data models. Filtering one flexible collection appears cleaner than multiplying collections around site sections.

### 2026-08-18 | Proving the Artifact Card pattern

**Item:** Artifact Card  
**Type:** Build  

#### Problem / Goal

I wanted to know whether one reusable Framer card component could represent work across multiple filtered CMS views.

#### Constraint

The component needed enough variation to support hierarchy without becoming several unrelated card components.

#### What I did

I built an `Artifact Card` component with:

- Primary variant
- Featured variant
- hover state
- pressed state
- variable bindings for title
- variable bindings for summary
- variable bindings for image

#### Outcome

The component became a working proof that CMS content could feed reusable visual patterns rather than requiring page-specific cards.

#### What I learned

The useful unit is not the page section. It is the artifact. That supports the broader CMS decision to keep content unified and let presentation vary around it.

### 2026-08-18 | Cutting the first build down to three pages

**Item:** Initial page set  
**Type:** Decision  

#### Problem / Goal

I needed to move from design-system discussion into actual page production without trying to build the entire portfolio at once.

#### Constraint

Too many page types would make it difficult to distinguish problems with the design system from problems with individual content.

#### What I did

I reduced the initial proof set to:

- Landing
- Case Study
- Bio

I renamed the planned homepage from `Home` to `Landing`. The first case study candidate shifted away from Packs toward either the powerlifting data-visualization project or Toyota.

#### Outcome

The project now had a small representative page set capable of testing the major layout and content patterns.

#### What I learned

A small set of real pages will expose more useful problems than another round of abstract system refinement.

### 2026-08-18 | Using Claude as a design-system critic

**Item:** Design system  
**Type:** Review  
**Tools:** Claude  

#### Problem / Goal

I wanted to pressure-test the emerging portfolio design system across color, typography, spacing, layout, and component consistency.

#### Constraint

The AI work needed to produce artifacts that were actually usable in Framer. The goal was not endless theoretical refinement.

#### What I did

Across August 18 and 19, I ran a multi-step design-system process with Claude. The work included:

- Critics A through D
- Step 15 adversarial review
- Step 16 handoff

The Step 16 handoff passed with reservations. I used Claude less as a generator of isolated visual ideas and more as a critical reviewer of the system as a whole.

#### Outcome

The process surfaced useful inconsistencies and helped tighten the system. It also clarified the limit of how much more abstract design-system work was useful before implementation needed to take over.

#### What I learned

Claude was most useful when asked to criticize the system rather than simply extend it. At some point, another review pass becomes less valuable than putting the system into Framer and seeing what breaks.

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

### 2026-08-18 | Finding the practical limit of Framer automation

**Item:** Framer token ingestion  
**Type:** Experiment  
**Tools:** Framer, Claude  

#### Problem / Goal

I wanted to determine how much of the design system could be transferred into Framer through a deterministic, repeatable workflow.

#### Constraint

Framer compatibility remained a hard requirement. The original standard leaned toward direct programmatic ingestion, but that standard risked making the automation exercise larger than the design problem.

#### What I did

Across August 18 and 19, I tested ways to move tokens and related design-system artifacts into Framer. The acceptance criterion gradually broadened from direct writes to deterministic, low-friction ingestion using practical intermediate steps where necessary. Plugins, generated artifacts, and small manual adjustments became acceptable if the workflow remained reliable.

#### Outcome

Perfect automation stopped being a requirement. I accepted a small amount of manual finishing work as preferable to repeatedly extending the automation pipeline.

The practical threshold became clear: if ten minutes of manual radius adjustment solves the remaining problem, another twenty prompts are probably not the better use of time.

#### What I learned

Automation can become its own form of scope creep. The goal is not to prove that every design-system property can be automated. The goal is to get the system into Framer reliably enough that the remaining work is trivial.

#### AI process note

**Role:** Implementation exploration and critique  

**Prompt sketch**

```text
Test how reliably the design system can move into Framer.

Prefer deterministic and repeatable ingestion.

Do not assume direct API or programmatic writes are required.

Identify the point where more automation costs more than a small amount of manual finishing.
```

### 2026-08-19 | Moving from system design to proof

**Item:** Portfolio proof set  
**Type:** Milestone  

#### Problem / Goal

I needed to stop extending the design system in the abstract and test it against real portfolio pages.

#### Constraint

The system had already received substantial critique and refinement. Continuing to add rules without implementation risked solving hypothetical problems.

#### What I did

I committed to using the Lab/Sandbox to build a small proof set:

- Landing
- one project / case-study page
- Bio

The emphasis shifted toward putting real content into the system and observing the result.

#### Outcome

Implementation became the next source of evidence. The Sandbox became the place where design assumptions would either survive contact with real content or fail.

#### What I learned

A design system is not proven because its rules are internally coherent. It is proven when real pages can use it without constant exception-making.

### 2026-08-19 | Establishing a local and Git-backed workflow

**Item:** Local development workflow  
**Type:** Setup  

#### Problem / Goal

I needed AI-assisted work to inspect and modify actual local portfolio files and maintain those changes through Git.

#### Constraint

The existing Portfolio project contained substantial design and ideation context but did not have the required local filesystem access. The local version of the portfolio was currently a single HTML file.

#### What I did

I established a separate project with local file access. I confirmed read and write access to the relevant project files and connected the workflow to the Git repository. The local server used during development could be stopped once the HTML file was confirmed in place.

#### Outcome

There is now a working environment where AI-assisted changes can operate directly on local files and participate in the Git workflow.

#### What I learned

Conversational context and filesystem access are different capabilities. The project needs durable files that can carry important context between environments rather than assuming every AI session shares the same history.

### 2026-08-19 | Creating durable records of the project

**Item:** Portfolio documentation  
**Type:** Setup  

#### Problem / Goal

I needed to preserve the project's thinking and production history beyond individual AI conversations.

#### Constraint

Important context was spread across conversations and project memory. Different environments may have different access to that context. The records also need to remain useful if they are eventually exposed publicly.

#### What I did

I created three Markdown records:

- `portfolio-ideation-log.md`
- `portfolio-production-diary.md`
- `portfolio-change-log.md`

I separated their responsibilities. `portfolio-ideation-log.md` records evolving ideas, references, experiments, questions, and creative directions. `portfolio-production-diary.md` records the actual making of the portfolio using abbreviated case-study entries. `portfolio-change-log.md` is reserved for pushed updates after the site is live.

I also created:

- `portfolio-production-diary-instructions.md`
- `agents.md`

The instructions file defines diary structure and formatting. `agents.md` governs voice, writing, Git, and other operating instructions for work in this project.

#### Outcome

The project now has a durable documentation structure that can survive across tools, sessions, and AI systems.

#### What I learned

Memory is useful, but it should not be the only archive. The Markdown files can become the shared record that different tools read rather than asking each environment to reconstruct the project from scratch.
