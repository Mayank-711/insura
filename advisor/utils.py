import json
import os
import google.generativeai as genai
import re
from dotenv import load_dotenv

load_dotenv()

# Initialize Gemini
genai.configure(api_key="AIzaSyAC-f1Ag4eL5iQkUMrkvsFvMO-jWomDww4")
model = genai.GenerativeModel('gemma-3-27b-it')

SYSTEM_PROMPT = """
You are a professional insurance advisor helping users find the best insurance products.
Respond using clean and structured HTML. Use:

- <h3> for sections (e.g., "Section 1: Profile Summary")
- <h4> for sub-sections
- <p> for paragraphs
- <ul><li> for bullet points
- <table> with <thead>, <tbody>, <tr>, <td>, and <th> for comparisons

Avoid using markdown, asterisks (**), or special characters like ## or **bold**.

Keep responses clear, professional, and directly renderable in a chat UI. No <html> or <body> tags.
"""

# Basic profanity filter
BLOCKED_TERMS = [
    r'fuck', r'shit', r'asshole', r'bitch', r'cunt', r'dick', r'pussy', 
    r'nigger', r'fag', r'retard', r'kill', r'murder', r'hate', r'terrorist'
]

def contains_profanity(text):
    text = text.lower()
    return any(re.search(term, text) for term in BLOCKED_TERMS)

def get_ai_response(prompt, context=None):
    try:
        if context:
            prompt = f"{context}\n\n{prompt}"
        response = model.generate_content(SYSTEM_PROMPT + prompt)
        return response.text.strip()
    except Exception as e:
        return f"<p>Sorry, I encountered an error: {str(e)}</p>"

def extract_user_profile(user_input):
    prompt = f"""
Extract the following details from the user input and return ONLY valid JSON (no explanations, no code blocks):
- age (integer)
- marital_status (Single/Married/Divorced/Widowed)
- occupation (string)
- dependents (list like ["Spouse", "Children"])
- income_bracket (string like "13LPA")
- risk_appetite (Low/Medium/High)
- goals (list like ["Life insurance", "Child education", "Tax saving"])

User input: "{user_input}"

IMPORTANT: Output only valid JSON, do not include any explanations or text.
"""
    response = get_ai_response(prompt)
    try:
        json_str = response[response.find('{'):response.rfind('}')+1]
        return json.dumps(json.loads(json_str), indent=2)  # Return valid JSON string
    except Exception as e:
        print("Failed to parse profile JSON:", str(e))
        return None


def recommend_plans(profile_json):
    prompt = f"""
 Insurance Recommendations

Based on this profile, recommend 1–3 insurance products from:
- Term Life Insurance
- ULIPs
- Endowment Plans
- Health Insurance
- Pension Plans

For each product:
- Use <h4> for title
- Use <p> for explanation
- Then include a <table> comparing all recommended plans with columns:
  Premiums, Term, Returns, Coverage, Tax Benefits

  
keep it short response

No ```html
User profile:
{profile_json}
"""
    return get_ai_response(prompt)

def explain_bfsi_term(user_input):
    prompt = f"""
Check if the input contains any insurance or banking terms.
If yes, explain it in:
- Simple English using <p>
- An analogy using <p>
- Technical definition using <p>
- Also ask user details if no details found <p>

Else return "None".

keep it short response
No ```html

User input: {user_input}
"""
    response = get_ai_response(prompt)
    return response if "None" not in response else None

def compare_plans(plans_text):
    prompt = f"""
 Plan Comparison

Create a <table> comparing these plans using:
- Premiums (Low/Medium/High)
- Term (Short/Medium/Long)
- Returns (Low/Medium/High)
- Coverage (Low/Medium/High)
- Tax Benefits (Yes/No)

Wrap the table in proper HTML table tags.
No ```html

keep it short response


Plans: {plans_text}
"""
    return get_ai_response(prompt)

def generate_summary(profile_json, recommendations):
    prompt = f"""
Final Summary

Include:
- <h4>Summary of best plan</h4>
- <p>Why it suits the user</p>
- <ul> with 2–3 Next Steps</ul>
- Mention sample banks or providers offering these (generic names like LIC, SBI, etc.)
- <p>Disclaimer: We do not store your data. Please consult a licensed advisor.</p>


keep it short response
No ```html

Profile:
{profile_json}

Recommendations:
{recommendations}
"""
    return get_ai_response(prompt)