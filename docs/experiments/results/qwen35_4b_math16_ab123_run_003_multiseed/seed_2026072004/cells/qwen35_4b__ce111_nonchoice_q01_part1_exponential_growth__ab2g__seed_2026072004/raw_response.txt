def generate(level=1, **kwargs):
    question_text = r"The population of a bacteria culture starts with 1 individual ($P_0 = 1$). The population doubles every generation according to $P_{n} = P_{n-1} \times S$, where $S$ is the split factor. If there are no deaths and only reproduction occurs, what will be the total number of individuals after 15 generations with a split factor of 4?"
    initial_population = kwargs.get("initial", 1)
    days = kwargs.get("days", 15)
    hours_per_generation = kwargs.get("hours_per_generation", 20)
    split_factor = kwargs.get("split_factor", 4)

    generations_passed = int(days / (hours_per_generation // 2)) if isinstance(hours_per_generation, float) else days // hours_per_generation
    
    final_population = initial_population * (split_factor ** generations_passed)
    
    correct_answer = {"k": int(final_population)}
    oracle_payload = {**kwargs}

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }