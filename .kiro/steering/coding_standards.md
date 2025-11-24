---
inclusion: fileMatch
fileMatchPattern: '**/mimamori-pi/**'
---

# Coding Standards

## Code Quality Standards
- **Code Style**: Ruff
- **Type Hints**: 全ての関数にtype hintsを付与
- **Documentation**: docstring (Google Style)
- **Error Handling**: 適切な例外処理とログ出力

## Naming Conventions
- **Files**: snake_case (例: bme280_sensor.py)
- **Classes**: PascalCase (例: BME280Sensor)
- **Functions/Variables**: snake_case (例: read_temperature)
- **Constants**: UPPER_SNAKE_CASE (例: DEFAULT_INTERVAL)
- **Private Members**: 先頭にアンダースコア (例: _internal_method)

## Module Design Principles
- **Single Responsibility**: 各モジュールは単一の責任を持つ
- **Interface Segregation**: 小さく特化したインターフェース
- **Dependency Inversion**: 抽象に依存し、具象に依存しない
- **Plugin Architecture**: 新機能を既存コードを変更せずに追加可能

## Testing Strategy
- **Unit Tests**: pytest を使用、カバレッジ80%以上
- **Integration Tests**: カメラとの統合テスト
- **Mock Testing**: カメラハードウェアのモック（開発環境用）
- **Hardware Testing**: Raspberry Pi Zero 2 W実機での動作確認

## Performance Requirements
TBD

## Development Tools
- **Code Quality**: pre-commit hooks (Ruff)
- **Testing**: pytest + coverage (80%以上)
- **CI/CD**: GitHub Actions
- **Containerization**: Docker (開発・テスト用)