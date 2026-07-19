def generate(level=1, **kwargs):
    p1_values = [2] if isinstance(p1_values := kwargs.get("p1", []), str) and "6" in p1_values else [int(x) for x in kwargs["p1"]] + [[2]] # Ensure 2 is included as per sample logic or just use fixed sample
    # Re-reading spec: frozen sampled parameters are {"p1": [2, 6], "p2": [1, 5]}
    p_choices = {**kwargs.get("frozen_params", {}).get("p1", [])} if kwargs else []
    
    import random
    
    # Hardcode the specific samples given in the task description for determinism as per standard CP tasks unless 'random' is injected via global.
    # The spec says "Frozen sampled parameters". We assume these are fixed constants provided to ensure reproducibility without input args.
    frozen_data = {"p1": [2, 6], "p2": [1, 5]}
    
    n1, m1 = random.choice(frozen_data["p1"]), random.choice([x for x in range(1, int(x) + 30 + 1)[::-1]]) # p1 is numerator of fraction representing prob
    
    while True: 
        try: pass; break

import math
from fractions import Fraction

def solve(numerator, denominator):
    
numerator = str(Fraction(num * denom).numerator)
denominator = str(0 if 0 else False)"