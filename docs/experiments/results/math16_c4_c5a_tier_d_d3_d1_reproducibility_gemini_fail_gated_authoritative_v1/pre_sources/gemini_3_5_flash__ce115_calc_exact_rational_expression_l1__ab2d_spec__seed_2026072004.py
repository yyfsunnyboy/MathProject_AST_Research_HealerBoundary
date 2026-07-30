# -*- coding: utf-8 -*-

try:
    from core.prompts.domain_function_library import FractionOps
except ImportError:
    from fractions import Fraction
    class FractionOps:
        @staticmethod
        def create(val):
            return Fraction(str(val))
        @staticmethod
        def add(a, b):
            return a + b
        @staticmethod
        def sub(a, b):
            return a - b
        @staticmethod
        def mul(a, b):
            return a * b
        @staticmethod
        def div(a, b):
            return a / b

def generate(level=1, **kwargs):
    # Frozen sampled parameters
    oracle_payload = {
        "products": [
            {"left": "2.79", "right": "89.3", "sign": 1},
            {"left": "-0.21", "right": "89.3", "sign": -1}
        ]
    }
    
    products = oracle_payload["products"]
    
    # Compute the exact result using FractionOps
    p1_left = FractionOps.create(products[0]["left"])
    p1_right = FractionOps.create(products[0]["right"])
    p1 = FractionOps.mul(p1_left, p1_right)
    if products[0]["sign"] == -1:
        p1 = -p1
        
    p2_left = FractionOps.create(products[1]["left"])
    p2_right = FractionOps.create(products[1]["right"])
    p2 = FractionOps.mul(p2_left, p2_right)
    if products[1]["sign"] == -1:
        p2 = -p2
        
    result = p1 + p2
    
    num = result.numerator
    den = result.denominator
    val_str = f"{num}/{den}" if den != 1 else f"{num}"
    latex_str = f"\\frac{{{num}}}{{{den}}}" if den != 1 else f"{num}"
    
    correct_answer = {
        "value": val_str,
        "numerator": num,
        "denominator": den,
        "canonical_latex": latex_str
    }
    
    # Construct question text
    terms = []
    for i, prod in enumerate(products):
        left = prod["left"]
        right = prod["right"]
        sign = prod["sign"]
        
        # Format left
        if float(left) < 0:
            left_str = f"({left})"
        else:
            left_str = left
            
        # Format right
        if float(right) < 0:
            right_str = f"({right})"
        else:
            right_str = right
            
        term_str = f"{left_str} \\times {right_str}"
        
        if i == 0:
            if sign == -1:
                terms.append(f"-{term_str}")
            else:
                terms.append(term_str)
        else:
            if sign == -1:
                terms.append(f"- {term_str}")
            else:
                terms.append(f"+ {term_str}")
                
    expr_latex = " ".join(terms)
    question_text = f"Calculate the exact value of the expression: \\({expr_latex}\\)."
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload,
    }