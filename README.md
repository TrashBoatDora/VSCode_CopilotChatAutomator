
# Hybrid UI Automation Script

一個專為 VS Code Copilot Chat 設計的「純鍵盤」自動化腳本，能夠自動處理大量專案的程式碼補全任務，無需任何圖像辨識或滑鼠操作。


## 專案特色

- **模組化設計**：功能分離，易於維護與擴充
- **純鍵盤自動化**：全程僅用鍵盤快捷鍵，無需圖像辨識或滑鼠操作，穩定性高
- **智能錯誤處理**：完整的錯誤分類、重試機制和恢復策略
- **批次處理**：支援大規模專案的分批處理和中斷續跑
- **詳細日誌**：多層級日誌記錄，包含專案級和系統級日誌
- **Copilot 記憶體清除**：每個專案處理前自動清除 Copilot 記憶體，避免交叉污染
- **回應複製/關閉強化**：自動重試複製 Copilot 回應，確保內容完整，並智能判斷何時關閉 VS Code
- **一鍵重置**：ProjectStatusReset.py 可自動重設狀態並刪除 Copilot_AutoComplete 報告

## 專案架構

```
VSCode_Hybrid UI Automation Script/
├── config/
│   ├── config.py          # 配置管理
│   └── settings.json      # JSON 配置檔
├── src/
│   ├── logger.py          # 日誌系統
│   ├── project_manager.py # 專案管理
│   ├── vscode_controller.py # VS Code 控制
│   ├── copilot_handler.py # Copilot Chat 操作
│   ├── vscode_ui_initializer.py # UI 初始化（已棄用）
│   └── error_handler.py   # 錯誤處理
├── assets/               # （已棄用）
├── logs/                # 日誌檔案
├── projects/            # 待處理專案
├── tests/               # 測試腳本
├── docs/                # 文檔
├── main.py              # 主執行腳本
├── requirements.txt     # 依賴套件
└── README.md           # 說明文件
```

## 安裝與設定

### 1. 安裝 Python 依賴

```bash
pip install -r requirements.txt
```

### 2. 設定提示詞

編輯專案根目錄的 `prompt.txt` 檔案，內容為你想要 Copilot 執行的任務：

```
幫我分析這個專案的程式碼，並補全缺失的 TODO 項目。請提供：
1. 程式碼結構分析
2. TODO 項目的實作建議
3. 可能的改進方案

請確保回應包含具體的程式碼範例。
```

### 3. 放置專案檔案

將待處理的專案資料夾放置在 `projects/` 目錄下。

### 4. 配置設定

編輯 `config/config.py` 調整參數：

- VS Code 啟動延遲時間
- Copilot 回應超時時間
- 批次處理大小等

**注意：** 本腳本已改用純鍵盤操作，無需圖像資源檔案，`assets/` 及相關模組已棄用。

## 使用方法

### 基本執行

```bash
python main.py
```

### 測試單一模組

```bash
# 測試專案掃描
python -m src.project_manager

# 測試 VS Code 控制
python -m src.vscode_controller


```

## 工作流程

1. **環境檢查**：驗證配置、提示詞檔案和執行環境
2. **專案掃描**：掃描 `projects/` 目錄下的所有專案
3. **分批處理**：將專案分批，避免長時間運行的不穩定性
4. **專案處理**：
   - 開啟 VS Code 專案
  - 使用 `Ctrl+Shift+I` 開啟 Copilot Chat
  - 從 `prompt.txt` 讀取並發送提示詞
  - 等待回應完成
  - 使用鍵盤快捷鍵複製回應內容（自動重試，確保完整）
  - 儲存結果到專案目錄
  - 關閉專案（自動清除 Copilot 記憶體，僅關閉自動啟動的 VS Code）
5. **錯誤處理**：自動重試失敗的專案
6. **生成報告**：輸出詳細的執行摘要

## 錯誤處理機制

- **自動重試**：對於暫時性錯誤，自動重試最多 3 次
- **錯誤分類**：將錯誤分為 VS Code、Copilot、圖像識別等類型
- **恢復策略**：根據錯誤類型採用不同的恢復策略
- **緊急停止**：支援 Ctrl+C 中斷和滑鼠左上角緊急停止

## 日誌系統

- **主日誌**：記錄整個執行過程的詳細資訊
- **專案日誌**：每個專案在其目錄下生成獨立日誌
- **錯誤追蹤**：完整記錄錯誤堆疊和恢復過程

## 注意事項

1. **環境穩定性**：確保在穩定的環境下運行，避免其他程式干擾
2. **鍵盤操作**：腳本使用純鍵盤操作，無需圖像識別，穩定性更高
3. **權限設定**：確保腳本有足夠權限操作檔案和控制應用程式
4. **網路連線**：Copilot 需要網路連線才能正常運作
5. **記憶體需求**：大量專案處理時需要充足的系統記憶體
6. **提示詞設定**：記得在 `prompt.txt` 中設定適合的提示詞內容
7. **Copilot_AutoComplete 報告清理**：使用 ProjectStatusReset.py 重設狀態時，會自動刪除所有 Copilot_AutoComplete.txt/md/report

## 故障排除

### 清除專案處理狀態

如果你想重新處理已經完成或失敗的專案，可以使用以下方法清除專案狀態：

#### 方法 1：刪除狀態檔案（推薦）
```bash
# 刪除整個狀態檔案，重新掃描所有專案
rm projects/automation_status.json
```

#### 方法 2：手動編輯狀態檔案
打開 `projects/automation_status.json`，找到要重新處理的專案，將其 `status` 改為 `"pending"`：

```json
{
  "projects": {
    "sample_project": {
      "name": "sample_project",
      "path": "Y:\\VSCode_Hybrid UI Automation Script\\projects\\sample_project",
      "status": "pending",  // 改成 pending
      "has_copilot_file": false,
      "file_count": 2,
      "supported_files": ["main.py", "Calculator.java"],
      "last_processed": null,
      "error_message": null,
      "processing_time": null,
      "retry_count": 0
    }
  }
}
```

#### 方法 3：使用 Python 腳本重設
```python
# 在專案根目錄執行
python -c "
import json
from pathlib import Path

status_file = Path('projects/automation_status.json')
if status_file.exists():
    with open(status_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 重設所有專案為 pending
    for project in data['projects'].values():
        project['status'] = 'pending'
        project['retry_count'] = 0
        project['error_message'] = None
        project['last_processed'] = None
    
    with open(status_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print('✅ 所有專案狀態已重設為 pending')
else:
    print('❌ 狀態檔案不存在')
"
```

### 常見問題

**VS Code 無法啟動**
- 檢查 VS Code 是否正確安裝
- 確認 `code` 命令在 PATH 中
- 嘗試手動執行 `code --version`


**圖像識別相關問題**
- 本腳本已完全移除圖像識別與滑鼠操作，僅用鍵盤快捷鍵，無需任何圖像資源。

**提示詞檔案問題**
- 檢查 `prompt.txt` 是否存在於專案根目錄
- 確認檔案內容不為空
- 使用 UTF-8 編碼儲存檔案

**Copilot 無回應**
- 檢查 Copilot 擴充功能是否啟用
- 確認網路連線正常
- 嘗試手動測試 Copilot Chat

**專案處理失敗**
- 查看專案目錄下的 `automation_log.txt`
- 檢查專案是否包含支援的程式檔案
- 確認專案路徑和權限

## 擴展說明

本腳本採用模組化設計，可以輕鬆擴展新功能：
- 添加新的程式語言支援
- 自定義提示詞模板
- 集成其他 AI 工具
- 添加更多錯誤恢復策略

## 技術細節

### 核心技術

- **pyautogui**：UI 自動化操作（僅用鍵盤快捷鍵）
- **pyperclip**：剪貼簿操作
- **psutil**：進程管理
- **subprocess**：程式啟動控制

### 設計原則

- **穩定性優先**：全程僅用鍵盤操作，完全移除圖像識別與滑鼠依賴
- **可觀測性**：詳細的日誌和狀態追蹤
- **容錯性**：完善的錯誤處理和恢復機制
- **可維護性**：清晰的模組分離和代碼結構
- **記憶隔離**：每個專案獨立處理，避免交叉污染

## 貢獻指南

歡迎提交 Issue 和 Pull Request。在開發新功能時，請：

1. 遵循現有的代碼風格
2. 添加適當的測試
3. 更新相關文檔
4. 確保向後兼容性

## 授權條款

本專案基於 MIT 授權條款發布。

## 更新日誌

### v1.1.0 (2025-09-13)
- 完全移除圖像辨識與滑鼠操作，純鍵盤自動化
- Copilot 記憶體清除、回應複製/關閉強化
- ProjectStatusReset.py 支援自動刪除 Copilot_AutoComplete 報告

### v1.0.0 (2024-12-12)
- 初始版本發布
- 完整的模組化架構
- 支援大規模專案批次處理
- 智能錯誤處理和恢復機制