# 用語集

状態: 参考。規範ではない。

本仕様に出てくるプロジェクト固有の用語を、一か所にまとめた索引である。各用語の定義は「定義」の列の要件にあり、本書と規範が食い違う場合は規範を正とする（食い違いは仕様の欠陥として報告する）。対象は[組み合わせて使える版](../spec/README.md#組み合わせて使える版)の組1（`loj/v1alpha2`と、共通の型・4種類の`v1alpha1`）である。凍結した`loj/v1alpha1`の用語は含めない。

- 「表記」の列は、データやschemaに現れるフィールド名・値・型の名前である。
- 「定義」の列は、その用語を主に定める要件を先に置き、補う要件を後に続ける。
- 二語以上の列挙値はcamelCase、Markdownのマーカーの名前はkebab-caseで書く（[DDR-022](design-decisions/022-spec-structure.md)）。
- 似た語の区別は、末尾の[取り違えやすい用語](#取り違えやすい用語)にまとめた。

## データの全体像

| 用語 | 表記 | 意味 | 定義 |
|---|---|---|---|
| LoJ | Law of Japan | 日本法令をMarkdownとYAMLで記録するためのデータと、その規範仕様 | [規範仕様の入口](../spec/README.md) |
| 正本 | — | 人がPRで編集する規範的なデータ（登録台帳、履歴マニフェスト、版パッケージ、字体注記、再構築報告）と、そのGit履歴。適合の判定と固定参照の対象は正本だけである | [CORE-01](../spec/common/v1alpha1/01-overview.md#core-01-データの構成)、[VIEW-01](../spec/common/v1alpha1/09-views.md#view-01-定義と一方向性) |
| 派生ビュー | — | 正本から生成器が機械的に作る閲覧用の成果物（historyブランチ、版間差分等）。規範外で、判定の対象にも判断の根拠にもならない | [VIEW-01](../spec/common/v1alpha1/09-views.md#view-01-定義と一方向性) |
| 登録台帳 | registry | 法令を同定するRecordの集合。法令リポジトリとは別の一つのリポジトリに置く | [CORE-01](../spec/common/v1alpha1/01-overview.md#core-01-データの構成)、[REG-01](../spec/loj-registry/v1alpha1/01-registry.md#reg-01-置き場所と形式) |
| 登録空間 | `space` | Record IDを発行する名前空間。小文字の短い識別子（例: `loj`）で示す。適合ケースの登録空間は`loj` | [RID-04](../spec/loj-registry/v1alpha1/02-record-ids.md#rid-04-登録空間の識別子) |
| Record | Record | 登録台帳で同定する一つの法令。登録台帳の一つのファイルに当たり、登録空間とRecord IDの組で指す | [REG-02](../spec/loj-registry/v1alpha1/01-registry.md#reg-02-recordのファイル)、[TYPE-01](../spec/common/v1alpha1/05-types.md#type-01-recordref) |
| Record ID | `id` | Recordの永続的な識別子。新しいものはCrockford Base32の小文字10文字。既存の`law.id`はそのまま引き継ぐ | [RID-01](../spec/loj-registry/v1alpha1/02-record-ids.md#rid-01-新しいrecord-idの発行)、[RID-02](../spec/loj-registry/v1alpha1/02-record-ids.md#rid-02-idの文字種と長さ)、[REB-02](../spec/loj-rebuild/v1alpha1/01-rebuild.md#reb-02-idの維持) |
| 法令リポジトリ | — | 一つのRecordの履歴を置くGitリポジトリ。履歴マニフェスト、版ごとの版パッケージ・字体注記、再構築報告を置く。名前はRecord IDと同じにする | [CORE-01](../spec/common/v1alpha1/01-overview.md#core-01-データの構成)、[HIST-01](../spec/loj-history/v1alpha1/01-history.md#hist-01-ファイルと形式)、[RID-03](../spec/loj-registry/v1alpha1/02-record-ids.md#rid-03-リポジトリの名前) |
| 正本ブランチ | `canonicalBranch` | 正本を置くブランチ。その履歴をforce push等で書き換えてはならない | [CORE-01](../spec/common/v1alpha1/01-overview.md#core-01-データの構成)、[REG-02](../spec/loj-registry/v1alpha1/01-registry.md#reg-02-recordのファイル)、[FIXREF-04](../spec/common/v1alpha1/08-references.md#fixref-04-commitの条件) |
| 記録版 | — | 正本のあるcommitにおける記録の内容。同じRevisionでも、記録訂正や復元の進展で記録版は更新される。判定の結果には対象の記録版を記録する | [VAL-03](../spec/common/v1alpha1/03-validation.md#val-03-判定の入力と対象の記録版)、[FIXREF-01](../spec/common/v1alpha1/08-references.md#fixref-01-参照の種類と構造化形式) |
| 版、Revision | Revision | 法令の一つの状態。単位は「一つの施行時点 × 一つの改正法令」 | [REV-04](../spec/loj-history/v1alpha1/02-revision-ids.md#rev-04-版の粒度)、[HIST-04](../spec/loj-history/v1alpha1/01-history.md#hist-04-起点と基礎状態) |
| revision_id | `revision` | Revisionの識別子。Crockford Base32の小文字8文字の不透明な値で、一つのRecordの中で一意。施行日や順序を導かない | [REV-01](../spec/loj-history/v1alpha1/02-revision-ids.md#rev-01-revision_idの性質) |
| 可読ラベル | `label` | 表示用の名前（例: `2007-01-01_H17-043`）。一意でなくてよく、訂正で変わる。参照の解決に使わない | [REV-02](../spec/loj-history/v1alpha1/02-revision-ids.md#rev-02-可読ラベル)、[REG-02](../spec/loj-registry/v1alpha1/01-registry.md#reg-02-recordのファイル) |
| 旧リポジトリ、旧形式 | `legacy` | 次期仕様より前の形式で法令を収めていたリポジトリ。凍結し、原典から再構築して移す | [REB-01](../spec/loj-rebuild/v1alpha1/01-rebuild.md#reb-01-対象と新しい版で書くこと)、[REB-08](../spec/loj-rebuild/v1alpha1/01-rebuild.md#reb-08-既存の参照の維持と旧形式) |

## ファイル

法令と、その版（Revision）を記録するファイルである。仕様の版（schemaVersion）は[次の表](#仕様の版とschema)にまとめた。

| 用語 | 表記 | 意味 | 定義 |
|---|---|---|---|
| ファイルの種類 | — | 版パッケージ、履歴マニフェスト、字体注記、再構築報告、登録台帳のRecordの5種類 | [CORE-02](../spec/common/v1alpha1/01-overview.md#core-02-ファイルの種類とschemaversion) |
| 版パッケージ | `law.yaml`と本文のMarkdown | 一つの法令の一つの版（Revision）の`law.yaml`と、そこに列挙したMarkdown。法令リポジトリの`versions/<revision_id>/`に置く。「版」は法令の版であり、仕様の版ではない | [BASIC-01](../spec/v1alpha2/01-overview.md#basic-01-入力とschemaversion)、[CORE-02](../spec/common/v1alpha1/01-overview.md#core-02-ファイルの種類とschemaversion) |
| Manifest | `law.yaml` | 版パッケージのメタデータ（`law`）と、本文のファイルの一覧（`documents`） | [MAN-01](../spec/v1alpha2/02-manifest.md#man-01-lawyamlの形) |
| 履歴マニフェスト | `history.yaml` | 一つのRecordの履歴（Revision、そのRecordを終点とする関係、収録範囲、効力の終了）。法令リポジトリの最上位に置く | [HIST-01](../spec/loj-history/v1alpha1/01-history.md#hist-01-ファイルと形式)、[HIST-02](../spec/loj-history/v1alpha1/01-history.md#hist-02-トップレベル) |
| 字体注記 | `glyphs.yaml` | 原典との対応を決められなかった字や、特に記録が要る字の注記。版ごとに一つ、版パッケージと同じディレクトリに置く | [GLYPH-01](../spec/loj-glyphs/v1alpha1/01-glyphs.md#glyph-01-ファイルと形式) |
| 再構築報告 | `rebuild.yaml` | 旧リポジトリから移したRecordの、再構築の進み具合と見つかった差の記録。正本に属するが、法令の状態のデータではない | [REBR-01](../spec/loj-rebuild/v1alpha1/02-report.md#rebr-01-置き場所と形式) |
| Recordのファイル | `records/<Record ID>.yaml` | 登録台帳の中の、Recordごとの一つのファイル | [REG-01](../spec/loj-registry/v1alpha1/01-registry.md#reg-01-置き場所と形式)、[REG-02](../spec/loj-registry/v1alpha1/01-registry.md#reg-02-recordのファイル) |

## 仕様の版とschema

各ファイルの形式を定める仕様とschemaの版である。法令の版（Revision）とは別の概念である。

| 用語 | 表記 | 意味 | 定義 |
|---|---|---|---|
| schemaVersion | `schemaVersion` | 各ファイルが最上位で宣言する、自身の種類と仕様の版。接頭辞は種類ごとに`loj/`（版パッケージ）、`loj-history/`、`loj-glyphs/`、`loj-rebuild/`、`loj-registry/`。知らない値のファイルは処理不能とする | [CORE-02](../spec/common/v1alpha1/01-overview.md#core-02-ファイルの種類とschemaversion)、[CORE-04](../spec/common/v1alpha1/01-overview.md#core-04-版番号) |
| 仕様の版、版番号 | `v1alpha2`、`v1alpha1`等 | 種類ごとに独立して上げる仕様の版。新しい種類は`v1alpha1`から始める。alphaの版は版の間の互換を保証しないが、一度公開した版の意味は変えない | [CORE-04](../spec/common/v1alpha1/01-overview.md#core-04-版番号)、[CORE-05](../spec/common/v1alpha1/01-overview.md#core-05-種類ごとの版と対応表) |
| 対応表 | — | 組み合わせて使える仕様の版の一覧。表にない組み合わせは処理不能として報告してよい | [CORE-05](../spec/common/v1alpha1/01-overview.md#core-05-種類ごとの版と対応表)、[規範仕様の入口](../spec/README.md#組み合わせて使える版) |
| 版の状態 | 草案、公開、凍結 | 仕様の版が、変えてよい段階にあるかどうか。規範仕様の入口の表を正とする | [規範仕様の入口](../spec/README.md#版の状態) |
| 草案の版 | 草案 | `main`にあるが、公開していない仕様の版。版番号を上げずに意味を変えてよく、予告なく変わる | [規範仕様の入口](../spec/README.md#版の状態) |
| 公開した版 | 公開 | 規範仕様の入口の表の状態を「公開」とした変更が、`main`に入った仕様の版。意味を変えない。公開したcommitに、schemaVersionと同じ名前のタグを打つ | [規範仕様の入口](../spec/README.md#版の状態)、[CORE-04](../spec/common/v1alpha1/01-overview.md#core-04-版番号) |
| 意味を変える | — | いずれかの入力について、適合の結果、診断の規則、ASTのいずれかが変わること | [規範仕様の入口](../spec/README.md#版の状態) |
| 凍結した版 | `loj/v1alpha1` | 公開した版のうち、保守を止めた仕様の版。内容を変えない。検査器と適合データが対応し続けることを求めない | [規範仕様の入口](../spec/README.md#凍結した版) |
| 共通の型 | `schemas/common/` | 各種類のschemaが参照する型（RecordRef、Source、Evidence、Verification、Scope、時点値等）。それを使う種類とは別に版を上げる | [共通の型](../spec/common/v1alpha1/05-types.md)、[CORE-04](../spec/common/v1alpha1/01-overview.md#core-04-版番号) |
| 閉じたschema | — | 未知のフィールドを拒否するschema。新しいフィールドは新しいschemaVersionでだけ定める | [CORE-02](../spec/common/v1alpha1/01-overview.md#core-02-ファイルの種類とschemaversion) |

## 版パッケージの構造

| 用語 | 表記 | 意味 | 定義 |
|---|---|---|---|
| scope | `main`、`supplement/<key>`、`appendix/<key>` | 本則・附則・附属資料のそれぞれの区間。`documents`の`parent`で指定し、この順に連続して置く | [MAN-01](../spec/v1alpha2/02-manifest.md#man-01-lawyamlの形)、[MAN-03](../spec/v1alpha2/02-manifest.md#man-03-読み込みの順序とファイルの分割) |
| 本則 | MainProvision | 法令の本則のscope | [AST-01](../spec/v1alpha2/06-semantic-model.md#ast-01-意味astの形)、[ID-01](../spec/v1alpha2/07-identifiers.md#id-01-idの導出) |
| 附則 | SupplementaryProvision、`supplements` | `key`で区別する附則のscope。条の形式か直接の項の形式のどちらか。改正法の附則は収録しない | [HEAD-03](../spec/v1alpha2/04-headings.md#head-03-附則と附属資料のscope)、[BASIC-03](../spec/v1alpha2/01-overview.md#basic-03-対象とする構造と収録しないもの) |
| key | `key` | 附則・附属資料を区別する名前（小文字の英数字とハイフン）。位置による自動採番を禁止する。制定時の附則の推奨は`original` | [MAN-01](../spec/v1alpha2/02-manifest.md#man-01-lawyamlの形) |
| 附属資料 | AppendedMaterial、`appendices` | 別表等。内部を型付けせず、不透明な本文として保持する | [HEAD-03](../spec/v1alpha2/04-headings.md#head-03-附則と附属資料のscope)、[BASIC-03](../spec/v1alpha2/01-overview.md#basic-03-対象とする構造と収録しないもの) |
| 分類 | Part、Chapter、Section、Subsection、Division | 編・章・節・款・目。rank（1〜5）で入れ子を決める | [HEAD-01](../spec/v1alpha2/04-headings.md#head-01-見出しの形)、[HEAD-02](../spec/v1alpha2/04-headings.md#head-02-分類と所属) |
| rank | — | 分類の深さ。Part=1〜Division=5、Article=6。見出しの`#`の数（Hレベル）ではなくrankで所属を決める | [HEAD-02](../spec/v1alpha2/04-headings.md#head-02-分類と所属) |
| 条 | Article | `第N条`・`第N條`の見出しで始まる単位。`status`は`active`か`deleted` | [HEAD-01](../spec/v1alpha2/04-headings.md#head-01-見出しの形)、[AST-01](../spec/v1alpha2/06-semantic-model.md#ast-01-意味astの形) |
| 削除条 | `status: deleted` | ラベルの直後の行に`削除`だけを置いた条。項を持たず、元の条のIDを保つ | [HEAD-04](../spec/v1alpha2/04-headings.md#head-04-削除条) |
| 項 | Paragraph、`paragraph` | 条（または直接の項の形式の附則）の下の単位 | [DIR-01](../spec/v1alpha2/05-directives.md#dir-01-マーカーの字句)、[DIR-02](../spec/v1alpha2/05-directives.md#dir-02-対応入れ子空の禁止) |
| 無番号の項 | `numbering=implicit` | 原典に項番号がない項。`number`は原典上の順序で明示する。省略時は`explicit` | [PARA-01](../spec/v1alpha2/09-structures.md#para-01-無番号の項) |
| 号 | Item、`item` | 項の下の単位 | [DIR-01](../spec/v1alpha2/05-directives.md#dir-01-マーカーの字句)、[DIR-02](../spec/v1alpha2/05-directives.md#dir-02-対応入れ子空の禁止) |
| 細分 | Subitem、`subitem`、`level` | 号の下の単位。`level`は1〜10で、飛び越せない | [DIR-02](../spec/v1alpha2/05-directives.md#dir-02-対応入れ子空の禁止) |
| 表、行、セル | Table、Row、Cell | 項・号・細分の本文の中の法令の表。マーカーで書き、GFMの表は使わない | [TABLE-01](../spec/v1alpha2/09-structures.md#table-01-表の構造)、[TABLE-03](../spec/v1alpha2/09-structures.md#table-03-セル) |
| 行のkey | `row key=…` | 表の行の不透明な識別子（Crockford Base32の小文字4文字）。改正・訂正で変えず、削った行のkeyも再使用しない | [TABLE-02](../spec/v1alpha2/09-structures.md#table-02-行のkey) |
| 前文 | Preamble、`preamble` | 本則の前に置く前文。項として型付けしない | [PRE-01](../spec/v1alpha2/09-structures.md#pre-01-前文) |
| 制定文 | EnactStatement、`enact-statement` | 「……この政令を制定する。」等の文。Lawの最初の子 | [PRE-02](../spec/v1alpha2/09-structures.md#pre-02-制定文) |
| マーカー | `<!-- loj:… -->` | 項・号・表等の始まりと終わりを示す、文書の直下の単独のHTMLコメント。`loj:`で始まるコメントは予約の候補として検査する | [MD-01](../spec/v1alpha2/03-markdown.md#md-01-構造マーカーの候補)、[DIR-01](../spec/v1alpha2/05-directives.md#dir-01-マーカーの字句) |
| 構造の見出し | — | 分類・条・附則・附属資料を示すATX見出し。Setextや装飾を禁止する | [HEAD-01](../spec/v1alpha2/04-headings.md#head-01-見出しの形)、[HEAD-03](../spec/v1alpha2/04-headings.md#head-03-附則と附属資料のscope) |
| 番号、枝番号 | `number` | 番号の成分は1〜9999。枝番号は`の`・`ノ`で連ねる（第十二条の二） | [NUM-01](../spec/v1alpha2/04-headings.md#num-01-番号) |
| 正規の番号 | `number`（例: `12-2-3`） | 各成分をASCIIの十進にしてハイフンで連ねた形。区切りの字によらず同じ | [NUM-01](../spec/v1alpha2/04-headings.md#num-01-番号) |
| 表示番号、display | `display` | 原文のラベルや番号のtokenをそのまま保持した値。番号の比較には使わない | [DISP-01](../spec/v1alpha2/05-directives.md#disp-01-表示番号)、[HEAD-01](../spec/v1alpha2/04-headings.md#head-01-見出しの形)、[AST-01](../spec/v1alpha2/06-semantic-model.md#ast-01-意味astの形) |
| 未対応の構造 | `unsupportedFeatures` | 本版が型付けしない構造（目次、図、入れ子の表等）。含む入力は申告し、L1は不合格となる | [BASIC-03](../spec/v1alpha2/01-overview.md#basic-03-対象とする構造と収録しないもの) |
| 意味AST | `root` | 版パッケージから導く規範のJSON表現。ノードは`kind`、`id`、`number`、`display`、`content`を持つ | [AST-01](../spec/v1alpha2/06-semantic-model.md#ast-01-意味astの形)、[AST-02](../spec/v1alpha2/06-semantic-model.md#ast-02-意味の検査) |
| ソースの位置 | `{path, start, end}` | 元のファイルのUTF-8のバイト数による半開区間。行・列はその代わりにならない | [SRC-01](../spec/v1alpha2/06-semantic-model.md#src-01-ソースの保持と位置) |
| ノードID（論理ID） | `id`（例: `…/main/article/2/paragraph/1`） | 版の中の位置を示すID。scope・番号・keyから導き、ファイル名や出現順を含めない。条の歴史的同一性を主張しない | [ID-01](../spec/v1alpha2/07-identifiers.md#id-01-idの導出)、[ID-02](../spec/v1alpha2/07-identifiers.md#id-02-idの安定性) |
| 不透明な本文 | — | 意味を型付けせず、原文のまま保持する本文（附属資料の中身等） | [HEAD-03](../spec/v1alpha2/04-headings.md#head-03-附則と附属資料のscope)、[MD-02](../spec/v1alpha2/03-markdown.md#md-02-本文に保持するもの) |
| 字間、組版 | — | 表記の慣行として定まった空白は本文に書き、行の幅に合わせて生じた空白・改行（均等割付等）は組版として書かない | [MD-04](../spec/v1alpha2/03-markdown.md#md-04-字間と改行) |

## 履歴

| 用語 | 表記 | 意味 | 定義 |
|---|---|---|---|
| 関係 | `relations` | Record間の法的な関係。種別は`amends`（改正）、`totallyRevises`（全部改正）、`repeals`（廃止）、`succeeds`（後継）。終点のRecordの履歴マニフェストに置く | [HIST-03](../spec/loj-history/v1alpha1/01-history.md#hist-03-関係と内訳) |
| 関係の起点・終点 | `from`／履歴マニフェストの`record` | 起点は関係を定める側（改正法令等）、終点は関係を受ける側（被改正法令等） | [HIST-03](../spec/loj-history/v1alpha1/01-history.md#hist-03-関係と内訳) |
| 内訳 | `items` | 関係を対象範囲ごとに分けた項目。各項目は`scope`と施行時点`effective`を持つ | [HIST-03](../spec/loj-history/v1alpha1/01-history.md#hist-03-関係と内訳) |
| 改正法令、被改正法令 | — | 改正を定める法令（関係の起点）と、改正される法令（関係の終点） | [HIST-03](../spec/loj-history/v1alpha1/01-history.md#hist-03-関係と内訳)、[BASIC-03](../spec/v1alpha2/01-overview.md#basic-03-対象とする構造と収録しないもの) |
| 起点（Revisionの） | `origin` | `basedOn`を持たないRevision。`enactment`（制定）、`totalRevision`（全部改正による最初の状態）、`coverageStart`（収録の開始） | [HIST-04](../spec/loj-history/v1alpha1/01-history.md#hist-04-起点と基礎状態) |
| 基礎状態 | `basedOn` | 直前の状態のrevision_id。版の順序は施行日の比較ではなくこの参照で表す。分岐を許す | [HIST-04](../spec/loj-history/v1alpha1/01-history.md#hist-04-起点と基礎状態) |
| 成立根拠 | `basis` | Revisionを成立させた関係の`id`と内訳の`id`の組。段階施行では`enactment` | [HIST-05](../spec/loj-history/v1alpha1/01-history.md#hist-05-成立根拠) |
| 段階施行 | `basis: enactment` | 制定時に施行時点が複数ある法令。起点に続くRevisionで表す | [HIST-05](../spec/loj-history/v1alpha1/01-history.md#hist-05-成立根拠) |
| 施行時点 | `effective` | Revisionの施行の時点値。すべてのRevisionが持つ | [HIST-06](../spec/loj-history/v1alpha1/01-history.md#hist-06-版の時間の情報と順序) |
| 適用関係 | `applicability` | 適用の条件の調査結果。`noneConfirmed`（ないことを確認）、`unsurveyed`（未調査）、`conditions`（条件あり） | [HIST-07](../spec/loj-history/v1alpha1/01-history.md#hist-07-適用関係) |
| 経過措置による併存 | — | 新旧の状態が同時に適用される状態。`basedOn`の分岐と適用関係で表す | [HIST-04](../spec/loj-history/v1alpha1/01-history.md#hist-04-起点と基礎状態)、[HIST-07](../spec/loj-history/v1alpha1/01-history.md#hist-07-適用関係) |
| 本文の状態 | `text.status` | `complete`（そろっている）、`partial`（一部欠ける。欠落は`gaps`）、`absent`（本文がない） | [HIST-08](../spec/loj-history/v1alpha1/01-history.md#hist-08-本文の状態) |
| 字体の照合状態 | `text.glyphs` | `verified`（原典の字体と照合した）、`unverified`（照合していない） | [HIST-08](../spec/loj-history/v1alpha1/01-history.md#hist-08-本文の状態)、[GLYPH-10](../spec/loj-glyphs/v1alpha1/01-glyphs.md#glyph-10-照合状態との関係) |
| 収録範囲 | `coverage` | 収録の網羅性の確認状態（`confirmed`／`unconfirmed`）と既知の欠落。Revisionの数を網羅性の根拠にしない | [HIST-11](../spec/loj-history/v1alpha1/01-history.md#hist-11-収録範囲) |
| 効力の終了 | `termination` | `repealed`、`totallyRevised`、`expired`（自身の規定による失効）。登録台帳には写さない | [HIST-12](../spec/loj-history/v1alpha1/01-history.md#hist-12-効力の終了) |
| Revisionの状態 | `status` | `active`、`retracted`（撤回）、`merged`（統合）、`split`（分割）。撤回等をしても削除しない | [HIST-10](../spec/loj-history/v1alpha1/01-history.md#hist-10-revisionの状態) |
| 外部識別子 | `externalIds` | e-Govの法令ID・法令履歴ID等。版を対象とするものは履歴マニフェスト、Recordを対象とするものは登録台帳に置く | [HIST-09](../spec/loj-history/v1alpha1/01-history.md#hist-09-外部識別子)、[REG-05](../spec/loj-registry/v1alpha1/01-registry.md#reg-05-外部識別子) |

## 時点値

| 用語 | 表記 | 意味 | 定義 |
|---|---|---|---|
| 時点値 | TimePoint | 公布・施行・失効等の法的な時点。日付の文字列やnullを直接置かない | [TIME-01](../spec/common/v1alpha1/06-time.md#time-01-時点値の状態)、[CORE-02](../spec/common/v1alpha1/01-overview.md#core-02-ファイルの種類とschemaversion) |
| 時点値の状態 | `state` | `date`（日が確定）、`derived`（規則で計算できる）、`pending`（法令上まだ定まっていない）、`unknown`（調査上不明）、`notApplicable`（該当しない） | [TIME-01](../spec/common/v1alpha1/06-time.md#time-01-時点値の状態) |
| 原表記 | `raw` | 原典の表記（和暦・漢数字等）。正規化した値で置き換えない | [TIME-02](../spec/common/v1alpha1/06-time.md#time-02-date)、[REG-03](../spec/loj-registry/v1alpha1/01-registry.md#reg-03-番号主張) |
| 精度 | `precision` | `date`の値の精度（`day`／`month`／`year`）。日に満たない値は順序の比較に使わない | [TIME-02](../spec/common/v1alpha1/06-time.md#time-02-date) |
| 確定日 | — | 精度が日の`date`、または確定日を計算できる`derived` | [TIME-03](../spec/common/v1alpha1/06-time.md#time-03-derivedとcalc) |
| 計算規則 | `rule`、`base`、`calc` | `derived`の規則の原文、基準の時点、機械が読める計算（`sameDay`、`nextDay`、`afterElapsed`） | [TIME-03](../spec/common/v1alpha1/06-time.md#time-03-derivedとcalc) |
| 委任、確定 | `delegation`、`determinedBy` | `pending`の委任先・条件と、確定させた根拠（施行期日政令等）。確定しても委任の記録を消さない | [TIME-04](../spec/common/v1alpha1/06-time.md#time-04-pendingと確定) |
| sameAs | `sameAs` | 同じ時点を定める他のRecordのRevisionを指す補助。L4の時点の整合で検査する | [TIME-07](../spec/common/v1alpha1/06-time.md#time-07-sameas)、[XREF-03](../spec/common/v1alpha1/10-cross-record.md#xref-03-時点の整合) |

## 根拠と同定

| 用語 | 表記 | 意味 | 定義 |
|---|---|---|---|
| 原典、原典資料 | — | 本文や判断の根拠となる資料。版の本文の字体の根拠は公布された本文（官報と官報正誤） | [GLYPH-07](../spec/loj-glyphs/v1alpha1/01-glyphs.md#glyph-07-字体の根拠とする資料)、[REB-05](../spec/loj-rebuild/v1alpha1/01-rebuild.md#reb-05-原典の入手経路と記録) |
| 官報、御署名原本 | — | 官報は公布された本文。御署名原本は官報を入手できないときに本文を起こせる資料で、字体の照合には使えない | [GLYPH-07](../spec/loj-glyphs/v1alpha1/01-glyphs.md#glyph-07-字体の根拠とする資料)、[REB-05](../spec/loj-rebuild/v1alpha1/01-rebuild.md#reb-05-原典の入手経路と記録) |
| Source | `sources`、`kind` | 出典の資料。種類は`promulgation`、`officialCorrection`、`index`、`egov`、`other`。`fixed`で内容を固定できる | [TYPE-02](../spec/common/v1alpha1/05-types.md#type-02-source) |
| Evidence | `evidence`、`locator` | 主張の出典。Sourceの`id`と、資料の中の箇所の原文表記の組 | [TYPE-03](../spec/common/v1alpha1/05-types.md#type-03-evidence) |
| 確認状態 | Verification、`verification.state` | `unverified`（未確認）、`confirmed`（確認済み）、`disputed`（疑義あり）、`retracted`（撤回） | [TYPE-04](../spec/common/v1alpha1/05-types.md#type-04-verification) |
| 確認済みの主張 | — | `verification.state: confirmed`の主張。箇所付きのEvidenceを一つ以上持つ。出典の内容が裏付けるかは機械で判定しない | [TYPE-05](../spec/common/v1alpha1/05-types.md#type-05-確認済みの主張の根拠) |
| 対象範囲 | Scope、`text`、`nodes` | 関係・条件が及ぶ範囲。`text`は改め文等の原文のまま、`nodes`は同じcommitの版のノードIDの補助 | [TYPE-06](../spec/common/v1alpha1/05-types.md#type-06-scope)、[TYPE-07](../spec/common/v1alpha1/05-types.md#type-07-scopeとノードの照合)、[TYPE-08](../spec/common/v1alpha1/05-types.md#type-08-scopeのノードの記録版) |
| 番号主張 | `numbers` | 法令番号についての、出典付きの主張。`state`（`exists`等）、原表記、構造化した値、`decision`を持つ | [REG-03](../spec/loj-registry/v1alpha1/01-registry.md#reg-03-番号主張) |
| 採否 | `decision` | 番号主張の`adopted`（採用）、`pending`（保留）、`retracted`（撤回）。採用は同時に一つまで | [REG-03](../spec/loj-registry/v1alpha1/01-registry.md#reg-03-番号主張) |
| supersedes | `supersedes` | 訂正後の番号主張から訂正前の主張を指す。訂正前の主張は削除しない | [REG-04](../spec/loj-registry/v1alpha1/01-registry.md#reg-04-訂正と履歴) |
| 同一性 | `identity` | Recordが指す対象の確認。資料・調査の記録と確認状態 | [REG-02](../spec/loj-registry/v1alpha1/01-registry.md#reg-02-recordのファイル) |
| 仮登録 | `status: provisional` | 同一性が未確定の登録。IDはこの段階で発行し、確定しても変えない | [REG-02](../spec/loj-registry/v1alpha1/01-registry.md#reg-02-recordのファイル)、[RID-01](../spec/loj-registry/v1alpha1/02-record-ids.md#rid-01-新しいrecord-idの発行) |
| Recordの状態 | `status` | `provisional`、`active`、`merged`（統合）、`split`（分割）、`withdrawn`（撤回）。登録の状態であり、効力の終了ではない | [REG-02](../spec/loj-registry/v1alpha1/01-registry.md#reg-02-recordのファイル)、[RID-05](../spec/loj-registry/v1alpha1/02-record-ids.md#rid-05-統合分割撤回) |
| 本文の取得状況 | `text.state`（登録台帳） | `collected`（法令リポジトリに本文がある）、`notCollected`（取得していない）、`nonexistentConfirmed`（本文が存在しないことを確認した） | [REG-02](../spec/loj-registry/v1alpha1/01-registry.md#reg-02-recordのファイル) |
| 別名 | `aliases` | 旧リポジトリの以前の名前。参照の解決にだけ使う | [REG-02](../spec/loj-registry/v1alpha1/01-registry.md#reg-02-recordのファイル)、[REB-02](../spec/loj-rebuild/v1alpha1/01-rebuild.md#reb-02-idの維持) |

## 文字

| 用語 | 表記 | 意味 | 定義 |
|---|---|---|---|
| コードポイント列の保持 | — | 原典から選んだ字をUnicodeのコードポイント列のまま保持すること。正規化（NFC等）を正本に適用しない | [CHAR-01](../spec/common/v1alpha1/02-characters.md#char-01-コードポイント列の保持) |
| 統合漢字、CJK互換漢字 | U+F900〜U+FAFF、U+2F800〜U+2FA1F | 互換漢字は正規化で統合漢字に変わるため、特に注意する。本文の互換漢字には字体注記が要る | [CHAR-01](../spec/common/v1alpha1/02-characters.md#char-01-コードポイント列の保持)、[GLYPH-11](../spec/loj-glyphs/v1alpha1/01-glyphs.md#glyph-11-互換漢字と異体字セレクタの注記) |
| 異体字セレクタ、IVS | Variation Selector | 字形を指定する符号。原典に対応して記録したものを保持し、自動で付け外ししない | [CHAR-03](../spec/common/v1alpha1/02-characters.md#char-03-異体字セレクタ)、[GLYPH-06](../spec/loj-glyphs/v1alpha1/01-glyphs.md#glyph-06-コードポイントの選択基準) |
| 踊り字 | 々、〻、ゝ、〳〵等 | 原典に印刷された記号のまま転記し、展開しない | [CHAR-02](../spec/common/v1alpha1/02-characters.md#char-02-字体の自動変換の禁止)、[GLYPH-08](../spec/loj-glyphs/v1alpha1/01-glyphs.md#glyph-08-踊り字) |
| 〓（ゲタ） | U+3013 | 判読困難・符号化不能の字の代わりに本文に置く字。本文の〓にはすべて注記が要る | [GLYPH-03](../spec/loj-glyphs/v1alpha1/01-glyphs.md#glyph-03-本文に置く字)、[GLYPH-02](../spec/loj-glyphs/v1alpha1/01-glyphs.md#glyph-02-注記する場合) |
| 字体注記の種類 | `kind` | `ambiguous`、`illegible`、`unencodable`、`literal`、`spacing`、`variance`、`sourceEdit`、`selected` | [GLYPH-02](../spec/loj-glyphs/v1alpha1/01-glyphs.md#glyph-02-注記する場合) |
| 字の決め方 | `basis`（字体注記） | `ambiguous`の字の選び方。`unifiedDefault`、`otherSource`、`sameSource`、`provisional`、`undetermined` | [GLYPH-05](../spec/loj-glyphs/v1alpha1/01-glyphs.md#glyph-05-注記の内容)、[GLYPH-06](../spec/loj-glyphs/v1alpha1/01-glyphs.md#glyph-06-コードポイントの選択基準) |
| 注記の位置 | `node`、`field`、`offset`、`recorded` | ノードIDと、そのノード自身の本文の中のコードポイント単位の位置で字を指す | [GLYPH-04](../spec/loj-glyphs/v1alpha1/01-glyphs.md#glyph-04-注記の位置) |
| 見え消し | `kind: sourceEdit` | 原典の中で印刷を消して書き直した箇所。訂正後の字句を本文に置く | [GLYPH-09](../spec/loj-glyphs/v1alpha1/01-glyphs.md#glyph-09-原典の中の訂正) |
| 下書きの資料 | — | 本文の下書きに使った機械可読の資料（e-Gov等）。字体を決められないときの仮の字に使う | [GLYPH-06](../spec/loj-glyphs/v1alpha1/01-glyphs.md#glyph-06-コードポイントの選択基準) |
| 派生処理 | — | 新字体への統一、正規化、検索用の統合等、正本とは独立した処理。結果を正本に書き戻さない | [CHAR-05](../spec/common/v1alpha1/02-characters.md#char-05-派生処理の分離) |

## 変更

| 用語 | 表記 | 意味 | 定義 |
|---|---|---|---|
| 変更の種類 | `LoJ-Change` | 正本の各commitが宣言する種類。`format`、`correction`、`officialCorrection`、`restoration`、`metadata`、`revisionAdd`、`revisionFix`、`migration` | [CHG-01](../spec/common/v1alpha1/07-changes.md#chg-01-変更の種類) |
| 書式変更 | `format` | ASTが変わらない表現の変更（書式・マーカー・ファイル分割） | [CHG-01](../spec/common/v1alpha1/07-changes.md#chg-01-変更の種類)、[CHG-02](../spec/common/v1alpha1/07-changes.md#chg-02-種類ごとの検査) |
| 記録訂正 | `correction` | LoJの転記・復元の誤りを原典に照らして直す。Revisionは変わらない | [CHG-01](../spec/common/v1alpha1/07-changes.md#chg-01-変更の種類) |
| 官報正誤 | `officialCorrection` | 官報正誤による公布本文の訂正の反映。法令の改正ではない | [CHG-01](../spec/common/v1alpha1/07-changes.md#chg-01-変更の種類) |
| 復元の進展 | `restoration` | 欠落していた本文を補う | [CHG-01](../spec/common/v1alpha1/07-changes.md#chg-01-変更の種類) |
| 状態の追加、状態の訂正 | `revisionAdd`、`revisionFix` | 新しい改正による版の追加と、状態の取り違えの訂正（撤回・統合・分割）。法令の改正に当たるのは`revisionAdd`だけ | [CHG-01](../spec/common/v1alpha1/07-changes.md#chg-01-変更の種類) |
| 仕様の版の移行 | `migration` | 版パッケージを別のschemaVersionへ変換する | [CHG-01](../spec/common/v1alpha1/07-changes.md#chg-01-変更の種類)、[CHG-02](../spec/common/v1alpha1/07-changes.md#chg-02-種類ごとの検査) |
| 変更検査 | — | 変更前後の二つの記録版を比べ、宣言した種類のとおりかを確かめる検査。適合レベルとは別に報告する | [CHG-02](../spec/common/v1alpha1/07-changes.md#chg-02-種類ごとの検査)、[CHG-05](../spec/common/v1alpha1/07-changes.md#chg-05-適合との関係) |
| trailer | `LoJ-Change`、`LoJ-Revisions` | commitメッセージの末尾に置く種類と対象の版の宣言 | [CHG-03](../spec/common/v1alpha1/07-changes.md#chg-03-種類の宣言) |

## 参照

| 用語 | 表記 | 意味 | 定義 |
|---|---|---|---|
| Record参照 | RecordRef | Recordを登録空間とRecord IDの組で指す。URLでは指さない | [TYPE-01](../spec/common/v1alpha1/05-types.md#type-01-recordref)、[FIXREF-01](../spec/common/v1alpha1/08-references.md#fixref-01-参照の種類と構造化形式) |
| Revision参照 | RevisionRef、`loj:<space>/<record>/<revision>` | 「この法令のこの状態」を指す。記録訂正等で指す内容は変わり得る。ノードを付けられない | [FIXREF-01](../spec/common/v1alpha1/08-references.md#fixref-01-参照の種類と構造化形式)、[FIXREF-05](../spec/common/v1alpha1/08-references.md#fixref-05-revision参照の解決) |
| 固定参照 | FixedRef、`…@<commit>`、`…@<commit>#<node>` | 正本のcommitまで固定した参照。指す記録版は変わらない。ノードを指せるのは固定参照だけ | [FIXREF-01](../spec/common/v1alpha1/08-references.md#fixref-01-参照の種類と構造化形式)、[FIXREF-03](../spec/common/v1alpha1/08-references.md#fixref-03-固定参照の解決)、[FIXREF-07](../spec/common/v1alpha1/08-references.md#fixref-07-ノードの指定) |
| 文字列表記 | `loj:` | データの外で参照を引用する表記。URIスキームの登録を前提にしない | [FIXREF-02](../spec/common/v1alpha1/08-references.md#fixref-02-文字列表記) |
| 解決の結果 | 解決済み、未取得、解決の誤り | 参照を解決した結果。未取得を不存在とみなさない | [FIXREF-06](../spec/common/v1alpha1/08-references.md#fixref-06-解決できない場合) |
| 不存在確認済み | `nonexistentConfirmed` | Record間の参照の結果の一つ。参照先が存在しないことを確認した | [VAL-06](../spec/common/v1alpha1/03-validation.md#val-06-l4の区分)、[XREF-01](../spec/common/v1alpha1/10-cross-record.md#xref-01-関係の解決) |

## 派生ビュー

| 用語 | 表記 | 意味 | 定義 |
|---|---|---|---|
| historyブランチ | `history` | 選択規則で選んだ版を施行日の順にcommitとして積む派生ビューの一例 | [VIEW-01](../spec/common/v1alpha1/09-views.md#view-01-定義と一方向性)、[付録A（参考）](../spec/common/v1alpha1/appendix-a-history-branch.md) |
| 生成器 | — | 正本の記録版から派生ビューを機械的に作るプログラム。同じ入力から同じビューを作る | [VIEW-01](../spec/common/v1alpha1/09-views.md#view-01-定義と一方向性)、[VIEW-03](../spec/common/v1alpha1/09-views.md#view-03-決定性と生成元の記録) |
| 選択規則 | `LoJ-View-Rule` | 版を一本の列に並べるときの明示した規則。除いた版はビューで示す | [VIEW-02](../spec/common/v1alpha1/09-views.md#view-02-選択規則と主張の限界) |
| 索引ファイル | `INDEX.md` | ビューの選択規則、除いた版と理由、ビューに含まれない情報を書くファイル | [VIEW-02](../spec/common/v1alpha1/09-views.md#view-02-選択規則と主張の限界) |
| 版間差分 | — | 二つの版の本文の変化。改正関係（どの改正がどこを改正したか）とは一致しないことがある | [VIEW-05](../spec/common/v1alpha1/09-views.md#view-05-版間差分) |

## 再構築

| 用語 | 表記 | 意味 | 定義 |
|---|---|---|---|
| 再構築 | — | 旧リポジトリのRecordを、原典から履歴マニフェスト・版パッケージ・字体注記へ作り直して移す作業。旧本文は取り込まない | [REB-01](../spec/loj-rebuild/v1alpha1/01-rebuild.md#reb-01-対象と新しい版で書くこと)、[REB-03](../spec/loj-rebuild/v1alpha1/01-rebuild.md#reb-03-本文の出どころ) |
| 凍結 | `legacy.frozenAt` | 旧リポジトリの規定のブランチをその時点で止め、以後pushしないこと。旧commitは到達できるように保つ | [REB-02](../spec/loj-rebuild/v1alpha1/01-rebuild.md#reb-02-idの維持)、[REB-08](../spec/loj-rebuild/v1alpha1/01-rebuild.md#reb-08-既存の参照の維持と旧形式)、[REBR-02](../spec/loj-rebuild/v1alpha1/02-report.md#rebr-02-項目) |
| 資料の確認結果 | `sourceChecks`、`glyphs` | 使った資料が旧字体・異体字を保持しているか。`preserved`、`normalized`、`unknown` | [REBR-03](../spec/loj-rebuild/v1alpha1/02-report.md#rebr-03-資料の確認結果) |
| 旧commitとの対応 | `mappings` | 旧リポジトリの各commitと、対応するRevisionの一覧。対応しないcommitも省略しない | [REBR-04](../spec/loj-rebuild/v1alpha1/02-report.md#rebr-04-旧commitとの対応と未再構築の改正) |
| 未再構築の改正 | `pending`（再構築報告） | 旧リポジトリにあるが、まだ再構築していない改正 | [REBR-04](../spec/loj-rebuild/v1alpha1/02-report.md#rebr-04-旧commitとの対応と未再構築の改正) |
| 原典と旧本文の差 | `differences`、`class` | `wording`（文言）、`structure`（構造）、`omission`（欠落）、`glyph`（字体だけ） | [REBR-05](../spec/loj-rebuild/v1alpha1/02-report.md#rebr-05-原典と旧本文の差) |

## 適合と検査

| 用語 | 表記 | 意味 | 定義 |
|---|---|---|---|
| 要求レベル | MUST、MUST NOT、SHOULD、MAY | 必須、禁止、推奨、任意。示さない文は定義または説明 | [規範仕様の入口](../spec/README.md#要求レベル) |
| 要件ID、系列 | `## <ID> <名前>`、例: `HIST-04` | 要件ごとのID。接頭辞（系列）は一つのディレクトリに属する。版ごとに意味を持つ | [規範仕様の入口](../spec/README.md#要件id) |
| 規則 | `rule` | 診断で報告する要件ID。実装固有の`code`・`message`・`severity`とは区別する | [VAL-07](../spec/common/v1alpha1/03-validation.md#val-07-規則と診断) |
| 診断 | — | 検査器が報告する違反等。規則と、対象のファイルのschemaVersionを示す | [VAL-07](../spec/common/v1alpha1/03-validation.md#val-07-規則と診断) |
| 検査器 | validator | 正本を規範に照らして検査する実装。このリポジトリのCIは検査器ではない | [CONF-03](../spec/common/v1alpha1/04-conformance.md#conf-03-このリポジトリの検査)、[実装ガイド](implementation-guide.md) |
| 適合レベル | L0〜L4 | L0 ファイル形式・Manifest・Markdown構文、L1 法令の構造、L2 法令内の参照（予約）、L3 原典・履歴、L4 他法令との整合。各レベルを独立に判定し、上位の合格から下位の合格を推論しない | [VAL-01](../spec/common/v1alpha1/03-validation.md#val-01-適合レベルの定義)、[VAL-02](../spec/common/v1alpha1/03-validation.md#val-02-独立した判定) |
| 区分 | `category` | L3・L4を分けた検査の単位。L3は`historyStructure`（履歴構造）、`evidence`（根拠）、`sourceMatch`（原典照合）。L4は`relationResolution`（関係の解決）、`relationConsistency`（関係の整合）、`timeConsistency`（時点の整合）、`clauseReference`（条項参照の解決） | [VAL-05](../spec/common/v1alpha1/03-validation.md#val-05-l3の区分と主張)、[VAL-06](../spec/common/v1alpha1/03-validation.md#val-06-l4の区分) |
| 正式、予約 | — | 正式は本版で合格を宣言できるもの。予約は将来の版で定めるもので、合格を主張できない（L2、原典照合、条項参照の解決） | [VAL-01](../spec/common/v1alpha1/03-validation.md#val-01-適合レベルの定義)、[VAL-05](../spec/common/v1alpha1/03-validation.md#val-05-l3の区分と主張)、[VAL-06](../spec/common/v1alpha1/03-validation.md#val-06-l4の区分) |
| 原典照合 | `sourceMatch` | 版の本文と固定した原典資料の一致を確かめるL3の区分。予約 | [SRCM-01](../spec/common/v1alpha1/03-validation.md#srcm-01-l3の原典照合) |
| 結果の値 | 合格、不合格、対象なし、未完了（`pass`、`fail`、`notApplicable`、`incomplete`） | 各レベル・区分の結果。対象なし・未完了を合格とみなさない | [VAL-04](../spec/common/v1alpha1/03-validation.md#val-04-結果の値) |
| 処理不能 | — | 読めない入力、知らないschemaVersion、対応表にない組み合わせ。結果は未完了とする | [VAL-04](../spec/common/v1alpha1/03-validation.md#val-04-結果の値)、[CORE-05](../spec/common/v1alpha1/01-overview.md#core-05-種類ごとの版と対応表) |
| 警告、判定不能、保留 | `warning`、`undetermined`、`pending` | 不合格の診断と区別して報告するもの。警告だけでは不合格にしない | [VAL-04](../spec/common/v1alpha1/03-validation.md#val-04-結果の値)、[HIST-06](../spec/loj-history/v1alpha1/01-history.md#hist-06-版の時間の情報と順序) |
| 適合ケース、適合データ | `conformance/` | 索引を入口とする固定の入力と期待結果。期待結果は規範から人が書き、検査器の出力を写さない | [CONF-01](../spec/common/v1alpha1/04-conformance.md#conf-01-適合ケース) |
| 正例、負例 | `valid/`、`invalid/` | 成功するケースと失敗するケース。負例の期待結果は期待する規則の診断の集合 | [CONF-01](../spec/common/v1alpha1/04-conformance.md#conf-01-適合ケース) |
| 規範のケース、参考のケース | normative、informative | 参考のケースの成否を、正式なレベルの結果に混ぜない | [CONF-01](../spec/common/v1alpha1/04-conformance.md#conf-01-適合ケース)、[CONF-02](../spec/common/v1alpha1/04-conformance.md#conf-02-レベルごとの適合の主張) |
| DDR | Design Decision Record | 設計判断の記録。規範ではないが、判断の理由を引くときに参照する | [設計判断](design-decisions/README.md) |

## 取り違えやすい用語

同じ語や似た語が、別の意味で使われる箇所がある。

| 語 | 区別 |
|---|---|
| 版 | 「版」「Revision」は法令の一つの状態で、「版パッケージ」の「版」もこれに当たる。「仕様の版」はschemaVersion（`loj/v1alpha2`等）。「記録版」は正本のcommitにおける記録の内容。一つのRevisionに、記録訂正のたびに新しい記録版ができる |
| 起点 | Revisionの起点（`origin`。`basedOn`を持たない最初の状態）と、関係の起点（`from`。改正法令等の関係を定める側）は別の概念である |
| 記録訂正と官報正誤 | 記録訂正（`correction`）はLoJの記録の誤りを直す。官報正誤（`officialCorrection`）は公布された本文の訂正を反映する。どちらも法令の改正ではなく、新しいRevisionを作らない |
| Revision参照と固定参照 | Revision参照は正本ブランチの最新の記録版に解決し、指す内容が変わり得る。固定参照は指定のcommitの記録版に解決し、変わらない。ノードを指せるのは固定参照だけ |
| ノードIDと条の同一性 | ノードIDは番号から作る版の中の位置であり、「同じ条」であることを主張しない。番号の訂正や繰上げで、同じIDが別の規定を指すことがある |
| 撤回 | 関係・Revision・番号主張・確認状態の`retracted`は撤回。登録台帳のRecordの撤回は`withdrawn` |
| 登録台帳の状態と効力の終了 | 登録台帳の`status`は登録の状態。廃止・失効は履歴マニフェストの`termination`で表し、登録台帳には写さない |
| `pending` | 時点値では「法令上まだ定まっていない」。番号主張の`decision`では「保留」。再構築報告では「未再構築の改正」。診断の`class`では「保留」 |
| `unknown` | 時点値では「調査上不明」。番号主張の`state`、`basedOn`、資料の確認結果（`sourceChecks.glyphs`）でもそれぞれ「不明」を表す。いずれも推測で値を補わない |
| `glyphs` | 履歴マニフェストの`text.glyphs`は字体の照合状態。`text.glyphNotes`は字体注記のファイルのパス。再構築報告の`sourceChecks.glyphs`は資料が字体を保持しているか。番号主張の`glyphs`は`raw`の字体注記 |
| `basis` | Revisionの`basis`は成立根拠（関係と内訳）。字体注記の`basis`は曖昧な字の決め方 |
| `text` | 版パッケージのASTの`text`は本文。履歴マニフェストの`text`は本文の状態。登録台帳の`text`は本文の取得状況。Scopeの`text`は対象範囲の原文 |
| 未取得と不存在 | 未取得（`notFetched`）はリポジトリ・commit・Recordを取得できなかったこと。不存在確認済み（`nonexistentConfirmed`）は存在しないことを確かめたこと。未取得を不存在とみなさない。登録台帳の`notCollected`（本文を取得していない）からも本文の不存在を推論しない |
| 未完了、判定不能、処理不能 | 未完了はレベル・区分の結果の値。判定不能は個々の検査の結論が出ないこと（警告・保留と同じく不合格と区別する）。処理不能は入力を扱えないことで、結果は未完了になる |
| 確認状態と適合 | `verification.state: confirmed`は主張の出典を記録したことであり、L3の合格は判断の正しさを保証しない |
| 適合レベルの外の検査 | 変更検査、登録台帳の検査、再構築報告の検査、自身のRecordへの参照の解決は、L0〜L4とは別に報告する |
| ラベル | 可読ラベル・`label`は表示用であり、参照の解決・同一性・順序の決定に使わない |
