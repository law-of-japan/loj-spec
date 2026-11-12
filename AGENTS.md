# AGENTS.md

このリポジトリで作業するAIエージェント向けの手引きである。規範ではない。規則の正は[CONTRIBUTING](CONTRIBUTING.md)と[規範仕様の入口](spec/README.md)にあり、本書と食い違う場合はそちらに従う。

## このリポジトリ

- 日本法令をMarkdownとYAMLで記録するための規範仕様（LoJ）である。成果物は、仕様の本文、JSON Schema、EBNF、適合ケースの固定データであり、実装ではない。
- 検査器（`loj-validator`）と法令リポジトリの運用は、別のリポジトリで扱う。ここのPythonは、仕様の資料の自己整合を確かめるだけである。
- 本仕様に固有の用語（正本、記録版、Revision、固定参照等）は、[用語集](docs/glossary.md)で意味と定義の要件を確かめてから使う。

## 構成

| 場所 | 内容 | 扱い |
|---|---|---|
| `spec/` | 要件の本文。入口は[spec/README.md](spec/README.md) | 規範 |
| `schemas/`、`grammar/` | JSON Schema、EBNF | 規範 |
| `conformance/` | 適合ケースの索引（`manifest.json`）、入力、期待結果 | 規範。人が書いた固定データ |
| `docs/` | 用語集、実装ガイド、制限、[要件との対応表](docs/coverage.md)等 | 参考 |
| `docs/design-decisions/` | 設計判断の記録（DDR） | 参考。設計の理由はここを引く |
| `docs/archive/` | 役目を終えた文書 | 規範ではない。内容を変えない |
| `examples/` | `loj/v1alpha1`の架空法令の例 | 参考。凍結した版の例 |
| `scripts/`、`tests/` | 資料の検査（`verify.py`）、適合ケースを展開する補助、検査のテスト | — |

`.build/`、`.research/`、`.venv/`はGitの管理外の作業場所である。成果物を置かない。

## 検査

変更したら、リポジトリルートで次の二つを実行し、両方が成功することを確かめる。CIも同じ検査をUbuntuとWindowsで実行する。

```sh
python scripts/verify.py
python -m unittest discover -s tests -v
```

- 仮想環境（`.venv`）がある場合は、その中のpython（Windows: `.venv/Scripts/python`、POSIX: `.venv/bin/python`）を使う。依存は`requirements.txt`にある。
- 検査の成功は、資料の自己整合を示すだけで、適合の認証ではない。L1負例とL3・L4等のケースは形だけを検査する（[制限](docs/limitations.md)）。検査が通ったことを「仕様として正しい」と報告しない。

## 変えてはならないもの

- 凍結した版: `spec/v1alpha1`、`schemas/v1alpha1`、`grammar/v1alpha1`、`conformance/v1alpha1`。
- `docs/archive/`の文書の内容。直してよいのは、冒頭の`状態:`の行、リンク先、要件IDの見出しの形だけである。削除もしない。
- 既存の期待結果を、検査や実装の都合で書き換えない。期待結果は規範から人が書く。検査器やパーサーの出力を写して正解にしない（[CONF-01](spec/common/v1alpha1/04-conformance.md)）。
- 公開した版の意味と、一度公開した要件IDの番号の意味。廃止した番号は欠番として残す。

版の状態（草案・公開・凍結）は、[規範仕様の入口](spec/README.md#規範とするもの)の表を正とする。変更の前に、対象の版の状態を確かめる。

- 草案の版は、版番号を上げずに意味を変えてよい。
- 公開した版は、意味を変えない修正（誤字、リンク、説明の補足）だけを行う。意味を変えるとは、いずれかの入力について、適合の結果、診断の規則、ASTのいずれかが変わることをいう。
- 表の状態を「公開」に変えること、タグを打つことは、指示されたときだけ行う。手順は[CONTRIBUTING](CONTRIBUTING.md)にある。

## 規範を変えるとき

- 要件の本文、JSON Schema、EBNF、正例・負例、必要なDDRを同じ変更で更新する。
- 新しい要件には適合ケースを加える。加えられないときは、理由を[要件との対応表](docs/coverage.md)に書く。
- 用語を加えた・変えたときは[用語集](docs/glossary.md)を、すべての変更で[CHANGELOG](CHANGELOG.md)を更新する。
- 要件IDは`## <ID> <名前>`の見出しで付け、系列とディレクトリの対応は[spec/README.md](spec/README.md)の表に従う。要件IDの見出しは`spec/`の中だけに置く。
- `spec/`から`docs/archive/`へリンクしない。要件は規範を、設計の理由はDDRを引く。
- 規範の間の矛盾を見つけたら、どちらかに合わせて黙って直さず、仕様の欠陥として報告する。
- 一つの規則の要求の語（MUST等）は、正の要件の一か所だけに書く。ほかの要件では、要求の語を使わずに要約し、正へリンクする（[DDR-022](docs/design-decisions/022-spec-structure.md)）。`verify.py`の警告（要求の語と別の要件IDを含む文）が増えていないかを確かめる。

## 適合ケースを扱うとき

- `conformance/`と`examples/`は、`.gitattributes`で改行と文字の変換を禁止している（`-text`）。CRLFのfixtureがある。一括の改行変換、整形、文字の正規化をかけない。
- 互換漢字（例: U+FA51）と異体字セレクタは、保存時に統合漢字へ正規化されることがある。スクリプトの中では`chr(0xFA51)`のようにコードポイントで書き、書いた後でファイルのコードポイントを確かめる。
- 新しく加えた負例と、規則が二つ以上関係しうる負例は、期待結果を書いた人と別のセッションが規範だけを読んで期待結果を書き、突き合わせる（[CONTRIBUTING](CONTRIBUTING.md#期待結果の確かめ方)）。検査器と期待結果が食い違ったら、規範の本文で決め、検査器の出力を根拠にしない。
- 版パッケージのケースを除く負例で、入力のYAMLがschemaに合わないものには、索引の`rejectedBy: schema`の印を付ける（`author_next_cases.py`の`SCHEMA_REJECTED`）。schemaの誤りが期待する規則の違反と対応するかを確かめてから付ける。
- 負例と索引は`scripts/author_*.py`が展開する。対象と実行の順は[CONTRIBUTING](CONTRIBUTING.md)の表にある。CIはこれらを実行しないので、実行したら生成された差分を確かめる。`author_data.py`（v1alpha1）は実行しない。
- 負例の多くは正例の写しであり、元と変更が索引の`derivedFrom`にある。正例を直したら`author_next_cases.py`を実行し直す。忘れると`verify.py`が写しの食い違いとして失敗する。写しのファイルを手で直さない。
- `git bundle`を作り直すとcommitのハッシュが変わる。ハッシュを参照する索引と期待結果も確かめる。
- 大文字・小文字だけが違うファイル名を作らない（Windowsで区別できない）。

## 文書の書き方

- 日本語で、である体で書く。要求レベルはMUST、MUST NOT、SHOULD、MAYで示す。
- 二語以上の列挙値はcamelCase、Markdownのマーカーの名前はkebab-caseで書く（[DDR-022](docs/design-decisions/022-spec-structure.md)）。
- 相対リンクとフラグメントは`verify.py`が検査する。リポジトリの外へ出る相対リンクを書かない。
- 参考の文書に、規範と取り違える書き方（要件IDの見出し、根拠のない「必須」）をしない。

## コミットとPR

- `main`へ直接コミットせず、ブランチを作ってPRにする。
- コミットの件名は、変更の内容を日本語の一文で書く（例: 「役目を終えた文書をdocs/archiveに移し、規範との取り違えを検査する」）。本文に、理由と、変更点の箇条書きを書く。
- 規範の変更と、関係のない文書の整理を一つのPRに混ぜない。
