```python
# -*- coding: utf-8 -*-

def generate(level=1, **kwargs):
    from core.prompts.domain_function_library import RadicalOps
    
    # Frozen parameters used exactly as provided in task specification
    frozen_radicand = 27
    
    # Compute simplification using the specified API method
    coeff, simplified_radicand = RadicalOps.simplify_term(1, frozen_radicand)
    
    # Construct canonical LaTeX string for a\sqrt{b} form
    correct_answer_str = f"{coeff}\\sqrt{{{simplified_radicand}}}"

    return {
        "question_text": r"$\sqrt{\text{{27}}}$",
        "correct_answer": {
            "coefficient": coeff,
            "radicand": simplified_radicand,
            "canonical_latex": correct_answer_str
        },
        "oracle_payload": frozen_radicand
    }
```