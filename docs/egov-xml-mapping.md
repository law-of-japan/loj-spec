# e-Gov法令標準XMLとの対応（参考）

[公式v3 XSD](https://laws.e-gov.go.jp/file/XMLSchemaForJapaneseLaw_v3.xsd)と
[要素解説](https://laws.e-gov.go.jp/docs/law-data-basic/419a603-xml-schema-for-japanese-law/)を参照した概念対応。
変換器・可逆変換の保証ではない。lojは独立モデルであり、XMLの要素順・全属性を再現しない。

| XML | loj/v1alpha1 | 範囲・損失管理 |
|---|---|---|
| Law / LawNum / LawTitle | lawとLaw | 番号・名称・言語・日付。元号等の属性分解は将来 |
| LawBody | Law.content | 独立ノードを作らない |
| MainProvision | MainProvision | 条を含む構造のみ |
| Part | Part | 編 |
| Chapter | Chapter | 章 |
| Section | Section | 節 |
| Subsection | Subsection | 款 |
| Division | Division | 目 |
| Article / ArticleTitle / ArticleCaption | Article / display | 番号と見出し。削除条を限定対応 |
| Paragraph / ParagraphNum | Paragraph | 第一項も明示 |
| Item / ItemTitle | Item | 本版の表示番号範囲のみ |
| Subitem1〜Subitem10 | Subitem(level=1〜10) | 階層対応。いろは等の表記は未対応 |
| Sentence等の本文 | text | 原文Markdown。文・列の型は再現しない |
| SupplProvision | SupplementaryProvision | Manifestの永続key。改正属性・施行条件は将来 |
| AppdxTable / AppdxNote / AppdxStyle / Appdx / AppdxFig / AppdxFormat | AppendedMaterial | 不透明本文のみ。原XML型、表セル、図・様式の構造は未対応 |
| SupplProvisionAppdx系 | 未対応 | 附則内の附属資料としての意味関係は保持できない |
| Preamble / EnactStatement / TOC | 未対応 | 本文へ押し込んで完全移行と扱わない |
| Ruby / Sup / Sub / Table / Fig / ArithFormula / AmendProvision | 将来 | 専用の型付き意味表現と往復テストが必要 |

XML→loj移行時は、未対応の属性・要素を一覧化してunsupportedFeaturesへ申告する。
入力XMLを別途保存し、削除・圧縮によって失われる情報を隠さない。lojのL1成功はXMLの情報保全を証明しない。
XMLで許される本則の直接項や混合構造を、lojがすべて許すわけではない。
往復対応を追加する場合は、型別fixtureと情報損失レポートを次版の条件にする。
