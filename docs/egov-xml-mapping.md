# e-Gov法令標準XMLとの対応（参考）

[公式v3 XSD](https://laws.e-gov.go.jp/file/XMLSchemaForJapaneseLaw_v3.xsd)と
[要素解説](https://laws.e-gov.go.jp/docs/law-data-basic/419a603-xml-schema-for-japanese-law/)を参照した概念の対応である。
変換器や可逆変換の保証ではない。LoJは独立したモデルであり、XMLの要素の順序・すべての属性を再現しない。

e-Govの本文は新字体に置き換えている。版の本文の根拠は公布された本文（官報と官報正誤）であり、e-Govの本文をそのまま版の本文にしない（[GLYPH-07](../spec/loj-glyphs/v1alpha1/01-glyphs.md)、[REB-05](../spec/loj-rebuild/v1alpha1/01-rebuild.md)）。e-Govは、構造の確認と字体の仮置きの手がかりとして使う。

## 版パッケージ（loj/v1alpha2）

| XML | loj/v1alpha2 | 範囲・損失の管理 |
|---|---|---|
| Law / LawNum / LawTitle | `law.yaml`と`Law` | 番号・題名・種別は版ごとに`law.yaml`へ。番号主張の構造化は登録台帳（REG-03） |
| LawBody | `Law`の内容 | 独立したノードを作らない |
| EnactStatement | `EnactStatement` | PRE-02。`Law`の最初の子 |
| Preamble | `Preamble` | PRE-01。`MainProvision`の前 |
| TOC | `Toc` | TOC-01。中身は不透明な本文で、TOCLabel・TOCChapter等の構造を型付けしない。`EnactStatement`の後、`Preamble`の前 |
| MainProvision | `MainProvision` | 条を含む構造だけ。条を持たない本則は未対応 |
| Part / Chapter / Section / Subsection / Division | `Part` / `Chapter` / `Section` / `Subsection` / `Division` | 編・章・節・款・目 |
| Article / ArticleTitle / ArticleCaption | `Article`と表示 | 番号と見出し。見出しの括弧書きを含む（HEAD-01）。削除条を含む |
| Paragraph / ParagraphNum | `Paragraph` | 番号のある項は`numbering: explicit`。ParagraphNumが空の項は`implicit`（PARA-01） |
| ParagraphCaption | `caption=present`と見出しの行、Paragraphの`caption` | 項の本文の最初の行に、括弧を含めて書く（PARA-02）。一つの見出しが続く項にかかる場合も、最初の項にだけ書く |
| Item / ItemTitle | `Item` | 表示番号の範囲はDISP-01 |
| Subitem1〜Subitem10 | `Subitem`（level 1〜10） | 表示はASCIIの十進、いろは、括弧付きの十進（DISP-01）。ローマ数字等は未対応 |
| Sentence等の本文 | `text` | 原文のMarkdown。文・列の型は再現しない |
| TableStruct / Table / TableRow / TableColumn | `Table` / `Row` / `Cell` | 項・号・細分の本文の中の表（TABLE-01〜03）。罫線・配置・列の幅は記録しない。罫線を省いて上の欄が続く空の`TableColumn`は、上の欄の結合（`rowspan`）として書く（原典で確かめる）。罫線に囲まれた空の欄、セルの中の項・号・表、入れ子の表は未対応 |
| SupplProvision | `SupplementaryProvision` | `law.yaml`の永続key。その法令自身の附則だけを収録する |
| SupplProvision（`AmendLawNum`を持つ改正法の附則） | 収録しない | 改正法のRecordに属する（BASIC-03）。施行時点は履歴マニフェストの関係（`relations`）に記録する |
| AppdxTable / AppdxNote / AppdxStyle / Appdx / AppdxFig / AppdxFormat | `AppendedMaterial` | 不透明な本文だけ。表のセル、図・様式の構造は未対応 |
| SupplProvisionAppdx系 | 未対応 | 附則の中の附属資料としての関係は保持できない |
| Ruby / Sup / Sub / Fig / ArithFormula / AmendProvision | 未対応 | 型付きの意味表現と往復の検査が必要 |

## 履歴と識別子

| e-Gov | LoJ | 備考 |
|---|---|---|
| 法令ID（例: `323AC1000000178`） | 登録台帳の外部識別子（REG-05） | Record IDの代わりに使わない |
| 法令履歴ID | 履歴マニフェストのRevisionの外部識別子（HIST-09） | revision_idの代わりに使わない。対応なし・複数の候補を許す |
| 改正法令の施行日 | 関係の内訳の時点値（TIME） | 原典で確かめた値を記録する。e-Govの値だけを根拠に確認済みにしない |

## 移行の注意

- XMLから起こす場合は、未対応の要素・属性を一覧にし、`unsupportedFeatures`に記録する。
- 入力のXMLを別に保存し、削除・圧縮で失われる情報を隠さない。LoJのL1の合格は、XMLの情報の保全を証明しない。
- XMLで許される構造を、LoJがすべて許すわけではない。

`loj/v1alpha1`との対応は、本書のGitの履歴にある。
