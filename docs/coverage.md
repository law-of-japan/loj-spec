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
| [conformance/v1alpha2](../conformance/v1alpha2/manifest.json) | pkg-001〜124 | v1alpha1の106件を写したもの（pkg-001〜106）と、「條」「ノ」「附　則」、無番号の項、表、前文・制定文とその違反（pkg-107〜124） |
| [conformance/loj-history/v1alpha1](../conformance/loj-history/v1alpha1/manifest.json) | hist-001〜015 | 祝日法の制定時と最初の改正後の版、履歴だけの法令リポジトリ三つ、その違反 |
| [conformance/loj-glyphs/v1alpha1](../conformance/loj-glyphs/v1alpha1/manifest.json) | glyph-001〜009 | 祝日法の字体注記と、その違反。L1が不合格の版の字体注記（未完了） |
| [conformance/loj-registry/v1alpha1](../conformance/loj-registry/v1alpha1/manifest.json) | reg-001〜008 | 三つのRecordの登録台帳と、その違反 |
| [conformance/loj-rebuild/v1alpha1](../conformance/loj-rebuild/v1alpha1/manifest.json) | rebuild-001〜004 | 祝日法の再構築報告と、その違反 |
| [conformance/common/v1alpha1](../conformance/common/v1alpha1/manifest.json) | common-001〜012 | L4の時点の整合（T-04）、変更検査、固定参照（`git bundle`の架空の履歴） |

`scripts/verify.py`は、すべての索引・期待結果・正例の入力の形と、要件IDの存在を検査し、v1alpha2の正例のASTを原文と突き合わせる。v1alpha2のL1の負例と、L3・L4・登録台帳・再構築報告・変更検査・固定参照のケースの合否は判定しない。検査器で判定する。

### ケースのない要件

次の要件にはケースを作らない（検査の対象外）。

| 要件 | 理由 |
|---|---|
| CORE-01〜05、CHAR-02〜05、VIEW-01〜07 | データの構成・作業・派生処理の制約であり、一つの入力の成否として検査できない。CORE-03（YAML）の違反は各系列の01で、CHAR-01はpkg-106で確かめる |
| CONF-01〜03、VAL-01、VAL-03、VAL-05、VAL-07、VAL-08 | 適合の主張とケースの契約そのもの。資料の監査とレビューで確かめる |
| REB-01〜08 | 再構築の作業の手順。結果は再構築報告（REBR）と履歴マニフェストのケースで確かめる |
| SRCM-01、XREF-04 | 予約の区分 |
| GLYPH-03、GLYPH-07、GLYPH-08 | 本文に置く字の選び方は原典と比べないと判定できない（原典照合） |
| RID-03、REV-02 | リポジトリの名前と可読ラベルは参照の解決に使わない、という制約 |
| TABLE-02の一部（既存の行の`key`の維持、基礎の版の同じ行が同じ`key`を持つこと） | 行の同一性は法的な判断であり、機械では確かめられない。入力者への要件とする（2026-11-12、[law-of-japan/loj-spec#23](https://github.com/law-of-japan/loj-spec/issues/23)） |

[規範仕様の入口](../spec/README.md#版の状態)の版の状態の定め（要件IDなし）にも、ケースを作らない。仕様の資料そのものの管理の規則であり、法令の入力の成否として検査できないためである。状態の表の形は`scripts/verify.py`が検査する。タグを打つことは、公開の手順（[CONTRIBUTING](../CONTRIBUTING.md)）で確かめる。

次の要件は機械で検査できるが、まだケースがない。今後加える: TIME-02、TIME-05、TIME-06、TYPE-01〜04、TYPE-06、HIST-09、CHG-04、CHG-05、RID-04、RID-05。

CHG-02・CHG-03（2026-11-12、[law-of-japan/loj-spec#18](https://github.com/law-of-japan/loj-spec/issues/18)）の従属するファイルの更新は、記録訂正で同じ版の`text.sources`を更新する正例（common-024）だけがある。common-024は、宣言した版だけのASTが変わり、従属する更新が宣言した版の`text.sources`に限られ、宣言した版の根拠（`text.sources`の箇所）があるので合格とする。Scopeの`nodes`・字体注記の更新、宣言していない版の従属するファイルを変える負例、登録台帳だけの`metadata`、mergeのcommit、最初のcommit、revertのcommitのケースは、まだない。登録台帳の`git bundle`と、親が二つのcommitを持つ`git bundle`が要るためである。

HIST-12の撤回した関係・内訳の扱い（2026-11-12、[law-of-japan/loj-spec#46](https://github.com/law-of-japan/loj-spec/issues/46)）は、撤回した関係を根拠とする負例（hist-034）、内訳をすべて撤回した関係を根拠とする負例（hist-035）、内訳の一部を撤回した関係を根拠とする正例（hist-036）がある。撤回の後に`termination`の項目を別の関係に置き換える変更のケースは、まだない。

HIST-13（2026-11-12、[law-of-japan/loj-spec#23](https://github.com/law-of-japan/loj-spec/issues/23)）は、削った行の`key`を使わずに行を加える正例（hist-031）と、削った`key`を後の版で再使用する負例（hist-032）と、本文が一部しかない版を挟んで飛ばす正例（hist-033）がある。本文のない版・L1が不合格の版を挟む場合、`basedOn`が分岐する場合と、表の番号が変わる場合のケースは、まだない。glyph-004（行の`key`を変えて注記が古くなる）は、字体注記の`node`の解決（GLYPH-04）の負例であり、`key`の維持そのものの検査ではない。

HIST-04・05・08の2026-11-11の追加（[law-of-japan/loj-spec#20](https://github.com/law-of-japan/loj-spec/issues/20)）は、ケースがあるが一部だけである（hist-023〜026）。`glyphNotes`のパスの不一致、`absent`のRevisionのディレクトリ、同じ関係・同じ施行時点の重複、統合・分割したRevisionを基礎状態とする版、撤回した内訳だけを参照する成立根拠の負例は、まだない。

v1alpha2の2026-11-11の追加（[law-of-japan/loj-spec#25](https://github.com/law-of-japan/loj-spec/issues/25)）のうち、マーカーの空白はpkg-125・126を代表例とし、`<!--`の後・`-->`の前・名前と最初の属性の間の負例は加えていない。番号のない第1項が数字で始まる場合の申告（DISP-01）は、`unsupportedFeatures`を申告した版のL1の不合格（BASIC-03）の既存のケースと同じ結果になるので、加えていない。`supplements[].title`を検査しないこと（MAN-01）は、既存の正例（附則の`title`が見出しと違う「制定附則」）が当たる。

GLYPH-05・GLYPH-07・GLYPH-10・GLYPH-11（2026-11-12、[law-of-japan/loj-spec#21](https://github.com/law-of-japan/loj-spec/issues/21)）: 正規分解を持たない互換漢字のブロックの字に注記がなくても合格する正例（glyph-010）と、字体を保持する資料を指さずに字体を照合済みにする負例（glyph-011）がある。`ivd`の必須、`variance`の`candidates`、`text.variances`・`text.correctionsSurveyed`はschemaにあるが、正例・負例はまだない。`text.correctionsSurveyed`は、hist-001の正例で使っている。

XREF-02（2026-11-12、[law-of-japan/loj-spec#16](https://github.com/law-of-japan/loj-spec/issues/16)）は、全部改正の対応の合格と、存在しない関係・撤回した関係・全部改正でない関係を指す負例、起点が食い違う負例がある（common-017・018・020〜022）。統合先への解決、分割したRecordに解決した場合の判定不能、未取得のケースは、まだない。XREF-01の不存在確認済み（`withdrawn`）は、確定した関係の違反（common-019）と、未確認の関係で違反にならない境界（common-023）がある。どちらも起点の側で、終点のRecordが`withdrawn`の場合のケースは、まだない。

XREF-05・XREF-06（2026-11-12、[law-of-japan/loj-spec#13](https://github.com/law-of-japan/loj-spec/issues/13)・[law-of-japan/loj-spec#19](https://github.com/law-of-japan/loj-spec/issues/19)）は、ケースがあるが一部だけである（common-013〜016）。common-013は`structured.period.raw`と`raw`を続けた文字列との一致に当たる。採用中の主張が`nonexistent`・`unknown`の場合の警告、`conflicting`等の判定しない場合、XREF-06の判定不能の場合のケースは、まだない。

TIME-03は、ケースがあるが一部だけである（hist-004、hist-015〜018）。`pending`等を基準とする`derived`に`value`を書いた負例と、`value`の書式（`YYYY-MM-DD`）に反する負例は、まだない。
