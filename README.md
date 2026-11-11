# Ripple — Scenario Studio

A visual, explainable what-if simulator for business decisions. The initial MVP explores how subscription pricing changes can affect churn, revenue, and profit.

## Run

Requires Python 3.10+; no external dependencies.

```bash
python app.py
```

Open http://localhost:8000. Run tests with `python -m unittest discover -v`.

## Model

- Adjusted price = base price × (1 + price change)
- Estimated churn = clamp(base churn + price change × sensitivity, 0, 1)
- Retained customers = round(customers × (1 − estimated churn))
- Revenue = retained customers × adjusted price
- Profit = revenue − fixed monthly costs

This model is **illustrative, not a business forecast**. Its purpose is to surface trade-offs and assumptions.

## Roadmap

1. Save and compare named scenarios in SQLite.
2. Add FastAPI endpoints and input validation.
3. Introduce customer segments and confidence intervals.
4. Add staffing, inventory, and operations scenarios.
5. Build a React/TypeScript frontend and CI.
