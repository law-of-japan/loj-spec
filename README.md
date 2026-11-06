# loj-spec

日本法令をMarkdownで表現するための、実装言語に依存しない規範仕様 **loj/v1alpha1**。
本版の正式な適合対象はL0・L1。alpha版として互換性変更の可能性がある。
HTMLコメントで項・号・細分を明示し、Manifestと見出しから法令意味ASTを構築する。

- [規範仕様の入口](spec/v1alpha1/01-overview.md)
- [Manifest](spec/v1alpha1/02-manifest.md) / [Markdown](spec/v1alpha1/03-markdown.md) / [見出し](spec/v1alpha1/04-headings.md)
- [マーカー](spec/v1alpha1/05-directives.md) / [意味AST・位置](spec/v1alpha1/06-semantic-model.md) / [ID](spec/v1alpha1/07-identifiers.md)
- [参照](spec/v1alpha1/08-references.md) / [検証](spec/v1alpha1/09-validation.md) / [適合データ契約](spec/v1alpha1/10-conformance.md)
- [Manifest Schema](schemas/v1alpha1/manifest.schema.json) / [AST Schema](schemas/v1alpha1/ast.schema.json) / [EBNF](grammar/v1alpha1/directives.ebnf)
- [適合ケース索引](conformance/manifest.json) / [必須25領域の対応表](docs/coverage.md)
- [架空法令のManifest](examples/fictional-law/law.yaml) / [本則第1章](examples/fictional-law/provisions/chapter1.md) / [期待AST](examples/fictional-law/expected.ast.json)
- [調査記録](docs/research.md) / [XML対応](docs/egov-xml-mapping.md) / [設計判断](docs/design-decisions/README.md)
- [実装ガイド](docs/implementation-guide.md) / [移行ガイド](docs/migration-from-legacy.md) / [制限](docs/limitations.md)
- [検証記録](docs/validation.md) / [最終報告](docs/final-report.md) / [変更履歴](CHANGELOG.md)

## 検査

Python 3.9以上で、リポジトリルートから実行する。

```sh
python -m venv .venv
# Windows: .venv/Scripts/python、POSIX: .venv/bin/python を使用
python -m pip install -r requirements.txt
python scripts/verify.py
python -m unittest discover -s tests -v
```

シェルで仮想環境を有効化するか、上記pythonを仮想環境内の実行ファイルに置き換える。
CIも同じ検査を実行する。**資料検査の成功は全L1適合の認証ではない。**
負例L1の診断実行、全Markdown文脈、原典照合、XML往復はまだ検証しない。
期待値は独立した固定データであり、validatorの出力から生成しない。

範囲: 編〜目、条、項、号、細分1〜10、枝番号、削除条、複数附則、不透明な附属資料。
いろは細分、前文、改正・施行履歴、図表セルの型付け等は[未対応](docs/limitations.md)。

ライセンス: [MIT](LICENSE)。貢献時は[CONTRIBUTING](CONTRIBUTING.md)を参照。
