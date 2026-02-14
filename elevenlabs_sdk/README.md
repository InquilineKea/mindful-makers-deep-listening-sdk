# ElevenLabs SDK - AI Meditation Audio Generation

Generate custom meditation sounds and music using ElevenLabs' AI audio generation.

## Setup

1. Get an API key at [elevenlabs.io](https://elevenlabs.io)
2. Add to your `.env` file:
   ```
   ELEVENLABS_API_KEY=your_key_here
   ```

## Features

- **Sound Effects** - Generate nature sounds, bells, chimes, and ambient textures
- **Music Generation** - Create original meditation music with the Music API (requires paid plan)
- **Presets** - Curated prompts for common meditation sounds
- **Session Generation** - Create complete meditation sessions with intro/outro

## Sound Effects (example.py)

Uses the Text-to-Sound-Effects API to generate meditation sounds.

### Generate Nature Sounds

```python
from elevenlabs_sdk import MeditationGenerator

generator = MeditationGenerator()

# Rain sounds
rain = generator.generate_nature_sound(
    description="gentle rain on leaves",
    duration_seconds=60
)
rain.save("rain.mp3")

# Ocean waves
ocean = generator.generate_nature_sound(
    description="calm ocean waves on a sandy beach",
    duration_seconds=60
)
ocean.save("ocean.mp3")
```

### Generate Transition Sounds

Perfect for marking meditation phases:

```python
# Available types: "bell", "chime", "bowl", "gong"
bell = generator.generate_transition_sound(
    sound_type="bowl",
    duration_seconds=5
)
bell.save("session_start.mp3")
```

### Use Sound Presets

```python
# List available presets
presets = generator.list_presets()
# Includes: nature_rain, ocean_waves, forest_morning, tibetan_bowls, etc.

# Generate from preset
audio = generator.generate_from_preset(
    preset="ocean_waves",
    duration_seconds=60
)
audio.save("ocean.mp3")
```

## Music Generation (example_music.py)

Uses the new ElevenLabs Music API to generate original meditation music. Requires a paid ElevenLabs plan.

### Generate Music from Prompts

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(api_key="your_key")

# Generate meditation music
audio_data = client.music.compose(
    prompt="peaceful ambient meditation music with soft piano, slow tempo",
    music_length_ms=60000,  # 60 seconds
    model_id="music_v1",
    force_instrumental=True,  # No vocals
)

# Save the streamed audio
with open("meditation.mp3", "wb") as f:
    for chunk in audio_data:
        f.write(chunk)
```

### Music API Parameters

| Parameter | Description |
|-----------|-------------|
| `prompt` | Text description of the music to generate |
| `music_length_ms` | Duration in milliseconds (3000-300000) |
| `model_id` | Use `"music_v1"` |
| `force_instrumental` | Set `True` to ensure no vocals |

### Example Music Prompts

```python
# Deep relaxation
"deep ambient drone, warm synthesizer pads, evolving textures, no rhythm"

# Morning meditation
"gentle acoustic guitar and flute, peaceful sunrise atmosphere, hopeful"

# Focus music
"soft lo-fi piano, minimal ambient, calm and focused"

# Sleep music
"extremely soft ambient tones, barely audible, warm frequencies"
```

## Working with Generated Audio

```python
# Save to file
audio.save("meditation.mp3")

# Get raw bytes
raw_bytes = audio.get_bytes()

# Get as BytesIO for streaming
buffer = audio.get_bytesio()

# Access metadata
print(f"Prompt: {audio.prompt}")
print(f"Duration: {audio.duration_seconds}s")
```

## Tips for Better Results

1. **Be descriptive** - More detail in prompts leads to better results
2. **Specify mood** - Include words like "peaceful", "calm", "gentle"
3. **Mention instruments** - "soft piano", "ambient synthesizer", "tibetan bowls"
4. **Avoid rhythm for relaxation** - Add "no beat" or "no rhythm" for deeper meditation

## Examples

Run the sound effects demo:
```bash
uv run python elevenlabs_sdk/example.py
```

Run the music generation demo:
```bash
uv run python elevenlabs_sdk/example_music.py
```
