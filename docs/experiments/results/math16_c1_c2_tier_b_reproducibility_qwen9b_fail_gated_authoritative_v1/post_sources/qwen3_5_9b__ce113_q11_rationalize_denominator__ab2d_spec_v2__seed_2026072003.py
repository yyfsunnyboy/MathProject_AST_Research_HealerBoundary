# -*- coding: utf-8 -*-

def generate(level=1, **kwargs):
    # Frozen sampled parameters as per specification
    denominator_str = "4-sqrt(7)"
    numerator_int = 9
    radicand_int = 7
    
    # Rationalize the denominator of numerator / (a - sqrt(b))
    # Formula: n / (A - S) = n * (A + S) / ((A)^2 - b) where S = sqrt(b)
    A = 4
    B = radicand_int  # The term under radical is sqrt(B), so denominator becomes A^2 - B
    
    numerator_val = numerator_int
    conjugate_A = A
    conjugate_B = radicand_int
    
    # Calculate new denominator: A^2 - b
    new_denominator = (A ** 2) - conjugate_B
    
    # Numerator after rationalization: n * (A + sqrt(b))
    # We need the sum of coefficients in the form a + b*sqrt(7) for the final fraction? 
    # Wait, standard interpretation: The result is usually expressed as P/Q.
    # However, the task asks to identify integers 'a' and 'b' in "the result".
    # Let's re-read carefully: "Identify the integers a and b in the result a + b\sqrt{7}."
    # This implies the final answer is expected to be an integer sum of coefficients? 
    # Or perhaps the fraction simplifies such that we look at numerator components over denominator?
    
    # Let's compute the exact rationalized form: (9 * (4 + sqrt(7))) / 3
    # Denominator = 16 - 7 = 9.
    # Numerator = 9 * (4 + sqrt(7)) = 36 + 9*sqrt(7).
    # Fraction = (36 + 9*sqrt(7)) / 9 = 4 + sqrt(7).
    
    # So the result is exactly 4 + 1*sqrt(7).
    # Here, coefficient of rational part 'a' = 4.
    # Coefficient of radical part 'b' = 1.
    # The task asks for "correct_answer" as a single exact integer: sum(a+b) or just the value?
    # Task spec says: "Return the integer value of a + b." (from Final Check section).
    
    term_rational_part = numerator_val * conjugate_A // new_denominator  # Integer division if divisible, else float logic needed. 
    # Actually, let's do exact arithmetic first.
    
    num_total_const = numerator_val * A
    num_total_radical_coeff = numerator_val
    
    final_num_const = num_total_const / new_denominator
    final_num_radical_coef = num_total_radical_coeff / new_denominator
    
    # Since we know mathematically it simplifies to integers here:
    a_int = int(final_num_const)
    b_int = int(final_num_radical_coef)
    
    correct_answer_val = a_int + b_int
    
    question_text = r"Rationalize the denominator of \frac{%d}{%s} and express the result in the form $a+b\sqrt{b}$, where $a$ and $b$ are integers. What is the value of $a+b$?" % (numerator_int, denominator_str)
    
    # Wait, LaTeX formatting for sqrt(7). The string was "4-sqrt(7)". 
    # In LaTeX: 4-\sqrt{7}
    question_text = r"Rationalize the denominator of \frac{%d}{%s}. Express the result in simplest form as $a+b\sqrt{b}$ where possible, or simply evaluate. Specifically for this case, find integers a and b such that the simplified expression equals $a + 1\cdot\sqrt{7}$. What is $a+b$?" % (numerator_int, "4-\sqrt{7}")
    
    # Let's refine question_text to be precise based on the specific numbers.
    # Numerator: 9, Denom: 4-sqrt(7). Result: 4 + sqrt(7). a=4, b_coefficient_of_sqrt_is_1? 
    # The prompt says "integers a and b in the result a + b\sqrt{7}". 
    # Usually this means coefficient of sqrt is 'b'. But here radicand is fixed at 7.
    # So form is x + y*sqrt(7). Then answer is x+y? Or maybe the variable name collision "b" refers to the coeff and also the radicand in text description confusingly?
    # Task spec: "Identify the integers a and b in the result a + b\sqrt{7}." 
    # And frozen params have "radicand": 7. So it's definitely x + y*sqrt(7).
    # My calculation gave 4 + sqrt(7). So a=4, coeff_of_sqrt = 1. Sum = 5? Or is 'b' the radicand (7)? 
    # If b in "a+b\sqrt{7}" refers to the coefficient, then sum is 4+1=5.
    # But wait, standard notation $a + b\sqrt{n}$ usually implies n is fixed or part of context.
    # Given frozen param radicand: 7. The form is likely a + c*sqrt(7). 
    # If the text says "integers a and b in ... a+b\sqrt{7}", then 'b' must be the coefficient.
    
    correct_answer = str(correct_answer_val)

    oracle_payload = {
        "denominator": denominator_str,
        "numerator": numerator_int,
        "radicand": radicand_int
    }

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }