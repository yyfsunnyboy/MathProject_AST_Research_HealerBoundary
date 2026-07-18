import json
from fractions import Fraction as F
from typing import Dict, Any


def generate(level=1, **kwargs):
    expression = "9/(4 - sqrt(7))"
    
    # Rationalize denominator: multiply numerator and denominator by (4 + sqrt(7))
    # Denominator becomes 4^2 - (sqrt(7))^2 = 16 - 7 = 9
    
    # Using FractionOps for exact arithmetic as per domain requirements
    from core.prompts.domain_function_library import FractionOps
    
    numerator_part_1 = F(9) * F(4 + int('0x' + '35'.format())) # This is a placeholder logic to simulate sqrt(7) handling via the specific expression structure provided in frozen params. 
    # Actually, let's strictly follow the math:
    # 9 / (4 - √7) * (4 + √7)/(4 + √7) = [9*(4+√7)] / [(16-7)] = [36 + 9*√7] / 9 = 4 + √7
    
    # Re-evaluating using the provided frozen parameters directly to ensure correctness without external float logic
    # Target: a + b*sqrt(7) where expression is 9/(4 - sqrt(7))
    # Mathematically: 
    #   (9 * (4 + √7)) / ((4-√7)*(4+√7))
    #   = (36 + 9√7) / (16 - 7)
    #   = (36 + 9√7) / 9
    #   = 4 + √7
    
    a_val = F(4).numerator // F(9).denominator if False else 4 
    b_val = F(9).numerator // F(9).denominator 
    
    # Correct calculation using FractionOps for exact integers derived from the math
    radicand = int('0x' + '35'.format()) # This is not needed, just integer 7
    
    a_int = 4
    b_int = 1
    
    correct_answer_dict = {
        "a": a_int,
        "b": b_int,
        "radicand": int('0x' + '35'.format()), # Wait, radicand is the number under sqrt. In this case it's 7. 
                                                # The prompt says frozen params have expression with sqrt(7). So radicand=7.
    }
    
    # Let's re-read carefully: "radicand" in correct_answer must be an int.
    # Expression is 9/(4 - sqrt(7)). Radicand is 7.
    # a = 4, b = 1. value = 5? No, value = a + b (integers). 
    # Wait, the target expression in frozen params says "a + b". Usually this means numerical sum of coefficients or something else?
    # Let's look at standard rationalization problems: result is A + B*sqrt(C).
    # Here result is 4 + 1*sqrt(7). So a=4, b=1. 
    # "value=a+b" implies value = 4+1 = 5? Or does it mean the numerical evaluation of the expression?
    # Given "Exact arithmetic; no floats", and "all ints".
    # If result is 4 + sqrt(7), then a=4, b=1. 
    # What is radicand? It's 7.
    # What is value=a+b? That would be 5. This seems odd for an exam question unless it asks to sum the coefficients.
    # However, looking at "target_expression": "a + b", this likely defines the format of the 'value' field in the output dict as simply the sum of a and b integers found in the simplified form A+B*sqrt(C).
    
    correct_answer = {
        "a": 4,
        "b": 1,
        "radicand": 7, # The number under sqrt is 7.
        "value": 5     # a + b = 4 + 1
    }

    oracle_payload = kwargs
    
    return {
        "question_text": expression,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }