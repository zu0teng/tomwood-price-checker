# tomwood-price-checker

このリポジトリは、Tom Woodの価格を自動でチェックし、履歴を記録・通知するPythonスクリプト集です。

## 特徴
- ウェブサイトから価格情報を自動取得
- 価格の履歴をJSONファイルに保存
- 価格変動時に通知

## 使い方
1. 必要なPythonパッケージをインストールします。
   ```bash
   pip install -r requirements.txt
   ```
2. `.env` ファイルを作成し、必要な設定（通知先など）を記入します。
3. スクリプトを実行します。
   ```bash
   python main.py
   ```

## ファイル構成
- `main.py` : メイン実行ファイル
- `scraper.py` : 価格取得用モジュール
- `storage.py` : 履歴保存用モジュール
- `notifier.py` : 通知用モジュール
- `requirements.txt` : 必要なパッケージ一覧

## 注意事項
- `.env` や `price_history.json` などの個人情報・履歴ファイルはGit管理から除外しています。
- 実行にはPython 3.11以上を推奨します。

---

何か分からないことがあれば、気軽にIssueやディスカッションでご質問ください。
