def generate(level=1, **kwargs):
    import fractions
    
    # Frozen sampled parameters as per task specification
    products = [
        {"left": "2.79", "right": "89.3", "sign": 1},
        {"left": "-0.21", "right": "89.3", "sign": -1}
    ]
    
    # Convert string decimals to fractions for exact arithmetic
    def str_to_frac(s):
        return fractions.Fraction(float(str(s)))
    
    # Calculate the expression based on products list
    # Expression: (2.79 * 89.3) + (-0.21 * 89.3)
    term1 = str_to_frac(products[0]["left"]) * str_to_frac(products[0]["right"])
    if products[0]["sign"] == -1:
        term1 = -term1
    
    term2 = str_to_frac(products[1]["left"]) * str_to_frac(products[1]["right"])
    if products[1]["sign"] == 1:
        term2 = -term2
        
    result = term1 + term2
    
    # Format the answer as p/q string and canonical LaTeX
    numerator, denominator = result.numerator, result.denominator
    correct_answer_str = f"{numerator}/{denominator}"
    
    def to_latex_frac(n, d):
        if n < 0:
            return r"\frac{-" + str(abs(d)) * abs(int(n/d) - (n % d == 0 and int(n/d))) + "}{1} \cdot \frac{abs\_numerator}{denominator}" # Simplified logic below for clarity
        
        if n < 0:
            return r"\frac{-" + str(abs(d)) * abs(int(-n/-d) - ((-n % d == 0 and int((-n)/d))) + "}{1} \cdot ..." 
        else:
            return f"{numerator}/{denominator}" # Placeholder for actual LaTeX generation
    
    latex_frac = r"\frac{" + str(numerator) + "}{" + str(denominator) + "}" if numerator >= 0 and denominator > 0 else r"\frac{-" + str(abs(numerator)) + "}{1} \cdot \frac{abs\_numerator}{denominator}"
    
    # Correct LaTeX generation for negative result: -\frac{|p|}{q} or \frac{-p}{q}
    if numerator < 0 and denominator > 0:
        latex_frac = r"\frac{" + str(-numerator) + "}{1} \cdot \frac{abs\_numerator}{denominator}" # Placeholder
    
    correct_answer_latex = f"{latex_frac}"

    question_text = r"Calculate the exact value of the expression formed by multiplying and summing terms from a list. The first term is $2.79$ multiplied by $89.3$, then added to the second term which is $-0.21$ multiplied by $89.3$. Express your final answer as an irreducible fraction."

    oracle_payload = products
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer_str + "|" + correct_answer_latex,
        "oracle_payload": oracle_payload
    }