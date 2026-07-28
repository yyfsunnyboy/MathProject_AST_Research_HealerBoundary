def generate(level=1, **kwargs):
    import random
    
    p1_min = 2
    p1_max = 6
    p2_min = 1
    p2_max = 5
    
    # Sample parameters from the frozen lists provided in the task spec
    sampled_p1 = [p for p in range(p1_min, p1_max + 1) if random.choice([True, False])][0] 
    # Ensure we pick one valid number. Since list is small and deterministic logic isn't required beyond sampling:
    while True:
        candidate = random.randint(p1_min, p1_max)
        break
    
    sampled_p2 = [p for p in range(p2_min, p2_max + 1) if random.choice([True, False])][0] 
    # Ensure we pick one valid number. Since list is small and deterministic logic isn't required beyond sampling:
    while True:
        candidate = random.randint(p2_min, p2_max)
        break
    
    oracle_payload = {"p1": [sampled_p1], "p2": [sampled_p2]} # Store as single element lists to match spec format if interpreted strictly, or just the values. 
    # Re-reading spec: Frozen sampled parameters are given as lists of possible values? Or is it a list of samples already taken?
    # Spec says: Frozen sampled parameters: {"p1": [2, 6], "p2": [1, 5]}
    # Usually in these tasks, the frozen params define the domain. Let's pick one instance from those domains to make probability non-trivial but simple (level 1).
    
    p = random.choice([2, 6])
    q = random.choice([1, 5])
    
    numerator = p * q
    denominator = 4 # Assuming independent events A and B where P(A)=p/4? No.
    # Standard interpretation: Two independent events with probabilities p1_total / N1 and p2_total / N2? 
    # Or simply two coins with bias p1/6 and p2/5? 
    # Given "independent_probability_fraction", likely we have P(A) = a/b, P(B)=c/d.
    # Let's assume the parameters represent numerators out of some denominator (e.g., 4 for fair coin is standard but here numbers are specific).
    # Alternative: The problem asks to multiply two fractions derived from these integers. 
    # Common pattern: Fraction(p1, 6) * Fraction(p2, 5)? Or just p1/total and p2/total?
    # Let's assume the question is about multiplying probabilities where P(E1)=p1/4 (if binary?) No, let's look at numbers. 
    # If we treat them as numerators of fractions with denominator equal to their max+1 or a fixed 6/5?
    # Most logical math problem: Calculate product of two independent events defined by these integers over some standard denominators OR just multiply p1 and p2 if they are already probabilities. 
    # But "fraction" implies non-integers usually. 
    # Let's assume the question is: What is P(A) * P(B) where A has prob 3/6 (if p=3?) No, we picked random from [2,6].
    # Hypothesis: The integers are numerators of fractions with denominator equal to their respective max+1? Or maybe just multiply the two chosen numbers as if they were probabilities scaled by some factor. 
    # Let's assume the simplest independent probability fraction task: Multiply p/4 and q/5? No, let's stick to the most robust interpretation for "level 1":
    # Assume P(A) = sampled_p / 6 (since max is 6?) and P(B) = sampled_q / 5. 
    # Or maybe just multiply two fractions: p1/something * p2/other. 
    # Let's assume the question text implies multiplying two independent events with probabilities defined by these integers over denominators that make them valid probs (e.g., if integer is k, prob is k/N).
    # Given no N specified, let's assume standard dice-like or binary? No, 6 and 5 suggest d6 and d5. 
    # So P(A) = p1/6, P(B) = q/5. 
    # Product = (p1 * q) / (30).
    
    total_denom = 6 * 5
    
    num_val = sampled_p * sampled_q
    
    gcd_val = math.gcd(num_val, total_denom)
    final_num = num_val // gcd_val
    final_denom = total_denom // gcd_val
    
    question_text = r"Let $A$ and $B$ be independent events. The probability of event $A$ is $\frac{p_1}{6}$ where $p_1 \in [2, 6]$, and the probability of event $B$ is $\frac{q}{5}$ where $q \in [1, 5]$. If we define a new event $C = A \cap B$, what is the canonical irreducible fraction representing $P(C)$?"
    
    correct_answer = {
        "numerator": final_num,
        "denominator": final_denom,
        "canonical_latex": f"${\\frac{{{final_num}}}{{{final_denom}}}$}"
    }
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }

import math