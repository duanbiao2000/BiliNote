import uuid
import itertools

from app.services.note import NoteGenerator


def test_retry_succeeds_after_failures(monkeypatch, tmp_output_dir):
    # 构造前两次抛错、第三次成功的可调用
    attempts = itertools.count(1)

    class _FakeTranscriber:
        def transcript(self, file_path: str):
            i = next(attempts)
            if i < 3:
                raise RuntimeError("flaky error")
            class _Ret:
                language = "zh"
                full_text = "ok"
                segments = []
            return _Ret()

    # 注入假 transcriber
    monkeypatch.setattr(NoteGenerator, "_init_transcriber", lambda self: _FakeTranscriber())
    # 假 downloader：立即返回
    class _FakeDownloader:
        def download(self, **kwargs):
            class _Audio:
                file_path = str(tmp_output_dir / "a.mp3")
                title = "t"
                duration = 1
                cover_url = ""
                platform = "bilibili"
                video_id = "BVTEST"
                raw_info = {}
            return _Audio()
    monkeypatch.setattr(NoteGenerator, "_get_downloader", lambda self, p: _FakeDownloader())
    # 假 GPT：返回 markdown
    class _FakeGPT:
        def summarize(self, source):
            return "# OK"
    monkeypatch.setattr(NoteGenerator, "_get_gpt", lambda self, m, p: _FakeGPT())

    ng = NoteGenerator()
    # 缩短重试阈值，确保测试快速
    ng.max_retries = 3
    ng.transcribe_timeout_s = 10

    res = ng.generate(
        video_url="https://www.bilibili.com/video/BVTEST",
        platform="bilibili",
        task_id=str(uuid.uuid4()),
        model_name="m",
        provider_id="p",
    )
    assert res is not None


def test_timeout_marks_failed(monkeypatch, tmp_output_dir):
    # 让 transcriber 持续阻塞超时（通过抛 TimeoutError 模拟）
    class _SlowTranscriber:
        def transcript(self, file_path: str):
            raise TimeoutError("too slow")

    monkeypatch.setattr(NoteGenerator, "_init_transcriber", lambda self: _SlowTranscriber())

    class _FakeDownloader:
        def download(self, **kwargs):
            class _Audio:
                file_path = str(tmp_output_dir / "a.mp3")
                title = "t"
                duration = 1
                cover_url = ""
                platform = "bilibili"
                video_id = "BVTEST"
                raw_info = {}
            return _Audio()
    monkeypatch.setattr(NoteGenerator, "_get_downloader", lambda self, p: _FakeDownloader())
    monkeypatch.setattr(NoteGenerator, "_get_gpt", lambda self, m, p: object())

    ng = NoteGenerator()
    ng.max_retries = 2
    ng.transcribe_timeout_s = 1

    res = ng.generate(
        video_url="https://www.bilibili.com/video/BVTEST",
        platform="bilibili",
        task_id=str(uuid.uuid4()),
        model_name="m",
        provider_id="p",
    )
    assert res is None

