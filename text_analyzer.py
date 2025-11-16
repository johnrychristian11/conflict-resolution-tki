from textblob import TextBlob


def analyze_sentiment(text):
    """
    Analyze text sentiment to determine tension and assertiveness.
    
    Args:
        text: Text string to analyze
        
    Returns:
        tuple: (tension, assertiveness) scores between 0 and 1
    """
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity
    
    # Tension from sentiment (negative = tense)
    sentiment_tension = 1 - ((polarity + 1) / 2)
    sentiment_tension += subjectivity * 0.2
    
    # Simple assertiveness from polarity
    text_assertiveness = 0.5  # Default neutral
    
    print(f"    [Sentiment]")
    print(f"      Polarity: {polarity:.2f}, Subjectivity: {subjectivity:.2f}")
    print(f"    [Text] Tension: {sentiment_tension:.3f}, Assertiveness: {text_assertiveness:.3f}")
    
    return min(sentiment_tension, 1.0), text_assertiveness