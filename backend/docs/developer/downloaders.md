# Downloaders（下載器）

以下用粵語簡短說明 `app/downloaders/` 嘅設計同重點檢查項。

## 主要檔案

- `app/downloaders/youtube_downloader.py`：YouTube/通用下載器，使用 `yt-dlp`。
- `app/downloaders/bilibili_downloader.py`：Bilibili 特定邏輯。
- `app/downloaders/base.py`：Downloader 抽象與共用 helper。

## 重點

- yt-dlp format 可能唔支援某啲影片，唔好硬性指定 single format（例如只選 `m4a`），應提供 fallback（`bestaudio/best`）並重試。
- output 目錄唔應假設已存在，下載 code 要做目錄存在檢查或 fallback。
- 所有狀態/結果檔寫入要跟項目既 atomic pattern（先寫 `.tmp` 再 `replace`）。

## 建議改進

- 在 `youtube_downloader.py` 加一個 `DEFAULT_FORMATS` 清單，遇到 `requested format not available` 時循序重試。
- 把 metadata extraction （例如 `yt-dlp` 的 info_dict）同下載行為分離，便於在無檔案創建時還能檢查可用格式。

## 注意

- 測試下載器需要網絡同外部依賴（yt-dlp、ffmpeg），本地測試可以用短片或 local file 模擬。
