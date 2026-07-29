def generate(level=1, **kwargs):
    import json
    
    # Frozen sampled parameters as specified in the task context
    frozen_params = {
        "days": 15, 
        "hours_per_generation": 20, 
        "initial": 1, 
        "split_factor": 4
    }
    
    # Calculate total hours based on days and hours per generation (assuming continuous growth logic)
    # However, the task implies a discrete exponential growth model: Final = Initial * (Split Factor ^ Number of Generations)
    # We need to determine the number of generations. 
    # Given "days" and "hours_per_generation", we assume 24 hours in a day for standard time conversion unless specified otherwise.
    total_hours = frozen_params["days"] * 24
    num_generations = int(total_hours / frozen_params["hours_per_generation"])
    
    initial_population = frozen_params["initial"]
    split_factor = frozen_params["split_factor"]
    
    # Calculate final population (k)
    k = initial_population * (split_factor ** num_generations)
    
    question_text = f"An organism starts with an initial count of {frozen_params['initial']} and splits every {frozen_params['hours_per_generation']} hours. After {frozen_params['days']} days, what is the final population count $k$? Assume a standard 24-hour day."
    
    correct_answer = {"k": k}
    
    oracle_payload = frozen_params
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }