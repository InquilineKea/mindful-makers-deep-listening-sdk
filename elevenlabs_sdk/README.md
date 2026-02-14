# ElevenLabs SDK - AI Meditation Music Generation

Generate custom meditation music, nature sounds, and transition effects using ElevenLabs' AI sound generation.

## Setup

1. Get an API key at [elevenlabs.io](https://elevenlabs.io)
2. Add to your `.env` file:
   ```
   ELEVENLABS_API_KEY=your_key_here
   ```

## Features

- **Meditation Music** - Generate ambient, peaceful music from text descriptions
- **Nature Sounds** - Create rain, ocean, forest, and other nature soundscapes
- **Transition Sounds** - Generate bells, chimes, and bowls for meditation cues
- **Presets** - Curated prompts for common meditation styles
- **Session Generation** - Create complete meditation sessions with intro/outro

## Usage

### Generate Meditation Music

```python
from elevenlabs_sdk import MeditationGenerator

generator = MeditationGenerator()

# Generate custom meditation music
audio = generator.generate_meditation_music(
    prompt="gentle piano with soft synthesizer pads, peaceful morning",
    duration_seconds=300  # 5 minutes
)

# Save to file
audio.save("morning_meditation.mp3")

# Or get raw bytes for streaming
audio_bytes = audio.get_bytes()
```

### Generate Nature Sounds

```python
# Rain sounds
rain = generator.generate_nature_sound(
    description="gentle rain on a tin roof",
    duration_seconds=600
)
rain.save("rain.mp3")

# Ocean waves
ocean = generator.generate_nature_sound(
    description="calm ocean waves on a tropical beach",
    duration_seconds=600
)
ocean.save("ocean.mp3")
```

### Use Presets

Curated prompts optimized for meditation:

```python
# List available presets
presets = generator.list_presets()
# {
#   'morning_meditation': 'Peaceful piano for morning meditation',
#   'deep_relaxation': 'Deep ambient drones for relaxation',
#   'nature_rain': 'Gentle rain for focus and sleep',
#   'ocean_waves': 'Ocean waves for relaxation',
#   'forest_morning': 'Forest sounds with birdsong',
#   'tibetan_bowls': 'Singing bowls and bells',
#   'breathing_guide': 'Rhythmic tones for breath pacing',
#   'sleep_music': 'Ultra-soft music for sleep'
# }

# Generate from preset
audio = generator.generate_from_preset(
    preset="deep_relaxation",
    duration_seconds=600
)
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

### Generate Complete Sessions

Create intro, main, and outro in one call:

```python
session = generator.generate_session(
    intro_seconds=30,
    main_seconds=600,
    outro_seconds=30,
    main_prompt="peaceful ambient music with soft nature sounds"
)

# Save each part
session['intro'].save("session_intro.mp3")
session['main'].save("session_main.mp3")
session['outro'].save("session_outro.mp3")

print(f"Total duration: {session['total_duration']} seconds")
```

### Working with Audio Data

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
5. **Layer sounds** - Combine music and nature sounds in prompts

### Example Prompts

```python
# Deep relaxation
"extremely slow ambient drones, warm evolving pads, no rhythm, hypnotic"

# Focus session
"soft lo-fi piano with gentle rain, minimal, focused"

# Sleep music
"barely audible ambient tones, soft warm frequencies, perfect for sleep"

# Nature meditation
"forest stream with distant bird songs, morning sunlight atmosphere"
```

## Example

Run the example to generate sample meditation music:

```bash
uv run python elevenlabs_sdk/example.py
```
