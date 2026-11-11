# HTMLコメントのマーカー

## DIR-01 マーカーの字句

- [マーカーの文法](../../grammar/v1alpha2/directives.ebnf)の開始・終了のマーカーを、単独の行で使わなければならない（MUST）。
- 次のマーカーだけを認める。名前は小文字とする。

  | マーカー | 必須の属性 | 任意の属性 | 要件 |
  |---|---|---|---|
  | `paragraph` | `number` | `numbering`（`explicit`／`implicit`） | [PARA-01](09-structures.md) |
  | `item` | `number` | — | |
  | `subitem` | `level`、`number` | — | |
  | `table` | `number` | — | [TABLE-01](09-structures.md) |
  | `row` | `key` | — | [TABLE-02](09-structures.md) |
  | `cell` | — | `rowspan`、`colspan` | [TABLE-03](09-structures.md) |
  | `enact-statement` | — | — | [PRE-02](09-structures.md) |
  | `preamble` | — | — | [PRE-01](09-structures.md) |

- `<!--`の直後と`-->`の直前、マーカーの名前と最初の属性の間、属性の間には、ASCII空白をちょうど1個置く。タブ、改行、引用符、2個以上の連続した空白、末尾の空白を禁止する。属性のないマーカー（`<!-- loj:cell -->`等）は、名前の後に`-->`の直前の空白1個だけを置く。属性の順は任意とする。
- 未知の属性、属性の重複・欠落、未知のマーカーは違反とする。終了のマーカーは属性を持たない。

```markdown
<!-- loj:paragraph number=1 -->
本文
<!-- loj:item number=1 -->
一　号の本文
<!-- loj:subitem level=1 number=1 -->
1　細分の本文
<!-- loj:end-subitem -->
<!-- loj:end-item -->
<!-- loj:end-paragraph -->
```

## DIR-02 対応・入れ子・空の禁止

- すべての開始のマーカーは、同じファイルの中に、明示的に対応する終了のマーカーを持たなければならない（MUST）。最も内側を、同じ種類の終了で閉じる。省略、交差、余分な終了、見出しやEOFを越える未閉鎖は違反とする。
- 親は次のとおりでなければならない（MUST）。

  | マーカー | 親 |
  |---|---|
  | `paragraph` | Article、または直接の項の形式のSupplementaryProvision |
  | `item` | Paragraph |
  | `subitem` | `level=1`はItem、`level=n`は`level=n-1`のSubitem（`level`は1〜10、飛び越し不可） |
  | `table` | Paragraph、Item、Subitem |
  | `row` | Table |
  | `cell` | Row |
  | `enact-statement`、`preamble` | なし（文書の直下。位置は[PRE-01](09-structures.md)・[PRE-02](09-structures.md)） |

- 兄弟の同じ種類・同じlevelの`number`は一意とする。
- Paragraph、Item、Subitem、Cell、Preamble、EnactStatementは、子を除く自身の本文に、空白以外の文字を持たなければならない（MUST）。コメントだけでも空でない原文となるが、法的な内容の有無は判定しない。
- Tableは1つ以上のRowを、Rowは1つ以上のCellを持たなければならない（MUST）。TableとRowの直下に、空白だけの行以外の本文を置いてはならない（MUST NOT）。

## DISP-01 表示番号

- 表示番号は、本文の最初の空でない行の先頭のtoken（ASCII空白または全角空白で終わる）で検査する。
- 表示番号の字種は、種類ごとに次のとおりとする。本文の枝番号は`の`または`ノ`で区切る。

  | 種類 | 許す字種 |
  |---|---|
  | paragraph | ASCIIの十進、全角の十進 |
  | item | NUM-01の漢数字、ASCIIの十進 |
  | subitem | ASCIIの十進 |

- 一つの表示番号のすべての成分は、同じ字種でなければならない（MUST。NUM-01）。例えば、itemの`二の2`、paragraphの`2の２`は違反とする。
- 表示番号の正規化した値は、`number`と等しくなければならない（MUST）。
- `paragraph number=1`だけは番号を省略できる。それ以外には表示番号が必要である。番号に続く同じ行に、空でない本文を置く。
- 番号を含む全文を`text`に残し、検出したtokenを`display`に保存する。表示のない第1項の`display`は空文字列とする。
- 第1項でも、認識できる数字のtokenで始まれば検査する。番号を意図しない数字で紛らわしい場合は、原典の確認を要し、自動で修正しない。
- 原典で番号のない第1項の本文が、数字のtoken（例: 「２　…」）で始まる場合は、本版では表せない。`numbering=implicit`は項が一つの親や、ほかの項に番号がある親では使えない（PARA-01）。未対応の構造として`unsupportedFeatures`に申告する（BASIC-03）。
- `numbering=implicit`の項には表示番号を置かない。検査を行わず、`display`は空文字列とする（[PARA-01](09-structures.md)）。
- Table、Row、Cell、Preamble、EnactStatementの`display`は空文字列とする。
- いろは・括弧・ローマ数字等の細分の表示は未対応である。勝手に十進へ転記せず、`unsupportedFeatures`に申告する。
