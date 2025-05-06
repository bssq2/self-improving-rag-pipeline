import guardrails as gr

# Example minimal usage
def guard_response(llm_response):
    """
    Processes the LLM response through Guardrails to filter out hallucinations or
    undesired content. Replace with your actual guardrails logic/JSON rail spec.
    """
    # Suppose we have a simple rail specification
    rail_spec = """
<rail version="0.1">
<output>
    <string name="answer" />
</output>
</rail>
"""
    validator = gr.Guard.from_rail_string(rail_spec)
    validated_output = validator(llm_response)
    return validated_output["answer"]