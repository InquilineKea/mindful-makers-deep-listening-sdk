"""Freesound API client for discovering meditation sounds."""

import os
from typing import Optional

import requests
from dotenv import load_dotenv


class FreesoundClient:
    """Client for searching and downloading sounds from Freesound.org.

    Freesound is a collaborative database of Creative Commons licensed sounds.
    Uses the Freesound API v2: https://freesound.org/docs/api/
    """

    BASE_URL = "https://freesound.org/apiv2"

    # Curated search presets for meditation
    MEDITATION_PRESETS = {
        "nature": {
            "query": "nature ambient",
            "tags": ["nature", "ambient", "field-recording"],
            "description": "Natural soundscapes - forests, streams, wind",
        },
        "bells": {
            "query": "meditation bell",
            "tags": ["bell", "meditation", "mindfulness"],
            "description": "Bells and chimes for meditation cues",
        },
        "bowls": {
            "query": "singing bowl",
            "tags": ["singing-bowl", "tibetan", "meditation"],
            "description": "Tibetan singing bowls and resonant tones",
        },
        "rain": {
            "query": "rain ambient",
            "tags": ["rain", "ambient", "weather"],
            "description": "Rain and water sounds",
        },
        "ocean": {
            "query": "ocean waves",
            "tags": ["ocean", "waves", "water"],
            "description": "Ocean waves and beach sounds",
        },
        "forest": {
            "query": "forest birds",
            "tags": ["forest", "birds", "nature"],
            "description": "Forest ambience with birdsong",
        },
        "drone": {
            "query": "ambient drone",
            "tags": ["drone", "ambient", "pad"],
            "description": "Sustained ambient drones and pads",
        },
        "breath": {
            "query": "breathing meditation",
            "tags": ["breathing", "breath", "meditation"],
            "description": "Breathing sounds for pacing",
        },
    }

    def __init__(
        self,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
    ):
        """Initialize the Freesound client.

        Args:
            client_id: Freesound OAuth2 client ID
            client_secret: Freesound OAuth2 client secret (used as API token)
        """
        load_dotenv()

        self.client_id = client_id or os.getenv("FREESOUND_CLIENT_ID")
        self.client_secret = client_secret or os.getenv("FREESOUND_CLIENT_SECRET")

        if not self.client_secret:
            raise ValueError(
                "Freesound credentials required. Set FREESOUND_CLIENT_ID and "
                "FREESOUND_CLIENT_SECRET environment variables. "
                "Get credentials at: https://freesound.org/apiv2/apply"
            )

        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Token {self.client_secret}"})

    def _request(self, endpoint: str, params: Optional[dict] = None) -> dict:
        """Make an API request."""
        url = f"{self.BASE_URL}/{endpoint}"
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def search_sounds(
        self,
        query: str,
        tags: Optional[list[str]] = None,
        duration_range: Optional[tuple[float, float]] = None,
        page_size: int = 15,
        sort: str = "score",
    ) -> list[dict]:
        """Search for sounds on Freesound.

        Args:
            query: Search query string
            tags: Optional list of tags to filter by
            duration_range: Optional (min, max) duration in seconds
            page_size: Number of results to return (max 150)
            sort: Sort order - "score", "duration_desc", "duration_asc",
                  "created_desc", "created_asc", "downloads_desc", "rating_desc"

        Returns:
            List of sound info dicts with 'id', 'name', 'duration', 'tags', 'preview_url', etc.
        """
        # Build filter string
        filters = []
        if duration_range:
            filters.append(f"duration:[{duration_range[0]} TO {duration_range[1]}]")
        if tags:
            for tag in tags:
                filters.append(f'tag:"{tag}"')

        params = {
            "query": query,
            "page_size": page_size,
            "sort": sort,
            "fields": "id,name,duration,tags,previews,license,username,description,avg_rating,num_downloads",
        }
        if filters:
            params["filter"] = " ".join(filters)

        data = self._request("search/text/", params)

        sounds = []
        for sound in data.get("results", []):
            previews = sound.get("previews", {})
            sounds.append(
                {
                    "id": sound["id"],
                    "name": sound["name"],
                    "duration": sound["duration"],
                    "tags": sound.get("tags", []),
                    "preview_url": previews.get("preview-hq-mp3", ""),
                    "preview_lq_url": previews.get("preview-lq-mp3", ""),
                    "license": sound.get("license", ""),
                    "username": sound.get("username", ""),
                    "description": (sound.get("description", "") or "")[:200],
                    "rating": sound.get("avg_rating", 0),
                    "downloads": sound.get("num_downloads", 0),
                }
            )

        return sounds

    def get_meditation_presets(self) -> dict:
        """Get available meditation-focused search presets.

        Returns:
            Dict of preset names to descriptions
        """
        return {
            name: preset["description"]
            for name, preset in self.MEDITATION_PRESETS.items()
        }

    def search_preset(
        self,
        preset: str,
        duration_range: Optional[tuple[float, float]] = None,
        page_size: int = 15,
    ) -> list[dict]:
        """Search using a meditation preset.

        Args:
            preset: Preset name (see get_meditation_presets())
            duration_range: Optional (min, max) duration filter
            page_size: Number of results

        Returns:
            List of sound info dicts
        """
        if preset not in self.MEDITATION_PRESETS:
            available = ", ".join(self.MEDITATION_PRESETS.keys())
            raise ValueError(f"Unknown preset '{preset}'. Available: {available}")

        config = self.MEDITATION_PRESETS[preset]
        return self.search_sounds(
            query=config["query"],
            tags=config.get("tags"),
            duration_range=duration_range,
            page_size=page_size,
        )

    def get_sound(self, sound_id: int) -> dict:
        """Get detailed information about a specific sound.

        Args:
            sound_id: Freesound sound ID

        Returns:
            Sound info dict with full details
        """
        data = self._request(f"sounds/{sound_id}/")
        previews = data.get("previews", {})
        return {
            "id": data["id"],
            "name": data["name"],
            "duration": data["duration"],
            "tags": data.get("tags", []),
            "description": data.get("description", ""),
            "license": data.get("license", ""),
            "username": data.get("username", ""),
            "preview_url": previews.get("preview-hq-mp3", ""),
            "download_url": data.get("download", ""),
            "rating": data.get("avg_rating", 0),
            "downloads": data.get("num_downloads", 0),
            "created": data.get("created", ""),
        }

    def download_sound(self, sound_id: int, path: str) -> str:
        """Download a sound to local file.

        Args:
            sound_id: Freesound sound ID
            path: Local path to save the file

        Returns:
            Path to downloaded file
        """
        sound = self.get_sound(sound_id)
        download_url = sound["download_url"]

        if not download_url:
            raise ValueError(f"No download URL available for sound {sound_id}")

        response = self.session.get(download_url, stream=True)
        response.raise_for_status()

        with open(path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"Downloaded: {sound['name']} -> {path}")
        return path

    def get_attribution(self, sound_id: int) -> str:
        """Get proper attribution text for a sound.

        Always include attribution when using CC-licensed sounds.

        Args:
            sound_id: Freesound sound ID

        Returns:
            Attribution text to include with your project
        """
        sound = self.get_sound(sound_id)
        return (
            f'"{sound["name"]}" by {sound["username"]} ({sound["license"]})\n'
            f"Source: https://freesound.org/s/{sound_id}/"
        )

    def preview_url(self, sound_id: int, quality: str = "high") -> str:
        """Get preview URL for a sound without downloading.

        Args:
            sound_id: Freesound sound ID
            quality: "high" or "low" quality preview

        Returns:
            URL to stream the preview
        """
        sound = self.get_sound(sound_id)
        if quality == "high":
            return sound["preview_url"]
        return sound.get("preview_lq_url", sound["preview_url"])

    def search_similar(self, sound_id: int, page_size: int = 10) -> list[dict]:
        """Find sounds similar to a given sound.

        Args:
            sound_id: Freesound sound ID to find similar sounds for
            page_size: Number of results

        Returns:
            List of similar sound info dicts
        """
        params = {
            "page_size": page_size,
            "fields": "id,name,duration,tags,previews",
        }
        data = self._request(f"sounds/{sound_id}/similar/", params)

        sounds = []
        for s in data.get("results", []):
            previews = s.get("previews", {})
            sounds.append(
                {
                    "id": s["id"],
                    "name": s["name"],
                    "duration": s["duration"],
                    "tags": s.get("tags", []),
                    "preview_url": previews.get("preview-hq-mp3", ""),
                }
            )

        return sounds
