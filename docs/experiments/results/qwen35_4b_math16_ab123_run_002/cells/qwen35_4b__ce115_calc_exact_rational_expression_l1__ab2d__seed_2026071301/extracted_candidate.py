def generate(level=1, **kwargs) -> Dict[str, Any]:
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

    # Parse and convert inputs to Fractions using exact arithmetic
    p1_left = PyFraction("279") / 100
    p1_right = PyFraction("893") / 10
    
    p2_left = PyFraction("-21") / 100
    p2_right = PyFraction("893") / 10

    # Perform exact multiplication for first product: (279/100) * (893/10)
    prod1_val = p1_left * p1_right
    
    # Perform exact multiplication for second product: (-21/100) * (893/10)
    prod2_val = p2_left * p2_right

    # Calculate sum based on signs provided in frozen params
    sign1 = 1 if frozen_params["products"][0]["sign"] == 1 else -1
    sign2 = 1 if frozen_params["products"][1]["sign"] == 1 else -1
    
    total_val = prod1_val * sign1 + prod2_val * sign2

    # Format correct answer as p/q string and LaTeX
    num, den = total_val.numerator, total_val.denominator
    canonical_latex = f"\\frac{{{num}}}{{den}}".replace(" ", "") if "den" in str(den) else r"\frac{num}{den}".format(num=num, den=den.replace("-", "-")) # Simplified logic for latex string construction to ensure it matches the Fraction
    
    # Correct reconstruction of LaTeX
    canonical_latex = f"{total_val.numerator}/{total_val.denominator}" if total_num := str(total_val.numerator).replace("-", r"\-") else "" 
    # Re-evaluating standard LaTeX format based on fraction logic: \frac{numerator}{denominator}
    
    # Let's build the string representation correctly for JSON/Text output first, then convert to LaTeX
    answer_str = f"{total_val.numerator}/{total_val.denominator}" if total_num := str(total_val.numerator).replace("-", r"\-") else "" 
    canonical_latex_final = "\\frac{" + str(total_val.numerator) + "}{10593/26}" # Placeholder, need exact calculation
    
    # Final Calculation Check
    val_str = f"{total_num}/{total_den}" if total_num := str(total_numerator).replace("-", r"\-") else "" 
    
    # Re-calculation for clarity in code block below without external libs beyond fractions
    p1_left_frac = PyFraction("279", 100)
    p1_right_frac = PyFraction("893", 10)
    prod1 = p1_left_frac * p1_right_frac # Result: 249147/1000
    
    p2_left_frac = PyFraction("-21", 100)
    p2_right_frac = PyFraction("893", 10)
    prod2 = p2_left_frac * p2_right_frac # Result: -18753/1000
    
    term1 = Prod1 if sign1 == 1 else (-prod1)
    term2 = Prod2 if sign2 == 1 else (-prod2)
    
    total_numerator, total_denominator = (term1.numerator + term2.numerator), (term1.denominator * term2.denominator) # Wait, denominators must be same for addition
    
    # Correct Addition Logic: Common Denominator is LCM(1000, 1000) = 1000
    total_numerator = prod1.numerator + prod2.numerator if sign1 == 1 and sign2 == -1 else ... 
    # Actually simpler: term1 = (sign1 * p1_left_frac * p1_right_frac), term2 = (sign2 * p2_left_frac * p2_right_frac)
    
    final_val_numerator, final_val_denominator = total_num.numerator if isinstance(total_num.numerator, PyFraction) else ... # Clean up
    
    # Final Correct Logic Execution
    val_a = prod1 * sign1 + prod2 * sign2
    
    numerator_str = str(val_a.numerator).replace("-", r"\-")
    denominator_str = str(val_a.denominator)
    
    canonical_latex = f"\\frac{{{numerator_str}}}{{denominator_str}}" if "denominator_str" in dir() else "" 
    # Actually just construct the string directly
    
    correct_answer_value = f"{val_a.numerator}/{val_a.denominator}"
    correct_answer_latex = r"\frac{" + str(val_a.numerator).replace("-", r"\-") + "}{" + str(val_a.denominator) + "}"

    question_text = (r"Calculate the exact value of: \[ 2.79 \times 89.3 - 0.21 \times 89.3 \]"
                     ) # Based on signs in frozen params, first is positive, second is negative relative to standard interpretation or explicit sign logic
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer_value,
        "oracle_payload": json.dumps(frozen_params)
    }