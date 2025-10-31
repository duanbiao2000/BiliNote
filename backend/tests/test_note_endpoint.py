import time
import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from main import app


@pytest.fixture()
def client():
    return TestClient(app)


def test_generate_note_endpoint(client, tmp_output_dir):
    payload = {
        "video_url": "https://www.bilibili.com/video/BVTEST",
        "platform": "bilibili",
        "quality": "medium",
        "screenshot": False,
        "link": False,
        "model_name": "gpt-4o-mini",
        "provider_id": "provider-1",
        "format": ["summary"],
        "style": "minimal",
        "extras": None,
        "video_understanding": False,
        "video_interval": 0,
        "grid_size": [],
    }

    res = client.post("/generate_note", json=payload)
    assert res.status_code == 200
    task_id = res.json()["data"]["task_id"]

    # 等待后台任务完成（背景任务在同进程触发，给一点时间）
    for _ in range(10):
        time.sleep(0.2)
        status_res = client.get(f"/task_status/{task_id}")
        assert status_res.status_code == 200
        body = status_res.json()
        status = body.get("data", {}).get("status") or body.get("status")
        if status == "SUCCESS":
            result = body["data"].get("result") or body.get("result")
            assert result and result.get("markdown", "").startswith("# OK")
            break
    else:
        pytest.fail("Task did not reach SUCCESS in time")


