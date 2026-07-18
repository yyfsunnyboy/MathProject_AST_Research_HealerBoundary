from core.prompts.domain_function_library import FractionOps

def generate(level=1, **kwargs):
    expression = "(5*x**2 - 2*x) - (4 - 3*x)"
    
    # Calculate coefficients using FractionOps
    c2 = FractionOps.create(5)
    c1 = FractionOps.add(FractionOps.create(-2), FractionOps.create(3))
    c0 = FractionOps.create(-4)
    
    def to_val(f):
        if f.denominator == 1:
            return int(f.numerator)
        return f"{f.numerator}/{f.denominator}"
        
    correct_answer = {
        "2": to_val(c2),
        "1": to_val(c1),
        "0": to_val(c0)
    }
    
    question_text = f"Simplify the expression:\n{expression}"
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": {
            "expression": expression
        }
    }