# -*- coding: utf-8 -*-

def generate(level=1, **kwargs):
    # Frozen sampled parameters as per task specification
    radicand = 135
    
    # Compute simplification manually to avoid external dependencies not in standard library or specified imports.
    # Factorize 135: 135 = 27 * 5 = (9*3) * 5? No, 135 = 81 * ? 
    # Let's find the largest perfect square factor of 135.
    # Factors of 135: 1, 3, 5, 9, 15, 27, 45, 135.
    # Squares <= 135: 1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 121.
    # Check divisibility by squares in descending order from largest possible (sqrt(135) ~ 11.6).
    # Try 81: 135 / 81 = not integer.
    # Try 49: no. ... 
    # Try 27? Not a square.
    # Try 9: 135 % 9 == 0 -> 135/9 = 15. So sqrt(135) = sqrt(9*15) = 3*sqrt(15).
    # Is there a larger square factor? 
    # Check factors again. 135 / 27 = 5 (no). 135/45=3(no).
    # Wait, 135 = 9 * 15. Are there other squares?
    # Let's re-evaluate prime factorization: 135 = 3^3 * 5.
    # Square factors come from even powers of primes. We have 3^2 in the mix (from 3^3).
    # So we take out 3^2 = 9. Remaining is 3*5 = 15.
    # Thus, coefficient = sqrt(9) = 3. Radicand = 15.
    
    coeff = 3
    simplified_radicand = 15
    
    # Construct the canonical LaTeX string for a\sqrt{b} form: "a\sqrt{b}"
    question_text = f"Simplify \\sqrt{{{radicand}}}: {coeff}\\sqrt{{{simplified_radicand}}}"
    
    correct_answer = {
        "coefficient": coeff,
        "radicand": simplified_radicand,
        "canonical_latex": f"{coeff}\\sqrt{{{simplified_radicand}}}",
    }

    oracle_payload = {"radicand": radicand}

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload,
    }