from core.prompts.domain_function_library import FractionOps
import re

def generate(level=1, **kwargs):
    expression = kwargs.get("expression", "9/22 + 11/18 - (23/22 - 7/18)")
    
    match = re.match(r"(\d+)/(\d+)\s*\+\s*(\d+)/(\d+)\s*-\s*\(\s*(\d+)/(\d+)\s*-\s*(\d+)/(\d+)\s*\)", expression)
    if match:
        nums = [int(x) for x in match.groups()]
        a = FractionOps.create(f"{nums[0]}/{nums[1]}")
        b = FractionOps.create(f"{nums[2]}/{nums[3]}")
        minus_c = FractionOps.create(f"-{nums[4]}/{nums[5]}")
        d = FractionOps.create(f"{nums[6]}/{nums[7]}")
        
        a_plus_b = FractionOps.add(a, b)
        minus_c_plus_d = FractionOps.add(minus_c, d)
        result = FractionOps.add(a_plus_b, minus_c_plus_d)
        
        latex_expr = f"\\frac{{{nums[0]}}}{{{nums[1]}}} + \\frac{{{nums[2]}}}{{{nums[3]}}} - \\left(\\frac{{{nums[4]}}}{{{nums[5]}}} - \\frac{{{nums[6]}}}{{{nums[7]}}}\\right)"
    else:
        result = FractionOps.create("4/11")
        latex_expr = "\\frac{9}{22} + \\frac{11}{18} - \\left(\\frac{23}{22} - \\frac{7}{18}\\right)"
        
    question_text = f"Evaluate the following expression:\n\n\\[\n{latex_expr}\n\\]\n\nProvide your answer as an irreducible fraction."
    
    numerator = result.numerator
    denominator = result.denominator
    canonical_latex = FractionOps.to_latex(result)
    
    correct_answer = {
        "numerator": numerator,
        "denominator": denominator,
        "canonical_latex": canonical_latex
    }
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": {
            "expression": expression
        }
    }