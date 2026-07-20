def generate(level=1, **kwargs):
    p1_options = [2, 6]
    p2_options = [1, 5]
    
    import random
    
    selected_p1 = random.choice(p1_options)
    selected_p2 = random.choice(p2_options)
    
    numerator = selected_p1 * selected_p2
    denominator = (selected_p1 + selected_p2) ** 3
    
    gcd_val = 1
    for i in range(1, min(numerator, denominator) + 1):
        if numerator % i == 0 and denominator % i == 0:
            gcd_val = i
            break
    
    irreducible_numerator = numerator // gcd_val
    irreducible_denominator = denominator // gcd_val
    
    question_text = r"Let $P_1$ be an event with probability $\frac{a}{b}$ where $a, b \in [2, 6]$ and $P_2$ be an independent event with probability $\frac{c}{d}$ where $c, d \in [1, 5]$. Given that the combined outcome involves a product of probabilities scaled by their sum cubed in the denominator context defined as $\left(\sum P_i\right)^3$, calculate the irreducible fraction representing the specific case."
    
    correct_answer = {
        "numerator": str(irreducible_numerator),
        "denominator": str(irreducible_denominator),
        "canonical_latex": f"${\\frac{{{irreducible\_numerator}}}{{{irreducible\_denominator}}}}$"
    }
    
    oracle_payload = {"p1": p1_options, "p2": p2_options}
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }