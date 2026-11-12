# 検査器の実装者向けガイド

次期仕様の検査器（loj-validator等）を作る人向けの参考である。正解は[規範](../spec/README.md)と固定の適合データであり、`scripts/verify.py`や試作のスクリプトではない。特定の言語の型や整数の上限を、規範に持ち込まない。

## 読む順

1. [規範仕様の入口](../spec/README.md): 規範の範囲、要件IDの付け方、組み合わせて使える版の対応表（CORE-05）。
2. [共通](../spec/common/v1alpha1/01-overview.md): ファイルの種類とschemaVersion、YAMLのデータモデル（CORE-03）、文字（CHAR）、適合レベルと結果（VAL）、共通の型（TYPE）、時点値（TIME）、変更の種類（CHG）、固定参照（FIXREF）、派生ビュー（VIEW）、Record間の検査（XREF）。
3. 種類ごとの要件: [版パッケージ](../spec/v1alpha2/01-overview.md)、[履歴マニフェスト](../spec/loj-history/v1alpha1/01-history.md)、[字体注記](../spec/loj-glyphs/v1alpha1/01-glyphs.md)、[登録台帳](../spec/loj-registry/v1alpha1/01-registry.md)、[再構築](../spec/loj-rebuild/v1alpha1/01-rebuild.md)。
4. 各種類の[JSON Schema](../schemas/)。schemaは閉じており、未知のフィールドを拒否する。schemaで表せない制約は本文の要件にある。

設計の理由は[DDR](design-decisions/README.md)（特にDDR-012〜022）にある。

## 検査と入力

| 検査 | 入力 | 結果の単位 |
|---|---|---|
| L0・L1 | 一つの版パッケージ（`law.yaml`とMarkdown） | 版ごと |
| L2 | 同上 | 予約。合格を宣言できない |
| L3 | 一つのRecordの正本の記録版（`history.yaml`、`versions/`、`glyphs.yaml`） | 区分ごと（`historyStructure`、`evidence`。`sourceMatch`は予約） |
| L4 | 登録台帳と、照合する複数のRecordの履歴マニフェスト | 区分ごと（`relationResolution`、`relationConsistency`、`timeConsistency`。`clauseReference`は予約） |
| 登録台帳の検査 | 登録台帳のリポジトリ | 適合レベルとは別（REG-01） |
| 再構築報告の検査 | `rebuild.yaml`と履歴マニフェスト | 適合レベルとは別 |
| 変更の検査 | 正本の二つのcommitの間の履歴 | commitごと（CHG-02、CHG-03） |
| 参照の解決 | 固定参照・Revision参照と、法令リポジトリ・登録台帳 | 参照ごと（FIXREF-03〜07） |

- 各判定は独立している（VAL-02）。履歴構造の検査は、版パッケージのL1の合格を前提にしない。数字の大きいレベルの合格で、小さいレベルの合格を代用しない。
- 読めない入力、知らないschemaVersion、対応表にない組み合わせは、未完了（`incomplete`）とする。対象なし・未完了を合格とみなさない（VAL-04）。
- 判定の結果には、対象とした記録版（リポジトリと正本のcommit）を記録する（VAL-03）。

## 処理の流れ

1. ファイルのバイトを読み、厳密なUTF-8、BOMなし、NULなし、単独のCRなしを確かめる。
2. YAMLは、JSON互換のデータモデルだけを受け付ける安全な読み込みで読む（CORE-03）。重複キー、タグ、アンカー、エイリアス、merge key、複数文書を拒否する。
3. `schemaVersion`で種類を決め、そのschemaで検査する。知らない値は推測で読み替えない。
4. 種類ごとの意味の検査を行う。版パッケージは、v1alpha1と同じく、CommonMarkの領域、予約コメント、見出しのrankスタック、明示マーカーのスタックから意味ASTを作り、ID・番号・構造を検査する。
5. 履歴マニフェストは、revision_id、時点値、版の順序、成立根拠が参照する関係、版パッケージの配置、本文の状態、効力の終了を検査する（HIST、REV、TIME）。
6. L4では、登録台帳でRecordを解決し、関係・時点の整合を確かめる。解決の結果は、解決済み・未取得・不存在確認済みの三つで報告する。未取得は不合格にしない。
7. 結果を[検査の報告](../schemas/common/v1alpha1/report.schema.json)の形で出す。

## 検査の報告

- `results`は、検査（`check`）ごと、L3・L4では区分（`category`）ごとに、`pass`・`fail`・`notApplicable`・`incomplete`のいずれかを持つ。
- `diagnostics`の各項目は、`rule`（要件ID）、`schemaVersion`（その規則を定める種類と版。共通の規則は`common/v1alpha1`）、`class`（`error`・`warning`・`undetermined`・`pending`）を持つ。実装固有の`code`・`message`・`location`は加えてよい。
- 要件IDは版ごとに意味を持つので、`rule`と`schemaVersion`の組で規則を特定する。
- 警告・判定不能・保留は、不合格の診断と区別する。警告だけでは不合格にしない。

## 適合ケースの使い方

- 索引は種類ごとにある（`conformance/<種類>/<版>/manifest.json`）。形は[索引のschema](../schemas/common/v1alpha1/conformance.schema.json)、期待結果は[期待結果のschema](../schemas/common/v1alpha1/expected.schema.json)にある。
- 入力の`kind`は、`package`（`law.yaml`）、`repository`（法令リポジトリのディレクトリ）、`registry`（登録台帳のディレクトリ）、`records`（登録台帳と複数の法令リポジトリ）、`change`（`git bundle`と、比べる二つのcommit）、`reference`（`git bundle`、登録台帳、参照の文字列）である。
- `git bundle`は、`git clone <bundle> <dir>`で取り出す。commitのハッシュは固定であり、作り直すと変わる。
- 成功するケースは、期待結果に挙げた`results`がすべて報告にあって一致し、ケースの検査（L3・L4は区分）に属する規則の`error`の診断がないことを確かめる。期待結果に挙げていない検査（区分）の結果と診断は比べない（CONF-01）。版パッケージのL1の正例では、意味ASTを位置情報を除いて完全一致で比べ、`positions`をソースのバイトで照合する。L0の正例はASTを持たず、L0の`pass`だけを比べる。L1の違反を含む入力も、L0では合格する（pkg-145）。
- 失敗するケースは、期待する`error`の診断（`rule`と`schemaVersion`の組）をすべて含むことを確かめる。ほかの診断が加わってもよい。部分的なASTは比べない。期待結果の診断に`location`があれば、同じ規則の診断の`location`の`path`・`start`・`end`も一致させる。位置はUTF-8のバイトで数え、行は行末の改行（CRLFは2バイト）まで含む（SRC-01）。
- 索引の`rejectedBy: schema`は、入力がschemaに合わない負例の印である。資料の検査のためのもので、ケースを満たすかの判定には使わない。schemaの違反でも、期待結果の規則の診断を報告する必要がある（CONF-01）。
- 結果は検査（L3・L4は区分）ごとに集計する（CONF-02）。予約の区分、L2、参考のケースを、正式な結果に混ぜない。
- どの要件にケースがないかは[要件との対応表](coverage.md)にある。

## v1alpha1から流用できる部分

- 版パッケージのMarkdownの扱い（CommonMarkの領域、予約コメント、見出し、マーカー、ID、ソースの位置）は、v1alpha1から大きく変わっていない。v1alpha1の実装を土台にできる。
- 変わる点: `schemaVersion`が`loj/v1alpha2`、`Paragraph`の`numbering`（`explicit`、無番号の項は`implicit`。PARA-01）、前文・制定文（PRE）、目次（TOC）、表の構造（TABLE）、細分の表示のいろは・括弧付きの十進（DISP-01）、条の見出しの括弧書き（HEAD-01）、診断に`schemaVersion`と`class`が加わる。規則と各レベルの対応は[v1alpha2の検証](../spec/v1alpha2/10-validation.md)にある。
- 目次（TOC-01）は中身を解析しない。目次と本文の見出しの一致はL1で検査しないので、L1の合格を、目次が本文と一致することの確認として報告しない。
- 履歴マニフェスト・字体注記・登録台帳・再構築報告と、L3・L4・変更・参照の検査は、新しく作る。

## 実装上の注意

- 本文のコードポイント列を正規化しない。互換漢字（例: U+FA51）は、NFC等で統合漢字に変わる。読み込み・比較・出力のどこでも正規化しないこと（CHAR-01）。
- ソースの位置は、文字数ではなく元のUTF-8のバイトで数える。CRLFや正規化後の文字列から逆算しない。
- `label`等の表示用の値を、参照の解決・同一性の判断・順序の決定に使わない。
- commitメッセージのtrailer（`LoJ-Change`、`LoJ-Revisions`）はUTF-8で読む。
- 推奨のCLIの例は`check <パス> --level L3 --json`である。推奨であり、規範ではない。
