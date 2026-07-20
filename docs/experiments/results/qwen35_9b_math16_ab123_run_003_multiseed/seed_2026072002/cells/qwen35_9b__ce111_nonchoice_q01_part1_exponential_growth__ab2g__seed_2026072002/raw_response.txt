def generate(level=1, **kwargs):
    frozen_params = {"days": 15, "hours_per_generation": 20, "initial": 1, "split_factor": 4}
    
    # Calculate number of generations based on hours per day (default 24) and given parameters.
    # Assuming standard day length if not specified in kwargs but implied by context or fixed to 24 for calculation stability unless overridden logic exists. 
    # However, strictly using frozen_params: we need total growth time. 
    # The task implies 'days' is the duration. We assume a full day has 24 hours unless 'hours_per_day' was in frozen (it isn't).
    # Let's calculate generations = floor(total_hours / hours_per_generation).
    # Total hours = days * 24.
    
    total_days = frozen_params["days"]
    hours_per_gen = frozen_params["hours_per_generation"]
    initial_count = frozen_params["initial"]
    split_factor = frozen_params["split_factor"]
    
    # Assuming standard day length of 24 hours for the calculation unless specified otherwise in similar problems.
    total_hours = total_days * 24
    
    generations = int(total_hours // hours_per_gen)
    
    if initial_count > 0:
        final_k = initial_count * (split_factor ** generations)
    else:
        final_k = 0
        
    correct_answer_dict = {"k": final_k}
    
    return {
        "question_text": f"Given an exponential growth process starting with $\\text{{initial}}$ items, where each generation lasts ${hours_per_gen}$ hours and the population splits by a factor of ${split_factor}$ every generation over ${total_days}$ days (assuming 24-hour days), calculate the final count. The formula is $N = N_0 \\cdot r^g$, where $r$ is the split factor and $g$ is the number of generations.",
        "correct_answer": correct_answer_dict,
        "oracle_payload": frozen_params
    }