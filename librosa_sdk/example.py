"""Example: Analyze audio for meditation suitability."""

import numpy as np

from librosa_sdk import MindfulAnalyzer


def generate_sample_audio(duration: float = 10.0, sr: int = 22050) -> np.ndarray:
    """Generate a simple ambient-style audio sample for demonstration.

    Creates a warm, low-frequency drone with subtle modulation.
    """
    t = np.linspace(0, duration, int(sr * duration))

    # Base drone at 110 Hz (warm, grounding frequency)
    drone = 0.3 * np.sin(2 * np.pi * 110 * t)

    # Add subtle harmonics
    drone += 0.15 * np.sin(2 * np.pi * 220 * t)
    drone += 0.08 * np.sin(2 * np.pi * 330 * t)

    # Slow amplitude modulation for breathing quality
    modulation = 0.7 + 0.3 * np.sin(2 * np.pi * 0.1 * t)
    drone *= modulation

    # Fade in/out
    fade_samples = int(sr * 0.5)
    fade_in = np.linspace(0, 1, fade_samples)
    fade_out = np.linspace(1, 0, fade_samples)
    drone[:fade_samples] *= fade_in
    drone[-fade_samples:] *= fade_out

    return drone.astype(np.float32)


def main():
    print("=" * 60)
    print("Librosa SDK - Mindful Audio Analysis Demo")
    print("=" * 60)
    print()

    # Generate sample audio
    print("Generating sample meditation audio...")
    sr = 22050
    audio = generate_sample_audio(duration=10.0, sr=sr)
    print("  Duration: 10 seconds")
    print(f"  Sample rate: {sr} Hz")
    print()

    # Create analyzer and load audio
    analyzer = MindfulAnalyzer()
    analyzer.load_from_array(audio, sr)

    # Analyze tempo
    print("Tempo Analysis:")
    print("-" * 40)
    tempo = analyzer.analyze_tempo()
    print(f"  BPM: {tempo['bpm']}")
    print(f"  Category: {tempo['category']}")
    print(f"  {tempo['description']}")
    print()

    # Analyze spectral warmth
    print("Spectral Warmth Analysis:")
    print("-" * 40)
    warmth = analyzer.analyze_spectral_warmth()
    print(f"  Spectral centroid: {warmth['centroid_hz']} Hz")
    print(f"  Warmth score: {warmth['warmth_score']} (0=bright, 1=warm)")
    print(f"  Character: {warmth['character']}")
    print(f"  {warmth['description']}")
    print()

    # Full meditation features
    print("Full Meditation Feature Analysis:")
    print("-" * 40)
    features = analyzer.extract_meditation_features()
    print(f"  Tempo: {features['tempo_bpm']} BPM ({features['tempo_category']})")
    print(f"  Warmth: {features['warmth_score']} ({features['warmth_character']})")
    print(f"  Dynamics: {features['dynamics']}")
    print(f"  Timbral complexity: {features['timbral_complexity']}")
    print(f"  Percussiveness: {features['percussiveness']}")
    print(f"  Meditation score: {features['meditation_score']}")
    print(f"  Suitability: {features['suitability'].upper()}")
    print()

    # Detect silence gaps
    print("Silence Gap Detection:")
    print("-" * 40)
    gaps = analyzer.detect_silence_gaps(min_silence_ms=200)
    if gaps:
        for i, gap in enumerate(gaps[:5]):  # Show first 5
            print(
                f"  Gap {i + 1}: {gap['start_sec']}s - {gap['end_sec']}s ({gap['duration_sec']}s)"
            )
    else:
        print("  No significant silence gaps detected (continuous audio)")
    print()

    # Harmonic/Percussive separation
    print("Harmonic/Percussive Separation:")
    print("-" * 40)
    harmonic, percussive = analyzer.separate_harmonic_percussive()
    harmonic_energy = np.mean(np.abs(harmonic))
    percussive_energy = np.mean(np.abs(percussive))
    total = harmonic_energy + percussive_energy
    print(f"  Harmonic content: {harmonic_energy / total * 100:.1f}%")
    print(f"  Percussive content: {percussive_energy / total * 100:.1f}%")
    print()

    print("=" * 60)
    print("Analysis complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
