from core.prompts.domain_function_library import IntegerOps

def generate(level=1, **kwargs):
    # Frozen parameters
    days = 15
    hours_per_generation = 20
    initial = 1
    split_factor = 4
    
    # Calculations
    total_hours = IntegerOps.safe_eval(f"{days} * 24")
    generations = IntegerOps.safe_eval(f"{total_hours} // {hours_per_generation}")
    ans = IntegerOps.safe_eval(f"{initial} * ({split_factor} ** {generations})")
    
    bacterium_word = "bacterium" if initial == 1 else "bacteria"
    
    question_text = (
        f"A population of bacteria starts with ${initial}$ {bacterium_word} "
        f"and splits into ${split_factor}$ every ${hours_per_generation}$ hours. "
        f"How many bacteria will there be after ${days}$ days?"
    )
    
    return {
        "question_text": question_text,
        "correct_answer": {"k": ans},
        "oracle_payload": {
            "days": days,
            "hours_per_generation": hours_per_generation,
            "initial": initial,
            "split_factor": split_factor
        }
    }