def generate(level=1, **kwargs):
    question_text = r"Starting with $1$ individual that splits into 4 every generation over a period of $d$ days where each generation takes $h$ hours, what is the total population count after $g$ generations? Express your answer as an integer."
    
    frozen_params = {"days": 15, "hours_per_generation": 20, "initial": 1, "split_factor": 4}
    
    g_days = int(frozen_params["days"] / (frozen_params["hours_per_generation"] // 3)) if frozen_params["hours_per_generation"] % 3 == 0 else int((frozen_params["days"] * 24) // frozen_params["hours_per_generation"])
    # Simplify logic for direct generation count based on total hours available in the problem context usually implying a fixed timeline or just using provided split factor directly if generations are implied. 
    # However, looking at standard exponential growth problems with these specific inputs: 
    # Total time = 15 days * 24 hours/day = 360 hours
    # Hours per generation = 20
    # Number of generations g = floor(360 / 20) = 18
    
    initial = frozen_params["initial"]
    split_factor = frozen_params["split_factor"]
    
    if level == 1:
        g = int((frozen_params["days"] * 24) // frozen_params["hours_per_generation"])
        
        k = initial * (split_factor ** g)
        correct_answer = {"k": k}
    else:
        # Fallback for other levels if needed, though task specifies difficulty level 1 logic via context
        raise ValueError("Level not supported")

    oracle_payload = frozen_params
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }