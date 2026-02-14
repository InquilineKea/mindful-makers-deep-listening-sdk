# Deep Listening Music SDK

A mindfulness-focused audio SDK for the **Deep Listening Mindful Makers Hack**. This collection of five mini-SDKs provides tools for meditation, emotional engagement with music, and mindful listening experiences.

## What is Deep Listening?

Deep Listening is a practice developed by composer Pauline Oliveros that involves listening with intention and awareness. It's about engaging with sound not just as background noise, but as a pathway to presence, meditation, and emotional connection.

This SDK brings Deep Listening principles to developers through:
- **Audio Analysis** - Understanding the meditative qualities of sound
- **Sound Discovery** - Finding the perfect ambient textures
- **Therapeutic Tones** - Generating binaural beats and isochronic tones
- **Voice Journaling** - Recording reflections and soundscapes
- **AI Generation** - Creating custom meditation music

## Installation

```bash
cd music
uv sync
cp .env.example .env  # Add your API keys
```

## Mini-SDKs

### 1. Librosa SDK - Audio Analysis for Mindfulness

Analyze audio to understand its meditative qualities.

```python
from librosa_sdk import MindfulAnalyzer

analyzer = MindfulAnalyzer("meditation_track.mp3")
features = analyzer.extract_meditation_features()
print(f"Tempo category: {features['tempo_category']}")  # "calming", "moderate", or "energizing"
print(f"Spectral warmth: {features['warmth']}")
```

See [librosa_sdk/README.md](librosa_sdk/README.md) for full documentation.

### 2. Freesound SDK - Discover Meditation Sounds

Search and download CC-licensed sounds for meditation.

```python
from freesound_sdk import FreesoundClient

client = FreesoundClient()
sounds = client.search_sounds("singing bowl", duration_range=(10, 30))
for sound in sounds[:5]:
    print(f"{sound['name']} - {sound['duration']}s")
```

**Requires:** Freesound API key (free at [freesound.org/apiv2/apply](https://freesound.org/apiv2/apply))

See [freesound_sdk/README.md](freesound_sdk/README.md) for full documentation.

### 3. WebAudio SDK - Therapeutic Tone Generation

Generate binaural beats and isochronic tones for meditation.

```python
from webaudio_sdk import BinauralGenerator, play_audio

generator = BinauralGenerator()
# Generate theta waves (4-8 Hz) for meditation
audio = generator.generate_binaural_beat(
    base_freq=200,
    beat_freq=6,  # Theta range
    duration=300  # 5 minutes
)
play_audio(audio)
```

See [webaudio_sdk/README.md](webaudio_sdk/README.md) for full documentation.

### 4. Recording SDK - Voice Journaling

Capture audio for journaling and soundscape creation.

```python
from recording_sdk import AudioRecorder

recorder = AudioRecorder()
# Record a 2-minute journal entry
audio = recorder.record_audio(duration=120)
recorder.save_recording(audio, "journal_entry.wav")
```

See [recording_sdk/README.md](recording_sdk/README.md) for full documentation.

### 5. ElevenLabs SDK - AI Meditation Music

Generate custom meditation music and nature sounds.

```python
from elevenlabs_sdk import MeditationGenerator

generator = MeditationGenerator()
audio = generator.generate_meditation_music(
    prompt="gentle piano with soft rain",
    duration_seconds=300
)
audio.save("morning_meditation.mp3")
```

**Requires:** ElevenLabs API key

See [elevenlabs_sdk/README.md](elevenlabs_sdk/README.md) for full documentation.

## Quick Start Examples

Run any example to see the SDK in action:

```bash
# Analyze audio (no API key needed)
uv run python librosa_sdk/example.py

# Generate binaural beats (no API key needed)
uv run python webaudio_sdk/example.py

# Record audio (no API key needed, requires microphone)
uv run python recording_sdk/example.py

# Search meditation sounds (requires Freesound API key)
uv run python freesound_sdk/example.py

# Generate AI music (requires ElevenLabs API key)
uv run python elevenlabs_sdk/example.py
```

## Brainwave Frequencies Reference

| Band | Frequency | State | Use Case |
|------|-----------|-------|----------|
| Delta | 0.5-4 Hz | Deep sleep | Sleep meditation |
| Theta | 4-8 Hz | Meditation, creativity | Deep meditation, visualization |
| Alpha | 8-14 Hz | Relaxation, calm focus | Light meditation, relaxation |
| Beta | 14-30 Hz | Active concentration | Focus sessions |

## License

MIT License - Built for the Deep Listening Mindful Makers Hack
