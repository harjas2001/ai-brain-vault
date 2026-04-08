# 🧠 AI Brain Vault

A personal knowledge graph built from my entire Claude conversation history — exported, tagged, linked, and visualised in Obsidian.

Built using **Claude Code**, **Obsidian**, and a token-efficient session workflow managed via `CLAUDE.md`.

<img width="420" height="358" alt="image" src="https://github.com/user-attachments/assets/f2fd069a-614e-4181-9803-44f720db7d6d" />
With tags:
<img width="468" height="438" alt="image" src="https://github.com/user-attachments/assets/b1580939-a767-4010-8e90-96ce790dc7cf" />

---

## What This Is

Every conversation I've had with Claude, converted into structured markdown files with:

- Frontmatter tags (topics, technologies, projects, people)
- Entity pages for recurring people, projects, and topics
- Wikilinks connecting related conversations
- A visual graph showing how ideas and projects connect over time

---

## Stack

| Tool | Role |
|---|---|
| Claude (claude.ai) | Source — conversation history exported as JSON |
| Claude Code (CLI) | Processing engine — tagging, linking, entity pages |
| Obsidian | Visualisation — graph view, full-text search |
| CLAUDE.md | Persistent context layer across Claude Code sessions |
| Python (build_vault.py) | Initial conversion of conversations.json to markdown |

---

## Vault Structure

```
ai-brain-vault/
├── CLAUDE.md               ← Session context and task state for Claude Code
├── README.md               ← This file
├── build_vault.py          ← Initial conversion script (run once)
├── conv_index.json         ← Index of all conversations (slug, date, category)
├── Home.md                 ← Vault home page
├── Conversations/          ← One .md file per conversation, fully tagged
├── People/                 ← Entity pages for people mentioned across chats
├── Projects/               ← Entity pages for recurring projects
└── Topics/                 ← Entity pages for recurring themes and topics
```

---

## How It Was Built

### 1. Export
Exported full Claude conversation history via **Settings → Privacy → Export Data**. Received `conversations.json` within ~5 minutes.

### 2. Initial Conversion
Ran `build_vault.py` to convert all conversations from JSON into individual markdown files with frontmatter scaffolding.

### 3. Tagging (Claude Code)
Used Claude Code in batches of 25 files per session to fill in tags, people, projects, and technologies on every conversation. The `CLAUDE.md` file tracked progress across sessions so no work was repeated.

### 4. Entity Pages (Claude Code)
Generated topic entity pages in `Topics/` based on recurring tags found during the tagging pass.

### 5. Wikilinks (Claude Code)
Added a `## Related` section to every conversation file linking to relevant People, Projects, and Topics pages — creating the connections that power the Obsidian graph.

---

## CLAUDE.md — The Key to Efficient Sessions

`CLAUDE.md` is the most important file in this project. Claude Code reads it automatically at the start of every session. It contains:

- Current task state (what's done, what's remaining)
- Directory structure and file locations
- Frontmatter schema and tagging rules
- Batch size and sub-agent limits
- A progress log updated after every session

This eliminates context re-establishment across sessions, which is the biggest source of token waste when using Claude Code for large projects.

---

## Conversation Categories

Conversations are organised into the following categories:

- Protein Biology & Antibody Discovery
- DevOps & Infrastructure
- Data & Analytics
- Machine Learning & AI
- Software Engineering
- Business & Strategy

---

## Obsidian Graph View

Open the vault in Obsidian and press `Ctrl+G` (Windows) or `Cmd+G` (Mac) to see the full knowledge graph. Hub nodes with the most connections represent the most recurring projects and themes across all conversations.

**Recommended graph settings:**
- Enable Tags in the filter panel
- Set Node size by number of connections
- Use Groups to colour-code by folder (Conversations / People / Projects / Topics)

---

## Keeping It Updated

Claude does not offer live sync — exports are manual. To add new conversations:

1. Export fresh data from claude.ai (Settings → Privacy → Export Data)
2. Place the new `conversations.json` in the vault directory
3. Run a Claude Code sync session:

```
Read CLAUDE.md. Check conversations.json for any conversations not already 
in Conversations/. Convert new ones, tag them, add wikilinks. 
Update CLAUDE.md when done. Stop.
```

---

## Token Efficiency Lessons

Key things learned running this project under Claude Pro usage limits:

- **One task per session, 25 files at a time** — keeps sessions bounded and recoverable
- **`tagged: true` frontmatter flag** — idempotency gate that prevents re-processing
- **CLAUDE.md progress log** — eliminates context re-establishment cost between sessions
- **End every prompt with "Stop."** — prevents Claude Code from chaining into the next task
- **Never chain tasks** — convert, tag, link, and entity pages are four separate sessions

---

## Note on Privacy

Raw export files (`conversations.json`, `memories.json`, `projects.json`) are excluded via `.gitignore`. This repo contains only the processed markdown output.
