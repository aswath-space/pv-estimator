import numpy as np

DEFAULT_COST_PER_KW = 1000  # USD per kWp (market average, IRENA 2022)
DEFAULT_ELECTRICITY_PRICE = 0.15  # USD per kWh
DEFAULT_LIFETIME_YEARS = 25

def estimate_initial_cost(capacity_kw, cost_per_kw=DEFAULT_COST_PER_KW):
    """Estimate initial investment from capacity in kW and cost per kW."""
    return capacity_kw * cost_per_kw


def estimate_annual_savings(annual_production_kwh, electricity_price=DEFAULT_ELECTRICITY_PRICE):
    """Estimate annual savings based on production and electricity price."""
    return annual_production_kwh * electricity_price


def calculate_irr(initial_cost, annual_savings, lifetime_years=DEFAULT_LIFETIME_YEARS):
    """Calculate internal rate of return for a PV system."""
    cash_flows = [-initial_cost] + [annual_savings] * lifetime_years
    irr = np.irr(cash_flows)
    return irr
