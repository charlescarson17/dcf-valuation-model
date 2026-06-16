"""
Projections: builds a multi-year unlevered Free Cash Flow forecast
Starts with a base revenue figure (last year) and applies a set of assumptions.

Unlevered FCF = EBIT * (1 - tax rate) + D&A - Capex - Change in Net Working Capital
"""

def project_fcf(base_revenue, assumptions, years=5):
    """
    Forecast unlevered FCF using per-year assumptions.

    Each assumption is a list with one value per year.
    Ex: 'revenue_growth': [0.20, 0.16, 0.12, 0.09, 0.06]

    Lists must each have a lenght == forecast years
    """

    #Validate that every assumption list matches the forecast horizon
    for key, value in assumptions.items():
        if len(value) != years:
            raise ValueError(
                f"'{key}' has {len(value)} values but needs {years}"
            )
        
    projections = []
    prev_revenue = base_revenue

    for i in range(years):
        year = i + 1

        #Index each assumption by the current year
        revenue = prev_revenue * (1 + assumptions['revenue_growth'][i])
        ebit = revenue * assumptions['operating_margin'][i]
        nopat = ebit * (1 - assumptions['tax_rate'][i])
        da = revenue * assumptions['da_pct'][i]
        capex = revenue * assumptions['capex_pct'][i]

        revenue_change = revenue - prev_revenue
        change_in_nwc = revenue_change * assumptions['nwc_pct'][i]

        fcf = nopat + da - capex - change_in_nwc

        projections.append({
            'year': year,
            'revenue': revenue,
            'ebit': ebit,
            'fcf': fcf,
        })

        prev_revenue = revenue

    return projections