import json
from typing import Dict, Any


def generate(level=1, **kwargs) -> Dict[str, Any]:
    frozen_params = {
        "days": 15,
        "hours_per_generation": 20,
        "initial": 1,
        "split_factor": 4
    }

    days = frozen_params["days"]
    hours_per_gen = frozen_params["hours_per_generation"]
    initial = frozen_params["initial"]
    split_factor = frozen_params["split_factor"]

    total_hours = days * hours_per_gen
    generations_count = int(total_hours / hours_per_gen) if hours_per_gen > 0 else 1
    
    final_population = initial * (split_factor ** generations_count)
    
    correct_answer_dict = {"k": int(final_population)}
    
    question_text = r"""Calculate the population size after exponential growth over multiple generations. Given an initial population of $initial$ individuals, where each generation splits into $split\_factor$ times its previous size, determine the final count $k$ after $generations\_count$ generations defined by total time in days and hours per generation."""
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer_dict,
        "oracle_payload": frozen_params
    }