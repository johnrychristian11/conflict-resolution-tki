import os
from analyzer import compute_tension_and_assertiveness
from tki_mapper import map_tki_style
from ai_resolution import generate_resolution
from input import SAMPLE_CONVERSATION


def analyze_conversation(conversation):
    """
    Analyze a full conversation and return analysis results.
    
    Args:
        conversation: List of dicts with 'person', 'text', and 'audio' keys
        
    Returns:
        list: Analysis results for each turn
    """
    conversation_analysis = []
    
    for i, turn in enumerate(conversation, 1):
        print(f"Turn {i}: {turn['person']}")
        
        tension, assertiveness = compute_tension_and_assertiveness(
            turn['text'], 
            turn['audio']
        )
        
        style = map_tki_style(tension, assertiveness)
        
        print(f"→ TENSION: {tension}, ASSERTIVENESS: {assertiveness}")
        print(f"→ TKI STYLE: {style}")
        print("-" * 70)
        
        conversation_analysis.append({
            'person': turn['person'],
            'text': turn['text'],
            'tension': tension,
            'assertiveness': assertiveness,
            'style': style
        })
    
    return conversation_analysis


def main():
    """Main execution function."""
    print("=== TKI Conversation Analysis (Audio-Focused) ===\n")
    
    # Analyze conversation
    conversation_analysis = analyze_conversation(SAMPLE_CONVERSATION)
    
    # Generate AI resolution
    print("\n" + "=" * 70)
    print("=== AI-DRIVEN CONFLICT RESOLUTION ===")
    print("=" * 70 + "\n")
    
    # Get API key from environment
    api_key = os.getenv('GOOGLE_API_KEY')
    
    if not api_key:
        print("No API key found. Please set GOOGLE_API_KEY environment variable")
        print("Example: export GOOGLE_API_KEY='your-api-key-here'")
        print("Or get one from: https://makersuite.google.com/app/apikey")
    else:
        resolution = generate_resolution(conversation_analysis, api_key)
        print(resolution)


if __name__ == "__main__":
    main()