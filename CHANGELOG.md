# 変更履歴

見出しの「草案」は、[草案の版](spec/README.md#版の状態)への変更であることを示す。版の状態の正は、[規範仕様の入口](spec/README.md#規範とするもの)の表にある。版を公開したときは、公開の日付の項目を加える。

## 字体注記の記録先と、互換漢字の範囲（2026-11-12、草案）

[law-of-japan/loj-spec#21](https://github.com/law-of-japan/loj-spec/issues/21)の修正である。草案の版への変更であり、版番号は上げない。

- HIST-08: Revisionの`text`に、任意の`variances`（原典資料の間の文言の食い違い）と`correctionsSurveyed`（官報正誤を確かめたか）を加えた。確認の状況を`sources`の`locator`に書くことを禁じた。GLYPH-07とREB-05の記録先を、これらに改めた。
- GLYPH-04・05: `law.number`の字体は注記しないとした。字体注記に`ivd`を加え、異体字セレクタを含む注記で必須とした。`variance`で`candidates`を必須とし、本文に置いた字と置かなかった字を書くとした。
- TYPE-02: Sourceに任意の`glyphPreservation`を加えた。GLYPH-10: `text.glyphs: verified`のRevisionは、`glyphPreservation: preserved`のSourceを指すとした。REBR-03の`sourceChecks`を確認の記録とした。
- GLYPH-06・GLYPH-11・VAL-08: 互換漢字の範囲を、正規分解を持つ字に限った（12字を除く）。Unicodeの版を15.1に固定した。
- 共通の型、履歴マニフェスト、字体注記のschemaを更新した。
- 正例hist-001の資料に`glyphPreservation`を加え、確認の状況を`locator`から`correctionsSurveyed`に移した（hist-001を写したケースも同じ行が変わる。期待結果は変わらない）。適合ケースglyph-010（注記のないU+FA11）とglyph-011（字体を保持する資料を指さない`verified`）を加えた。
- DDR-021、用語集、要件との対応表を更新した。

## 変更の種類の範囲、登録台帳の変更、正本ブランチの統合の方法（2026-11-12、草案）

[law-of-japan/loj-spec#18](https://github.com/law-of-japan/loj-spec/issues/18)と[law-of-japan/loj-spec#33](https://github.com/law-of-japan/loj-spec/issues/33)の修正である。草案の版への変更であり、版番号は上げない。

- CHG-02: `correction`・`officialCorrection`・`restoration`・`revisionAdd`の変更してよい範囲に、従属して更新するファイル（字体注記、Scopeの`nodes`、`text.sources`・`text.glyphs`、根拠、再構築報告の対応等）を加えた。従属する更新は別の種類として分けない。
- CHG-01・CHG-02: 登録台帳の変更を`metadata`に含め、検査にRID-05（IDの再利用の禁止）を適用した。`migration`は、ASTの対応表を提供する版の組に限るとし、v1alpha1からv1alpha2への移行で宣言することを禁じた。
- CHG-03: 正本ブランチへの統合をsquash・rebaseに限り、mergeのcommitを禁じた。法令リポジトリの最初のcommitを`revisionAdd`とした。revertを意味の上の取り消しと定め、取り消す変更と同じ種類とした。`revisionAdd`の取り消しは`revisionFix`（撤回）とし、Revisionを削除しない。変更検査は各commitをその親と比べるとした。従属して更新できるのは宣言した版の部分に限るとした。
- FIXREF-04: 正本ブランチのオブジェクト形式の変更を禁じた。作業ブランチのcommitが統合後に到達できないことを書いた。
- 適合ケースcommon-024（記録訂正で同じ版の本文の出典を併せて更新する）を加えた。既存の`git bundle`は変えていない。
- DDR-015・019、制限（commitの日時、複数のリポジトリにまたがる変更、オブジェクト形式）、要件との対応表を更新した。

## L4の関係の整合と不存在確認済み、他のRecordへの固定参照（2026-11-12、草案）

[law-of-japan/loj-spec#16](https://github.com/law-of-japan/loj-spec/issues/16)の修正である。草案の版への変更であり、版番号は上げない。

- XREF-02: 比べる記録のなかった「成立根拠が参照する関係と登録台帳・起点の記録」の比較を、全部改正後のRecordの`totallyRevises`が指す関係の対応（存在、種類、状態、起点）に改めた。対象範囲の比較を削った。VAL-06の表の説明を合わせた。
- XREF-01: 不存在確認済みのRecordを登録台帳の`status: withdrawn`とし、確定した関係を`status: active`かつ`verification.state: confirmed`の関係と定めた。登録台帳にないIDは未取得とした。REG-02に`withdrawn`の意味を書いた。
- FIXREF-06・VAL-07: 他のRecordへの参照の解決を、L4ではなく参照の解決の検査（適合レベルの外）で扱うとした。`sameAs`はXREF-03のままとした。
- 適合ケースcommon-017（全部改正の対応）、common-018（存在しない関係を指す`totallyRevises`）、common-019（確定した関係の起点が`withdrawn`のRecord）、common-020〜022（撤回した関係、全部改正でない関係、起点が別のRecordの関係を指す`totallyRevises`）、common-023（未確認の関係の起点が`withdrawn`のRecord。違反にしない）を加えた。
- DDR-016、用語集、要件との対応表を更新した。

## 検査の結果の決め方と、L1が不合格の版のL3根拠（2026-11-12、草案）

[law-of-japan/loj-spec#15](https://github.com/law-of-japan/loj-spec/issues/15)と[law-of-japan/loj-spec#24](https://github.com/law-of-japan/loj-spec/issues/24)の修正である。草案の版への変更であり、版番号は上げない。

- VAL-04: 区分の結果の決め方の表を置いた（違反→不合格、判定不能→未完了、警告・保留だけ→合格）。警告しか出さない検査（HIST-06の順序）の判定不能は数えない。知らないschemaVersion（知っている種類の知らない版を含む）を処理不能として未完了とし、理由をschemaVersionの規則の診断で示すと定めた。BASIC-01・HIST-01・GLYPH-01・REG-01・REBR-01から引いた。
- HIST-06: 順序の比較を、両方が確定日の場合とした。収録開始の起点の、確定日でない施行時点とは比べないとした。
- CONF-01と版パッケージの検査の章: 負例では、期待結果に挙げたすべての規則の診断を含める、に揃えた。期待結果には必ず出るべき規則だけを挙げる。
- VAL-05: 区分の結果をRecordにつき一つとした。VAL-06: 未取得を判定不能として表で扱うとした。
- VAL-07: MD系列をL1とし、L0の「CommonMarkの構文解析」を削った。診断のschemaVersionを規則を定める版のもの（共通の要件は`common/<版>`）とし、共通の型の規則の違反を、その型を使うファイルの検査で報告すると定めた。報告のschemaで`target`（`repository`、`commit`）を必須にした（VAL-03）。
- TYPE-07: L1が不合格の版の`nodes`は判定不能とした。GLYPH-11も判定不能として表で未完了にする形に揃えた。
- pkg-058・124の期待結果に、L0の`incomplete`を加えた。適合ケースhist-029（L1が不合格の版のScopeのノード）とhist-030（版に存在しないScopeのノード）を加えた。
- DDR-016、用語集、制限、要件との対応表を更新した。

## 法令番号・公布日の表示用の値と、公布の時点・遡及の根拠（2026-11-12、草案）

[law-of-japan/loj-spec#13](https://github.com/law-of-japan/loj-spec/issues/13)と[law-of-japan/loj-spec#19](https://github.com/law-of-japan/loj-spec/issues/19)の修正である。草案の版への変更であり、版番号は上げない。

- CORE-02に、版パッケージの`law.number`・`law.promulgatedAt`を表示用の値とする例外を書いた。根拠・順序・同定に使わない。正は、登録台帳の採用中の番号主張と、関係の`promulgated`とした。
- MAN-01: `number`と`promulgatedAt`の`null`を「表示する値を持たない」とし、判読できない字を〓とした。REG-03に、採用中の番号主張が法令番号の正であることを書いた。
- HIST-03: 関係に任意の`promulgated`（公布の時点）、内訳に任意の`retroactive`（遡及の根拠）を加えた。HIST-05は、改正法の公布の時点を関係から得るとした。HIST-06の順序の警告の根拠を、これらのフィールドで定めた。
- L4に区分「表示の整合」（`displayConsistency`）とXREF-05（`law.number`と採用中の番号主張。食い違いは警告）を加えた。XREF-06（同じ起点の関係の公布の時点。食い違いは違反）を「時点の整合」に加えた。
- 履歴マニフェストのschema、適合ケースの索引・期待結果・報告のschemaの区分、Manifestのschemaの説明を更新した。
- 正例hist-001・hist-016の関係に`promulgated`を加えた（hist-001を写した負例も同じ行が増える）。適合ケースhist-027（遡及の根拠のない公布より前の施行の警告）、hist-028（遡及の根拠あり）、common-013・014（表示の整合の合格と警告）、common-015・016（公布の時点の一致と食い違い）を加えた。
- DDR-012・016・017と用語集を更新した。

## 版パッケージの表示番号・マーカーの空白・セルの結合・附則のtitle（2026-11-11、草案）

[law-of-japan/loj-spec#25](https://github.com/law-of-japan/loj-spec/issues/25)の修正である。草案の版への変更であり、版番号は上げない。

- DISP-01: 表示番号の字種を種類ごとの表にした。番号のない第1項が数字で始まる場合は、未対応として`unsupportedFeatures`に申告すると定めた。
- NUM-01: 一つの番号のすべての成分を同じ字種とした（成分の中の幅の混在と、成分の間の字種の混在を禁止）。
- DIR-01とEBNF: マーカーの空白を、どの位置もちょうど1個とした。属性のない`cell`のマーカーが2個の空白を受け付けないようにした。
- 意味ASTのschema: Cellの`rowspan`・`colspan`の最小を2とした（TABLE-03に合わせた）。
- MAN-01: `supplements[].title`を、検査しない表示用の名前と定めた。
- 負例pkg-125〜128（属性の間の二つの空白、属性のないセルのマーカーの二つの空白、号の全角の表示番号、条の番号の字種の混在）を加えた。DDR-012に追記した。

## 旧データの値の記録（2026-11-11、草案）

[law-of-japan/loj-spec#22](https://github.com/law-of-japan/loj-spec/issues/22)の修正である。草案の版への変更であり、版番号は上げない。

- REB-06の「旧データの値をやむを得ず記録する場合」を削り、原典で確かめられない値は確かめていないことを記録し、旧データの値は確認状態の理由にだけ手がかりとして書くと改めた。値の欄と根拠に旧データの値を置くことを禁じた。
- 原典で確かめられない旧`number`（`null`を含む）を、番号主張の`state: unknown`・`verification.state: unverified`で記録すると定めた。旧`null`を`nonexistent`に読み替えることの禁止は残した。
- 移行の手順（参考）とDDR-020を合わせた。`law.yaml`の`number: null`の意味は#13で扱う。

## 履歴マニフェストの本文のパスと成立根拠（2026-11-11、草案）

[law-of-japan/loj-spec#20](https://github.com/law-of-japan/loj-spec/issues/20)の修正である。草案の版への変更であり、版番号は上げない。

- HIST-08: `text.package`と`text.glyphNotes`は、書く場合は自身のrevision_idの既定のパス（`versions/<revision_id>/law.yaml`、`versions/<revision_id>/glyphs.yaml`）とした。ディレクトリとの一対一を、`complete`・`partial`のRevisionに限った。GLYPH-01に字体注記のファイル名`glyphs.yaml`を書いた。
- HIST-05: `basis`を項目一つの配列とし、起点は`basis`を持たないとした。同じ関係・同じ施行時点の重複を、有効なRevisionの確定日どうしで比べると定めた。有効なRevisionの`basis`が、撤回した関係・内訳を参照することを禁じた。
- HIST-04: 有効なRevisionの`basedOn`が、撤回・統合・分割したRevisionを参照することを禁じ、付け替え先を定めた。
- FIXREF-03: `path`の照合先に、`text.package`を省略したときの既定のパスを書いた。
- 履歴マニフェストのschemaで、パスの形、`basis`の項目の数、起点の`basis`の禁止を検査するようにした。
- 負例hist-023〜026（既定と違うパス、撤回したRevisionを基礎状態とする版、撤回した関係を成立根拠とする版、成立根拠を持つ起点）を加えた。DDR-017に追記した。

## 固定参照の構造化形式（2026-11-11、草案）

[law-of-japan/loj-spec#17](https://github.com/law-of-japan/loj-spec/issues/17)の修正である。草案の版への変更であり、版番号は上げない。

- 共通の型のschemaに、RevisionRef、FixedRef、commitHashを定義した。`sameAs`はRevisionRefとした（形は変わらない）。
- Sourceの`fixed`を、FixedRefのmapping、またはLoJの外の資料を固定する記述の文字列とした（TYPE-02）。`loj:`で始まる文字列を拒否する。
- FIXREF-02に、Record参照の文字列表記`loj:<space>/<record>`を加えた。変換で落とさないものを参照の同一性のフィールドに限り、省略した`space`の補い方を定めた。
- 期待結果の参照の`target`を文字列表記で書くと定め（CONF-01）、期待結果のschemaに書式を加えた。common-001・003の`target`を`loj:loj/…`に書き直した。
- FIXREF-04で、commitのハッシュを小文字の16進数に限った（大文字を含むものは不合格）。
- 適合ケースhist-019（固定参照と外部の資料の固定、架空）と、負例hist-020〜022（短縮したcommit: FIXREF-04、`revision`のない固定参照: FIXREF-03、LoJの中の資料の文字列での固定: TYPE-02）を加えた。
- DDR-019、用語集、制限、要件との対応表を更新した。

## 確定日の定義（2026-11-11、草案）

[law-of-japan/loj-spec#14](https://github.com/law-of-japan/loj-spec/issues/14)の修正である。草案の版への変更であり、版番号は上げない。

- TIME-03に、確定日の定義（精度が日の`date`、または`base`が確定日である`derived`）を置いた。`base`が確定日なら`value`を必須とし、確定日でないなら`value`を禁じた。`base`が`date`でない場合を一律に禁じていた文を、`base`が確定日でない`derived`を順序の比較に使うことの禁止に改めた。
- TIME-02から確定日の定義を引き、TIME-01の`derived`の説明を、確定日を前提としない文に改めた。
- 共通の型のschemaで、`derived`の`value`を`YYYY-MM-DD`に限った。
- 適合ケースhist-016（`derived`を基準とする`derived`、架空）とhist-017（精度が月の`date`を基準として`value`を書いた負例）、hist-018（確定日の基準から計算した`value`の書き漏らし）を加えた。まだないケースを`docs/coverage.md`に書いた。
- DDR-014に「確定日の定義」を加えた。用語集の「確定日」を改めた。

## 互換漢字の例の訂正（2026-11-11、草案）

[law-of-japan/loj-spec#12](https://github.com/law-of-japan/loj-spec/issues/12)の訂正である。規範の意味は変えていない。

- CHAR-01、CHAR-02、GLYPH-06の2で「神 U+FA19」と書いた箇所の字が、統合漢字（U+795E）に変わっていた。U+FA19に直した。
- `scripts/verify.py`に、「字（U+XXXX）」「字 U+XXXX」の形で字とコードポイントを並べた箇所について、字のコードポイントが表記と一致することの検査を加えた。対象は、ルートの文書、`spec/`、`docs/`（`docs/archive/`を除く）である。範囲の表記と、語の末尾の字（「空白（U+3000）」の「白」）は対象にしない。
- `docs/archive/`の統合案にも同じ現象が残っているが、内容を変えない文書なので直していない。

## 版の状態と公開（2026-11-11、草案）

[law-of-japan/loj-spec#28](https://github.com/law-of-japan/loj-spec/issues/28)の結論に基づく。

- 版の状態（草案・公開・凍結）を、規範仕様の入口（`spec/README.md`）に定めた。「規範とするもの」の表に「状態」の列を加え、この表と「凍結した版」の表を状態の正とした。
- 公開を、表の状態を「公開」とした変更が`main`に入った時点と定めた。公開したcommitには、schemaVersionと同じ名前のタグを打つ（共通の型は`common/<版>`）。
- 意味を変える修正を、いずれかの入力について、適合の結果・診断の規則・ASTのいずれかが変わる修正と定めた。schemaの`description`と`$comment`、参考の付録、`docs/`、`examples/`の変更は、これらを変えない限り、意味を変えない。
- `spec/`の下でMarkdownを置くディレクトリを、規範仕様の入口の二つの表のディレクトリだけとした。
- 組1の6つ（`loj/v1alpha2`、4種類と共通の型の`v1alpha1`）を草案とした。草案は、版番号を上げずに意味を変えてよい。
- CORE-04から、版の状態の定義を引いた。
- DDR-023を加え、DDR-010から参照した。用語集に「版の状態」「草案の版」「公開した版」「意味を変える」を加えた。
- CONTRIBUTINGに、状態ごとの変えてよい範囲と、公開の手順を加えた。AGENTS.mdを合わせた。
- `scripts/verify.py`に、状態の表の検査（状態の値、`spec/`のディレクトリとの一致）を加えた。
- この変更履歴の見出しの「未公開」を、草案の版への変更の項目では「草案」に改め、版と関係のない項目からは外した。

## エージェント向けの手引き（2026-11-10）

- AIエージェント向けの手引き[AGENTS.md](AGENTS.md)（規範ではない）を加えた。構成、検査、変えてはならないもの、適合ケースの扱いをまとめ、規則の正はCONTRIBUTINGと規範仕様の入口に置いた。CONTRIBUTINGからリンクした。
- `scripts/verify.py`のリンクと要件IDの見出しの検査の対象に、AGENTS.mdを加えた。

## 用語集（2026-11-09）

- 本仕様に固有の用語を、定める要件へのリンクとともに一覧にした[用語集](docs/glossary.md)（参考）を加えた。取り違えやすい用語の区別も載せた。READMEと規範仕様の入口からリンクし、CONTRIBUTINGに更新の規則を加えた。

## 文書の整理（2026-11-09）

- 役目を終えた文書（統合案、v1alpha1の作成時の報告・調査・検査の記録）を`docs/archive/`に移し、冒頭に状態を書いた。統合案の要件IDの見出しには「案」を付けた。内容は変えていない。
- `scripts/verify.py`に、`spec/`から`docs/archive/`へのリンク、`docs/archive/`の文書の状態の行、`spec/`の外の要件IDの見出しの検査を加えた。

## 次期仕様 — loj/v1alpha2と新しい4種類（2026-11-09、草案）

[統合案](docs/archive/next-spec-integration.md)の決定に基づく。

- 規範仕様の入口（`spec/README.md`）を加えた。要件IDの付け方、組み合わせて使える版の対応表、凍結した版を定める。
- 種類にまたがる要件を`spec/common/v1alpha1`に置いた（構成、文字、適合レベル、共通の型、時点値、変更の種類、固定参照、派生ビュー、Record間の検査）。
- 版パッケージ`loj/v1alpha2`を加えた。無番号の項、項・号・細分の本文の中の表、前文と制定文を型付けし、診断に`schemaVersion`と`class`を加えた。
- 履歴マニフェスト（`loj-history/v1alpha1`）、字体注記（`loj-glyphs/v1alpha1`）、登録台帳（`loj-registry/v1alpha1`）、再構築報告（`loj-rebuild/v1alpha1`）を加えた。
- 各種類のJSON Schema、適合ケースの索引・期待結果・検査の報告のschema（`schemas/common/v1alpha1`）、v1alpha2の文法を加えた。
- DDR-012〜022を加え、DDR-003〜006・009〜011に次期仕様での扱いを追記した。
- 適合ケースを種類ごとの索引に分けた（版パッケージ124件、共通12件、履歴15件、字体注記9件、登録台帳8件、再構築4件）。L1負例とL3・L4等のケースの結果は、検査器で未確認である。
- `loj/v1alpha1`を凍結した。v1alpha1の適合データを`conformance/v1alpha1`に移した（内容は不変）。
- 移行の文書を、旧本文の変換から、原典による再構築の手順に書き直した。README、実装ガイド、制限、XML対応、検証記録、CONTRIBUTINGを次期仕様に合わせた。

## loj/v1alpha1 — 文字保存規則（2026-11-07）

CHAR-01を追加し、原典に対応するコードポイント列、正規化禁止、旧字体・異体字と異体字セレクタの保持、派生処理の分離を規定。VAL-01で機械検査と原典照合を区別し、DDR-011と既存データの移行上の制約を記録。Schema・EBNFは不変。文字保存の正式L1正例T106を追加。

## loj/v1alpha1 — 独立した適合レベル（2026-11-07）

VAL-01にL0〜L4の正確な定義表を明記。各レベルの判定は独立し、数字の大きいレベルの合格で
小さいレベルの合格を保証しない。CONF-02の累積適合要件を撤回し、指定レベルの正式ケースで検証する。
Schema・文法・固定ケースは不変。L0正例の期待値契約はIssue #1で扱い、今回は変更しない。

## loj/v1alpha1 — MAN-03明確化（2026-11-06、Issue #2 B案）

附属資料後続ファイルの見出し不要・非空条件、非最終ファイルのフェンス/HTML明示終端、
最終ファイルEOF許容、L0/L1の適用範囲と診断位置を明確化。DDR-007と見出し文法の注記を更新。
AST/Manifest Schemaは不変。旧74正式ケースを保持し、T076〜T105の30正式L1ケースを追加。
正式合計104（L0 11、L1 93）、参考L2 1。旧固定commitの意味は書き換えず、新commitで追跡する。

## loj/v1alpha1 — 2026-11-06

最初の規範仕様、Manifest/AST/ケース/期待結果Schema、コメントEBNF、固定適合データ、架空法令を追加。
HTMLコメント方式を採用。見出しの語による階層、scope基準の条ID、明示附則キーを確定。
L0/L1を正式対象とし、L2は参考設計に限定。CIは資料検査として提供。
調査、DDR、移行・実装ガイド及び検証の限界を記録。
