# -*- coding: utf-8 -*-

def generate(level=1, **kwargs):
    # Frozen sampled parameters defined directly as per specification
    days = 15
    hours_per_generation = 20
    initial = 1
    split_factor = 4
    
    # Convert total time to generations (integer division)
    total_hours = days * 24
    k = total_hours // hours_per_generation
    
    correct_answer = {"k": int(k)}
    
    question_text = r"""A population starts with $initial$ individuals. Each generation, the population splits by a factor of $split\_factor$. Given that each generation takes $hours\_per\_generation$ hours and there are $days$ days available, what is the number of complete generations ($k$) that can occur? Express your answer as an integer."""
    
    oracle_payload = {
        "days": 15,
        "hours_per_generation": 20,
        "initial": 1,
        "split_factor": 4
    }

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }