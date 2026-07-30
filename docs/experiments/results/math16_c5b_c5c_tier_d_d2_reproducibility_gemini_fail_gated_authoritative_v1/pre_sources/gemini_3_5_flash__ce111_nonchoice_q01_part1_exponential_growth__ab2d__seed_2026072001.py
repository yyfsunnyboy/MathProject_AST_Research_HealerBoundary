from core.prompts.domain_function_library import IntegerOps

def generate(level=1, **kwargs):
    # Frozen sampled parameters
    days = 15
    hours_per_generation = 20
    initial = 1
    split_factor = 4

    # Calculate the number of generations
    total_hours = IntegerOps.safe_eval(f"{days} * 24")
    generations = IntegerOps.safe_eval(f"{total_hours} // {hours_per_generation}")

    # Format numbers for the question text
    initial_str = IntegerOps.fmt_num(initial)
    split_factor_str = IntegerOps.fmt_num(split_factor)
    hours_str = IntegerOps.fmt_num(hours_per_generation)
    days_str = IntegerOps.fmt_num(days)

    organism_word = "organism" if initial == 1 else "organisms"
    question_text = f"A population of bacteria starts with ${initial_str}$ {organism_word} and splits into ${split_factor_str}$ organisms every ${hours_str}$ hours. How many generations of division will occur in ${days_str}$ days?"

    return {
        "question_text": question_text,
        "correct_answer": {"k": int(generations)},
        "oracle_payload": {
            "days": days,
            "hours_per_generation": hours_per_generation,
            "initial": initial,
            "split_factor": split_factor
        }
    }