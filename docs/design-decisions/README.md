# Design Decision Records

2026-11-06採用。実装コードから逆算せず、明示的な限定プロファイルとして判断した。

- [001 見出しと階層](001-headings.md)
- [002 コメントの厳密性](002-markers.md)
- [003 表示番号](003-display.md)
- [004 混在本文](004-content.md)
- [005 枝番号と削除](005-numbers.md)
- [006 附則キー](006-supplements.md)
- [007 ファイル統合](007-files.md)
- [008 XML対応](008-xml.md)
- [009 対応範囲](009-scope.md)
- [010 互換性と適合](010-versioning.md)
- [011 文字同一性とUnicode文字保存（2026-11-07）](011-character-preservation.md)

2026-11-09採用（次期仕様。[規範仕様の入口](../../spec/README.md)）。

- [012 版パッケージloj/v1alpha2](012-version-package-v1alpha2.md)
- [013 正本と派生ビュー](013-derived-views.md)
- [014 版の識別と時点値](014-revisions-and-time.md)
- [015 変更の種類と変更検査](015-change-kinds.md)
- [016 L3・L4の区分と結果の報告](016-l3-l4.md)
- [017 履歴マニフェストと関係の置き場所](017-history-manifest.md)
- [018 登録台帳とRecord ID](018-registry-and-record-ids.md)
- [019 固定参照](019-fixed-references.md)
- [020 原典からの再構築](020-rebuild.md)
- [021 字体注記](021-glyph-notes.md)
- [022 仕様の構成とschemaの書き方](022-spec-structure.md)

DDR-003・004・005・006・009・010・011には、2026-11-09にv1alpha2での扱いを追記した。

2026-11-11採用。

- [023 版の状態と公開](023-version-states.md)

DDR-010には、2026-11-11にDDR-023への参照を追記した。DDR-023には、2026-11-12に公開の条件と期待結果の確かめ方を追記した。DDR-016には、2026-11-12に版パッケージのL0の正例と診断の位置を追記した。

2026-11-15採用。

- [024 規範の適用対象と、運用・資料の管理の境界](024-scope-of-requirements.md)

DDR-023の公開の条件に書いた`rejectedBy: schema`の印の付け方の正は、DDR-024により、CONF-01からCONTRIBUTINGへ移った。

2026-11-16採用。

- [025 条を持たない本則](025-main-provision-paragraphs.md)
- [026 改正規定と改正内容](026-amendments.md)

DDR-012の制約で未対応とした条のない本則は、DDR-025で型付けした。

2026-11-20採用。

- [027 番号のない列挙（列記）](027-lists.md)
- [028 改正の指示の文のない改正規定](028-implicit-amendment-instructions.md)

DDR-026の制約とした、原典で番号のない項を改正内容に置くことのうち、条の全文の中の項は、DDR-028で書けることを明記した。

2026-11-24採用。

- [029 二つ以上の条をまとめた削除条](029-range-deleted-articles.md)

DDR-005の制約とした範囲削除のうち、二つの条を結ぶ範囲のラベルの削除条は、DDR-029で型付けした。
