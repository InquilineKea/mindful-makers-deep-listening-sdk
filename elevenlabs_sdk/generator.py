"""AI-powered meditation music and sound generation using ElevenLabs."""

import io
import os
from typing import Optional

from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs


class GeneratedAudio:
    """Container for generated audio data."""

    def __init__(self, audio_data: bytes, prompt: str, duration_seconds: float):
        """Initialize with audio data.

        Args:
            audio_data: Raw audio bytes
            prompt: The prompt used to generate this audio
            duration_seconds: Requested duration
        """
        self.audio_data = audio_data
        self.prompt = prompt
        self.duration_seconds = duration_seconds

    def save(self, path: str) -> str:
        """Save audio to file.

        Args:
            path: Output file path

        Returns:
            Path to saved file
        """
        with open(path, "wb") as f:
            f.write(self.audio_data)
        print(f"Saved: {path}")
        return path

    def get_bytes(self) -> bytes:
        """Get raw audio bytes."""
        return self.audio_data

    def get_bytesio(self) -> io.BytesIO:
        """Get audio as BytesIO for streaming."""
        return io.BytesIO(self.audio_data)


class MeditationGenerator:
    """Generate meditation music and nature sounds using ElevenLabs AI.

    Uses ElevenLabs' sound generation capabilities to create custom
    meditation music, nature sounds, and transition effects.
    """

    # Preset prompts for common meditation sounds
    PRESETS = {
        "morning_meditation": {
            "prompt": "gentle ambient piano with soft synthesizer pads, peaceful morning atmosphere, slow tempo, meditation music",
            "description": "Peaceful piano for morning meditation",
        },
        "deep_relaxation": {
            "prompt": "deep ambient drone, warm synthesizer pads, very slow evolving textures, hypnotic meditation music, no rhythm",
            "description": "Deep ambient drones for relaxation",
        },
        "nature_rain": {
            "prompt": "gentle rain falling on leaves, soft thunder in distance, peaceful rainstorm, nature sounds",
            "description": "Gentle rain for focus and sleep",
        },
        "ocean_waves": {
            "prompt": "calm ocean waves on sandy beach, gentle sea breeze, peaceful seaside ambience, nature recording",
            "description": "Ocean waves for relaxation",
        },
        "forest_morning": {
            "prompt": "peaceful forest ambience, birds singing, gentle wind through trees, morning sunlight atmosphere",
            "description": "Forest sounds with birdsong",
        },
        "tibetan_bowls": {
            "prompt": "tibetan singing bowls resonating, deep harmonic tones, meditation bells, peaceful temple atmosphere",
            "description": "Singing bowls and bells",
        },
        "breathing_guide": {
            "prompt": "soft ambient tones pulsing slowly, gentle rhythmic breathing pace, calming meditation guide",
            "description": "Rhythmic tones for breath pacing",
        },
        "sleep_music": {
            "prompt": "extremely soft ambient music, barely audible gentle tones, perfect for falling asleep, very quiet lullaby",
            "description": "Ultra-soft music for sleep",
        },
    }

    def __init__(self, api_key: Optional[str] = None):
        """Initialize the generator.

        Args:
            api_key: ElevenLabs API key. If not provided, looks for ELEVENLABS_API_KEY env var.
        """
        load_dotenv()
        self.api_key = api_key or os.getenv("ELEVENLABS_API_KEY")

        if not self.api_key:
            raise ValueError(
                "ElevenLabs API key required. Set ELEVENLABS_API_KEY environment variable "
                "or pass api_key parameter."
            )

        self.client = ElevenLabs(api_key=self.api_key)

    def generate_sound_effect(
        self,
        prompt: str,
        duration_seconds: float = 10.0,
    ) -> GeneratedAudio:
        """Generate a sound effect from a text prompt.

        Args:
            prompt: Description of the sound to generate
            duration_seconds: Desired duration (actual may vary)

        Returns:
            GeneratedAudio object with the generated sound
        """
        result = self.client.text_to_sound_effects.convert(
            text=prompt,
            duration_seconds=duration_seconds,
        )

        # Collect all chunks from generator
        audio_data = b"".join(chunk for chunk in result)

        return GeneratedAudio(
            audio_data=audio_data,
            prompt=prompt,
            duration_seconds=duration_seconds,
        )

    def generate_meditation_music(
        self,
        prompt: str,
        duration_seconds: float = 60.0,
    ) -> GeneratedAudio:
        """Generate meditation music from a description.

        Args:
            prompt: Description of the meditation music to create
            duration_seconds: Desired duration

        Returns:
            GeneratedAudio object with the generated music
        """
        # Enhance prompt for better meditation music results
        enhanced_prompt = f"meditation music: {prompt}, peaceful, calming, ambient"

        return self.generate_sound_effect(
            prompt=enhanced_prompt,
            duration_seconds=duration_seconds,
        )

    def generate_nature_sound(
        self,
        description: str,
        duration_seconds: float = 60.0,
    ) -> GeneratedAudio:
        """Generate nature sounds from a description.

        Args:
            description: Description of the nature sound (e.g., "rain", "ocean", "forest")
            duration_seconds: Desired duration

        Returns:
            GeneratedAudio object with the generated sound
        """
        # Enhance prompt for nature sounds
        enhanced_prompt = f"nature sound recording: {description}, high quality field recording, ambient"

        return self.generate_sound_effect(
            prompt=enhanced_prompt,
            duration_seconds=duration_seconds,
        )

    def generate_transition_sound(
        self,
        sound_type: str = "bell",
        duration_seconds: float = 5.0,
    ) -> GeneratedAudio:
        """Generate transition sounds for meditation cues.

        Args:
            sound_type: Type of transition - "bell", "chime", "bowl", "gong"
            duration_seconds: Desired duration

        Returns:
            GeneratedAudio object
        """
        prompts = {
            "bell": "single meditation bell strike, clear resonant tone, peaceful",
            "chime": "gentle wind chimes, soft melodic tones, peaceful transition",
            "bowl": "tibetan singing bowl being struck, deep resonant harmonic tone",
            "gong": "soft gong strike, deep resonant wash of sound, meditation",
        }

        prompt = prompts.get(sound_type, prompts["bell"])

        return self.generate_sound_effect(
            prompt=prompt,
            duration_seconds=duration_seconds,
        )

    def generate_from_preset(
        self,
        preset: str,
        duration_seconds: float = 60.0,
    ) -> GeneratedAudio:
        """Generate audio from a meditation preset.

        Args:
            preset: Preset name (see list_presets())
            duration_seconds: Desired duration

        Returns:
            GeneratedAudio object
        """
        if preset not in self.PRESETS:
            available = ", ".join(self.PRESETS.keys())
            raise ValueError(f"Unknown preset '{preset}'. Available: {available}")

        config = self.PRESETS[preset]
        return self.generate_sound_effect(
            prompt=config["prompt"],
            duration_seconds=duration_seconds,
        )

    @staticmethod
    def list_presets() -> dict:
        """List available meditation presets.

        Returns:
            Dict of preset names to descriptions
        """
        return {
            name: config["description"]
            for name, config in MeditationGenerator.PRESETS.items()
        }

    def generate_session(
        self,
        intro_seconds: float = 30.0,
        main_seconds: float = 300.0,
        outro_seconds: float = 30.0,
        main_prompt: str = "peaceful ambient meditation music",
    ) -> dict:
        """Generate a complete meditation session with intro, main, and outro.

        Args:
            intro_seconds: Duration of intro transition
            main_seconds: Duration of main meditation music
            outro_seconds: Duration of outro transition
            main_prompt: Prompt for the main meditation music

        Returns:
            Dict with 'intro', 'main', 'outro' GeneratedAudio objects
        """
        print("Generating meditation session...")
        print(f"  Intro: {intro_seconds}s")

        intro = self.generate_transition_sound("bowl", duration_seconds=intro_seconds)

        print(f"  Main: {main_seconds}s - {main_prompt}")
        main = self.generate_meditation_music(
            main_prompt, duration_seconds=main_seconds
        )

        print(f"  Outro: {outro_seconds}s")
        outro = self.generate_transition_sound("bell", duration_seconds=outro_seconds)

        return {
            "intro": intro,
            "main": main,
            "outro": outro,
            "total_duration": intro_seconds + main_seconds + outro_seconds,
        }
