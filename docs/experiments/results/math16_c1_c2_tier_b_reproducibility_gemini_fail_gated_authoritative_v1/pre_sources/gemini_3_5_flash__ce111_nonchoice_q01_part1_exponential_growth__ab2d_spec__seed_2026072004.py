def generate(level=1, **kwargs):
    days = 15
    hours_per_generation = 20
    initial = 1
    split_factor = 4

    # Convert days to hours
    total_hours = days * 24
    # Calculate complete generations
    k = total_hours // hours_per_generation

    question_text = (
        f"A population of bacteria starts with ${initial}$ organism. "
        f"Every ${hours_per_generation}$ hours, each organism splits into ${split_factor}$ organisms. "
        f"How many complete generations of division will occur in ${days}$ days?"
    )

    correct_answer = {"k": k}

    oracle_payload = {
        "days": days,
        "hours_per_generation": hours_per_generation,
        "initial": initial,
        "split_factor": split_factor,
    }

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload,
    }