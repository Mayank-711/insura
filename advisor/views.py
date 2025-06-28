from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from .utils import *

@csrf_exempt
def chat(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        user_input = data.get('message', '').strip()
        
        if not user_input:
            return JsonResponse({'error': 'Empty message'}, status=400)
            
        if contains_profanity(user_input):
            return JsonResponse({
                'response': "I'm sorry, but I can't respond to that language. Please rephrase your question professionally.",
                'level': 'error'
            })
        
        general_questions = [
            'what is insurance', 'how does insurance work',
            'what is maturity benefit', 'explain insurance',
            'what is premium', 'what is claim'
        ]
        
        if any(q in user_input.lower() for q in general_questions):
            response = get_ai_response(user_input)
            return JsonResponse({
                'response': response,
                'level': 'general'
            })
        
        # Level 1: User Profiling
        profile_json = extract_user_profile(user_input)
        if not profile_json:
            return JsonResponse({
                'response': "I couldn't extract your profile details. Could you please provide more information about your age, occupation, income, and insurance needs?",
                'level': 'error'
            })
        
        # Level 2: Plan Recommendation
        recommendations = recommend_plans(profile_json)
        
        # Level 3: BFSI Explainer
        explanation = explain_bfsi_term(user_input)
        
        # Level 4: Plan Comparison
        comparison = compare_plans(recommendations)
        
        # Level 5: Final Summary
        summary = generate_summary(profile_json, recommendations)
        
        return JsonResponse({
            'response': {
                'profile': json.loads(profile_json),
                'recommendations': recommendations,
                'explanation': explanation,
                'comparison': comparison,
                'summary': summary
            },
            'level': 'full_analysis'
        })
        
    except Exception as e:
        return JsonResponse({
            'error': str(e)
        }, status=500)

def home(request):
    return render(request, 'advisor/home.html')

def chat_interface(request):
    return render(request, 'advisor/chat.html')