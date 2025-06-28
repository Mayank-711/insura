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
Be concise, professional, and user-friendly. Explain complex terms simply with analogies when helpful.
Format responses with clear headings and bullet points when appropriate.
also return clean response as i am directly appending it at front. No *** whitespaces etc stuff. Also a clean table for comparison
"""

BLOCKED_TERMS = [
    r'fuck', r'shit', r'asshole', r'bitch', r'cunt', r'dick', r'pussy', 
    r'nigger', r'fag', r'retard', r'kill', r'murder', r'hate', r'terrorist'
]

def contains_profanity(text):
    text = text.lower()
    for term in BLOCKED_TERMS:
        if re.search(term, text):
            return True
    return False

def get_ai_response(prompt, context=None):
    try:
        if context:
            prompt = f"{context}\n\n{prompt}"
        response = model.generate_content(SYSTEM_PROMPT + prompt)
        return response.text
    except Exception as e:
        return f"Sorry, I encountered an error: {str(e)}"

def extract_user_profile(user_input):
    prompt = f"""
    Extract the following details from this user input as JSON. If any field is missing, use 'None':
    - age (integer)
    - marital_status (Single/Married/Divorced/Widowed)
    - occupation
    - dependents (list of relationships like ['Spouse', 'Children', 'Parents'])
    - income_bracket (like '5LPA', '10LPA', '15LPA+')
    - risk_appetite (Low/Medium/High)
    - goals (list like ['Life insurance', 'Wealth creation', 'Tax saving', 'Health cover'])
    User input: {user_input}
    
    Return ONLY valid JSON, nothing else.
    """
    response = get_ai_response(prompt)
    try:
        response = response[response.find('{'):response.rfind('}')+1]
        return response
    except:
        return None

def recommend_plans(profile_json):
    prompt = f"""
    Based on this user profile, recommend 1-3 insurance product categories from:
    - Term Life Insurance
    - ULIPs (Unit Linked Insurance Plans)
    - Endowment Plans
    - Health Insurance
    - Pension Plans
    also return clean response as i am directly appending it at front. No *** whitespaces etc stuff. Also a clean table for comparison
    For each recommended product, provide a 1-2 sentence user-friendly explanation.
    Format as: "Recommended: [product name] - [explanation]"
    
    User profile: {profile_json}
    """
    return get_ai_response(prompt)

def explain_bfsi_term(user_input):
    prompt = f"""
    Check if this user input contains any BFSI/insurance terms like ULIP, claim ratio, premium, etc.
    If yes, explain the first detected term in:
    1. Simple English
    2. With an analogy if possible
    3. Technical definition (if requested)
    
    If no BFSI terms found, return "None".
    also return clean response as i am directly appending it at front. No *** whitespaces etc stuff. Also a clean table for comparison
    User input: {user_input}
    """
    response = get_ai_response(prompt)
    return response if "None" not in response else None

def compare_plans(plans_text):
    prompt = f"""
    Create a comparison of these insurance plans using these metrics:
    - Premiums (Low/Medium/High)
    - Term (Short/Medium/Long)
    - Returns (Low/Medium/High)
    - Coverage (Low/Medium/High)
    - Tax benefits (Yes/No)
    
    Present as a markdown table with clear headings.
    also return clean response as i am directly appending it at front. No *** whitespaces etc stuff. Also a clean table for comparison
    
    Plans to compare: {plans_text}
    """
    return get_ai_response(prompt)

def generate_summary(profile_json, recommendations):
    prompt = f"""
    Based on this user profile and recommendations, provide:
    1. A concise summary of the best suited insurance plan
    2. Why it's a good fit (connect to their profile)
    3. Suggested next steps
    4. Include this disclaimer: 
    also return clean response as i am directly appending it at front. No *** whitespaces etc stuff. Also a clean table for comparison
    User profile: {profile_json}
    Recommendations: {recommendations}
    """
    return get_ai_response(prompt)