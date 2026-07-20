def generate(level=1, **kwargs):
    # Frozen sampled parameters used to construct the problem instance
    p1_candidates = kwargs.get("p1", [2, 6])
    p2_candidates = kwargs.get("p2", [1, 5])
    
    n1 = random.choice(p1_candidates) if "n1" not in globals() else None # Reset for fresh run logic? No, re-pick every time.
    m1 = n1 
    n2 = random.choice(p2_candidates) if "m2" not in globals() else None
    m2 = n2
    
    # Assumption: Probabilities are fractions with denominators equal to the max of their respective candidate lists
    # P(A) = n1 / 6, P(B) = n2 / 5 (since max(p1)=6, max(p2)=5)
    
    num_prod = m1 * m2
    den_prod = 30
    
    common_divisor = gcd(num_prod, den_prod)
    final_num = num_prod // common_divisor
    final_den = den_prod // common_divisor
    
    correct_answer_numerator = str(final_num)
    correct_answer_denominator = str(final_den)
    
    # Canonical LaTeX for irreducible fraction
    canonical_latex = r"\frac{" + correct_answer_numerator + "}{" + correct_answer_denominator + "}"
    
    question_text = (r"Let events $A$ and $B$ be independent. 
    If the probability of event $A$ is $\frac{\text{'\"{n1}'} }{6}$ and the probability of event $B$ is $\frac{\text{\"{m2}\"}}{5}$,
    what is the probability that both events occur?")
    
    # Replace placeholders with actual values for question text generation
    q_text = r"Let events $A$ and $B$ be independent. 
    If the probability of event $A$ is $\frac{\text{'\"{n1}'} }{6}$ and the probability of event $B$ is $\frac{\text{\"{m2}\"}}{5}$,
    what is the probability that both events occur?"".replace("'{n1}'", str(m1)).replace("'\\", "'").replace("\\'", "\\'") # Simple replacement
    
    # Better construction for LaTeX safety in string
    q_text = r"Let $A$ and $B$ be independent events with probabilities $\frac{\text{'\"{m1}'} }{6}$ and $\frac{\text{\"{m2}\"}}{5}$ respectively. What is the probability of both occurring?"
    
    # Final text construction avoiding quote issues in LaTeX string replacement
    
    q_text = f"Let $A$ and $B$ be independent events with probabilities $\\frac{{1}}{{6}}$? No."
    
    # Let's write it cleanly without complex escaping by building the string parts
    part_a = r"\frac{" + str(m1) + "}{6}"
    part_b = r"\frac{" + str(m2) + "}{5}"
    question_text = f"Let $A$ and $B$ be independent events with probabilities {part_a} and {part_b}. What is the probability of both occurring?"

    oracle_payload = {"p1": p1_candidates, "p2": p2_candidates} # Exactly as frozen
    
    return {
        "question_text": question_text,
        "correct_answer": {
            "numerator": correct_answer_numerator,
            "denominator": correct_answer_denominator,
            "canonical_latex": canonical_latex
        },
        "oracle_payload": oracle_payload
    }
