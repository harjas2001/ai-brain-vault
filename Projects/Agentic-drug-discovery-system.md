---
title: "Agentic drug discovery system"
uuid: 019cf061-9a5d-72e8-abcc-7fc90a7bcbd8
date: 2026-03-15
type: project
tags: []
---

# Agentic drug discovery system

## Description

The goal of this project is to build an agentic drug discovery system for antibody design that can iteratively generate and refine candidate antibodies against a given biological target.

Traditional computational drug discovery workflows often rely on single-model predictions, which can lead to model bias or overconfident outputs. Instead, this system explores a consensus-based modelling approach, where predictions from one or more AI models are evaluated, refined, and iteratively improved through an agent-driven decision loop.

The long-term vision is to create an “antibody discovery operating system” built around a design council architecture, where multiple models propose candidates and an agent aggregates their outputs to generate superior designs. Rather than trusting one model’s prediction, the system aggregates multiple expert-like opinions—similar to consulting multiple specialists rather than relying on a single diagnosis.

For the initial MVP, the system will implement a simplified two-agent architecture:

Model Agent (Generation Agent)

1. Uses a protein design model (e.g., BoltzGen or similar) to generate antibody candidates against a specified target.

2. Produces a ranked list of candidate binders (e.g., top 10 designs) with associated metrics such as binding scores, stability, or other structural evaluation metrics.

Master Agent (Evaluation Agent)

Acts as the decision-making and evaluation layer.

Reviews the generated candidates and their metrics.

Identifies weaknesses or areas for improvement (e.g., binding affinity, stability, structural plausibility).

Sends structured feedback back to the Model Agent to guide the next design iteration.

This creates an iterative optimization loop:

Target → Model Agent generates binders → Master Agent evaluates → Feedback → Model Agent redesigns → Repeat

The loop continues until the Master Agent determines that a candidate satisfies predefined quality thresholds. At that point, the system outputs the final antibody design candidate.

The purpose of this MVP is to establish the core agentic workflow required for automated antibody discovery. Once validated, the system will be extended into a multi-model “design council” architecture, where several AI models independently propose candidates and a coordinating agent aggregates the strongest features from each design to generate improved hybrid candidates.

Ultimately, this project aims to demonstrate that agent-based consensus modelling can improve robustness, confidence, and exploration of the antibody design space, forming the foundation for a scalable automated drug discovery platform.

## Prompt Template

Role
You are an expert in:
- computational biology
- antibody engineering
- protein design systems
- AI agents and multi-agent architectures
 -drug discovery pipelines

Your task is to help design and implement an agentic antibody discovery system.
You should think like a research engineer building a drug discovery platform, not just answering questions.

Prioritize:
- system architecture
- reproducible pipelines
- modular design
- biologically realistic constraints
- scalable AI workflows


Behaviour
When responding:
1. Think in terms of drug discovery pipelines.
2. Break problems into modular components.
3. Suggest agent architectures and orchestration workflows.
4. Prefer structured outputs when possible.
5. Focus on automation and iterative improvement loops.

When discussing antibody design:
Consider factors such as:
- binding affinity
- structural stability
- developability
- solubility
- sequence plausibility
- CDR design
- structural compatibility with antigen


Goal of the System
The system should behave like an automated antibody discovery workflow that:
1. Generates antibody candidates
2. Evaluates them using defined metrics
3. Iteratively improves them
4. Outputs a final candidate design

## Related Conversations

_To be populated by tagging agents_
