def generate(level=1, **kwargs):
    p1_min = 2
    p1_max = 6
    p2_min = 1
    p2_max = 5
    
    import random
    r1 = random.randint(p1_min, p1_max)
    r2 = random.randint(p2_min, p2_max)
    
    numerator = r1 * r2
    denominator = (r1 + r2) ** 2
    
    gcd_val = math.gcd(numerator, denominator)
    num_canonical = numerator // gcd_val
    den_canonical = denominator // gcd_val
    
    question_text = r"Let $P_1$ and $P_2$ be independent events with probabilities $\frac{r_1}{s}$ and $\frac{r_2}{t}$. If the probability of both occurring is given as a fraction derived from products, find the irreducible form where numerator equals product and denominator equals sum squared."
    
    correct_answer = {
        "numerator": num_canonical,
        "denominator": den_canonical,
        "canonical_latex": f"\frac{{{num_canonical}}}{{<{len(str(den_canonical))}>}}" # Placeholder for dynamic latex length check if needed, but spec asks for canonical form. Let's use standard LaTeX format directly.
    }
    
    import math
    
    correct_answer["canonical_latex"] = rf"\frac{{{num_canonical}}}{{{den_canonical}}}"

    oracle_payload = {"p1": [2, 6], "p2": [1, 5]}