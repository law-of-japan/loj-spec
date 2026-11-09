# loj/v1alpha1 作業完了報告

状態: 凍結した版`loj/v1alpha1`の作成時の記録（経緯）。規範ではない。

本書はv1alpha1の作成時の記録であり、変えない。次期仕様は[規範仕様の入口](../../spec/README.md)にある。

## MAN-03のB案採用後の追記（2026-11-06）

Issue #2のB案をユーザーが承認。非最終附属資料ファイルのフェンス/HTML明示終端と、
後続の非空白本文を規範化した。Schemaの形状は不変。T001〜T075は変更せず、
独立に手定義したT076〜T105を追加。validator出力を期待値に転用していない。
現行105定義＝正式L0 11＋L1 93＋参考L2 1。正式104件の内訳は正例47、負例57。
`python scripts/verify.py` は105定義・正例47のsource/tree・L0負例11に成功。
L1負例46は定義検査のみで、仕様監査をL1検証器の実行成功とは数えない。
`python -m unittest discover -s tests -v` は17件成功。
以下は初期仕様作成時の履歴であり、現在の件数ではない。


2026-11-06（JST）。既存の空loj-specリポジトリに成果物を構築した。
既存Git管理情報・originを保持。コミット、push、PR作成は行っていない。

## 成果物

規範10章、Manifest/AST/ケース/期待結果の4 JSON Schema、コメントと見出しの2 EBNF、
固定適合データ75件、3ファイルに分割した架空法令と完全意味AST、DDR10件、調査・XML対応・
移行・実装ガイド、資料検査スクリプト、16件の監査回帰テスト、GitHub Actionsを追加した。
[README](../../README.md)から各成果物を参照できる。

## 確定した仕様と理由

項・号・細分は厳密なHTMLコメントで明示開始終了。曖昧な暗黙終了を避け、通常表示ではマーカーを隠す。
分類・条の所属は見出しの語とrankで決め、MarkdownのHレベルに固定しない。
条IDはscope基準で章・ファイル名を含めず、適法な分割と分類間移動で安定する。
本文は順序付き混在contentで保存し、元バイトと位置を別に保持する。
Manifestで順序・附則キーを確定し、ファイル境界は条間に限定する。
重要な選択肢と制約は[DDR](../design-decisions/README.md)に比較して記録した。

## 対応・非対応

編、章、節、款、目、条、項、号、細分1〜10、枝番号、削除条、複数附則、直接項形式の附則、
不透明な附属資料を対象とする。正式適合はL0/L1のみ。
前文、いろは等の細分表示、図表セル等の型付け、改正施行履歴、他法令参照、XML可逆変換は未対応。
未対応構造を申告した入力はL1不合格とする。詳細は[制限](../limitations.md)。

## 適合データ・検証

75件＝正式L1正例31＋正式L0負例11＋正式L1負例32＋参考L2負例1。
依頼の25必須領域を[対応表](../coverage.md)で追跡する。実装から期待ASTを自動生成していない。
正例31件の限定source/tree照合とL0負例11件の拒否検査に成功。監査回帰テスト16件成功。
先行構文実験も52件すべて成功した。実コマンド・範囲・位置期待値訂正は[検証記録](../validation.md)。

CIはSchema、Manifest、ケース定義、一意ID、入力と期待値、ローカルリンク、サンプル整合を検査する。
L1負例の実際の診断は今後のvalidator統合で実行する。資料CI成功を全仕様の実装認証とは表示しない。
GitHub Actions自体の実行はpushしていないため未確認である。

## 完了条件の対応

| 条件 | 成果物・確認 |
|---|---|
| v1alpha1規範 | spec/v1alpha1の10章 |
| Manifest Schema | schemas/v1alpha1/manifest.schema.json |
| コメント構文 | 05-directives、directives.ebnf |
| 見出し解釈 | 04-headings、headings.ebnf |
| 意味AST・親子 | 06-semantic-model、ast.schema.json |
| 論理ID | 07-identifiers、固定期待AST |
| 複数ファイル統合 | MAN-03、T016/T017同一ASTの検査 |
| L0/L1条件 | 09-validation、10-conformance |
| 正例負例 | conformance/v1alpha1/valid、invalid、expected |
| 完全架空例 | examples/fictional-law、17ノードAST |
| XML対応 | egov-xml-mapping.md |
| DDR | design-decisions/001〜010 |
| CI機械検査 | scripts/verify.py、validate.yml、ローカル成功 |
| README導線 | リンク監査成功 |
| 実装者資料 | implementation-guide.md |
| 移行資料 | migration-from-legacy.md |
| 矛盾・未定義の整理 | 制限を列挙し、未知構造・拡張を拒否。L2は参考と明示 |

## loj-validatorの次作業

独立v1alpha1パイプラインにManifest統合、Markdown領域判定、マーカースタック、rank見出し、
混在AST、ID、位置、rule対応を実装する。75件のうち正式74件を実装アダプターから実行し、
参考L2を分離する。旧profileとの自動混同を避け、別エンジン又は別言語実装で曖昧さを検出する。
次の仕様マイルストーンでは、原典例とテストを用意したうえで字母細分・前文の対応を拡大し、
L2参照を確定する。今回の範囲にvalidator本体の改修や実法令移行は含めていない。
