def build_prompt_for_context():
    prompt_text = """

Context Header:
- Source: ISRO VEDAS site content extracted from official pages.
- Purpose: Provide raw, factual context for downstream prompt stages.
- Scope: Headings, announcements, awards, webinars, interferometric, descriptive paragraphs and etc details available.

"""
    return prompt_text.strip()



def build_prompt_for_outline():
    prompt_text = """

Outline Instructions:
- Begin with site heading.
- Include bullet points for key details.
- Keep the outline concise and factual.
"""
    return prompt_text.strip()


def build_prompt_for_system():
    prompt_text = """

System Prompt:
You are an expert and consultant in ISRO VEDAS content.

Output Requirements:
- Methods/technology if present (short paragraph).
- Cite VEDAS inline as [VEDAS]
- Provide the factual answers, DO NOT mix it with additional information.

Tone & Style:
- Professional, clear and consice.
- Prioritize factual accuracy and structured presentation.
"""
    return prompt_text.strip()


def build_prompt_for_user_template():
    prompt_text = """

User Prompt Template:
Task: Provide the concise answers for the questions asked by user. DO NOT provide the additional information.

Query: {query}

Context: {context}

Deliverable:
- A single concise answer for the question.
- Use [VEDAS] for citations.
"""
    return prompt_text.strip()



def build_prompt_for_guidance():
    prompt_text = """
Guidance Instructions:
- Plan the structure based on the outline.
- Verify consistency across sections.
- Do not expose intermediate steps.
- Only output the final structured summary.
"""
    return prompt_text.strip()

