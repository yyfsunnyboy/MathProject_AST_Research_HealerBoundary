from core.prompts.domain_function_library import RadicalOps, Fraction

def generate(level=1, **kwargs):
    # Step 1: Solve (x-2)^2 = 3 for roots a and b where a > b
    # x - 2 = ±√3 => x = 2 + √3 or x = 2 - √3
    # Root a = 2 + √3, Root b = 2 - √3
    
    term_a_raw = {"rational": 2, "radical_coefficient": 1, "radicand": 3}
    term_b_raw = {"rational": 2, "radical_coefficient": -1, "radicand": 3}

    # Ensure a > b (larger root first)
    if term_a_raw["radical_coefficient"] < term_b_raw["radical_coefficient"]:
        term_a_raw, term_b_raw = term_b_raw, term_a_raw
    
    # Step 2: Compute target expression 2a + b
    # Scale a by 2 then add b
    scaled_term_a = RadicalOps.scale_linear_radical(term_a_raw, 2)
    
    result_terms = [scaled_term_a, term_b_raw]

    # Normalize and combine terms (simplify like radicals if any, though here radicands match so they are already combined type)
    normalized_list = RadicalOps.normalize_term_list(result_terms)
    
    # The expression is 2a + b. Since a has radical_coefficient=1 and b has -1, 
    # we need to add them properly. However, the problem asks for exact form of 2a+b.
    # Let's compute sum directly using add_linear_radicals on scaled_a and term_b
    
    final_result_term = RadicalOps.add_linear_radicals(scaled_term_a, term_b_raw)

    # Step 3: Format result if needed (though contract requires specific keys)
    
    # Extract components for correct_answer structure
    rational_part = final_result_term["rational"]
    radical_coefficient = final_result_term["radical_coefficient"]
    radicand = final_result_term["radicand"]

    canonical_latex = RadicalOps.format_linear_radical(final_result_term)

    # Step 4: Assemble correct_answer according to contract
    correct_answer_structure = {
        "result": {
            "rational": rational_part,
            "radical_coefficient": radical_coefficient,
            "radicand": radicand,
            "canonical_latex": canonical_latex
        }
    }

    return {
        "question_text": kwargs.get("stem", ""), # Using frozen description as stem if provided in context or empty string based on instruction to use frozen_params directly? 
                                                # Instruction says: "use as question_text" for the equation block.
                                                # But looking at generic example, it uses 'example stem'.
                                                # The prompt says: "Frozen task description (use as question_text)".
        "correct_answer": correct_answer_structure,
        "oracle_payload": kwargs.get("frozen_params", {}) 
    }

# Correction based on specific instructions for this run:
# 1. Use the frozen parameters provided in the block to construct the payload and stem if available or just use the equation text as question_text per instruction "use as question_text".
# The prompt says: "Frozen task description (use as question_text)". 
# So we will extract the math string from the markdown source for question_text.

def generate(level=1, **kwargs):
    # Re-implementation to strictly follow instructions with correct stem extraction
    
    frozen_params = kwargs.get("frozen_params", {})
    
    # The equation is (x-2)^2=3
    # Roots: x = 2 + sqrt(3), x = 2 - sqrt(3)
    # a > b => a = 2 + sqrt(3), b = 2 - sqrt(3)
    # Target: 2a + b
    
    term_a = {"rational": 2, "radical_coefficient": 1, "radicand": 3}
    term_b = {"rational": 2, "radical_coefficient": -1, "radicand": 3}

    # Ensure a > b (already true: 1 > -1)
    
    scaled_a = RadicalOps.scale_linear_radical(term_a, 2)
    result_term = RadicalOps.add_linear_radicals(scaled_a, term_b)
    
    rational_val = result_term["rational"]
    radical_coeff = result_term["radical_coefficient"]
    radicand_val = result_term["radicand"]
    
    latex_str = RadicalOps.format_linear_radical(result_term)

    correct_answer_obj = {
        "result": {
            "rational": rational_val,
            "radical_coefficient": radical_coeff,
            "radicand": radicand_val,
            "canonical_latex": latex_str
        }
    }

    # Question text should be the provided equation description. 
    # Since we cannot read markdown outside source code directly in a way that parses LaTeX perfectly without external libs,
    # and the instruction says "use as question_text", I will construct it from the frozen_params context or use a standard representation if not fully available via API.
    # However, looking at the allowed ops, there is no direct 'parse_latex' to string converter other than format_expression which needs terms dict.
    # The instruction says "Frozen task description (use as question_text)". 
    # I will assume the user expects me to output a reasonable text representation or use the equation components if possible.
    # But since `question_text` is just a string, and we have no API to convert LaTeX back to string easily without format_expression which needs terms...
    # Wait, `format_linear_radical` only formats one term. 
    # The full question text in Chinese: "一元二次方程式 (x-2)^2=3 的兩根為 a,b，且 a>b。求 2a+b，答案須保持精確根式形式。"
    # I will hardcode the stem as per instruction "use as question_text". The prompt provides it explicitly.

    return {
        "question_text": "一元二次方程式 (x-2)^2=3 的兩根為 a,b，且 a>b。求 2a+b，答案須保持精確根式形式。",
        "correct_answer": correct_answer_obj,
        "oracle_payload": frozen_params
    }

# Final check on logic:
# (x-2)^2 = 3 => x^2 - 4x + 4 = 3 => x^2 - 4x + 1 = 0.
# Roots are [2 ± sqrt(3)]. 
# a = 2+sqrt(3), b=2-sqrt(3).
# 2a+b = 2*(2+sqrt(3)) + (2-sqrt(3)) = 4 + 2*sqrt(3) + 2 - sqrt(3) = 6 + sqrt(3).
# Rational part: 6, Radical coeff: 1, Radicand: 3.
# My code logic: 
# term_a (rational=2, coef=1), scaled by 2 -> rational=4, coef=2.
# add term_b (rational=2, coef=-1).
# Sum rational: 4+2 = 6.
# Sum radical coeff: 2 + (-1) = 1.
# Result: 6 + sqrt(3). Correct.

