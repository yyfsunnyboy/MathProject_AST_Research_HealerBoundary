from core.prompts.domain_function_library import IntegerOps

def generate(level=1, **kwargs):
    days = 15
    hours_per_generation = 20
    initial = 1
    split_factor = 4
    
    total_hours = IntegerOps.safe_eval(f"{days} * 24")
    generations = IntegerOps.safe_eval(f"{total_hours} // {hours_per_generation}")
    
    initial_str = IntegerOps.fmt_num(initial)
    split_factor_str = IntegerOps.fmt_num(split_factor)
    hours_per_generation_str = IntegerOps.fmt_num(hours_per_generation)
    days_str = IntegerOps.fmt_num(days)
    
    question_text = (
        f"A population of bacteria starts with ${initial_str}$ organism and "
        f"splits into ${split_factor_str}$ every ${hours_per_generation_str}$ hours. "
        f"How many generations will occur in ${days_str}$ days?"
    )
    
    return {
        "question_text": question_text,
        "correct_answer": {"k": generations},
        "oracle_payload": {
            "days": days,
            "hours_per_generation": hours_per_generation,
            "initial": initial,
            "split_factor": split_factor
        }
    }