# Test Plan

## Deployment smoke tests

- App loads with valid Secrets.
- App shows configuration error when key is missing.
- UI renders on Python 3.12.

## Agent tests

- Definition request routes to TEACH.
- Uploaded-document request routes to KNOWLEDGE or TEACH with retrieved context.
- Practice request routes to PRACTICE.
- Answer-check request routes to EVALUATE.
- Revision request routes to REVISION.
- Planning request routes to PLAN.
- Calculation request routes to CALCULATE.

## RAG tests

- PDF extraction preserves page numbers.
- DOCX extraction returns text.
- TXT/MD extraction works.
- Empty documents do not crash the app.
- Hybrid retrieval returns relevant chunks.

## Safety and integrity tests

- Tutor encourages learning and reasoning rather than pretending unsupported facts are known.
- Research failures are reported instead of fabricated.
- Secrets never appear in logs or UI.
