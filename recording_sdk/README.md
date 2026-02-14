# Recording SDK - Voice Journaling & Soundscape Capture

Record audio from your microphone for voice journaling, soundscape creation, and mindfulness documentation.

## Features

- **Fixed Duration Recording** - Record for a specific length of time
- **Auto-Stop Recording** - Automatically stop when silence is detected
- **Continuous Recording** - Start/stop manually for flexible capture
- **Device Selection** - Choose which microphone to use
- **Level Monitoring** - Test your microphone setup

## Usage

### Basic Recording

```python
from recording_sdk import AudioRecorder

recorder = AudioRecorder(sample_rate=44100, channels=1)

# Record for 2 minutes
audio = recorder.record_audio(duration=120)

# Save the recording
recorder.save_recording(audio, "journal_entry.wav")
```

### Auto-Stop on Silence

Perfect for voice journaling where you want to speak freely and have the recording stop automatically:

```python
# Record until 2 seconds of silence
audio = recorder.record_until_silence(
    silence_threshold=0.01,  # Adjust based on background noise
    silence_duration=2.0,    # Seconds of silence before stopping
    timeout=300.0,           # Maximum recording time (5 minutes)
    min_duration=1.0         # Minimum recording before checking silence
)
```

### Manual Start/Stop

For more control over when recording happens:

```python
# Start recording
recorder.start_recording()

# ... do other things, perhaps during a meditation session ...

# Stop and get the audio
audio = recorder.stop_recording()
recorder.save_recording(audio, "meditation_sounds.wav")
```

### Device Selection

```python
# List available microphones
devices = recorder.get_audio_devices()
for device in devices['devices']:
    print(f"[{device['index']}] {device['name']}")

# Select a specific microphone
recorder.set_input_device(device_index=2)
```

### Test Microphone Level

```python
# Check if microphone is working
level = recorder.get_input_level(duration=2.0)
print(f"Input level: {level:.2f}")  # 0.0 = silence, 1.0 = loud
```

### Stereo Recording

```python
# Record in stereo for ambient soundscapes
recorder = AudioRecorder(sample_rate=44100, channels=2)
audio = recorder.record_audio(duration=60)
```

## Voice Journaling Ideas

1. **Morning Intentions** - Record your intention for the day
2. **Gratitude Practice** - Speak three things you're grateful for
3. **Evening Reflection** - Summarize your day's mindfulness moments
4. **Breath Observations** - Describe your breathing patterns
5. **Emotion Check-in** - Name and describe current emotions
6. **Soundscape Diary** - Capture ambient sounds from meaningful places

## File Formats

Supported formats for saving:
- WAV (default, lossless)
- FLAC (lossless, compressed)
- OGG (lossy, smaller files)

```python
recorder.save_recording(audio, "journal.wav")    # WAV
recorder.save_recording(audio, "journal.flac")   # FLAC
recorder.save_recording(audio, "journal.ogg")    # OGG
```

## Tips for Quality Recordings

1. **Quiet environment** - Reduce background noise
2. **Consistent distance** - Keep microphone at same distance from mouth
3. **Test levels first** - Use `get_input_level()` to check setup
4. **Use an external mic** - Built-in laptop mics often have noise

## Example

Run the example to test recording:

```bash
uv run python recording_sdk/example.py
```
