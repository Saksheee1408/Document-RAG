# Milestone 9 — Source Attribution

## Goal

Make every answer verifiable.

## Required source information

For each supporting result expose:

- source document name
- page number
- chunk ID/reference
- optionally a short source excerpt

## Example output concept

Answer:
Employees are entitled to ...

Sources:
- Employee_Handbook.pdf — Page 5 — Chunk employee_handbook_p5_03
- Employee_Handbook.pdf — Page 6 — Chunk employee_handbook_p6_01

## Critical rules

- Never invent page numbers.
- Never invent chunk IDs.
- Only show sources retrieved for the current question.
- Keep source metadata attached from ingestion through final response.

## Acceptance criteria

Answerable questions display source information.
Unanswerable questions do not display fabricated sources.
