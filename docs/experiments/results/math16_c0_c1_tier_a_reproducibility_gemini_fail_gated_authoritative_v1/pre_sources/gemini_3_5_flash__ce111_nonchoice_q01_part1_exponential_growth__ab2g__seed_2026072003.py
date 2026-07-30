def generate(level=1, **kwargs):
    days = 15
    hours_per_generation = 20
    initial = 1
    split_factor = 4
    
    total_hours = days * 24
    generations = total_hours // hours_per_generation
    
    question_text = (
        f"A population of bacteria starts with ${initial}$ bacterium and splits into "
        f"${split_factor}$ bacteria every ${hours_per_generation}$ hours. "
        f"How many generations of bacteria will have occurred after ${days}$ days?"
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