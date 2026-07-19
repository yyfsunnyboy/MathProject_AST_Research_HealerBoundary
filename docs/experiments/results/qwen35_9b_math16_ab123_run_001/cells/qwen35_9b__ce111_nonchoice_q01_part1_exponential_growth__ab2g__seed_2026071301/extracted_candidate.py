def generate(level=1, **kwargs):
    import json
    
    frozen_params = {
        "days": 15, 
        "hours_per_generation": 20, 
        "initial": 1, 
        "split_factor": 4
    }
    
    # Calculate total hours: days * hours_per_day. The problem implies a standard day unless specified otherwise (usually 24).
    # However, looking at typical exponential growth problems in this context without explicit 'hours_per_day' given as input but implied by "days", 
    # we must assume a standard day duration to convert total_days into generations or vice versa.
    # Standard assumption: 1 day = 24 hours.
    
    days = frozen_params["days"]
    initial = frozen_params["initial"]
    split_factor = frozen_params["split_factor"]
    generation_time_hours = frozen_params["hours_per_generation"]
    assumed_hours_per_day = 24
    
    total_growth_hours = days * assumed_hours_per_day
    
    # Number of generations that fit in the timeframe
    num_generations = int(total_growth_hours / generation_time_hours) if generation_time_hours > 0 else 0
    
    # Final count calculation for discrete steps usually found at integer boundaries or floor logic. 
    # Given "days", we often calculate population after N doublings (or splits).
    final_count = initial * (split_factor ** num_generations)
    
    question_text = f"A culture starts with {initial} bacteria. The population doubles every {hours_per_generation:=d}-{frozen_params['hours_per_generation']:02d}-hour intervals. How many bacteria are there after {days} days? Assume a day has 24 hours." # Wait, split_factor is not necessarily doubling (2). It's 'split'. 
    # Let's refine the text to use variables properly from frozen params
    
    h = str(frozen_params["hours_per_generation"])
    d_days = str(days)
    
    question_text = f"A culture starts with {initial} cells. The population splits every {h}-hour intervals (assuming a 24-hour day). Calculate the total number of cells after {d_days} days."
    
    correct_answer_k = final_count
    
    return {
        "question_text": question_text,
        "correct_answer": {"k": correct_answer_k},
        "oracle_payload": frozen_params
    }