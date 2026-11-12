# 旧リポジトリから原典による再構築への移行の手順

旧形式の法令リポジトリ（[旧リポジトリ管理ガイドライン](https://github.com/law-of-japan/loj-repository-management-guideline/blob/27eaa01db778aac04349eadab0942da3f8800a44/CONTRIBUTING.md)に従ったもの）のRecordを、次期仕様の形へ移す作業の手順である。移した後の法令リポジトリの運用は、次期仕様に合わせた[リポジトリ管理ガイドライン](https://github.com/law-of-japan/loj-repository-management-guideline/blob/24b89b40474f9238120cc23e35ff01a6c44c8077/CONTRIBUTING.md)に従う。本書は参考であり、規範は[loj-rebuild/v1alpha1](../spec/loj-rebuild/v1alpha1/01-rebuild.md)と、そこから参照する各種類の要件である。手順と規範が食い違えば、規範に従う。

## 方針

- 本文は原典資料から作り直す。旧リポジトリの本文を、版の本文として取り込まない（[REB-03](../spec/loj-rebuild/v1alpha1/01-rebuild.md)）。旧本文を新しい形へ変換する手順は、もう案内しない。v1alpha1の変換の手順は、本書のGitの履歴で参照できる。
- IDと既存のリンクは保つ。既存の`law.id`（`law.yaml`のない旧リポジトリでは、凍結した時点のリポジトリの名前）をRecord IDとし、再発行しない（REB-02）。旧リポジトリのcommitは、凍結した状態で到達できるように保つ（REB-08）。
- 旧データ（履歴の並び、commitメッセージ、`law.yaml`の値）は、確かめる改正と資料の作業の一覧として使う。記録する値の根拠にはしない（REB-06）。
- 既存の法令リポジトリの移行は、検査器（統合案のO-17）ができてから始める。L0・L1・L3の結果を確かめずに移すと、REB-01の適合を主張できないためである。

## 作業の順序

| 順 | 作業 | 作るもの | 主な要件 |
|---|---|---|---|
| 1 | 旧リポジトリの凍結 | 凍結した時点の規定のブランチのcommit | REB-02、REB-08 |
| 2 | 登録台帳への登録 | 登録台帳の`records/<Record ID>.yaml` | REG-01〜05、RID-01〜05、REB-02 |
| 3 | 原典資料の確認 | 使う資料と、文字情報の保持の確認結果 | REB-04、REB-05、GLYPH-07 |
| 4 | 履歴マニフェスト | `history.yaml` | HIST-01〜12、REV-01〜04、TIME-01〜07、REB-07 |
| 5 | 原典から版を起こす | `versions/<revision_id>/`の版パッケージ | `loj/v1alpha2`の各章、CHAR-01〜05、REB-03 |
| 6 | 字体注記 | `versions/<revision_id>/glyphs.yaml` | GLYPH-01〜11 |
| 7 | 再構築報告 | `rebuild.yaml` | REBR-01〜05 |
| 8 | commitと変更の種類の宣言 | trailerを付けた正本の`main`のcommit | CHG-01〜03 |
| 9 | 派生ビュー | 例えば`history`ブランチ | VIEW-01〜07、付録A |
| 10 | 検査 | 検査の報告 | VAL-01〜08、CONF-02 |

### 1. 旧リポジトリの凍結

- 規定のブランチ（`master`、または`main`）を凍結する。凍結した時点のcommitの完全なハッシュを控える。これが再構築報告の`legacy.frozenAt`になる。
- 凍結した旧履歴に、push・force pushしない。ブランチの名前による既存のリンク（`blob/master/…`）を壊さないように、新しい正本は別のブランチ（`main`）に置く。旧`master`が規定のブランチなら、`main`を新しく作り、規定のブランチを`main`に切り替える。
- 凍結より後は、リポジトリの名前を変えない。リポジトリの名前とRecord IDの対応は、登録台帳で解決する。
- 見つかった誤りを、旧リポジトリで直さない。差は再構築報告に記録する（REBR-05）。

### 2. 登録台帳への登録

- 登録台帳のリポジトリに、`records/<Record ID>.yaml`を一つ作る。Record IDは手順1の既存のIDである。
- それより前のリポジトリの名前は`aliases`に入れ、各別名に根拠（旧本文のリンク、GitHubの転送等）を付ける。
- `repository`に、法令リポジトリの`location`と`canonicalBranch: main`を書く。
- 番号主張・外部識別子は、原典で確かめた根拠と共に記録する。旧`law.yaml`の値を、確かめずに写さない。原典で確かめられない番号は`state: unknown`の主張とし、旧`number`の値（`null`を含む）は確認状態の理由に手がかりとして書く（REB-06）。
- 改正法など、本文を収録しないが関係の起点になるRecordも、ここで登録する（`text.state: notCollected`）。

### 3. 原典資料の確認

- 版の本文の根拠は、公布された本文（官報と官報正誤）である。官報を入手できなければ、御署名原本から起こしてよい。その場合の記録の仕方はREB-05に従う。
- 使う資料ごとに、旧字体・異体字・異体字セレクタを保持しているかを、再構築を始める前に確かめる（e-Govは新字体に置き換えている）。結果は手順7で`sourceChecks`に書く。
- 改正後の本文を、e-Govの改正後の全文から起こさない。官報も御署名原本も入手できない改正の版は、本文のない版（`text.status: absent`）として記録する。

### 4. 履歴マニフェスト

- 法令リポジトリの最上位に`history.yaml`を置く。`sources`に手順3の資料を定義し、ほかのファイルからはその`id`で参照する。
- 版（Revision）ごとに、新しいrevision_idを発行する（REV-01）。旧来の短い呼び名（例: `S23-178`）は、可読ラベルとしてだけ残せる。
- 改正の関係（`relations`）は、改正法のRecordを起点とし、このRecordを終点として記録する。施行時点は時点値で書き、確かめられないものは`unknown`・`pending`とする。
- 収録範囲は、再構築した直後は`coverage.state: unconfirmed`とする。旧リポジトリの版の数を、網羅性の根拠にしない（REB-07）。

### 5. 原典から版を起こす

- 各版を`versions/<revision_id>/`に、`loj/v1alpha2`の版パッケージ（`law.yaml`と本文のMarkdown）として置く。
- 本文は原典の文字をそのまま写す。旧字体・異体字を新字体に置き換えない。決められない字は、CHAR-04に従って記録する。
- 前文・制定文・目次・表・無番号の項は、v1alpha2の構造（PRE、TOC、TABLE、PARA）で書く。
- 既存の条のIDは、`loj/v1alpha2`のIDの導出（ID-01）で決まる。

### 6. 字体注記

- 本文の字の字体について、原典の字形と、本文に置いたコードポイントの関係を記録する必要があれば、`glyphs.yaml`に注記する（GLYPH-02）。
- 原典の中の訂正（GLYPH-09）、踊り字（GLYPH-08）、互換漢字と異体字セレクタ（GLYPH-11）の扱いもここで記録する。
- 官報の字体と照合していない版は、`text.glyphs: unverified`のままにする。

### 7. 再構築報告

- 法令リポジトリの最上位に`rebuild.yaml`を置く。
- `legacy`に、旧リポジトリと`frozenAt`（手順1のcommit）を書く。
- `mappings`に、旧commitと、対応するRevisionを書く。旧commitは完全なハッシュで指し、ブランチ名・タグ名で指さない。
- まだ再構築していない改正は`pending`に、原典と旧本文の間に見つかった差は`differences`に書く。
- 再構築報告は作業の記録であり、登録台帳・履歴マニフェスト・版パッケージの値の根拠にしない。

### 8. commitと変更の種類の宣言

正本の`main`の各commitに、変更の種類をtrailerで宣言する。一つのcommitに一つの種類とする。

```text
制定時の版を加える

LoJ-Change: revisionAdd
LoJ-Revisions: 98mj5vgx
```

- 版を加えるcommitは`revisionAdd`、履歴マニフェストの属性・字体注記・再構築報告だけを加えるcommitは`metadata`とする。
- 後で見つけた転記の誤りは`correction`、官報正誤の反映は`officialCorrection`とし、新しいRevisionを作らない。

### 9. 派生ビュー

- 旧来の「一つの線形なGit履歴」が必要なら、正本から派生ビューとして生成する。参考の形式は[付録A（historyブランチ）](../spec/common/v1alpha1/appendix-a-history-branch.md)にある。
- ビューに保存できない情報（併存する版、未確定の施行時点、本文のない版、確認状態）は、索引ファイルで除外・欠落として示す。ビューのcommitへのリンクは安定しないので、引用には正本の固定参照（FIXREF-02）を使う。

### 10. 検査

- 版ごとにL0・L1、Recordの正本にL3（`historyStructure`、`evidence`）、登録台帳と関係する複数のRecordにL4を、それぞれ別に報告する（VAL-02）。
- 結果には、対象とした記録版（正本のcommit）を記録する（VAL-03）。
- 変更の種類の検査は、commitごとに行う（CHG-02）。

## 例: 祝日法

国民の祝日に関する法律（昭和二十三年法律第百七十八号、Record ID `19480720-law-178`）の制定時の版と、最初の改正（昭和四十一年法律第八十六号）の後の版を、この手順で作った試作が適合ケースの正例にある。

| 手順 | 適合ケースのファイル |
|---|---|
| 2 | [登録台帳](../conformance/loj-registry/v1alpha1/valid/reg-001/registry/records/19480720-law-178.yaml)（改正法のRecord `19660625-act-86`も含む） |
| 4 | [履歴マニフェスト](../conformance/loj-history/v1alpha1/valid/hist-001/repo/history.yaml) |
| 5・6 | [制定時の版](../conformance/loj-history/v1alpha1/valid/hist-001/repo/versions/98mj5vgx/law.yaml)、[改正後の版](../conformance/loj-history/v1alpha1/valid/hist-001/repo/versions/zwgmz1rt/law.yaml)と、それぞれの`glyphs.yaml` |
| 7 | [再構築報告](../conformance/loj-history/v1alpha1/valid/hist-001/repo/rebuild.yaml) |

試作の経緯と、原典資料の確認の結果は、[統合案](archive/next-spec-integration.md)の§10.5〜§10.18にある。適合ケースは試作であり、実際の旧リポジトリの凍結・移行はまだ行っていない。
