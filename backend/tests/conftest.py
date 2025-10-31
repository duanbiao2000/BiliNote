import os
import json
import tempfile
import shutil
import types
import contextlib
from pathlib import Path

import pytest

# FastAPI app import
from app.services.provider import ProviderService
from app.gpt.gpt_factory import GPTFactory
from app.transcriber import transcriber_provider
from app.services.note import NoteGenerator
from app.models.notes_model import AudioDownloadResult
from app.models.transcriber_model import TranscriptResult, TranscriptSegment


@pytest.fixture()
def tmp_output_dir():
    d = tempfile.mkdtemp(prefix="bilinote-tests-")
    os.environ["NOTE_OUTPUT_DIR"] = d
    os.environ["OUT_DIR"] = os.path.join(d, "screenshots")
    os.makedirs(os.environ["OUT_DIR"], exist_ok=True)
    try:
        yield Path(d)
    finally:
        shutil.rmtree(d, ignore_errors=True)


@pytest.fixture(autouse=True)
def mock_services(monkeypatch, tmp_output_dir):
    # Mock provider lookup
    monkeypatch.setattr(
        ProviderService,
        "get_provider_by_id",
        staticmethod(lambda provider_id: {
            "api_key": "test-key",
            "base_url": "http://test.local",
            "type": "universal",
            "name": "TestProvider",
        }),
    )

    # Mock GPT factory
    class _FakeGPT:
        def summarize(self, source):
            return "# OK\n\nGenerated from tests."

    monkeypatch.setattr(GPTFactory, "from_config", lambda self, cfg: _FakeGPT())

    # Mock transcriber
    class _FakeTranscriber:
        def transcript(self, file_path: str) -> TranscriptResult:
            return TranscriptResult(
                language="zh",
                full_text="hello world",
                segments=[TranscriptSegment(start=0, end=1, text="hello world")],
                raw={}
            )

    monkeypatch.setattr(
        transcriber_provider,
        "get_transcriber",
        lambda transcriber_type=None: _FakeTranscriber(),
    )

    # Mock downloader selection to return a fake downloader instance
    class _FakeDownloader:
        def download(self, video_url: str, output_dir: str = None, quality: str = "fast", need_video: bool = False):
            audio_path = str(tmp_output_dir / "sample.mp3")
            Path(audio_path).write_bytes(b"fake-audio")
            return AudioDownloadResult(
                file_path=audio_path,
                title="Test Video",
                duration=1,
                cover_url="",
                platform="bilibili",
                video_id="BVTEST",
                raw_info={}
            )

        def download_video(self, video_url: str, output_dir: str = None) -> str:
            video_path = str(tmp_output_dir / "sample.mp4")
            Path(video_path).write_bytes(b"fake-video")
            return video_path

    monkeypatch.setattr(NoteGenerator, "_get_downloader", lambda self, platform: _FakeDownloader())

    yield


