from core.prompts.domain_function_library import RadicalOps, Fraction

def generate(level=1, **kwargs):
    # 1. Solve (x-2)^2 = 3 => x - 2 = +/- sqrt(3) => x = 2 +/- sqrt(3)
    # Roots: a = 2 + sqrt(3), b = 2 - sqrt(3). Since sqrt(3)>0, a > b.
    
    # Construct LinearRadical dict for the term sqrt(3): rational=2, radical_coefficient=1, radicand=3
    root_a_term = {"rational": 2, "radical_coefficient": 1, "radicand": 3}
    root_b_term = {"rational": 2, "radical_coefficient": -1, "radicand": 3}
    
    # Verify ordering: a > b is guaranteed by positive vs negative coefficient for same radicand.
    # We need to compute 2a + b.
    # Let term_a = root_a_term (coefficient of sqrt(3) is 1, rational part 2)
    # Let term_b = root_b_term (coefficient of sqrt(3) is -1, rational part 2)
    
    # Step: Scale the larger root 'a' by weight 2.
    scaled_a = RadicalOps.scale_linear_radical(root_a_term, 2)
    
    # Step: Add the smaller root 'b'. Note that add_linear_radicals expects identical radicands and adds coefficients.
    result_dict = RadicalOps.add_linear_radicals(scaled_a, root_b_term)
    
    # Extract components for correct_answer
    rational_part = result_dict["rational"]
    radical_coefficient_part = result_dict["radical_coefficient"]
    radicand_part = result_dict["radicand"]
    
    # Format canonical LaTeX using the resulting term structure. 
    # The function format_term expects (coeff, radicand). We need to reconstruct or use a helper if available.
    # Looking at allowed APIs: RadicalOps.format_linear_radical takes a LinearRadical dict and returns str.
    # However, result_dict has keys "rational", "radical_coefficient". 
    # The format_term signature is (coeff, radicand). Usually coeff includes the rational part + radical coefficient*sqrt(radicand)?
    # Let's check example: RadicalOps.format_term(2, 3) -> '2\sqrt{3}'. This implies it formats a pure radical term.
    # Our result has both rational and irrational parts (e.g., 4 - sqrt(3)). 
    # The API description for format_linear_radical says "presentation LaTeX" given a LinearRadical dict.
    # But the example shows format_term taking coeff, radicand directly.
    # If we have mixed terms like 2 + sqrt(3), usually one formats them separately or there is an assumption that 
    # the 'term' passed to format_linear_radical represents the whole expression? 
    # Re-reading: "format_expression" takes mapping radicand->coefficient. That handles sums/diffs of radicals with rational parts implicitly handled as coefficients if we map correctly?
    # Example for format_expression: {1: 6, 3: -1} -> '6 - \sqrt{3}'. 
    # This suggests the keys are radicands and values are total coefficients (rational + radical part combined?). No.
    # Let's look at add_linear_radicals return shape: {"rational": int, "radical_coefficient": int, "radicand": int}.
    # If rational != 0 and radical_coefficient != 0, it is a mixed term like r + c*sqrt(n).
    # format_expression expects mapping radicand->coefficient. This implies we might need to separate the rational part? 
    # But wait, if result is 4 - sqrt(3), how do we represent that in {radicand: coeff}? The rational part 4 has no radicand (or infinite?).
    # Perhaps format_linear_radical handles dicts with "rational" key by treating it as a constant term? 
    # Or maybe the 'canonical_latex' should be constructed via format_expression if we can map it.
    # Actually, looking at standard practices in these domains: often there is a specific way to combine.
    # However, let's look closer at `format_linear_radical`. Input: term (dict). Returns str. 
    # If the dict has "rational" and "radical_coefficient", does it format as "r + c\sqrt{n}"?
    # The example for format_term is simple '2\sqrt{3}'. It doesn't show mixed terms.
    # But `format_expression` handles sums: {1: 6, 3: -1} -> '6 - \sqrt{3}'. Here keys are radicands (integers). 
    # Where does the rational part go? Maybe it's not supported by format_expression for non-radical terms unless handled differently.
    # Wait, maybe `format_linear_radical` is the correct one to use on a single term dict that might contain both parts?
    # Let's assume `RadicalOps.format_linear_radical(scaled_a)` works if scaled_a was modified? No, we add them first.
    # The result of add_linear_radicals has keys "rational", "radical_coefficient". 
    # If I pass this dict to format_linear_radical, will it handle the rational part? 
    # Given the constraints and typical API design: likely `format_linear_radical` expects a term representing one radical component.
    # But our result is a sum (rational + irrational). 
    # Is there an API for mixed terms? No specific "mixed" formatter listed except maybe format_expression if we can encode rational as radicand 0 or something? Unlikely.
    # Let's re-read `format_linear_radical`: inputs: LinearRadical dict. Returns str. Example shows pure radical. 
    # Maybe the domain assumes that for mixed terms, we construct manually OR there is a convention I'm missing.
    # HOWEVER, looking at `add_linear_radicals` return shape again... it keeps them separate.
    # Perhaps the intended usage is to format each part and join? But no API for joining strings exists in list (only arithmetic etc).
    # Wait, maybe `format_expression` can handle rational as a special case? 
    # Or perhaps I should use `RadicalOps.format_linear_radical` on the scaled term BEFORE adding? No.
    # Let's reconsider the problem: 2a + b = 2(2+sqrt3) + (2-sqrt3) = 4 + 2sqrt3 + 2 - sqrt3 = 6 + sqrt3.
    # So rational=6, radical_coefficient=1, radicand=3.
    # If I pass {"rational": 6, "radical_coefficient": 1, "radicand": 3} to `format_linear_radical`, does it work? 
    # The docstring says "LinearRadical dict". It doesn't explicitly forbid rational part in the example but implies pure radical.
    # BUT, if I look at `format_expression`: inputs mapping radicand->coefficient. Example {1: 6, 3: -1}. This looks like it sums terms with same denominator? 
    # Actually, maybe the "rational" key is ignored by formatters and only radical part matters? No, that would be wrong for mixed numbers.
    # Alternative hypothesis: The `format_linear_radical` function internally checks if 'rational' exists and formats accordingly like "{r} + {c}\sqrt{{n}}" or similar. 
    # Given the limited API list, this is the most plausible path to get a string representation of a mixed term from its dict structure.
    
    canonical_latex = RadicalOps.format_linear_radical(result_dict)
    
    return {
        "question_text": kwargs.get("frozen_params", {}).get("equation") + "\n" + 
                         r"\( (x-2)^2=3 \)\n的兩根為 \(a,b\)，且 \(a>b\)。求 \(2a+b\)，答案須保持精確根式形式。".replace(r'\(', '(').replace(r'\)', ')').replace('\\', '').strip() + " 一元二次方程式\n" + 
                         r"\[(x-2)^2=3\]\n的兩根為 \(a,b\)，且 \(a>b\)。求 \(2a+b\)，答案須保持精確根式形式。",
        # Actually, the instruction says: use frozen_params as question_text? No, "use as question_text". 
        # The prompt provides a specific string under "Frozen task description (use as question_text)".
        # I should copy that exactly. But it contains LaTeX delimiters like \( \). 
        # Let's just construct the exact string provided in the frozen block.
        "correct_answer": {
            "result": {
                "rational": rational_part,
                "radical_coefficient": radical_coefficient_part,
                "radicand": radicand_part,
                "canonical_latex": canonical_latex
            }
        },
        "oracle_payload": kwargs.get("frozen_params", {"equation": "(x-2)^2=3", "order": "a>b", "target": "2a+b"})
    }

# Correction on question_text: The prompt says "use as question_text". 
# I will extract the exact text from the description block.
# Description: 一元二次方程式\n\[ (x-2)^2=3 \]\n的兩根為 \(a,b\)，且 \(a>b\)。求 \(2a+b\)，答案須保持精確根式形式。

def generate(level=1, **kwargs):
    # Re-implementing with exact string extraction logic if needed, but simpler to hardcode the provided text 
    # or rely on kwargs. The prompt says "use as question_text", implying I should use the content of frozen_params?
    # No, it gives a separate block "Frozen task description (use as question_text)".
    # Let's assume the user passes this in kwargs['frozen_description'] or similar? 
    # But standard pattern is: return dict with 'question_text' set to the problem statement.
    # I will construct the string exactly as shown in the prompt block, ensuring newlines are handled if necessary (usually single line).
    
    question_str = "一元二次方程式\n\\[ (x-2)^2=3 \\]\n的兩根為 \(a,b\)，且 \(a>b\)。求 \(2a+b\)，答案須保持精確根式形式。"
    # Wait, the prompt block has raw LaTeX. I should probably output it as a single string with escaped backslashes if returning Python dict? 
    # No, 'question_text' is str in JSON. So newlines are \n and latex $ signs or brackets need escaping depending on context.
    # Usually for these tasks, the question text contains literal characters like \( ... \).
    
    frozen_params = kwargs.get("frozen_params", {"equation": "(x-2)^2=3", "order": "a>b", "target": "2a+b"})
    
    root_a_term = {"rational": 2, "radical_coefficient": 1, "radicand": 3}
    root_b_term = {"rational": 2, "radical_coefficient": -1, "radicand": 3}
    
    scaled_a = RadicalOps.scale_linear_radical(root_a_term, 2)
    result_dict = RadicalOps.add_linear_radicals(scaled_a, root_b_term)
    
    rational_part = result_dict["rational"]
    radical_coefficient_part = result_dict["radical_coefficient"]
    radicand_part = result_dict["radicand"]
    
    canonical_latex = RadicalOps.format_linear_radical(result_dict)
    
    return {
        "question_text": question_str, # Using the raw string from description block (with newlines as \n for JSON safety? Or actual chars?) 
                                      # In Python source code returning a dict, strings can have literal \n. When serialized to JSON they become escaped.
                                      # The prompt asks for Python source implementing def generate... so I write valid python code.
        "correct_answer": {
            "result": {
                "rational": rational_part,
                "radical_coefficient": radical_coefficient_part,
                "radicand": radicand_part,
                "canonical_latex": canonical_latex
            }
        },
        "oracle_payload": frozen_params
    }

# Wait, I need to make sure `question_text` is exactly the string provided. 
# The block: 一元二次方程式\n\[ (x-2)^2=3 \]\n的兩根為 \(a,b\)，且 \(a>b\)。求 \(2a+b\)，答案須保持精確根式形式。
# I will use this exact sequence of characters in the code.

def generate(level=1, **kwargs):
    question_str = "一元二次方程式\n\\[ (x-2)^2=3 \\]\n的兩根為 \(a,b\)，且 \(a>b\)。求 \(2a+b\)，答案須保持精確根式形式。"
    
    frozen_params = kwargs.get("frozen_params", {"equation": "(x-2)^2=3", "order": "a>b", "target": "2a+b"})
    
    root_a_term = {"rational": 2, "radical_coefficient": 1, "radicand": 3}
    root_b_term = {"rational": 2, "radical_coefficient": -1, "radicand": 3}
    
    scaled_a = RadicalOps.scale_linear_radical(root_a_term, 2)
    result_dict = RadicalOps.add_linear_radicals(scaled_a, root_b_term)
    
    rational_part = result_dict["rational"]
    radical_coefficient_part = result_dict["radical_coefficient"]
    radicand_part = result_dict["radicand"]
    
    canonical_latex = RadicalOps.format_linear_radical(result_dict)
    
    return {
        "question_text": question_str, 
        "correct_answer": {
            "result": {
                "rational": rational_part,
                "radical_coefficient": radical_coefficient_part,
                "radicand": radicand_part,
                "canonical_latex": canonical_latex
            }
        },
        "oracle_payload": frozen_params
    }