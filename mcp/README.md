# MCPサーバー

エージェントがオシロスコープ等の画像を直接閲覧できるMCPサーバー。

## 仕組み

画像ファイル → Pythonがbase64変換 → VS Code経由でモデルに画像として渡る

## ファイル

| ファイル | 説明 |
|----------|------|
| mcp_image_server.py | MCPサーバー本体（約80行） |

VS Code設定は `.vscode/mcp.json` で管理。

## 前提条件

- Python 3.12以上
- `pip install fastmcp`
- VS Code + GitHub Copilot Chat 拡張

## 使い方

1. VS Code再起動（MCPサーバー有効化）
2. `list_images(folder)` → 指定フォルダの画像一覧取得
3. `view_image(path)` → 画像を直接見る

## セキュリティガード（組み込み済み）

- シンボリックリンク拒否
- 拡張子制限（.png/.jpg/.jpeg/.bmp のみ）
- ファイルサイズ上限（10MB）
- マジックバイト確認（拡張子偽装対策）
- 監査ログ（アクセス日時・パス・結果を記録）

## カスタマイズ

他環境で使う場合、`mcp_image_server.py` 内の監査ログ出力先を変更すること。
