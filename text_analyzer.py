from textblob import TextBlob


# Compliance patterns - indicate accepting/accommodating behavior
ACCEPTANCE_KEYWORDS = {
    'ok', 'okay', 'yes', 'agree', 'agreed', 'will do', 'let us', 'let\'s do',
    'sounds good', 'that works', 'fine', 'alright', 'sure', 'absolutely',
    'certainly', 'understood', 'no problem', 'that\'s fine', 'acceptable',
    'i understand', 'makes sense', 'appreciate', 'thank you', 'thanks',
    'i accept', 'accepted', 'good', 'great', 'perfect', 'exactly'
}

# Collaborative/empathetic keywords
COLLABORATIVE_KEYWORDS = {
    'understand', 'frustration', 'solution', 'works for both',
    'find a solution', 'let\'s see', 'let us see', 'i understand',
    'empathy', 'help', 'work together', 'both of us', 'mutual'
}

# Demanding/assertive keywords
ASSERTIVE_KEYWORDS = {
    'need', 'must', 'have to', 'should', 'require', 'demand', 'insist',
    'postponed', 'twice', 'again', 'urgent', 'immediately', 'now',
    'schedule', 'today', 'asap'
}

RESISTANCE_KEYWORDS = {
    'but', 'however', 'disagree', 'no', 'never', 'cannot', 'can\'t', 'won\'t',
    'refuse', 'refuse', 'not', 'don\'t', 'doesn\'t', 'argument', 'problem',
    'issue', 'wrong', 'busy', 'later', 'delay', 'postpone'
}


def detect_compliance(text):
    """
    Detect if text shows compliance/acceptance patterns.
    
    Args:
        text: Text string to analyze
        
    Returns:
        float: Compliance score (0-1), higher = more accepting
    """
    text_lower = text.lower()
    words = set(text_lower.split())
    
    # Count acceptance vs resistance keywords
    acceptance_count = sum(1 for word in words if any(kw in word for kw in ACCEPTANCE_KEYWORDS))
    resistance_count = sum(1 for word in words if any(kw in word for kw in RESISTANCE_KEYWORDS))
    assertive_count = sum(1 for word in words if any(kw in word for kw in ASSERTIVE_KEYWORDS))
    
    # If acceptance keywords present and no resistance, high compliance
    if acceptance_count > 0 and resistance_count == 0:
        compliance = min(0.9 + (acceptance_count * 0.05), 1.0)
    # If resistance/assertive keywords present, low compliance
    elif resistance_count > 0 or assertive_count > 1:
        compliance = 0.1
    else:
        compliance = 0.5
    
    return compliance


def detect_collaboration(text):
    """
    Args:
        text: Text string to analyze
        
    Returns:
        float: Collaboration score (0-1), higher = more collaborative
    """
    text_lower = text.lower()
    
    collab_count = sum(1 for kw in COLLABORATIVE_KEYWORDS if kw in text_lower)
    
    if collab_count >= 2:
        return 0.9  # Strong collaboration signal
    elif collab_count == 1:
        return 0.7
    else:
        return 0.0


def detect_compliance(text):
    """
    Detect if text shows compliance/acceptance patterns.
    
    Args:
        text: Text string to analyze
        
    Returns:
        float: Compliance score (0-1), higher = more accepting
    """
    text_lower = text.lower()
    words = set(text_lower.split())
    
    # Count acceptance vs resistance keywords
    acceptance_count = sum(1 for word in words if any(kw in word for kw in ACCEPTANCE_KEYWORDS))
    resistance_count = sum(1 for word in words if any(kw in word for kw in RESISTANCE_KEYWORDS))
    assertive_count = sum(1 for word in words if any(kw in word for kw in ASSERTIVE_KEYWORDS))
    
    # If acceptance keywords present and no resistance, high compliance
    if acceptance_count > 0 and resistance_count == 0:
        compliance = min(0.9 + (acceptance_count * 0.05), 1.0)
    # If resistance/assertive keywords present, low compliance
    elif resistance_count > 0 or assertive_count > 1:
        compliance = 0.1
    else:
        compliance = 0.5
    
    return compliance


def detect_avoidance(text):
    """
    Detect if text shows avoidance/withdrawal patterns (asking to postpone, delay, etc).
    
    Args:
        text: Text string to analyze
        
    Returns:
        float: Avoidance score (0-1), higher = more avoiding
    """
    text_lower = text.lower()
    
    # Strong avoidance indicators
    strong_avoidance = {'can we discuss', 'can we', 'later?', 'busy right now', 'busy'}
    strong_count = sum(1 for kw in strong_avoidance if kw in text_lower)
    
    # Weak avoidance indicators (but could be assertive context)
    weak_avoidance = {'postponed', 'delay'}
    weak_count = sum(1 for kw in weak_avoidance if kw in text_lower)
    
    # If speaker is saying they want to postpone (weak), it's avoidance
    # If speaker is complaining about postponement (weak), it's assertive
    if 'postponed' in text_lower or 'delay' in text_lower:
        # Check if complaining or demanding action (assertive context)
        assertive_words = {'twice', 'already', 'schedule', 'today', 'need'}
        if any(word in text_lower for word in assertive_words):
            weak_count = 0  # This is assertive, not avoidant
    
    # Combine scores
    if strong_count >= 2:
        return 0.95  # Very strong avoidance
    elif strong_count >= 1:
        return 0.80  # Strong avoidance
    elif weak_count > 0:
        return 0.30  # Weak signal, not primary indicator
    else:
        return 0.0


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
    
    # Get compliance, collaboration, and avoidance scores
    compliance = detect_compliance(text)
    collaboration = detect_collaboration(text)
    avoidance = detect_avoidance(text)
    
    if collaboration > 0.6:
        # Collaborative/empathetic tone - moderate to low assertiveness
        text_assertiveness = 0.35
    elif avoidance > 0.7:
        # Strong avoidance pattern - very low assertiveness
        text_assertiveness = 0.15
    elif compliance > 0.8:
        # Pure acceptance - low assertiveness
        text_assertiveness = 0.25
    else:
        # Default: neutral to assertive
        text_assertiveness = 0.65
    
    print(f"    [Sentiment]")
    print(f"      Polarity: {polarity:.2f}, Subjectivity: {subjectivity:.2f}")
    print(f"    [Compliance] Score: {compliance:.3f}, [Avoidance] Score: {avoidance:.3f}, [Collaboration] Score: {collaboration:.3f}")
    print(f"    [Text] Tension: {sentiment_tension:.3f}, Assertiveness: {text_assertiveness:.3f}")
    
    return min(sentiment_tension, 1.0), text_assertiveness