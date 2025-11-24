---
inclusion: fileMatch
fileMatchPattern: '**/mimamori-pi/**'
---

# Build & Test Guidelines

## Development Environment Requirements

### Hardware Prerequisites
- Raspberry Pi Zero 2 W
- MicroSD カード (32GB以上)

### Software Prerequisites
- Python 3.12+
- Git
- [uv](https://github.com/astral-sh/uv) (Pythonパッケージマネージャー)

## Setup & Tooling

### 仮想環境
1. 依存関係のインストール（仮想環境は自動的に作成されます）
   ```bash
   uv sync
   ```
   または、開発/テスト依存関係を含む場合:
   ```bash
   uv sync --dev
   ```
2. 仮想環境の有効化（必要な場合）
   - `uv` は `uv run` コマンドで自動的に仮想環境を使用します
   - 手動で有効化する場合: `source .venv/bin/activate` （Windows: `.venv\Scripts\activate`）

### 環境変数
- `MIMAMORI_PI_LOG_LEVEL`: `INFO` / `DEBUG` などログレベルを制御
- `SECRET_KEY`: Flask セッション用シークレットキー
- 秘匿情報は `.env` 管理（コード直書き禁止）

### コマンド一覧

| コマンド | 用途 |
| --- | --- |
| `uv run pytest` | ユニットテスト実行 |
| `ruff format .` | フォーマット整形 |
| `ruff check .` | スタイル/静的解析 |
| `ruff check --fix .` | 自動修正可能な問題を修正 |
| `uv run mypy` | 型検査 |
| `uv run pytest --maxfail=1 -q` | 軽量検証（PR前など） |
| `uv run pytest tests/storage/` | ストレージモジュール専用テスト |

## Testing Strategy

### Test Categories
- **Unit Tests**: 各モジュールの独立テスト
- **Integration Tests**: モジュール間の統合テスト
- **Hardware Tests**: Raspberry Pi Zero 2 W実機での統合テスト
- **Mock Tests**: カメラハードウェアなしでの開発テスト

### Test-Driven Development
- 機能実装前にテストを作成
- Red-Green-Refactorサイクル
- 最低80%のテストカバレッジ

### 実機テスト（Raspberry Pi）

TBD

## Code Quality Standards

### Automated Checks
- **Ruff**: コードフォーマット・リンティング・インポート整理（Black/flake8/isort の代替）
- **mypy**: 型チェック
- `pytest.ini` で `src/` を `PYTHONPATH` に追加済み

### Pre-commit Hooks
実装時にpre-commit設定を追加予定

## Continuous Integration

### GitHub Actions (予定)
- プルリクエスト時の自動テスト
- コード品質チェック
- セキュリティスキャン
- 手順案: `uv sync --dev` → `ruff format --check .` → `ruff check .` → `uv run mypy` → `uv run pytest`

### Hardware Testing
- Raspberry Pi実機での定期テスト
- 長時間稼働テスト

## Build Process (実装後に詳細化)

### Phase 1 Build
基本的なPythonパッケージとしてのビルド

### Phase 2 Build
AWS IoT統合を含むビルド

## Deployment Strategy

### Local Deployment
- systemdサービスとしての登録
- 自動起動設定
- デプロイスクリプト実行前に `uv run pytest` 合格および `ruff check` 通過を必須

### Configuration Management
- JSON設定ファイル
- 環境変数による秘匿情報管理

---

**Note**: このガイドラインは実装の進行に合わせて具体的な手順を追加していきます。
