from core.prompts.domain_function_library import FractionOps

def generate(level=1, **kwargs):
    # Parse operands from frozen_params strings directly into Fractions
    term1 = FractionOps.create("2.79") * 893 / 10   # 2.79 * 89.3 -> (279/100)*(893/10)
    term2_val = FractionOps.create("-0.21") * 893 / 10  # -0.21 * 89.3
    
    # Reconstruct exact calculation using Fractions to avoid float drift before final serialization
    # Term 1: 2.79 * 89.3 = (279/100) * (893/10)
    t1_left = FractionOps.create("2.79")
    t1_right = FractionOps.create("89.3")
    term1_res = FractionOps.mul(t1_left, t1_right)

    # Term 2: -0.21 * 89.3 (sign handled by the negative number or explicit subtraction logic in problem structure)
    # Problem: 2.79*89.3 - (-0.21*89.3) = term1 + abs(term2_part) if we treat inner as positive magnitude then subtract? 
    # Actually expression is A*B - (C*D). C is "-0.21". So it's Term1 - (NegativeNumber * Positive).
    # Let's stick to direct evaluation of the terms inside parentheses first.
    
    t2_left = FractionOps.create("-0.21")
    term2_res = FractionOps.mul(t2_left, t1_right)  # This will be negative
    
    # The expression is: Term1 - (Term2_Res) => Term1 + abs(Term2_Res) if Term2_Res is neg? 
    # Wait, standard order of operations: calculate inside parens first.
    # Inside parens: (-0.21 * 89.3). This results in a negative fraction.
    # Then subtract that result from the first product.
    
    final_result = FractionOps.sub(term1_res, term2_res)

    # Serialize to exact string (int or 'p/q') and LaTeX
    value_str = FractionOps.to_exact(final_result)
    latex_str = FractionOps.to_latex(final_result)

    return {
        "question_text": "精確計算\n\\[ 2.79\times 89.3-(-0.21\times 89.3). \\]\n答案不得使用近似值。",
        "correct_answer": {
            "value": value_str,
            "canonical_latex": latex_str
        },
        "oracle_payload": {
          "products": [
            {
              "left": "2.79",
              "right": "89.3",
              "sign": 1
            },
            {
              "left": "-0.21",
              "right": "89.3",
              "sign": -1
            }
          ]
        }
    }