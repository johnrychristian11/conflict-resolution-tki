"""
Audio prosody analysis module for conflict detection.
Analyzes speech patterns including energy, pitch, and pauses.
"""

import librosa
import numpy as np


def analyze_prosody(audio_path):
    """
    Analyze audio prosody to determine tension and assertiveness.
    
    Args:
        audio_path: Path to audio file
        
    Returns:
        tuple: (tension, assertiveness) scores between 0 and 1
    """
    if audio_path is None:
        return 0.0, 0.5
    
    try:
        y, sr = librosa.load(audio_path, sr=None)
        
        # 1. Pitch analysis
        pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
        pitch_values = []
        for t in range(pitches.shape[1]):
            index = magnitudes[:, t].argmax()
            pitch = pitches[index, t]
            if pitch > 0:
                pitch_values.append(pitch)
        pitch_values = np.array(pitch_values)
        
        if len(pitch_values) > 0:
            pitch_mean = np.mean(pitch_values)
            pitch_std = np.std(pitch_values)
        else:
            pitch_mean = 0
            pitch_std = 0
        
        # 2. RMS Energy frame-by-frame
        rms = librosa.feature.rms(y=y)[0]
        energy_mean = np.mean(rms)
        energy_std = np.std(rms)
        energy_max = np.max(rms)
        
        # 3. Detect pauses/silence
        energy_threshold = energy_mean * 0.4
        low_energy_frames = np.sum(rms < energy_threshold)
        silence_ratio = low_energy_frames / len(rms)
        
        # 4. Speech continuity
        speech_frames = np.sum(rms > energy_mean * 0.2)
        speech_ratio = speech_frames / len(rms)
        
        # 5. Speaking rate
        zcr = np.mean(librosa.feature.zero_crossing_rate(y))
        
        # 6. Spectral features
        spectral_centroid = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))
        
        # 7. Sustained energy
        high_energy_threshold = energy_mean * 1.5
        sustained_energy_frames = 0
        current_streak = 0
        for val in rms:
            if val > high_energy_threshold:
                current_streak += 1
            else:
                sustained_energy_frames = max(sustained_energy_frames, current_streak)
                current_streak = 0
        sustained_energy_ratio = sustained_energy_frames / len(rms)
        
        # Calculate assertiveness
        energy_score = min(energy_mean / 0.08, 1.0)
        sustained_score = min(sustained_energy_ratio / 0.3, 1.0)
        
        assertiveness = (
            0.40 * energy_score +
            0.30 * sustained_score +
            0.20 * speech_ratio +
            0.10 * (1 - silence_ratio)
        )
        
        # Penalize stuttering/pauses
        if silence_ratio > 0.3:
            assertiveness *= 0.5
        
        # Calculate tension
        pitch_var_score = min(pitch_std / 50.0, 1.0)
        energy_var_score = min(energy_std / 0.05, 1.0)
        
        weighted_pitch_var = pitch_var_score * min(energy_score * 1.5, 1.0)
        weighted_energy_var = energy_var_score * min(energy_score * 1.5, 1.0)
        
        tension = (
            0.20 * energy_score +
            0.30 * weighted_pitch_var +
            0.30 * weighted_energy_var +
            0.10 * min(zcr / 0.15, 1.0) +
            0.10 * min(spectral_centroid / 3000.0, 1.0)
        )
        
        _print_debug_info(pitch_mean, pitch_std, energy_mean, energy_std, 
                         energy_max, silence_ratio, energy_threshold, 
                         speech_ratio, sustained_energy_ratio, 
                         weighted_pitch_var, weighted_energy_var, 
                         tension, assertiveness)
        
        return tension, assertiveness
        
    except Exception as e:
        print(f"Audio error: {e}")
        return 0.0, 0.5


def _print_debug_info(pitch_mean, pitch_std, energy_mean, energy_std, 
                     energy_max, silence_ratio, energy_threshold, 
                     speech_ratio, sustained_energy_ratio, 
                     weighted_pitch_var, weighted_energy_var, 
                     tension, assertiveness):
    """Print detailed prosody analysis debug information."""
    print(f"    [Prosody Debug]")
    print(f"      Pitch: {pitch_mean:.1f}Hz (std: {pitch_std:.1f})")
    print(f"      Energy: mean={energy_mean:.4f}, std={energy_std:.4f}, max={energy_max:.4f}")
    print(f"      Silence ratio: {silence_ratio:.3f} (threshold: {energy_threshold:.4f})")
    print(f"      Speech ratio: {speech_ratio:.3f}")
    print(f"      Sustained energy ratio: {sustained_energy_ratio:.3f}")
    print(f"      Weighted variance - Pitch: {weighted_pitch_var:.3f}, Energy: {weighted_energy_var:.3f}")
    print(f"    [Prosody] Tension: {tension:.3f}, Assertiveness: {assertiveness:.3f}")