from typing import Dict, Any
import json

def generate(level=1, **kwargs):
    frozen_params = {"days": 15, "hours_per_generation": 20, "initial": 1, "split_factor": 4}
    
    # Calculate the number of generations based on days and hours per generation
    total_hours = frozen_params["days"] * 24
    num_generations = int(total_hours / frozen_params["hours_per_generation"])
    
    initial_population = frozen_params["initial"]
    split_factor = frozen_params["split_factor"]
    
    # Calculate final population using integer arithmetic as per typical discrete growth models in this context
    # Population = Initial * (Split Factor ^ Number of Generations)
    k = initial_population * (split_factor ** num_generations)
    
    from core.prompts.domain_function_library import IntegerOps
    
    question_text = f"Starting with {IntegerOps.fmt_num(initial_population)} organisms, if each organism splits into {split_factor} new ones every {frozen_params['hours_per_generation']} hours over a period of {frozen_params['days']} days, how many organisms will there be in total?"
    
    correct_answer = {"k": k}
    
    oracle_payload = frozen_params
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }