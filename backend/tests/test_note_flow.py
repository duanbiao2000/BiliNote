import json
import uuid
from pathlib import Path

from app.routers.note import run_note_task


def test_run_note_task_generates_result(tmp_output_dir):
    task_id = str(uuid.uuid4())
    video_url = "https://www.bilibili.com/video/BVTEST"

    # 执行后台任务主流程（已通过 fixtures mock 外部依赖）
    run_note_task(
        task_id=task_id,
        video_url=video_url,
        platform="bilibili",
        quality="medium",
        link=False,
        screenshot=False,
        model_name="gpt-4o-mini",
        provider_id="provider-1",
        _format=["summary"],
        style="minimal",
        extras=None,
        video_understanding=False,
        video_interval=0,
        grid_size=[],
    )

    status_file = Path(tmp_output_dir) / f"{task_id}.status.json"
    result_file = Path(tmp_output_dir) / f"{task_id}.json"

    # 结果文件应存在且包含 markdown
    assert result_file.exists(), "result json should exist"
    data = json.loads(result_file.read_text(encoding="utf-8"))
    assert data.get("markdown", "").startswith("# OK"), "markdown content should be generated"

    # 最终状态应为 SUCCESS（状态由 NoteGenerator 写入）
    assert status_file.exists(), "status json should exist"
    status = json.loads(status_file.read_text(encoding="utf-8")).get("status")
    assert status in ("SUCCESS", "SAVING", "SUMMARIZING", "TRANSCRIBING", "DOWNLOADING", "PARSING"), "status should be a known phase"


