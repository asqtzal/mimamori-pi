---
inclusion: fileMatch
fileMatchPattern: '**/mimamori-pi/**'
---

# Project Structure

## High-Level Structure Principles
- **src/**: メインのソースコード
- **tests/**: テストコード（ソース構造を反映）
- **docs/**: ドキュメント
- **scripts/**: 運用・デプロイスクリプト


## Naming Conventions
- **Files**: snake_case (例: camera_service.py)
- **Classes**: PascalCase (例: CameraService)
- **Functions/Variables**: snake_case (例: start_streaming)
- **Constants**: UPPER_SNAKE_CASE (例: DEFAULT_RESOLUTION)
- **Private Members**: 先頭にアンダースコア (例: _cleanup_resources)

## Architectural Decisions
- **Modular Design**: 機能別にモジュールを分離
- **Service Layer Pattern**: ビジネスロジックをサービスクラスに集約
- **Configuration-Driven**: 設定ファイルによる動作制御
- **Flask Blueprint Pattern**: ルーティングをBlueprintで分離し、循環インポートを回避
