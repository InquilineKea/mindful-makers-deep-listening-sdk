# WebAudio SDK - Therapeutic Tone Generation

Generate binaural beats and isochronic tones for meditation and brainwave entrainment.

## How It Works

### Binaural Beats
When you play two slightly different frequencies in each ear (via headphones), your brain perceives a third "beat" frequency equal to the difference. This can help entrain your brainwaves to specific states.

### Isochronic Tones
Rhythmic pulses of a single tone that work through regular speakers. The brain synchronizes to the pulse rate.

## Brainwave Frequencies

| Band | Frequency | State | Use Case |
|------|-----------|-------|----------|
| Delta | 0.5-4 Hz | Deep sleep, healing | Sleep meditation, recovery |
| Theta | 4-8 Hz | Meditation, creativity | Deep meditation, visualization |
| Alpha | 8-14 Hz | Relaxation, calm focus | Light meditation, relaxation |
| Beta | 14-30 Hz | Active concentration | Focus sessions, studying |

## Usage

### Generate Binaural Beats

```python
from webaudio_sdk import BinauralGenerator, play_audio, save_audio

generator = BinauralGenerator(sample_rate=44100)

# Generate theta waves for meditation
audio = generator.generate_binaural_beat(
    base_freq=200,    # Carrier frequency
    beat_freq=6,      # Desired brainwave frequency (Theta)
    duration=300,     # 5 minutes
    fade_duration=5   # 5 second fade in/out
)

# Play with headphones!
play_audio(audio)

# Or save to file
save_audio(audio, "theta_meditation.wav")
```

### Use Presets

```python
# Available presets
generator.list_presets()
# {
#   'deep_sleep': 'Delta waves for deep sleep',
#   'meditation': 'Theta waves for deep meditation',
#   'relaxation': 'Alpha waves for relaxation',
#   'focus': 'Beta waves for concentration',
#   'creativity': 'Theta-Alpha border for creativity'
# }

# Generate from preset
audio = generator.generate_from_preset("meditation", duration=600)  # 10 minutes
```

### Generate Isochronic Tones

```python
# Works with regular speakers (no headphones needed)
audio = generator.generate_isochronic_tones(
    freq=300,         # Tone frequency
    pulse_rate=10,    # Alpha range
    duration=300,     # 5 minutes
    duty_cycle=0.5    # 50% on/off
)
```

### Layered Binaural Beats

Combine multiple frequencies for complex entrainment:

```python
layers = [
    {"base_freq": 150, "beat_freq": 4, "amplitude": 0.5},   # Theta
    {"base_freq": 300, "beat_freq": 10, "amplitude": 0.5},  # Alpha
]

audio = generator.generate_layered_binaural(layers, duration=300)
```

### Playback Controls

```python
from webaudio_sdk import play_audio, stop_playback, get_audio_devices

# List available devices
devices = get_audio_devices()
print(devices['output'])

# Non-blocking playback
play_audio(audio, blocking=False)

# Stop playback
stop_playback()
```

## Tips for Effective Sessions

1. **Use headphones** - Required for binaural beats (each ear needs different frequency)
2. **Quiet environment** - Minimize distractions
3. **Comfortable position** - Sit or lie down comfortably
4. **Close your eyes** - Focus inward
5. **Session length** - 15-30 minutes is ideal
6. **Consistency** - Regular practice increases effectiveness

## Safety Notes

- Binaural beats are generally safe for most people
- Avoid if you have epilepsy or are prone to seizures
- Start with shorter sessions (5-10 minutes)
- Discontinue if you experience discomfort

## Example

Run the example to hear binaural beats in action:

```bash
uv run python webaudio_sdk/example.py
```
