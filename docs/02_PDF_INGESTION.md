# Milestone 2 — PDF Ingestion

## Goal

Load the supplied PDFs and extract useful text while preserving page-level source information.

## Documents

The assignment provides:

- Product_Manual.pdf
- Employee_Handbook.pdf
- API_Reference.pdf
- FAQ_Support.pdf
- Security_Policy.pdf
- Onboarding_Guide.pdf
- Pricing_and_SLA.pdf

## AI IDE instructions

Build an ingestion component that:

1. Finds PDFs in the configured input directory.
2. Opens every PDF.
3. Processes every page.
4. Extracts text.
5. Preserves document name.
6. Preserves page number.
7. Handles empty/problematic pages without crashing the whole run.
8. Handles tables reasonably.
9. Normalizes obvious extraction artifacts.
10. Produces reusable processed output.

## Metadata

Every extracted page/segment must retain:

- document name
- page number
- extracted text
- section information when available

Do not lose page numbers. They are required for final source attribution.

## Acceptance criteria

- All PDFs can be processed in one ingestion run.
- Extraction failures are logged.
- One bad page does not stop all documents.
- Page metadata survives processing.
- Table content is reasonably usable as text.

## Tests

Add tests for:

- PDF discovery
- page extraction
- metadata preservation
- problematic/empty input handling
