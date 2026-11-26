"""Hand-authored cases for the history, glyph, registry, rebuild and common suites.

Authoring helper (O-15). Not a validator: each negative case is a copy of a
checked-in positive input with one hand-written change, and its expected rule
and result are written here by hand from the spec text. Each copy is listed in
the index (derivedFrom: its source and the changes), and verify.py rebuilds it
from the source to find copies left behind by a changed source (CONF-01).
The fictional Git history for the change and reference cases is built with
fixed authors and dates so that the bundle and the commit hashes are
reproducible.
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
POS_016 = "conformance/loj-history/v1alpha1/valid/hist-016/repo"
REG_POS = "conformance/loj-registry/v1alpha1/valid/reg-001/registry"
# loj-registry/v1alpha2 (draft): the positive is a hand-written copy of REG_POS with names (REG-06).
REG2_POS = "conformance/loj-registry/v1alpha2/valid/reg-001/registry"
SV = {"hist": "loj-history/v1alpha1", "glyph": "loj-glyphs/v1alpha1", "reg": "loj-registry/v1alpha1",
      "rebuild": "loj-rebuild/v1alpha1", "pkg": "loj/v1alpha2", "common": "common/v1alpha1",
      "reg2": "loj-registry/v1alpha2"}
FOLDER = {"hist": "loj-history/v1alpha1", "glyph": "loj-glyphs/v1alpha1", "reg": "loj-registry/v1alpha1",
          "rebuild": "loj-rebuild/v1alpha1", "common": "common/v1alpha1", "reg2": "loj-registry/v1alpha2"}
# Case ID prefix of a suite key, when it differs from the key (both registry versions use reg-NNN).
PREFIX = {"reg2": "reg"}
INDEX = {key: [] for key in FOLDER}
# CONF-01: the source and the changes of every copied input, by the copy's path; add() moves them to the index.
DERIVED = {}
ZWG = "versions/zwgmz1rt/"
# CONF-01: negatives whose input breaks the schema of its schemaVersion. Written by hand: the schema error
# of each one was checked to be the violation of the case's expected rule (law-of-japan/loj-spec#32).
SCHEMA_REJECTED = {"hist-005", "hist-006", "hist-010", "hist-012", "hist-013", "hist-020", "hist-021", "hist-022",
                   "hist-026", "hist-038", "hist-041", "hist-042", "hist-043", "hist-045", "hist-046", "glyph-005", "reg-005",
                   "reg-006", "reg-007", "reg-010", "rebuild-002", "hist-056", "hist-057", "hist-058", "hist-059",
                   "hist-060", "hist-061", "rebuild-005", "reg-013", "glyph-014", "glyph-015",
                   "glyph-016", "glyph-019", "hist-068", "glyph-033", "reg-015", "rebuild-006", "reg-016", "rebuild-007"}
# The same for loj-registry/v1alpha2, whose case IDs repeat those of v1alpha1.
SCHEMA_REJECTED_REG2 = {"reg-004", "reg-005", "reg-006"}


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes((json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))


def mutate(dest, source, edits, files=None):
    """Copy the directory source to dest, replace the first old with new in order, then write whole files."""
    source = source if isinstance(source, str) else rel(source)
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(ROOT / source, dest)
    record = []
    for name, old, new in edits:
        path = dest / name
        text = path.read_bytes().decode("utf-8")
        assert old and old in text, (dest, name, old)  # the index schema requires a non-empty old
        path.write_bytes(text.replace(old, new, 1).encode("utf-8"))
        record.append({"file": name, "old": old, "new": new})
    for name, body in (files or {}).items():
        (dest / name).write_bytes(body.encode("utf-8"))
        record.append({"file": name, "content": body})
    DERIVED[rel(dest)] = {"path": rel(dest), "from": source, "edits": record}


def copy_file(dest, source):
    """Copy one file (a git bundle) unchanged."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(source, dest)
    DERIVED[rel(dest)] = {"path": rel(dest), "from": rel(source), "edits": []}


def diag(rule, schema_version, klass="error"):
    return {"rule": rule, "schemaVersion": schema_version, "class": klass}


def add(suite, title, requirements, check, inp, expected, success, category=None, normative=True):
    ident = "%s-%03d" % (PREFIX.get(suite, suite), len(INDEX[suite]) + 1)
    exp_path = "conformance/%s/expected/%s.json" % (FOLDER[suite], ident)
    write_json(ROOT / exp_path, expected)
    case = {"id": ident, "title": title, "requirements": requirements, "check": check}
    if category:
        case["category"] = category
    case.update({"normative": normative, "input": inp, "expected": exp_path, "success": success})
    if ident in (SCHEMA_REJECTED_REG2 if suite == "reg2" else SCHEMA_REJECTED):
        assert not success, ident
        case["rejectedBy"] = "schema"
    # A copy belongs to the case whose directory holds it; other cases may read it as a shared input.
    own = "conformance/%s/%s/%s/" % (FOLDER[suite], "valid" if success else "invalid", ident)
    paths = [inp[key] for key in ("path", "registry", "bundle") if key in inp] + inp.get("repositories", [])
    derived = [DERIVED.pop(path) for path in paths if path.startswith(own) and path in DERIVED]
    if derived:
        case["derivedFrom"] = derived
    INDEX[suite].append(case)
    return ident


def next_dir(suite, success):
    ident = "%s-%03d" % (PREFIX.get(suite, suite), len(INDEX[suite]) + 1)
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
        # TIME-06 makes TYPE-05 apply to time points; TYPE-05 stays the rule of the diagnostic.
        requirements = [rule, "TIME-06"] if rule == "TYPE-05" else [rule]
        add("hist", title, requirements, "L3", {"kind": "repository", "path": rel(dest)},
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
    dest = next_dir("hist", False) / "repo"
    mutate(dest, "conformance/loj-history/v1alpha1/valid/hist-004/repo",
           [("history.yaml", '          value: "2019-05-01"\n', "")])
    add("hist", "確定日の基準から計算したvalueの書き漏らし", ["TIME-03"], "L3", {"kind": "repository", "path": rel(dest)},
        {"results": [l3("historyStructure", "fail")], "diagnostics": [diag("TIME-03", SV["common"])]}, False,
        "historyStructure")
    fixed_pos = "conformance/loj-history/v1alpha1/valid/hist-019/repo"
    add("hist", "Sourceのfixedに書く固定参照と外部の資料の固定（架空）", ["FIXREF-01", "TYPE-02"], "L3",
        {"kind": "repository", "path": fixed_pos}, {"results": [l3("evidence")]}, True, "evidence")
    for title, rule, edits in [
        ("固定参照の短縮したcommit", "FIXREF-04", [("history.yaml", "commit: f1162fe2cfefa04e9a0d656706e37977fb3d0731", "commit: f1162fe")]),
        ("revisionのない固定参照", "FIXREF-03", [("history.yaml", "      revision: b7k2m9qd\n", "")]),
        ("LoJの中の資料を文字列で固定する", "TYPE-02", [("history.yaml",
                                     "    fixed:\n      record: {id: 20990101-act-1, label: 架空法律第一号}\n      revision: b7k2m9qd\n"
                                     "      commit: f1162fe2cfefa04e9a0d656706e37977fb3d0731\n"
                                     "      node: 20990101-act-1/main/article/1/paragraph/1\n",
                                     "    fixed: loj:loj/20990101-act-1/b7k2m9qd@f1162fe2cfefa04e9a0d656706e37977fb3d0731\n")]),
    ]:
        dest = next_dir("hist", False) / "repo"
        mutate(dest, fixed_pos, edits)
        add("hist", title, sorted({"FIXREF-01", rule}), "L3", {"kind": "repository", "path": rel(dest)},
            {"results": [l3("evidence", "fail")], "diagnostics": [diag(rule, SV["common"])]}, False, "evidence")
    for title, rule, edits in [
        ("既定と違う版パッケージのパス", "HIST-08", [("history.yaml", "      glyphNotes: versions/zwgmz1rt/glyphs.yaml\n",
                                                "      package: versions/98mj5vgx/law.yaml\n      glyphNotes: versions/zwgmz1rt/glyphs.yaml\n")]),
        ("撤回したRevisionを基礎状態とする有効なRevision", "HIST-04",
         [("history.yaml", "      glyphNotes: versions/98mj5vgx/glyphs.yaml\n    status: active\n",
           "      glyphNotes: versions/98mj5vgx/glyphs.yaml\n    status: retracted\n")]),
        ("撤回した関係を成立根拠とする有効なRevision", "HIST-05",
         [("history.yaml", "    verification: {state: confirmed}\n    status: active\n",
           "    verification: {state: retracted, reason: 適合ケースのために撤回した}\n    status: retracted\n")]),
        # An enactment basis has no effective to compare, so only "an origin has no basis" is broken.
        ("成立根拠を持つ起点", "HIST-05", [("history.yaml", "    origin: enactment\n",
                                       "    origin: enactment\n    basis: [{enactment: {scope: {text: 全部}, "
                                       "evidence: [{source: src-kanpo-19480720, locator: 1コマ}]}}]\n")]),
    ]:
        dest = next_dir("hist", False) / "repo"
        mutate(dest, HIST_POS, edits)
        add("hist", title, [rule], "L3", {"kind": "repository", "path": rel(dest)},
            {"results": [l3("historyStructure", "fail")], "diagnostics": [diag(rule, SV["hist"])]}, False,
            "historyStructure")
    # 2026-11-11 (#19): promulgation of the from-law later than the effective time (HIST-06).
    late = ('      value: "2099-06-01"\n      raw: 令和八十一年六月一日\n      precision: day\n      evidence: [{source: src-fictional, locator: 公布の日}]\n',
            '      value: "2099-08-01"\n      raw: 令和八十一年八月一日\n      precision: day\n      evidence: [{source: src-fictional, locator: 公布の日}]\n')
    dest = next_dir("hist", True) / "repo"
    mutate(dest, POS_016, [("history.yaml",) + late])
    add("hist", "施行時点より後の公布で遡及の根拠がない（架空）", ["HIST-06", "HIST-03"], "L3",
        {"kind": "repository", "path": rel(dest)},
        {"results": [l3("historyStructure")], "diagnostics": [diag("HIST-06", SV["hist"], "warning")]}, True,
        "historyStructure")
    dest = next_dir("hist", True) / "repo"
    mutate(dest, POS_016, [("history.yaml",) + late,
                           ("history.yaml", "      - id: i1\n        scope: {text: 第一条}\n",
                            "      - id: i1\n        scope: {text: 第一条}\n"
                            "        retroactive:\n          raw: この法律は、令和八十一年七月一日から適用する\n"
                            "          evidence: [{source: src-fictional, locator: 附則第二項}]\n")])
    add("hist", "施行時点より後の公布で遡及の根拠がある（架空）", ["HIST-06", "HIST-03"], "L3",
        {"kind": "repository", "path": rel(dest)}, {"results": [l3("historyStructure")]}, True, "historyStructure")
    # 2026-11-12 (#24): Scope nodes of a version whose L1 fails, and nodes that do not exist (TYPE-07).
    nodes = ("      - id: i1\n        scope: {text: 第二条成人の日の項の次に建国記念の日の項を加える}\n",
             "      - id: i1\n        scope:\n          text: 第二条成人の日の項の次に建国記念の日の項を加える\n"
             "          nodes: [19480720-law-178/main/article/{}]\n")
    dest = next_dir("hist", False) / "repo"
    mutate(dest, HIST_POS, [("history.yaml", nodes[0], nodes[1].format("2")), (ZWG + "main.md", "## 第三條", "## 三")])
    add("hist", "版パッケージのL1が不合格のときのScopeのノード", ["TYPE-07", "TYPE-08", "VAL-02", "VAL-04", "VAL-05"], "L3",
        {"kind": "repository", "path": rel(dest)},
        {"results": [{"check": "L1", "result": "fail"}, l3("evidence", "incomplete"), l3("historyStructure")],
         "diagnostics": [diag("HEAD-01", SV["pkg"])]}, False, "evidence")
    dest = next_dir("hist", False) / "repo"
    mutate(dest, HIST_POS, [("history.yaml", nodes[0], nodes[1].format("9"))])
    add("hist", "版に存在しないScopeのノード", ["TYPE-07"], "L3", {"kind": "repository", "path": rel(dest)},
        {"results": [l3("evidence", "fail")], "diagnostics": [diag("TYPE-07", SV["common"])]}, False, "evidence")


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
    # GLYPH-11: U+FA11 is in the compatibility block but has no canonical decomposition (#21).
    dest = next_dir("glyph", True) / "repo"
    mutate(dest, HIST_POS, [(ZWG + "main.md", "元日\n", "元日" + chr(0xFA11) + "\n")])
    add("glyph", "正規分解を持たない互換漢字のブロックの字（U+FA11）に注記がない", ["GLYPH-11", "VAL-08"], "L3",
        {"kind": "repository", "path": rel(dest)}, {"results": [l3("evidence")]}, True, "evidence")
    # GLYPH-10: verified glyphs need a Source with glyphPreservation: preserved (#21).
    dest = next_dir("glyph", False) / "repo"
    mutate(dest, HIST_POS, [("history.yaml", "    glyphPreservation: preserved\nrelations:\n", "relations:\n"),
                            ("history.yaml", "      glyphCheck: unverified\n      glyphNotes: versions/zwgmz1rt/",
                             "      glyphCheck: verified\n      glyphNotes: versions/zwgmz1rt/")])
    add("glyph", "字体を保持する資料を指さずに字体を照合済みにする", ["GLYPH-10", "TYPE-02"], "L3",
        {"kind": "repository", "path": rel(dest)},
        {"results": [l3("evidence", "fail")], "diagnostics": [diag("GLYPH-10", SV["glyph"])]}, False, "evidence")


# --- loj-registry ------------------------------------------------------------
def registry():
    add("reg", "登録台帳の六つのRecord", ["REG-01", "REG-02", "REG-03", "REG-05", "RID-02"], "registry",
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


def registry_names():
    """loj-registry/v1alpha2 (draft): names (REG-06). The positive is hand-written; each negative changes it once."""
    add("reg2", "名称を持つRecordと持たないRecord", ["REG-01", "REG-02", "REG-06", "RID-02"], "registry",
        {"kind": "registry", "path": REG2_POS}, {"results": [{"check": "registry", "result": "pass"}]}, True)
    law = "records/19480720-law-178.yaml"
    mine = "records/19490516-law-70.yaml"
    negatives = [
        ("同じ種別と表記の名称が二つ", "REG-06", [(law, "    value: 祝日法\n", "    value: 国民祝日法\n")]),
        ("名称のidの重複", "REG-06", [(law, "  - id: m2\n", "  - id: m1\n")]),
        ("定めのない名称の種別", "REG-06", [(law, "    kind: abbreviation\n    value: 祝日法\n",
                                         "    kind: nickname\n    value: 祝日法\n")]),
        # unverified, so that only REG-06 applies: a confirmed claim with no evidence also breaks TYPE-05.
        ("根拠のない未確認の名称", "REG-06", [(law, "    value: 祝日法\n    evidence: [{source: src-egov, locator: 法令略称}]\n"
                                           "    verification: {state: confirmed}\n",
                                           "    value: 祝日法\n    evidence: []\n"
                                           "    verification: {state: unverified, reason: 根拠の資料を記録していない}\n")]),
        ("名称の一覧がない", "REG-02", [(mine, "names: []\n", "")]),
    ]
    for title, rule, edits in negatives:
        dest = next_dir("reg2", False) / "registry"
        mutate(dest, REG2_POS, edits)
        add("reg2", title, [rule], "registry", {"kind": "registry", "path": rel(dest)},
            {"results": [{"check": "registry", "result": "fail"}], "diagnostics": [diag(rule, SV["reg2"])]}, False)


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
         "references": [{"target": "loj:loj/20170616-law-63", "result": "resolved"}]}, True, "timeConsistency")
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
         "references": [{"target": "loj:loj/20170616-law-63/q3c8h0tw", "result": "notFetched"}]}, True, "timeConsistency")


# --- common: change kinds and fixed references -------------------------------
FIX_LAW = {"id": "20990101-act-1", "title": "架空雲保管法（実在しないサンプル）", "type": "act", "number": "架空法律第一号",
           "promulgatedAt": "2099-01-01", "language": "ja"}
REV = "b7k2m9qd"
# The kind of a build_bundle step whose subject is the whole commit message, written as given (CHG-03 syntax).
RAW = "raw"
NODE = "20990101-act-1/main/article/1/paragraph/1"
# build_bundle steps that make no commit: create a branch at HEAD and switch to it, or switch to a branch (CHG-03 merge).
BRANCH = "branch"
CHECKOUT = "checkout"
# A key of the files of a build_bundle step, not a path: the paths to record with the Git mode 100755 (executable).
# Every other file is recorded as 100644, so a file leaves EXECUTABLE to go back to a regular file (CHG-02).
EXECUTABLE = "<executable>"


class Merge:
    """The files of a build_bundle step that merges the named branch into HEAD with a merge commit (two parents)."""
    def __init__(self, branch):
        self.branch = branch


def fictional_files(body1, files_split=False, label="制定", locator="本則"):
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
               "      sources: [{source: src-fiction, locator: " + locator + "}]\n      glyphCheck: unverified\n    status: active\n"
               "coverage: {state: unconfirmed}\n")
    out = {"history.yaml": history, "versions/" + REV + "/law.yaml": json.dumps(law, ensure_ascii=False, indent=2) + "\n"}
    out.update({"versions/" + REV + "/" + k: v for k, v in md.items()})
    return out


def build_bundle(path, steps=None, verbatim=False):
    """Build a git bundle of the branch main from steps; return the hash of each commit, in the order of the steps.

    A step is (subject, kind, with_revs, files, *trailers), or (BRANCH, name) and (CHECKOUT, name), which make no
    commit. files is the whole set of files to write (a value of None deletes that file), or Merge(branch) for a merge commit of that branch. The modes
    are set in the index, not read from the working tree, so the bundle is the same on every system (EXECUTABLE).
    The date of a commit is fixed by the number of its step, counting the steps that make no commit, so a step
    put in before others changes the hashes of the commits after it. The bundle holds main only: a branch must
    be merged into main, or its commits are left out.
    """
    steps = steps if steps is not None else [
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
        git = lambda *args, **kw: subprocess.run(["git", "-C", str(repo), "-c", "commit.gpgsign=false", *args], check=True, capture_output=True, env=env, **kw)
        git("init", "-q", "-b", "main")
        git("config", "core.autocrlf", "false")
        git("config", "core.filemode", "false")
        for i, step in enumerate(steps):
            if step[0] in (BRANCH, CHECKOUT):
                git("checkout", "-q", *(["-b"] if step[0] == BRANCH else []), step[1])
                continue
            subject, kind, with_revs, files, *extra = step
            # Further trailers follow a declaration: a step without a kind, or with the whole message (RAW), has none.
            assert kind not in (None, RAW) or not extra, subject
            if isinstance(files, Merge):
                # --no-ff keeps two parents even when HEAD could fast-forward; the commit below records the merge.
                git("merge", "-q", "--no-ff", "--no-commit", files.branch)
            else:
                for old in repo.glob("versions/*/*.md"):
                    old.unlink()
                for name, body in files.items():
                    if name == EXECUTABLE:
                        continue
                    target = repo / name
                    # None deletes the file (a step that removes a version package, CHG-03 revert).
                    if body is None:
                        target.unlink(missing_ok=True)
                        continue
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(body.encode("utf-8"))
                git("add", "-A")
                executable = set(files.get(EXECUTABLE, ()))
                listed = git("ls-files", "-s", "-z").stdout.decode("utf-8").split("\0")
                staged = [line.split("\t", 1) for line in listed if line]
                demote = [name for info, name in staged if info.split()[0] == "100755" and name not in executable]
                for flag, names in (("--chmod=+x", sorted(executable)), ("--chmod=-x", demote)):
                    if names:
                        git("update-index", flag, "--", *names)
            message = subject if kind == RAW else subject + "\n"
            if kind and kind != RAW:
                message += "\nLoJ-Change: " + kind + "\n" + ("LoJ-Revisions: " + REV + "\n" if with_revs else "")
                # Further trailers (CHG-04: LoJ-Reviewed) follow the declaration; a step without a kind has none.
                message += "".join(extra)
            date = "2099-01-%02dT00:00:00+0900" % (i + 1)
            env["GIT_AUTHOR_DATE"] = env["GIT_COMMITTER_DATE"] = date
            # verbatim keeps blanks at the end of a trailer line (CHG-03: a value of only blanks is empty).
            git("commit", "-q", *(["--cleanup=verbatim"] if verbatim else []), "-F", "-", input=message.encode("utf-8"))
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
        copy_file(dest, bundle_pos)
        add("common", title, [rule], "change", {"kind": "change", "bundle": rel(dest), "base": base, "head": head},
            {"results": [{"check": "change", "result": "fail"}], "diagnostics": [diag(rule, SV["common"])]}, False)
    registry = next_dir("common", True) / "registry/records/20990101-act-1.yaml"
    registry.parent.mkdir(parents=True, exist_ok=True)
    registry.write_bytes(("schemaVersion: loj-registry/v1alpha1\nid: 20990101-act-1\nlabel: 架空雲保管法\nstatus: active\n"
                          "identity:\n  evidence: [{source: src-fiction, locator: 題名}]\n  verification: {state: confirmed}\n"
                          "collection: {state: collected}\nrepository: {location: example.invalid/20990101-act-1, canonicalBranch: main}\n"
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
        copy_file(dest / "repo.bundle", bundle_pos)
        mutate(dest / "registry", reg, [])
        add("common", title, list(dict.fromkeys([rule, "FIXREF-06"])), "reference",
            {"kind": "reference", "bundle": rel(dest / "repo.bundle"), "registry": rel(dest / "registry"), "reference": reference},
            {"resolution": {"result": "error"}, "diagnostics": [diag(rule, SV["common"])]}, False)


# --- common: L4 display and promulgation (2026-11-11, #13 and #19) ---------------
def fictional_record(folder, ident, label, repository):
    body = ("schemaVersion: loj-registry/v1alpha1\nid: " + ident + "\nlabel: " + label + "\nstatus: active\n"
            "identity:\n  evidence: [{source: src-fictional, locator: 題名}]\n  verification: {state: confirmed}\n"
            "collection: {state: notCollected}\n")
    if repository:
        body += "repository: {location: example.invalid/" + ident + ", canonicalBranch: main}\n"
    body += "sources:\n  - {id: src-fictional, kind: other, title: 適合ケースのための架空の資料}\nnumbers: []\nexternalIds: []\n"
    path = folder / "records" / (ident + ".yaml")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(body.encode("utf-8"))


def display_and_promulgation():
    display = {"check": "L4", "category": "displayConsistency", "result": "pass"}
    add("common", "版パッケージの番号と採用中の番号主張（祝日法）", ["XREF-05", "MAN-01", "REG-03"], "L4",
        {"kind": "records", "registry": REG_POS, "repositories": [HIST_POS]}, {"results": [display]}, True,
        "displayConsistency")
    dest = next_dir("common", True) / "hist-001"
    mutate(dest, HIST_POS, [(ZWG + "law.yaml", '"昭和二十三年法律第百七十八号"', '"昭和二十三年法律第百七十九号"')])
    add("common", "版パッケージの番号が採用中の番号主張と食い違う", ["XREF-05", "MAN-01"], "L4",
        {"kind": "records", "registry": REG_POS, "repositories": [rel(dest)]},
        {"results": [display], "diagnostics": [diag("XREF-05", SV["common"], "warning")]}, True, "displayConsistency")
    base = next_dir("common", True)
    registry = base / "registry"
    fictional_record(registry, "20990401-law-1", "架空の法律（時点の計算の例）", True)
    fictional_record(registry, "20990402-law-3", "架空の法律（公布の時点の比較の例）", True)
    fictional_record(registry, "20990601-law-2", "架空の改正法", False)
    other = base / "hist-016b"
    mutate(other, POS_016, [("history.yaml", "record: {id: 20990401-law-1, label: 架空の法律（時点の計算の例）}",
                             "record: {id: 20990402-law-3, label: 架空の法律（公布の時点の比較の例）}")])
    time = {"check": "L4", "category": "timeConsistency"}
    add("common", "同じ改正法令の公布の時点が一致する（架空）", ["XREF-06", "HIST-03"], "L4",
        {"kind": "records", "registry": rel(registry), "repositories": [POS_016, rel(other)]},
        {"results": [dict(time, result="pass")]}, True, "timeConsistency")
    dest = next_dir("common", False) / "hist-016b"
    mutate(dest, rel(other), [("history.yaml", '      value: "2099-06-01"\n      raw: 令和八十一年六月一日\n',
                               '      value: "2099-06-02"\n      raw: 令和八十一年六月二日\n')])
    add("common", "同じ改正法令の公布の時点が食い違う（架空）", ["XREF-06"], "L4",
        {"kind": "records", "registry": rel(registry), "repositories": [POS_016, rel(dest)]},
        {"results": [dict(time, result="fail")], "diagnostics": [diag("XREF-06", SV["common"])]}, False,
        "timeConsistency")


OLD_LAW = ("20990101-law-5", "架空の旧法（全部改正の例）")
NEW_LAW = ("20991001-law-9", "架空の新法（全部改正の例）")
FICT = "      evidence: [{source: src-fictional, locator: %s}]\n      verification: {state: unverified, reason: 架空の資料}\n"


def total_revision_files(base):
    """Old and new fictional Records of one total revision (HIST-04, HIST-12)."""
    old = ("schemaVersion: loj-history/v1alpha1\nrecord: {id: %s, label: %s}\n" % OLD_LAW
           + "sources:\n  - {id: src-fictional, kind: other, title: 適合ケースのための架空の資料}\n"
           "relations:\n  - id: rel-total\n    type: totallyRevises\n    from: {id: %s, label: %s}\n" % NEW_LAW
           + "    evidence: [{source: src-fictional, locator: 附則第一条}]\n"
           "    verification: {state: unverified, reason: 架空の資料}\n    status: active\n    items:\n"
           "      - id: i1\n        scope: {text: 全部}\n        effective:\n          state: date\n"
           '          value: "2099-10-01"\n          raw: 令和八十一年十月一日\n          precision: day\n'
           "          evidence: [{source: src-fictional, locator: 附則第一条}]\n"
           "          verification: {state: unverified, reason: 架空の資料}\n"
           "        evidence: [{source: src-fictional, locator: 附則第一条}]\n"
           "        verification: {state: unverified, reason: 架空の資料}\n"
           "revisions:\n  - id: 2p6r8v4x\n    origin: coverageStart\n"
           "    effective: {state: unknown, reason: 適合ケースで省略}\n    applicability: {state: unsurveyed}\n"
           "    text: {status: absent}\n    status: active\n"
           "termination:\n  - {type: totallyRevised, relation: rel-total}\n"
           "coverage: {state: unconfirmed}\n")
    new = ("schemaVersion: loj-history/v1alpha1\nrecord: {id: %s, label: %s}\n" % NEW_LAW
           + "sources:\n  - {id: src-fictional, kind: other, title: 適合ケースのための架空の資料}\n"
           "relations: []\n"
           "revisions:\n  - id: 7c3j5m9q\n    origin: totalRevision\n"
           "    totallyRevises: {record: {id: %s, label: %s}, relation: rel-total}\n" % OLD_LAW
           + "    effective:\n      state: date\n      value: \"2099-10-01\"\n      raw: 令和八十一年十月一日\n"
           "      precision: day\n" + FICT % "附則第一条"
           + "    applicability: {state: unsurveyed}\n    text: {status: absent}\n    status: active\n"
           "coverage: {state: unconfirmed}\n")
    for ident, body in ((OLD_LAW[0], old), (NEW_LAW[0], new)):
        path = base / ident / "history.yaml"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(body.encode("utf-8"))
    fictional_record(base / "registry", OLD_LAW[0], OLD_LAW[1], True)
    fictional_record(base / "registry", NEW_LAW[0], NEW_LAW[1], True)


def total_revision():
    base = next_dir("common", True)
    total_revision_files(base)
    registry, old, new = rel(base / "registry"), rel(base / OLD_LAW[0]), rel(base / NEW_LAW[0])
    resolution = {"check": "L4", "category": "relationResolution"}
    consistency = {"check": "L4", "category": "relationConsistency"}
    add("common", "全部改正後のRecordと旧Recordの全部改正の関係が対応する（架空）", ["XREF-01", "XREF-02", "HIST-04"], "L4",
        {"kind": "records", "registry": registry, "repositories": [old, new]},
        {"results": [dict(resolution, result="pass"), dict(consistency, result="pass")]}, True, "relationConsistency")
    dest = next_dir("common", False) / NEW_LAW[0]
    mutate(dest, new, [("history.yaml", "relation: rel-total}", "relation: rel-nowhere}")])
    add("common", "totallyRevisesが旧Recordにない関係を指す（架空）", ["XREF-02"], "L4",
        {"kind": "records", "registry": registry, "repositories": [old, rel(dest)]},
        {"results": [dict(consistency, result="fail")], "diagnostics": [diag("XREF-02", SV["common"])]}, False,
        "relationConsistency")
    dest = next_dir("common", False)
    mutate(dest / "registry", registry, [("records/%s.yaml" % NEW_LAW[0], "status: active\n", "status: withdrawn\n")])
    mutate(dest / OLD_LAW[0], old, [("history.yaml", "    verification: {state: unverified, reason: 架空の資料}\n    status: active\n",
                                     "    verification: {state: confirmed}\n    status: active\n")])
    add("common", "確定した関係の起点が登録を撤回したRecord（架空）", ["XREF-01", "REG-02", "VAL-06"], "L4",
        {"kind": "records", "registry": rel(dest / "registry"), "repositories": [rel(dest / OLD_LAW[0]), new]},
        {"results": [dict(resolution, result="fail")], "diagnostics": [diag("XREF-01", SV["common"])],
         "references": [{"target": "loj:loj/" + NEW_LAW[0], "result": "nonexistentConfirmed"}]}, False,
        "relationResolution")
    # The old Record's relation is changed instead of the reference (XREF-02: status and type).
    for title, *edits in [
        # HIST-12: retracting the relation removes the termination item in the same change.
        ("totallyRevisesが撤回した関係を指す（架空）",
         ("    verification: {state: unverified, reason: 架空の資料}\n    status: active\n",
          "    verification: {state: unverified, reason: 架空の資料による撤回}\n    status: retracted\n"),
         ("termination:\n  - {type: totallyRevised, relation: rel-total}\n", "")),
        # HIST-12: the termination follows the relation type, so that only XREF-02 is broken.
        ("totallyRevisesが全部改正でない関係を指す（架空）", ("    type: totallyRevises\n", "    type: repeals\n"),
         ("type: totallyRevised, relation", "type: repealed, relation")),
        ("全部改正の関係の起点が別のRecord（架空）", ("    from: {id: %s, label: %s}\n" % NEW_LAW,
                                                      "    from: {id: %s, label: %s}\n" % OLD_LAW)),
    ]:
        dest = next_dir("common", False) / OLD_LAW[0]
        mutate(dest, old, [("history.yaml", a, b) for a, b in edits])
        add("common", title, ["XREF-02"], "L4",
            {"kind": "records", "registry": registry, "repositories": [rel(dest), new]},
            {"results": [dict(consistency, result="fail")], "diagnostics": [diag("XREF-02", SV["common"])]}, False,
            "relationConsistency")
    # Boundary of XREF-01: a withdrawn Record referenced by an unconfirmed relation is not a violation.
    dest = next_dir("common", True) / "registry"
    mutate(dest, registry, [("records/%s.yaml" % NEW_LAW[0], "status: active\n", "status: withdrawn\n")])
    add("common", "未確認の関係の起点が登録を撤回したRecord（架空）", ["XREF-01", "VAL-06"], "L4",
        {"kind": "records", "registry": rel(dest), "repositories": [old, new]},
        {"results": [dict(resolution, result="pass")],
         "references": [{"target": "loj:loj/" + NEW_LAW[0], "result": "nonexistentConfirmed"}]}, True,
        "relationResolution")


def change_dependents():
    """CHG-02: a correction that also updates a dependent file (text.sources of the same Revision)."""
    bundle = next_dir("common", True) / "repo.bundle"
    c1, c2 = build_bundle(bundle, [
        ("制定時の版を加える", "revisionAdd", True, fictional_files("架空の雲を保管すろ。\n")),
        ("第一条の誤転記を直し、本文の出典の箇所を改める", "correction", True,
         fictional_files("架空の雲を保管する。\n", locator="本則第一条")),
    ])
    add("common", "記録訂正で、同じ版の本文の出典（history.yamlのtext.sources）を併せて更新する", ["CHG-02", "CHG-03"], "change",
        {"kind": "change", "bundle": rel(bundle), "base": c1, "head": c2},
        {"results": [{"check": "change", "result": "pass"}]}, True)


ROW_LAW = ("20990201-act-2", "架空雲分類法（実在しないサンプル）")
ROW_REVS = ["c4f7h2k9", "d5g8j3m6", "e6h9k4n7"]
CLOUDS = {"a1b2": "積雲", "c3d4": "層雲", "e5f6": "巻雲"}


def row_key_files(base, key_sets, partial=None):
    """Three fictional versions of one table (TABLE-02, HIST-13). key_sets: row keys of each version."""
    fict = "      evidence: [{source: src-fiction, locator: %s}]\n      verification: {state: unverified, reason: 架空の資料}\n"
    rels, revs = "", ""
    for i, (rev, keys) in enumerate(zip(ROW_REVS, key_sets)):
        day = "2099-0%d-01" % (i + 2)
        raw = "二千九十九年" + "二三四"[i] + "月一日"
        effective = ("    effective:\n      state: date\n      value: \"" + day + "\"\n      raw: " + raw + "\n"
                     "      precision: day\n" + fict % "施行期日")
        if i:
            rels += ("  - id: rel-%d\n    type: amends\n    from: {id: 2099%02d01-act-%d, label: 架空の改正法}\n" % (i, i + 2, i + 10)
                     + "    evidence: [{source: src-fiction, locator: 本則}]\n"
                     "    verification: {state: unverified, reason: 架空の資料}\n    status: active\n    items:\n"
                     "      - id: i1\n        scope: {text: 第一条の表}\n        effective:\n          state: date\n"
                     "          value: \"" + day + "\"\n          raw: " + raw + "\n          precision: day\n"
                     "          evidence: [{source: src-fiction, locator: 附則}]\n"
                     "          verification: {state: unverified, reason: 架空の資料}\n"
                     "        evidence: [{source: src-fiction, locator: 附則}]\n"
                     "        verification: {state: unverified, reason: 架空の資料}\n")
        revs += "  - id: " + rev + "\n"
        revs += ("    origin: enactment\n" if not i else
                 "    basedOn: " + ROW_REVS[i - 1] + "\n    basis: [{relation: rel-%d, items: [i1]}]\n" % i)
        status = "partial\n      gaps: [{text: 第一条の表の一部}]" if i == partial else "complete"
        revs += (effective + "    applicability: {state: unsurveyed}\n    text:\n      status: " + status + "\n"
                 "      sources: [{source: src-fiction, locator: 本則}]\n      glyphCheck: unverified\n    status: active\n")
        rows = "".join("<!-- loj:row key=" + k + " -->\n<!-- loj:cell -->\n" + CLOUDS[k] + "\n<!-- loj:end-cell -->\n"
                       "<!-- loj:end-row -->\n" for k in keys)
        md = ("# 第一条\n<!-- loj:paragraph number=1 -->\n架空の雲の種類を次のように定める。\n"
              "<!-- loj:table number=1 -->\n" + rows + "<!-- loj:end-table -->\n<!-- loj:end-paragraph -->\n")
        law = {"schemaVersion": "loj/v1alpha2",
               "law": {"id": ROW_LAW[0], "title": ROW_LAW[1], "type": "act", "number": "架空法律第二号",
                       "promulgatedAt": "2099-02-01", "language": "ja"},
               "documents": [{"path": "main.md", "parent": "main"}]}
        folder = base / "versions" / rev
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "law.yaml").write_bytes((json.dumps(law, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
        (folder / "main.md").write_bytes(md.encode("utf-8"))
    history = ("schemaVersion: loj-history/v1alpha1\nrecord: {id: " + ROW_LAW[0] + ", label: 架空雲分類法}\n"
               "sources:\n  - {id: src-fiction, kind: other, title: 適合ケースのための架空の資料}\n"
               "relations:\n" + rels + "revisions:\n" + revs + "coverage: {state: unconfirmed}\n")
    (base / "history.yaml").write_bytes(history.encode("utf-8"))


def row_keys():
    dest = next_dir("hist", True) / "repo"
    row_key_files(dest, [["a1b2", "c3d4"], ["a1b2"], ["a1b2", "e5f6"]])
    add("hist", "削った行のkeyを使わずに行を加える（架空）", ["HIST-13", "TABLE-02"], "L3",
        {"kind": "repository", "path": rel(dest)}, {"results": [l3("historyStructure")]}, True, "historyStructure")
    dest = next_dir("hist", False) / "repo"
    row_key_files(dest, [["a1b2", "c3d4"], ["a1b2"], ["a1b2", "c3d4"]])
    add("hist", "削った行のkeyを後の版で再使用する（架空）", ["HIST-13", "TABLE-02"], "L3",
        {"kind": "repository", "path": rel(dest)},
        {"results": [l3("historyStructure", "fail")], "diagnostics": [diag("HIST-13", SV["hist"])]}, False,
        "historyStructure")
    dest = next_dir("hist", True) / "repo"
    row_key_files(dest, [["a1b2", "c3d4"], ["a1b2"], ["a1b2", "c3d4"]], partial=1)
    add("hist", "本文が一部しかない版で行がなくても、削ったとみなさない（架空）", ["HIST-13", "HIST-08"], "L3",
        {"kind": "repository", "path": rel(dest)}, {"results": [l3("historyStructure")]}, True, "historyStructure")


def termination_retraction():
    """HIST-12: termination does not rest on a retracted relation or on retracted items only."""
    source = "conformance/loj-history/v1alpha1/valid/hist-002/repo"
    item_check = "\n        verification: {state: unverified, reason: 官報と未照合}\n"
    for title, edits in [
        ("撤回した関係を根拠とする効力の終了（架空）",
         [("    verification: {state: unverified, reason: 官報と未照合}\n    status: active\n",
           "    verification: {state: unverified, reason: 適合ケースのための架空の撤回}\n    status: retracted\n")]),
        ("内訳をすべて撤回した関係を根拠とする効力の終了（架空）",
         [(item_check, "\n        verification: {state: retracted, reason: 適合ケースのための架空の撤回}\n")]),
    ]:
        dest = next_dir("hist", False) / "repo"
        mutate(dest, source, [("history.yaml", a, b) for a, b in edits])
        add("hist", title, ["HIST-12"], "L3", {"kind": "repository", "path": rel(dest)},
            {"results": [l3("historyStructure", "fail")], "diagnostics": [diag("HIST-12", SV["hist"])]}, False,
            "historyStructure")
    # One retracted item next to an active one: the time comes from the active item only.
    dest = next_dir("hist", True) / "repo"
    mutate(dest, source, [("history.yaml", item_check + "termination:",
                           item_check
                           + "      - id: i2\n        scope: {text: 第一条}\n        effective:\n          state: date\n"
                           '          value: "1959-04-13"\n          raw: 昭和三十四年四月十三日\n          precision: day\n'
                           "          evidence: [{source: src-egov-s34-122, locator: 附則}]\n"
                           "          verification: {state: unverified, reason: 官報と未照合}\n"
                           "        evidence: [{source: src-egov-s34-122, locator: 第二条}]\n"
                           "        verification: {state: retracted, reason: 適合ケースのための架空の撤回}\n"
                           "termination:")])
    add("hist", "内訳の一部を撤回した関係を根拠とする効力の終了（架空）", ["HIST-12", "HIST-03"], "L3",
        {"kind": "repository", "path": rel(dest)}, {"results": [l3("historyStructure")]}, True, "historyStructure")


# --- 2026-11-12 (#32): common types and time points in the history manifest -----------------
def common_types():
    space = [("history.yaml", "record: {id: 19480720-law-178, label:", "record: {id: 19480720-law-178, space: loj, label:"),
             ("history.yaml", "from: {id: 19660625-act-86, label:", "from: {id: 19660625-act-86, space: loj, label:")]
    external = ("    status: active\ncoverage:",
                "    externalIds:\n      - issuer: egov\n        kind: {}\n        value: 323AC1000000178_19660625_341AC0000000086\n"
                "        evidence: [{{source: src-egov, locator: 法令履歴}}]\n"
                "        verification: {{state: unverified, reason: 適合ケースのための形の例（e-Govと未照合）}}\n"
                "    status: active\ncoverage:")
    dest = next_dir("hist", True) / "repo"
    mutate(dest, HIST_POS, space + [("history.yaml", external[0], external[1].format("revision"))])
    add("hist", "登録空間を書いたRecordの参照と、版の外部識別子", ["HIST-09", "RID-04", "TYPE-01", "TYPE-03", "TYPE-04"], "L3",
        {"kind": "repository", "path": rel(dest)}, {"results": [l3("historyStructure"), l3("evidence")]}, True,
        "historyStructure")
    enacted_base = ("      base:\n        state: date\n        value: \"1948-07-20\"\n        raw: 昭和二十三年七月二十日\n"
                    "        precision: day\n        evidence: [{source: src-kanpo-19480720, locator: 1コマ 発行日}]\n"
                    "        verification: {state: confirmed}\n")
    pending_base = ("      base:\n        state: pending\n        raw: 別に政令で定める日\n"
                    "        delegation: {raw: 別に政令で定める日, evidence: [{source: src-kanpo-19480720, locator: 附則第一項}]}\n"
                    "        evidence: [{source: src-kanpo-19480720, locator: 附則第一項}]\n"
                    "        verification: {state: unverified, reason: 適合ケースのための架空の変更}\n")
    for title, rule, edits in [
        ("リポジトリの所在で指すRecord", "TYPE-01",
         [("history.yaml", "from: {id: 19660625-act-86, label:", "from: {id: https://github.com/law-of-japan/19660625-act-86, label:")]),
        ("ファイルの中で重複するSourceのid", "HIST-02",
         [("history.yaml", "relations:\n", "  - id: src-goshomei\n    kind: other\n    title: 同じidの別の資料（適合ケース）\nrelations:\n")]),
        ("同じファイルにないSourceを指すEvidence", "TYPE-03",
         [("history.yaml", "{source: src-kanpo-19480720, locator: 附則第一項}", "{source: src-kanpo-19480721, locator: 附則第一項}")]),
        ("Verificationの未知の状態", "TYPE-04",
         [("history.yaml", "    verification: {state: confirmed}\n    status: active\n    items:",
           "    verification: {state: checked}\n    status: active\n    items:")]),
        ("原文のないScope", "TYPE-06",
         [("history.yaml", "scope: {text: 第二条秋分の日の項の次に体育の日の項を加える}", "scope: {nodes: [19480720-law-178/main/article/2]}")]),
        # The promulgation of a relation is no base of a derived time point, so TIME-03 does not follow.
        ("精度と書式が合わない日付", "TIME-02",
         [("history.yaml", "      raw: 昭和四十一年六月二十五日\n      precision: day\n",
           "      raw: 昭和四十一年六月二十五日\n      precision: month\n")]),
        ("確定日でない基準から計算したvalue（pendingの基準）", "TIME-03", [("history.yaml", enacted_base, pending_base)]),
        ("日の書式でないderivedのvalue", "TIME-03",
         [("history.yaml", '      value: "1948-07-20"\n      raw: 公布の日からこれを施行する\n',
           '      value: "1948-07"\n      raw: 公布の日からこれを施行する\n')]),
        ("版を対象としない外部識別子", "HIST-01", [("history.yaml", external[0], external[1].format("record"))]),
    ]:
        dest = next_dir("hist", False) / "repo"
        mutate(dest, HIST_POS, edits)
        sv = SV["common"] if rule.startswith(("TIME", "TYPE")) else SV["hist"]
        category = "evidence" if rule.startswith("TYPE") else "historyStructure"
        # HIST-01 is the source of the ban on Record identifiers in the history manifest; HIST-09 restates it.
        requirements = ["HIST-01", "HIST-09"] if rule == "HIST-01" else [rule]
        add("hist", title, requirements, "L3", {"kind": "repository", "path": rel(dest)},
            {"results": [l3(category, "fail")], "diagnostics": [diag(rule, sv)]}, False, category)


# --- 2026-11-12 (#32): parts of HIST-04, HIST-05 and HIST-08 that had no case -------------------
def history_gaps():
    package_text = ("    text:\n      status: complete\n      sources:\n        - {source: src-goshomei-s41-86, locator: 2画像 本則（改正の内容）}\n"
                    "      glyphCheck: unverified\n      glyphNotes: versions/zwgmz1rt/glyphs.yaml\n"
                    "      correctionsSurveyed: {state: unsurveyed, reason: 官報（昭和41年6月25日）を入手していない（REB-05）}\n")
    duplicate = ("  - id: k3d8w2xn\n    label: 同じ関係と施行時点の二つ目の版（適合ケース）\n    basedOn: zwgmz1rt\n"
                 "    basis: [{relation: rel-s41-86, items: [i1]}]\n    effective:\n      state: derived\n      rule: 公布の日から\n"
                 "      base: {state: date, value: \"1966-06-25\", raw: 昭和四十一年六月二十五日, precision: day,\n"
                 "             evidence: [{source: src-goshomei-s41-86, locator: \"1画像 公布文の日付\"}],\n"
                 "             verification: {state: unverified, reason: 官報の発行日と未照合（REB-05）}}\n"
                 "      value: \"1966-06-25\"\n      raw: この法律は、公布の日から施行する\n"
                 "      evidence: [{source: src-goshomei-s41-86, locator: 附則第一項}]\n      verification: {state: confirmed}\n"
                 "    applicability: {state: unsurveyed}\n    text:\n      status: absent\n    status: active\n")
    item = ("        evidence: [{source: src-goshomei-s41-86, locator: 本則}]\n        verification: {state: confirmed}\n",
            "        evidence: [{source: src-goshomei-s41-86, locator: 本則}]\n"
            "        verification: {state: retracted, reason: 適合ケースのための架空の撤回}\n")
    for title, rule, edits in [
        ("自身のrevision_idのパスでない字体注記", "HIST-08",
         [("history.yaml", "      glyphNotes: versions/zwgmz1rt/glyphs.yaml\n", "      glyphNotes: versions/98mj5vgx/glyphs.yaml\n")]),
        ("本文のない版のディレクトリ", "HIST-08", [("history.yaml", package_text, "    text:\n      status: absent\n")]),
        ("同じ関係・同じ施行時点の二つの有効な版", "HIST-05", [("history.yaml", "coverage:\n", duplicate + "coverage:\n")]),
        ("統合したRevisionを基礎状態とする有効なRevision", "HIST-04",
         [("history.yaml", "      glyphNotes: versions/98mj5vgx/glyphs.yaml\n    status: active\n",
           "      glyphNotes: versions/98mj5vgx/glyphs.yaml\n    status: merged\n    replacedBy:\n      revisions: [zwgmz1rt]\n"
           "      evidence: [{source: src-goshomei-s41-86, locator: 本則}]\n"
           "      verification: {state: unverified, reason: 適合ケースのための架空の統合}\n")]),
        ("撤回した内訳だけを参照する成立根拠", "HIST-05", [("history.yaml",) + item] * 3),
    ]:
        dest = next_dir("hist", False) / "repo"
        mutate(dest, HIST_POS, edits)
        add("hist", title, [rule], "L3", {"kind": "repository", "path": rel(dest)},
            {"results": [l3("historyStructure", "fail")], "diagnostics": [diag(rule, SV["hist"])]}, False,
            "historyStructure")


# --- 2026-11-12 (#32): a merged Record kept in the registry (RID-04, RID-05) ---------------------
def merged_record(space=""):
    return ("schemaVersion: loj-registry/v1alpha1\nid: k7m2p9qd3x\nlabel: 祝日法の重複した登録（架空）\nstatus: merged\n"
            "identity:\n  evidence: [{source: src-fiction, locator: 登録の記録}]\n  verification: {state: confirmed}\n"
            "collection: {state: notCollected}\nsources:\n  - {id: src-fiction, kind: other, title: 架空の登録の記録（適合ケース）}\n"
            "numbers: []\nexternalIds: []\nreplacedBy:\n"
            "  - record: {id: 19480720-law-178, " + space + "label: 昭和二十三年法律第百七十八号}\n"
            "    evidence: [{source: src-fiction, locator: 統合の記録}]\n    verification: {state: confirmed}\n")


def registry_ids():
    for success, title, requirements, space in [
        (True, "統合したRecordを残した登録台帳", ["REG-02", "RID-04", "RID-05"], "space: loj, "),
        (False, "大文字を含む登録空間の識別子", ["RID-04"], "space: LoJ, "),
    ]:
        dest = next_dir("reg", success) / "registry"
        mutate(dest, REG_POS, [], {"records/k7m2p9qd3x.yaml": merged_record(space)})
        if success:
            expected = {"results": [{"check": "registry", "result": "pass"}]}
        else:
            expected = {"results": [{"check": "registry", "result": "fail"}], "diagnostics": [diag("RID-04", SV["reg"])]}
        add("reg", title, requirements, "registry", {"kind": "registry", "path": rel(dest)}, expected, success)


# --- 2026-11-12 (#32): changes over a version whose L1 fails (CHG-04) -----------------------------
def broken(files):
    # HEAD-01: an article heading without its structure label, so the version has no AST.
    return {name: body.replace("# 第一条\n", "# 一\n") for name, body in files.items()}


def change_without_ast():
    body = "架空の雲を保管する。\n"
    bundle_pos = next_dir("common", True) / "repo.bundle"
    c1, c2, c3 = build_bundle(bundle_pos, [
        ("見出しの誤った版を加える", "revisionAdd", True, broken(fictional_files(body))),
        ("ラベルを改める", "metadata", False, broken(fictional_files(body, False, "制定時"))),
        ("ASTのない版のファイルを分ける", "format", False, broken(fictional_files(body, True, "制定時"))),
    ])
    add("common", "ASTを生成できない版を含む変更は判定不能", ["CHG-02", "CHG-04"], "change",
        {"kind": "change", "bundle": rel(bundle_pos), "base": c1, "head": c2},
        {"results": [{"check": "change", "result": "incomplete"}]}, True)
    dest = next_dir("common", False) / "repo.bundle"
    copy_file(dest, bundle_pos)
    add("common", "ASTを生成できない版のファイルを書式変更で変える", ["CHG-04"], "change",
        {"kind": "change", "bundle": rel(dest), "base": c2, "head": c3},
        {"results": [{"check": "change", "result": "fail"}], "diagnostics": [diag("CHG-04", SV["common"])]}, False)


# --- 2026-11-13 (#53): the time of termination comes from the one item that is not retracted ----------
def termination_time():
    """HIST-03: at most one item that is not retracted; HIST-12: the warning compares fixed dates (CONF-01 compares it)."""
    source = "conformance/loj-history/v1alpha1/valid/hist-036/repo"
    late = 'value: "1960-04-01"\n          raw: 昭和三十五年四月一日'
    early = 'value: "1959-04-13"\n          raw: 昭和三十四年四月十三日'
    # The active item ends the law on 1959-04-13; the retracted item has the later 1960-04-01; the version is
    # in force from 1959-10-01. Only a checker that takes the active item finds the version after the end.
    dest = next_dir("hist", True) / "repo"
    mutate(dest, source, [("history.yaml", late, "@LATE@"), ("history.yaml", early, late),
                          ("history.yaml", "@LATE@", early),
                          ("history.yaml", "    effective: {state: unknown, reason: 未調査}\n",
                           "    effective:\n      state: date\n      value: \"1959-10-01\"\n      raw: 昭和三十四年十月一日\n"
                           "      precision: day\n      evidence: [{source: src-egov-s34-122, locator: 附則}]\n"
                           "      verification: {state: unverified, reason: 官報と未照合}\n")])
    add("hist", "効力の終了の時点より後に施行される版（撤回した内訳の時点より前。警告）（架空）",
        ["HIST-12", "HIST-03", "CONF-01"], "L3", {"kind": "repository", "path": rel(dest)},
        {"results": [l3("historyStructure")], "diagnostics": [diag("HIST-12", SV["hist"], "warning")]}, True,
        "historyStructure")
    dest = next_dir("hist", False) / "repo"
    mutate(dest, source, [("history.yaml", "verification: {state: retracted, reason: 適合ケースのための架空の撤回}",
                           "verification: {state: unverified, reason: 官報と未照合}")])
    add("hist", "撤回していない内訳が二つある廃止の関係（架空）", ["HIST-03", "HIST-12"], "L3",
        {"kind": "repository", "path": rel(dest)},
        {"results": [l3("historyStructure", "fail")], "diagnostics": [diag("HIST-03", SV["hist"])]}, False,
        "historyStructure")


REVIEW_URL = "https://example.invalid/law-repository/pull/12"


def reviewed_format_steps(trailers):
    """A version without an AST, then a format commit changing its files with the given LoJ-Reviewed trailers (CHG-04)."""
    body = "架空の雲を保管する。\n"
    return [
        ("見出しの誤った版を加える", "revisionAdd", True, broken(fictional_files(body))),
        ("ラベルを改める", "metadata", False, broken(fictional_files(body, False, "制定時"))),
        ("ASTのない版のファイルを人のレビューを経て分ける", "format", False, broken(fictional_files(body, True, "制定時")), trailers),
    ]


# --- 2026-11-15 (#63): reuse of a retired Record ID (RID-05) and a reviewed format change (CHG-04) ---------
def retired_ids_and_reviewed_format():
    """RID-01 sends a collision with a merged Record to RID-05; CHG-04 reads LoJ-Reviewed as the record of a review."""
    source = "conformance/loj-registry/v1alpha1/valid/reg-009/registry"
    dest = next_dir("reg", False) / "registry"
    mutate(dest, source, [("records/20170616-law-63.yaml", "status: active\n", "status: active\naliases:\n  - id: k7m2p9qd3x\n"
                           "    evidence: [{source: src-egov-h29-63, locator: 法令名}]\n    verification: {state: unverified}\n")])
    add("reg", "統合したRecordのIDを別のRecordの別名に再利用する（RID-01で重ねて報告しない）", ["RID-05", "RID-01"], "registry",
        {"kind": "registry", "path": rel(dest)},
        {"results": [{"check": "registry", "result": "fail"}], "diagnostics": [diag("RID-05", SV["reg"])]}, False)
    bundle_pos = next_dir("common", True) / "repo.bundle"
    _, c2, c3 = build_bundle(bundle_pos, reviewed_format_steps("LoJ-Reviewed: " + REVIEW_URL + "\n"))
    add("common", "ASTを生成できない版のファイルを人のレビューの記録を付けて書式変更で変える", ["CHG-04", "CHG-03"], "change",
        {"kind": "change", "bundle": rel(bundle_pos), "base": c2, "head": c3},
        {"results": [{"check": "change", "result": "incomplete"}]}, True)


# --- 2026-11-15 (#68): the registration space is an input of the checker (VAL-03) -------------------------
def registration_space():
    """A RecordRef whose space differs from the input space points to another registry: not fetched, not a failure."""
    source = "conformance/loj-history/v1alpha1/valid/hist-004/repo"
    dest = next_dir("common", True) / "hist-004"
    mutate(dest, source, [("history.yaml", "    from: {id: 20170616-law-63, label:", "    from: {id: 20170616-law-63, space: other-space, label:")])
    add("common", "他の登録空間のRecordを起点とする関係", ["VAL-03", "XREF-01", "VAL-06"], "L4",
        {"kind": "records", "registry": REG_POS, "repositories": [rel(dest)]},
        {"results": [{"check": "L4", "category": "relationResolution", "result": "incomplete"}],
         "references": [{"target": "loj:other-space/20170616-law-63", "result": "notFetched"}]}, True, "relationResolution")
    # REG-02 asks replacedBy to resolve in the same registry, so another space is a violation there.
    dest = next_dir("reg", False) / "registry"
    mutate(dest, REG_POS, [], {"records/k7m2p9qd3x.yaml": merged_record("space: other-space, ")})
    add("reg", "他の登録空間を指す統合先", ["REG-02", "VAL-03"], "registry", {"kind": "registry", "path": rel(dest)},
        {"results": [{"check": "registry", "result": "fail"}], "diagnostics": [diag("REG-02", SV["reg"])]}, False)


# --- 2026-11-16 (#86): LoJ-Reviewed that counts as no record (CHG-03) --------------------------------------
def invalid_review_records():
    """common-027's history with the format commit's LoJ-Reviewed doubled, empty or blank: no record, so CHG-04 fails.

    The first two commits are common-027's (same files, messages and dates), so the base hash is the same.
    The blank value needs --cleanup=verbatim: git's default cleanup strips trailing blanks from each line.
    """
    for title, trailers in [
        ("ASTを生成できない版のファイルを、人のレビューの記録を二つ付けて書式変更で変える",
         "LoJ-Reviewed: " + REVIEW_URL + "\nLoJ-Reviewed: https://example.invalid/law-repository/pull/13\n"),
        ("ASTを生成できない版のファイルを、人のレビューの記録を値を空にして付けて書式変更で変える", "LoJ-Reviewed:\n"),
        ("ASTを生成できない版のファイルを、人のレビューの記録を値を空白だけにして付けて書式変更で変える", "LoJ-Reviewed: \t \n"),
    ]:
        bundle = next_dir("common", False) / "repo.bundle"
        _, c2, c3 = build_bundle(bundle, reviewed_format_steps(trailers), verbatim=True)
        add("common", title, ["CHG-04", "CHG-03"], "change", {"kind": "change", "bundle": rel(bundle), "base": c2, "head": c3},
            {"results": [{"check": "change", "result": "fail"}], "diagnostics": [diag("CHG-04", SV["common"])]}, False)


# --- 2026-11-16 (#87): which glyphs.yaml the glyph-note check reads (HIST-08), seen in the evidence category ----
def glyph_file_selection():
    """HIST-08 reads versions/<own revision_id>/glyphs.yaml of complete and partial Revisions only.

    Each input breaks HIST-08 (history structure, fixed by hist-047 and hist-048); the evidence category passes
    because the glyphs.yaml that would fail GLYPH-01 is not read as a Revision's glyph notes.
    """
    absent = ("    text:\n      status: complete\n      sources:\n        - {source: src-goshomei-s41-86, locator: 2画像 本則（改正の内容）}\n"
              "      glyphCheck: unverified\n      glyphNotes: versions/zwgmz1rt/glyphs.yaml\n"
              "      correctionsSurveyed: {state: unsurveyed, reason: 官報（昭和41年6月25日）を入手していない（REB-05）}\n")
    for title, edits in [
        ("本文のない版のディレクトリに残った字体注記を検査にかけない",
         [("history.yaml", absent, "    text:\n      status: absent\n"), (ZWG + "glyphs.yaml", "revision: zwgmz1rt", "revision: 98mj5vgx")]),
        ("別の版の字体注記を指すglyphNotesで、指す先を自身の字体注記として読まない",
         [("history.yaml", "      glyphNotes: versions/zwgmz1rt/glyphs.yaml\n", "      glyphNotes: versions/98mj5vgx/glyphs.yaml\n")]),
    ]:
        dest = next_dir("hist", True) / "repo"
        mutate(dest, HIST_POS, edits)
        add("hist", title, ["HIST-08", "GLYPH-01"], "L3", {"kind": "repository", "path": rel(dest)},
            {"results": [l3("evidence")]}, True, "evidence")


# --- 2026-11-16 (#104): fields the schemas forbid outside their condition, now forbidden in the text ----------
def conditional_fields():
    """Each input adds one field outside the condition that allows it; the schema rejects it (SCHEMA_REJECTED).

    The category field has no case: it belongs to the forms of the index, the expected results and the report,
    which are no input of a check (docs/coverage.md).
    """
    fiction = "verification: {state: unverified, reason: 適合ケースのための架空の変更}"
    hist2 = "conformance/loj-history/v1alpha1/valid/hist-002/repo"
    hist3 = "conformance/loj-history/v1alpha1/valid/hist-003/repo"
    pending = ("      delegation: {raw: この法律の施行の日以前に皇室典範第四条の規定による皇位の継承があったとき, "
               "evidence: [{source: src-egov-h29-63, locator: 附則第二条}]}\n")
    for title, rule, source, edits in [
        ("適用の条件を調べていない版の条件", "HIST-07", HIST_POS,
         [("history.yaml", "    applicability: {state: unsurveyed}\n",
           "    applicability:\n      state: unsurveyed\n      conditions:\n        - scope: {text: 全部}\n"
           "          text: 架空の適用の条件\n          evidence: [{source: src-kanpo-19480720, locator: 附則第一項}]\n"
           "          " + fiction + "\n")]),
        ("制定の起点が持つ全部改正の参照", "HIST-04", HIST_POS,
         [("history.yaml", "    origin: enactment\n",
           "    origin: enactment\n    totallyRevises: {record: {id: 20990101-law-5, label: 架空の旧法}, relation: rel-total}\n")]),
        ("有効な版の統合先", "HIST-10", HIST_POS,
         [("history.yaml", "      glyphNotes: versions/98mj5vgx/glyphs.yaml\n    status: active\n",
           "      glyphNotes: versions/98mj5vgx/glyphs.yaml\n    status: active\n    replacedBy:\n      revisions: [zwgmz1rt]\n"
           "      evidence: [{source: src-kanpo-19480720, locator: 1コマ}]\n      " + fiction + "\n")]),
        ("廃止の項目に写した根拠と確認状態", "HIST-12", hist2,
         [("history.yaml", "  - {type: repealed, relation: rel-repeal}",
           "  - {type: repealed, relation: rel-repeal, evidence: [{source: src-egov-s34-122, locator: 第二条}], "
           "verification: {state: unverified, reason: 官報と未照合}}")]),
        ("自身の規定による失効が持つ関係", "HIST-12", hist3,
         [("history.yaml", "  - type: expired\n", "  - type: expired\n    relation: rel-repeal\n")]),
        ("確定していない時点の確定の根拠", "TIME-01", hist3,
         [("history.yaml", pending, pending + "      determinedBy: {record: {id: tfy1ccapzk, label: 平成二十九年政令第三百二号}, "
                                       "evidence: [{source: src-egov-h29-302, locator: 本則}]}\n")]),
    ]:
        dest = next_dir("hist", False) / "repo"
        mutate(dest, source, edits)
        sv = SV["common"] if rule.startswith("TIME") else SV["hist"]
        add("hist", title, [rule], "L3", {"kind": "repository", "path": rel(dest)},
            {"results": [l3("historyStructure", "fail")], "diagnostics": [diag(rule, sv)]}, False, "historyStructure")
    dest = next_dir("rebuild", False) / "repo"
    mutate(dest, HIST_POS, [("rebuild.yaml", "    note: 旧本文は祝日の表を箇条書きで書いている\n",
                             "    note: 旧本文は祝日の表を箇条書きで書いている\n    count: 1\n")])
    add("rebuild", "構造の差の件数", ["REBR-05"], "rebuild", {"kind": "repository", "path": rel(dest)},
        {"results": [{"check": "rebuild", "result": "fail"}], "diagnostics": [diag("REBR-05", SV["rebuild"])]}, False)
    dest = next_dir("reg", False) / "registry"
    mutate(dest, REG_POS, [("records/19660625-act-86.yaml", "status: active\n",
                            "status: active\nreplacedBy:\n  - record: {id: 19480720-law-178, label: 昭和二十三年法律第百七十八号}\n"
                            "    evidence: [{source: src-goshomei-s41-86, locator: 1・2画像}]\n    " + fiction + "\n")])
    add("reg", "有効なRecordの統合先", ["REG-02"], "registry", {"kind": "registry", "path": rel(dest)},
        {"results": [{"check": "registry", "result": "fail"}], "diagnostics": [diag("REG-02", SV["reg"])]}, False)


# --- 2026-11-16 (#107): the trailer syntax (CHG-03) and the undetermined AST check of CHG-04 ----------------
def trailer_syntax():
    """CHG-03 reads trailers from the last paragraph only when every line of it is a trailer line.

    The two correction commits that break the syntax have no declaration, so CHG-03 fails them. The format commit
    with LoJ-Revisions passes: the format check does not use declared versions.
    """
    bundle_pos = next_dir("common", True) / "repo.bundle"
    c1, c2, c3, c4, c5 = build_bundle(bundle_pos, [
        ("制定時の版を加える", "revisionAdd", True, fictional_files("架空の雲を保管すろ。\n")),
        ("第一条の誤転記を直す\n\nLoJ-Change:\tcorrection\nLoJ-Revisions:  " + REV + "\n", RAW, False,
         fictional_files("架空の雲を保管する。\n")),
        ("条ごとにファイルを分ける", "format", True, fictional_files("架空の雲を保管する。\n", files_split=True)),
        ("第一条の誤転記を直す（名前とコロンの間に空白）\n\nLoJ-Change : correction\nLoJ-Revisions: " + REV + "\n", RAW, False,
         fictional_files("架空の雲を保管し続ける。\n", files_split=True)),
        ("第一条の誤転記を直す（trailerの後の段落）\n\nLoJ-Change: correction\nLoJ-Revisions: " + REV + "\n\n原典の箇所は第一条。\n",
         RAW, False, fictional_files("架空の雲を保管し続けろ。\n", files_split=True)),
    ])
    bundle = rel(bundle_pos)
    add("common", "コロンの後にタブと二つの空白を置いた種類の宣言", ["CHG-03", "CHG-02"], "change",
        {"kind": "change", "bundle": bundle, "base": c1, "head": c2}, {"results": [{"check": "change", "result": "pass"}]}, True)
    add("common", "宣言した版を書いた書式変更", ["CHG-03", "CHG-02"], "change",
        {"kind": "change", "bundle": bundle, "base": c2, "head": c3}, {"results": [{"check": "change", "result": "pass"}]}, True)
    for title, base, head in [("名前とコロンの間に空白を置いた種類の宣言", c3, c4),
                              ("trailerの後に段落が続く種類の宣言", c4, c5)]:
        dest = next_dir("common", False) / "repo.bundle"
        copy_file(dest, bundle_pos)
        add("common", title, ["CHG-03"], "change", {"kind": "change", "bundle": rel(dest), "base": base, "head": head},
            {"results": [{"check": "change", "result": "fail"}], "diagnostics": [diag("CHG-03", SV["common"])]}, False)
    # The undetermined AST check is a CHG-04 diagnostic (class undetermined), also next to a CHG-04 violation.
    first = {case["id"]: case["input"] for case in INDEX["common"]}
    for success, ident, title, diagnostics in [
        (True, "common-025", "ASTを生成できない版を含む変更の判定不能の診断",
         [diag("CHG-04", SV["common"], "undetermined")]),
        (False, "common-026", "ASTを生成できない版のファイルを書式変更で変える違反と判定不能の診断",
         [diag("CHG-04", SV["common"]), diag("CHG-04", SV["common"], "undetermined")]),
    ]:
        dest = next_dir("common", success) / "repo.bundle"
        copy_file(dest, ROOT / first[ident]["bundle"])
        result = "incomplete" if success else "fail"
        add("common", title, ["CHG-04"], "change",
            {"kind": "change", "bundle": rel(dest), "base": first[ident]["base"], "head": first[ident]["head"]},
            {"results": [{"check": "change", "result": result}], "diagnostics": diagnostics}, success)
    # CRLF line ends: the CR at the end of each line is removed, so the declaration reads as correction.
    bundle_pos = next_dir("common", True) / "repo.bundle"
    c1, c2 = build_bundle(bundle_pos, [
        ("制定時の版を加える", "revisionAdd", True, fictional_files("架空の雲を保管すろ。\n")),
        ("第一条の誤転記を直す（CRLFの行末）\r\n\r\nLoJ-Change: correction\r\nLoJ-Revisions: " + REV + "\r\n", RAW, False,
         fictional_files("架空の雲を保管する。\n")),
    ], verbatim=True)
    add("common", "行末をCRLFにした種類の宣言", ["CHG-03", "CHG-02"], "change",
        {"kind": "change", "bundle": rel(bundle_pos), "base": c1, "head": c2},
        {"results": [{"check": "change", "result": "pass"}]}, True)
    # Only U+0020 and U+0009 are trimmed: a value of U+3000 alone is a record, as in common-027.
    bundle_pos = next_dir("common", True) / "repo.bundle"
    _, c2, c3 = build_bundle(bundle_pos, reviewed_format_steps("LoJ-Reviewed: " + chr(0x3000) + "\n"), verbatim=True)
    add("common", "ASTを生成できない版のファイルを、人のレビューの記録を値を全角空白だけにして付けて書式変更で変える",
        ["CHG-04", "CHG-03"], "change", {"kind": "change", "bundle": rel(bundle_pos), "base": c2, "head": c3},
        {"results": [{"check": "change", "result": "incomplete"}]}, True)


# --- 2026-11-16 (#115): a LoJ-Change value that is no kind is reported by CHG-03 -------------------------
def unknown_kind():
    """The second commit declares a value that is not a kind of CHG-01; CHG-03 reports it and no kind check runs."""
    bundle = next_dir("common", False) / "repo.bundle"
    c1, c2 = build_bundle(bundle, [
        ("制定時の版を加える", "revisionAdd", True, fictional_files("架空の雲を保管すろ。\n")),
        ("第一条の誤転記を直す（種類でない値）", "fix", True, fictional_files("架空の雲を保管する。\n")),
    ])
    add("common", "変更の種類でない値の宣言", ["CHG-03", "CHG-01"], "change",
        {"kind": "change", "bundle": rel(bundle), "base": c1, "head": c2},
        {"results": [{"check": "change", "result": "fail"}], "diagnostics": [diag("CHG-03", SV["common"])]}, False)


# --- 2026-11-16 (#116): the evidence of each declared version of officialCorrection (CHG-02) ----------------
def official_correction_evidence():
    """officialCorrection needs, after the change, an Evidence of text.sources that points to an officialCorrection Source."""
    def with_seigo(files, cited=True):
        """Add the officialCorrection Source; cite it from text.sources only when cited."""
        out = dict(files)
        history = out["history.yaml"].replace(
            "  - {id: src-fiction, kind: other, title: 架空の原典}\n",
            "  - {id: src-fiction, kind: other, title: 架空の原典}\n"
            "  - {id: src-seigo, kind: officialCorrection, title: 架空の官報正誤}\n", 1)
        assert history != files["history.yaml"]  # the Source was added
        if cited:
            cited_history = history.replace("      sources: [{source: src-fiction, locator: 本則}]\n",
                                            "      sources: [{source: src-fiction, locator: 本則}, {source: src-seigo, locator: 第一条}]\n", 1)
            assert cited_history != history  # the Evidence was added
            history = cited_history
        out["history.yaml"] = history
        return out
    bundle_pos = next_dir("common", True) / "repo.bundle"
    c1, c2, c3 = build_bundle(bundle_pos, [
        ("制定時の版を加える", "revisionAdd", True, fictional_files("架空の雲を保管すろ。\n")),
        ("官報正誤により第一条を直す", "officialCorrection", True, with_seigo(fictional_files("架空の雲を保管する。\n"))),
        ("官報正誤と宣言して、官報正誤を根拠にせず第一条を直す", "officialCorrection", True,
         with_seigo(fictional_files("架空の雲を保管し続ける。\n"), cited=False)),
    ])
    add("common", "官報正誤のSourceを本文の出典に加える官報正誤", ["CHG-02", "CHG-01"], "change",
        {"kind": "change", "bundle": rel(bundle_pos), "base": c1, "head": c2},
        {"results": [{"check": "change", "result": "pass"}]}, True)
    dest = next_dir("common", False) / "repo.bundle"
    copy_file(dest, bundle_pos)
    add("common", "官報正誤のSourceを本文の出典で指さない官報正誤", ["CHG-02", "CHG-01"], "change",
        {"kind": "change", "bundle": rel(dest), "base": c2, "head": c3},
        {"results": [{"check": "change", "result": "fail"}], "diagnostics": [diag("CHG-02", SV["common"])]}, False)


# --- 2026-11-16 (#117): two LoJ-Change or two LoJ-Revisions trailers in one commit (CHG-03) -----------------
def duplicate_trailers():
    """Each correction commit declares a trailer twice; CHG-03 reports it and no kind check runs."""
    bundle_pos = next_dir("common", False) / "repo.bundle"
    c1, c2, c3 = build_bundle(bundle_pos, [
        ("制定時の版を加える", "revisionAdd", True, fictional_files("架空の雲を保管すろ。\n")),
        ("第一条の誤転記を直す（種類の宣言を二つ）\n\nLoJ-Change: correction\nLoJ-Change: correction\nLoJ-Revisions: " + REV + "\n",
         RAW, False, fictional_files("架空の雲を保管する。\n")),
        ("第一条の誤転記を直す（宣言した版を二行）\n\nLoJ-Change: correction\nLoJ-Revisions: " + REV + "\nLoJ-Revisions: " + REV + "\n",
         RAW, False, fictional_files("架空の雲を保管し続ける。\n")),
    ])
    add("common", "同じ値の種類の宣言を二つ置いたcommit", ["CHG-03"], "change",
        {"kind": "change", "bundle": rel(bundle_pos), "base": c1, "head": c2},
        {"results": [{"check": "change", "result": "fail"}], "diagnostics": [diag("CHG-03", SV["common"])]}, False)
    dest = next_dir("common", False) / "repo.bundle"
    copy_file(dest, bundle_pos)
    add("common", "宣言した版を二行に置いたcommit", ["CHG-03"], "change",
        {"kind": "change", "bundle": rel(dest), "base": c2, "head": c3},
        {"results": [{"check": "change", "result": "fail"}], "diagnostics": [diag("CHG-03", SV["common"])]}, False)
    # format may omit LoJ-Revisions, but two of them still fail (the form of the declaration does not depend on the kind).
    bundle = next_dir("common", False) / "repo.bundle"
    c1, c2 = build_bundle(bundle, [
        ("制定時の版を加える", "revisionAdd", True, fictional_files("架空の雲を保管する。\n")),
        ("条ごとにファイルを分ける（宣言した版を二行）\n\nLoJ-Change: format\nLoJ-Revisions: " + REV + "\nLoJ-Revisions: " + REV + "\n",
         RAW, False, fictional_files("架空の雲を保管する。\n", files_split=True)),
    ])
    add("common", "宣言した版を二行に置いた書式変更", ["CHG-03"], "change",
        {"kind": "change", "bundle": rel(bundle), "base": c1, "head": c2},
        {"results": [{"check": "change", "result": "fail"}], "diagnostics": [diag("CHG-03", SV["common"])]}, False)


# --- 2026-11-16 (#120): a merge commit on the canonical branch (CHG-03) ------------------------------------
def merge_commit():
    """A correction made on a branch is merged into main by a merge commit; CHG-03 fails the merge commit unchecked.

    The correction (c2) alone passes, so however the commits between base and head are counted, only the merge
    commit fails. It declares correction and the version, but a merge commit is not compared (CHG-03).
    """
    bundle = next_dir("common", False) / "repo.bundle"
    c1, _, merge = build_bundle(bundle, [
        ("制定時の版を加える", "revisionAdd", True, fictional_files("架空の雲を保管すろ。\n")),
        (BRANCH, "fix"),
        ("第一条の誤転記を直す", "correction", True, fictional_files("架空の雲を保管する。\n")),
        (CHECKOUT, "main"),
        ("第一条の誤転記の訂正をmergeする", "correction", True, Merge("fix")),
    ])
    add("common", "正本ブランチに置いたmergeのcommit", ["CHG-03"], "change",
        {"kind": "change", "bundle": rel(bundle), "base": c1, "head": merge},
        {"results": [{"check": "change", "result": "fail"}], "diagnostics": [diag("CHG-03", SV["common"])]}, False)


# --- 2026-11-16 (#122): a correction that keeps the text of the declared version (CHG-01, CHG-02) ------------
def correction_without_text_change():
    """The correction changes only the locator of text.sources; the AST of the declared version is the same.

    CHG-01 forbids declaring a version whose text does not change, but the change check does not compare the AST of
    the declared versions (CHG-02), so the check passes. The text.sources Evidence is there, so CHG-02 holds.
    """
    bundle = next_dir("common", True) / "repo.bundle"
    c1, c2 = build_bundle(bundle, [
        ("制定時の版を加える", "revisionAdd", True, fictional_files("架空の雲を保管する。\n")),
        ("本文の出典の箇所を直す（記録訂正と宣言）", "correction", True,
         fictional_files("架空の雲を保管する。\n", locator="本則第一条")),
    ])
    add("common", "宣言した版の本文を変えず、本文の出典の箇所だけを直す記録訂正（CHG-01の宣言の誤りだが、変更検査は判定しない）", ["CHG-02", "CHG-01"], "change",
        {"kind": "change", "bundle": rel(bundle), "base": c1, "head": c2},
        {"results": [{"check": "change", "result": "pass"}]}, True)


# --- 2026-11-16 (#126): declared versions without an AST are not compared (CHG-02, CHG-04) ------------------
def partial_text(files):
    """Leave out the second article and record the version as partial, with the article as its gap (HIST-07)."""
    out = dict(files)
    md = "versions/" + REV + "/main.md"
    article2 = "# 第二条\n"
    assert article2 in out[md]
    out[md] = out[md][:out[md].index(article2)]
    status = "      status: complete\n"
    assert out["history.yaml"].count(status) == 1
    out["history.yaml"] = out["history.yaml"].replace(status, "      status: partial\n      gaps: [{text: 第二条}]\n", 1)
    return out


def declared_versions_without_ast():
    """correction and restoration do not build the AST of the declared version, so no CHG-04 undetermined is reported.

    The correction fixes the text of a version that fails L1 (HEAD-01) and still fails it after the change. The
    restoration adds the missing article to a partial version and records it as complete.
    """
    bundle = next_dir("common", True) / "repo.bundle"
    c1, c2 = build_bundle(bundle, [
        ("見出しの誤った版を加える", "revisionAdd", True, broken(fictional_files("架空の雲を保管すろ。\n"))),
        ("見出しの誤った版の第一条の誤転記を直す", "correction", True, broken(fictional_files("架空の雲を保管する。\n"))),
    ])
    add("common", "ASTを生成できない版の本文を直す記録訂正", ["CHG-02", "CHG-04"], "change",
        {"kind": "change", "bundle": rel(bundle), "base": c1, "head": c2},
        {"results": [{"check": "change", "result": "pass"}]}, True)
    bundle = next_dir("common", True) / "repo.bundle"
    c1, c2 = build_bundle(bundle, [
        ("第一条だけの版を加える", "revisionAdd", True, partial_text(fictional_files("架空の雲を保管する。\n"))),
        ("欠けていた第二条を補う", "restoration", True, fictional_files("架空の雲を保管する。\n")),
    ])
    add("common", "一部しか本文がない版の欠落を補う復元", ["CHG-02", "CHG-04"], "change",
        {"kind": "change", "bundle": rel(bundle), "base": c1, "head": c2},
        {"results": [{"check": "change", "result": "pass"}]}, True)


# --- 2026-11-16 (#132): a sourceEdit note in the amending law's own version, on a cell of an amendment content ---
def amendment_glyph_notes():
    """The Record of 昭和四十一年法律第八十六号 itself, its enactment version only (hand-written, not a copy).

    The note points to a cell inside the content of the first amendment of the main provision (AMEND-02, GLYPH-04,
    GLYPH-09). The version package uses the paragraph form of the main provision (PARA-03) and amendments (AMEND-01).
    """
    add("glyph", "改正法の版の改正内容の中のセルを指す見え消しの注記", ["GLYPH-04", "GLYPH-09", "AMEND-02", "PARA-03"],
        "L3", {"kind": "repository", "path": "conformance/loj-glyphs/v1alpha1/valid/glyph-012/repo"},
        {"results": [l3("evidence")]}, True, "evidence")


# --- 2026-11-17 (#138): a commit that changes no file of the canonical data declares auxiliary (CHG-01, CHG-02) ---
WORKFLOW = ".github/workflows/validate.yml"


def with_workflow(files, job="validate"):
    """Add a CI setting, a file outside the canonical data (CHG-01), to the files of a step."""
    out = dict(files)
    out[WORKFLOW] = ("name: validate\non: [push, pull_request]\njobs:\n  " + job + ":\n    runs-on: ubuntu-latest\n"
                     "    steps:\n      - uses: actions/checkout@v4\n")
    return out


def auxiliary_changes():
    """auxiliary checks only that no file of the canonical data changes; it compares no AST.

    The first bundle adds a CI setting by auxiliary, then corrects the text in a commit that also changes the CI
    setting (a file outside the data is in no kind's check, CHG-01), then declares auxiliary but changes the label
    of the Revision in history.yaml (a file of the data, CHG-02). The second bundle has a version whose L1 fails
    (HEAD-01): adding the CI setting by auxiliary compares no AST, so no CHG-04 undetermined is reported.
    """
    body = "架空の雲を保管する。\n"
    bundle_pos = next_dir("common", True) / "repo.bundle"
    c1, c2, c3, c4 = build_bundle(bundle_pos, [
        ("制定時の版を加える", "revisionAdd", True, fictional_files("架空の雲を保管すろ。\n")),
        ("検証のワークフローを加える", "auxiliary", False, with_workflow(fictional_files("架空の雲を保管すろ。\n"))),
        ("第一条の誤転記を直し、検証のワークフローのジョブの名前を改める", "correction", True,
         with_workflow(fictional_files(body), "check")),
        ("正本のデータの外の変更と宣言して、ラベルを改める", "auxiliary", False,
         with_workflow(fictional_files(body, False, "制定時"), "check")),
    ])
    bundle = rel(bundle_pos)
    add("common", "CIの設定だけを加える正本のデータの外の変更", ["CHG-01", "CHG-02", "CHG-03"], "change",
        {"kind": "change", "bundle": bundle, "base": c1, "head": c2},
        {"results": [{"check": "change", "result": "pass"}]}, True)
    add("common", "CIの設定の変更を含む記録訂正", ["CHG-01", "CHG-02"], "change",
        {"kind": "change", "bundle": bundle, "base": c2, "head": c3},
        {"results": [{"check": "change", "result": "pass"}]}, True)
    dest = next_dir("common", False) / "repo.bundle"
    copy_file(dest, bundle_pos)
    add("common", "正本のデータの外の変更と宣言して、履歴マニフェストを変える", ["CHG-02", "CHG-01"], "change",
        {"kind": "change", "bundle": rel(dest), "base": c3, "head": c4},
        {"results": [{"check": "change", "result": "fail"}], "diagnostics": [diag("CHG-02", SV["common"])]}, False)
    bundle = next_dir("common", True) / "repo.bundle"
    c1, c2 = build_bundle(bundle, [
        ("見出しの誤った版を加える", "revisionAdd", True, broken(fictional_files(body))),
        ("検証のワークフローを加える", "auxiliary", False, with_workflow(broken(fictional_files(body)))),
    ])
    add("common", "ASTを生成できない版を持つリポジトリにCIの設定を加える正本のデータの外の変更", ["CHG-02", "CHG-04", "CHG-01"], "change",
        {"kind": "change", "bundle": rel(bundle), "base": c1, "head": c2},
        {"results": [{"check": "change", "result": "pass"}]}, True)
    # Every file under versions/ is a file of the data, a document that is not part of the version package too (CHG-01).
    bundle = next_dir("common", False) / "repo.bundle"
    readme = dict(fictional_files(body))
    readme["versions/" + REV + "/README.md"] = "この版の説明である。\n"
    c1, c2 = build_bundle(bundle, [
        ("制定時の版を加える", "revisionAdd", True, fictional_files(body)),
        ("版のディレクトリに説明の文書を加える（正本のデータの外の変更と宣言）", "auxiliary", False, readme),
    ])
    add("common", "正本のデータの外の変更と宣言して、版のディレクトリにファイルを加える", ["CHG-02", "CHG-01"], "change",
        {"kind": "change", "bundle": rel(bundle), "base": c1, "head": c2},
        {"results": [{"check": "change", "result": "fail"}], "diagnostics": [diag("CHG-02", SV["common"])]}, False)
    # auxiliary may omit LoJ-Revisions; written, it does not change the result (CHG-03).
    bundle = next_dir("common", True) / "repo.bundle"
    c1, c2 = build_bundle(bundle, [
        ("制定時の版を加える", "revisionAdd", True, fictional_files(body)),
        ("検証のワークフローを加える（宣言した版を書く）", "auxiliary", True, with_workflow(fictional_files(body))),
    ])
    add("common", "宣言した版を書いた正本のデータの外の変更", ["CHG-03", "CHG-02"], "change",
        {"kind": "change", "bundle": rel(bundle), "base": c1, "head": c2},
        {"results": [{"check": "change", "result": "pass"}]}, True)


# --- 2026-11-20 (#141): an illegible character read in another original source (GLYPH-05, GLYPH-06 6) ---------
ENA = "versions/98mj5vgx/"
ILLEGIBLE_OTHER = ('  - id: g20\n'
                   '    node: 19480720-law-178/main/article/1/paragraph/1\n'
                   '    offset: 3\n'
                   '    recorded: "平和"\n'
                   '    kind: illegible\n'
                   '    basis: otherSource\n'
                   '    evidence: [{source: src-kanpo-19480720, locator: "1コマ 第一條（汚れ）"}, {source: src-goshomei, locator: "第一條"}]\n'
                   '    verification: {state: confirmed, reason: "官報の画像では汚れで読めず、御署名原本で読めた。'
                   '「平」は右端だけが見え、御署名原本の字と合う"}\n')
ILLEGIBLE_PLAIN = ('  - id: g21\n'
                   '    node: 19480720-law-178/main/article/2/paragraph/1/table/1/row/b6gr/cell/1\n'
                   '    offset: 1\n'
                   '    recorded: "〓"\n'
                   '    kind: illegible\n'
                   '    evidence: [{source: src-kanpo-19480720, locator: "1コマ 第二條 元日の項"}]\n'
                   '    verification: {state: unverified, reason: "ほかの原典資料を確かめていない"}\n')


def illegible_other_source():
    """The enactment version gets two illegible notes: 平和 read in the 御署名原本 (basis: otherSource, the text keeps
    the characters) and 元〓 not read anywhere (basis omitted, the same as undetermined). The negatives change the
    first note only."""
    pos = next_dir("glyph", True) / "repo"
    mutate(pos, HIST_POS, [(ENA + "glyphs.yaml", "  - id: g15\n", ILLEGIBLE_OTHER + ILLEGIBLE_PLAIN + "  - id: g15\n"),
                           (ENA + "main.md", "元日\n", "元〓\n")])
    add("glyph", "官報の複製で読めず、ほかの原典資料で読めた字を本文に置く判読困難の注記",
        ["GLYPH-02", "GLYPH-03", "GLYPH-05", "GLYPH-06", "GLYPH-07", "GLYPH-10"], "L3",
        {"kind": "repository", "path": rel(pos)}, {"results": [l3("evidence")]}, True, "evidence")
    kanpo = '{source: src-kanpo-19480720, locator: "1コマ 第一條（汚れ）"}'
    goshomei = '{source: src-goshomei, locator: "第一條"}'
    negatives = [
        ("判読困難の字を下書きの資料の字で置く", [(ENA + "glyphs.yaml", '    kind: illegible\n    basis: otherSource\n',
                                         '    kind: illegible\n    basis: provisional\n')]),
        ("ほかの原典資料で読めたとして〓を置く",
         [(ENA + "glyphs.yaml", '    recorded: "平和"\n    kind: illegible\n', '    recorded: "〓〓"\n    kind: illegible\n'),
          (ENA + "main.md", "自由と平和を", "自由と〓〓を")]),
        ("ほかの原典資料で読めた字の根拠が一件だけ", [(ENA + "glyphs.yaml", kanpo + ", " + goshomei, goshomei)]),
        ("ほかの原典資料で読めた字の根拠が同じ資料だけ",
         [(ENA + "glyphs.yaml", kanpo + ", " + goshomei,
           kanpo + ', {source: src-kanpo-19480720, locator: "1コマ 第一條"}')]),
        ("ほかの原典資料で読めた字の根拠に公布された本文がない",
         [(ENA + "glyphs.yaml", kanpo + ", " + goshomei, '{source: src-egov, locator: "第一条"}, ' + goshomei)]),
        ("字の決め方のない判読困難の注記で〓でない字を置く", [(ENA + "glyphs.yaml", '    kind: illegible\n    basis: otherSource\n',
                                                 '    kind: illegible\n')]),
        ("ほかの原典資料で読めた字の根拠が下書きの資料",
         [(ENA + "glyphs.yaml", kanpo + ", " + goshomei, kanpo + ', {source: src-egov, locator: "第一条"}')]),
    ]
    for title, edits in negatives:
        dest = next_dir("glyph", False) / "repo"
        mutate(dest, rel(pos), edits)
        add("glyph", title, ["GLYPH-05"], "L3", {"kind": "repository", "path": rel(dest)},
            {"results": [l3("evidence", "fail")], "diagnostics": [diag("GLYPH-05", SV["glyph"])]}, False, "evidence")


# --- 2026-11-20 (#147): a change of the Git mode of a file of the data changes the file (CHG-02) -----------------
def file_modes():
    """A file of the data is a regular file of mode 100644, checked on the files a commit adds or changes.

    The bundle adds the version, then makes its text executable by format (in the range of format, but a mode other
    than 100644), then makes it a regular file again by format (in the range: passes, though the parent fails). The
    second bundle makes it a regular file again by metadata, which may not change a file of the version package:
    the mode alone is out of the range, and the mode it leaves is 100644.
    """
    body = "架空の雲を保管する。\n"
    executable = dict(fictional_files(body))
    executable[EXECUTABLE] = ["versions/" + REV + "/main.md"]
    steps = [
        ("制定時の版を加える", "revisionAdd", True, fictional_files(body)),
        ("本文のファイルを実行可能にする（書式変更と宣言）", "format", False, executable),
    ]
    bundle_pos = next_dir("common", True) / "repo.bundle"
    c1, c2, c3 = build_bundle(bundle_pos, steps + [
        ("本文のファイルを通常のファイルに戻す", "format", False, fictional_files(body))])
    add("common", "書式変更で、版パッケージのファイルのモードを通常のファイルに戻す", ["CHG-02"], "change",
        {"kind": "change", "bundle": rel(bundle_pos), "base": c2, "head": c3},
        {"results": [{"check": "change", "result": "pass"}]}, True)
    dest = next_dir("common", False) / "repo.bundle"
    copy_file(dest, bundle_pos)
    add("common", "書式変更で、版パッケージのファイルを実行可能にする", ["CHG-02"], "change",
        {"kind": "change", "bundle": rel(dest), "base": c1, "head": c2},
        {"results": [{"check": "change", "result": "fail"}], "diagnostics": [diag("CHG-02", SV["common"])]}, False)
    bundle = next_dir("common", False) / "repo.bundle"
    _, c2, c3 = build_bundle(bundle, steps + [
        ("本文のファイルを通常のファイルに戻す（属性の更新と宣言）", "metadata", False, fictional_files(body))])
    add("common", "属性の更新と宣言して、版パッケージのファイルのモードだけを変える", ["CHG-02"], "change",
        {"kind": "change", "bundle": rel(bundle), "base": c2, "head": c3},
        {"results": [{"check": "change", "result": "fail"}], "diagnostics": [diag("CHG-02", SV["common"])]}, False)


# --- 2026-11-20 (#149): the first commit of a repository, checked with no base (CHG-02, CHG-03) ------------------
def root_commits(bundle):
    """The commits without a parent of the branch main of a git bundle."""
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(["git", "clone", "-q", "--bare", str(bundle), tmp + "/r"], check=True, capture_output=True)
        out = subprocess.run(["git", "-C", tmp + "/r", "rev-list", "--max-parents=0", "main"], check=True,
                             capture_output=True).stdout.decode()
    return out.split()


def first_commits():
    """The first commit (without a parent) is checked with no record before it; the index omits base.

    The positive is the first commit of the bundle of common-004 (revisionAdd). The first negative adds the same
    files but declares format: a first commit that is not revisionAdd (CHG-03). The second declares revisionAdd but
    records the text of the version as executable: every file of the data of a first commit is checked (CHG-02).
    """
    first = {case["id"]: case["input"] for case in INDEX["common"]}
    shared = first["common-004"]
    # A case without base reads head as the first commit: each head must be the only commit without a parent.
    assert root_commits(ROOT / shared["bundle"]) == [shared["base"]], shared
    add("common", "法令リポジトリの最初のcommitで、制定時の版を加える", ["CHG-02", "CHG-03"], "change",
        {"kind": "change", "bundle": shared["bundle"], "head": shared["base"]},
        {"results": [{"check": "change", "result": "pass"}]}, True)
    body = "架空の雲を保管すろ。\n"
    bundle = next_dir("common", False) / "repo.bundle"
    (c1,) = build_bundle(bundle, [("制定時の版を加える（書式変更と宣言）", "format", False, fictional_files(body))])
    assert root_commits(bundle) == [c1], bundle
    add("common", "法令リポジトリの最初のcommitを、書式変更と宣言する", ["CHG-03"], "change",
        {"kind": "change", "bundle": rel(bundle), "head": c1},
        {"results": [{"check": "change", "result": "fail"}], "diagnostics": [diag("CHG-03", SV["common"])]}, False)
    executable = dict(fictional_files(body))
    executable[EXECUTABLE] = ["versions/" + REV + "/main.md"]
    bundle = next_dir("common", False) / "repo.bundle"
    (c1,) = build_bundle(bundle, [("制定時の版を加える（本文のファイルを実行可能にする）", "revisionAdd", True, executable)])
    assert root_commits(bundle) == [c1], bundle
    add("common", "法令リポジトリの最初のcommitで、版パッケージのファイルを実行可能にして置く", ["CHG-02"], "change",
        {"kind": "change", "bundle": rel(bundle), "head": c1},
        {"results": [{"check": "change", "result": "fail"}], "diagnostics": [diag("CHG-02", SV["common"])]}, False)


# --- 2026-11-24 (#152): the first commit of the repository of the registry (CHG-02, CHG-03) ----------------------
REGISTRY_FIRST = {
    "space.yaml": "{}\n",
    "records/20990101-act-1.yaml": (
        "schemaVersion: loj-registry/v1alpha1\nid: 20990101-act-1\nlabel: 架空法律第一号（実在しないサンプル）\n"
        "status: active\nidentity:\n  evidence: [{source: src-fiction, locator: 本文}]\n  verification: {state: confirmed}\n"
        "collection: {state: notCollected}\nsources:\n  - {id: src-fiction, kind: other, title: 架空の原典}\n"
        "numbers: []\nexternalIds: []\n"),
}


def registry_first_commits():
    """The first commit of the repository of the registry declares metadata (CHG-03); the index says registry.

    The positive registers one Record with space.yaml: in the range of metadata (CHG-02), with no version and no
    retired Record to compare. The negative adds the same files but declares revisionAdd, the kind a first commit of
    a law repository declares: a first commit of the registry that is not metadata fails by CHG-03 alone.
    """
    for success, kind, title in ((True, "metadata", "登録台帳のリポジトリの最初のcommitで、Recordを登録する"),
                                 (False, "revisionAdd", "登録台帳のリポジトリの最初のcommitを、状態の追加と宣言する")):
        bundle = next_dir("common", success) / "repo.bundle"
        (c1,) = build_bundle(bundle, [("Recordを登録する", kind, False, dict(REGISTRY_FIRST))])
        assert root_commits(bundle) == [c1], bundle
        expected = {"results": [{"check": "change", "result": "pass" if success else "fail"}]}
        if not success:
            expected["diagnostics"] = [diag("CHG-03", SV["common"])]
        add("common", title, ["CHG-02", "CHG-03"] if success else ["CHG-03"], "change",
            {"kind": "change", "bundle": rel(bundle), "head": c1, "repository": "registry"}, expected, success)
    # A first commit with neither space.yaml nor history.yaml: the kind of repository comes from the input alone
    # (CHG-03). Read as a law repository, metadata would not be revisionAdd and the commit would fail.
    bundle = next_dir("common", True) / "repo.bundle"
    (c1,) = build_bundle(bundle, [("説明を置く", "metadata", False, {"README.md": "架空の登録台帳である。\n"})])
    assert root_commits(bundle) == [c1], bundle
    add("common", "登録台帳のリポジトリの最初のcommitで、正本のデータのファイルを置かずに説明だけを置く", ["CHG-03"], "change",
        {"kind": "change", "bundle": rel(bundle), "head": c1, "repository": "registry"},
        {"results": [{"check": "change", "result": "pass"}]}, True)


# --- 2026-11-24 (#163): a canonical branch started on a commit of the legacy repository (CHG-02, CHG-03) -----------
LEGACY_STEPS = [
    ("Initial commit", None, False, {"README.md": "架空法律第一号の旧リポジトリである。\n"}),
    ("旧形式の本文を加える", None, False, {"README.md": "架空法律第一号の旧リポジトリである。\n",
                                       "main.md": "# 第一条\n\n架空の雲を保管すろ。\n"}),
]


def legacy_boundary():
    """The canonical branch main starts on the commits of the legacy repository; the index gives legacyBoundary.

    The bundle holds two legacy commits without a declaration (the second is the boundary), then the first commit
    of the canonical branch (revisionAdd, which makes history.yaml whole) and a correction. Given the boundary, the
    legacy commits are not checked and its child is the first commit, in the range of a first commit (CHG-02); a
    base on a legacy commit starts at the same first commit. Without the boundary, the commit without a parent is
    the first commit: both legacy commits fail by CHG-03, and the commit of revisionAdd has a record before it, so
    making the top-level fields of history.yaml is out of its range (CHG-02). The boundary is never inferred from
    the files or the missing trailers (CHG-03). The last negative declares the child of the boundary format.
    """
    body = "架空の雲を保管すろ。\n"
    steps = LEGACY_STEPS + [
        ("制定時の版を加える", "revisionAdd", True, fictional_files(body)),
        ("第一条の誤転記を直す", "correction", True, fictional_files("架空の雲を保管する。\n")),
    ]
    pos = next_dir("common", True) / "repo.bundle"
    l1, l2, c1, c2 = build_bundle(pos, steps)
    assert root_commits(pos) == [l1], pos
    add("common", "旧リポジトリのcommitの上に始めた正本ブランチを、旧履歴の境界を与えて検査する", ["CHG-02", "CHG-03"], "change",
        {"kind": "change", "bundle": rel(pos), "head": c2, "legacyBoundary": l2},
        {"results": [{"check": "change", "result": "pass"}]}, True)
    add("common", "旧履歴の境界を与え、旧履歴のcommitをbaseとして検査する", ["CHG-03"], "change",
        {"kind": "change", "bundle": rel(pos), "base": l1, "head": c2, "legacyBoundary": l2},
        {"results": [{"check": "change", "result": "pass"}]}, True)
    dest = next_dir("common", False) / "repo.bundle"
    copy_file(dest, pos)
    add("common", "旧リポジトリのcommitの上に始めた正本ブランチを、旧履歴の境界を与えずに検査する", ["CHG-02", "CHG-03"], "change",
        {"kind": "change", "bundle": rel(dest), "head": c2},
        {"results": [{"check": "change", "result": "fail"}],
         "diagnostics": [diag("CHG-03", SV["common"]), diag("CHG-02", SV["common"])]}, False)
    # A boundary that is head itself is not a boundary (CHG-03): the check fails by CHG-03 without checking a commit.
    dest = next_dir("common", False) / "repo.bundle"
    copy_file(dest, pos)
    add("common", "headそのものを旧履歴の境界として与える", ["CHG-03"], "change",
        {"kind": "change", "bundle": rel(dest), "head": c2, "legacyBoundary": c2},
        {"results": [{"check": "change", "result": "fail"}], "diagnostics": [diag("CHG-03", SV["common"])]}, False)
    bundle = next_dir("common", False) / "repo.bundle"
    _, l2, c1 = build_bundle(bundle, LEGACY_STEPS + [("制定時の版を加える（書式変更と宣言）", "format", False, fictional_files(body))])
    add("common", "旧履歴の境界を親とする最初のcommitを、書式変更と宣言する", ["CHG-03"], "change",
        {"kind": "change", "bundle": rel(bundle), "head": c1, "legacyBoundary": l2},
        {"results": [{"check": "change", "result": "fail"}], "diagnostics": [diag("CHG-03", SV["common"])]}, False)


# --- 2026-11-24 (#159): spacing notes on line breaks of a two-line setting (GLYPH-02, GLYPH-04, MD-04) ----------
SPACING_POS = "conformance/loj-glyphs/v1alpha1/valid/glyph-021/repo"


def spacing_line_breaks():
    """A fictional imperial order whose version has three spacing notes on 二行割り line breaks (hand-written).

    one.md uses LF and two.md CRLF. g1 records the LF written in the text, g2 the CR and LF of a CRLF line (its
    offset is the CR), g3 the empty string for a break not written (its offset is after the last character of the
    line read first). The negative records only LF for the CRLF line break of g2: the text at the offset is CR LF.
    """
    add("glyph", "二行割りの行の区切りを書いた・書かなかった字間の注記（LFとCRLFの本文）",
        ["GLYPH-02", "GLYPH-04", "MD-04"], "L3", {"kind": "repository", "path": SPACING_POS},
        {"results": [l3("evidence")]}, True, "evidence")
    dest = next_dir("glyph", False) / "repo"
    mutate(dest, SPACING_POS, [("versions/q7v3n2xc/glyphs.yaml", r'recorded: "\r\n"', r'recorded: "\n"')])
    add("glyph", "CRLFの行の区切りをLFだけで記録した字間の注記", ["GLYPH-04", "GLYPH-02"], "L3",
        {"kind": "repository", "path": rel(dest)},
        {"results": [l3("evidence", "fail")], "diagnostics": [diag("GLYPH-04", SV["glyph"])]}, False, "evidence")
    # GLYPH-04 (#161): the range of a note stays in the text and never ends between the CR and LF of a CRLF.
    for title, edits in [
        ("文字列の長さを超えるoffsetを持つ空の字間の注記", [("versions/q7v3n2xc/glyphs.yaml", "offset: 9\n", "offset: 99\n")]),
        ("CRLFの行の終端のLFの位置を指してLFだけを記録した字間の注記",
         [("versions/q7v3n2xc/glyphs.yaml", 'offset: 14\n    recorded: "\\r\\n"', 'offset: 15\n    recorded: "\\n"')]),
    ]:
        dest = next_dir("glyph", False) / "repo"
        mutate(dest, SPACING_POS, edits)
        add("glyph", title, ["GLYPH-04"], "L3", {"kind": "repository", "path": rel(dest)},
            {"results": [l3("evidence", "fail")], "diagnostics": [diag("GLYPH-04", SV["glyph"])]}, False, "evidence")
    # GLYPH-04 (#161): the boundary of the range. An empty note whose offset equals the length of the text points to
    # its end and is in the range. A fixture of the boundary only: g3 no longer points to the break of its source.
    pos = next_dir("glyph", True) / "repo"
    mutate(pos, SPACING_POS, [("versions/q7v3n2xc/glyphs.yaml", "offset: 9\n", "offset: 28\n")])
    add("glyph", "文字列の長さに等しいoffsetを持つ空の字間の注記（文字列の末尾）", ["GLYPH-04"], "L3",
        {"kind": "repository", "path": rel(pos)}, {"results": [l3("evidence")]}, True, "evidence")
    for title, edits in [
        ("CRLFの行の終端のCRとLFの間を指す空の字間の注記", [("versions/q7v3n2xc/glyphs.yaml", "offset: 9\n", "offset: 27\n")]),
        ("CRLFの行の終端のCRだけを記録した字間の注記",
         [("versions/q7v3n2xc/glyphs.yaml", 'offset: 14\n    recorded: "\\r\\n"', 'offset: 14\n    recorded: "\\r"')]),
    ]:
        dest = next_dir("glyph", False) / "repo"
        mutate(dest, SPACING_POS, edits)
        add("glyph", title, ["GLYPH-04"], "L3", {"kind": "repository", "path": rel(dest)},
            {"results": [l3("evidence", "fail")], "diagnostics": [diag("GLYPH-04", SV["glyph"])]}, False, "evidence")


def staged_enactment():
    """The two versions of a staged enactment (鉱山保安法, hand-written, #173): the origin and a Revision whose basis is
    the enactment. The text of both is absent: whether a version package holds the whole promulgated text (HIST-05) is
    compared with the sources, not checked on the data.
    """
    add("hist", "段階施行の二つの版（鉱山保安法）", ["HIST-04", "HIST-05", "TIME-04"], "L3",
        {"kind": "repository", "path": "conformance/loj-history/v1alpha1/valid/hist-062/repo"},
        {"results": [l3("historyStructure")]}, True, "historyStructure")


# --- 2026-11-25: cases listed as missing in docs/coverage.md before the first publication -------------------------
def row_key_versions(base, versions, based_on=None):
    """Fictional versions of one law for HIST-13, more general than row_key_files.

    versions: one dict per Revision of ROW_REVS (in order) with "status" (complete / partial / absent), "tables"
    (the row keys of each table of 第一条第一項, in table order; table numbers are 1, 2, ... as TABLE-01 requires) and
    optionally "broken" (the text breaks HEAD-01, so the version fails L1). based_on: the index of the Revision each
    later Revision is based on (default: the one before it).
    """
    fict = "      evidence: [{source: src-fiction, locator: %s}]\n      verification: {state: unverified, reason: 架空の資料}\n"
    clouds = dict(CLOUDS, g7h8="高積雲")
    rels, revs = "", ""
    for i, (rev, version) in enumerate(zip(ROW_REVS, versions)):
        day = "2099-0%d-01" % (i + 2)
        raw = "二千九十九年" + "二三四"[i] + "月一日"
        effective = ("    effective:\n      state: date\n      value: \"" + day + "\"\n      raw: " + raw + "\n"
                     "      precision: day\n" + fict % "施行期日")
        if i:
            rels += ("  - id: rel-%d\n    type: amends\n    from: {id: 2099%02d01-act-%d, label: 架空の改正法}\n" % (i, i + 2, i + 10)
                     + "    evidence: [{source: src-fiction, locator: 本則}]\n"
                     "    verification: {state: unverified, reason: 架空の資料}\n    status: active\n    items:\n"
                     "      - id: i1\n        scope: {text: 第一条の表}\n        effective:\n          state: date\n"
                     "          value: \"" + day + "\"\n          raw: " + raw + "\n          precision: day\n"
                     "          evidence: [{source: src-fiction, locator: 附則}]\n"
                     "          verification: {state: unverified, reason: 架空の資料}\n"
                     "        evidence: [{source: src-fiction, locator: 附則}]\n"
                     "        verification: {state: unverified, reason: 架空の資料}\n")
        parent = (based_on or {}).get(i, i - 1)
        revs += "  - id: " + rev + "\n"
        revs += ("    origin: enactment\n" if not i else
                 "    basedOn: " + ROW_REVS[parent] + "\n    basis: [{relation: rel-%d, items: [i1]}]\n" % i)
        status = version["status"]
        if status == "absent":
            text = "    text:\n      status: absent\n"
        else:
            text = ("    text:\n      status: " + ("partial\n      gaps: [{text: 第一条の表の一部}]" if status == "partial"
                                                  else "complete") + "\n"
                    "      sources: [{source: src-fiction, locator: 本則}]\n      glyphCheck: unverified\n")
        revs += effective + "    applicability: {state: unsurveyed}\n" + text + "    status: active\n"
        if status == "absent":
            continue
        tables = "".join(
            "<!-- loj:table number=%d -->\n" % (n + 1) +
            "".join("<!-- loj:row key=" + k + " -->\n<!-- loj:cell -->\n" + clouds[k] + "\n<!-- loj:end-cell -->\n"
                    "<!-- loj:end-row -->\n" for k in keys) + "<!-- loj:end-table -->\n"
            for n, keys in enumerate(version["tables"]))
        md = (("# 一\n" if version.get("broken") else "# 第一条\n") +
              "<!-- loj:paragraph number=1 -->\n架空の雲の種類を次のように定める。\n" + tables +
              "<!-- loj:end-paragraph -->\n")
        law = {"schemaVersion": "loj/v1alpha2",
               "law": {"id": ROW_LAW[0], "title": ROW_LAW[1], "type": "act", "number": "架空法律第二号",
                       "promulgatedAt": "2099-02-01", "language": "ja"},
               "documents": [{"path": "main.md", "parent": "main"}]}
        folder = base / "versions" / rev
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "law.yaml").write_bytes((json.dumps(law, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
        (folder / "main.md").write_bytes(md.encode("utf-8"))
    history = ("schemaVersion: loj-history/v1alpha1\nrecord: {id: " + ROW_LAW[0] + ", label: 架空雲分類法}\n"
               "sources:\n  - {id: src-fiction, kind: other, title: 適合ケースのための架空の資料}\n"
               "relations:\n" + rels + "revisions:\n" + revs + "coverage: {state: unconfirmed}\n")
    (base / "history.yaml").write_bytes(history.encode("utf-8"))


def row_key_gaps():
    """HIST-13 cases that docs/coverage.md listed as missing. Each would fail if the skipped version were compared or
    if the key c3d4 of the first table were compared across a renumbered table or across two branches; HIST-13 says
    none of them is compared, so every one passes the history structure category."""
    full = {"status": "complete", "tables": [["a1b2", "c3d4"]]}
    cases = [
        ("本文のない版を挟んで行がなくても、削ったとみなさない（架空）", ["HIST-13", "HIST-08"],
         [full, {"status": "absent"}, full], None),
        ("L1が不合格の版で行がなくても、削ったとみなさない（架空）", ["HIST-13", "VAL-05"],
         [full, {"status": "complete", "tables": [["a1b2"]], "broken": True}, full], None),
        ("表の番号が変わった表の行のkeyを、前の番号の表と比べない（架空）", ["HIST-13", "ID-01", "TABLE-01"],
         [full, {"status": "complete", "tables": [["g7h8"], ["a1b2"]]},
          {"status": "complete", "tables": [["g7h8"], ["a1b2", "c3d4"]]}], None),
        ("basedOnが分岐した別の枝の版とは、行のkeyを比べない（架空）", ["HIST-13", "HIST-04"],
         [full, {"status": "complete", "tables": [["a1b2"]]}, full], {2: 0}),
    ]
    for title, requirements, versions, based_on in cases:
        dest = next_dir("hist", True) / "repo"
        row_key_versions(dest, versions, based_on)
        add("hist", title, requirements, "L3", {"kind": "repository", "path": rel(dest)},
            {"results": [l3("historyStructure")]}, True, "historyStructure")


VARIANCES = ("      variances:\n"
             "        - scope: {text: 第一條}\n"
             "          readings:\n"
             "            - {source: src-kanpo-19480720, locator: 1コマ 第一條, raw: 美しい風習を育てつつ}\n"
             "            - {source: src-goshomei, locator: 第一條, raw: 美しい風俗を育てつつ}\n"
             "          verification: {state: disputed, reason: 適合ケースのための架空の食い違い。官報正誤は見つかっていない}\n")


def text_variances():
    """HIST-08 text.variances, which had no case. The positive records a (fictional) wording difference between the
    官報 and the 御署名原本 of the enactment version; the negative gives one reading only (two or more: HIST-08,
    a schema error of the history manifest)."""
    anchor = "      glyphNotes: versions/98mj5vgx/glyphs.yaml\n"
    pos = next_dir("hist", True) / "repo"
    mutate(pos, HIST_POS, [("history.yaml", anchor, anchor + VARIANCES)])
    add("hist", "原典資料の間の文言の食い違いを、官報正誤が見つからない間はdisputedとして記録する", ["HIST-08", "GLYPH-07", "TYPE-06"],
        "L3", {"kind": "repository", "path": rel(pos)}, {"results": [l3("historyStructure")]}, True, "historyStructure")
    dest = next_dir("hist", False) / "repo"
    mutate(dest, rel(pos), [("history.yaml",
                             "            - {source: src-goshomei, locator: 第一條, raw: 美しい風俗を育てつつ}\n", "")])
    add("hist", "原典資料の間の文言の食い違いの資料ごとの文言が一件だけ", ["HIST-08"], "L3",
        {"kind": "repository", "path": rel(dest)},
        {"results": [l3("historyStructure", "fail")], "diagnostics": [diag("HIST-08", SV["hist"])]}, False,
        "historyStructure")


IVS_NOTE = ('  - id: g30\n'
            '    node: 19480720-law-178/main/article/2/paragraph/1/table/1/row/b6gr/cell/1\n'
            '    offset: 1\n'
            '    recorded: "日' + chr(0xE0100) + '"\n'
            '    kind: selected\n'
            '    ivd: {collection: Moji_Joho, sequence: 65E5 E0100}\n'
            '    evidence: [{source: src-kanpo-19480720, locator: "1コマ 第二條 元日の項"}]\n'
            '    verification: {state: unverified, reason: "適合ケースのための架空の注記"}\n')
VARIANCE_NOTE = ('  - id: g31\n'
                 '    node: 19480720-law-178/main/article/1/paragraph/1\n'
                 '    offset: 15\n'
                 '    recorded: "國"\n'
                 '    kind: variance\n'
                 '    candidates: ["國", "国"]\n'
                 '    evidence: [{source: src-kanpo-19480720, locator: "1コマ 第一條"}, {source: src-goshomei, locator: "第一條"}]\n'
                 '    verification: {state: unverified, reason: "適合ケースのための架空の注記"}\n')
CORRECTION_ILLEGIBLE = ('  - id: g32\n'
                        '    node: 19480720-law-178/main/article/2/paragraph/1/table/1/row/2aph/cell/3\n'
                        '    offset: 13\n'
                        '    recorded: "國"\n'
                        '    kind: illegible\n'
                        '    basis: otherSource\n'
                        '    evidence: [{source: src-kanpo-19480928, locator: "2コマ 正誤 第二條八行（かすれ）"}, '
                        '{source: src-goshomei, locator: "第二條 憲法記念日の項"}]\n'
                        '    verification: {state: unverified, reason: "適合ケースのための架空の注記"}\n')


def glyph_note_gaps():
    """GLYPH-05 cases that docs/coverage.md listed as missing, on the enactment version of hist-001 (fictional notes).

    ivd: a selected note whose recorded text has a variation selector (U+E0100) carries ivd; the negatives drop it,
    make its sequence differ from recorded, and give ivd to a note without a selector. These are checked by the
    validator, not by the schema. variance: a positive, and a negative without candidates (a schema error).
    officialCorrection: the 官報正誤 as the publication whose copy cannot be read (GLYPH-05 allows promulgation or
    officialCorrection there)."""
    pos = next_dir("glyph", True) / "repo"
    mutate(pos, HIST_POS, [(ENA + "glyphs.yaml", "  - id: g15\n", IVS_NOTE + "  - id: g15\n"),
                           (ENA + "main.md", "元日\n", "元日" + chr(0xE0100) + "\n")])
    add("glyph", "異体字セレクタを付けた字の注記に、IVDのコレクションと登録の並びを書く", ["GLYPH-05", "GLYPH-06", "CHAR-03"], "L3",
        {"kind": "repository", "path": rel(pos)}, {"results": [l3("evidence")]}, True, "evidence")
    negatives = [
        ("異体字セレクタを付けた字の注記にivdがない", [(ENA + "glyphs.yaml", "    ivd: {collection: Moji_Joho, sequence: 65E5 E0100}\n", "")]),
        ("ivdの登録の並びが、注記の字と合わない", [(ENA + "glyphs.yaml", "sequence: 65E5 E0100}", "sequence: 65E5 E0101}")]),
        ("異体字セレクタを含まない注記にivdを書く",
         [(ENA + "glyphs.yaml", '    recorded: "号"\n    kind: ambiguous\n',
           '    recorded: "号"\n    kind: ambiguous\n    ivd: {collection: Moji_Joho, sequence: 53F7 E0100}\n')]),
    ]
    for title, edits in negatives:
        dest = next_dir("glyph", False) / "repo"
        mutate(dest, rel(pos), edits)
        add("glyph", title, ["GLYPH-05"], "L3", {"kind": "repository", "path": rel(dest)},
            {"results": [l3("evidence", "fail")], "diagnostics": [diag("GLYPH-05", SV["glyph"])]}, False, "evidence")
    pos = next_dir("glyph", True) / "repo"
    mutate(pos, HIST_POS, [(ENA + "glyphs.yaml", "  - id: g15\n", VARIANCE_NOTE + "  - id: g15\n")])
    add("glyph", "官報とほかの原典資料で字体が違う字に、官報の字を置いて両方の字を注記する", ["GLYPH-02", "GLYPH-05", "GLYPH-07"], "L3",
        {"kind": "repository", "path": rel(pos)}, {"results": [l3("evidence")]}, True, "evidence")
    dest = next_dir("glyph", False) / "repo"
    mutate(dest, rel(pos), [(ENA + "glyphs.yaml", '    candidates: ["國", "国"]\n', "")])
    add("glyph", "字体の違いの注記に候補がない", ["GLYPH-05"], "L3", {"kind": "repository", "path": rel(dest)},
        {"results": [l3("evidence", "fail")], "diagnostics": [diag("GLYPH-05", SV["glyph"])]}, False, "evidence")
    pos = next_dir("glyph", True) / "repo"
    mutate(pos, HIST_POS, [(ENA + "glyphs.yaml", "  - id: g15\n", CORRECTION_ILLEGIBLE + "  - id: g15\n")])
    add("glyph", "官報正誤の複製で読めず、ほかの原典資料で読めた字を本文に置く判読困難の注記", ["GLYPH-05", "GLYPH-06", "GLYPH-07"], "L3",
        {"kind": "repository", "path": rel(pos)}, {"results": [l3("evidence")]}, True, "evidence")


# --- 2026-11-26: missing cross-record cases (XREF-01, XREF-02, XREF-05, XREF-06) -----------------
MERGED_ID = ("m4x8k2p7qd", "架空の統合した登録")
SPLIT_ID = ("s5r9n3t6wc", "架空の分割した登録")
SPLIT_OTHER = ("20990602-law-4", "架空の分割先の候補")
TOTAL_POS = "conformance/common/v1alpha1/valid/common-017"
PROM_POS = "conformance/common/v1alpha1/valid/common-015"
NUMBER_179 = "conformance/common/v1alpha1/valid/common-014/hist-001"


def replaced_record(ident, label, status, targets):
    """A merged or split Record of the fictional registries (REG-02: replacedBy in the same registry)."""
    body = ("schemaVersion: loj-registry/v1alpha1\nid: " + ident + "\nlabel: " + label + "\nstatus: " + status + "\n"
            "identity:\n  evidence: [{source: src-fictional, locator: 登録の記録}]\n  verification: {state: confirmed}\n"
            "collection: {state: notCollected}\n"
            "sources:\n  - {id: src-fictional, kind: other, title: 適合ケースのための架空の資料}\nnumbers: []\nexternalIds: []\n"
            "replacedBy:\n")
    for target, state in targets:
        body += ("  - record: {id: %s, label: %s}\n" % target
                 + "    evidence: [{source: src-fictional, locator: %sの記録}]\n" % ("統合" if status == "merged" else "分割")
                 + ("    verification: {state: confirmed}\n" if state == "confirmed" else
                    "    verification: {state: unverified, reason: 分割先が確定していない（架空）}\n"))
    return body


def fictional_record_body(ident, label):
    return ("schemaVersion: loj-registry/v1alpha1\nid: " + ident + "\nlabel: " + label + "\nstatus: active\n"
            "identity:\n  evidence: [{source: src-fictional, locator: 題名}]\n  verification: {state: confirmed}\n"
            "collection: {state: notCollected}\n"
            "sources:\n  - {id: src-fictional, kind: other, title: 適合ケースのための架空の資料}\nnumbers: []\nexternalIds: []\n")


def cross_record_gaps():
    registry, old, new = TOTAL_POS + "/registry", TOTAL_POS + "/" + OLD_LAW[0], TOTAL_POS + "/" + NEW_LAW[0]
    resolution = {"check": "L4", "category": "relationResolution"}
    consistency = {"check": "L4", "category": "relationConsistency"}
    from_new = "    from: {id: %s, label: %s}\n" % NEW_LAW
    # XREF-02: the from of the old Record's relation is a merged Record; it resolves to its target, the new Record.
    dest = next_dir("common", True)
    mutate(dest / "registry", registry, [], {"records/%s.yaml" % MERGED_ID[0]: replaced_record(
        MERGED_ID[0], MERGED_ID[1], "merged", [(NEW_LAW, "confirmed")])})
    mutate(dest / OLD_LAW[0], old, [("history.yaml", from_new, "    from: {id: %s, label: %s}\n" % MERGED_ID)])
    add("common", "全部改正の関係の起点が、全部改正後のRecordへ統合したRecord（架空）", ["XREF-01", "XREF-02", "REG-02"], "L4",
        {"kind": "records", "registry": rel(dest / "registry"), "repositories": [rel(dest / OLD_LAW[0]), new]},
        {"results": [dict(consistency, result="pass")]}, True, "relationConsistency")
    # XREF-02: the from is a split Record; it is not resolved, so whether it is the same Record is undetermined.
    dest = next_dir("common", True)
    mutate(dest / "registry", registry, [], {
        "records/%s.yaml" % SPLIT_ID[0]: replaced_record(SPLIT_ID[0], SPLIT_ID[1], "split",
                                                          [(NEW_LAW, "unverified"), (SPLIT_OTHER, "unverified")]),
        "records/%s.yaml" % SPLIT_OTHER[0]: fictional_record_body(*SPLIT_OTHER)})
    mutate(dest / OLD_LAW[0], old, [("history.yaml", from_new, "    from: {id: %s, label: %s}\n" % SPLIT_ID)])
    add("common", "全部改正の関係の起点が、分割したRecord（架空）", ["XREF-01", "XREF-02", "VAL-04"], "L4",
        {"kind": "records", "registry": rel(dest / "registry"), "repositories": [rel(dest / OLD_LAW[0]), new]},
        {"results": [dict(consistency, result="incomplete")],
         "diagnostics": [diag("XREF-02", SV["common"], "undetermined")]}, True, "relationConsistency")
    # XREF-02: the old Record is registered, but its history manifest is not in the input (not fetched).
    add("common", "totallyRevisesが指す旧Recordの履歴マニフェストを取得できない（架空）", ["XREF-02", "VAL-04", "VAL-06"], "L4",
        {"kind": "records", "registry": registry, "repositories": [new]},
        {"results": [dict(consistency, result="incomplete")]}, True, "relationConsistency")
    # XREF-01: the end of a confirmed relation (the Record whose manifest holds it) is withdrawn.
    dest = next_dir("common", False)
    mutate(dest / "registry", registry, [("records/%s.yaml" % OLD_LAW[0], "status: active\n", "status: withdrawn\n")])
    mutate(dest / OLD_LAW[0], old, [("history.yaml", "    verification: {state: unverified, reason: 架空の資料}\n    status: active\n",
                                     "    verification: {state: confirmed}\n    status: active\n")])
    add("common", "確定した関係の終点が登録を撤回したRecord（架空）", ["XREF-01", "REG-02", "VAL-06"], "L4",
        {"kind": "records", "registry": rel(dest / "registry"), "repositories": [rel(dest / OLD_LAW[0]), new]},
        {"results": [dict(resolution, result="fail")], "diagnostics": [diag("XREF-01", SV["common"])],
         "references": [{"target": "loj:loj/" + OLD_LAW[0], "result": "nonexistentConfirmed"}]}, False,
        "relationResolution")

    # XREF-05: the state of the adopted number claim of the Act on National Holidays.
    display = {"check": "L4", "category": "displayConsistency", "result": "pass"}
    law = "records/19480720-law-178.yaml"
    text = (ROOT / REG_POS / law).read_bytes().decode("utf-8")
    numbers = text[text.index("numbers:\n"):text.index("externalIds:\n")]
    claim = ("numbers:\n  - id: n1\n    state: %s\n"
             "    evidence: [{source: src-kanpo-19480720, locator: 1コマ 法律の冒頭}]\n"
             "    verification: {state: unverified, reason: 適合ケースのための架空の変更}\n    decision: adopted\n")
    conflicting = ("numbers:\n  - id: n1\n    state: conflicting\n    raw:\n"
                   "      - {source: src-kanpo-19480720, raw: 法律第百七十八号}\n      - {source: src-egov, raw: 法律第百七十九号}\n"
                   "    evidence: [{source: src-kanpo-19480720, locator: 1コマ 法律の冒頭}, {source: src-egov, locator: 法令番号}]\n"
                   "    verification: {state: disputed, reason: 適合ケースのための架空の食い違い}\n    decision: adopted\n")
    for success, title, edit, repo, warns in [
        (True, "採用中の番号主張が番号のないことを確認したもので、版パッケージに番号がある", claim % "nonexistent", HIST_POS, True),
        (True, "採用中の番号主張の番号が不明で、版パッケージに番号がある", claim % "unknown", HIST_POS, True),
        # Not judged: the number of the version package (百七十九号) would not match an exists claim either.
        (True, "採用中の番号主張が資料の間で食い違う（判定しない）", conflicting, NUMBER_179, False),
    ]:
        dest = next_dir("common", success) / "registry"
        mutate(dest, REG_POS, [(law, numbers, edit)])
        expected = {"results": [display]}
        if warns:
            expected["diagnostics"] = [diag("XREF-05", SV["common"], "warning")]
        add("common", title, ["XREF-05", "REG-03"], "L4", {"kind": "records", "registry": rel(dest), "repositories": [repo]},
            expected, success, "displayConsistency")
    dest = next_dir("common", True) / "registry"
    mutate(dest, REG_POS, [(law, "    decision: adopted\n", "    decision: pending\n")])
    add("common", "採用中の番号主張がない（判定しない）", ["XREF-05", "REG-03"], "L4",
        {"kind": "records", "registry": rel(dest), "repositories": [NUMBER_179]}, {"results": [display]}, True,
        "displayConsistency")

    # XREF-06: the second Record's relation from the same amending law, against hist-016 (promulgated 2099-06-01).
    time = {"check": "L4", "category": "timeConsistency"}
    other = PROM_POS + "/hist-016b"
    prom = ('    promulgated:\n      state: date\n      value: "2099-06-01"\n      raw: 令和八十一年六月一日\n      precision: day\n'
            "      evidence: [{source: src-fictional, locator: 公布の日}]\n      verification: {state: unverified, reason: 架空の資料}\n")
    june2 = prom.replace('"2099-06-01"', '"2099-06-02"').replace("六月一日", "六月二日")
    from_law2 = "    from: {id: 20990601-law-2, label: 架空の改正法}\n"
    retracted = ("  - id: rel-amend-x\n    type: amends\n" + from_law2 + june2
                 + "    evidence: [{source: src-fictional, locator: 附則第一条}]\n"
                 "    verification: {state: unverified, reason: 公布の日を誤って記録した関係の撤回（架空）}\n"
                 "    status: retracted\n    items:\n      - id: i1\n        scope: {text: 第一条}\n"
                 "        effective: {state: unknown, reason: 適合ケースで省略}\n"
                 "        evidence: [{source: src-fictional, locator: 附則第一条}]\n"
                 "        verification: {state: unverified, reason: 架空の資料}\n")
    month = ('    promulgated:\n      state: date\n      value: "2099-06"\n      raw: 令和八十一年六月\n      precision: month\n'
             "      evidence: [{source: src-fictional, locator: 公布の日}]\n      verification: {state: unverified, reason: 架空の資料}\n")
    dest = next_dir("common", True) / "hist-016b"
    mutate(dest, other, [("history.yaml", prom, month)])
    add("common", "同じ改正法令の公布の時点の一方が確定日でない（架空）", ["XREF-06", "TIME-03", "VAL-04"], "L4",
        {"kind": "records", "registry": PROM_POS + "/registry", "repositories": [POS_016, rel(dest)]},
        {"results": [dict(time, result="incomplete")], "diagnostics": [diag("XREF-06", SV["common"], "undetermined")]},
        True, "timeConsistency")
    for title, requirements, edits in [
        ("撤回した関係の公布の時点は比べない（架空）", ["XREF-06", "HIST-03"], [("history.yaml", "revisions:\n", retracted + "revisions:\n")]),
        ("一方の関係だけが公布の時点を持つ（判定しない）", ["XREF-06", "HIST-03"], [("history.yaml", prom, "")]),
    ]:
        dest = next_dir("common", True) / "hist-016b"
        mutate(dest, other, edits)
        add("common", title, requirements, "L4",
            {"kind": "records", "registry": PROM_POS + "/registry", "repositories": [POS_016, rel(dest)]},
            {"results": [dict(time, result="pass")]}, True, "timeConsistency")
    for success, title, ident, status, targets in [
        (False, "統合したRecordを起点とする関係の公布の時点が、統合先を起点とする関係と食い違う（架空）", MERGED_ID, "merged",
         [(("20990601-law-2", "架空の改正法"), "confirmed")]),
        (True, "分割したRecordを起点とする関係の公布の時点は比べない（架空）", SPLIT_ID, "split",
         [(("20990601-law-2", "架空の改正法"), "unverified"), (SPLIT_OTHER, "unverified")]),
    ]:
        dest = next_dir("common", success)
        records = {"records/%s.yaml" % ident[0]: replaced_record(ident[0], ident[1], status, targets)}
        if status == "split":
            records["records/%s.yaml" % SPLIT_OTHER[0]] = fictional_record_body(*SPLIT_OTHER)
        mutate(dest / "registry", PROM_POS + "/registry", [], records)
        mutate(dest / "hist-016b", other, [("history.yaml", from_law2, "    from: {id: %s, label: %s}\n" % ident),
                                           ("history.yaml", prom, june2)])
        expected = ({"results": [dict(time, result="pass")]} if success else
                    {"results": [dict(time, result="fail")], "diagnostics": [diag("XREF-06", SV["common"])]})
        add("common", title, ["XREF-01", "XREF-06"], "L4",
            {"kind": "records", "registry": rel(dest / "registry"), "repositories": [POS_016, rel(dest / "hist-016b")]},
            expected, success, "timeConsistency")


# --- 2026-11-26: common types in the registry and the rebuild report (VAL-07) ---------------------
def common_type_gaps():
    law = "records/19480720-law-178.yaml"
    identity = "  evidence: [{source: src-kanpo-19480720, locator: 1コマ}]\n  verification: {state: confirmed}\n"
    for title, rule, new in [
        ("同一性の確認が登録台帳にないSourceを指す", "TYPE-03",
         "  evidence: [{source: src-kanpo-19480721, locator: 1コマ}]\n  verification: {state: confirmed}\n"),
        ("同一性の確認のVerificationの未知の状態", "TYPE-04",
         "  evidence: [{source: src-kanpo-19480720, locator: 1コマ}]\n  verification: {state: checked}\n"),
        ("出典のない同一性の確認を確認済みにする", "TYPE-05", "  evidence: []\n  verification: {state: confirmed}\n"),
    ]:
        dest = next_dir("reg", False) / "registry"
        mutate(dest, REG_POS, [(law, identity, new)])
        add("reg", title, [rule, "REG-02"], "registry", {"kind": "registry", "path": rel(dest)},
            {"results": [{"check": "registry", "result": "fail"}], "diagnostics": [diag(rule, SV["common"])]}, False)
    for title, rule, old, new in [
        ("旧commitとの対応のVerificationの未知の状態", "TYPE-04",
         "    verification: {state: confirmed, reason: リポジトリ作成時のcommitで、本文を含まない}\n",
         "    verification: {state: checked, reason: リポジトリ作成時のcommitで、本文を含まない}\n"),
        ("出典のない差の記録を確認済みにする", "TYPE-05",
         "    evidence: [{source: src-kanpo-19480720, locator: 第二條}]\n    verification: {state: confirmed}\n",
         "    evidence: []\n    verification: {state: confirmed}\n"),
    ]:
        dest = next_dir("rebuild", False) / "repo"
        mutate(dest, HIST_POS, [("rebuild.yaml", old, new)])
        add("rebuild", title, [rule, "REBR-04" if "旧commit" in title else "REBR-05"], "rebuild", {"kind": "repository", "path": rel(dest)},
            {"results": [{"check": "rebuild", "result": "fail"}], "diagnostics": [diag(rule, SV["common"])]}, False)


# --- 2026-11-26: change checks with bundles (CHG-02, CHG-03, CHG-04) ------------------------------------------
def raw_message(subject, kind, revisions=None):
    """A whole commit message (RAW step) that declares revision ids other than REV (CHG-03)."""
    message = subject + "\n\nLoJ-Change: " + kind + "\n"
    return message + ("LoJ-Revisions: " + ", ".join(revisions) + "\n" if revisions else "")


def replace_nth(text, old, new, n):
    """Replace the n-th (0-based; -1 for the last) occurrence of old."""
    starts = [i for i in range(len(text)) if text.startswith(old, i)]
    start = starts[n]
    return text[:start] + new + text[start + len(old):]


def row_files(key_sets):
    """The files of row_key_files (fictional versions of 架空雲分類法) as a build_bundle step."""
    with tempfile.TemporaryDirectory() as tmp:
        row_key_files(Path(tmp), key_sets)
        out = {p.relative_to(tmp).as_posix(): p.read_bytes().decode("utf-8") for p in sorted(Path(tmp).rglob("*"))
               if p.is_file()}
    # A single version has no relation: row_key_files leaves the list empty.
    out["history.yaml"] = out["history.yaml"].replace("relations:\nrevisions:", "relations: []\nrevisions:")
    return out


def glyph_note_file(revision, node, offset, reason="適合ケースのための架空の注記"):
    return ("schemaVersion: loj-glyphs/v1alpha1\nrevision: " + revision + "\nnotes:\n  - id: g1\n    node: " + node + "\n"
            "    offset: " + str(offset) + "\n    recorded: \"雲\"\n    kind: variance\n    candidates: [\"雲\", \"云\"]\n"
            "    evidence: [{source: src-fiction, locator: 本則}]\n    verification: {state: unverified, reason: " + reason + "}\n")


def with_glyph_notes(files, revision, node, offset, n=0, reason="適合ケースのための架空の注記"):
    """Record fictional glyph notes for one version (the n-th Revision of history.yaml): glyphNotes and the file."""
    out = dict(files)
    path = "versions/" + revision + "/glyphs.yaml"
    check = "      glyphCheck: unverified\n"
    out["history.yaml"] = replace_nth(out["history.yaml"], check, check + "      glyphNotes: " + path + "\n", n)
    out[path] = glyph_note_file(revision, node, offset, reason)
    return out


REGISTRY_RETIRED = ("q3w8e5r2t7", "架空法律第一号の重複した登録（実在しないサンプル）")


def retired_registry_files():
    """REGISTRY_FIRST and a Record merged into it (REG-02, RID-05)."""
    out = dict(REGISTRY_FIRST)
    out["records/" + REGISTRY_RETIRED[0] + ".yaml"] = (
        "schemaVersion: loj-registry/v1alpha1\nid: " + REGISTRY_RETIRED[0] + "\nlabel: " + REGISTRY_RETIRED[1] + "\n"
        "status: merged\nidentity:\n  evidence: [{source: src-fiction, locator: 登録の記録}]\n"
        "  verification: {state: confirmed}\ncollection: {state: notCollected}\n"
        "sources:\n  - {id: src-fiction, kind: other, title: 架空の原典}\nnumbers: []\nexternalIds: []\nreplacedBy:\n"
        "  - record: {id: 20990101-act-1, label: 架空法律第一号}\n"
        "    evidence: [{source: src-fiction, locator: 統合の記録}]\n    verification: {state: confirmed}\n")
    return out


def change_partial_text():
    """CHG-04: a version with only part of its text has no AST to compare, like a version that fails L1.

    metadata compares the AST of every version, so the check is undetermined (CHG-04 undetermined). format that
    changes the files of that version without LoJ-Reviewed is an automatic conversion, which CHG-04 forbids.
    """
    body = "架空の雲を保管する。\n"
    renamed = partial_text(fictional_files(body, False, "制定時"))
    renamed["versions/" + REV + "/one.md"] = renamed.pop("versions/" + REV + "/main.md")
    law = "versions/" + REV + "/law.yaml"
    assert renamed[law].count('"main.md"') == 1
    renamed[law] = renamed[law].replace('"main.md"', '"one.md"')
    bundle_pos = next_dir("common", True) / "repo.bundle"
    c1, c2, c3 = build_bundle(bundle_pos, [
        ("第一条だけの版を加える", "revisionAdd", True, partial_text(fictional_files(body))),
        ("ラベルを改める", "metadata", False, partial_text(fictional_files(body, False, "制定時"))),
        ("一部しか本文がない版のファイルの名前を改める", "format", False, renamed),
    ])
    add("common", "一部しか本文がない版を含む属性の更新は判定不能", ["CHG-04", "CHG-02"], "change",
        {"kind": "change", "bundle": rel(bundle_pos), "base": c1, "head": c2},
        {"results": [{"check": "change", "result": "incomplete"}],
         "diagnostics": [diag("CHG-04", SV["common"], "undetermined")]}, True)
    dest = next_dir("common", False) / "repo.bundle"
    copy_file(dest, bundle_pos)
    add("common", "一部しか本文がない版のファイルを、人のレビューの記録なしに書式変更で変える", ["CHG-04"], "change",
        {"kind": "change", "bundle": rel(dest), "base": c2, "head": c3},
        {"results": [{"check": "change", "result": "fail"}],
         "diagnostics": [diag("CHG-04", SV["common"]), diag("CHG-04", SV["common"], "undetermined")]}, False)


ROW_NODE = ROW_LAW[0] + "/main/article/1/paragraph/1"


def change_dependent_files():
    """CHG-02: the files that depend on the declared version, and the same files of a version not declared.

    A correction may update the glyph notes of the declared version (GLYPH-04) and the Scope nodes that point to it
    (TYPE-08). It must not change the Revision entry or the glyph notes of a version it does not declare, even when
    the AST of that version stays the same.
    """
    # The glyph note follows 雲 when the correction puts two characters before it (offset 3 -> 5).
    bundle = next_dir("common", True) / "repo.bundle"
    c1, c2 = build_bundle(bundle, [
        ("制定時の版を加える", "revisionAdd", True,
         with_glyph_notes(fictional_files("架空の雲を保管すろ。\n"), REV, NODE, 3)),
        ("第一条の誤転記を直し、字体注記の位置を改める", "correction", True,
         with_glyph_notes(fictional_files("架空の白い雲を保管する。\n"), REV, NODE, 5)),
    ])
    add("common", "記録訂正で、同じ版の字体注記を併せて更新する", ["CHG-02", "GLYPH-04"], "change",
        {"kind": "change", "bundle": rel(bundle), "base": c1, "head": c2},
        {"results": [{"check": "change", "result": "pass"}]}, True)

    # The second version was recorded with its article as 第二条; the correction renumbers it and the Scope of the
    # amendment that is its basis, whose nodes point to the article.
    old_rev, new_rev = ROW_REVS[0], ROW_REVS[1]
    keys = [["a1b2", "c3d4"], ["a1b2", "c3d4"]]

    def scoped(article):
        out = row_files(keys)
        md = "versions/" + new_rev + "/main.md"
        out[md] = out[md].replace("# 第一条\n", "# 第" + "一二"[article - 1] + "条\n")
        scope = "scope: {text: 第一条の表}"
        assert out["history.yaml"].count(scope) == 1
        out["history.yaml"] = out["history.yaml"].replace(
            scope, "scope: {nodes: [" + ROW_LAW[0] + "/main/article/" + str(article) + "]}")
        return out

    bundle = next_dir("common", True) / "repo.bundle"
    c1, c2 = build_bundle(bundle, [
        ("二つの版を加える", "revisionAdd", False, scoped(2)),
        (raw_message("第二の版の条の番号の誤転記を直し、改正の対象範囲のノードを改める", "correction", [new_rev]), RAW, False,
         scoped(1)),
    ])
    add("common", "記録訂正で、その版を指す対象範囲のノード（Scopeのnodes）を併せて更新する", ["CHG-02", "TYPE-08"], "change",
        {"kind": "change", "bundle": rel(bundle), "base": c1, "head": c2},
        {"results": [{"check": "change", "result": "pass"}]}, True)

    # Negatives: the correction declares the first version and fixes its text, and also changes a file that depends
    # on the second version, which it does not declare. The AST of the second version does not change.
    def typo(fixed, edit=None):
        out = row_files(keys)
        if not fixed:
            md = "versions/" + old_rev + "/main.md"
            out[md] = out[md].replace("定める。", "定めろ。")
        return edit(out) if edit else out

    sources = "      sources: [{source: src-fiction, locator: 本則}]\n"

    def other_sources(out):
        out["history.yaml"] = replace_nth(out["history.yaml"], sources, sources.replace("本則", "本則第一条"), 1)
        return out

    def other_notes(reason):
        return lambda out: with_glyph_notes(out, new_rev, ROW_NODE, 3, n=1, reason=reason)

    for title, before, after in (
            ("記録訂正で、宣言していない版の本文の出典（text.sources）を変える", typo(False), typo(True, other_sources)),
            ("記録訂正で、宣言していない版の字体注記を変える", typo(False, other_notes("適合ケースのための架空の注記")),
             typo(True, other_notes("適合ケースのための架空の注記（改めた）")))):
        bundle = next_dir("common", False) / "repo.bundle"
        c1, c2 = build_bundle(bundle, [
            ("二つの版を加える", "revisionAdd", False, before),
            (raw_message("第一の版の誤転記を直す", "correction", [old_rev]), RAW, False, after),
        ])
        add("common", title, ["CHG-02"], "change", {"kind": "change", "bundle": rel(bundle), "base": c1, "head": c2},
            {"results": [{"check": "change", "result": "fail"}], "diagnostics": [diag("CHG-02", SV["common"])]}, False)


def registry_metadata_changes():
    """CHG-02: metadata in the repository of the registry, after its first commit (no version to compare).

    Changing the label of a Record passes. Replacing the file of a merged Record with an active Record of the same
    ID reuses the retired ID (RID-05): the registry after the commit holds no retired Record, so only the change
    check finds it. The table of CHG-02 refers the check to RID-05, the requirement that forbids the reuse, so the
    violation is reported by RID-05 (CHG-03: by the requirement that defines the check).
    """
    relabeled = dict(REGISTRY_FIRST)
    path = "records/20990101-act-1.yaml"
    relabeled[path] = relabeled[path].replace("label: 架空法律第一号（実在しないサンプル）", "label: 架空雲保管法（実在しないサンプル）")
    assert relabeled[path] != REGISTRY_FIRST[path]
    bundle = next_dir("common", True) / "repo.bundle"
    c1, c2 = build_bundle(bundle, [("Recordを登録する", "metadata", False, dict(REGISTRY_FIRST)),
                                   ("Recordのラベルを改める", "metadata", False, relabeled)])
    add("common", "登録台帳のリポジトリで、Recordのラベルを改める属性の更新", ["CHG-02"], "change",
        {"kind": "change", "bundle": rel(bundle), "base": c1, "head": c2, "repository": "registry"},
        {"results": [{"check": "change", "result": "pass"}]}, True)

    reused = dict(REGISTRY_FIRST)
    reused["records/" + REGISTRY_RETIRED[0] + ".yaml"] = (
        "schemaVersion: loj-registry/v1alpha1\nid: " + REGISTRY_RETIRED[0] + "\nlabel: 架空の別の法令（実在しないサンプル）\n"
        "status: active\nidentity:\n  evidence: [{source: src-fiction, locator: 本文}]\n  verification: {state: confirmed}\n"
        "collection: {state: notCollected}\nsources:\n  - {id: src-fiction, kind: other, title: 架空の原典}\n"
        "numbers: []\nexternalIds: []\n")
    bundle = next_dir("common", False) / "repo.bundle"
    c1, c2 = build_bundle(bundle, [("Recordを登録し、重複した登録を統合する", "metadata", False, retired_registry_files()),
                                   ("統合したRecordのIDを別の法令のRecordに使う", "metadata", False, reused)])
    add("common", "登録台帳のリポジトリで、統合したRecordのIDを別の法令のRecordに再利用する属性の更新", ["CHG-02", "RID-05"], "change",
        {"kind": "change", "bundle": rel(bundle), "base": c1, "head": c2, "repository": "registry"},
        {"results": [{"check": "change", "result": "fail"}], "diagnostics": [diag("RID-05", SV["reg"])]}, False)


def revert_revision_add():
    """CHG-03: the revert of revisionAdd is revisionFix, which retracts the Revision and keeps its version package.

    The positive retracts the added Revision. The negative is the diff of git revert, declared revisionAdd (the kind
    of the change it reverts): it deletes the version package and the Revision, outside the range of revisionAdd.
    """
    old_rev, new_rev = ROW_REVS[0], ROW_REVS[1]
    one, two = row_files([["a1b2", "c3d4"]]), row_files([["a1b2", "c3d4"], ["a1b2"]])
    retracted = dict(two)
    retracted["history.yaml"] = replace_nth(two["history.yaml"], "    status: active\n", "    status: retracted\n", -1)
    first = [("制定時の版を加える", "revisionAdd", False, one),
             (raw_message("改正による版を加える", "revisionAdd", [new_rev]), RAW, False, two)]
    bundle = next_dir("common", True) / "repo.bundle"
    _, c2, c3 = build_bundle(bundle, first + [
        (raw_message("改正による版の追加を取り消す", "revisionFix", [new_rev]), RAW, False, retracted)])
    add("common", "状態の追加の取り消しを、Revisionを撤回する状態の訂正とする", ["CHG-03", "CHG-02"], "change",
        {"kind": "change", "bundle": rel(bundle), "base": c2, "head": c3},
        {"results": [{"check": "change", "result": "pass"}]}, True)
    reverted = dict(one)
    reverted.update({"versions/" + new_rev + "/law.yaml": None})
    bundle = next_dir("common", False) / "repo.bundle"
    _, c2, c3 = build_bundle(bundle, first + [
        (raw_message("Revert \"改正による版を加える\"", "revisionAdd", [new_rev]), RAW, False, reverted)])
    add("common", "状態の追加の取り消しを、版パッケージを削除する差分で状態の追加と宣言する", ["CHG-03", "CHG-02"], "change",
        {"kind": "change", "bundle": rel(bundle), "base": c2, "head": c3},
        {"results": [{"check": "change", "result": "fail"}], "diagnostics": [diag("CHG-02", SV["common"])]}, False)


# --- 2026-11-26: the result of a reference to a split Record (#183) -------------------------------
def split_reference_candidates():
    # XREF-01: the from of the old Record's relation is a split Record (the input of common-071). The reference is
    # not resolved; its result is candidates, listing replacedBy of the split Record, and it is undetermined.
    split = "conformance/common/v1alpha1/valid/common-071"
    add("common", "関係の起点が分割したRecordで、参照の結果が候補になる（架空）", ["XREF-01", "VAL-04", "VAL-06"], "L4",
        {"kind": "records", "registry": split + "/registry",
         "repositories": [split + "/" + OLD_LAW[0], TOTAL_POS + "/" + NEW_LAW[0]]},
        {"results": [{"check": "L4", "category": "relationResolution", "result": "incomplete"}],
         "diagnostics": [diag("XREF-01", SV["common"], "undetermined")],
         "references": [{"target": "loj:loj/" + SPLIT_ID[0], "result": "candidates",
                         "candidates": ["loj:loj/" + NEW_LAW[0], "loj:loj/" + SPLIT_OTHER[0]]}]},
        True, "relationResolution")


# --- 2026-11-26: the kind of the retraction of a relation (#184) ------------------------------------
def relation_retraction_changes():
    """HIST-12: retracting a relation and deleting (or replacing) the termination item that rests on it is one
    metadata change (CHG-01: the update of a relation), not revisionFix (the retraction of a Revision).

    The history manifest of hist-002 has no version package (text.status: absent), so no AST is compared.
    """
    base = (ROOT / "conformance/loj-history/v1alpha1/valid/hist-002/repo/history.yaml").read_bytes().decode("utf-8")
    active = "    verification: {state: unverified, reason: 官報と未照合}\n    status: active\n"
    retracted = ("    verification: {state: unverified, reason: 公布の日の法令を取り違えた関係の撤回（架空）}\n"
                 "    status: retracted\n")
    termination = "termination:\n  - {type: repealed, relation: rel-repeal}\n"
    assert base.count(active) == 1 and base.count(termination) == 1
    deleted = base.replace(active, retracted).replace(termination, "")
    other = ("  - id: rel-repeal-2\n    type: repeals\n    from: {id: 19590413-law-123, label: 架空の廃止法}\n"
             "    evidence: [{source: src-egov-s34-122, locator: 第三条}]\n"
             "    verification: {state: unverified, reason: 官報と未照合}\n    status: active\n    items:\n"
             "      - id: i1\n        scope: {text: 全部}\n        effective:\n          state: date\n"
             '          value: "1960-04-01"\n          raw: 昭和三十五年四月一日\n          precision: day\n'
             "          evidence: [{source: src-egov-s34-122, locator: 第一条}]\n"
             "          verification: {state: unverified, reason: 官報と未照合}\n"
             "        evidence: [{source: src-egov-s34-122, locator: 第三条}]\n"
             "        verification: {state: unverified, reason: 官報と未照合}\n")
    # The new relation follows the retracted one, and the termination item rests on it instead.
    replaced = base.replace(active, retracted).replace(
        termination, other + "termination:\n  - {type: repealed, relation: rel-repeal-2}\n")
    for title, head in [
        ("関係の撤回と、それを根拠とする効力の終了の項目の削除を、一つの属性の更新とする", deleted),
        ("関係の撤回と、効力の終了の項目の別の関係への置き換えを、一つの属性の更新とする", replaced),
    ]:
        bundle = next_dir("common", True) / "repo.bundle"
        c1, c2 = build_bundle(bundle, [("効力の終了を記録する", "revisionAdd", False, {"history.yaml": base}),
                                       ("関係を撤回する", "metadata", False, {"history.yaml": head})])
        add("common", title, ["HIST-12", "CHG-01", "CHG-02"], "change",
            {"kind": "change", "bundle": rel(bundle), "base": c1, "head": c2},
            {"results": [{"check": "change", "result": "pass"}]}, True)
    # The same change as common-094 declared revisionFix (the old reading of HIST-12), with the only Revision
    # declared: the relation and the termination are outside its range (the declared version and the record of the
    # retraction, merge or split of Revisions), so the commit fails by CHG-02.
    bundle = next_dir("common", False) / "repo.bundle"
    c1, c2 = build_bundle(bundle, [("効力の終了を記録する", "revisionAdd", False, {"history.yaml": base}),
                                   (raw_message("関係を撤回する", "revisionFix", ["2d6d257a"]), RAW, False,
                                    {"history.yaml": deleted})])
    add("common", "関係の撤回と効力の終了の項目の削除を、状態の訂正と宣言する", ["HIST-12", "CHG-01", "CHG-02"], "change",
        {"kind": "change", "bundle": rel(bundle), "base": c1, "head": c2},
        {"results": [{"check": "change", "result": "fail"}], "diagnostics": [diag("CHG-02", SV["common"])]}, False)


# --- 2026-11-26: the reuse of a retired revision_id in revisionFix (#189) ----------------------------
def revision_id_reuse():
    """CHG-02: a revisionFix that splits a Revision and gives one of the new Revisions the revision_id of a
    retracted Revision. The retracted Revision stays in the manifest (HIST-10), so two Revisions hold the id; the
    violation is reported by REV-01 (the table of CHG-02 names it). No Revision has a version package
    (text.status: absent), so no AST is compared and the version directories do not collide.
    """
    r0, r1, r2, r3 = "2d6d257a", "h3k8m2p5", "j4n9q3r6", "t5v2w8x1"
    fict = "{source: src-fiction, locator: %s}"

    def date(indent, value, raw, locator):
        pad = " " * indent
        return (pad + "effective:\n" + pad + "  state: date\n" + pad + '  value: "' + value + '"\n' + pad + "  raw: " + raw
                + "\n" + pad + "  precision: day\n" + pad + "  evidence: [" + fict % locator + "]\n" + pad
                + "  verification: {state: unverified, reason: 架空の資料}\n")

    def item(ident, value, raw):
        return ("      - id: " + ident + "\n        scope: {text: 第一条}\n" + date(8, value, raw, "附則")
                + "        evidence: [" + fict % "附則" + "]\n        verification: {state: unverified, reason: 架空の資料}\n")

    def relation(ident, law, items):
        return ("  - id: " + ident + "\n    type: amends\n    from: {id: " + law + ", label: 架空の改正法}\n"
                "    evidence: [" + fict % "本則" + "]\n    verification: {state: unverified, reason: 架空の資料}\n"
                "    status: active\n    items:\n" + items)

    def revision(ident, based, rel, items, value, raw, status="active", extra=""):
        return ("  - id: " + ident + "\n    basedOn: " + based + "\n    basis: [{relation: " + rel + ", items: [" + items + "]}]\n"
                + date(4, value, raw, "施行期日") + "    applicability: {state: unsurveyed}\n    text: {status: absent}\n"
                "    status: " + status + "\n" + extra)

    head = ("schemaVersion: loj-history/v1alpha1\nrecord: {id: 20990101-act-7, label: 架空雲測量法（実在しないサンプル）}\n"
            "sources:\n  - {id: src-fiction, kind: other, title: 適合ケースのための架空の資料}\nrelations:\n"
            + relation("rel-1", "20990201-act-11", item("i1", "2099-02-01", "二千九十九年二月一日"))
            + relation("rel-2", "20990301-act-12", item("i1", "2099-03-01", "二千九十九年三月一日")
                       + item("i2", "2099-04-01", "二千九十九年四月一日"))
            + "revisions:\n  - id: " + r0 + "\n    origin: coverageStart\n    effective: {state: unknown, reason: 未調査}\n"
            "    applicability: {state: unsurveyed}\n    text: {status: absent}\n    status: active\n")
    first = head + revision(r1, r0, "rel-1", "i1", "2099-02-01", "二千九十九年二月一日") + revision(
        r2, r0, "rel-2", "i1, i2", "2099-03-01", "二千九十九年三月一日")
    tail = "coverage: {state: unconfirmed}\n"
    retracted = head + revision(r1, r0, "rel-1", "i1", "2099-02-01", "二千九十九年二月一日", "retracted") + revision(
        r2, r0, "rel-2", "i1, i2", "2099-03-01", "二千九十九年三月一日")
    split = (head + revision(r1, r0, "rel-1", "i1", "2099-02-01", "二千九十九年二月一日", "retracted")
             + revision(r2, r0, "rel-2", "i1, i2", "2099-03-01", "二千九十九年三月一日", "split",
                        "    replacedBy:\n      revisions: [" + r3 + ", " + r1 + "]\n"
                        "      evidence: [" + fict % "附則" + "]\n"
                        "      verification: {state: unverified, reason: 施行期日の異なる二つの段階を一つの版にした誤りの訂正（架空）}\n")
             + revision(r3, r0, "rel-2", "i1", "2099-03-01", "二千九十九年三月一日")
             + revision(r1, r3, "rel-2", "i2", "2099-04-01", "二千九十九年四月一日"))
    bundle = next_dir("common", False) / "repo.bundle"
    _, c2, c3 = build_bundle(bundle, [
        ("制定後の二つの版を加える", "revisionAdd", False, {"history.yaml": first + tail}),
        (raw_message("取り違えた版を撤回する", "revisionFix", [r1]), RAW, False, {"history.yaml": retracted + tail}),
        (raw_message("一つにした二つの段階の版を分割する", "revisionFix", [r2, r3, r1]), RAW, False,
         {"history.yaml": split + tail})])
    add("common", "状態の訂正で、分割先のRevisionに撤回したRevisionのrevision_idを再利用する", ["CHG-02", "REV-01", "HIST-10"],
        "change", {"kind": "change", "bundle": rel(bundle), "base": c2, "head": c3},
        {"results": [{"check": "change", "result": "fail"}], "diagnostics": [diag("REV-01", SV["hist"])]}, False)


# --- 2026-11-26: a version without text declared by correction or restoration (CHG-02) ---------------------------
def absent_text(files):
    """The version recorded without text (HIST-08): no version package, and no sources or glyphCheck."""
    out = {k: v for k, v in files.items() if not k.startswith("versions/")}
    text = ("    text:\n      status: complete\n      sources: [{source: src-fiction, locator: 本則}]\n"
            "      glyphCheck: unverified\n")
    assert out["history.yaml"].count(text) == 1
    out["history.yaml"] = out["history.yaml"].replace(text, "    text: {status: absent}\n")
    return out


def with_readme(files):
    """Add a file outside the canonical data (CHG-01), which no kind's check covers, so the commit is not empty."""
    out = dict(files)
    out["README.md"] = "架空法律第一号の法令リポジトリである。\n"
    return out


def absent_version_declarations():
    """CHG-02: a version without text has no text.sources (HIST-08), so correction cannot show its basis.

    A correction that declares the version and changes only a file outside the canonical data fails the check of
    its basis. A correction that adds the version package and records the text as complete changes text.status,
    outside its range. Adding the text is restoration, which passes; a restoration that leaves the version without
    text does not update the state of the text.
    """
    body = "架空の雲を保管する。\n"
    absent = absent_text(fictional_files(body))
    for success, title, kind, after in (
            (False, "本文のない版を宣言し、正本のデータの外のファイルだけを変える記録訂正", "correction", with_readme(absent)),
            (False, "本文のない版を宣言し、版パッケージを加えて本文をそろえる記録訂正", "correction", fictional_files(body)),
            (True, "本文のない版に版パッケージを加えて本文をそろえる復元", "restoration", fictional_files(body)),
            (False, "本文のない版を宣言し、本文を補わずに正本のデータの外のファイルだけを変える復元", "restoration", with_readme(absent))):
        bundle = next_dir("common", success) / "repo.bundle"
        c1, c2 = build_bundle(bundle, [("本文のない版を加える", "revisionAdd", True, absent), (title, kind, True, after)])
        expected = {"results": [{"check": "change", "result": "pass" if success else "fail"}]}
        if not success:
            expected["diagnostics"] = [diag("CHG-02", SV["common"])]
        add("common", title, ["CHG-02", "HIST-08"], "change", {"kind": "change", "bundle": rel(bundle), "base": c1, "head": c2},
            expected, success)


# --- 2026-11-26: the clauses of XREF-05 and XREF-06 without a case (publication step 2) ------------
def cross_record_clauses():
    display = {"check": "L4", "category": "displayConsistency", "result": "pass"}
    warning = {"results": [display], "diagnostics": [diag("XREF-05", SV["common"], "warning")]}
    law = "records/19480720-law-178.yaml"
    exists_raw = "    state: exists\n    raw: 法律第百七十八号\n"
    period = '      period: {raw: 昭和二十三年, gregorian: {from: "1948-01-01", to: "1948-12-31"}}\n'
    ambiguous = ('      - {id: g1, offset: 7, recorded: "号", kind: ambiguous, candidates: ["号", "號"],\n'
                 "         basis: provisional, evidence: [{source: src-egov, locator: 法令番号}],\n"
                 "         verification: {state: confirmed, reason: 画像の最大解像度で字体を決められない}}\n")
    # XREF-05: an illegible claim is compared like exists; 昭和二十三年法律第百七十八号 matches neither
    # 法律第百七十〓号 nor 昭和二十三年法律第百七十〓号. The 〓 has its GLYPH-05 note (basis undetermined).
    illegible = ('      - {id: g1, offset: 6, recorded: "〓", kind: illegible, basis: undetermined,\n'
                 "         evidence: [{source: src-kanpo-19480720, locator: 1コマ 法律の冒頭}],\n"
                 "         verification: {state: unverified, reason: 適合ケースのための架空の判読不能}}\n")
    dest = next_dir("common", True) / "registry"
    mutate(dest, REG_POS, [(law, exists_raw, "    state: illegible\n    raw: 法律第百七十〓号\n"), (law, ambiguous, illegible)])
    add("common", "採用中の番号主張が判読不能で、版パッケージの番号と一致しない", ["XREF-05", "REG-03"], "L4",
        {"kind": "records", "registry": rel(dest), "repositories": [HIST_POS]}, warning, True, "displayConsistency")
    # XREF-05: law.number null against an exists claim is a mismatch.
    dest = next_dir("common", True) / "hist-001"
    mutate(dest, HIST_POS, [(ZWG + "law.yaml", '  number: "昭和二十三年法律第百七十八号"\n', "  number: null\n")])
    add("common", "版パッケージの番号がnullで、採用中の番号主張は番号がある", ["XREF-05", "MAN-01"], "L4",
        {"kind": "records", "registry": REG_POS, "repositories": [rel(dest)]}, warning, True, "displayConsistency")
    # XREF-05: without structured.period only raw is compared, so 昭和二十三年法律第百七十八号 (period + raw)
    # no longer matches.
    dest = next_dir("common", True) / "registry"
    mutate(dest, REG_POS, [(law, period, "")])
    add("common", "採用中の番号主張にstructured.periodがなく、版パッケージの番号がrawと一致しない", ["XREF-05", "REG-03"],
        "L4", {"kind": "records", "registry": rel(dest), "repositories": [HIST_POS]}, warning, True,
        "displayConsistency")

    time = {"check": "L4", "category": "timeConsistency", "result": "pass"}
    # XREF-06: only the Record of hist-016 is in the input; the other Record that has a relation from the same
    # amending law (20990402-law-3, notCollected) is not compared, and the check is not incomplete.
    add("common", "同じ改正法令からの関係を持つ、もう一方のRecordを収録していない（判定しない）", ["XREF-06", "REG-02"], "L4",
        {"kind": "records", "registry": PROM_POS + "/registry", "repositories": [POS_016]}, {"results": [time]}, True,
        "timeConsistency")
    # XREF-06: two relations of one history manifest from the same amending law, promulgated on different days.
    other = PROM_POS + "/hist-016b"
    second = ("  - id: rel-amend-x\n    type: amends\n    from: {id: 20990601-law-2, label: 架空の改正法}\n"
              '    promulgated:\n      state: date\n      value: "2099-06-02"\n      raw: 令和八十一年六月二日\n'
              "      precision: day\n      evidence: [{source: src-fictional, locator: 公布の日}]\n"
              "      verification: {state: unverified, reason: 架空の資料}\n"
              "    evidence: [{source: src-fictional, locator: 附則第二条}]\n"
              "    verification: {state: unverified, reason: 架空の資料}\n"
              "    status: active\n    items:\n      - id: i1\n        scope: {text: 第二条}\n"
              "        effective: {state: unknown, reason: 適合ケースで省略}\n"
              "        evidence: [{source: src-fictional, locator: 附則第二条}]\n"
              "        verification: {state: unverified, reason: 架空の資料}\n")
    dest = next_dir("common", True) / "hist-016b"
    mutate(dest, other, [("history.yaml", "revisions:\n", second + "revisions:\n")])
    add("common", "同じ履歴マニフェストの、同じ改正法令からの関係の公布の時点は比べない（架空）", ["XREF-06", "HIST-03"], "L4",
        {"kind": "records", "registry": PROM_POS + "/registry", "repositories": [rel(dest)]}, {"results": [time]}, True,
        "timeConsistency")


def main():
    for suite, folder in FOLDER.items():
        for group in ("invalid", "expected"):
            shutil.rmtree(C / folder / group, ignore_errors=True)
    shutil.rmtree(C / "common/v1alpha1/valid", ignore_errors=True)
    history()
    glyphs()
    registry()
    registry_names()
    rebuild()
    cross_record()
    changes_and_references()
    display_and_promulgation()
    total_revision()
    change_dependents()
    row_keys()
    termination_retraction()
    common_types()
    history_gaps()
    registry_ids()
    change_without_ast()
    termination_time()
    retired_ids_and_reviewed_format()
    registration_space()
    invalid_review_records()
    glyph_file_selection()
    conditional_fields()
    trailer_syntax()
    unknown_kind()
    official_correction_evidence()
    duplicate_trailers()
    merge_commit()
    correction_without_text_change()
    declared_versions_without_ast()
    amendment_glyph_notes()
    auxiliary_changes()
    illegible_other_source()
    file_modes()
    first_commits()
    registry_first_commits()
    legacy_boundary()
    spacing_line_breaks()
    staged_enactment()
    row_key_gaps()
    text_variances()
    glyph_note_gaps()
    cross_record_gaps()
    common_type_gaps()
    change_partial_text()
    change_dependent_files()
    registry_metadata_changes()
    revert_revision_add()
    split_reference_candidates()
    relation_retraction_changes()
    revision_id_reuse()
    absent_version_declarations()
    cross_record_clauses()
    assert not DERIVED, sorted(DERIVED)  # every copy is listed by the case that owns it
    marked = {case["id"] for suite, cases in INDEX.items() if suite != "reg2" for case in cases if "rejectedBy" in case}
    assert marked == SCHEMA_REJECTED, SCHEMA_REJECTED - marked
    marked = {case["id"] for case in INDEX["reg2"] if "rejectedBy" in case}
    assert marked == SCHEMA_REJECTED_REG2, SCHEMA_REJECTED_REG2 - marked
    for suite, folder in FOLDER.items():
        write_json(C / folder / "manifest.json", {"suite": SV[suite], "cases": INDEX[suite]})
    print("Authored " + ", ".join(f"{k}: {len(v)}" for k, v in INDEX.items()) + "; no validator invoked.")


if __name__ == "__main__":
    main()
