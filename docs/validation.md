# 検証記録

## MAN-03 B案採用後の追記（2026-11-06）

Issue #2のB案をユーザーが承認。非最終附属資料ファイルのフェンス/HTML明示終端と、
後続の非空白本文を規範化した。Schemaの形状は不変。T001〜T075は変更せず、
独立に手定義したT076〜T105を追加。validator出力を期待値に転用していない。
現行105定義＝正式L0 11＋L1 93＋参考L2 1。正式104件の内訳は正例47、負例57。
`python scripts/verify.py` は105定義・正例47のsource/tree・L0負例11に成功。
L1負例46は定義検査のみで、仕様監査をL1検証器の実行成功とは数えない。
`python -m unittest discover -s tests -v` は17件成功。
以下は初期仕様作成時の履歴であり、現在の件数ではない。


2026-11-06（JST）。ローカルWindows、Python 3.9.13で実施。
GitHub Actionsの実行は未確認（push未実施）。ワークフローはLinux/Windowsで資料検査を実行する設計。

再現コマンドは[README](../README.md)。外部依存はrequirements.txtで直接依存を固定。
適合期待値は入力から推論せず、人手定義の木と本文から展開して固定した。

初回の位置照合で固定期待値の終端を1バイト過大に記述したことを検出し、
見出し12、開始行32、本文31、終了行27バイトの独立集計でLF全長102に訂正した。
CRLFは4行分の増分で106。パーサー出力を正解として取り込んだ修正ではない。

検査対象: 4 SchemaのDraft 2020-12妥当性、Manifestの型・日付・キー・パス・順序・ファイル、
ケースID一意性、期待結果対応、正例の意味木・本文・ID・選択位置、ローカル文書リンク、サンプル。
L1負例は形式と期待rule対応のみで、診断実行は行わない。
外部URLのリンク生存監視、任意Markdownの全意味解析、全ソース位置、原典照合は対象外。

## 実行結果

loj-specルートから次を実行した。

```powershell
./.venv/Scripts/python scripts/author_data.py
./.venv/Scripts/python scripts/verify.py
./.venv/Scripts/python -m unittest discover -s tests -v
cargo test --manifest-path ../loj-syntax-evaluation/Cargo.toml --target-dir .build/syntax-target --locked --offline
```

- author_data: 75ケースと4 Schemaを展開。パーサー未使用。
- verify: 75定義、正例31件のsource/tree照合、L0負例11件の実際の拒否、サンプル17ノードに成功。
- L1負例32件は定義検査のみ。L2参考負例1件は正式合格数から除外。
- unittest: 16件成功。ID/本文/位置/親子/番号/メタデータの改変検出、YAMLとバイト・パスの回帰検査。
- 構文実験の再実行: 52件成功、0失敗。ビルド出力はloj-spec/.buildへ限定し、実験ソースは変更しなかった。

今回の構文実験結果は試作の旧文法に対する証拠であり、新v1alpha1の75件を実行した結果ではない。
機械検査に含まれないVAL/CONFの適合主張・独立性要件は文書レビュー対象として明示した。
ローカルで検証したOSはWindowsのみ。GitHub上のCI、Linux、Python 3.12の実行結果はまだない。
