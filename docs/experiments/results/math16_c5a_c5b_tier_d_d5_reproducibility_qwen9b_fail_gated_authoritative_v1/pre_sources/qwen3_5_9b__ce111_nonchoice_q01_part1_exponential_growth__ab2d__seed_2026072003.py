from core.prompts.domain_function_library import IntegerOps

def generate(level=1, **kwargs):
    frozen = {"days": 15, "hours_per_generation": 20, "initial": 1, "split_factor": 4}
    
    # Calculate number of generations: total hours / hours per generation
    days = frozen["days"]
    hours_per_day = 24
    total_hours = days * hours_per_day
    n_generations = IntegerOps.safe_eval(f"int({total_hours} // {frozen['hours_per_generation']})")
    
    # Calculate final count: initial * (split_factor ^ generations)
    split_factor = frozen["split_factor"]
    k = IntegerOps.safe_eval(f"{frozen['initial']} * ({split_factor} ** {n_generations})")
    
    question_text = f"A population starts with an initial size of {IntegerOps.fmt_num(frozen['initial'])}. It splits every {IntegerOps.fmt_num(frozen['hours_per_generation'])} hours. After {IntegerOps.fmt_num(days)} days, how many individuals are there? Assume a 24-hour day."
    
    correct_answer = {"k": k}
    oracle_payload = frozen
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }