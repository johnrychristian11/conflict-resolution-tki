from google import genai

def generate_resolution(conversation_analysis, api_key):
    """
    Generate conflict resolution suggestions using Gemini API.
    
    Args:
        conversation_analysis: List of dicts with person, text, tension, assertiveness, style
        api_key: Google API key
        
    Returns:
        str: AI-generated resolution suggestions
    """
    try:
        client = genai.Client(api_key=api_key)
        
        # Build conversation summary for prompt
        conversation_summary = ""
        for i, turn in enumerate(conversation_analysis, 1):
            conversation_summary += f"Turn {i} - {turn['person']}:\n"
            conversation_summary += f"  Text: \"{turn['text']}\"\n"
            conversation_summary += f"  Tension: {turn['tension']}, Assertiveness: {turn['assertiveness']}\n"
            conversation_summary += f"  TKI Style: {turn['style']}\n\n"
        
        # Create prompt
        prompt = f"""You are a conflict resolution expert analyzing a workplace conversation using the Thomas-Kilmann Conflict Mode Instrument (TKI).
            Here is the conversation analysis:
            {conversation_summary}

            Based on the TKI styles and tension/assertiveness scores:

            1. Suggest 1 or 2 specific, actionable resolution strategies that consider each person's conflict style
            2. Recommend how each person could adjust their approach for better outcomes
            Keep your response concise, practical, and focused on de-escalation."""

        # Generate response
        response = client.models.generate_content(
            model="gemini-2.0-flash", 
            contents=prompt
        )
        return response.text
        
    except Exception as e:
        return f"Error generating resolution: {e}\n\nPlease ensure you have set your GOOGLE_API_KEY environment variable or pass it directly."