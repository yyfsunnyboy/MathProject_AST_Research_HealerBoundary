def generate(level=1, **kwargs):
    expression = "3/7 - (-1/4)"
    
    # Calculate 3/7 + 1/4
    common_denominator = 28
    
    numerator_3_over_7 = (3 * 4)  # 12
    denominator_part_one = 4      # part of first fraction: 12/28
    
    numerator_minus1_over_4_negated = (-(-1)) * 7  # 7
    denominator_part_two = 7       # part of second fraction: 7/28
    
    total_numerator = (numerator_3_over_7 + numerator_minus1_over_4_negated)  # 19
    total_denominator = common_denominator  # 28

    question_text = r"\text{Calculate } \frac{3}{7} - \left(-\frac{1}{4}\right)."
    
    correct_answer = {
        "numerator": 19,
        "denominator": 28,
        "canonical_latex": "\\frac{19}{28}"
    }

    oracle_payload = {"expression": expression}
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }