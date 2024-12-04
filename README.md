# gomod-dependency-fetcher

`go.mod` ファイルに記載されたすべての依存関係を取得し、それらの参照用URLを生成するPythonツールです。

## 特徴

- `go.mod` にリストされたすべての依存関係を抽出します。
- 各依存モジュールの [pkg.go.dev](https://pkg.go.dev/) に基づいたURLを生成します。

## 前提条件

- **Go**: システムにGoがインストールされており、`PATH` に登録されている必要があります。
  - [Goインストールガイド](https://go.dev/doc/install)
- **Python**: Python 3.6以上が必要です。

## 使い方

```
$ python main.py
```