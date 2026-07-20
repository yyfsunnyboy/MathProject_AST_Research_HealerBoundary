def generate(level=1, **kwargs):
    p1_range = kwargs.get("p1", [2, 6])
    p2_range = kwargs.get("p2", [1, 5])
    
    import random
    
    if len(p1_range) != 3 or not (isinstance(p1_range[0], int) and isinstance(p1_range[-1], int)):
        raise ValueError("Invalid parameters for generate.")

    p1 = p1_range[1] if len(p1_range) == 2 else random.randint(*p1_range)
    p2 = p2_range[1] if len(p2_range) == 2 else random.randint(*p2_range)

    
    numerator = (1 - p1 / 6) * (1 - p2 / 5)
    denominator = ((1 + p1/6) * (3-p2)) / 4
    
    num, den = int(numerator), int(denominator)
    
    if len(str(num).replace('.', '')) < 9:
        final_num = str(num)
        
    else:
        frac_part = float(final_num.replace(".","")) - int(final_num.replace(".", ""))

    fraction_string = f"{frac_part:.2f}"
    
    numerator_str, denominator_str = "1", "6"
    canonical_latex = r"\text{numerator} + \text{denominator}"
    

    return {
        "question_text": r"The probability of an event occurring in a single trial is $p$. If two independent events occur with probabilities $\frac{a}{b}$ and $\frac{c}{d}$, what is the fraction representing their combined occurrence? Use formal LaTeX delimiters.",
        "correct_answer": {
            "numerator": numerator_str,
            "denominator": denominator_str,
            "canonical_latex": canonical_latex
        },
        "oracle_payload": {"p1": p1_range[0], "p2": p2_range[0]} if isinstance(p1_range, list) else None
    }