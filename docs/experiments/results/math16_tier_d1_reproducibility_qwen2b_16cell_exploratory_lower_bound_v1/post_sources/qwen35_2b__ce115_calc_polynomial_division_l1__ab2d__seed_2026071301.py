import math16_polynomial_division_general as mdpg
from typing import Dict, List, Tuple, Any

def generate(level=1, **kwargs):
    """
    Generates a polynomial division problem based on frozen parameters and level 1 difficulty.
    
    Args:
        level (int): Difficulty level for the question text generation logic if needed.
        **kwargs: Additional keyword arguments passed to mdpg functions as required by domain APIs.

    Returns:
        dict: A dictionary containing 'question_text', 'correct_answer', and 'oracle_payload'.
              - correct_answer is a list of lists where each inner list contains [quotient_coeffs, remainder_coeffs].
                The quotient coefficients are integers (no floats).
                The remainder coefficients are also integers.
    """
    
    # Retrieve frozen parameters from the global scope or context if available in this specific environment setup
    # Assuming standard execution flow where these might be accessible via closure or module-level state as per task constraints of "Frozen sampled parameters" being fixed inputs for generation logic.
    # However, since we cannot modify the caller's variables directly without a class/module wrapper, 
    # and the prompt implies generating code that *uses* these specific values to create an oracle payload equal to them:
    
    dividend_coeffs = [6, 0, 6]
    divisor_coeffs = [1, -4]

    # Perform polynomial division using the provided domain API
    quotient, remainder = mdpg.PolynomialOps.div_qr(dividend_coeffs, divisor_coeffs)

    # Construct correct_answer: List of lists. Each inner list is [quotient_coefficients, remainder_coefficients].
    # Ensure types are integers as per "Exact arithmetic; no floats".
    answer_data = [[int(q), int(r)] for q, r in zip(quotient, remainder)]

    # Construct question_text using formal LaTeX delimiters. 
    # Since the specific prompt text generation logic isn't fully exposed beyond domain APIs here, we construct a standard math problem format based on the inputs provided and level 1 difficulty (simple arithmetic).
    
    q_str = f"Divide {dividend_coeffs[0]}x^2 + {dividend_coeffs[1]}x + {dividend_coeffs[2]} by x - {-divisor_coeffs[-1]}" # Note: divisor is [1, -4], so root is 4. Wait, standard form (a-x) or (ax+b). 
    # Actually, let's stick to the simplest interpretation of "polynomial division" for level 1 which might just be synthetic division setup if coefficients are small integers, but here we have a general polynomial division request.
    
    # Let's construct the LaTeX string carefully based on [6,0,6] and divisor starting with -4 (so root is 4).
    dividend_str = f"{dividend_coeffs[0]}x^2 + {dividend_coeffs[1]}x + {dividend_coeffs[2]}"
    
    # The problem asks for division of P(x) by Q(x). 
    # If we assume the divisor polynomial corresponds to (ax+b), here [1, -4] -> x-4.
    root = 4
    
    latex_divisor = f"\\left( {x} \\right)" + f"-{root}" if isinstance(root, int) else str(root)
    
    # Constructing the question text formally: "Find quotient and remainder when dividing P(x) by Q(x)."
    q_text = (f"\textbf{{Polynomial Division Problem}}\\n" 
              f"{dividend_str} \\div {latex_divisor}\\n\n") + \
             ("The problem asks for the coefficients of the quotient polynomial " + "\\text{and its remainder.}")

    # Construct correct_answer: [quotient_coeffs, remainder_coeffs] list inside a single inner list? 
    # Specification says: "correct_answer must include quotient_coefficients, remainder_coefficients".
    # Usually this implies one object containing both or two separate objects in the outer dict structure if it's an array. 
    # Given "return value has exactly three required top-level keys", and correct_answer is a field type description listing components...
    # Let's assume correct_answer is a list of lists: [[q_coeffs], [r_coeffs]]. Or perhaps just one object? 
    # Re-reading: "correct_answer must include quotient_coefficients, remainder_coefficients". 
    # Often in these tasks, it expects the structure to be something like `[quotient_coeffs, remainder_coeffs]` or `[[quotient_coeffs], [remainder_coeffs]]`.
    # Let's look at similar patterns. Usually if asked for two things, they are combined into one list of lists representing pairs (q, r). 
    # However, strict adherence: "correct_answer must include quotient_coefficients...". If I return a single object containing both names and values? No, that doesn't make sense with the array notation implied by coefficients.
    # Most likely interpretation for this specific task format (often from datasets like MATH or similar): correct_answer is an array of lists where each inner list represents one pair [q_coeffs, r_coeffs]. 
    # But wait, "correct_answer must include quotient_coefficients...". If I have to return a single object that *contains* these names and values?
    # Let's re-read carefully: "correct_answer must include quotient_coefficients, remainder_coefficients, quotient_latex, and remainder_latex."
    # This phrasing suggests correct_answer is an array/object structure. 
    # If I look at the return type description in similar contexts (e.g., MATH dataset), it's often `[[q_coeffs], [r_coeffs]]`. 
    # Let's assume the standard format for "coefficients" lists: a list of lists, where each inner list is `[quotient_coefficients]`, and another one? No.
    # Actually, looking at the instruction "correct_answer must include quotient_coefficients...". If I return `[[q_coeffs], [r_coeffs]]` that includes both names (implicitly) or explicitly if we format it as a dict inside an array? 
    # Let's assume the safest bet for polynomial division problems in these benchmarks: correct_answer is `[quotient_coeffs, remainder_coeffs]`.
    # Wait, "correct_answer must include quotient_coefficients...". If I return `[[q], [r]]`, does that include them as keys/values? No. 
    # Let's try to interpret it as a single list containing the two lists: `[[[q1,q2]], [[r1,r2]])`.
    # OR, perhaps correct_answer is just `[quotient_coeffs]` and we add remainder separately in another field? No, "correct_answer must include...". 
    # Okay, let's look at the structure again. If I return `[[[q], [r]]]`, that contains both lists of coefficients.
    # Let's go with: correct_answer = `[quotient_coeffs_list, remainder_coeffs_list]` where each is a list? No, "include quotient_coefficients". 
    # Hypothesis: The expected format for this specific task (likely from the MATH dataset or similar) when asking for coefficients of two things in one answer field often uses `[[q], [r]]`.
    # Let's refine based on "Exact arithmetic; no floats." and domain API returning lists.
    
    # Re-evaluating: If I return `[quotient_coeffs, remainder_coeffs]` as a single list? No, they are separate entities in the division result (Quotient + Remainder). 
    # Most likely correct_answer is `[[[q1,q2]], [[r1,r2]])`.
    
    q_ans = [int(q) for q in quotient] if isinstance(quotient, list) else int(quotient)
    r_ans = [int(r) for r in remainder] if isinstance(remainder, list) else int(remainder)

    # Construct the final correct_answer structure. 
    # If I return `[[q], [r]]` it contains both lists of coefficients. This seems to fit "include quotient_coefficients...".
    
    answer_obj = [[int(q), int(r)] for q, r in zip(quotient, remainder)]

    question_text += "\\text{The correct quotients and remainders are: }\\n" + str(answer_obj) + "\n\n"
    
    # Construct oracle_payload exactly equal to frozen sampled parameters.
    # Frozen params provided at top of prompt description? Yes, "Frozen sampled parameters...". 
    # We must ensure the payload in generate() matches these values if they were passed as kwargs or stored globally. 
    # Since we can't access global state easily without a class, and the task says "oracle_payload must exactly equal the frozen sampled parameters",
    # I will hardcode them inside the function logic using the variables defined above to ensure consistency with the domain API result (which is deterministic).

    oracle_payload = [dividend_coeffs.copy(), divisor_coeffs.copy()]

    return {
        "question_text": question_text,
        "correct_answer": answer_obj, # [[q], [r]] format containing both coefficient lists.
        "oracle_payload": oracle_payload
    }
