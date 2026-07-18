from core.prompts.domain_function_library import IntegerOps

def generate(level=1, **kwargs):
    # Frozen parameters
    days = 15
    hours_per_generation = 20
    initial = 1
    split_factor = 4
    
    # Calculations using domain APIs
    total_hours = IntegerOps.safe_eval(f"{days} * 24")
    generations = IntegerOps.safe_eval(f"{total_hours} // {hours_per_generation}")
    
    # Formatting
    days_fmt = IntegerOps.fmt_num(days)
    hours_fmt = IntegerOps.fmt_num(hours_per_generation)
    initial_fmt = IntegerOps.fmt_num(initial)
    split_factor_fmt = IntegerOps.fmt_num(split_factor)
    
    question_text = (
        f"A population of bacteria starts with ${initial_fmt}$ organism and splits by a factor of "
        f"${split_factor_fmt}$ every ${hours_fmt}$ hours. How many generations will occur in ${days_fmt}$ days?"
    )
    
    correct_answer = {"k": int(generations)}
    
    oracle_payload = {
        "days": days,
        "hours_per_generation": hours_per_generation,
        "initial": initial,
        "split_factor": split_factor
    }
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }