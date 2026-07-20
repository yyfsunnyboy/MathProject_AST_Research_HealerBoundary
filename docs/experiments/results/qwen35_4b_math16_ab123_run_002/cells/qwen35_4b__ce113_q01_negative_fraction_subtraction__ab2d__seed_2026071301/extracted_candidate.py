import json
from fractions import Fraction as PythonFraction
# Simulating the required domain APIs since they are not in standard library
class MockDomainOps:
    @staticmethod
    def create(value):
        return PythonFraction(value) if isinstance(value, (int, float)) else value
    
    @staticmethod
    def sub(a, b):
        # Ensure inputs are treated as fractions for precision
        a = PythonFraction(str(a).split('/')[0]) / PythonFraction(str(a).split('/')[1]) if '/' in str(a) else PythonFraction(float(a))
        b = PythonFraction(str(b).split('/')[0]) / PythonFraction(str(b).split('/')[1]) if '/' in str(b) else PythonFraction(float(b))
        return a - b
    
    @staticmethod
    def to_latex(val, mixed=False):
        frac_val = PythonFraction(str(val).replace('/', '').strip())
        num = frac_val.numerator
        den = frac_val.denominator
        if den == 1:
            latex = f"{num}"
        else:
            # Ensure irreducible (Python Fraction handles this automatically)
            latex = rf"\frac{{{int(num)}}}{{int(den)}}"
        return latex

def generate(level=1, **kwargs):
    frozen_params = {"expression": "3/7 - (-1/4)"}
    
    expr_text = frozen_params["expression"]
    
    # Parse the expression manually to handle negative signs correctly for subtraction
    # 3/7 - (-1/4) becomes 3/7 + 1/4
    parts = [x.strip() for x in expr_text.split('-')]
    if len(parts[0].strip().split('/')[0]) == 2 and '-' in parts[1]:
        a_str, b_neg_str = parts[0], parts[1]
        # Remove the negative sign from the second fraction part before parsing
        num_a, den_a = int(a_str.split('/')[0]), int(a_str.split('/')[1])
        neg_part = float(b_neg_str) if '/' in b_neg_str else -float(b_neg_str)
        
        # Construct positive version of B for subtraction: a - (-b) = a + b
        num_b, den_b = abs(int(neg_part.replace('-', ''))), int(neg_part.split('/')[1]) if '/' in str(-neg_part).replace('-','') else 4
        
        # Recalculate using domain APIs on the actual fractions extracted from string logic
        # Direct extraction for this specific frozen case: 3/7 and -(-1/4) -> +1/4
        val_a = MockDomainOps.create("3") / MockDomainOps.create("7")
        
        # Handle "- (-1/4)" which is effectively adding "1/4"
        # The expression is a - b where b is -1/4. So we compute a + 1/4.
        val_b = MockDomainOps.create("-1") / MockDomainOps.create("4") 
        result_frac = MockDomainOps.sub(val_a, val_b)
        
        correct_answer_data = {
            "numerator": int(result_frac.numerator),
            "denominator": int(result_frac.denominator),
            "canonical_latex": f"\\frac{{{int(result_frac.numerator)}}}{{int(result_frac.denominator)}}"
        }

    question_text = rf"\textbf{Problem: Compute the difference.}\n\$\text{Expression: {expr_text}}\$"
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer_data,
        "oracle_payload": frozen_params
    }