# Implementation Plan - mimamori-pi

このドキュメントは、mimamori-piの実装タスクリストです。MVP（Minimum Viable Product）アプローチで、早期に動作するシステムを構築し、段階的に機能を追加していきます。

## 実装戦略

**原則:**
1. **動くものを早く作る**: 各フェーズで動作確認可能な状態にする
2. **テスト駆動**: 機能実装と同時にテストを書く
3. **段階的な拡張**: コア機能→拡張機能の順で実装

## Phase 0: プロジェクトセットアップ（最小限）

### 1. 基本プロジェクト構造の作成

- [ ] 1.1 ディレクトリ構造の作成
  - `src/mimamori_pi/`以下の基本ディレクトリを作成
  - `camera/`, `storage/`, `snapshot/`, `config/`, `routes/`, `templates/`, `static/`
  - `tests/`ディレクトリを作成
  - _Requirements: 全般_

- [ ] 1.2 pyproject.tomlの作成
  - プロジェクトメタデータを定義
  - uv依存関係を定義（Flask, picamera2, pytest, ruff, mypy）
  - Ruff、mypy設定を追加
  - _Requirements: 全般_

- [ ] 1.3 基本設定ファイルの作成
  - `.gitignore`を作成（`.venv/`, `data/`, `*.pyc`等）
  - `.env.example`を作成（環境変数テンプレート）
  - `pytest.ini`を作成（`src/`をPYTHONPATHに追加）
  - _Requirements: 全般_

- [ ] 1.4 依存関係のインストール確認
  - `uv sync --dev`を実行して依存関係をインストール
  - `ruff check .`、`uv run mypy src/`が動作することを確認
  - _Requirements: 全般_

## Phase 1: コア機能実装（最小限で動くシステム）

### 2. 設定管理の実装

- [x] 2.1 設定クラスの実装
  - `src/mimamori_pi/config/settings.py`を作成
  - Flask基本設定（HOST, PORT, SECRET_KEY）を定義
  - カメラ基本設定（RESOLUTION, FRAMERATE）を定義
  - 環境変数からの読み込み機能を実装
  - _Requirements: 全般_
  - **実装済み**: Settingsクラス、環境変数読み込み、型変換、テスト（カバレッジ100%）

- [x] 2.2 ロギング設定の実装
  - `src/mimamori_pi/config/logging_config.py`を作成
  - ログレベル、フォーマット、ファイル出力を設定
  - コンソールとファイルの両方に出力
  - _Requirements: 6.3_
  - **実装済み**: setup_logging関数、環境変数からのログレベル読み込み、コンソール/ファイルハンドラー、ログローテーション、テスト（カバレッジ78%）

### 3. カメラサービスの基本実装

- [x] 3.1 カメラサービスクラスの骨格作成
  - `src/mimamori_pi/camera/__init__.py`を作成
  - `src/mimamori_pi/camera/camera_service.py`を作成
  - `CameraService`クラスを定義（`__init__`, `start`, `stop`メソッド）
  - _Requirements: 1.2, 2.3, 2.4_
  - **実装済み**: CameraServiceクラスの骨格、型ヒント、docstring、パッケージエクスポート

- [x] 3.2 picamera2の初期化実装
  - picamera2のインポートとエラーハンドリング
  - カメラ設定（解像度、フレームレート）の適用
  - カメラ起動・停止処理の実装
  - _Requirements: 1.2, 2.3, 2.4, 2.6_
  - **実装済み**: picamera2のインポート（ImportErrorハンドリング）、カメラ初期化、設定適用、起動・停止処理、ロギング、エラーハンドリング

- [x] 3.3 カメラサービスのユニットテスト
  - `tests/test_camera_service.py`を作成
  - モックを使用したカメラ初期化テスト
  - 起動・停止のテスト
  - _Requirements: 1.2, 2.3, 2.4_
  - **実装済み**: 8つのテストケース（初期化、picamera2未利用時、起動成功、重複起動、エラーハンドリング、停止成功、未起動時の停止、停止エラー）、カバレッジ100%（camera_service.py）

### 4. ストリーミング機能の実装

- [x] 4.1 Motion JPEGストリーム生成
  - `CameraService.generate_stream()`メソッドを実装
  - フレームキャプチャとJPEGエンコード
  - ジェネレータ関数として実装
  - _Requirements: 1.1, 1.4, 1.5_
  - **実装済み**: generate_stream()メソッド、multipart/x-mixed-replace形式のMJPEGフレーム生成、エラーハンドリング（picamera2未利用時、カメラ未起動時、フレーム取得エラー）

- [x] 4.2 ストリーミングのテスト
  - `tests/test_camera_service.py`にストリーミングテストを追加
  - モックカメラでフレーム生成をテスト
  - _Requirements: 1.1, 1.4, 1.5_
  - **実装済み**: 4つのテストケース（正常系、カメラ未起動、picamera2未利用、フレーム取得エラー）、カバレッジ100%（camera_service.py）

### 5. 最小限のFlaskアプリケーション

- [ ] 5.1 Flaskアプリの初期化
  - `src/mimamori_pi/app.py`を作成
  - Flaskアプリを初期化
  - 設定とロギングを適用
  - CameraServiceのインスタンスを作成
  - _Requirements: 全般_

- [ ] 5.2 ストリーミングルートの実装
  - `src/mimamori_pi/routes/__init__.py`を作成
  - `src/mimamori_pi/routes/stream.py`を作成
  - `/video_feed`ルートを実装（Motion JPEGレスポンス）
  - `/stream/start`、`/stream/stop`ルートを実装
  - _Requirements: 1.1, 2.1, 2.2, 2.3, 2.4_

- [ ] 5.3 最小限のHTMLテンプレート
  - `src/mimamori_pi/templates/base.html`を作成（シンプルなレイアウト）
  - `src/mimamori_pi/templates/index.html`を作成
  - ビデオストリーム表示（`<img src="/video_feed">`）
  - 開始/停止ボタン
  - _Requirements: 1.1, 2.1, 2.2_

- [ ] 5.4 メインルートの実装
  - `src/mimamori_pi/routes/main.py`を作成
  - `/`ルートを実装（index.htmlをレンダリング）
  - _Requirements: 全般_

- [ ] 5.5 動作確認（Milestone 1）
  - `uv run python -m mimamori_pi.app`でアプリを起動
  - ブラウザで`http://localhost:5000`にアクセス
  - ストリーミングが表示されることを確認
  - 開始/停止ボタンが動作することを確認
  - **🎯 ここで最小限のMVPが完成**

## Phase 2: 拡張機能の追加

### 6. ストレージサービスの実装

- [ ] 6.1 ストレージサービスクラスの実装
  - `src/mimamori_pi/storage/__init__.py`を作成
  - `src/mimamori_pi/storage/local_storage.py`を作成
  - `StorageService`クラスを実装
  - ディレクトリ作成、ファイル保存機能
  - _Requirements: 4.2, 4.3_

- [ ] 6.2 ストレージ管理機能の実装
  - ディスク使用量取得機能（`shutil.disk_usage`）
  - 日付ごとのディレクトリ整理（`YYYY-MM-DD/YYYYMMDD_HHMMSS.jpg`）
  - _Requirements: 4.3, 7.2_

- [ ] 6.3 自動クリーンアップ機能の実装
  - ストレージ90%超過時の古い画像削除
  - 最も古い日付ディレクトリから削除
  - _Requirements: 4.5_

- [ ] 6.4 ストレージサービスのテスト
  - `tests/test_storage_service.py`を作成
  - ファイル保存、ディレクトリ整理のテスト
  - 自動クリーンアップのテスト
  - _Requirements: 4.2, 4.3, 4.5_

### 7. スナップショット機能の実装

- [ ] 7.1 スナップショットサービスクラスの実装
  - `src/mimamori_pi/snapshot/__init__.py`を作成
  - `src/mimamori_pi/snapshot/snapshot_service.py`を作成
  - `SnapshotService`クラスを実装
  - CameraServiceとStorageServiceを統合
  - _Requirements: 4.1, 4.2_

- [ ] 7.2 手動スナップショット機能
  - `capture_now()`メソッドを実装
  - カメラからフレームを取得してストレージに保存
  - _Requirements: 4.2_

- [ ] 7.3 定期スナップショット機能
  - `threading.Timer`を使用したスケジューラ実装
  - 設定可能な間隔（5/10/30/60分）
  - `start(interval)`、`stop()`メソッドを実装
  - _Requirements: 4.1, 4.4_

- [ ] 7.4 スナップショットサービスのテスト
  - `tests/test_snapshot_service.py`を作成
  - 手動スナップショットのテスト
  - 定期スナップショットのテスト（モックタイマー使用）
  - _Requirements: 4.1, 4.2, 4.4_

### 8. スナップショットAPI・UIの実装

- [ ] 8.1 スナップショットAPIルートの実装
  - `src/mimamori_pi/routes/api.py`を作成
  - `/api/snapshot/start`（定期スナップショット開始）
  - `/api/snapshot/stop`（定期スナップショット停止）
  - `/api/snapshot/capture`（手動スナップショット）
  - _Requirements: 4.4_

- [ ] 8.2 スナップショット一覧取得機能
  - `StorageService.get_snapshots()`メソッドを実装
  - 日付フィルタリング機能
  - ファイルメタデータ取得
  - _Requirements: 5.1, 5.2_

- [ ] 8.3 スナップショットルートの実装
  - `src/mimamori_pi/routes/snapshots.py`を作成
  - `/snapshots`（一覧ページ）
  - `/snapshots/<path>`（画像取得）
  - `/snapshots/<path>/delete`（画像削除）
  - _Requirements: 5.1, 5.2, 5.3, 5.5_

- [ ] 8.4 スナップショット一覧ページの実装
  - `src/mimamori_pi/templates/snapshots.html`を作成
  - グリッドレイアウトでサムネイル表示
  - 日付フィルター
  - 画像モーダル表示
  - _Requirements: 5.1, 5.2, 5.3, 5.4_

- [ ] 8.5 動作確認（Milestone 2）
  - スナップショット手動取得が動作することを確認
  - 定期スナップショットが動作することを確認
  - 一覧ページで画像が表示されることを確認
  - **🎯 スナップショット機能が完成**

### 9. システム状態監視機能

- [ ] 9.1 システム状態API の実装
  - `src/mimamori_pi/routes/main.py`に`/status`ルートを追加
  - カメラ状態、ストレージ使用量、システム稼働時間を返す
  - JSON形式でレスポンス
  - _Requirements: 7.1, 7.2, 7.3, 7.4_

- [ ] 9.2 メインページにシステム状態表示を追加
  - `templates/index.html`にシステム状態表示エリアを追加
  - カメラ状態、ストレージ使用量、最終スナップショット時刻を表示
  - _Requirements: 7.1, 7.2, 7.4_

- [ ] 9.3 JavaScriptで状態の定期更新
  - `src/mimamori_pi/static/js/app.js`を作成
  - 5秒ごとに`/status`をポーリング
  - システム状態を更新
  - _Requirements: 7.5_

### 10. カメラ回転機能

- [ ] 10.1 カメラ回転メソッドの実装
  - `CameraService.set_rotation(degrees)`メソッドを実装
  - 0/90/180/270度をサポート
  - 回転設定変更時にカメラを再起動
  - _Requirements: 3.1, 3.3, 3.4_

- [ ] 10.2 カメラ回転APIの実装
  - `src/mimamori_pi/routes/api.py`に`/api/camera/rotation`を追加
  - POSTリクエストで回転角度を受け取る
  - _Requirements: 3.2_

- [ ] 10.3 UI に回転設定を追加
  - `templates/index.html`に回転設定ボタンを追加
  - `static/js/app.js`に回転設定のイベントハンドラを追加
  - _Requirements: 3.2_

- [ ] 10.4 カメラ回転のテスト
  - `tests/test_camera_service.py`に回転設定テストを追加
  - _Requirements: 3.1, 3.3_

## Phase 3: UI/UX の改善

### 11. レスポンシブデザインの実装

- [ ] 11.1 CSSフレームワークの実装
  - `src/mimamori_pi/static/css/style.css`を作成
  - CSS変数でカラーパレットを定義（ライト/ダーク）
  - レスポンシブブレークポイント（768px, 1024px）を定義
  - _Requirements: 全般_

- [ ] 11.2 モバイルレイアウトの実装
  - 縦1カラムレイアウト
  - ビデオストリームを画面の70%に
  - タッチ操作に適したボタンサイズ（44x44px以上）
  - _Requirements: 全般_

- [ ] 11.3 タブレット・デスクトップレイアウトの実装
  - タブレット: 横2カラムレイアウト
  - デスクトップ: 3カラムレイアウト
  - _Requirements: 全般_

- [ ] 11.4 ダークモード実装
  - `prefers-color-scheme`でシステム設定を検出
  - 手動切り替えボタンを実装
  - `localStorage`に設定を保存
  - _Requirements: 全般_

- [ ] 11.5 アクセシビリティ対応
  - ARIAラベルを追加
  - キーボード操作対応（Tab, Enter, Escape）
  - コントラスト比WCAG AA準拠を確認
  - _Requirements: 全般_

### 12. エラーハンドリングとユーザーフィードバック

- [ ] 12.1 エラーハンドラーの実装
  - `app.py`にFlaskエラーハンドラーを追加
  - 404、500エラーページを作成
  - _Requirements: 全般_

- [ ] 12.2 ローディング状態の実装
  - ビデオ読み込み中のスピナー表示
  - スナップショット保存中のフィードバック
  - _Requirements: 全般_

- [ ] 12.3 トースト通知の実装
  - 成功・エラーメッセージのトースト表示
  - 3秒後に自動消去
  - _Requirements: 全般_

## Phase 4: デプロイメントと仕上げ

### 13. デプロイメント設定

- [ ] 13.1 systemdサービスファイルの作成
  - `mimamori-pi.service`を作成
  - uvを使用した起動設定
  - 自動再起動、ログ出力設定
  - _Requirements: 6.1, 6.2_

- [ ] 13.2 セットアップスクリプトの作成
  - `scripts/setup.sh`を作成
  - Python 3.12+の確認
  - uvのインストール
  - 依存関係のインストール
  - データディレクトリの作成
  - `.env`ファイルの作成
  - _Requirements: 6.1_

- [ ] 13.3 サービスインストールスクリプトの作成
  - `scripts/install_service.sh`を作成
  - systemdサービスの登録と有効化
  - _Requirements: 6.1_

- [ ] 13.4 Raspberry Pi Zero 2 Wでの動作確認
  - 実機にデプロイ
  - カメラモジュールの接続確認
  - ストリーミング、スナップショットの動作確認
  - パフォーマンステスト（CPU使用率、メモリ使用量）
  - _Requirements: 全般_

### 14. 統合テストと品質保証

- [ ] 14.1 統合テストの実装
  - `tests/integration/test_app.py`を作成
  - Flaskアプリ全体のエンドツーエンドテスト
  - ストリーミング、スナップショット、API呼び出しのテスト
  - _Requirements: 全般_

- [ ] 14.2 テストカバレッジの確認
  - `uv run pytest --cov`を実行
  - カバレッジ80%以上を確認
  - 不足している部分のテストを追加
  - _Requirements: 全般_

- [ ] 14.3 コード品質チェック
  - `ruff format .`でフォーマット
  - `ruff check .`でリント
  - `uv run mypy src/`で型チェック
  - 全てのチェックをパス
  - _Requirements: 全般_

### 15. ドキュメント作成

- [ ] 15.1 READMEの作成
  - プロジェクト概要と機能一覧
  - ハードウェア要件
  - インストール手順（Raspberry Pi Zero 2 W向け）
  - 使用方法
  - トラブルシューティング
  - _Requirements: 全般_

- [ ]* 15.2 開発者向けドキュメントの作成
  - アーキテクチャ説明
  - API仕様
  - 開発環境セットアップ
  - コントリビューションガイド
  - _Requirements: 全般_

- [ ] 15.3 最終動作確認（Milestone 3）
  - 全機能が動作することを確認
  - ドキュメント通りにインストールできることを確認
  - **🎯 Phase 1 MVP完成！**

## 実装の進め方

### タスクの実行順序
- **Phase 0 → Phase 1 → Phase 2 → Phase 3 → Phase 4**の順に実装
- 各Phaseの最後にMilestoneで動作確認
- 問題があれば前のタスクに戻って修正

### テスト駆動開発
- 機能実装と同時にテストを書く
- テストが通ってから次のタスクに進む
- カバレッジ80%以上を維持

### 並行作業可能なタスク
- Phase 2のタスク6-10は、依存関係が少ないため並行作業可能
- Phase 3のUI/UX改善は、Phase 2完了後に並行作業可能

### オプションタスク
- `*`マークのタスクは任意（15.2のみ）
- 時間があれば実装、なくてもMVPは完成

## 注意事項

### 開発環境
- カメラハードウェアが必要な機能は、モックを使用して開発可能
- Raspberry Pi Zero 2 Wでの実機テストは、Phase 4で実施

### コード品質
- 各タスク完了後、`ruff check .`と`uv run mypy src/`を実行
- テストカバレッジ80%以上を維持
- コミット前に必ず品質チェックを実施

### パフォーマンス
- Raspberry Pi Zero 2 Wはリソースが限られているため、パフォーマンスに注意
- ストリーミングは15fps、解像度640x480を推奨
- メモリ使用量を監視

### セキュリティ
- Phase 1ではLAN内のみの使用を想定（認証なし）
- `.env`ファイルに秘匿情報を保存（Gitにコミットしない）
- Phase 2以降でリモートアクセスを実装する際は、認証機能を追加
