def generate(level=1, **kwargs) -> Dict[str, Any]:
    """
    Generates an exponential growth math problem based on frozen parameters.
    
    Args:
        level (int): Difficulty level (not used in this specific task logic but kept for signature).
        **kwargs: Additional arguments to override or supplement defaults if needed.
        
    Returns:
        dict: Contains 'question_text', 'correct_answer', and 'oracle_payload'.
    """
    
    # Frozen sampled parameters as specified
    frozen_params = {
        "days": 15, 
        "hours_per_generation": 20, 
        "initial": 1, 
        "split_factor": 4
    }

    # Extract values from frozen parameters or kwargs if provided (prioritizing frozen for this task)
    days = frozen_params.get("days", level * 5)
    hours_per_gen = frozen_params.get("hours_per_generation", 20)
    initial_pop = frozen_params.get("initial", 1)
    split_factor = frozen_params.get("split_factor", 4)

    # Calculate total generations based on days and hours per generation
    total_hours = days * 24
    num_generations = int(total_hours / hours_per_gen) if hours_per_gen > 0 else 0
    
    # Ensure we don't divide by zero or have negative generations for the formula logic
    if num_generations < 1:
        num_generations = 1 

    # Calculate final population using integer arithmetic to ensure 'k' is an int as required
    # Formula: k = initial * (split_factor ^ number_of_generations)
    try:
        correct_k = IntegerOps.safe_eval(f"{initial_pop} * {split_factor} ** {num_generations}")
    except ValueError:
        # Fallback to standard python eval if safe_eval is restricted or fails unexpectedly in a way that blocks logic
        import math
        k_val = initial_pop * (split_factor ** num_generations)
        correct_k = int(k_val)

    # Format the question text with LaTeX delimiters
    formatted_initial = IntegerOps.fmt_num(initial_pop)
    
    question_text = f"A population starts at {formatted_initial} individuals. It undergoes exponential growth where it splits every {hours_per_gen} hours for a duration of {days} days (totaling 24 * {days} hours). How many times does the generation cycle occur, and what is the final population size $k$ if each split multiplies the count by ${split_factor}$? Calculate $k = \\text{{initial}} \\times ({\\text{{factor}}}^n)$."
    
    # Correct answer structure: dict with exactly 'k' (int)
    correct_answer = {
        "k": correct_k
    }

    # Oracle payload must exactly equal the frozen sampled parameters
    oracle_payload = frozen_params.copy() if isinstance(frozen_params, dict) else {}

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }