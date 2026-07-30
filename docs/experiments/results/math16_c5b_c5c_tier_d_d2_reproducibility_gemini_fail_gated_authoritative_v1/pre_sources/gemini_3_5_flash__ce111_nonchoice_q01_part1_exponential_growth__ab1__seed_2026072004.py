def generate(level=1, **kwargs):
    days = 15
    hours_per_generation = 20
    initial = 1
    split_factor = 4

    total_hours = days * 24
    generations = total_hours // hours_per_generation

    question_text = (
        f"A population of bacteria begins with ${initial}$ organism. "
        f"Every ${hours_per_generation}$ hours, each organism splits into ${split_factor}$ organisms. "
        f"How many generations will occur in ${days}$ days?"
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