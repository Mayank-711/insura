from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from .utils import *
from .utils import (
    contains_profanity,
    get_ai_response,
    extract_user_profile,
    recommend_plans,
    explain_bfsi_term,
    compare_plans,
    generate_summary
)


# @csrf_exempt
# def chat(request):
#     if request.method != 'POST':
#         return JsonResponse({'error': 'Only POST allowed'}, status=405)
    
#     try:
#         data = json.loads(request.body)
#         user_input = data.get('message', '').strip()
        
#         if not user_input:
#             return JsonResponse({'error': 'Empty message'}, status=400)
        
#         if contains_profanity(user_input):
#             return JsonResponse({
#                 'messages': [
#                     {"role": "bot", "text": "I'm sorry, but I can't respond to that language. Please rephrase your question professionally."}
#                 ]
#             })

#         # Handle general BFSI questions (Gemini Level 0)
#         explanation = explain_bfsi_term(user_input)
#         if explanation:
#             return JsonResponse({
#                 'messages': [
#                     {"role": "bot", "text": explanation}
#                 ]
#             })

#         # --- Level 1: User Profiling ---
#         profile_json = extract_user_profile(user_input)
#         if not profile_json:
#             return JsonResponse({
#                 'messages': [
#                     {"role": "bot", "text": "I couldn't extract your profile details. Please tell me your age, income, goals, and dependents."}
#                 ]
#             })

#         # --- Level 2: Plan Recommendation ---
#         recommendations = recommend_plans(profile_json)

#         # --- Level 3: BFSI Explanation ---
#         bfs_info = explain_bfsi_term(user_input) or "No specific terms to explain."

#         # --- Level 4: Plan Comparison ---
#         comparison = compare_plans(recommendations)

#         # --- Level 5: Final Summary ---
#         summary = generate_summary(profile_json, recommendations)

#         return JsonResponse({
#             'messages': [
#                 {"role": "bot", "text": "Step 1: Here's the extracted profile:\n" + profile_json},
#                 {"role": "bot", "text": "Step 2: Insurance Recommendations:\n" + recommendations},
#                 {"role": "bot", "text": "Step 3: Explanation of Terms (if any):\n" + bfs_info},
#                 {"role": "bot", "text": "Step 4: Comparison of Plans:\n" + comparison},
#                 {"role": "bot", "text": "Step 5: Summary & Next Steps:\n" + summary}
#             ]
#         })
        
#     except Exception as e:
#         return JsonResponse({
#             'messages': [
#                 {"role": "bot", "text": f"Oops! Something went wrong: {str(e)}"}
#             ]
#         })

def home(request):
    return render(request, 'advisor/home.html')

def chat_interface(request):
    return render(request, 'advisor/chat.html')


@csrf_exempt
def chat(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST allowed'}, status=405)

    try:
        data = json.loads(request.body)
        full_message = data.get('message', '').strip()
        user_messages = data.get('userchat', [])
        full_message = "\n".join(user_messages).strip()
        if not full_message:
            return JsonResponse({'error': 'Empty message'}, status=400)

        if contains_profanity(full_message):
            return JsonResponse({
                'messages': [
                    {"role": "bot", "text": "I'm sorry, but I can't respond to that language. Please rephrase your question professionally."}
                ]
            })

        # Check for BFSI term explanation
        explanation = explain_bfsi_term(full_message)
        if explanation:
            return JsonResponse({
                'messages': [
                    {"role": "bot", "text": explanation}
                ]
            })

        # Extract full profile using all context (history)
        profile_json = extract_user_profile(full_message)
        if not profile_json:
            return JsonResponse({
                'messages': [
                    {"role": "bot", "text": "I couldn't extract your profile details. Please tell me your age, income, goals, and dependents."}
                ]
            })

        # Recommendation, comparison, summary using context
        recommendations = recommend_plans(profile_json)
        comparison = compare_plans(recommendations)
        summary = generate_summary(profile_json, recommendations)
        bfs_info = explain_bfsi_term(full_message) or "No specific BFSI terms to explain."

        return JsonResponse({
            'messages': [
                # {"role": "bot", "text": "" + profile_json.replace('\n', '<br>')},
                {"role": "bot", "text": "" + recommendations.replace('\n', '<br>')},
                {"role": "bot", "text": "" + bfs_info.replace('\n', '<br>')},
                {"role": "bot", "text": "" + comparison.replace('\n', '<br>')},
                {"role": "bot", "text": "" + summary.replace('\n', '<br>')}
            ]
        })

    except Exception as e:
        return JsonResponse({
            'messages': [
                {"role": "bot", "text": f"Oops! Something went wrong: {str(e)}"}
            ]
        })
