import os
import json
from pathlib import Path
from google import genai
from google.genai import types
from app.prompts.prompt import build_prompt_for_context, build_prompt_for_guidance, build_prompt_for_outline, build_prompt_for_system, build_prompt_for_user_template
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY", default="")
CLIENT = genai.Client(api_key=API_KEY)


def load_json():
    path = Path("app/data/vedas.json")
    if not path.exists():
        raise FileNotFoundError("Scraped JSON was not found")
    with open(path, "r", encoding='utf-8') as f:
        return json.load(f)
    

def _build_context(doc: dict):
    lines = []
    if doc.get("site_heading"):
        lines.append(f"Site Heading: {doc['site_heading'].get('title')}")
    if doc.get("announcements"):
        lines.append(f"Announcements: {doc['announcements'].get('items')}")
    if doc.get("awards"):
        lines.append(f"Awards: {doc['awards'].get('description')}")
    if doc.get("builtup_area"):
        lines.append(f"Builtup_area: {doc['builtup_area'].get("description")}")
    if doc.get("webinar"):
        lines.append(f"Webinar: {doc['webinar'].get('description')}")
    if doc.get("interferometric"):
        lines.append(f"Interferometric: {doc['interferometric'].get('description')}")
    if doc.get("solar_power_plants"):
        lines.append(f"solar_power_plants: {doc['solar_power_plants'].get('description')}")

    if doc.get("contact"):
        lines.append("Contact Info: ")
        for line in doc['contact'].get("contact", []):
            lines.append(f" - {line}")
        if doc['contact'].get("phone"):
            lines.append(f"Phone: {doc['contact']['phone']}")

    return "\n".join(lines)


def answer_question(query: str):
    doc = load_json()
    context = _build_context(doc=doc)

    system_prompt = build_prompt_for_system()
    user_prompt_template = build_prompt_for_user_template()
    user_prompt = user_prompt_template.format(query=query, context=context)

    resp = CLIENT.models.generate_content(
        model="gemini-2.5-flash",
        config={
            "max_output_tokens": 4000,
            "temperature": 0.2
        },
        
        contents=[
            types.Content(parts=[types.Part(text=system_prompt)]),
            types.Content(role="user", parts=[types.Part(text=user_prompt)]),

        ]
    
    )

    return resp.text




    

    

