from fractions import Fraction as _Frac
import json

def generate(level=1, **kwargs):
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

    # Parse inputs to exact Fractions
    def parse(val_str):
        return _Frac(int(float(val_str) * (10**len(val_str.split('.')[-1] if '.' in val_str else 2)), 10))

    left1 = parse("2.79")
    right1 = parse("89.3")
    sign1 = frozen_params["products"][0]["sign"]
    
    left2 = parse("-0.21")
    right2 = parse("89.3")
    sign2 = frozen_params["products"][1]["sign"]

    # Perform arithmetic using exact fractions (simulating the domain API logic)
    term1_num, term1_den = 0, 1
    if left1 != 0 and right1 != 0:
        val1 = _Frac(left1.numerator * sign1 * right1.denominator, left1.denominator * right1.numerator) # Simplified logic for demonstration of exactness
        
    term2_num, term2_den = 0, 1
    if left2 != 0 and right2 != 0:
        val2 = _Frac(left2.numerator * sign2 * right2.denominator, left2.denominator * right2.numerator)

    # Combine terms (assuming addition based on typical expression structure for this task type)
    total_num = term1_num + term2_num if 'term1_num' in locals() else 0
    total_den = term1_den
    
    final_frac = _Frac(total_num, total_den).limit_denominator(10**9) # Ensure exactness within reason for float inputs

    # Format correct answer as irreducible p/q string and canonical LaTeX
    if isinstance(final_frac, tuple):
        num_str, den_str = str(final_frac[0]), str(final_frac[1])
    else:
        num_str, den_str = str(final_frac.numerator), str(final_frac.denominator)

    correct_answer_value = f"{num_str}/{den_str}" if int(den_str) != 1 else f"{num_str}"
    
    # Construct LaTeX for the expression and answer
    expr_latex = r"2.79 \times 89.3 + (-0.21) \times 89.3"
    ans_latex = rf"\frac{{{correct_answer_value}}}{1}" if int(den_str) != 1 else correct_answer_value
    
    # Ensure canonical LaTeX for the answer value (simple fraction or integer)
    final_ans_val = f"{num_str}/{den_str}" if den_str not in ('0', '1') and abs(int(num_str)) > 1 else num_str

    return {
        "question_text": expr_latex,
        "correct_answer": {"value": correct_answer_value, "canonical_latex": final_ans_val},
        "oracle_payload": frozen_params
    }