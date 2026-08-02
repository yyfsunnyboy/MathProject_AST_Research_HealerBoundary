from core.prompts.domain_function_library import RadicalOps

def generate(level=1, **kwargs):
    # Frozen params
    frozen_params = {
      "equation": "(x-2)^2=3",
      "order": "a>b",
      "target": "2a+b"
    }
    
    # Roots of (x-2)^2 = 3 are 2 + sqrt(3) and 2 - sqrt(3)
    # Since a > b:
    # a = 2 + sqrt(3)
    # b = 2 - sqrt(3)
    a = {"rational": 2, "radical_coefficient": 1, "radicand": 3}
    b = {"rational": 2, "radical_coefficient": -1, "radicand": 3}
    
    # Calculate 2a
    term_2a = RadicalOps.scale_linear_radical(a, 2)
    
    # Calculate 2a + b
    result = RadicalOps.add_linear_radicals(term_2a, b)
    
    # Format the result
    canonical_latex = RadicalOps.format_linear_radical(result)
    
    question_text = "一元二次方程式\n\\[\n(x-2)^2=3\n\\]\n的兩根為 \\(a,b\\)，且 \\(a>b\\)。求 \\(2a+b\\)，答案須保持精確根式形式。"
    
    correct_answer = {
        "result": {
            "rational": RadicalOps.exact_integer(result["rational"]),
            "radical_coefficient": RadicalOps.exact_integer(result["radical_coefficient"]),
            "radicand": RadicalOps.exact_integer(result["radicand"]),
            "canonical_latex": canonical_latex
        }
    }
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": frozen_params
    }