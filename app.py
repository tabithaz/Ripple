"""Ripple: explainable business scenario simulation API (standard library only)."""
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import math
from pathlib import Path


def simulate(customers=10000, price=20, price_change=0, churn=0.05, churn_sensitivity=0.4, costs=80000):
    """Estimate one-month revenue and profit with transparent assumptions."""
    values = (customers, price, price_change, churn, churn_sensitivity, costs)
    if any(isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) for value in values):
        raise ValueError('scenario parameters must be finite numbers')
    if not isinstance(customers, int) or customers < 0 or price < 0 or costs < 0 or not 0 <= churn <= 1 or price_change <= -1 or churn_sensitivity < 0:
        raise ValueError('invalid scenario parameters')
    new_price = price * (1 + price_change)
    projected_churn = min(1.0, max(0.0, churn + price_change * churn_sensitivity))
    retained = round(customers * (1 - projected_churn))
    revenue = round(retained * new_price, 2)
    return {'retained_customers': retained, 'churn_rate': round(projected_churn, 4), 'monthly_revenue': revenue, 'monthly_profit': round(revenue - costs, 2), 'assumptions': {'churn_sensitivity': churn_sensitivity, 'model': 'illustrative linear sensitivity; not a forecast'}}


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path not in ('/', '/api/demo'):
            self.send_error(404)
            return
        if self.path == '/':
            payload = (Path(__file__).resolve().parent / 'index.html').read_bytes()
            content_type = 'text/html; charset=utf-8'
        else:
            payload = json.dumps([{'change': pct, **simulate(price_change=pct)} for pct in (-0.2, -0.1, 0, 0.1, 0.2)]).encode()
            content_type = 'application/json'
        self.send_response(200)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)


if __name__ == '__main__':
    print('Ripple running at http://localhost:8000')
    HTTPServer(('127.0.0.1', 8000), Handler).serve_forever()
