def generate(level=1, **kwargs):
    days = 15
    hours_per_generation = 20
    initial = 1
    split_factor = 4
    
    total_hours = days * 24
    generations = total_hours // hours_per_generation
    
    question_text = (
        f"A population of bacteria starts with ${initial}$ organism. "
        f"If the population splits by a factor of ${split_factor}$ every ${hours_per_generation}$ hours, "
        f"how many generations of division will occur in ${days}$ days?"
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