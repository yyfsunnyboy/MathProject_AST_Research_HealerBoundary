def generate(level=1, **kwargs):
    return {
        "question_text": r"Given an initial population of $P_0 = 1$ that splits by a factor of $S = 4$ every $h = 20$ hours over a total duration of $D = 15$ days. Calculate the final count $k$, where time is measured in generations ($g = D / (24/h)$).",
        "correct_answer": {"k": 67983},
        "oracle_payload": {"days": 15, "hours_per_generation": 20, "initial": 1, "split_factor": 4}
    }