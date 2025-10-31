# Transcribers（轉寫器）

簡短說明 `app/transcriber/` 架構同擴展要點（粵語）。

## 主要檔案

- `app/transcriber/transcriber_provider.py`：轉寫器註冊與取得共享實例。
- 各個實作（faster-whisper、bcut 等）位於 `app/transcriber/providers/`（或同級目錄）。

## 重點

- Provider pattern：用 registry 管理不同實作，新增時在 provider list 註冊。
- 某啲轉寫器有 platform 限制（例如 MLX 只係 macOS 可用），實作時要檢查平台與可用資源。

## 建議

- 提供一個 `is_available()` 方法給每個 transcriber，啟動時做 health-check 並記錄到 log。
- 若支援多模型（CPU/GPU），在 config 提供優先級設定。

## 測試

- 單元測試可以 mock audio input，驗證回傳的文字段落結構與長度。
