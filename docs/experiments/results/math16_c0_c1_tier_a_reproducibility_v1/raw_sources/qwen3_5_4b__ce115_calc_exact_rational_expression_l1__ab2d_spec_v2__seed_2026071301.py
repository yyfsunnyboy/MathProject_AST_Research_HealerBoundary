# -*- coding: utf-8 -*-

from fractions import Fraction


def generate(level=1, **kwargs):
    # Frozen sampled parameters used for this task instance
    frozen_params = {
        "products": [
            {"left": "2.79", "right": "89.3", "sign": 1},
            {"left": "-0.21", "right": "89.3", "sign": -1}
        ]
    }

    # Convert decimal strings to Fractions for exact arithmetic
    f_279 = Fraction("2.79")
    f_893 = Fraction("89.3")
    f_neg021 = Fraction("-0.21")

    # Perform calculations: (2.79 * 89.3) + (-0.21 * -89.3) -> wait, sign logic check
    # Product 1: left=2.79, right=89.3, sign=1 => term = 2.79 * 89.3
    p1_val = f_279 * f_893

    # Product 2: left=-0.21, right=89.3, sign=-1 
    # The 'sign' likely indicates the operation or a multiplier to apply based on context of "rational_arithmetic"
    # Usually in these tasks: term = (left * right) applied with sign logic? Or is it left_op_right + sign*something?
    # Re-reading typical patterns for such datasets: 
    # Often it's sum(left1 * right1, left2 * right2). The 'sign' might be the multiplier for the second term if it was a subtraction in expression generation.
    # Let's assume standard arithmetic expression construction where sign determines addition/subtraction of products or multiplies result by -1.
    # Given "rational_arithmetic", likely: (a * b) + c * d? 
    # Or maybe the 'sign' is part of the second product definition effectively making it (-0.21 * 89.3 * sign)? No, usually expression is A op B.
    # Let's interpret as two terms being summed or subtracted based on signs provided in a list context? 
    # Actually, looking at "products" list: [ {l:a, r:b, s:+}, {l:c, d:e, f:-} ]
    # It implies calculating Term1 = l*r (with sign +) and Term2 = l*d * (-sign)? Or just sum(l*r*s1 + c*e*s2)? 
    # Let's assume the expression is: (left_0 * right_0) - (left_1 * right_1) if signs were operations?
    # But 'sign' is inside product dict. Maybe it means: result = left*right for first, and then apply sign to second term relative to addition? 
    # Most logical interpretation for "exact rational expression": Calculate the sum of products where each product might have a coefficient or operation implied by 'sign'.
    # Let's try: Term1 = 2.79 * 89.3. Term2 = -0.21 * (-89.3) because sign=-1? Or just add (left*right)*sign? 
    # If expression is A + B, and we have two products with signs...
    # Let's assume the task asks to compute: (2.79 * 89.3) - (-0.21 * 89.3)? No that would be adding a positive if second term was negative? 
    # Alternative interpretation common in these specific benchmarks: The expression is formed by combining terms where 'sign' dictates the operation between products or modifies the product value directly before summation.
    # Let's assume standard linear combination: sum( (left_i * right_i) * sign_i ) ? Or maybe just left*right and then add/sub based on global context? 
    # Given "products" list, likely we compute term1 = 2.79 * 89.3 and term2 = -0.21 * (-89.3)? No right is fixed at 89.3 in both.
    # Let's assume the expression is: (2.79)(89.3) + (-0.21)(-89.3). Why? Because sign=-1 on second product might mean "multiply by -1" or it represents a subtraction term which becomes addition of negative? 
    # Actually, simplest exact arithmetic interpretation for such JSON structures in math tasks:
    # Calculate P1 = left0 * right0. Calculate P2 = left1 * (right1 if sign==1 else -right1). Then sum them? Or maybe the expression is simply the algebraic result of these operations combined with a specific operator implied by 'sign'? 
    # Let's go with: Result = (left_0 * right_0) + (left_1 * right_1 * (-1 if sign==-1 else 1))? No, that overcomplicates.
    # Re-evaluating based on "rational_arithmetic": Usually it's a single expression like $a \cdot b - c \cdot d$. 
    # If the list represents terms in an equation: Term1 (sign +) and Term2 (sign -). Maybe Result = P1 - P2?
    # Let's try calculating: val1 = f_279 * f_893. val2 = f_neg021 * f_893. 
    # If sign indicates the operation between products in a sum expression (e.g., A + B), then maybe it means add P1 and subtract P2? Or multiply by sign?
    # Let's assume the most robust interpretation for "exact rational": Compute the algebraic value where signs are applied as multipliers to the product terms before summation. 
    # Expression: (2.79 * 89.3) + (-0.21 * -89.3). Why? Because sign=-1 on second item might imply flipping the right operand or just applying a negative coefficient.
    # Actually, looking at similar tasks online: Often it's `left * right` for first, and then if there is a list of products with signs, it implies an expression like $a \cdot b - c \cdot d$. 
    # But here we have two items in the list. Maybe Result = (2.79 * 89.3) + (-0.21 * 89.3)? And 'sign' is just metadata? No, must use it.
    # Hypothesis: The expression is constructed as sum of products where each product's value is multiplied by its sign. 
    # Term1 = (2.79 * 89.3) * 1. Term2 = (-0.21 * 89.3) * -1? Or just the term itself has a sign attached to it in the expression generation logic which we don't see, but 'sign' tells us how to treat it relative to an addition base? 
    # Let's assume: Result = (f_279 * f_893) + (-0.21 * 89.3). Wait, where is the sign used?
    # Maybe: Result = (f_279 * f_893) - (abs(f_neg021) * abs(f_893))? 
    # Let's try a different angle: The 'sign' field in the product dict likely indicates whether to add or subtract that specific term from zero, OR it modifies the right operand.
    # Given "products": [{"left": ..., "right": ..., "sign": 1}, ...]
    # If we treat this as generating an expression like $2.79 \times 89.3 - (-0.21) \times 89.3$? 
    # Let's calculate: A = 2.79 * 89.3. B = -0.21 * 89.3. If sign=1 means add, sign=-1 means subtract? Then Result = A + (-B)? No.
    # Most likely interpretation for these specific "ce115" tasks: The expression is a sum of terms where each term is `left * right`. The 'sign' indicates the operation between this product and the running total (add or sub). 
    # So, start with 0? Or just combine them. If sign=1 -> add, if sign=-1 -> subtract.
    # Result = (2.79 * 89.3) - (-0.21 * 89.3)? No, that would be adding a negative product which is subtraction of positive. 
    # Let's assume the expression is: $T_1 \text{ op}_1 T_2$. If it's a list of terms to sum with signs?
    # Okay, let's compute: val = (f_279 * f_893) + (-0.21 * 89.3). This ignores the sign field usage which is bad. 
    # Correct logic likely: The expression represents a calculation where we sum products, and 'sign' tells us if it's addition or subtraction of that product from the main value? Or maybe the second term is subtracted because its sign is -1 relative to the first positive one?
    # Let's assume the standard form for such problems: Calculate $A \cdot B + C \cdot D$. If 'sign' was an operator... 
    # Wait, could it be that the expression is simply $(2.79)(89.3) - (-0.21)(-89.3)$? No.
    # Let's try: Result = (f_279 * f_893) + (f_neg021 * f_893). This is just sum of products. The 'sign' might be redundant or I am missing a nuance about how it modifies the right operand? 
    # If sign=-1, maybe right becomes -right? Then term = (-0.21) * (-89.3).
    # Let's try that: Term1 = 2.79 * 89.3. Term2 = -0.21 * (89.3 if s==1 else -89.3). 
    # Then Result = Term1 + Term2? Or just the sum of these modified terms?
    # Let's calculate: T1 = 279/100 * 893/10 = ... T2 = -21/100 * (-893/10) (if sign flips right). 
    # Sum = T1 + T2. This seems like a plausible "exact rational expression" task where signs flip operands based on the list item's property.
    
    term_right_0 = f_893 if frozen_params["products"][0]["sign"] == 1 else -f_893
    p1_val = f_279 * term_right_0
    
    term_right_1 = f_893 if frozen_params["products"][1]["sign"] == 1 else -f_893
    # Note: left is already negative in the input "-0.21". 
    p2_val = f_neg021 * term_right_1
    
    total_sum = p1_val + p2_val

    # Format answer as irreducible fraction string and LaTeX
    num, den = total_sum.numerator, total_sum.denominator
    latex_str = r"\frac{" + str(num) + "}{\text{" + str(den) + "}\n}" if False else f"\\frac{{{num}}}{{den}}" # Wait standard is \frac{a}{b}
    
    correct_latex = rf"\frac{{{total_sum.numerator}}}{{{total_sum.denominator}}}"

    question_text = r"$\text{Calculate the exact value of: } (2.79)(89.3) + (-0.21)\left(\begin{cases} 89.3 & \text{if sign}=1 \\ -89.3 & \text{if sign}=-1 \end{cases}\right)$" # This is too complex for a single line question text usually
    # Let's simplify the question to reflect the computed expression directly based on our logic: 
    # Expression used: (2.79 * 89.3) + (-0.21 * -89.3). Wait, if sign=-1 flips right for second term? 
    # Actually, let's look at the numbers: 2.79*89.3 = 249.147. -0.21*-89.3 = 18.753. Sum = 267.9.
    # What if it was subtraction? 249.147 + (-0.21*89.3) = 249.147 - 18.753 = 230.394. 
    # Let's stick to the logic: sign determines the value of 'right'.
    
    question_text = r"\text{Compute } (2.79 \times 89.3) + (-0.21 \times -89.3)"

    correct_answer_value = f"{total_sum.numerator}/{total_sum.denominator}"

    return {
        "question_text": question_text,
        "correct_answer": {
            "value": correct_answer_value,
            "canonical_latex": r"\frac{" + str(total_sum.numerator) + "}{" + str(total_sum.denominator) + "}"
        },
        "oracle_payload": frozen_params
    }
