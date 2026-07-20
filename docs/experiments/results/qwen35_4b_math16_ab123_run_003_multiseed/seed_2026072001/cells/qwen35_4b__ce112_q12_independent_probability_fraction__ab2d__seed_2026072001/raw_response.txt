import random
from core.prompts.domain_function_library import FractionOps


def generate(level=1, **kwargs):
    p1_min = kwargs.get("p1", [2]) if "p1" not in kwargs else kwargs["p1"][0]
    p1_max = kwargs.get("p1_end", 6) if "p1_end" not in kwargs and len(kwargs.get("p1", [])) > 1 else 5 + (kwargs.get("p1", [])[-1] - 2 if isinstance(kwargs.get("p1"), list) else 0)
    
    p2_min = kwargs.get("p2", [1]) if "p2" not in kwargs else kwargs["p2"][0]
    p2_max = kwargs.get("p2_end", 5) if "p2_end" not in kwargs and len(kwargs.get("p2", [])) > 1 else 4 + (kwargs.get("p2", [])[-1] - 1 if isinstance(kwargs.get("p2"), list) else 0)

    p = FractionOps.create(random.randint(p1_min, p1_max) / random.randint(2, 6))
    q = FractionOps.create(random.randint(p2_min, p2_max) / random.randint(3, 5))

    product_frac = FractionOps.mul(q, p)

    question_text = r"\text{What is the probability of two independent events occurring? The first event has a probability of } $\frac{\text{{numerator}}}{\text{{denominator}}} \cdot \frac{\text{{numerator2}}}{\text{{denominator2}}}$"
    
    num, den = product_frac.numerator, product_frac.denominator
    
    correct_answer = {
        "numerator": str(num),
        "denominator": str(den),
        "canonical_latex": FractionOps.to_latex(product_frac) + r"$$"
    }

    oracle_payload = {"p1": [2, 6], "p2": [1, 5]}

    return {
        "question_text": question_text.format(numerator=str(num), denominator=str(den), numerator2=kwargs.get("numerator", str(product_frac.numerator)), denominator2=kwargs.get("denominator", str(product_frac.denominator))),
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }