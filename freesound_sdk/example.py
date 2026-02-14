"""Example: Search and explore meditation sounds on Freesound."""

import os

from dotenv import load_dotenv

from freesound_sdk import FreesoundClient


def main():
    print("=" * 60)
    print("Freesound SDK - Meditation Sound Discovery Demo")
    print("=" * 60)
    print()

    # Check for API credentials
    load_dotenv()
    if not os.getenv("FREESOUND_CLIENT_SECRET"):
        print("FREESOUND_CLIENT_SECRET not set!")
        print()
        print("To use this SDK:")
        print("1. Get credentials at: https://freesound.org/apiv2/apply")
        print("2. Add to .env file:")
        print("   FREESOUND_CLIENT_ID=your_client_id")
        print("   FREESOUND_CLIENT_SECRET=your_client_secret")
        print()
        print("Demo will show available features without API calls.")
        print("-" * 40)
        print()

        # Show presets even without API key
        print("Available Meditation Presets:")
        presets = FreesoundClient.MEDITATION_PRESETS
        for name, config in presets.items():
            print(f"  {name}: {config['description']}")
        print()
        return

    client = FreesoundClient()

    # Show available presets
    print("Available Meditation Presets:")
    print("-" * 40)
    for name, description in client.get_meditation_presets().items():
        print(f"  {name}: {description}")
    print()

    # Search for singing bowls
    print("Searching for singing bowl sounds (10-30 seconds)...")
    print("-" * 40)
    sounds = client.search_sounds(
        query="singing bowl",
        duration_range=(10, 30),
        page_size=5,
    )

    for sound in sounds:
        print(f"  [{sound['id']}] {sound['name']}")
        print(
            f"        Duration: {sound['duration']:.1f}s | Rating: {sound['rating']:.1f}"
        )
        print(f"        Tags: {', '.join(sound['tags'][:5])}")
        print()

    # Search using a preset
    print("Searching 'nature' preset for ambient sounds...")
    print("-" * 40)
    nature_sounds = client.search_preset(
        "nature", duration_range=(30, 120), page_size=5
    )

    for sound in nature_sounds:
        print(f"  [{sound['id']}] {sound['name']}")
        print(f"        Duration: {sound['duration']:.1f}s")
        print()

    # Get detailed info about a sound
    if sounds:
        first_sound = sounds[0]
        print(f"Detailed info for sound {first_sound['id']}:")
        print("-" * 40)
        details = client.get_sound(first_sound["id"])
        print(f"  Name: {details['name']}")
        print(f"  Duration: {details['duration']:.1f} seconds")
        print(f"  License: {details['license']}")
        print(f"  Downloads: {details['downloads']}")
        print(f"  Preview URL: {details['preview_url']}")
        print()

        # Show attribution
        print("Attribution (include when using this sound):")
        print("-" * 40)
        attribution = client.get_attribution(first_sound["id"])
        print(f"  {attribution}")
        print()

    print("=" * 60)
    print("Demo complete!")
    print()
    print("To download sounds, use:")
    print('  client.download_sound(sound_id, "meditation_bell.wav")')
    print()
    print("Remember to include attribution for CC-licensed sounds!")
    print("=" * 60)


if __name__ == "__main__":
    main()
