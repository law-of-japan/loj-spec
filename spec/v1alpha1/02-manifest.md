# Manifest

## MAN-01

law.yamlはYAML 1.2のJSON互換データモデルによる単一mappingでなければならない（MUST）。キーは文字列、重複キー、タグ、アンカー、エイリアス、merge key、複数文書は禁止（MUST NOT）。スカラーは文字列、JSON形式の数、true/false/nullのみ。文字列を意図する日付は引用する（MUST）。全階層の未知フィールドを拒否する。正確な必須・任意フィールドと型は[Schema](../../schemas/v1alpha1/manifest.schema.json)に定義する。

必須: schemaVersion、law（id/title/type/number/promulgatedAt/language）、documents。numberは文字列又はnull（法令番号なし）、promulgatedAtは実在するグレゴリオ暦YYYY-MM-DD又はnull（不明）。空文字列で不明を表してはならない。languageはja。typeはconstitution/act/cabinetOrder/imperialOrder/ministerialOrdinance/rule/ordinance/other。idは英数字先頭のASCII英数字とハイフンで、大小文字を区別し、永続的な登録キーとする。旧リポジトリ名を継承してよいが、idから種別・日付を導出しない。

任意: sources（出典URI文字列配列）、unsupportedFeatures（非空文字列配列）、supplements（key/title）、appendices（key/title）。各documentはpathとparentだけを持つ。parentはmain、supplement/key、appendix/keyのいずれかでなければならない（MUST）。keyは小文字ASCII英字先頭、小文字英数字とハイフン。定義済みキーのみ参照でき、各キーは同種の配列内で一意でなければならない。originalは制定時附則の推奨キーであり、位置による自動採番は禁止。

## MAN-02

pathはlaw.yamlのあるディレクトリからの相対POSIXパスでなければならない（MUST）。ASCII英数字、ハイフン、アンダースコア、ピリオドのセグメントと`/`のみを許し、拡張子は`.md`。絶対パス、空セグメント、`.`/`..`セグメント、バックスラッシュ、ドライブ、URL、末尾のドット、Windows予約名CON/PRN/AUX/NUL/COM1〜9/LPT1〜9（拡張子付きも含む）を禁止する。symlink/junction経由、ルート外への解決、非通常ファイルも禁止する。比較はASCII小文字化したパスで行い、重複・ハードリンクによる同一実体の二重指定を禁止（MUST NOT）。ファイルは実在し読めなければならない。未列挙ファイルは法令入力に含めない。

## MAN-03

documents順に読み込む（MUST）。mainを最初の連続区間とし、その後supplements宣言順、appendices宣言順にそれぞれ連続区間を設ける。mainと宣言された各scopeには1ファイル以上が必要。別scopeから戻ってはならない。scope切替時に見出し文脈を初期化する。同scopeの次ファイルには編〜目の文脈だけを引き継ぐ。条、明示マーカー、Markdownブロック・参照リンク定義をファイル境界で継続してはならない（MUST NOT）。各ファイルは独立したCommonMark文書として解析する。

分割は完結した条の間（附属資料では完結したMarkdownブロック間）のみ許可する。後続ファイルは新しい条又は分類見出しから始める。分類見出しの再掲は継続宣言ではなく重複である。変更後も同じscope・出現順・分類文脈・原文本文を維持する場合、意味ASTとIDは不変でなければならない（MUST）。見出しのないファイルを前の条の続きと推測してはならない。

JSON Schemaでは日付formatの実検査を有効にする（MUST）。参照キー、区間順、重複path、ファイル解決は意味制約でありSchemaだけでは検査できない。
