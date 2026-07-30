# -*- coding: utf-8 -*-

def generate(level=1, **kwargs):
    # Frozen sampled parameters
    days = 15
    hours_per_generation = 20
    initial = 1
    split_factor = 4

    # Compute the number of complete generations
    total_hours = days * 24
    k = total_hours // hours_per_generation

    # Format the question text with LaTeX delimiters
    question_text = (
        f"A population of bacteria starts with ${initial}$ organism. "
        f"Every ${hours_per_generation}$ hours, each organism splits into ${split_factor}$ organisms. "
        f"How many complete generations will have occurred after ${days}$ days?"
    )

    correct_answer = {"k": k}

    oracle_payload = {
        "days": days,
        "hours_per_generation": hours_per_generation,
        "initial": initial,
        "split_factor": split_factor,
    }

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload,
    }