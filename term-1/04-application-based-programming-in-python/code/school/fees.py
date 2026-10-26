"""school.fees: fee calculation."""
PER_CREDIT = 6_500          # illustrative fee per credit hour (Rs)

def fee_due(credits, scholarship_pct=0, late=False):
    """Semester fee after scholarship, plus a flat Rs 2,000 late charge if late."""
    fee = credits * PER_CREDIT * (1 - scholarship_pct / 100)
    return round(fee + (2_000 if late else 0))
