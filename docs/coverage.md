# 必須テスト領域の追跡

固定入力と結果は[索引](../conformance/v1alpha1/manifest.json)を参照。
T016/T017は同じ意味ASTを持つ分割後/前の対であり、位置は意味比較から独立する。

| 依頼領域 | ケース |
|---|---|
| 1 単一項 | T001 |
| 2 複数項 | T002 |
| 3 複数号 | T003 |
| 4 号の細分 | T004、T053 |
| 5 複数段落 | T005、T037 |
| 6 開始終了不一致 | T006、T029 |
| 7 不正親子 | T007、T033 |
| 8 重複番号 | T008、T050 |
| 9 枝番号 | T009 |
| 10 表示番号不一致 | T010 |
| 11 コード内マーカー | T011 |
| 12 通常コメント | T012、T045 |
| 13 属性欠落重複 | T013、T014 |
| 14 未知属性 | T015 |
| 15 複数ファイル | T016、T043 |
| 16 分割ID | T016、T017 |
| 17 日本語位置 | T018 |
| 18 CRLF | T019 |
| 19 Manifest不正 | T020、T038〜T041、T058〜T060 |
| 20 本則附則空間 | T021、T051 |
| 21 不正見出し | T022、T036、T044、T049 |
| 22 マーカー欠落 | T023 |
| 23 引用リスト強調リンク | T024 |
| 24 不正論理参照 | T025（L1成功）、T026（将来L2参考失敗） |
| 25 空ファイル/構造 | T027、T028 |

さらに削除条、レベル非依存、Unicode幅、raw HTML保護、全分類、細分10段、附属資料、
入力バイト、予約構文、完全サンプルを含む。索引のrequirementsが各規範IDへ対応する。
T062〜T075は複数附則、引用/リスト/インデントコードの保護、最終改行省略、削除条の矛盾、
数字幅混在、タブ、終了属性、項内見出し、分類再掲、欠番逆順、字母の拒否、属性順交換を扱う。
VAL-01/02とCONF-01/02は適合主張・試験契約そのものなので、資料監査とレビューで検証し、
法令入力の成功/失敗だけで検査するケースにはしない。その他の規範も1件で全節を網羅するとは主張しない。


T076〜T105は承認されたMAN-03 B案の独立ケース。附属資料の通常本文/見出しでの開始、
空白だけの後続、フェンスの文字種・長さ・引用内・CRLF・最終EOF、HTML7種類の明示/暗黙終端、
予約マーカー禁止、参照定義のファイル境界、インデントコード、先頭空行の保存を扱う。

## 次期仕様（loj/v1alpha2と新しい4種類）

適合ケースは、規範仕様と同じ分け方で置く。各ディレクトリの`manifest.json`が索引である。

| ディレクトリ | ケース | 内容 |
|---|---|---|
| [conformance/v1alpha2](../conformance/v1alpha2/manifest.json) | pkg-001〜233 | v1alpha1の106件を写したもの（pkg-001〜106。pkg-074の入力は2026-11-13に直した）と、「條」「ノ」「附　則」、無番号の項、表、前文・制定文、目次、いろは・括弧付きの十進の細分、括弧書きを含む条の見出しとその違反（pkg-107〜143）、L0の正例と、診断の位置を固定した負例（pkg-144〜150）、表の結合（pkg-151・152）、未対応の構造の申告の有無（pkg-153・154）、項の見出し（pkg-155〜165）、重複・見出しの違反の診断の位置（pkg-166〜173）、空白の字・表の矩形・附属資料の診断の位置（pkg-174〜182）、項の形式の本則（pkg-183〜191）、改正規定（pkg-192〜207）、列記（pkg-208〜216）、改正の指示の文のない改正規定（pkg-217〜225）、範囲の削除条（pkg-226〜230）、二行割りの引いた字句（pkg-231）、目次の中のATX見出しと`sourceUris`（pkg-232・233） |
| [conformance/loj-history/v1alpha1](../conformance/loj-history/v1alpha1/manifest.json) | hist-001〜068 | 祝日法の制定時と最初の改正後の版、履歴だけの法令リポジトリ三つ、その違反、共通の型と時点値の違反。行のkey（hist-031〜033）、効力の終了の根拠と時点（hist-034〜036、hist-052・053）、字体注記のファイルの選び方（hist-047・054・055）、条件の外で禁止するフィールド（hist-056〜061）、段階施行の二つの版（hist-062）、行のkeyの比べない版・表・枝（hist-063〜066）、原典資料の間の文言の食い違い（hist-067・068） |
| [conformance/loj-glyphs/v1alpha1](../conformance/loj-glyphs/v1alpha1/manifest.json) | glyph-001〜034 | 祝日法の字体注記と、その違反。L1が不合格の版の字体注記（未完了）。改正法（昭和四十一年法律第八十六号）の版の改正内容の中のセルを指す見え消しの注記（glyph-012）。ほかの原典資料で読めた判読困難の字（glyph-013〜020）。二行割りの行の区切りの字間の注記と、注記の範囲とその違反（glyph-021〜027）。異体字セレクタとivd、字体の違い、官報正誤の複製で読めない字（glyph-028〜034） |
| [conformance/loj-registry/v1alpha1](../conformance/loj-registry/v1alpha1/manifest.json) | reg-001〜016 | 六つのRecordの登録台帳、統合したRecordを残した登録台帳と、その違反。IDの再利用（reg-011）、統合先の解決（reg-012・013）、共通の型の違反（reg-014〜016） |
| [conformance/loj-rebuild/v1alpha1](../conformance/loj-rebuild/v1alpha1/manifest.json) | rebuild-001〜007 | 祝日法の再構築報告と、その違反（構造の差の件数はrebuild-005）。共通の型の違反（rebuild-006・007） |
| [conformance/common/v1alpha1](../conformance/common/v1alpha1/manifest.json) | common-001〜082 | L4の時点の整合（T-04）・番号・公布の時点・全部改正・撤回したRecord・他の登録空間、変更検査、固定参照（`git bundle`の架空の履歴）。変更検査は、ASTを生成できない版と人のレビューの記録（common-025〜027、029〜031、036・037、039、048、053）、種類の宣言の書き方（common-032〜035、038、040、043〜045）、官報正誤（common-041・042）、mergeのcommit（common-046）、正本のデータの外の変更（common-050〜055）、ファイルのモード（common-056〜058）、最初のcommit（common-059〜064）、旧履歴の境界（common-065〜069）。L4の統合・分割・未取得・終点の撤回（common-070〜073、081・082）、番号主張の状態（common-074〜077）、公布の時点を判定しない場合（common-078〜080） |

`scripts/verify.py`は、すべての索引・期待結果・正例の入力の形と、要件IDの存在を検査し、v1alpha2の正例のASTを原文と突き合わせる。v1alpha2のL0の正例は、ASTを持たずにL0の`pass`を挙げることと、ManifestがL0の検査を通ることを検査する。期待結果の診断の位置は、`documents`のファイルの中の一つの行（行末の改行を含む）であることだけを検査し（`law.yaml`を指す位置は拒否する。SRC-01はManifestの意味の違反の位置を定めない）、規則が指すべき行かは判定しない。版パッケージのケースを除く負例は、索引の`rejectedBy: schema`の印のとおりに、入力のYAMLがschemaで落ちるか、schemaを通るかを検査する（[CONTRIBUTING](../CONTRIBUTING.md#適合ケースの作り方)）。別の入力の写しに変更を加えて作った入力（索引の`derivedFrom`）は、元に変更を適用し直した結果と一致することを検査する。元の正例だけを直して`author_next_cases.py`を実行し忘れると、ここで失敗する。変更が期待する規則の違反だけを生むかは判定せず、レビューで確かめる。v1alpha2のL1の負例と、L3・L4・登録台帳・再構築報告・変更検査・固定参照のケースの合否は判定しない。検査器で判定する。

### ケースのない要件

次の要件にはケースを作らない（検査の対象外）。

| 要件 | 理由 |
|---|---|
| CORE-01〜05、CHAR-02〜05、VIEW-01〜07 | データの構成・作業・派生処理の制約であり、一つの入力の成否として検査できない。CORE-03（YAML）の違反は各系列の01で、CHAR-01はpkg-106で確かめる |
| CONF-01・02、VAL-01、VAL-03、VAL-05、VAL-07、VAL-08 | 適合の主張とケースの契約そのもの。資料の監査とレビューで確かめる |
| REB-01〜08 | 再構築の作業の手順。結果は再構築報告（REBR）と履歴マニフェストのケースで確かめる |
| SRC-02 | ファイルを書き出す実装の内部の保持であり、固定した入力と期待結果では表せない（実装の試験） |
| SRCM-01、XREF-04 | 予約の区分 |
| GLYPH-03、GLYPH-07、GLYPH-08 | 本文に置く字の選び方は原典と比べないと判定できない（原典照合） |
| RID-03、REV-02 | リポジトリの名前と可読ラベルは参照の解決に使わない、という制約 |
| TIME-05 | `reason`に書く理由の中身と、確認した範囲（SHOULD）は、レビューで確かめる。`reason`があることはTIME-01の必須のフィールドとして検査する（2026-11-12、[law-of-japan/loj-spec#32](https://github.com/law-of-japan/loj-spec/issues/32)） |
| CHG-05 | 変更検査の結果を適合レベルとして主張しないことは、実装と適合の主張への要求であり、レビューで確かめる（同上） |
| CHG-01の一部（正本のデータのファイルを変えないcommitを`auxiliary`と宣言する） | 変更検査は宣言した種類の検査だけで合否を決めるので、ほかの種類と宣言する誤りはレビューで確かめる（2026-11-17、[law-of-japan/loj-spec#138](https://github.com/law-of-japan/loj-spec/issues/138)） |
| CHG-01の一部（`correction`・`officialCorrection`・`restoration`で、本文の内容を変えない版を宣言しない） | 変更検査は宣言した版のASTを生成・比較しない（CHG-02）ので、レビューで確かめる。変更検査で合格することはcommon-047が当たる（2026-11-16、[law-of-japan/loj-spec#122](https://github.com/law-of-japan/loj-spec/issues/122)） |
| TABLE-02の一部（既存の行の`key`の維持、基礎の版の同じ行が同じ`key`を持つこと） | 行の同一性は法的な判断であり、機械では確かめられない。入力者への要件とする（2026-11-12、[law-of-japan/loj-spec#23](https://github.com/law-of-japan/loj-spec/issues/23)） |

[規範仕様の入口](../spec/README.md#版の状態)の版の状態の定め（要件IDなし）にも、ケースを作らない。仕様の資料そのものの管理の規則であり、法令の入力の成否として検査できないためである。状態の表の形は`scripts/verify.py`が検査する。タグを打つことは、公開の手順（[CONTRIBUTING](../CONTRIBUTING.md)）で確かめる。

機械で検査できるのにケースがない要件は、2026-11-12の時点でない（[law-of-japan/loj-spec#32](https://github.com/law-of-japan/loj-spec/issues/32)の結論（4））。下の段落に、ケースが一部の場合だけにとどまる要件を挙げる。

MD-04の空白の字（2026-11-15、[law-of-japan/loj-spec#72](https://github.com/law-of-japan/loj-spec/issues/72)）は、全角空白だけのセル（pkg-174）とNBSPだけの項（pkg-175）の負例（DIR-02）と、ゼロ幅の字だけのセルの正例（pkg-176）がある。タブ・ほかのZsだけの本文、空白だけの後続のファイル（MAN-03）、構造の外の全角空白だけの行（MD-03）のケースは、同じ定義で判定するので加えていない。

CHG-04（2026-11-12）は、L1が不合格の版を含む`metadata`の変更を判定不能とする正例（common-025）と、その版のファイルを`format`で`LoJ-Reviewed`なしに変える負例（common-026）がある。人のレビューの記録（`LoJ-Reviewed`）を付けた`format`の変換を判定不能とする正例（common-027）は、2026-11-15に加えた（[law-of-japan/loj-spec#63](https://github.com/law-of-japan/loj-spec/issues/63)）。記録がないものとして扱う`LoJ-Reviewed`（CHG-03）の負例は、2026-11-16に加えた（[law-of-japan/loj-spec#86](https://github.com/law-of-japan/loj-spec/issues/86)）。common-027の履歴の`format`のcommitで、`LoJ-Reviewed`を二つ置くもの（common-029）、値が空のもの（common-030）、値が空白だけのもの（common-031）で、どれもCHG-04の違反である。空白だけの値は、gitの`commit`の既定の整形で消えるので、バンドルの中のメッセージのバイト列で固定した。空白だけの値は、U+0020、U+0009、U+0020の三字の値の一例で固定し、どちらか一方だけの値は加えていない。U+3000等、ほかの空白の字だけの値は空でない値（記録）になる（CHG-03のtrailerの構文で、2026-11-16に確かめた）。U+3000だけの値を記録とし、判定不能とする正例（common-039）がある。`format`以外のcommitの`LoJ-Reviewed`のケースは加えていない。結果を変えないものとして、common-025と同じ判定になるためである。一部しか本文がない版のケースは、まだない。

CHG-03のtrailerの構文とCHG-04の判定不能の診断（2026-11-16、[law-of-japan/loj-spec#107](https://github.com/law-of-japan/loj-spec/issues/107)）は、次のケースがある。
- 正例: コロンの後にタブと二つの空白を置いた`correction`の宣言（common-032）、`LoJ-Revisions`を書いた`format`（common-033）、行末をCRLFにした宣言（common-038）、U+3000だけの値の`LoJ-Reviewed`（common-039）。common-038・039のメッセージは、gitの`commit`の既定の整形で変わらないよう、バンドルの中のバイト列で固定した。
- 負例（宣言のないcommitとしてCHG-03の違反）: 名前とコロンの間に空白を置いた宣言（common-034）と、trailerの後に段落が続く宣言（common-035）。
- 判定不能の診断を期待結果に挙げたケース: common-025の写しで、CHG-04の`undetermined`の診断を挙げる正例（common-036）と、common-026の写しで、CHG-04の違反と`undetermined`の診断の両方を挙げる負例（common-037）。common-025・026の期待結果に診断を足さず、写しのケースにしたのは、既存の期待結果を変えないためである。
- 加えていないケース: 値のない行は、`LoJ-Reviewed`の空の値（common-030）が当たる。最初の段落だけのメッセージは、宣言のないcommit（common-006）が当たる。`metadata`の`LoJ-Revisions`は、`format`と同じ文で定めるので、加えていない。`migration`は、本版で宣言できない（CHG-03の取り消しの項）ので、ケースを作れない。

登録空間の入力（VAL-03、2026-11-15、[law-of-japan/loj-spec#68](https://github.com/law-of-japan/loj-spec/issues/68)）は、他の登録空間のRecordを起点とする関係を未取得とする正例（common-028）と、他の登録空間を指す統合先の負例（reg-012、REG-02）がある。`space`を入力と同じ`loj`と書いた参照は、既存のケース（reg-009の`replacedBy`等）が解決済みとして確かめる。登録空間の入力がない場合の判定不能と、`space.yaml`を置いた登録台帳のケースは、加えていない。前者は、ケースの実行で入力を`loj`とする（CONF-01）ので、索引で表せない。後者は、`space.yaml`の形を定めていないので、適合ケースの登録台帳に置かない（CONF-01）。

RID-04・RID-05（2026-11-12）は、統合したRecordを残し、`replacedBy`で登録空間を書いて統合先を指す正例（reg-009）と、大文字を含む登録空間の負例（reg-010）がある。どちらの規則で報告するかは、2026-11-15にRID-01で定めた（一方が統合・分割・撤回したRecordならRID-05、そうでなければRID-01。[law-of-japan/loj-spec#63](https://github.com/law-of-japan/loj-spec/issues/63)）。統合したRecordのIDを別のRecordの別名に再利用する負例（reg-011）がある。分割・撤回したRecordのIDの再利用は、統合と同じ規則なので加えていない。

共通の型と時点値（2026-11-12、[law-of-japan/loj-spec#32](https://github.com/law-of-japan/loj-spec/issues/32)）は、履歴マニフェストの中で確かめる。登録空間と版の外部識別子の正例（hist-037）と、リポジトリの所在で指すRecord（TYPE-01、hist-038）、Sourceのidの重複（HIST-02、hist-039）、同じファイルにないSource（TYPE-03、hist-040）、Verificationの未知の状態（TYPE-04、hist-041）、原文のないScope（TYPE-06、hist-042）、精度と書式の不一致（TIME-02、hist-043）、版を対象としない外部識別子（HIST-01・HIST-09、hist-046）の負例がある。確認済みの時点値の根拠（TIME-06）は、hist-013が当たる。登録台帳・再構築報告の中の共通の型の違反（VAL-07）は、登録台帳の同一性の確認で、登録台帳にないSource（TYPE-03、reg-014）、Verificationの未知の状態（TYPE-04、reg-015）、出典のない確認済み（TYPE-05、reg-016）の負例と、再構築報告で、旧commitとの対応のVerificationの未知の状態（TYPE-04、rebuild-006）、出典のない確認済みの差（TYPE-05、rebuild-007）の負例がある（2026-11-26）。RecordRefに仮の値を置くことの禁止（TYPE-01、2026-11-25、[law-of-japan/loj-spec#172](https://github.com/law-of-japan/loj-spec/issues/172)）には、負例を置かない。仮の値はRecord IDの文字種に合い、登録台帳にないIDは未取得として報告されて違反にならないので（XREF-01）、検査の入力の成否として表せないためである。入力者への要求として、レビューで確かめる。

CHG-02・CHG-03（2026-11-12、[law-of-japan/loj-spec#18](https://github.com/law-of-japan/loj-spec/issues/18)）の従属するファイルの更新は、記録訂正で同じ版の`text.sources`を更新する正例（common-024）だけがある。common-024は、宣言した版だけのASTが変わり、従属する更新が宣言した版の`text.sources`に限られ、宣言した版の根拠（`text.sources`の箇所）があるので合格とする。Scopeの`nodes`・字体注記の更新、宣言していない版の従属するファイルを変える負例、登録台帳だけの`metadata`、revertのcommitのケースは、まだない。登録台帳の`git bundle`が要るためである。mergeのcommitは下のcommon-046が、最初のcommitは下のcommon-059〜061が当たる。

HIST-12の撤回した関係・内訳の扱い（2026-11-12、[law-of-japan/loj-spec#46](https://github.com/law-of-japan/loj-spec/issues/46)）は、撤回した関係を根拠とする負例（hist-034）、内訳をすべて撤回した関係を根拠とする負例（hist-035）、内訳の一部を撤回した関係を根拠とする正例（hist-036）がある。hist-036は撤回した内訳の`effective`を有効な内訳より前にしているが、期待結果は区分の結果だけで、終了の時点そのものは比べない。撤回した内訳から時点を得る誤りは、hist-036では区別できず、hist-052で区別する（下の段落）。関係を撤回して`termination`の項目を削らない状態はhist-034（L3）で検査する。撤回と削除を同じ変更で行うことを変更の検査で確かめるケースと、撤回の後に`termination`の項目を別の関係に置き換える変更のケースは、まだない。

HIST-12の終了の時点と警告（2026-11-13、[law-of-japan/loj-spec#53](https://github.com/law-of-japan/loj-spec/issues/53)）は、撤回していない内訳を一つに限る規則（HIST-03）の負例（hist-053）と、終了の時点より後に施行される版の警告の正例（hist-052）がある。hist-052は、有効な内訳の時点（1959-04-13）と撤回した内訳の時点（1960-04-01）の間に施行される版を持ち、期待結果にHIST-12の警告を挙げる。CONF-01により、成功するケースに挙げた警告は比べるので、撤回した内訳から時点を得る実装と、最も遅い時点を選ぶ実装は、警告を出さずにこのケースを満たさない。一方、警告を出さないことは比べないので、常に警告を出す実装は区別できない。hist-053の`requirements`のHIST-12は、HIST-03に違反する関係では終了の時点を決めず警告を判定しないことに関わるが、警告を出さないことは比べないので、この点はケースでは検査されない。終了の時点が確定日でない場合の判定不能を数えないことは、条件付きの失効（`pending`）と確定日の版を持つ既存の正例hist-003が当たるので、ケースを加えていない。

段階施行の版の本文（2026-11-25、[law-of-japan/loj-spec#173](https://github.com/law-of-japan/loj-spec/issues/173)）は、鉱山保安法の段階施行の二つの版の正例（hist-062、HIST-04・HIST-05・TIME-04）がある。起点（公布の日に施行する規定）と、`basis`が`enactment`で施行期日を政令で確定したRevisionを持つ。版パッケージに公布された本文の全体を書き、未施行の規定を除かないこと（HIST-05）は、本文を原典と比べて確かめる入力者への要求なので、hist-062の本文は`absent`とし、負例を置かない。未施行の規定を除いた本文も、版パッケージとしては正しい形を持ち、データだけからは区別できないためである。派生ビューで後の段階施行の施行時点を示すこと（VIEW-02）は、実装の試験で確かめる。

HIST-13（2026-11-12、[law-of-japan/loj-spec#23](https://github.com/law-of-japan/loj-spec/issues/23)）は、削った行の`key`を使わずに行を加える正例（hist-031）と、削った`key`を後の版で再使用する負例（hist-032）と、本文が一部しかない版を挟んで飛ばす正例（hist-033）がある。本文のない版を挟む正例（hist-063）、L1が不合格の版を挟む正例（hist-064）、表の番号が変わった表を前の番号の表と比べない正例（hist-065）、`basedOn`が分岐した別の枝の版と比べない正例（hist-066）は、2026-11-25に加えた。どれも、比べないとされた版・表・枝を比べると`c3d4`の再使用として不合格になる入力である。hist-065は、TABLE-01の連番のため、新しい表を前に加えて元の表を第2の表にした。glyph-004（行の`key`を変えて注記が古くなる）は、字体注記の`node`の解決（GLYPH-04）の負例であり、`key`の維持そのものの検査ではない。GLYPH-04の、ASTを変える変更での注記の更新（2026-11-15、[law-of-japan/loj-spec#70](https://github.com/law-of-japan/loj-spec/issues/70)）は、ノードIDが変わって注記が解決できなくなる場合をglyph-004が確かめる。ノードの分割・統合で注記が偶然同じ字の別の位置を指す場合は、機械では検出できないので、ケースを加えない。

HIST-04・05・08の2026-11-11の追加（[law-of-japan/loj-spec#20](https://github.com/law-of-japan/loj-spec/issues/20)）は、hist-023〜026のほか、`glyphNotes`のパスの不一致（hist-047）、`absent`のRevisionのディレクトリ（hist-048）、同じ関係・同じ施行時点の重複（hist-049）、統合したRevisionを基礎状態とする版（hist-050）、撤回した内訳だけを参照する成立根拠（hist-051）の負例がある（2026-11-12）。hist-047・048で字体注記の検査（L3（根拠））にかけるファイルは、2026-11-15にHIST-08で、自身のrevision_idのパスで決めるとした（[law-of-japan/loj-spec#63](https://github.com/law-of-japan/loj-spec/issues/63)）。hist-047・048の期待結果は履歴構造の区分だけを比べ、根拠の区分は比べない。L3のケースは区分の結果を一つだけ挙げる（CONF-01）ので、検査にかけるファイルの選び方（他の版の`glyphs.yaml`を検査にかけないこと）を根拠の区分で固定するには、誤りのある`glyphs.yaml`を他の版に置いた別のケースが要る。このケースは、下の段落のhist-054・055（2026-11-16）が当たる。分割したRevisionを基礎状態とする版の負例は、統合と同じ規則なので加えていない。

HIST-08の字体注記の検査にかけるファイルの選び方は、根拠の区分の正例で固定する（2026-11-16、[law-of-japan/loj-spec#87](https://github.com/law-of-japan/loj-spec/issues/87)）。hist-054は、hist-048と同じく`absent`のRevisionのディレクトリが残り、その`glyphs.yaml`の`revision`が合わない（GLYPH-01の違反になる）。hist-055は、hist-047と同じく`glyphNotes`が別の版の`glyphs.yaml`を指す。どちらも、そのファイルを字体注記として読まないので、根拠の区分は合格である。履歴構造の区分のHIST-08の違反はhist-047・048が固定するので、期待結果に挙げない（CONF-01）。

v1alpha2の2026-11-11の追加（[law-of-japan/loj-spec#25](https://github.com/law-of-japan/loj-spec/issues/25)）のうち、マーカーの空白はpkg-125・126を代表例とし、`<!--`の後・`-->`の前・名前と最初の属性の間の負例は加えていない。番号のない第1項が数字で始まる場合の申告（DISP-01）は、`unsupportedFeatures`を申告した版のL1の不合格（BASIC-03）の既存のケースと同じ結果になるので、加えていない。`supplements[].title`を検査しないこと（MAN-01）は、既存の正例（附則の`title`が見出しと違う「制定附則」）が当たる。

v1alpha2の2026-11-12の追加（[law-of-japan/loj-spec#27](https://github.com/law-of-japan/loj-spec/issues/27)）は、目次（pkg-129）、いろは・括弧付きの十進の細分（pkg-130）、括弧書きを含む条の見出し（pkg-131）、ヰを使わないいろはの欠番（ウ・ノ）とヱ・ス、括弧付きのASCIIの十進（pkg-142）の正例と、目次の位置・中身・数（pkg-132〜135、143）、細分の表示（pkg-136〜139）、条の見出しの括弧（pkg-140・141）の負例がある。目次の中のATX見出しの負例（pkg-232）は、2026-11-25に加えた。ATX見出しの行は、TOC-01の禁止に当たるほか、`toc`のマーカーを見出しを越えて閉じない（DIR-02）ので、二つの規則の診断を期待する。未対応の構造を申告した版の参考の集計（BASIC-03）は、L1の結果を変えない任意の報告であり、ケースを作らない。

v1alpha2の2026-11-12の追加（[law-of-japan/loj-spec#1](https://github.com/law-of-japan/loj-spec/issues/1)）は、L0の正例（未対応の構造を申告した入力のpkg-144、L1の違反を含む入力のpkg-145。L0では成功するケースなので`valid/`に置く）と、診断の位置（SRC-01）を固定した負例（CRLFと4バイトの文字を含む表示の不一致のpkg-146、未閉鎖のpkg-147、対応しない終了のpkg-148、属性の不正のpkg-149、改行のない最後の行の対応しない終了のpkg-150）である。既存の負例の期待結果には、位置を加えていない。重複・見出しの違反の位置のケースは、後の2026-11-13の追加にある。

v1alpha2の診断の位置（2026-11-13、[law-of-japan/loj-spec#67](https://github.com/law-of-japan/loj-spec/issues/67)、SRC-01）は、`documents`の順（`b.md`、`a.md`）で後のファイル（CRLFの`a.md`）にある章をまたぐ条の重複（pkg-166）、4バイトの文字の後の別のファイルの分類の番号の重複（pkg-167）、項の番号の重複（後の開始のマーカーの行。コンテナの範囲ではない、pkg-168）、`main.md`でないファイルの行の`key`の重複（pkg-169）、属性の重複（pkg-170）、CRLFと4バイトの文字の後の表にない字体の条ラベル（pkg-171）、4バイトの文字の後の条の見出しの対応しない括弧（pkg-172）、CRLFの附則の見出しの半角空白（pkg-173）の負例である。行の`key`の重複は、表が一つのファイルの中で閉じる（DIR-02、MAN-03）ので、後の定義を別のファイルに置くケースは作れない。Manifestの意味の違反と、SRC-01の一覧にない診断（削除条の形の違反等）は、SRC-01が位置を定めないので、位置のケースの対象外である。2026-11-15に、附属資料の`title`と最初の見出しの不一致（HEAD-03、最初の見出しの行、pkg-180）、空白だけの後続のファイル（MAN-03、ファイルの全体、pkg-181）、後続のファイルの前で閉じないコードフェンス（MAN-03、ブロックの開始行、pkg-182）の負例を加えた（[law-of-japan/loj-spec#81](https://github.com/law-of-japan/loj-spec/issues/81)）。ファイルの全体の位置は複数の行にわたりうるので、`verify.py`は、一つの行のほかに、ファイルの全体を位置として受け付ける。番号・`key`の重複（pkg-008、pkg-050、pkg-115、pkg-166〜169）が生むノードIDの重複（AST-02）は連鎖する違反なので、期待結果に挙げない（AST-02に書いた）。

TABLE-04（2026-11-15、[law-of-japan/loj-spec#73](https://github.com/law-of-japan/loj-spec/issues/73)）は、続く先にもセルを書いた列数の不一致（pkg-177）、最後の行を越える`rowspan`（pkg-178）、`rowspan`のセルの位置に重なる`colspan`（pkg-179）の負例がある。矩形の正例は、既存のpkg-110（`colspan`）、pkg-151（`rowspan`）、pkg-176が当たる。既存の負例pkg-117（`colspan=1`）は矩形でないので、TABLE-03に加えてTABLE-04の診断も出るが、期待結果に挙げない規則の診断が加わってよい（CONF-01）ので、期待結果は変えない。矩形でない表を申告した版のL1の不合格（BASIC-03）は、既存のケースと同じ結果になるので、加えていない。

v1alpha2の表の空の欄（2026-11-12、[law-of-japan/loj-spec#57](https://github.com/law-of-japan/loj-spec/issues/57)）は、上の欄が続く読替えの表を`rowspan`で書く正例（pkg-151）と、空のセルの負例（pkg-152、DIR-02）がある。pkg-151がL1で確かめるのは、結合したセルの書式（属性、セルの`c`の数え方、ID、AST）だけで、欄が続くことを結合で書いたかどうかではない。pkg-152の`requirements`のTABLE-03は、入力の背景（続く欄を空のセルで書いた形）を示すもので、L1の診断はDIR-02だけである。左の欄が右へ続く場合（`colspan`）は同じ規則で、書式は既存の正例pkg-110の`colspan=2`が当たるので、加えていない。続く欄を結合で書くことと、空の欄をコメントや原典にない字で埋めないこと（TABLE-03）は、原典と比べないと判定できないので、ケースを作らない。罫線に囲まれた空の欄を申告した版のL1の不合格（BASIC-03）は、既存のケースと同じ結果になるので、加えていない。

v1alpha2の項の見出し（2026-11-13、[law-of-japan/loj-spec#56](https://github.com/law-of-japan/loj-spec/issues/56)、PARA-02）は、直接の項の形式の附則の第1項・第2項の見出し（pkg-155）、条の見出しを持つ条の、表示番号を省略した第1項の見出しと号・見出しのない第2項（pkg-156）、無番号の項の見出しと属性の順の入れ替え（pkg-157）、CRLFの見出しの行（pkg-165。`caption`は行末のCRもLFも含まず、`text`は両方を保つ）の正例と、見出しの行がない（pkg-158）、見出しの行の後に本文が続く（pkg-159）、見出しの行の末尾の空白（pkg-160）、属性のない第2項の見出しの行（pkg-161、DISP-01）、属性の値`absent`（pkg-162、DIR-01）、見出しの行の後に本文の行がなく号が続く（pkg-163）、対応しない括弧の見出しの行（pkg-164）の負例がある。pkg-161・162を除く負例は、診断の位置（見出しの行として検査した本文の行、SRC-01）も期待結果に挙げる。pkg-161（表示の不一致）とpkg-162（属性の不正）は、PARA-02の診断ではなく、位置の数え方が既存のケース（pkg-146・149）で確かめられているので、位置を挙げていない。pkg-161は、属性のない項の本文の行を見出しと推測しないこと（実装）の確かめを兼ねる。属性のない第1項と`numbering=implicit`の項の最初の行が括弧だけの行である場合は、L1では本文として合格するので、見出しの書き落としは原典照合で確かめ、ケースを作らない。続く項にかかる見出しを最初の項にだけ書くことも原典と比べないと判定できず、pkg-157は書式だけを確かめる。

v1alpha2の項の形式の本則（2026-11-16、[law-of-japan/loj-spec#131](https://github.com/law-of-japan/loj-spec/issues/131)、PARA-03）は、表示番号のある二つの項からなる本則（pkg-183。元号法の形）、項番号のない一つの項からなる改正法の本則（pkg-184。改正の指示は本文の文だけ）、制定文と無番号の二つの項からなる本則（pkg-185）の正例と、項の後の条の見出し（pkg-186、混在）、二つのファイルに分けた項の形式の本則（pkg-187）、条を置かない章の下の項（pkg-188、DIR-02）、制定文だけで分類・条・項のどれもない本則（pkg-189）、項の後の制定文（pkg-190、PRE-02）、一つだけの無番号の項（pkg-191、PARA-01）の負例がある。pkg-184と附則は、条の形式でない本則と直接の項の形式の附則が一つの版に並ぶことを兼ねて確かめる。原典にない条・項の番号を補わないことは、原典と比べないと判定できず、ケースを作らない。改正の指示の後に規定や表を置く本則（複雑な改正指示）は、本版では未対応のままであり、ケースを作らない。

v1alpha2の改正規定（2026-11-16、[law-of-japan/loj-spec#132](https://github.com/law-of-japan/loj-spec/issues/132)、AMEND-01〜03）は、次のケースがある。
- 正例: 昭和四十一年法律第八十六号と同じ構造の架空の改正法（pkg-192）。項の形式の本則の一つの項に、表の行を加える改正規定が二つ並ぶ。附則の項に、表の行を加える改正規定とその後の本文だけの改正の指示、見出しの変更・項の削除・字句の置換・番号の変更を本文だけで述べる改正の指示、条の全文を改める改正規定がある。条の形式の改正法で、項・号・細分・本文・章を改正内容とし、改正法自身と同じ番号の条（第二条）を改正内容の中に置く正例（pkg-193）。pkg-193は、項の形式の本則（PARA-03）によらない。
- 負例: 改正内容のない改正規定（pkg-194）、改正内容の後の本文（pkg-195）、改正の指示のない改正規定（pkg-196）、1から始まらない番号（pkg-197）、改正規定の外の改正内容（pkg-198、DIR-02）、項と表を混ぜた改正内容（pkg-199）、空の改正内容（pkg-200）、`level`の違う細分（pkg-201）、改正内容の中の改正規定（pkg-202）、改正規定の本文の中の条の見出し（pkg-203、DIR-02。引用した条を改正内容の外に書いた誤り）、改正内容の中の項の中の見出し（pkg-204、DIR-02。pkg-071と同じ扱い）、改正内容の中の条の番号の重複（pkg-205、HEAD-02）、改正内容の中の章の下の項（pkg-206、DIR-02）、改正内容の中の附則の見出し（pkg-207、HEAD-01）。
- 加えていないケース: 改正内容を改正法自身の条・表として書くことは、構造の形としては正しく、原典と比べないと判定できない（原典照合）。改正の指示の文を構造と推測しないことは、pkg-192の本文だけの改正の指示（附則第三項）が、項の本文のまま合格することで確かめる。原典の見え消しを改正内容の中のセルで指す字体注記（GLYPH-09）は、昭和四十一年法律第八十六号のRecordの、制定の版だけの履歴リポジトリの正例（glyph-012）で確かめる。注記は`19660625-act-86/main/paragraph/1/amendment/1/content/table/1/row/f9km/cell/2`の`政令で定める日`を指す。被改正法令（祝日法）の版の同じ見え消しの注記（hist-001の`row/a1w3`）とは、別の版の別のノードであり、行の`key`も合わせない（AMEND-02）。glyph-012の本文は、衆議院の制定法律の本文を下書きとし、字句の明らかな誤り（「附属磯関」「一都」「判り」）を構成から直したもので、原典の字体とは照合していない（`glyphCheck: unverified`）。注記の位置の規則（GLYPH-04）は変えていない。

v1alpha2の列記（2026-11-20、[law-of-japan/loj-spec#142](https://github.com/law-of-japan/loj-spec/issues/142)、LIST-01・LIST-02）は、次のケースがある。
- 正例: 労働省設置法（昭和二十二年法律第九十七号）第三條と同じ構造の項の列記、号の中の列記、各行の頭に「一」（ひとつ）を置く列記とその後の柱書の続きの本文、改正内容の列記（pkg-208）。行の頭の「一」は本文に残し、`display`は空文字列である。
- 負例: 連番でない番号（pkg-209、LIST-01）、申告のない号と列記の混在（pkg-210、LIST-02）、申告のない細分と列記の混在（pkg-211、LIST-02）、申告した号と列記の混在（pkg-212、BASIC-03だけ）、列記の中の列記（pkg-213、DIR-02）、空白だけの列記（pkg-214、DIR-02）、`number`のない列記のマーカー（pkg-215、DIR-01）、列記と号を混ぜた改正内容（pkg-216、AMEND-02）。
- pkg-210・211の索引の`requirements`にBASIC-03を挙げるのは、申告のない機械で認識できる未対応の構造を、その構造を扱う規則（ここではLIST-02）の違反とするのがBASIC-03の定めだからである。期待結果の診断はLIST-02だけである。pkg-212との対で、申告の有無で診断の規則が変わることを確かめる（ローマ数字の細分のpkg-074・pkg-153と同じ形）。
- 加えていないケース: 法令の列記を行に分けた本文で書くこと、番号のない列挙を号として書くこと（号と列記の区別）、段に分けた列記を一つの本文で書くことは、構造の形としては正しく、原典と比べないと判定できない（原典照合）。

v1alpha2の改正の指示の文のない改正規定（2026-11-20、[law-of-japan/loj-spec#143](https://github.com/law-of-japan/loj-spec/issues/143)、AMEND-01の`instruction=implicit`）は、次のケースがある。
- 正例: 労働省設置法（昭和二十二年法律第九十七号）附則第十四條・第十五條と同じ構造の架空の改正規定（pkg-217）。第十四條は、本文だけの改正の指示と二行にわたる引いた字句（MD-04。改行は本文の`text`に残る）、指示の文を持つ改正規定、その直後の指示の文のない削除条の形（第七條）、本文だけの改正の指示、指示の文のない削除条の形（第二十三條）を一つの項に並べる。第十五條は、指示の文のない、無番号の三つの項（`numbering=implicit`）からなる条の全文（第十條の二）と、その後に続く本文だけの改正の指示を置く。改正内容の中の削除条は、`削除`の行の後に空行を置く（HEAD-04）。
- 負例: 改正の指示の本文を持つ`instruction=implicit`の改正規定（pkg-218、AMEND-01）、改正内容のない`instruction=implicit`の改正規定（pkg-219、AMEND-01）、続けて置いた`instruction=implicit`の改正規定（pkg-220、AMEND-01）、`instruction=explicit`を書いた改正規定（pkg-221、DIR-01。書ける値は`implicit`だけ）、改正内容の中の削除条の後に空行がないもの（pkg-222、HEAD-04）。
- 加えていないケース: 原典にない改正の指示の文を補うこと、原典に指示の文がある改正規定に`instruction=implicit`を書くこと、掲げた規定の範囲、指示の文を持つ改正規定の改正内容の直後に掲げた規定を、その続きとするか別の改正規定とするかは、原典と比べないと判定できない（原典照合）。改行が引用元の行の区切りか組版か（MD-04）も同じである。

同じ時期の改正規定の調査（2026-11-24、[law-of-japan/loj-spec#150](https://github.com/law-of-japan/loj-spec/issues/150)、[調査の記録](survey-showa-amendments.md)）で見つけた形を試料に、次の正例を加えた。どれも原典の構造をなぞった架空の本文である。
- 國有林野法の一部を改正する法律（昭和二十二年法律第百七十四号）の形（pkg-223）。項の形式の本則の一つの項が、指示の文のない削除条の形（第二十六條）だけを改正内容とする。附則は一つの項である。
- 簡易生命保險法等の一部を改正する法律（昭和二十二年法律第百七十三号）の形（pkg-224）。改正法の各条（第一條・第二條）が、ほかの法令の条の全文（一つの項）を、指示の文なしに掲げる。附則は、番号のない二つの項（`numbering=implicit`）である。
- 國有財產法施行令の一部を改正する政令（昭和二十二年政令第四十五号）の形（pkg-225）。項の形式の本則の一つの項で、冒頭の文の直後の指示の文のない削除条の形（第二條）、本文だけの改正の指示、続けて掲げた四つの削除条（第六條・第八條・第九條・第十條。一つの改正内容。AMEND-01）、本文だけの改正の指示を並べる。
- 加えていないケース: 二つ以上の条をまとめた削除条の形（「第九十條及ヒ第九十一條　削除」等）は、調査の時点ではHEAD-04で未対応だった。今は下の範囲の削除条のケースが当たる。二行割りで組んだ引いた字句の行の区切りは、調査の時点ではMD-04で書き方が決まらなかった。今は下の二行割りのケースが当たる。

v1alpha2の範囲の削除条（2026-11-24、[law-of-japan/loj-spec#153](https://github.com/law-of-japan/loj-spec/issues/153)、HEAD-04）は、次のケースがある。
- 正例: 範囲のラベルの削除条（pkg-226）。本則に、`から…まで`（`第二条から第四条まで`、`2:4`）と`及び`（`第五条及び第六条`、`5:6`）の削除条を置き、続く条（第七条）の改正規定の改正内容に、単独の削除条（第八十九條）と`及ヒ`の削除条（`90:91`）を続けて掲げ、もう一つの改正内容に、枝番号を持つ`乃至`の削除条（`第百十二條ノ二乃至第百十二條ノ五`、`112-2:112-5`）を掲げる。刑法の一部を改正する法律（昭和二十二年法律第百二十四号）と所得税法施行令の形をなぞった架空の本文である。
- 負例: 範囲のラベルの条に`削除`の行を置かずに項を置いたもの（pkg-227、HEAD-04）、始めの条が終わりの条より後のもの（pkg-228、HEAD-04）、範囲の削除条の範囲に番号が含まれる条（pkg-229、HEAD-02。範囲の番号`2:4`と条`3`のIDは違うので、ノードIDの重複（AST-02）にはならない）、`から`の後に`まで`を欠くラベル（pkg-230、HEAD-01の未認識の見出し）。
- 加えていないケース: 結ぶ語を原典どおりに書いたか、条ごとの削除条をまとめて書いていないか、範囲の中にどの条があったかは、原典と比べないと判定できない（原典照合）。範囲の始めと終わりが同じ番号のもの（`第二条及び第二条`）は、pkg-228と同じ文（始めが終わりより前）の範囲なので加えていない。二つの範囲の削除条の範囲が重なるもの、改正内容の中の範囲の重複は、pkg-229と同じ文（範囲に含まれる番号の重複）の範囲なので加えていない。範囲のラベルの中の`（見出し）`、表にない結ぶ語は、pkg-230と同じ文（範囲のラベルの形に当たらない）の範囲なので加えていない。三つ以上の条を列挙した削除の表示は、未対応（HEAD-04）である。Scopeの照合（TYPE-07）の範囲の番号のケースは、加えていない。範囲の削除条を持つ履歴のケースが要るためである。

v1alpha2の二行割りの行の区切り（2026-11-24、[law-of-japan/loj-spec#154](https://github.com/law-of-japan/loj-spec/issues/154)、MD-04）は、逓信省官制の一部を改正する勅令（昭和二十二年勅令第百四十三号）の形をなぞった正例（pkg-231）がある。二行割りで組んだ「總務局／勞務局」の区切りを、項の本文の`text`の改行として書く。
- 加えていないケース: 区切りが引用元の行か組版か（MD-04）は、原典と比べないと判定できない（原典照合）。二つの行をつないで書いた割注は、本文の通常の文字列であり、L1で区別できる入力がない。見出しの中の区切りをつないで書くこと（MD-04）は、見出しが改行を含めないこと（HEAD-01）の帰結であり、見出しの行は一行で終わるので、改行を書いた見出しを入力として作れない。判断できない区切りを`kind: spacing`で記録する字体注記のケース（改行を書いた場合の`recorded`、書かなかった場合の空文字列）は、加えていない。判断できない区切りを`kind: spacing`で記録する字体注記のケースは、下のglyph-021・022が当たる（[law-of-japan/loj-spec#159](https://github.com/law-of-japan/loj-spec/issues/159)）。

v1alpha2の未対応の構造の申告の有無（2026-11-13、[law-of-japan/loj-spec#50](https://github.com/law-of-japan/loj-spec/issues/50)）は、ローマ数字の細分の表示`（ｉ）`を、申告せずに書いた負例（pkg-074、L1でDISP-01）と、申告して書いた負例（pkg-153、L1でBASIC-03）・L0の正例（pkg-144）の対と、空の`unsupportedFeatures`の負例（pkg-154、L0でMAN-01）がある。pkg-074の入力は、細分の字種にいろはを加えた変更（[law-of-japan/loj-spec#54](https://github.com/law-of-japan/loj-spec/pull/54)）の後、`イ　細分。`がDISP-01に違反しなくなっていたので、`（ｉ）　細分。`に直した（期待結果は変わらない）。[CONF-01](../spec/common/v1alpha1/04-conformance.md)は期待結果に挙げていない診断が加わることを許すので、申告のないpkg-074でBASIC-03を報告する実装と、申告のあるpkg-153でDISP-01をL1の診断として報告する実装を、固定ケースでは区別できない。

GLYPH-05・GLYPH-07・GLYPH-10・GLYPH-11（2026-11-12、[law-of-japan/loj-spec#21](https://github.com/law-of-japan/loj-spec/issues/21)）: 正規分解を持たない互換漢字のブロックの字に注記がなくても合格する正例（glyph-010）と、字体を保持する資料を指さずに字体を照合済みにする負例（glyph-011）がある。`text.correctionsSurveyed`は、hist-001の正例で使っている。次は2026-11-25に加えた。いずれも制定時の版に架空の注記を加えたものである。`ivd`は、異体字セレクタ（U+E0100）を付けた字の`selected`の注記の正例（glyph-028）と、`ivd`がない（glyph-029）、`sequence`が`recorded`と合わない（glyph-030）、異体字セレクタを含まない注記に`ivd`がある（glyph-031）負例がある。これらはschemaでは確かめられず、検査器がGLYPH-05で判定する。`variance`は、正例（glyph-032）と、`candidates`のない負例（glyph-033、schemaで不合格）がある。`text.variances`は、`disputed`の正例（hist-067）と、`readings`が一件だけの負例（hist-068、schemaで不合格）がある。

GLYPH-02・03・05・06・07（2026-11-20、[law-of-japan/loj-spec#141](https://github.com/law-of-japan/loj-spec/issues/141)）: 官報の複製で読めず、ほかの原典資料（御署名原本）で読めた字を本文に置く`illegible`・`basis: otherSource`の注記と、`basis`を省いた〓の`illegible`の注記の正例（glyph-013）がある。どちらもhist-001の制定時の版の写しに加えた。負例は、`illegible`の`basis: provisional`（glyph-014）、`otherSource`で〓を置く（glyph-015）、`evidence`が一件だけ（glyph-016）がschemaで不合格になり、`evidence`が同じSourceだけ（glyph-017）、公布された本文のSourceを指さない（glyph-018）、読めた資料が下書きの資料（`kind: egov`）だけ（glyph-020）がL3（根拠）で不合格になる。官報正誤（`officialCorrection`）のSourceを読めない側に使う正例（glyph-034）は、2026-11-25に加えた。`basis`を省いて〓でない字を置く負例（glyph-019）は、従来の`recorded`の規則の境界であり、schemaで不合格になる。同じ号の官報の別の複製を別のSourceとして`text.sources`から指すこと（GLYPH-07）と、`evidence`のどの箇所が読めない箇所を示すかは、機械では検査できない（原典照合）。GLYPH-10の、`otherSource`の判読困難の注記が残っていても`verified`にできることは、正例がない。正例の基にしたhist-001の版は`glyphCheck: unverified`であり、再構築報告の記録と合わせて`verified`に変えると、ほかの記録と食い違うためである。

GLYPH-02・GLYPH-04の改行の`spacing`（2026-11-24、[law-of-japan/loj-spec#159](https://github.com/law-of-japan/loj-spec/issues/159)、MD-04）: 架空の勅令の版の、二行割りの行の区切りの字間の注記三件の正例（glyph-021）がある。本文のファイルは、LFの`one.md`とCRLFの`two.md`である。注記は、LFの本文に書いた改行（`recorded: "\n"`、`offset`はLFの位置）、CRLFの本文に書いた改行（`recorded: "\r\n"`の2字、`offset`はCRの位置）、つないで書いて改行を書かなかった区切り（`recorded: ""`、`offset`は読む順で先の行の最後の字の直後）である。負例は、CRLFの行の区切りを`recorded: "\n"`だけで記録したもの（glyph-022、GLYPH-04。`offset`の字はCRなので、本文と一致しない）である。
- 注記の範囲（2026-11-24、[law-of-japan/loj-spec#161](https://github.com/law-of-japan/loj-spec/issues/161)、GLYPH-04）: 空の`recorded`の`offset`を本文の長さより大きくした負例（glyph-023）と、CRLFの行の終端のLFの位置を`offset`として`recorded: "\n"`とした負例（glyph-024。`recorded`はその位置の本文と一致するが、範囲の端がCRとLFの間にある）がある。どちらもglyph-021の写しである。範囲の境界の正例として、g3の`offset`を第三條の項の本文の長さ（28）にした空の注記（glyph-025。文字列の末尾を指し、範囲の中にある）がある。境界を固定するための写しで、g3はもう原典の区切りの位置を指さないが、機械の検査（GLYPH-04）では検出できない。空の注記の`offset`をCRLFのCRとLFの間（第三條の項の本文の位置27）にした負例（glyph-026）と、CRLFの行の終端のCRだけを`recorded: "\r"`とした負例（glyph-027。範囲の終わりがCRとLFの間にある）もある。
- 加えていないケース: 改行を書かなかった`spacing`の注記の`offset`が、本文の範囲の中で区切りの位置からずれていることは、`recorded`が空文字列なので、機械の検査（GLYPH-04）では検出できない。`offset`が区切りの位置を指すかは、原典照合で確かめる。`display`の範囲の外の注記は、glyph-023と同じ文（注記の範囲）の範囲なので加えていない。`display`の範囲は、検査器が本文と別の経路で実装しやすい点だが、文は本文と同じである。LFの本文の`offset`のずれは、glyph-002と同じ文（`recorded`と本文の一致）の範囲なので加えていない。

XREF-02（2026-11-12、[law-of-japan/loj-spec#16](https://github.com/law-of-japan/loj-spec/issues/16)）は、全部改正の対応の合格と、存在しない関係・撤回した関係・全部改正でない関係を指す負例、起点が食い違う負例がある（common-017・018・020〜022）。関係の`from`が統合したRecordで、統合先が全部改正後のRecordである正例（common-070）、`from`が分割したRecordで判定不能になる正例（common-071）、旧Recordの履歴マニフェストを取得できず未取得になる正例（common-072）は、2026-11-26に加えた。XREF-01の不存在確認済み（`withdrawn`）は、起点の側の確定した関係の違反（common-019）と、未確認の関係で違反にならない境界（common-023）、終点の側の確定した関係の違反（common-073）がある。分割したRecordへの参照の結果（解決済み・未取得・不存在確認済みのどれで報告するか）は、VAL-06の三つの値に当てはまらないので、common-071の期待結果には参照の結果と関係の解決の区分を挙げない。

XREF-05・XREF-06（2026-11-12、[law-of-japan/loj-spec#13](https://github.com/law-of-japan/loj-spec/issues/13)・[law-of-japan/loj-spec#19](https://github.com/law-of-japan/loj-spec/issues/19)）は、ケースがあるが一部だけである（common-013〜016）。common-013は`structured.period.raw`と`raw`を続けた文字列との一致に当たる。採用中の主張が`nonexistent`・`unknown`で`law.number`がある場合の警告（common-074・075）、`conflicting`の場合と採用中の主張がない場合の判定しない正例（common-076・077）は、2026-11-26に加えた。判定しない正例は、`exists`の主張なら警告になる番号の版を入力にしているが、警告を出さないことは比べない（CONF-01）。XREF-06は、一方が確定日でない判定不能（common-078）、撤回した関係を比べない正例（common-079）、一方だけが`promulgated`を持つ判定しない正例（common-080）、統合したRecordを起点とする関係を統合先と同じ起点として比べる負例（common-081）、分割したRecordを起点とする関係を比べない正例（common-082）がある。

条件の外で禁止するフィールド（2026-11-16、[law-of-japan/loj-spec#104](https://github.com/law-of-japan/loj-spec/issues/104)）は、本文に禁止を加えたフィールドごとに、schemaで落ちる負例がある。`conditions`のある`unsurveyed`の適用関係（hist-056、HIST-07）、制定の起点の`totallyRevises`（hist-057、HIST-04）、`active`のRevisionの`replacedBy`（hist-058、HIST-10）、`repealed`の項目の`evidence`・`verification`（hist-059、HIST-12）、`expired`の項目の`relation`（hist-060、HIST-12）、`pending`の`determinedBy`（hist-061、TIME-01）、`structure`の差の`count`（rebuild-005、REBR-05）、`active`のRecordの`replacedBy`（reg-013、REG-02）である。同じ文のほかのフィールド・値（`repealed`の`effective`、`totallyRevised`の項目、`examples`等）は、同じ規則・同じschemaの枝なので、加えていない。`category`の禁止（CONF-01）は、適合ケースの索引・期待結果と実装の報告の形であり、検査の入力にならないので、ケースを作らない。索引と期待結果は`verify.py`がschemaで検査する。

適合レベルとは別に報告する検査の結果（VAL-04）と、宣言のないcommitの規則（CHG-03）（2026-11-16、[law-of-japan/loj-spec#115](https://github.com/law-of-japan/loj-spec/issues/115)）は、既存のケースが当たる。変更検査の未完了（common-025・027）、登録台帳・再構築報告の不合格（reg-002〜、rebuild-002〜）、宣言のないcommit（common-006・034・035）である。`LoJ-Change`の値が種類でない負例（common-040）を加えた。common-040の`requirements`のCHG-01は、値を比べる種類の表を示すもので、診断はCHG-03だけである（CHG-01の診断は出ない）。mergeのcommitのケースは、下のcommon-046が当たる。参照の解決のケースは各参照の`references`で比べ、検査の結果を挙げていない（CONF-01）。

CHG-02の`correction`・`officialCorrection`の根拠の判定（2026-11-16、[law-of-japan/loj-spec#116](https://github.com/law-of-japan/loj-spec/issues/116)）は、官報正誤のSourceを本文の出典に加える`officialCorrection`の正例（common-041）と、官報正誤のSource（`kind: officialCorrection`）を`sources`に置くが`text.sources`で指さない`officialCorrection`の負例（common-042）がある。`correction`の根拠は、既存の正例（common-004、common-024、common-032）の`text.sources`が当たる。本文のない版を宣言した`correction`の負例は、まだない。本文のない版には版パッケージがなく、訂正する本文もない。そのため、この入力では根拠の欠け（CHG-02）のほかに、宣言した版の範囲・AST検査の扱い（CHG-02の表、CHG-04）が関係しうる。期待する規則を一つに決められる入力を、まだ定めていない。

CHG-03の宣言の重複（2026-11-16、[law-of-japan/loj-spec#117](https://github.com/law-of-japan/loj-spec/issues/117)）は、同じ値の`LoJ-Change`を二つ置いた`correction`の負例（common-043）と、同じrevision_idの`LoJ-Revisions`を二行に置いた`correction`の負例（common-044）と、`LoJ-Revisions`を省略してよい`format`で二行に置いた負例（common-045）がある。common-044のbaseは、common-043で不合格のcommitである。各commitは親とだけ比べて単独で検査される（CHG-03）ので、baseの不合格は影響しない。重複を除いた同じ`correction`が合格することは、common-004が当たる。値の違う`LoJ-Change`の重複は、同じ文の範囲なので加えていない。`LoJ-Reviewed`の重複は、記録がないものとして扱う（common-029）。

CHG-03のmergeのcommit（2026-11-16、[law-of-japan/loj-spec#120](https://github.com/law-of-japan/loj-spec/issues/120)）は、分岐したブランチの`correction`を、`correction`と宣言したmergeのcommitで`main`に統合する負例（common-046）がある。baseは分岐の元のcommit、headはmergeのcommitである。分岐したブランチの`correction`は、単独では合格する記録訂正（common-004と同じ変更）なので、baseとheadの間のcommitの数え方によらず、不合格になるのはmergeのcommitだけである。mergeのcommitは、宣言によらず比べずに不合格とする（CHG-03）。宣言のないmergeのcommitと、親が三つ以上のcommitは、同じ文の範囲なので加えていない。

宣言した版の本文の内容の変化（2026-11-16、[law-of-japan/loj-spec#122](https://github.com/law-of-japan/loj-spec/issues/122)）は、宣言した版の本文を変えず、`text.sources`の箇所だけを直す`correction`の正例（common-047）がある。CHG-01はこの宣言を禁じるが、CHG-02の検査は宣言した版のASTを比べないので、変更検査は合格する。宣言した版がASTを生成できない`correction`・`restoration`で、CHG-04の判定不能が出ないこと（2026-11-16、[law-of-japan/loj-spec#126](https://github.com/law-of-japan/loj-spec/issues/126)）は、L1が不合格の版（条の見出しに構造ラベルがない。HEAD-01）の本文を直し、変更後もL1が不合格のままの`correction`の正例（common-048）と、第一条だけの一部しか本文がない版（`text.status: partial`、`gaps`）に第二条を補い、`complete`にする`restoration`の正例（common-049）がある。どちらも宣言した版のほかに版がないので、比べるASTはなく、合格になる。ASTを比べる版（metadataではすべての版）がASTを生成できない場合の判定不能は、common-025が当たる。`officialCorrection`は、宣言した版の扱いが`correction`と同じ行なので、加えていない。

正本のデータの外の変更（2026-11-17、[law-of-japan/loj-spec#138](https://github.com/law-of-japan/loj-spec/issues/138)）は、CIの設定（`.github/workflows/validate.yml`）だけを加える`auxiliary`の正例（common-050）と、記録訂正と同じcommitでCIの設定を変える`correction`の正例（common-051）と、`auxiliary`と宣言して`history.yaml`のRevisionのラベルを変える負例（common-052）と、L1が不合格の版（HEAD-01）を持つリポジトリにCIの設定を加える`auxiliary`の正例（common-053）がある。common-051は、正本のデータの外のファイルの変更がどの種類の検査の対象にもならないこと（CHG-01）を示す。common-052は、`auxiliary`の検査（正本のデータのファイルが一致すること）の違反で、CHG-02の規則で報告する。common-053は、`auxiliary`がASTを比べないので、`metadata`のcommon-025と違い、CHG-04の判定不能にならず合格する。`versions/`の下に版パッケージ以外のファイル（説明の文書）を加える`auxiliary`の負例（common-054）は、`versions/`の下のすべてのファイルが正本のデータのファイルであること（CHG-01）と、ファイルの追加が一致の検査に反すること（CHG-02）を示す。登録台帳のリポジトリ（`space.yaml`、`records/`）の`auxiliary`のケースは、加えていない。登録台帳の`git bundle`が要るためである（上のCHG-02・CHG-03の従属するファイルの項と同じ）。`LoJ-Revisions`を書いた`auxiliary`が合格すること（CHG-03の「書いても、検査の結果を変えない」）は、正例（common-055）が当たる。`rebuild.yaml`を変える`auxiliary`、正本のデータのファイルのパスだけを変える（改名する）`auxiliary`、ファイルのモードだけを変える`auxiliary`は、common-052・054と同じ一致の検査（CHG-02の表の`auxiliary`の行）の範囲なので加えていない。どのファイルも変えない`auxiliary`のcommit（空のcommit）は、正本のデータのファイルが一致する入力の一つで、common-050と同じ文の範囲なので加えていない。

正本のデータのファイルのGitのモード（2026-11-20、[law-of-japan/loj-spec#147](https://github.com/law-of-japan/loj-spec/issues/147)、CHG-02）は、一つの版を加えた後、版の本文のファイル（`main.md`）のモードだけを`100755`にする`format`の負例（common-057）と、それを`100644`に戻す`format`の正例（common-056）と、同じ戻しを`metadata`と宣言する負例（common-058）がある。common-057は、`format`の範囲の中のファイルだが、モードが`100644`でない。common-056は、親のcommit（common-057のhead）が不合格でも、そのcommitが変えたファイルのモードだけを確かめるので合格する。common-058は、残るモードは`100644`だが、`metadata`の範囲の外の版パッケージのファイルのモードだけを変えた違反である。バイト列は、三つのcommitを通じて変わらない。`history.yaml`のモードを変える`format`、宣言していない版のファイルのモードを変える`correction`は、common-058と同じ文（範囲の外の変更）の範囲なので加えていない。シンボリックリンク（`120000`）・サブモジュール（`160000`）を置くcommitは、common-057と同じ文（`100644`でないモード）の範囲なので加えていない。期待する規則と結果もcommon-057と同じで、モードの値のほかに比べるものがない。変えていないファイルの誤ったモードを確かめないことは、common-056が当たる。最初のcommit（変更前の記録版がなく、すべての正本のデータのファイルのモードを確かめる場合）は、下のcommon-061が当たる。

最初のcommit（2026-11-20、[law-of-japan/loj-spec#149](https://github.com/law-of-japan/loj-spec/issues/149)、CHG-02・CHG-03）は、適合ケースの索引の変更の入力で`base`を省き、親のないcommitを`head`として検査する。`revisionAdd`の最初のcommitの正例（common-059。common-004の`git bundle`の最初のcommit）と、同じファイルを置いて`format`と宣言する負例（common-060。CHG-03）と、`revisionAdd`と宣言して版の本文のファイル（`main.md`）を`100755`で置く負例（common-061。CHG-02）がある。三つの最初のcommitは、正本のデータのファイルのバイト列が同じで、宣言とモードだけが違う。common-060は、範囲の外の変更（`format`の範囲にない`history.yaml`の追加）にも当たるが、`revisionAdd`でない最初のcommitは種類ごとの検査をせずに不合格とする（CHG-03）ので、期待する規則はCHG-03だけである。`base`を省いて二つ以上のcommitを順に検査するケース、正本のデータのファイルを含まない最初のcommit（例: `auxiliary`と宣言してREADMEだけを置く）のケースは、加えていない。前者は、各commitを単独で検査する（CHG-03）ので、最初のcommitのケースと、`base`を置く既存のケースの組で足りる。後者は、common-060と同じ文（`revisionAdd`でない最初のcommit）の範囲で、期待する規則と結果も同じである。`revisionAdd`でない最初のcommitに`100755`のファイルを置くケースも加えていない。そのcommitではモードを確かめず、CHG-03だけで報告する（CHG-02・CHG-03）が、期待結果に挙げない診断は加わってもよい（CONF-01）ので、ケースはcommon-060と区別できない。

最初のcommitの範囲と登録台帳の最初のcommit（2026-11-24、[law-of-japan/loj-spec#152](https://github.com/law-of-japan/loj-spec/issues/152)、CHG-02・CHG-03）は、次のケースがある。
- 法令リポジトリの最初のcommitが`history.yaml`のファイルの全体を作ることは、`revisionAdd`の範囲に入る（CHG-02）。common-059の最初のcommitが`history.yaml`を作り、合格することで確かめる。`rebuild.yaml`を置く最初のcommitのケースは加えていない。同じ文の範囲で、再構築報告の内容の検査は変更検査の外（loj-rebuild）にある。
- 登録台帳のリポジトリの最初のcommit（索引の変更の入力の`repository: registry`）で、`space.yaml`と一つのRecordのファイルを置く`metadata`の正例（common-062）と、同じファイルを置いて`revisionAdd`と宣言する負例（common-063。CHG-03）がある。二つのcommitは、正本のデータのファイルが同じで、宣言だけが違う。登録台帳の最初のcommitで、`100755`のファイルを置くケースは加えていない。モードの確かめはリポジトリの種類によらない同じ文（CHG-02）で、common-061と同じ検査になる。
- リポジトリの別をファイルから推定しないこと（CHG-03）は、`space.yaml`も`history.yaml`も置かず、説明のファイル（`README.md`）だけを置く登録台帳の最初のcommitを`metadata`と宣言する正例（common-064）で確かめる。別を索引の`repository: registry`から受け取れば合格し、ファイルから法令リポジトリと推定すれば`revisionAdd`でない最初のcommitとして不合格になる。正本のデータのファイルを変えないcommitは`auxiliary`とする（CHG-01）が、最初のcommitは除き、CHG-03の最初のcommitの種類とする（CHG-01のただし書き）ので、合格である。common-062・063は、登録台帳のファイルを持つので、推定しても同じ結果になる。

旧リポジトリのcommitの上に始めた正本ブランチ（2026-11-24、[law-of-japan/loj-spec#163](https://github.com/law-of-japan/loj-spec/issues/163)、CHG-02・CHG-03）は、宣言のない二つの旧commitの上に、`revisionAdd`の最初のcommit（`history.yaml`の全体を作る）と`correction`のcommitを置いた`git bundle`で、次のケースがある。
- 索引の変更の入力の`legacyBoundary`に二つ目の旧commitを与え、`base`を省く正例（common-065）。旧履歴のcommitを検査せず、境界の子を最初のcommitとして、最初のcommitの範囲で検査する。
- `base`に一つ目の旧commit（旧履歴のcommit）を与える正例（common-066）。common-065と同じく、境界の子から検査する。
- 同じ`git bundle`の写しで、境界を与えない負例（common-067。CHG-02・CHG-03）。親のないcommitが最初のcommitになり、二つの旧commitが宣言のないcommitとしてCHG-03で、`revisionAdd`のcommitが変更前の記録版を持つので、`history.yaml`の最上位のフィールドを作る範囲の外の変更としてCHG-02で不合格になる。境界をファイルやtrailerの有無から推定しないこと（CHG-03）を確かめる。
- `head`そのものを境界として与える負例（common-068。CHG-03）。境界の条件に合わない入力は、各commitを検査せずに不合格とする。
- 境界の子を`format`と宣言する負例（common-069。CHG-03）。common-060と同じく、`revisionAdd`でない最初のcommitである。
- 加えていないケース: 旧履歴にmergeのcommitを含むもの（旧履歴のcommitを報告しない同じ文の範囲で、common-065と同じ結果になる）、`head`から到達できない境界・登録台帳のリポジトリに与えた境界（common-068と同じ文の範囲）、境界の木に正本のデータのファイルの名前のファイルがあるもの（境界の木と比べない同じ文の範囲）、`rebuild.yaml`を置く最初のcommit（上の#152の項と同じ）。

TIME-03は、hist-004、hist-015〜018のほか、`pending`を基準とする`derived`に`value`を書いた負例（hist-044）と、`value`の書式（`YYYY-MM-DD`）に反する負例（hist-045）がある。`calc`のない`derived`の`value`を検査せず、結果を未完了にしないこと（2026-11-16、[law-of-japan/loj-spec#136](https://github.com/law-of-japan/loj-spec/issues/136)）は、`calc`のない施行の時点を持ち、L3（履歴構造）の合格を期待するhist-001が当たる。警告を出すかは任意（MAY）なので、警告は期待結果に挙げない。

フィールドの改名（2026-11-12、[law-of-japan/loj-spec#29](https://github.com/law-of-japan/loj-spec/issues/29)）は、改めたschemaで正例のYAMLを検査して確かめる。`law.yaml`の`sourceUris`（旧`sources`）は任意のフィールドで、使用例の正例（pkg-233）を2026-11-25に加えた。`sourceUris`はASTに現れないので、期待結果のASTは置かない場合（pkg-001）と同じである。旧名は閉じたschemaにより未知のフィールドとして拒否されるが、旧名を使う負例は加えていない（未知のフィールドの負例は、Manifestのpkgのケースと、Revisionのhist-005にある）。

規則の正の整理（2026-11-12、[law-of-japan/loj-spec#30](https://github.com/law-of-japan/loj-spec/issues/30)）で、二つの規則の正が変わった。改正法の附則を版パッケージに写さない規則（HIST-03からBASIC-03へ）と、L0・L1で文字の存在を違反にしない規則（版パッケージの検査の章からBASIC-02へ）である。前者は原典と比べないと確かめられず、後者は違反を出さないことの定めなので、どちらも負例を作れない。後者は、互換漢字・異体字セレクタを含む正例（pkg-106等）がL0・L1に合格することで確かめる。

## 要件の名宛人と確かめ方

2026-11-12、[law-of-japan/loj-spec#31](https://github.com/law-of-japan/loj-spec/issues/31)の結論による一覧である。参考であり、要件の本文が正である。要件の本文には区分を書かない（本文と区分が食い違う経路を増やさないため）。一つの要件に性質の違う要求が混ざる場合は、行を分け、「対象」の列に該当する文を示す。

- 名宛人: **データ**（入力の法令データ・登録台帳・再構築報告と、正本のcommitが満たす）／**入力者**（データを作る人の作業と判断）／**実装**（検査器・生成器・表示器。種類を括弧で示すことがある）／**利用者**（検査の結果を使って適合を主張する者）／**仕様の資料**（本リポジトリの文書・schema・適合ケース）。
- 確かめ方: **機械検査**（入力のデータを検査器が判定する。規則は診断になる。括弧の中は報告する検査）／**原典照合**（原典と比べて確かめる。L3の原典照合は予約であり、本版では診断にならない）／**レビュー**（PRのレビュー、作業の記録、公開の手順、実装のコードと適合の主張の文面の確認で、人が確かめる。診断にならない）／**適合ケース**（実装の挙動を、固定した入力と期待結果で確かめる）／**実装の試験**（実装の内部の挙動。本リポジトリの固定データでは表せず、実装の側で確かめる。[CONF-02](../spec/common/v1alpha1/04-conformance.md)）／**予約**（区分が予約であり、本版では確かめない）。仕様の資料の機械検査は、検査器ではなく`scripts/verify.py`が行う。
- 適合レベルの合格は、機械検査の行だけを示す。原典照合・レビュー・実装の試験の行を満たすことは、合格に含まれない（CONF-02）。

| 要件 | 対象 | 名宛人 | 確かめ方 |
|---|---|---|---|
| CORE-01 | 正本ブランチの履歴を書き換えない | 入力者 | レビュー（mergeのcommitはCHG-03の変更検査） |
| CORE-02 | schemaVersionの宣言、閉じたschema、時点値で表すこと | データ | 機械検査（各系列の01、各ファイルの検査） |
| CORE-02 | 知らない版として読まない。表示用の値を根拠・順序・同定に使わない | 実装 | 適合ケース、実装の試験 |
| CORE-03 | 全体 | データ | 機械検査（MAN-01、各系列の01） |
| CORE-04 | 全体 | 仕様の資料 | レビュー（版の状態の表の形は`verify.py`が検査する） |
| CORE-05 | 対応表 | 仕様の資料 | レビュー |
| CORE-05 | 対応表にない組み合わせの扱い | 実装 | 実装の試験（処理不能の扱いはVAL-04） |
| CHAR-01 | 原典の文字の区別を保ってコードポイントを選ぶ | 入力者 | 原典照合 |
| CHAR-01 | コードポイント列を保持し、正規化しない | 実装 | 適合ケース（pkg-106） |
| CHAR-02〜CHAR-04 | 全体 | 入力者、実装 | 原典照合 |
| CHAR-05 | 全体 | 実装 | 実装の試験 |
| VAL-01、VAL-06、VAL-08 | 定義 | 仕様の資料 | レビュー |
| VAL-02、VAL-04、VAL-07 | 結果と診断の報告 | 実装 | 適合ケース |
| VAL-03 | 対象の記録版の記録 | 実装 | 実装の試験 |
| VAL-03 | 登録空間の入力によるRecordRefの解決（入力と異なる`space`） | データ | 適合ケース（L4、登録台帳の検査） |
| VAL-03 | 登録空間の入力がない場合の判定不能 | 実装 | 実装の試験 |
| VAL-05 | 区分ごとの判定と報告 | 実装 | 適合ケース |
| VAL-05 | 区分を付けずにL3合格と主張しない | 実装 | レビュー |
| SRCM-01 | 全体 | 実装 | 原典照合 |
| CONF-01 | 索引・期待結果の形 | 仕様の資料 | 機械検査（`verify.py`） |
| CONF-01 | ケースを満たす条件 | 実装 | 適合ケース |
| CONF-01 | 期待結果を規範の本文から定め、規範の判定を行う処理の出力から作らない | 仕様の資料 | レビュー |
| CONF-01 | 資料の管理の情報（`rejectedBy`、`derivedFrom`）は判定を変えず、実装は読まなくてよい | 実装 | 実装の試験 |
| CONF-02 | レベルごとのケースの成功、結果の集計 | 実装 | 実装の試験（実装の適合の宣言は本仕様では定めない） |
| CONF-02 | 合格を、機械で検査しない要求を満たしたことの主張に使わない | 実装、利用者 | レビュー |
| TYPE-01 | 形、登録空間とRecord IDの組で指すこと | データ | 機械検査（その型を使うファイルの検査） |
| TYPE-01 | 発行したRecord IDで指し、仮の値（`unregistered`等）を置かない | 入力者 | レビュー（仮の値はRecord IDの文字種に合うことがあり、機械では区別できない。登録台帳にないIDは関係の解決（L4）で未取得と報告され、違反にならない） |
| TYPE-03〜TYPE-05、TYPE-08 | 全体 | データ | 機械検査（その型を使うファイルの検査） |
| TYPE-02 | Sourceの形、`glyphPreservation`、`fixed`の形 | データ | 機械検査（同上） |
| TYPE-02 | 旧形式のURIを自動で根拠に認定しない | 入力者 | レビュー |
| TYPE-06 | Scopeの形 | データ | 機械検査（同上） |
| TYPE-06 | `text`を原文のまま記録する | 入力者 | 原典照合 |
| TYPE-07 | Scopeとノードの照合 | データ | 機械検査（L3根拠） |
| TYPE-07 | 照合の補助だけで`nodes`を確定しない | 入力者 | レビュー |
| TIME-01、TIME-03、TIME-04、TIME-06、TIME-07 | 全体 | データ | 機械検査（その型を使うファイルの検査） |
| TIME-02 | 形と原表記の保存 | データ | 機械検査（同上） |
| TIME-02 | 暦や精度が不明な値を推定で`date`にしない | 入力者 | 原典照合 |
| TIME-05 | 確認した範囲を書く（SHOULD） | 入力者 | レビュー |
| CHG-01〜CHG-04 | 正本のcommit | データ | 機械検査（変更検査） |
| CHG-05 | 全体 | 実装 | レビュー |
| FIXREF-01〜FIXREF-02、FIXREF-04 | 参照の形 | データ | 機械検査（参照の解決） |
| FIXREF-03、FIXREF-05〜FIXREF-07 | 参照の解決 | 実装 | 適合ケース |
| FIXREF-07 | 最新で同じIDのノードを示す補助（MAY） | 実装 | 実装の試験 |
| VIEW-01、VIEW-05〜VIEW-07 | 生成器 | 実装 | 実装の試験 |
| VIEW-02 | 除いた版等の存在と、選択規則と、表の内容（除いた版のrevision_idと理由、列に含めた版の施行時点の原表記・条件の原文・併存する版のrevision_id・後の段階施行の施行時点のRevisionと施行の範囲の原文）を示す | 実装 | 実装の試験（除いた版、列に含めた確定日でない版・適用の条件がある版・併存する版のある版・後に段階施行の施行時点がある版を含む記録版から生成し、ビューに選択規則と、表の各行の内容があることを確かめる。適用の条件が複数ある版では、すべての条件の原文があること、併存する版を除いた場合は除いた版としても示されること、起点どうしと`basedOn`が`unknown`の版どうしを併存する版として示さないこと、後の段階施行の施行時点を、`basedOn`を辿って到達する版に示し、分岐した別の版には示さないことを確かめる。段階施行の記録版の入力には、hist-062（起点と、後の施行時点のRevision）を使える。ビューの形式によらない） |
| VIEW-02 | 一本の列を明示した選択規則による並べ方とし、現行の一意性・網羅性・適用関係を主張しない | 実装 | 実装の試験（表示の文言と、先頭を「現行」と表示する条件を確かめる） |
| VIEW-03 | 生成元の記録 | 実装 | 実装の試験（生成したビューの各単位から、記録した正本のcommitと版パッケージのパスをたどって版パッケージがあること、記録した生成器の版で再生成して同じ単位になることを確かめる。ビューの形式によらない） |
| VIEW-03 | 決定性、法的な日付を作成の日時に使わない | 実装 | 実装の試験 |
| VIEW-04 | 派生ビューの単位（commit等）を固定参照として案内しない | 実装 | 実装の試験 |
| XREF-01〜XREF-03、XREF-05、XREF-06 | 全体 | データ | 機械検査（L4） |
| XREF-04 | 全体 | データ | 予約 |
| BASIC-01、BASIC-04 | 全体 | データ | 機械検査（L0・L1） |
| BASIC-02 | 入力のバイト | データ | 機械検査（L0） |
| BASIC-02 | 文字の存在を違反にしない（位置の数え方はSRC-01、元の入力の保持はSRC-02） | 実装 | 適合ケース |
| BASIC-03 | `unsupportedFeatures`の申告がある版を不合格とする（申告の有無だけを判定する） | データ | 機械検査（L1） |
| BASIC-03 | 未対応の構造を`unsupportedFeatures`に記録する（申告の漏れ） | 入力者 | 原典照合。機械で認識できる構造は、DISP-01等の違反としてL1で現れる |
| BASIC-03 | 未表現の構造を本文に隠さない。改正法の附則を写さない | 入力者 | 原典照合 |
| BASIC-03 | 参考の集計（MAY）と、それを適合の主張に使わないこと | 実装 | レビュー |
| MAN-01〜MAN-03 | 全体 | データ | 機械検査（L0・L1。`law.id`とRecord IDの一致はHIST-02） |
| MD-01、MD-03 | 全体 | データ | 機械検査（L1） |
| MD-02 | 本文に保持するもの。リストの番号から項を作らない | 実装 | 適合ケース |
| MD-02 | 表示器が意味を変えない | 実装 | 実装の試験 |
| MD-04 | 全体 | 入力者 | 原典照合 |
| HEAD-01〜HEAD-04、NUM-01、DIR-01、DIR-02、DISP-01、AST-01、AST-02、ID-01、PARA-01、TABLE-03、TABLE-04、PRE-01、PRE-02 | 全体 | データ | 機械検査（L1） |
| TABLE-04 | 原典の表が矩形でないときに申告し、セルや結合を足さない | 入力者 | 原典照合 |
| PARA-02 | 属性と見出しの行の形、見出しの行の後の本文の行 | データ | 機械検査（L1） |
| PARA-03 | 二つの形式の混在、ファイルの数、分類・条・項のどれもない本則 | データ | 機械検査（L1） |
| PARA-03 | 原典にない条・項の番号を補わない | 入力者 | 原典照合 |
| AMEND-01 | マーカー、改正規定の中の順序と番号、改正内容のない改正規定 | データ | 機械検査（L1） |
| AMEND-01 | 改正内容を改正法自身の条・項・表として書かない。改正内容をマーカーで囲まずに本文として書かない。原典にない改正の指示の文を補わない。原典に指示の文がある改正規定に`instruction=implicit`を書かない。掲げた規定の範囲 | 入力者 | 原典照合 |
| AMEND-02 | 全体 | データ | 機械検査（L1） |
| AMEND-03 | 未対応の改正規定の申告 | 入力者 | 原典照合 |
| AMEND-03 | 改正の指示の文を構造と推測しない | 実装 | 適合ケース |
| LIST-01 | 列記の順序（`number`の連番） | データ | 機械検査（L1） |
| LIST-01 | 法令の列記をマーカーで囲まずに本文として書かない。番号のない列挙を号として書かない | 入力者 | 原典照合 |
| LIST-02 | 号・細分と列記の混在 | データ | 機械検査（L1） |
| LIST-02 | 未対応の列記（入れ子の列記、段に分けた列記）の申告 | 入力者 | 原典照合 |
| PARA-02 | 原典の見出しを書くこと、見出しのない項に属性を書かないこと、続く項にかかる見出しを最初の項にだけ書くこと | 入力者 | 原典照合 |
| PARA-02 | 属性のない項の本文の行を見出しと推測しない | 実装 | 適合ケース |
| HEAD-01、HEAD-04 | 見出しのレベル・語の出現から所属・削除を推論しない | 実装 | 適合ケース |
| SRC-01 | 診断の位置 | 実装 | 適合ケース |
| SRC-02 | 全体 | 実装（ファイルを書き出す機能） | 実装の試験 |
| ID-02 | IDの保持 | データ | 機械検査（L1。ID-01で満たされる） |
| ID-02 | 重複を自動の連番で解消しない | 実装 | 適合ケース |
| REF-01 | 全体 | 実装 | 適合ケース |
| TABLE-01 | 表のマーカーと`number` | データ | 機械検査（L1） |
| TABLE-01 | 法令の表を箇条書き等で書かない | 入力者 | 原典照合 |
| TABLE-02 | `key`の形と一意性 | データ | 機械検査（L1） |
| TABLE-02 | 削った`key`の再使用 | データ | 機械検査（L3履歴構造、HIST-13） |
| TABLE-02 | 既存の行の`key`の維持、ランダムに選ぶ（連番、内容・位置・順序から計算する方式を使わない）、衝突を確かめる | 入力者 | レビュー |
| TABLE-03 | 続く欄を結合で書く。空の欄をコメント等で埋めない | 入力者 | 原典照合 |
| TOC-01 | 位置と中身の形 | データ | 機械検査（L1） |
| TOC-01 | 目次を構造として解析しない | 実装 | 適合ケース |
| HIST-01〜HIST-03、HIST-05〜HIST-10、HIST-12、HIST-13、REV-01、REV-03 | 形、参照、整合 | データ | 機械検査（L3履歴構造） |
| HIST-05 | 段階施行の法令の版パッケージに本文の全体を書き、未施行の規定を除かない | 入力者 | 原典照合 |
| HIST-01、HIST-11、REV-02 | 表示用の値・Revisionの数を、解決・同一性・網羅性に使わない | 実装 | 実装の試験 |
| HIST-04 | 順序を推測や法令番号で補わない | 入力者 | レビュー |
| HIST-07 | 時点照会（適用関係の形の検査は、機械検査（L3履歴構造）の行）で日付だけから一つのRevisionを決めない。`unsurveyed`を条件なし・適用なしと扱わない | 実装 | 実装の試験（時点照会の結果を規範にしないので、適合ケースを加えない） |
| HIST-08 | 確認の状況を`locator`に書かない | 入力者 | レビュー |
| REV-01 | ランダムに発行し（連番、時刻を含む方式、情報や発行の順序から計算する方式を使わない）、衝突を確かめる | 入力者 | レビュー |
| REV-04 | 版の粒度 | 入力者 | 原典照合 |
| GLYPH-01、GLYPH-04、GLYPH-05、GLYPH-11 | 全体 | データ | 機械検査（L3根拠） |
| GLYPH-04 | ASTを変える変更で、注記が指す字を確かめ直し、同じcommitで更新する | 入力者 | レビュー（解決できない・一致しない注記はL3根拠で機械検査。偶然同じ字の別の位置への対応は原典照合） |
| GLYPH-02 | 〓の注記、本文だけで状態を表さないこと | データ | 機械検査（L3根拠） |
| GLYPH-02 | 注記すべき字に当たるか | 入力者 | 原典照合 |
| GLYPH-03、GLYPH-06〜GLYPH-09 | 全体 | 入力者 | 原典照合 |
| GLYPH-10 | `verified`のSourceの条件 | データ | 機械検査（L3根拠） |
| GLYPH-10 | 照合したこと。注記の数から推論しない | 入力者、実装 | 原典照合、レビュー |
| REG-01〜REG-05、RID-02、RID-04、RID-05 | 形、参照、一意性 | データ | 機械検査（登録台帳の検査） |
| REG-02、REG-03 | `notCollected`から不存在を推論しない。番号の一致で同一と判断しない | 実装 | 実装の試験 |
| REG-03 | `raw`を原表記のまま書く。所管から逆算しない | 入力者 | 原典照合 |
| REG-05 | 外部の収録の単位がRecordと一致すると仮定しない | 入力者 | レビュー |
| RID-01 | 発行の方法（ランダム。連番、時刻を含む方式、情報や登録の順序から計算する方式を使わない。仮登録でIDを変えない） | 入力者 | レビュー（形はRID-02で機械検査） |
| RID-01 | 登録台帳の中のIDの衝突（別名と大小文字の違いを含む） | データ | 機械検査（登録台帳の検査） |
| RID-03 | 全体 | 実装 | 実装の試験 |
| RID-05 | 凍結したリポジトリを削除しない | 入力者 | レビュー |
| REB-01〜REB-08 | 全体 | 入力者 | レビュー（結果は再構築報告と履歴マニフェストの機械検査で一部を確かめる。本文の出どころは原典照合） |
| REBR-01、REBR-02、REBR-04 | 形と参照 | データ | 機械検査（再構築報告の検査） |
| REBR-03 | `sourceChecks`の形 | データ | 機械検査（再構築報告の検査） |
| REBR-03 | `preserved`でない資料から起こした本文を原典どおりと主張しない | 入力者 | レビュー |
| REBR-05 | 差の記録の形 | データ | 機械検査（再構築報告の検査） |
| REBR-05 | 原因が分かるまで旧データの誤りと決めつけない | 入力者 | レビュー |

[規範仕様の入口](../spec/README.md)の要件IDを持たない規則（要件IDの付け方、版の状態、タグ）は、仕様の資料の管理の規則であり、名宛人は仕様の資料、確かめ方はレビューと`verify.py`の表の検査である。

## 条件の外で禁止するフィールド

2026-11-16、[law-of-japan/loj-spec#83](https://github.com/law-of-japan/loj-spec/issues/83)による一覧である。参考であり、要件の本文とschemaが正である。

[要求レベル](../spec/README.md#要求レベル)により、フィールドの表の「〜で必須」「条件付き」は、条件を満たすときのMUSTだけを表し、条件の外で置いてよいかは導かない。禁止する場合は要件の本文に書く。この表は、草案の版のschemaが`if`/`then`/`else`で条件の外のフィールドを禁止している箇所と、その禁止を書いた本文の要件を対応させる。

- 「位置」は、禁止を書いた`then`・`else`のJSON Pointerである。「本文の要件」は禁止を書いた要件、「本文になし」は禁止の文が本文にないフィールドである。どの文が禁止に当たるかは人の判断であり、`verify.py`は確かめない。
- `verify.py`は、schemaから抽出した位置とフィールドがこの表の行と一致することを検査する（一致しなければ失敗）。「本文になし」のフィールドと、「本文の要件」の節に名前が現れないフィールドは、警告として挙げる。警告は仕様の欠陥であり、本文とschemaのどちらに合わせるかを決めて直す。
- `then`・`else`の直下とその`allOf`の中で、`not`の`required`（一つのフィールド）、その`anyOf`、`properties`の`false`（または`{not: {}}`）を禁止として読む。そこにほかの形の`not`があれば失敗とする。`then`・`else`の中の`anyOf`・`oneOf`の下と、`$ref`の先は読まない。
- 警告がないことは、挙げた要件の節にフィールドの名前があることだけを示し、その文が禁止であることは示さない。

| schema | 位置 | 条件 | 禁止するフィールド | 本文の要件 | 本文になし |
|---|---|---|---|---|---|
| `common/v1alpha1/conformance.schema.json` | `/properties/cases/items/allOf/1/else` | `check`がL3・L4でない | `category` | CONF-01 | — |
| `common/v1alpha1/expected.schema.json` | `/properties/results/items/allOf/0/else` | `check`がL3・L4でない | `category` | CONF-01 | — |
| `common/v1alpha1/report.schema.json` | `/properties/results/items/allOf/0/else` | `check`がL3・L4でない | `category` | CONF-01 | — |
| `common/v1alpha1/types.schema.json` | `/$defs/TimePoint/allOf/1/then` | `state: date` | `base`、`calc`、`rule` | TIME-01 | — |
| `common/v1alpha1/types.schema.json` | `/$defs/TimePoint/allOf/5/else` | `state`が`derived`でない | `base`、`calc`、`rule` | TIME-01 | — |
| `common/v1alpha1/types.schema.json` | `/$defs/TimePoint/allOf/6/then` | `state: pending` | `determinedBy`、`value` | TIME-01 | — |
| `common/v1alpha1/types.schema.json` | `/$defs/TimePoint/allOf/7/then` | `state`が`unknown`・`notApplicable` | `raw`、`value` | TIME-01 | — |
| `loj-history/v1alpha1/history.schema.json` | `/properties/revisions/items/properties/applicability/allOf/0/else` | `state`が`conditions`でない | `conditions` | HIST-07 | — |
| `loj-history/v1alpha1/history.schema.json` | `/properties/revisions/items/properties/text/properties/correctionsSurveyed/allOf/0/then` | `state: surveyed` | `reason` | HIST-08 | — |
| `loj-history/v1alpha1/history.schema.json` | `/properties/revisions/items/properties/text/properties/correctionsSurveyed/allOf/1/then` | `state: unsurveyed` | `evidence` | HIST-08 | — |
| `loj-history/v1alpha1/history.schema.json` | `/properties/revisions/items/properties/text/allOf/0/else` | `status`が`complete`・`partial`でない | `glyphCheck`、`glyphNotes`、`package`、`sources` | HIST-08 | — |
| `loj-history/v1alpha1/history.schema.json` | `/properties/revisions/items/properties/text/allOf/1/else` | `status`が`partial`でない | `gaps` | HIST-08 | — |
| `loj-history/v1alpha1/history.schema.json` | `/properties/revisions/items/properties/text/allOf/2/then` | `status: absent` | `correctionsSurveyed`、`variances` | HIST-08 | — |
| `loj-history/v1alpha1/history.schema.json` | `/properties/revisions/items/allOf/0/then` | `origin`を持つ | `basedOn`、`basis` | HIST-04、HIST-05 | — |
| `loj-history/v1alpha1/history.schema.json` | `/properties/revisions/items/allOf/1/else` | `origin`が`totalRevision`でない | `totallyRevises` | HIST-04 | — |
| `loj-history/v1alpha1/history.schema.json` | `/properties/revisions/items/allOf/2/else` | `status`が`merged`・`split`でない | `replacedBy` | HIST-10 | — |
| `loj-history/v1alpha1/history.schema.json` | `/properties/termination/items/allOf/0/then` | `type`が`repealed`・`totallyRevised` | `effective`、`evidence`、`verification` | HIST-12 | — |
| `loj-history/v1alpha1/history.schema.json` | `/properties/termination/items/allOf/0/else` | `type`が`repealed`・`totallyRevised`でない | `relation` | HIST-12 | — |
| `loj-rebuild/v1alpha1/rebuild.schema.json` | `/properties/differences/items/allOf/4/else` | `class`が`glyph`でない | `count`、`examples` | REBR-05 | — |
| `loj-registry/v1alpha1/record.schema.json` | `/allOf/1/else` | `status`が`merged`・`split`でない | `replacedBy` | REG-02 | — |
| `v1alpha2/ast.schema.json` | `/$defs/node/allOf/0/else` | `kind`が`Article`でない | `status` | AST-01 | — |
| `v1alpha2/ast.schema.json` | `/$defs/node/allOf/1/else` | `kind`が`Subitem`でない | `level` | AST-01 | — |
| `v1alpha2/ast.schema.json` | `/$defs/node/allOf/3/else` | `kind`が`Paragraph`でない | `numbering` | AST-01 | — |
| `v1alpha2/ast.schema.json` | `/$defs/node/allOf/4/else` | `kind`が`Row`でない | `key` | AST-01 | — |
| `v1alpha2/ast.schema.json` | `/$defs/node/allOf/5/else` | `kind`が`Cell`でない | `colspan`、`rowspan` | AST-01 | — |
| `v1alpha2/ast.schema.json` | `/$defs/node/allOf/7/else` | `kind`が`Paragraph`でない | `caption` | AST-01 | — |
| `v1alpha2/ast.schema.json` | `/$defs/node/allOf/9/else` | `kind`が`Amendment`でない | `instruction` | AST-01 | — |
