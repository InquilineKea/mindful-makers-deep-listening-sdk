# Freesound SDK - Meditation Sound Discovery

Search and download Creative Commons licensed sounds from [Freesound.org](https://freesound.org) for your meditation and mindfulness projects.

## Setup

1. Get a free API key at [freesound.org/apiv2/apply](https://freesound.org/apiv2/apply)
2. Add to your `.env` file:
   ```
   FREESOUND_API_KEY=your_key_here
   ```

## Features

- **Search sounds** with filters for duration, tags, and quality
- **Meditation presets** - curated searches for common meditation sounds
- **Download sounds** to local files
- **Get attribution** text for proper Creative Commons credit

## Usage

### Basic Search

```python
from freesound_sdk import FreesoundClient

client = FreesoundClient()

# Search for singing bowl sounds between 10-30 seconds
sounds = client.search_sounds(
    query="singing bowl",
    duration_range=(10, 30),
    page_size=10
)

for sound in sounds:
    print(f"{sound['name']} - {sound['duration']}s")
    print(f"  Preview: {sound['preview_url']}")
```

### Use Meditation Presets

Curated search configurations for common meditation sounds:

```python
# See available presets
presets = client.get_meditation_presets()
# {
#   'nature': 'Natural soundscapes - forests, streams, wind',
#   'bells': 'Bells and chimes for meditation cues',
#   'bowls': 'Tibetan singing bowls and resonant tones',
#   'rain': 'Rain and water sounds',
#   'ocean': 'Ocean waves and beach sounds',
#   'forest': 'Forest ambience with birdsong',
#   'drone': 'Sustained ambient drones and pads',
#   'breath': 'Breathing sounds for pacing'
# }

# Search using a preset
nature_sounds = client.search_preset("nature", duration_range=(60, 300))
```

### Download Sounds

```python
# Download a sound by ID
client.download_sound(sound_id=123456, path="meditation_bell.wav")
```

### Get Sound Details

```python
# Get full details about a sound
details = client.get_sound(sound_id=123456)
print(f"Name: {details['name']}")
print(f"Duration: {details['duration']} seconds")
print(f"License: {details['license']}")
```

### Attribution

Always include attribution when using Creative Commons sounds:

```python
attribution = client.get_attribution(sound_id=123456)
print(attribution)
# "Tibetan Singing Bowl" by username (CC BY 3.0)
# Source: https://freesound.org/s/123456/
```

### Find Similar Sounds

```python
# Find sounds similar to one you like
similar = client.search_similar(sound_id=123456, page_size=5)
for sound in similar:
    print(f"{sound['name']} - {sound['duration']}s")
```

### Preview Without Download

```python
# Get URL to stream preview
preview_url = client.preview_url(sound_id=123456, quality="high")
# Use with any audio player that supports URLs
```

## Search Options

### Sorting

```python
sounds = client.search_sounds(
    query="ocean waves",
    sort="rating_desc"  # Sort by highest rated
)
```

Available sort options:
- `score` (default) - Relevance
- `duration_desc` / `duration_asc` - By length
- `created_desc` / `created_asc` - By upload date
- `downloads_desc` - By popularity
- `rating_desc` - By user rating

### Tags

```python
# Filter by specific tags
sounds = client.search_sounds(
    query="ambient",
    tags=["meditation", "relaxing", "calm"]
)
```

## License Information

Freesound hosts sounds under various Creative Commons licenses:
- **CC0** - Public domain, no attribution required
- **CC BY** - Attribution required
- **CC BY-NC** - Attribution required, non-commercial use only

Always check the `license` field and include proper attribution.

## Example

Run the example to explore meditation sounds:

```bash
uv run python freesound_sdk/example.py
```
