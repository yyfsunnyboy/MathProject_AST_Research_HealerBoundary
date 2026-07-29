# -*- coding: utf-8 -*-

def generate(level=1, **kwargs):
    # Define all frozen parameters directly as per specification
    days = 15
    hours_per_generation = 20
    initial = 1
    split_factor = 4
    
    # Convert days to total available hours using native Python arithmetic
    total_hours = days * 24
    
    # Compute the number of complete generations (k)
    # k is the integer division of total_hours by hours_per_generation
    k = total_hours // hours_per_generation
    
    correct_answer = {"k": k}
    
    question_text = r"Given an initial population of $1$ and a split factor of $4$, with each generation taking $20$ hours to complete, how many full generations can occur in $15$ days? Express your answer as the integer $k$."
    
    oracle_payload = {"days": 15, "hours_per_generation": 20, "initial": 1, "split_factor": 4}

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload,
    }