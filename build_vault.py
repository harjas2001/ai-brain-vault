"""
Obsidian Vault Builder for Claude Conversations
Converts conversations.json into individual markdown files with frontmatter.
"""
import json
import os
import re
from datetime import datetime

BASE = "C:/Users/harja/OneDrive/Desktop/Claude DB"
DATA = f"{BASE}/data-2026-04-05-07-51-26-batch-0000"

DIRS = [
    f"{BASE}/Conversations",
    f"{BASE}/Projects",
    f"{BASE}/People",
    f"{BASE}/Topics",
    f"{BASE}/.obsidian",
]

CATEGORY_RULES = [
    ("Protein Biology & Antibody Discovery", [
        "antibody", "antigen", "epitope", "protein", "boltz", "lightdock",
        "cdr", "vhh", "docking", "binding", "affinity", "nanobody", "igfold",
        "prodigy", "alphafold", "fasta", "pdb", "structure", "residue",
        "abodybuilder", "binder", "fab", "paratope", "clash", "chain"
    ]),
    ("Conversational AI & Voicebot", [
        "genesys", "dialogflow", "voicebot", "chatbot", "intent", "utterance",
        "nlu", "stt", "no_match", "fallback", "tpg", "iinet", "containment",
        "phrase", "conversational", "bot flow", "nlp topic"
    ]),
    ("ML & AI Engineering", [
        "machine learning", "model", "training", "inference", "pipeline",
        "embedding", "checkpoint", "gat", "esm", "pytorch", "ml pipeline",
        "neural", "classification", "clustering", "kmeans", "tfidf"
    ]),
    ("Business & Strategy", [
        "actimo", "actimap", "startup", "pitch", "strategy", "naming",
        "prochestra", "drug discovery", "roadmap", "pilot", "client",
        "monetis", "revenue", "business", "co-founder", "launch", "brand"
    ]),
    ("Career & Resume", [
        "resume", "job", "role", "assessment", "interview", "application",
        "linkedin", "vivanti", "heidi", "mantel", "career", "performance review"
    ]),
    ("DevOps & Infrastructure", [
        "conda", "environment", "installation", "gcp", "gcloud", "docker",
        "compute engine", "bigquery", "gcs", "path", "error", "debug",
        "segmentation fault", "long path", "windows", "gpu", "a100"
    ]),
    ("Data & Analytics", [
        "csv", "pandas", "data", "analysis", "power bi", "aggregation",
        "sql", "extract", "parse", "format", "column", "mapping"
    ]),
    ("Finance & Investment", [
        "investment", "banking", "financial", "company", "valuation",
        "extraction", "standardis"
    ]),
    ("Travel & Personal", [
        "travel", "insurance", "racv", "flight", "uae", "cancelled",
        "geopolitical", "claim"
    ]),
]

PROJECT_MAP = {
    "0199b378": "epitope-mapping-test-portal",
    "019a72e6": "web-test-portal",
    "019cdb2c": "voicebot-phrase-app",
    "019cf061": "agentic-drug-discovery-system",
    "019d3eee": "investment-banking-agent",
    "01975367": "how-to-use-claude",
}

def slugify(text):
    """Convert text to safe filename."""
    text = re.sub(r'[^\w\s-]', '', text or "untitled")
    text = re.sub(r'[\s]+', '-', text.strip())
    text = text[:80]
    return text.strip('-') or "untitled"

def detect_category(text):
    text_lower = text.lower()
    scores = {}
    for cat, keywords in CATEGORY_RULES:
        score = sum(1 for kw in keywords if kw in text_lower)
        if score > 0:
            scores[cat] = score
    if not scores:
        return "General"
    return max(scores, key=scores.get)

def format_messages(messages):
    parts = []
    for msg in messages:
        sender = "**Harjas**" if msg.get("sender") == "human" else "**Claude**"
        text = msg.get("text") or ""
        # Also check content array for text
        if not text and msg.get("content"):
            for block in msg["content"]:
                if isinstance(block, dict) and block.get("type") == "text":
                    text = block.get("text", "")
                    break
        if text:
            parts.append(f"{sender}\n\n{text.strip()}")
    return "\n\n---\n\n".join(parts)

def build_conversations():
    with open(f"{DATA}/conversations.json", "r", encoding="utf-8") as f:
        convs = json.load(f)
    with open(f"{DATA}/projects.json", "r", encoding="utf-8") as f:
        projects = json.load(f)

    # Build project lookup
    proj_by_uuid = {p["uuid"]: p for p in projects}

    # Track filenames for dedup
    used_names = {}
    conv_index = []  # for the index file

    for conv in convs:
        uuid = conv["uuid"]
        name = conv.get("name") or "Untitled Conversation"
        summary = conv.get("summary") or ""
        created = conv.get("created_at", "")[:10]
        updated = conv.get("updated_at", "")[:10]
        messages = conv.get("chat_messages", [])

        # Detect category from name + summary + messages text
        full_text = name + " " + summary
        for m in messages[:3]:
            full_text += " " + (m.get("text") or "")
        category = detect_category(full_text)

        # Filename
        base_slug = slugify(name)
        if base_slug in used_names:
            used_names[base_slug] += 1
            slug = f"{base_slug}-{used_names[base_slug]}"
        else:
            used_names[base_slug] = 1
            slug = base_slug

        filename = f"{slug}.md"
        filepath = f"{BASE}/Conversations/{filename}"

        # Message content
        msg_md = format_messages(messages)
        msg_count = len(messages)

        # Frontmatter
        frontmatter = f"""---
title: "{name.replace('"', "'")}"
date: {created}
updated: {updated}
uuid: {uuid}
category: "{category}"
tags: []
people: []
places: []
projects: []
technologies: []
msg_count: {msg_count}
---"""

        # Summary section
        summary_section = ""
        if summary:
            summary_section = f"\n## Summary\n\n{summary}\n"

        content = f"""{frontmatter}

# {name}
{summary_section}
## Conversation

{msg_md}
"""

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

        conv_index.append({
            "slug": slug,
            "name": name,
            "date": created,
            "category": category,
            "filename": filename,
        })
        print(f"  Created: {filename}")

    return conv_index, projects

def build_projects(projects):
    for p in projects:
        uuid_short = p["uuid"][:8]
        name = p.get("name", "Unnamed Project")
        desc = p.get("description") or ""
        slug = slugify(name)
        created = p.get("created_at", "")[:10]

        content = f"""---
title: "{name.replace('"', "'")}"
uuid: {p['uuid']}
date: {created}
type: project
tags: []
---

# {name}

## Description

{desc}

## Prompt Template

{p.get('prompt_template') or '_None_'}

## Related Conversations

_To be populated by tagging agents_
"""
        filepath = f"{BASE}/Projects/{slug}.md"
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  Created project: {slug}.md")

def build_people_note():
    content = """---
title: "People Index"
type: index
tags: [people, index]
---

# People

Key people mentioned across conversations.

## Harjas Singh
- Co-founder & Engineer at [[Projects/agentic-drug-discovery-system|ActiMo Labs]]
- Conversational AI Specialist at TPG Telecom
- Background: Biomedical Engineering (RMIT)

## Organisations
- **ActiMo Labs** — AI-driven antibody discovery startup (co-founded by Harjas)
- **TPG Telecom** — Telco; Harjas builds voicebot systems here
- **iiNet** — TPG subsidiary, voicebot work
- **Novartis** — Pharma; key meeting that shaped ActiMo strategy
- **Vivanti** — Data engineering role assessment
- **RMIT** — Harjas's university
- **Mantel** — Job application target
- **RACV** — Travel insurance claim context
"""
    with open(f"{BASE}/People/People-Index.md", "w", encoding="utf-8") as f:
        f.write(content)
    print("  Created: People/People-Index.md")

def build_home(conv_index):
    # Group by category
    by_cat = {}
    for c in conv_index:
        cat = c["category"]
        by_cat.setdefault(cat, []).append(c)

    sections = []
    for cat, items in sorted(by_cat.items()):
        items_sorted = sorted(items, key=lambda x: x["date"], reverse=True)
        lines = [f"## {cat}\n"]
        for item in items_sorted:
            lines.append(f"- [[Conversations/{item['slug']}|{item['name']}]] `{item['date']}`")
        sections.append("\n".join(lines))

    home_content = f"""---
title: "Home"
type: dashboard
tags: [home, index]
---

# Claude Conversations Vault

> Knowledge base of {len(conv_index)} conversations with Claude, organised by topic.

## Quick Stats
- **Total Conversations**: {len(conv_index)}
- **Date Range**: Oct 2025 – Apr 2026
- **Categories**: {len(by_cat)}

## Projects
- [[Projects/agentic-drug-discovery-system|Agentic Drug Discovery System]]
- [[Projects/epitope-mapping-test-portal|Epitope Mapping Test Portal]]
- [[Projects/voicebot-phrase-app|Voicebot Phrase App]]
- [[Projects/investment-banking-agent|Investment Banking Agent]]
- [[Projects/web-test-portal|Web Test Portal]]

## People & Context
- [[People/People-Index|People & Organisations]]

---

{chr(10).join(chr(10).join(s.split(chr(10))) + chr(10) for s in sections)}
"""
    with open(f"{BASE}/Home.md", "w", encoding="utf-8") as f:
        f.write(home_content)
    print("  Created: Home.md")

def build_obsidian_config():
    config = """{
  "versioningScheme": "none",
  "defaultViewMode": "source",
  "livePreview": true,
  "theme": "obsidian",
  "accentColor": ""
}"""
    with open(f"{BASE}/.obsidian/app.json", "w", encoding="utf-8") as f:
        f.write(config)

    appearance = '{"theme": "obsidian"}'
    with open(f"{BASE}/.obsidian/appearance.json", "w", encoding="utf-8") as f:
        f.write(appearance)

    # Graph config
    graph = """{
  "collapse-filter": false,
  "search": "",
  "showTags": true,
  "showAttachments": false,
  "hideUnresolved": false,
  "showOrphans": true,
  "collapse-color-groups": false,
  "colorGroups": [],
  "collapse-display": false,
  "showArrow": true,
  "textFadeMultiplier": 0,
  "nodeSizeMultiplier": 1,
  "lineSizeMultiplier": 1,
  "collapse-forces": false,
  "centerStrength": 0.518713248970312,
  "repelStrength": 10,
  "linkStrength": 1,
  "linkDistance": 30,
  "scale": 1,
  "close": false
}"""
    with open(f"{BASE}/.obsidian/graph.json", "w", encoding="utf-8") as f:
        f.write(graph)
    print("  Created: .obsidian config files")

def main():
    print("Creating directories...")
    for d in DIRS:
        os.makedirs(d, exist_ok=True)

    print("\nConverting conversations...")
    conv_index, projects = build_conversations()

    print("\nBuilding project files...")
    build_projects(projects)

    print("\nBuilding people index...")
    build_people_note()

    print("\nBuilding Home dashboard...")
    build_home(conv_index)

    print("\nBuilding Obsidian config...")
    build_obsidian_config()

    print(f"\nDone! {len(conv_index)} conversations converted.")
    print(f"Vault is at: {BASE}")

    # Output the conversation list as JSON for agents to use
    with open(f"{BASE}/conv_index.json", "w", encoding="utf-8") as f:
        json.dump(conv_index, f, indent=2, ensure_ascii=False)
    print("Saved conv_index.json for tagging agents.")

if __name__ == "__main__":
    main()
