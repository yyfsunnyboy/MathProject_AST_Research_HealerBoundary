def generate(level=1, **kwargs):
    import json
    
    frozen_params = {"days": 15, "hours_per_generation": 20, "initial": 1, "split_factor": 4}
    
    # Calculate total generations based on days and hours per generation
    total_hours_available = level * frozen_params["days"] * (frozen_params["hours_per_generation"] / 24) if isinstance(frozen_params["days"], int) else frozen_params["days"] * (frozen_params["hours_per_generation"] / 24)
    
    # Assuming 'level' scales the time available linearly for this specific task context based on typical exponential growth problem structures where level often implies duration multiplier or similar. 
    # However, looking at standard interpretations: if days=15 is fixed and hours_per_gen=20 (which is 4/3 of a day), let's calculate generations directly from the frozen params first to ensure correctness for Level 1.
    
    # Re-evaluating based on strict "frozen sampled parameters" usage without external logic assumptions:
    # Total time in days = level * 15? Or is 'days' just one of many inputs scaled by level? 
    # Given the task name implies exponential growth, usually N(t) = P0 * r^t.
    # Let's assume standard interpretation where 'level' might scale the duration or it's a fixed problem instance for Level 1.
    # To be safe and robust: Calculate generations as (total_days_available / hours_per_generation). 
    # If level=1, days=15. Hours per gen = 20. Generations = floor(15 * 24 / 20) ? Or simply based on the provided 'days' being total duration?
    # Let's assume the problem asks for growth over a specific number of generations derived from the parameters.
    
    # Standard interpretation: 
    # Initial population P0 = frozen_params["initial"] (1)
    # Growth factor r = frozen_params["split_factor"] (4, meaning 4x per generation? Or split into 4 parts?)
    # "Split factor" in exponential growth usually implies multiplication by that factor. So N(t+1) = N(t) * 4.
    
    # How many generations? 
    # If 'days' is the total duration and 'hours_per_generation' is the time per generation:
    # Generations = floor( (level * frozen_params["days"]) / (frozen_params["hours_per_generation"] / 24) ) ?
    # Or simply using the raw numbers if level=1 acts as a base. 
    # Let's calculate generations based on days provided in frozen params, assuming 'level' scales time linearly for this specific challenge type often found in these datasets (e.g., Project Euler style or similar coding challenges).
    
    total_days = level * frozen_params["days"]
    hours_per_gen = frozen_params["hours_per_generation"]
    # Convert days to hours and divide by hours per generation
    generations = int(total_days * 24 / hours_per_gen)
    
    initial_pop = frozen_params["initial"]
    split_factor = frozen_params["split_factor"]
    
    final_population = initial_pop * (split_factor ** generations)
    
    question_text = r"""Consider a population that grows exponentially. If the initial population is $P_0$ and it splits by a factor of $r$ every generation, what will be the population after $n$ generations? Given: $P_0 = 1$, $r = 4$. Calculate the final population if there are exactly $\text{generations}$ generations."""
    
    correct_answer_dict = {"k": int(final_population)}
    
    oracle_payload = frozen_params
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer_dict,
        "oracle_payload": oracle_payload
    }