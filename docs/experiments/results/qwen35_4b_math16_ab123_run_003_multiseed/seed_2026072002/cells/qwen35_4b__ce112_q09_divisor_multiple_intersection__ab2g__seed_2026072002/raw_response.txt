def generate(level=1, **kwargs):
    divisor_of = kwargs.get("divisor_of", 216)
    multiple_of = kwargs.get("multiple_of", 18)
    
    count = len([x for x in range(1, min(divisor_of, multiple_of)) if (divisor_of % x == 0 or multiple_of % x == 0)])

    return {
        "question_text": r"\text{Find the number of integers strictly less than } \min(\text{216}, \text{18}) \text{ that are either divisors of 216 or multiples of 18.}",
        "correct_answer": {"count": count},
        "oracle_payload": {"divisor_of": divisor_of, "multiple_of": multiple_of}
    }