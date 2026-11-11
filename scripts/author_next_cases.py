"""Hand-authored cases for the history, glyph, registry, rebuild and common suites.

Authoring helper (O-15). Not a validator: each negative case is a copy of a
checked-in positive input with one hand-written change, and its expected rule
and result are written here by hand from the spec text. The fictional Git
history for the change and reference cases is built with fixed authors and
dates so that the bundle and the commit hashes are reproducible.
CI does not run this script; it reads the checked-in files.
"""
import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
C = ROOT / "conformance"
HIST_POS = "conformance/loj-history/v1alpha1/valid/hist-001/repo"
REG_POS = "conformance/loj-registry/v1alpha1/valid/reg-001/registry"
SV = {"hist": "loj-history/v1alpha1", "glyph": "loj-glyphs/v1alpha1", "reg": "loj-registry/v1alpha1",
      "rebuild": "loj-rebuild/v1alpha1", "pkg": "loj/v1alpha2", "common": "common/v1alpha1"}
FOLDER = {"hist": "loj-history/v1alpha1", "glyph": "loj-glyphs/v1alpha1", "reg": "loj-registry/v1alpha1",
          "rebuild": "loj-rebuild/v1alpha1", "common": "common/v1alpha1"}
INDEX = {key: [] for key in FOLDER}
ZWG = "versions/zwgmz1rt/"


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes((json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))


def mutate(dest, source, edits):
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(ROOT / source, dest)
    for name, old, new in edits:
        path = dest / name
        text = path.read_bytes().decode("utf-8")
        assert old in text, (dest, name, old)
        path.write_bytes(text.replace(old, new, 1).encode("utf-8"))


def diag(rule, schema_version, klass="error"):
    return {"rule": rule, "schemaVersion": schema_version, "class": klass}


def add(suite, title, requirements, check, inp, expected, success, category=None, normative=True):
    ident = "%s-%03d" % (suite, len(INDEX[suite]) + 1)
    exp_path = "conformance/%s/expected/%s.json" % (FOLDER[suite], ident)
    write_json(ROOT / exp_path, expected)
    case = {"id": ident, "title": title, "requirements": requirements, "check": check}
    if category:
        case["category"] = category
    case.update({"normative": normative, "input": inp, "expected": exp_path, "success": success})
    INDEX[suite].append(case)
    return ident


def next_dir(suite, success):
    ident = "%s-%03d" % (suite, len(INDEX[suite]) + 1)
    return C / FOLDER[suite] / ("valid" if success else "invalid") / ident


def rel(path):
    return path.relative_to(ROOT).as_posix()


def l3(category, result="pass"):
    return {"check": "L3", "category": category, "result": result}


# --- loj-history -------------------------------------------------------------
def history():
    add("hist", "祝日法の制定時と最初の改正後の版", ["HIST-01", "HIST-02", "HIST-03", "HIST-04", "HIST-05", "HIST-06",
                                         "HIST-07", "HIST-08", "HIST-10", "HIST-11", "REV-01", "REV-03", "REV-04"],
        "L3", {"kind": "repository", "path": HIST_POS},
        {"results": [l3("historyStructure"), l3("evidence")]}, True, "historyStructure")
    add("hist", "履歴だけの法令リポジトリ（旧特許法の廃止）", ["HIST-01", "HIST-03", "HIST-12"], "L3",
        {"kind": "repository", "path": "conformance/loj-history/v1alpha1/valid/hist-002/repo"},
        {"results": [{"check": "L0", "result": "notApplicable"}, {"check": "L1", "result": "notApplicable"},
                     l3("historyStructure")]}, True, "historyStructure")
    add("hist", "条件付きの失効（皇室典範特例法）", ["HIST-12", "TIME-04"], "L3",
        {"kind": "repository", "path": "conformance/loj-history/v1alpha1/valid/hist-003/repo"},
        {"results": [l3("historyStructure")]}, True, "historyStructure")
    add("hist", "他のRecordの時点を参照する改正（T-04）", ["HIST-03", "HIST-05", "TIME-03", "TIME-07"], "L3",
        {"kind": "repository", "path": "conformance/loj-history/v1alpha1/valid/hist-004/repo"},
        {"results": [l3("historyStructure")]}, True, "historyStructure")
    negatives = [
        ("Revisionの未知のフィールド", "HIST-01", [("history.yaml", "    label: 制定\n", "    label: 制定\n    current: true\n")]),
        ("revision_idの形式", "REV-01", [("history.yaml", "  - id: zwgmz1rt", "  - id: zwgmz1r")]),
        ("関係の内訳のidの重複", "HIST-03", [("history.yaml", "      - id: i2\n", "      - id: i1\n")]),
        ("内訳にない成立根拠", "HIST-05", [("history.yaml", "items: [i1, i2, i3]", "items: [i1, i2, i4]")]),
        ("存在しない基礎状態", "HIST-04", [("history.yaml", "basedOn: 98mj5vgx", "basedOn: 98mj5vgy")]),
        ("本文のない版の版パッケージ", "HIST-08", [("history.yaml", "      status: complete\n      sources:\n        - {source: src-goshomei-s41-86",
                                             "      status: absent\n      sources:\n        - {source: src-goshomei-s41-86")]),
        ("law.idとRecord IDの不一致", "HIST-02", [(ZWG + "law.yaml", 'id: "19480720-law-178"', 'id: "19480720-law-179"')]),
        ("原表記のない確定日", "TIME-01", [("history.yaml", "        raw: 昭和二十三年七月二十日\n", "")]),
        ("根拠のない確認済みの時点", "TYPE-05", [("history.yaml", "        evidence: [{source: src-kanpo-19480720, locator: 1コマ 発行日}]\n",
                                          "        evidence: []\n")]),
    ]
    for title, rule, edits in negatives:
        dest = next_dir("hist", False) / "repo"
        mutate(dest, HIST_POS, edits)
        sv = SV["common"] if rule.startswith(("TIME", "TYPE")) else SV["hist"]
        category = "evidence" if rule.startswith("TYPE") else "historyStructure"
        add("hist", title, [rule], "L3", {"kind": "repository", "path": rel(dest)},
            {"results": [l3(category, "fail")], "diagnostics": [diag(rule, sv)]}, False, category)
    dest = next_dir("hist", False) / "repo"
    mutate(dest, "conformance/loj-history/v1alpha1/valid/hist-002/repo",
           [("history.yaml", "  - {type: repealed, relation: rel-repeal}", "  - {type: totallyRevised, relation: rel-repeal}")])
    add("hist", "効力の終了の種類と関係の種類の不一致", ["HIST-12"], "L3", {"kind": "repository", "path": rel(dest)},
        {"results": [l3("historyStructure", "fail")], "diagnostics": [diag("HIST-12", SV["hist"])]}, False,
        "historyStructure")
    dest = next_dir("hist", False) / "repo"
    mutate(dest, "conformance/loj-history/v1alpha1/valid/hist-004/repo",
           [("history.yaml", '      value: "2019-05-01"\n      raw: 附則第十条及び第十一条の規定はこの法律の施行の日の翌日から施行する\n'
             "      evidence: [{source: src-egov-h29-63, locator: 附則第一条第一項ただし書}]\n      verification: {state: unverified, reason: 基礎の時点が未照合}\n    applicability",
             '      value: "2019-05-03"\n      raw: 附則第十条及び第十一条の規定はこの法律の施行の日の翌日から施行する\n'
             "      evidence: [{source: src-egov-h29-63, locator: 附則第一条第一項ただし書}]\n      verification: {state: unverified, reason: 基礎の時点が未照合}\n    applicability")])
    add("hist", "calcと計算結果の不一致", ["TIME-03"], "L3", {"kind": "repository", "path": rel(dest)},
        {"results": [l3("historyStructure", "fail")], "diagnostics": [diag("TIME-03", SV["common"])]}, False,
        "historyStructure")
    add("hist", "確定日であるderivedを基準とするderived（架空）", ["TIME-03"], "L3",
        {"kind": "repository", "path": rel(next_dir("hist", True) / "repo")},
        {"results": [l3("historyStructure")]}, True, "historyStructure")
    dest = next_dir("hist", False) / "repo"
    month_base = ('value: "2019-04-30"\n{0}raw: 平成三十一年四月三十日\n{0}precision: day\n',
                  'value: "2019-04"\n{0}raw: 平成三十一年四月\n{0}precision: month\n')
    mutate(dest, "conformance/loj-history/v1alpha1/valid/hist-004/repo",
           [("history.yaml", month_base[0].format(" " * 12), month_base[1].format(" " * 12)),
            ("history.yaml", month_base[0].format(" " * 8), month_base[1].format(" " * 8))])
    add("hist", "確定日でない基準から計算したvalue", ["TIME-03"], "L3", {"kind": "repository", "path": rel(dest)},
        {"results": [l3("historyStructure", "fail")], "diagnostics": [diag("TIME-03", SV["common"])]}, False,
        "historyStructure")


# --- loj-glyphs --------------------------------------------------------------
def glyphs():
    add("glyph", "祝日法の版の字体注記", ["GLYPH-01", "GLYPH-02", "GLYPH-04", "GLYPH-05", "GLYPH-06", "GLYPH-09",
                                  "GLYPH-10", "GLYPH-11"], "L3", {"kind": "repository", "path": HIST_POS},
        {"results": [l3("evidence")]}, True, "evidence")
    negatives = [
        ("注記の位置のずれ", "GLYPH-04", [(ZWG + "glyphs.yaml", "offset: 63", "offset: 62")]),
        ("注記のノードが解決できない", "GLYPH-04", [(ZWG + "glyphs.yaml", "article/3/paragraph/1\n", "article/4/paragraph/1\n")]),
        ("行のkeyを変えて注記が古くなる", "GLYPH-04", [(ZWG + "main.md", "row key=b6gr", "row key=b6gs")]),
        ("候補が一つだけの曖昧な字", "GLYPH-05", [(ZWG + "glyphs.yaml", 'candidates: ["祝", "' + chr(0xFA51) + '"]', 'candidates: ["祝"]')]),
        ("注記のない〓", "GLYPH-02", [(ZWG + "main.md", "元日\n", "元〓\n")]),
        ("注記のrevisionの不一致", "GLYPH-01", [(ZWG + "glyphs.yaml", "revision: zwgmz1rt", "revision: 98mj5vgx")]),
        ("注記のない互換漢字", "GLYPH-11", [(ZWG + "main.md", "元日\n", "元日" + chr(0xFA19) + "\n")]),
    ]
    for title, rule, edits in negatives:
        dest = next_dir("glyph", False) / "repo"
        mutate(dest, HIST_POS, edits)
        add("glyph", title, [rule], "L3", {"kind": "repository", "path": rel(dest)},
            {"results": [l3("evidence", "fail")], "diagnostics": [diag(rule, SV["glyph"])]}, False, "evidence")
    dest = next_dir("glyph", False) / "repo"
    mutate(dest, HIST_POS, [(ZWG + "main.md", "## 第三條", "## 三")])
    add("glyph", "版パッケージのL1が不合格のときの字体注記", ["GLYPH-11", "VAL-02", "VAL-04"], "L3",
        {"kind": "repository", "path": rel(dest)},
        {"results": [{"check": "L1", "result": "fail"}, l3("evidence", "incomplete"), l3("historyStructure")],
         "diagnostics": [diag("HEAD-01", SV["pkg"])]}, False, "evidence")


# --- loj-registry ------------------------------------------------------------
def registry():
    add("reg", "登録台帳の三つのRecord", ["REG-01", "REG-02", "REG-03", "REG-05", "RID-02"], "registry",
        {"kind": "registry", "path": REG_POS}, {"results": [{"check": "registry", "result": "pass"}]}, True)
    act = "records/19660625-act-86.yaml"
    law = "records/19480720-law-178.yaml"
    negatives = [
        ("ファイル名とIDの不一致", "REG-01", [(act, "id: 19660625-act-86\n", "id: 19660625-act-87\n")]),
        ("採用中の番号主張が二つ", "REG-03", [(law, "    decision: adopted\n", "    decision: adopted\n  - id: n2\n    state: exists\n"
                                                "    raw: 法律第百七十九号\n    evidence: [{source: src-egov, locator: 法令番号}]\n"
                                                "    verification: {state: unverified, reason: 索引の転記}\n    decision: adopted\n")]),
        ("訂正前の主張が見つからない", "REG-04", [(law, "    decision: adopted\n", "    decision: adopted\n    supersedes: n9\n")]),
        ("採番期間を西暦年だけにする", "REG-03", [(law, 'gregorian: {from: "1948-01-01", to: "1948-12-31"}', "gregorian: 1948")]),
        ("仮登録で同一性を確認済みにする", "REG-02", [(act, "status: active\n", "status: provisional\n")]),
        ("本文がある法令にリポジトリがない", "REG-02", [(law, "repository:\n  location: github.com/law-of-japan/19480720-law-178\n  canonicalBranch: main\n", "")]),
    ]
    for title, rule, edits in negatives:
        dest = next_dir("reg", False) / "registry"
        mutate(dest, REG_POS, edits)
        add("reg", title, [rule], "registry", {"kind": "registry", "path": rel(dest)},
            {"results": [{"check": "registry", "result": "fail"}], "diagnostics": [diag(rule, SV["reg"])]}, False)
    dest = next_dir("reg", False) / "registry"
    # A case-only file-name collision cannot be stored on case-insensitive file systems, so the
    # collision is made through an alias of another Record (RID-01 counts aliases as issued IDs).
    mutate(dest, REG_POS, [(law, "status: active\n", "status: active\naliases:\n  - id: 19660625-ACT-86\n"
                            "    evidence: [{source: src-egov, locator: 法令ID}]\n    verification: {state: unverified}\n")])
    add("reg", "別名と大小文字だけが違うRecord ID", ["RID-01", "RID-02"], "registry", {"kind": "registry", "path": rel(dest)},
        {"results": [{"check": "registry", "result": "fail"}], "diagnostics": [diag("RID-01", SV["reg"])]}, False)


# --- loj-rebuild -------------------------------------------------------------
def rebuild():
    add("rebuild", "祝日法の再構築報告", ["REBR-01", "REBR-02", "REBR-03", "REBR-04", "REBR-05"], "rebuild",
        {"kind": "repository", "path": HIST_POS}, {"results": [{"check": "rebuild", "result": "pass"}]}, True)
    negatives = [
        ("短縮した旧commit", "REBR-02", [("rebuild.yaml", "commit: 43934f17a35c8b4dce2caec609bddbae4eb6841b", "commit: 43934f1")]),
        ("履歴マニフェストにない資料", "REBR-02", [("rebuild.yaml", "  - source: src-egov\n", "  - source: src-egov-nowhere\n")]),
        ("存在しないRevisionへの対応", "REBR-04", [("rebuild.yaml", "revisions: [98mj5vgx]", "revisions: [98mj5vgy]")]),
    ]
    for title, rule, edits in negatives:
        dest = next_dir("rebuild", False) / "repo"
        mutate(dest, HIST_POS, edits)
        add("rebuild", title, [rule], "rebuild", {"kind": "repository", "path": rel(dest)},
            {"results": [{"check": "rebuild", "result": "fail"}], "diagnostics": [diag(rule, SV["rebuild"])]}, False)


# --- common: L4 ----------------------------------------------------------------
def cross_record():
    repos = ["conformance/loj-history/v1alpha1/valid/hist-003/repo", "conformance/loj-history/v1alpha1/valid/hist-004/repo"]
    add("common", "特例法の施行の日と祝日法の改正の時点（T-04）", ["XREF-01", "XREF-03", "VAL-06"], "L4",
        {"kind": "records", "registry": REG_POS, "repositories": repos},
        {"results": [{"check": "L4", "category": "relationResolution", "result": "pass"},
                     {"check": "L4", "category": "timeConsistency", "result": "pass"}],
         "references": [{"target": "loj/20170616-law-63", "result": "resolved"}]}, True, "timeConsistency")
    dest = next_dir("common", False)
    mutate(dest / "hist-004", repos[1], [("history.yaml", '            value: "2019-04-30"\n', '            value: "2019-04-29"\n'),
                                         ("history.yaml", "        value: \"2019-04-30\"\n", "        value: \"2019-04-29\"\n")])
    add("common", "sameAsの参照先と時点が食い違う", ["XREF-03", "TIME-07"], "L4",
        {"kind": "records", "registry": REG_POS, "repositories": [repos[0], rel(dest / "hist-004")]},
        {"results": [{"check": "L4", "category": "timeConsistency", "result": "fail"}],
         "diagnostics": [diag("XREF-03", SV["common"])]}, False, "timeConsistency")
    add("common", "参照先のRecordを収録していない", ["XREF-03", "VAL-04", "VAL-06"], "L4",
        {"kind": "records", "registry": REG_POS, "repositories": [repos[1]]},
        {"results": [{"check": "L4", "category": "timeConsistency", "result": "incomplete"}],
         "references": [{"target": "loj/20170616-law-63/q3c8h0tw", "result": "notFetched"}]}, True, "timeConsistency")


# --- common: change kinds and fixed references -------------------------------
FIX_LAW = {"id": "20990101-act-1", "title": "架空雲保管法（実在しないサンプル）", "type": "act", "number": "架空法律第一号",
           "promulgatedAt": "2099-01-01", "language": "ja"}
REV = "b7k2m9qd"
NODE = "20990101-act-1/main/article/1/paragraph/1"


def fictional_files(body1, files_split=False, label="制定"):
    docs = [{"path": "one.md", "parent": "main"}, {"path": "two.md", "parent": "main"}] if files_split else \
        [{"path": "main.md", "parent": "main"}]
    law = {"schemaVersion": "loj/v1alpha2", "law": FIX_LAW, "documents": docs}
    art1 = "# 第一条\n<!-- loj:paragraph number=1 -->\n" + body1 + "<!-- loj:end-paragraph -->\n"
    art2 = "# 第二条\n<!-- loj:paragraph number=1 -->\n雲は返す。\n<!-- loj:end-paragraph -->\n"
    md = {"one.md": art1, "two.md": art2} if files_split else {"main.md": art1 + art2}
    history = ("schemaVersion: loj-history/v1alpha1\nrecord: {id: 20990101-act-1, label: 架空法律第一号}\n"
               "sources:\n  - {id: src-fiction, kind: other, title: 架空の原典}\nrelations: []\nrevisions:\n"
               "  - id: " + REV + "\n    label: " + label + "\n    origin: enactment\n    effective:\n      state: date\n"
               "      value: \"2099-01-01\"\n      raw: 二千九十九年一月一日\n      precision: day\n"
               "      evidence: [{source: src-fiction, locator: 附則}]\n      verification: {state: confirmed}\n"
               "    applicability: {state: unsurveyed}\n    text:\n      status: complete\n"
               "      sources: [{source: src-fiction, locator: 本則}]\n      glyphs: unverified\n    status: active\n"
               "coverage: {state: unconfirmed}\n")
    out = {"history.yaml": history, "versions/" + REV + "/law.yaml": json.dumps(law, ensure_ascii=False, indent=2) + "\n"}
    out.update({"versions/" + REV + "/" + k: v for k, v in md.items()})
    return out


def build_bundle(path):
    steps = [
        ("制定時の版を加える", "revisionAdd", True, fictional_files("架空の雲を保管すろ。\n")),
        ("第一条の誤転記を直す", "correction", True, fictional_files("架空の雲を保管する。\n")),
        ("条ごとにファイルを分ける", "format", False, fictional_files("架空の雲を保管する。\n", files_split=True)),
        ("ラベルを改める（宣言なし）", None, False, fictional_files("架空の雲を保管する。\n", True, "制定時")),
        ("書式変更と宣言して本文を変える", "format", False, fictional_files("架空の雲を保管し続ける。\n", True, "制定時")),
    ]
    env = dict(os.environ, GIT_AUTHOR_NAME="LoJ conformance", GIT_AUTHOR_EMAIL="conformance@example.invalid",
               GIT_COMMITTER_NAME="LoJ conformance", GIT_COMMITTER_EMAIL="conformance@example.invalid")
    hashes = []
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp) / "repo"
        repo.mkdir()
        git = lambda *args, **kw: subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True, env=env, **kw)
        git("init", "-q", "-b", "main")
        git("config", "core.autocrlf", "false")
        for i, (subject, kind, with_revs, files) in enumerate(steps):
            for old in repo.glob("versions/*/*.md"):
                old.unlink()
            for name, body in files.items():
                target = repo / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(body.encode("utf-8"))
            git("add", "-A")
            message = subject + "\n"
            if kind:
                message += "\nLoJ-Change: " + kind + "\n" + ("LoJ-Revisions: " + REV + "\n" if with_revs else "")
            date = "2099-01-%02dT00:00:00+0900" % (i + 1)
            env["GIT_AUTHOR_DATE"] = env["GIT_COMMITTER_DATE"] = date
            git("commit", "-q", "-F", "-", input=message.encode("utf-8"))
            hashes.append(git("rev-parse", "HEAD").stdout.decode().strip())
        path.parent.mkdir(parents=True, exist_ok=True)
        git("bundle", "create", str(path), "main")
    return hashes


def changes_and_references():
    bundle_pos = next_dir("common", True) / "repo.bundle"
    hashes = build_bundle(bundle_pos)
    c1, c2, c3, c4, c5 = hashes
    bundle = rel(bundle_pos)
    add("common", "記録訂正の宣言と変更", ["CHG-01", "CHG-02", "CHG-03"], "change",
        {"kind": "change", "bundle": bundle, "base": c1, "head": c2}, {"results": [{"check": "change", "result": "pass"}]}, True)
    add("common", "ASTを変えない書式変更", ["CHG-02", "CHG-03"], "change",
        {"kind": "change", "bundle": bundle, "base": c2, "head": c3}, {"results": [{"check": "change", "result": "pass"}]}, True)
    for title, rule, base, head in [("変更の種類の宣言がない", "CHG-03", c3, c4), ("書式変更と宣言してASTを変える", "CHG-02", c4, c5)]:
        dest = next_dir("common", False) / "repo.bundle"
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(bundle_pos, dest)
        add("common", title, [rule], "change", {"kind": "change", "bundle": rel(dest), "base": base, "head": head},
            {"results": [{"check": "change", "result": "fail"}], "diagnostics": [diag(rule, SV["common"])]}, False)
    registry = next_dir("common", True) / "registry/records/20990101-act-1.yaml"
    registry.parent.mkdir(parents=True, exist_ok=True)
    registry.write_bytes(("schemaVersion: loj-registry/v1alpha1\nid: 20990101-act-1\nlabel: 架空雲保管法\nstatus: active\n"
                          "identity:\n  evidence: [{source: src-fiction, locator: 題名}]\n  verification: {state: confirmed}\n"
                          "text: {state: collected}\nrepository: {location: example.invalid/20990101-act-1, canonicalBranch: main}\n"
                          "sources:\n  - {id: src-fiction, kind: other, title: 架空の原典}\nnumbers: []\nexternalIds: []\n").encode("utf-8"))
    reg = rel(registry.parent.parent)
    ref = "loj:loj/20990101-act-1/" + REV
    add("common", "固定参照で訂正前の本文を指す", ["FIXREF-02", "FIXREF-03", "FIXREF-07"], "reference",
        {"kind": "reference", "bundle": bundle, "registry": reg, "reference": ref + "@" + c1 + "#" + NODE},
        {"resolution": {"result": "resolved", "record": "20990101-act-1", "revision": REV, "commit": c1,
                        "path": "versions/" + REV + "/law.yaml", "node": NODE, "text": "架空の雲を保管すろ。\n"}}, True)
    add("common", "Revision参照は最新の記録版に解決する", ["FIXREF-05"], "reference",
        {"kind": "reference", "bundle": bundle, "registry": reg, "reference": ref},
        {"resolution": {"result": "resolved", "record": "20990101-act-1", "revision": REV, "commit": c5}}, True)
    for title, rule, reference in [("commitのないノードの指定", "FIXREF-07", ref + "#" + NODE),
                                   ("短縮したcommit", "FIXREF-04", ref + "@" + c1[:7]),
                                   ("そのcommitにないRevision", "FIXREF-06", "loj:loj/20990101-act-1/zzzzzzzz@" + c1)]:
        dest = next_dir("common", False)
        dest.mkdir(parents=True, exist_ok=True)
        shutil.copy(bundle_pos, dest / "repo.bundle")
        shutil.copytree(registry.parent.parent, dest / "registry", dirs_exist_ok=True)
        add("common", title, list(dict.fromkeys([rule, "FIXREF-06"])), "reference",
            {"kind": "reference", "bundle": rel(dest / "repo.bundle"), "registry": rel(dest / "registry"), "reference": reference},
            {"resolution": {"result": "error"}, "diagnostics": [diag(rule, SV["common"])]}, False)


def main():
    for suite, folder in FOLDER.items():
        for group in ("invalid", "expected"):
            shutil.rmtree(C / folder / group, ignore_errors=True)
    shutil.rmtree(C / "common/v1alpha1/valid", ignore_errors=True)
    history()
    glyphs()
    registry()
    rebuild()
    cross_record()
    changes_and_references()
    for suite, folder in FOLDER.items():
        write_json(C / folder / "manifest.json", {"suite": SV[suite], "cases": INDEX[suite]})
    print("Authored " + ", ".join(f"{k}: {len(v)}" for k, v in INDEX.items()) + "; no validator invoked.")


if __name__ == "__main__":
    main()
