# loj-spec

日本法令をMarkdownとYAMLで記録するための、実装言語に依存しない規範仕様。
版パッケージ（`loj/v1alpha2`）と、履歴マニフェスト・字体注記・登録台帳・再構築報告の4種類（各`v1alpha1`）からなる。
alpha版であり、互換性のない変更があり得る。正式な適合対象はL0・L1、L3の履歴構造・根拠、L4の関係の解決・関係の整合・時点の整合である。L2、L3の原典照合、L4の条項参照の解決は予約である。

- [規範仕様の入口](spec/README.md)（規範の範囲、要件IDの付け方、組み合わせて使える版）
- [用語集](docs/glossary.md)（正本、記録版、Revision、固定参照等、本仕様に固有の用語と、その定義の要件）
- [共通](spec/common/v1alpha1/01-overview.md) / [版パッケージ](spec/v1alpha2/01-overview.md) / [履歴マニフェスト](spec/loj-history/v1alpha1/01-history.md) / [字体注記](spec/loj-glyphs/v1alpha1/01-glyphs.md) / [登録台帳](spec/loj-registry/v1alpha1/01-registry.md) / [再構築](spec/loj-rebuild/v1alpha1/01-rebuild.md)
- [JSON Schema](schemas/) / [EBNF](grammar/v1alpha2/directives.ebnf)
- 適合ケース: [版パッケージ](conformance/v1alpha2/manifest.json) / [共通](conformance/common/v1alpha1/manifest.json) / [履歴](conformance/loj-history/v1alpha1/manifest.json) / [字体注記](conformance/loj-glyphs/v1alpha1/manifest.json) / [登録台帳](conformance/loj-registry/v1alpha1/manifest.json) / [再構築](conformance/loj-rebuild/v1alpha1/manifest.json) / [要件との対応表](docs/coverage.md)
- 完全な例: [祝日法の法令リポジトリ](conformance/loj-history/v1alpha1/valid/hist-001/repo/history.yaml)（適合ケースの正例）
- [実装ガイド](docs/implementation-guide.md) / [移行の手順](docs/migration-from-legacy.md) / [制限](docs/limitations.md) / [XML対応](docs/egov-xml-mapping.md)
- [設計判断](docs/design-decisions/README.md) / [検証記録](docs/validation.md) / [変更履歴](CHANGELOG.md)
- [経緯の記録](docs/archive/README.md)（規範ではない。採用前の統合案、v1alpha1の作成時の報告と調査）

凍結した版: [loj/v1alpha1](spec/v1alpha1/01-overview.md)（内容を変えない。[適合ケース](conformance/v1alpha1/manifest.json)、[架空法令の例](examples/fictional-law/law.yaml)、[作成時の報告](docs/archive/final-report.md)、[調査記録](docs/archive/research.md)）。

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
CIも同じ検査を実行する。**資料検査の成功は適合の認証ではない**（[CONF-03](spec/common/v1alpha1/04-conformance.md)）。
schema、正例の意味木と位置、L0負例の拒否は検査するが、L1負例とL3・L4・登録台帳・再構築・変更・参照のケースは形だけを検査する。その結果を確かめるには検査器が要る。
期待値は人が書いた固定データであり、検査器の出力から生成しない。

範囲と、まだ対応していないものは[制限](docs/limitations.md)にある。

ライセンス: [MIT](LICENSE)。貢献時は[CONTRIBUTING](CONTRIBUTING.md)を参照。
