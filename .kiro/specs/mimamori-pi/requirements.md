# Requirements Document

## Introduction

mimamori-piは、Raspberry Piとカメラモジュールを使用した赤ちゃん見守りシステムです。ベビーベッド近くに設置し、保護者がリアルタイムで赤ちゃんの様子を確認できる機能を提供します。初期段階ではLAN内でのアクセスに対応し、将来的には外部アクセスや機械学習による安全確認機能の拡張を想定しています。

## Glossary

- **mimamori-pi**: Raspberry Piベースの赤ちゃん見守りシステム全体
- **Camera Module**: Raspberry Piに接続されたカメラモジュール（Camera Module v2/v3またはHQ Camera）
- **Web Interface**: ユーザーがブラウザからアクセスする監視画面
- **Streaming Service**: picamera2ライブラリを使用したビデオストリーミング機能
- **LAN**: ローカルエリアネットワーク（家庭内ネットワーク）
- **Snapshot Service**: 定期的に静止画を保存する機能
- **Safety Detection**: 機械学習を用いた赤ちゃんの安全確認機能
- **Flask Application**: Webサーバーとして動作するPythonアプリケーション
- **Edge Processing**: Raspberry Pi上でのローカル処理
- **Cloud Processing**: AWS LambdaなどのクラウドサービスでのServerless処理
- **Cloud Storage**: AWS S3などのクラウドストレージサービス

## Requirements

### Requirement 1

**User Story:** 保護者として、LAN内の任意のデバイスから赤ちゃんのリアルタイム映像を確認したい。そうすることで、別の部屋にいても赤ちゃんの様子を常に把握できる。

#### Acceptance Criteria

1. WHEN 保護者がブラウザでWeb Interfaceにアクセスする, THE mimamori-pi SHALL Motion JPEGフォーマットでリアルタイムビデオストリームを表示する
2. THE mimamori-pi SHALL picamera2ライブラリを使用してカメラを制御する
3. THE mimamori-pi SHALL LAN内の複数デバイスから同時アクセスを許可する
4. THE mimamori-pi SHALL 15fps以上のフレームレートでストリーミングを提供する
5. THE mimamori-pi SHALL 640x480ピクセル以上の解像度でビデオを配信する

### Requirement 2

**User Story:** 保護者として、カメラのストリーミングを手動で開始・停止したい。そうすることで、必要な時だけカメラを稼働させてプライバシーを保護できる。

#### Acceptance Criteria

1. THE Web Interface SHALL ストリーミング開始ボタンを提供する
2. THE Web Interface SHALL ストリーミング停止ボタンを提供する
3. WHEN 保護者がストリーミング開始ボタンを押す, THE mimamori-pi SHALL picamera2を使用してカメラを起動する
4. WHEN 保護者がストリーミング停止ボタンを押す, THE mimamori-pi SHALL カメラを安全に停止する
5. THE Web Interface SHALL 現在のストリーミング状態（稼働中/停止中）を表示する
6. THE mimamori-pi SHALL カメラ起動後2秒以内にストリーミングを開始する

### Requirement 3

**User Story:** 保護者として、カメラの向きや設置角度を調整したい。そうすることで、ベビーベッド全体を適切に映すことができる。

#### Acceptance Criteria

1. THE mimamori-pi SHALL カメラ映像の回転設定（0度、90度、180度、270度）をサポートする
2. THE Web Interface SHALL カメラ回転設定を変更する機能を提供する
3. WHEN 保護者が回転設定を変更する, THE mimamori-pi SHALL 新しい設定を適用してストリーミングを再開する
4. THE mimamori-pi SHALL 設定変更後も3秒以内にストリーミングを再開する

### Requirement 4

**User Story:** 保護者として、定期的に赤ちゃんの静止画を自動保存したい。そうすることで、後から赤ちゃんの睡眠パターンや様子を振り返ることができる。

#### Acceptance Criteria

1. THE mimamori-pi SHALL 設定可能な間隔（5分、10分、30分、60分）で静止画を自動保存する
2. THE Snapshot Service SHALL タイムスタンプ付きのファイル名で画像を保存する
3. THE mimamori-pi SHALL 保存された画像を日付ごとにディレクトリ整理する
4. THE Web Interface SHALL 自動保存機能の有効化・無効化を切り替える機能を提供する
5. THE mimamori-pi SHALL ストレージ容量が90%を超える場合、最も古い画像から自動削除する

### Requirement 5 (将来拡張)

**User Story:** 保護者として、保存された静止画を一覧表示して確認したい。そうすることで、赤ちゃんの様子を時系列で振り返ることができる。

#### Acceptance Criteria

1. THE Web Interface SHALL 保存された静止画を日付順に一覧表示する
2. THE Web Interface SHALL 各画像のサムネイルと撮影日時を表示する
3. WHEN 保護者がサムネイルをクリックする, THE Web Interface SHALL フルサイズ画像を表示する
4. THE Web Interface SHALL 日付範囲でフィルタリングする機能を提供する
5. THE Web Interface SHALL 不要な画像を削除する機能を提供する

### Requirement 6

**User Story:** システム管理者として、Raspberry Pi起動時に自動的に監視システムが起動してほしい。そうすることで、電源を入れるだけで監視を開始できる。

#### Acceptance Criteria

1. THE mimamori-pi SHALL Raspberry Pi起動時にWeb Interfaceを自動起動する
2. THE mimamori-pi SHALL システム起動後60秒以内にアクセス可能な状態になる
3. WHEN システム起動に失敗する, THE mimamori-pi SHALL エラーログを記録する
4. THE mimamori-pi SHALL ネットワーク接続が確立されるまで待機する

### Requirement 7

**User Story:** 保護者として、システムの動作状態（カメラ状態、ストレージ使用量など）を確認したい。そうすることで、システムが正常に動作しているか把握できる。

#### Acceptance Criteria

1. THE Web Interface SHALL カメラの接続状態を表示する
2. THE Web Interface SHALL ストレージの使用量と残量を表示する
3. THE Web Interface SHALL システムの稼働時間を表示する
4. THE Web Interface SHALL 最後に保存された画像の日時を表示する
5. THE mimamori-pi SHALL 5秒ごとにシステム状態を更新する

### Requirement 8 (将来拡張)

**User Story:** 保護者として、外出先からもインターネット経由で赤ちゃんの様子を確認したい。そうすることで、家を離れていても安心できる。

#### Acceptance Criteria

1. THE mimamori-pi SHALL セキュアな認証機能を提供する
2. THE mimamori-pi SHALL HTTPS通信をサポートする
3. WHERE リモートアクセスが有効である, THE mimamori-pi SHALL VPN経由またはクラウドサービス経由でのアクセスを許可する
4. WHERE クラウド統合が有効である, THE mimamori-pi SHALL 画像をクラウドストレージ（S3など）にアップロードする機能を提供する
5. THE mimamori-pi SHALL ローカルストレージとクラウドストレージの選択を設定可能にする

### Requirement 9 (将来拡張)

**User Story:** 保護者として、赤ちゃんが危険な姿勢（うつ伏せなど）になっていないか自動検知してほしい。そうすることで、窒息などのリスクを早期に発見できる。

#### Acceptance Criteria

1. THE Safety Detection SHALL 機械学習モデルを使用して赤ちゃんの姿勢を分析する
2. WHERE エッジ処理が選択されている, THE Safety Detection SHALL Raspberry Pi上でモデルを実行する
3. WHERE クラウド処理が選択されている, THE mimamori-pi SHALL 画像をクラウド（AWS Lambdaなど）に送信して分析を実行する
4. WHEN 危険な姿勢を検知する, THE mimamori-pi SHALL 保護者に通知を送信する
5. THE Safety Detection SHALL 顔の向き（上向き/下向き）を判定する
6. THE mimamori-pi SHALL 検知結果をログに記録する
7. THE mimamori-pi SHALL エッジ処理とクラウド処理の選択を設定可能にする
