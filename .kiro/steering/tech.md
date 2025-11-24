---
inclusion: fileMatch
fileMatchPattern: '**/mimamori-pi/**'
---

# Technology Stack

## Hardware Platform
- **Primary Platform**: Raspberry Pi Zero 2 W
- **Camera**: Camera Module v2/v3 または HQ Camera
- **OS**: Raspberry Pi OS  (64-bit)
- **Storage**: MicroSD カード (32GB以上推奨)
- **Power**: 公式電源アダプタ (5V 3A)

## Core Technologies
- **Language**: Python 3.12+
- **Package Manager**: uv
- **Web Framework**: Flask 3.0+
- **Camera Library**: picamera2
- **Concurrency**: threading（Phase 1）、asyncio（Phase 2以降でクラウドI/O時に検討）

## Phase 1 Technology Stack
- **Web**: Flask（同期処理）
- **Background Tasks**: threading.Timer（スナップショット定期保存）
- **Storage**: ローカルファイルシステム
- **Frontend**: HTML5 + CSS3 + Vanilla JavaScript

## Phase 2+ Technology Stack（将来拡張）
- **Async Framework**: asyncio + aiohttp（クラウドI/O用）
- **Cloud Storage**: boto3 / aioboto3（AWS S3）
- **ML Inference**: TensorFlow Lite（エッジ）/ AWS Lambda（クラウド）

## Development Tools
- **Code Quality**: Ruff（フォーマット・リント）
- **Type Checking**: mypy
- **Testing**: pytest + coverage（80%以上）
- **CI/CD**: GitHub Actions
- **Version Control**: Git with conventional commits



## Technical Constraints
- **Resource Limits**: TBD
- **Network**: 家庭用Wi-Fi環境での動作
- **Power**: 24時間連続稼働対応
- **Environment**: 新生児の部屋での静音動作
