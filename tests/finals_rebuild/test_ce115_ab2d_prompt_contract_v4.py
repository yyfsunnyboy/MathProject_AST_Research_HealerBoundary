from agent_tools.finals_rebuild.ce115_ab2d_assembly import runtime_toolbox_inventory, stub_for_task

def test_v4_prompt_is_available_toolbox_not_must_call():
 text=stub_for_task("ce115_calc_polynomial_division_l1")
 assert "Available Domain APIs" in text
 assert "Required APIs" not in text and "MUST_CALL" not in text
 assert "Do not call irrelevant APIs merely for compliance" in text
 assert "returned value contributes to the final answer" in text

def test_prompt_inventory_is_runtime_derived_and_complete():
 text=stub_for_task("ce115_calc_radical_simplification_l1")
 for api in runtime_toolbox_inventory():
  assert api["canonical_name"] in text
  assert api["signature"] in text
  assert api["return_structure"] in text
