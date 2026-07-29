from typing import Dict, Any
import math

def generate(level=1, **kwargs):
    frozen_params = {"days": 15, "hours_per_generation": 20, "initial": 1, "split_factor": 4}
    
    # Calculate number of generations based on days and hours per generation (assuming 24h day)
    total_hours = frozen_params["days"] * 24
    num_generations = int(total_hours / frozen_params["hours_per_generation"])
    
    initial_pop = frozen_params["initial"]
    split_factor = frozen_params["split_factor"]
    
    # Calculate final population: P = I * (S ^ G)
    correct_value = initial_pop * (split_factor ** num_generations)
    
    from core.prompts.domain_function_library import IntegerOps
    
    formatted_answer_str = IntegerOps.fmt_num(correct_value)
    
    question_text = f"A bacterial culture starts with {IntegerOps.fmt_num(initial_pop)} cells. The population splits every {frozen_params['hours_per_generation']} hours for a duration of {frozen_params['days']} days (24-hour day). If the split factor is {split_factor}, what is the final population count? Express your answer as an integer."
    
    correct_answer = {"k": int(correct_value)}
    oracle_payload = frozen_params
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }