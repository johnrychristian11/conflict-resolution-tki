def map_tki_style(tension, assertiveness):
    """
    Map tension and assertiveness scores to TKI conflict styles.
    
    TKI model: Assertiveness vs Cooperativeness
    We use: Assertiveness vs Tension (inverse of cooperation)
    
    Args:
        tension: Tension score (0-1)
        assertiveness: Assertiveness score (0-1)
        
    Returns:
        str: TKI conflict style description
    """
    # Competing: High assertiveness + High tension
    if assertiveness >= 0.60 and tension >= 0.75:
        return "Competing (assertive, high tension)"
    
    # Collaborating: Medium-high assertiveness + Low tension
    if assertiveness >= 0.50 and tension < 0.65:
        return "Collaborating (assertive, constructive)"
    
    # Compromising: Medium assertiveness + Medium tension
    if assertiveness >= 0.45 and assertiveness < 0.60 and tension >= 0.50:
        return "Compromising (moderate assertiveness/tension)"
    
    # Avoiding: Low assertiveness + High tension
    if assertiveness < 0.45 and tension >= 0.55:
        return "Avoiding (withdrawal, anxious)"
    
    # Accommodating: Low assertiveness + Low tension
    if assertiveness < 0.45 and tension < 0.55:
        return "Accommodating (yielding, low tension)"
    
    # Default fallback based on assertiveness
    if assertiveness >= 0.55:
        return "Collaborating (assertive, constructive)"
    else:
        return "Accommodating (yielding, low tension)"


def debug_tki_mapping(tension, assertiveness):
    """
    Debug function to show TKI mapping logic.
    
    Args:
        tension: Tension score (0-1)
        assertiveness: Assertiveness score (0-1)
    """
    print(f"    [TKI Debug] Tension={tension:.2f}, Assertiveness={assertiveness:.2f}")
    print(f"    [TKI Debug] Assertiveness >= 0.6? {assertiveness >= 0.6}")
    print(f"    [TKI Debug] Assertiveness >= 0.35? {assertiveness >= 0.35}")
    if assertiveness < 0.35:
        print(f"    [TKI Debug] Low assertiveness - checking tension >= 0.35: {tension >= 0.35}")