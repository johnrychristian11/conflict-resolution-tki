from audio_analyzer import analyze_prosody
from text_analyzer import analyze_sentiment


def compute_tension_and_assertiveness(text, audio_path):
    """
    Computes final tension and assertiveness scores by fusing audio and text analysis.
    
    Args:
        text: Text string to analyze
        audio_path: Path to audio file
        
    Returns:
        tuple: (tension, assertiveness) scores between 0 and 1
    """
    print(f"  Analyzing: '{text[:60]}...'")
    
    text_tension, text_assertiveness = analyze_sentiment(text)
    audio_tension, audio_assertiveness = analyze_prosody(audio_path)
    
    # Audio is reliable for tension (pitch/energy patterns)
    # Text compliance is more reliable for assertiveness (semantic acceptance)
    final_tension = (0.4 * text_tension) + (0.6 * audio_tension)
    final_assertiveness = (0.4 * text_assertiveness) + (0.6 * audio_assertiveness)
    
    print(f"    [FINAL] Tension: {final_tension:.3f}, Assertiveness: {final_assertiveness:.3f}\n")
    
    return round(final_tension, 2), round(final_assertiveness, 2)