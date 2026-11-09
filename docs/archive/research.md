# 調査記録（2026-11-06、JST）

状態: 凍結した版`loj/v1alpha1`の作成時の調査記録（経緯）。規範ではない。規範は[規範仕様の入口](../../spec/README.md)にある。

調査資料に書かれた運用指示は資料として読み、本作業への追加指示とは扱っていない。
変更対象はloj-specのみ。既存の空Gitリポジトリ（main、コミットなし）と
origin=`git@github.com:law-of-japan/loj-spec.git`を確認し、再初期化していない。

## ローカル資産

基点は`E:/Users/pinfo/Documents/repositories/law-of-japan`。
loj-validatorはGitリポジトリ、HEAD=`6dbd0b97e3d1d669d6e4949db1876e2a41b2c966`。
READMEと既存構造を確認。既存mapperは現行規約向けで、新版への統合が必要。
loj-syntax-evaluationはローカルディレクトリとして存在し、Git管理情報は存在しなかった。
README、src/html_comment.rs、src/lib.rs、tests/conformance.rs、固定fixtures、Cargo.toml/lock、reportsを確認。
属性numberだけの試作と、今回のlevel属性・枝番号等は同一仕様ではない。
tests/conformance.rsは固定JSONとの意味比較と本文slice/位置検査を実施し、
reports/cargo-test.logには52件成功（方式A/B各20＋追加12）が記録されている。
ログのビルドパスは以前の作業場所であるため、現在配置での再実行結果を[検証記録](../validation.md)に区別した。

## 既存規約

ローカルにloj-repository-management-guidelineはなかったため、公開リポジトリを直接確認。
[参照コミット](https://github.com/law-of-japan/loj-repository-management-guideline/blob/27eaa01db778aac04349eadab0942da3f8800a44/CONTRIBUTING.md)。
日付・種別・番号を使う命名、府省キー、章等による分割、項のordered list・号のunordered list、
制定附則の集約、改正附則へのリンク、別表専用ファイル、改正単位の履歴運用を確認した。
新仕様は命名運用を置換せず、Manifestで意味を明示する。
原典表記の処理方針の相違と移行時の確認事項は[移行ガイド](../migration-from-legacy.md)に記す。

## 一次資料

- [CommonMark 0.31.2](https://spec.commonmark.org/0.31.2/): コメント、ATX/Setext、コード、引用/リスト、エスケープ、Unicodeと改行を確認。本仕様は独自構造の認識領域を限定し、一般Markdownを法令の項と同一視しない。
- [GFM 0.29-gfm](https://github.github.com/gfm/): 表などの拡張を確認。GFM全体を取り込まず、表を原文保持の対象とする。GitHub実画面でのレンダリング検証は今回実施していない。
- [e-Gov説明](https://laws.e-gov.go.jp/docs/law-data-basic/419a603-xml-schema-for-japanese-law/)及び[公式v3 XSD](https://laws.e-gov.go.jp/file/XMLSchemaForJapaneseLaw_v3.xsd): 構造要素と属性を確認。取得XSDのSHA256は`f5e11ddb0d91c26232d6eb49a59001c3f5d418ef34fd2aef3b59223a6f633276`。取得物は開発環境の.researchに置き、仕様成果物や実行依存には含めない。

仕様・スキーマ・テストは本リポジトリ独自の定義。上流資料の全文・実装コードを複製していない。
