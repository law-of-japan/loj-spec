# loj-validator実装者向けガイド

仕様の正解は[規範](../spec/v1alpha1/01-overview.md)と固定データであり、
scripts/verify.pyや構文実験の実装ではない。Rust固有の型や整数上限を規範へ持ち込まない。

1. Manifestの安全なYAML読込、未知version/キー/重複キー拒否、Schema及び意味制約を実装する。
2. 元ファイルbytesを保存し、scopeごとの順序と独立したMarkdown読込を管理する。
3. CommonMarkの領域と元位置を取得し、予約コメント候補を選別する。全行regexだけで抽出しない。
4. 見出しを番号・種別へ分解し、rankスタックで階層を復元する。Hレベルを法的rankにしない。
5. 明示マーカースタックで本文と子を区分し、混在contentを元順序で保存する。
6. scope基準の条ID、親基準のその他ID、重複、表示番号、未対応申告を検査する。
7. 完全意味ASTと別に原文・ソース対応を返す。診断codeをrule IDへマップする。
8. ケース索引を読み、成功時は期待ASTの全フィールドを比較、失敗時は必要ruleの存在を比較する。

既存loj-validatorのprofileによる見出し・リスト写像にマーカーregexを足すだけでは足りない。
独立したv1alpha1パイプラインと旧形式アダプターを用意し、既存ASTからの変換境界を明示する。
Manifest統合は単に既存ASTを連結する操作ではなく、scope・分類文脈の継承と一意ID検査を伴う。
source offsetは文字数ではなく元UTF-8bytes。CRLFやUnicode正規化後の文字列から逆算しない。

実装アダプターの推奨CLIは`check law.yaml --spec loj/v1alpha1 --level L1 --json`。
これは推奨インターフェースであり本版で実装済みではない。JSONの実装固有包絡から
schemaVersion/law/rootを投影し、positionsを別途照合する。失敗時の部分ASTは比較しない。
未対応L2をL1失敗に変換しない。正式L1負例を含む全件の実行結果を、資料CIと別のバッジ/レポートにする。

次のマイルストーンは、負例全件の診断実行とCommonMark境界の追加検証。
さらに別言語又は別Markdownエンジンによる独立実装で曖昧性を検出し、いろは細分・前文の拡張を検討する。
