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
    if assertiveness >= 0.6:
        if tension >= 0.6:
            return "Competing (assertive, high tension)"
        else:
            return "Collaborating (assertive, constructive)"
    elif assertiveness >= 0.35:
        return "Compromising (moderate assertiveness/tension)"
    else:  # Low assertiveness
        if tension >= 0.35:
            return "Avoiding (withdrawal, anxious)"
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