# HCM-Engine (Hierarchical Containment Model Engine)

**Governance-driven containment decision engine** for sociotechnical smart home cybersecurity.

This repository implements the **core HCM decision logic** as an auditable, deterministic engine:
- Impact: `I = a × T(s) × C(s)`
- Decision outcomes: `ALLOW`, `DEFER`, `CONTAIN`
- Focus: **proportional, context-sensitive governance** (not surveillance, not raw detection)

## Why this exists
Smart home security decisions cannot be reduced to anomaly magnitude alone. HCM makes containment a *governance problem*:
- `a` (anomaly) is necessary but insufficient
- `T(s)` (trust) and `C(s)` (dependency/centrality) shape systemic consequence
- decisions remain **interpretable and auditable**

## Quick Example (Decision Core)
Input:
- device: `camera`
- anomaly: `0.78`
- trust: `0.90`
- centrality: `0.60`

Impact:
- `I = 0.78 × 0.90 × 0.60 = 0.4212`

Decision (default thresholds):
- `theta_a = 0.5`
- `theta_I = 0.3`
=> **CONTAIN**

## Project Structure
- `core/` : deterministic decision logic
- `schemas/` : decision output contracts (JSON Schema)
- `tests/` : unit tests for governance correctness
- `api/` : service layer (FastAPI)

## Roadmap
- [ ] FastAPI service endpoint for real integrations
- [ ] Policy plugins (learned policy as optional layer)
- [ ] Centrality loader for real home network graphs
- [ ] Governance audit logs + stability metrics
