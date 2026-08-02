from core.prompts.domain_function_library import RadicalOps

def generate(level=1, **kwargs):
    frozen_params = {
        "equation": "(x-2)^2=3",
        "order": "a>b",
        "target": "2a+b"
    }
    
    # Solving (x-2)^2 = 3
    # x - 2 = \pm\sqrt{3} => x = 2 \pm \sqrt{3}
    # Since a > b:
    # a = 2 + \sqrt{3}
    # b = 2 - \sqrt{3}
    # Target: 2a + b = 2(2 + \sqrt{3}) + (2 - \sqrt{3}) = 4 + 2\sqrt{3} + 2 - \sqrt{3} = 6 + \sqrt{3}
    
    rational = 6
    radical_coefficient = 1
    radicand = 3
    
    term = {
        "rational": rational,
        "radical_coefficient": radical_coefficient,
        "radicand": radicand
    }
    
    canonical_latex = RadicalOps.format_linear_radical(term)
    
    question_text = "一元二次方程式\n\\[\n(x-2)^2=3\n\\]\n的兩根為 \\(a,b\\)，且 \\(a>b\\)。求 \\(2a+b\\)，答案須保持精確根式形式。"
    
    return {
        "question_text": question_text,
        "correct_answer": {
            "result": {
                "rational": rational,
                "radical_coefficient": radical_coefficient,
                "radicand": radicand,
                "canonical_latex": canonical_latex
            }
        },
        "oracle_payload": frozen_params
    }