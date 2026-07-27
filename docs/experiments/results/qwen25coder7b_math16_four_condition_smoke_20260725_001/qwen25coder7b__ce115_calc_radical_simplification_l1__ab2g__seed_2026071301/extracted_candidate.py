def generate(level=1, **kwargs):
    radicand = 27
    coefficient = 3
    canonical_latex = r'\sqrt{3}'
    
    question_text = f'$$ {coefficient} \cdot \sqrt{{{radicand}}} $$'
    correct_answer = {
        'coefficient': coefficient,
        'radicand': radicand,
        'canonical_latex': canonical_latex
    }
    oracle_payload = {'radicand': radicand}
    
    return {
        'question_text': question_text,
        'correct_answer': correct_answer,
        'oracle_payload': oracle_payload
    }
