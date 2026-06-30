# Hormone Analysis Engine (LIE-v1.0)

This directory contains the integration wrapper for the Lab Intelligence Engine (LIE) of the Oviora platform.

Unlike typical parameter-based tabular risk models, the Hormone Analysis Engine acts as an orchestrator for OCR extraction, biomarker normalization, and LLM clinical insight generation.

## Files
- `inference.py`: Production integration entry point exposing the `predict()` function.
- `__init__.py`: Module initializer.
