# Claude DB — AI Brain Vault

## Project Goal
Convert exported Claude conversation history into a fully-tagged, interlinked
Obsidian vault with entity pages for people, projects, and topics. All conversations
are already exported from Claude (conversations.json) and partially processed.

## Current State (as of 7 April 2026)
- [x] Claude export placed in: data-2026-04-05-07-51-26-batch-0000/conversations.json
- [x] build_vault.py ran successfully — converted 99 conversations to markdown
- [x] conv_index.json created (index of all 99 conversations with slugs, dates, categories)
- [x] Home.md updated with vault stats, folder navigation, Topics nav, and category table
- [x] People/ folder: 1 entity page exists
- [x] Projects/ folder: 6 entity pages exist
- [x] Topics/ folder: 9 entity pages created
- [ ] Tagging pass: 75/99 conversations have been tagged (batch 3 complete; 24 remain)
- [ ] People tagging: people: [] is empty on all conversations
- [x] Wikilinks: added to 91/99 conversations (8 skipped — empty or no relevant links)
- [x] Topics entity pages: 9 pages created (see Topics/)

## Directory Structure
```
Claude DB/
├── CLAUDE.md                          ← you are here
├── build_vault.py                     ← original conversion script (do not re-run)
├── conv_index.json                    ← index of all 99 conversations
├── Home.md                            ← vault home page
├── Welcome.md
├── Conversations/                     ← 99 .md files, all need tagging + wikilinks
├── People/                            ← 1 entity page (needs more)
├── Projects/                          ← 6 entity pages (needs more)
├── Topics/                            ← empty, needs populating
└── data-2026-04-05-07-51-26-batch-0000/
    ├── conversations.json             ← raw Claude export (32MB, source of truth)
    ├── memories.json
    ├── projects.json
    └── users.json
```

## Existing Frontmatter Format (already on all 99 files)
```yaml
---
title: "conversation title"
date: YYYY-MM-DD
updated: YYYY-MM-DD
uuid: <uuid>
category: "Category Name"
tags: []
people: []
places: []
projects: []
technologies: []
msg_count: N
---
```

## Known Categories (from conv_index.json)
- Protein Biology & Antibody Discovery
- DevOps & Infrastructure
- Data & Analytics
- (others present — read conv_index.json for full list)

## Rules — MUST Follow Every Session
1. NEVER re-run build_vault.py — conversations are already converted
2. ALWAYS check if a file already has `tagged: true` in frontmatter before processing — skip if so
3. Process in batches of 25 files maximum per session
4. After completing a batch, update the Progress Log section at the bottom of this file
5. Use maximum 2 sub-agents at a time to stay within token limits
6. After finishing any task, update the Current State checkboxes above

## Tagging Guidelines
When filling in frontmatter fields for each conversation file:
- tags: [2-5 lowercase descriptive tags e.g. "antibody-design", "gcp", "python"]
- people: [named people mentioned e.g. "Harjas", "Novartis contact"]
- places: [locations if relevant e.g. "Melbourne", "GCP"]
- projects: [project names e.g. "ActiMo Labs", "ActiMap", "TPG Telecom"]
- technologies: [tools/frameworks e.g. "Boltz-2", "IgFold", "Genesys Cloud", "Dialogflow CX"]

After filling all fields, append this line to the frontmatter so it is skipped next session:
tagged: true

## Wikilink Guidelines
At the bottom of each conversation file, add a Related section:
```
## Related
- [[PersonName]]
- [[ProjectName]]
- [[TopicName]]
```
Only link to files that actually exist in People/, Projects/, or Topics/.

## Entity Page Format (for People/, Projects/, Topics/)
```markdown
---
type: person|project|topic
name: "Name"
---
# Name

## Overview
Brief description.

## Related Conversations
- [[conversation-slug]]
```

## Tasks Queue (complete in this order, one task per session)
1. **Tagging Pass** — Fill tags, people, projects, technologies on all 99 conversations (25 per session)
2. **Topics Entity Pages** — Create topic pages in Topics/ based on recurring themes found during tagging
3. **Wikilink Pass** — Add Related sections to each conversation linking to entity pages
4. **Home.md Update** — Update Home.md with vault stats and navigation links

## Progress Log
| Date       | Task                | Files Processed | Notes                                              |
|------------|---------------------|-----------------|----------------------------------------------------|
| 2026-04-05 | Initial conversion  | 99              | build_vault.py ran, frontmatter created, tags empty |
| 2026-04-06 | Tagging pass batch 1 | 25             | Files 1–25 from conv_index.json tagged; 2 empty conversations skipped (Untitled-Conversation, Untitled-Conversation-2) |
| 2026-04-06 | Tagging pass batch 2 | 25             | Files 26–50 tagged; 2 empty conversations (Untitled-Conversation-3, Untitled-Conversation-4) |
| 2026-04-06 | Tagging pass batch 3 | 25             | Files 51–75 tagged; 1 empty conversation (Untitled-Conversation-5) |
| 2026-04-07 | Topics entity pages  | 9 pages        | Created 9 topic pages in Topics/ based on recurring tag analysis: Epitope-Mapping, Molecular-Docking, Antibody-Design, Binding-Affinity, Voicebot-and-Conversational-AI, GCP-Cloud-Infrastructure, Structure-Prediction, Prochestra-Multi-Agent-System, Startup-Strategy, Career-and-Resumes |
| 2026-04-07 | Wikilink pass        | 91/99          | Added ## Related sections to 91 conversations linking to Topics/ and Projects/ pages; 8 skipped (5 empty Untitled, 3 with no relevant entity links) |
| 2026-04-07 | Home.md update       | 1              | Added vault stats table, folder navigation, Topics nav with counts, and category summary table; all 99 conversations retained in category sections |