import json
import uuid
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.exceptions.note import NoteError
from app.services.note import NoteGenerator
from app.routers.note import run_note_task
from main import app


@pytest.fixture()
def client():
    return TestClient(app)


def test_run_note_task_missing_model_provider_raises(tmp_output_dir):
    task_id = str(uuid.uuid4())
    with pytest.raises(Exception):
        run_note_task(
            task_id=task_id,
            video_url="https://www.bilibili.com/video/BVTEST",
            platform="bilibili",
            quality="medium",
            link=False,
            screenshot=False,
            model_name=None,
            provider_id=None,
            _format=[],
            style=None,
            extras=None,
            video_understanding=False,
            video_interval=0,
            grid_size=[],
        )


def test_invalid_platform_raises_note_error(monkeypatch, tmp_output_dir):
    # 强制 _get_downloader 抛出 NoteError，模拟不支持平台
    monkeypatch.setattr(
        NoteGenerator,
        "_get_downloader",
        lambda self, platform: (_ for _ in ()).throw(NoteError(code=400, message="unsupported")),
    )

    ng = NoteGenerator()
    res = ng.generate(
        video_url="https://www.bilibili.com/video/BVTEST",
        platform="unsupported",
        task_id=str(uuid.uuid4()),
        model_name="gpt-4o-mini",
        provider_id="provider-1",
    )
    # 失败路径下，generate 返回 None，并写入 FAILED 状态
    assert res is None


def test_transcriber_failure_marks_failed(monkeypatch, tmp_output_dir):
    # 让 _transcribe_audio 抛错
    monkeypatch.setattr(
        NoteGenerator,
        "_transcribe_audio",
        lambda self, **kwargs: (_ for _ in ()).throw(RuntimeError("transcribe error")),
    )

    task_id = str(uuid.uuid4())
    ng = NoteGenerator()
    res = ng.generate(
        video_url="https://www.bilibili.com/video/BVTEST",
        platform="bilibili",
        task_id=task_id,
        model_name="gpt-4o-mini",
        provider_id="provider-1",
    )
    assert res is None
    status_file = Path(tmp_output_dir) / f"{task_id}.status.json"
    assert status_file.exists()
    status = json.loads(status_file.read_text(encoding="utf-8")).get("status")
    assert status == "FAILED"


def test_gpt_failure_marks_failed(monkeypatch, tmp_output_dir):
    class _BoomGPT:
        def summarize(self, source):
            raise RuntimeError("gpt error")

    monkeypatch.setattr(NoteGenerator, "_get_gpt", lambda self, m, p: _BoomGPT())

    task_id = str(uuid.uuid4())
    ng = NoteGenerator()
    res = ng.generate(
        video_url="https://www.bilibili.com/video/BVTEST",
        platform="bilibili",
        task_id=task_id,
        model_name="gpt-4o-mini",
        provider_id="provider-1",
    )
    assert res is None
    status_file = Path(tmp_output_dir) / f"{task_id}.status.json"
    assert status_file.exists()
    status = json.loads(status_file.read_text(encoding="utf-8")).get("status")
    assert status == "FAILED"


def test_task_status_pending_when_not_found(client):
    task_id = str(uuid.uuid4())
    r = client.get(f"/task_status/{task_id}")
    assert r.status_code == 200
    data = r.json()
    payload = data.get("data", data)
    assert payload.get("status") == "PENDING"


def test_task_status_success_when_only_result_exists(client, tmp_output_dir):
    task_id = str(uuid.uuid4())
    result_path = Path(tmp_output_dir) / f"{task_id}.json"
    result_path.write_text(json.dumps({"markdown": "# OK", "transcript": {}, "audio_meta": {}}), encoding="utf-8")

    r = client.get(f"/task_status/{task_id}")
    assert r.status_code == 200
    data = r.json()
    payload = data.get("data", data)
    assert payload.get("status") == "SUCCESS"
    result = payload.get("result")
    assert result and result.get("markdown", "").startswith("# OK")


