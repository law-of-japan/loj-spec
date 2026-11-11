"""Hand-authored loj/v1alpha2 cases for the structures new in v1alpha2.

Authoring helper (O-15). Not a parser: every expected tree below is written by
hand from the spec text. Run after port_v1alpha2_cases.py; it replaces cases
pkg-107 and later in conformance/v1alpha2/manifest.json. CI does not run it.
"""
import copy
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DST = ROOT / "conformance/v1alpha2"
LAW = {"id": "20990101-act-1", "title": "架空雲保管法（実在しないサンプル）", "type": "act",
       "number": "架空法律第一号", "promulgatedAt": "2099-01-01", "language": "ja"}
LID = LAW["id"]
FIRST = 107


def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data.encode("utf-8") if isinstance(data, str) else data)


def manifest(files, **extra):
    man = {"schemaVersion": "loj/v1alpha2", "law": LAW,
           "documents": [{"path": name, "parent": parent} for name, parent in files]}
    man.update(extra)
    return json.dumps(man, ensure_ascii=False, indent=2) + "\n"


def node(kind, ident, number=None, display="", content=None, **extra):
    value = {"kind": kind, "id": ident, "number": number, "display": display, "content": content or []}
    value.update(extra)
    return value


def text(value):
    return {"text": value}


def para(parent, number, body, display="", numbering="explicit", children=None):
    ident = parent + "/paragraph/" + number
    content = [text(body)] + (children(ident) if children else [])
    return node("Paragraph", ident, number, display, content, numbering=numbering)


def article(scope, number, display, paragraphs):
    ident = scope + "/article/" + number
    return node("Article", ident, number, display, [p(ident) for p in paragraphs], status="active")


def ast(main_children, lead=(), supplements=()):
    root = node("Law", LID, None, LAW["title"],
                list(lead) + [node("MainProvision", LID + "/main", None, "", main_children)] + list(supplements))
    return {"schemaVersion": "loj/v1alpha2", "law": LAW, "root": root}


CASES = []


def case(title, requirements, files, expected, success, check="L1", man_extra=None):
    ident = "pkg-%03d" % (FIRST + len(CASES))
    folder = DST / ("valid" if success else "invalid") / ident
    if folder.exists():
        shutil.rmtree(folder)
    names = [(name, parent) for name, parent, _ in files]
    write(folder / "law.yaml", manifest(names, **(man_extra or {})))
    for name, _, body in files:
        write(folder / name, body)
    exp_path = "conformance/v1alpha2/expected/" + ident + ".json"
    write(ROOT / exp_path, json.dumps(expected, ensure_ascii=False, indent=2) + "\n")
    CASES.append({"id": ident, "title": title, "requirements": requirements, "check": check, "normative": True,
                  "input": {"kind": "package", "path": (folder / "law.yaml").relative_to(ROOT).as_posix()},
                  "expected": exp_path, "success": success})


def fail(*rules):
    return {"diagnostics": [{"rule": r, "schemaVersion": "loj/v1alpha2", "class": "error"} for r in rules]}


MAIN = LID + "/main"
BODY = "架空の雲を保管する。\n"

# --- positive ---------------------------------------------------------------
case("旧字体の条ラベルと「ノ」の枝番号", ["HEAD-01", "NUM-01", "ID-01"],
     [("main.md", "main", "# 第一條\n<!-- loj:paragraph number=1 -->\n" + BODY + "<!-- loj:end-paragraph -->\n"
       "# 第一條ノ二\n<!-- loj:paragraph number=1 -->\n" + BODY + "<!-- loj:end-paragraph -->\n")],
     {"ast": ast([article(MAIN, "1", "第一條", [lambda a: para(a, "1", BODY)]),
                  article(MAIN, "1-2", "第一條ノ二", [lambda a: para(a, "1", BODY)])])}, True)

SUPP = LID + "/supplement/original"
case("附則の見出しの字間", ["HEAD-03", "MD-04", "AST-01"],
     [("main.md", "main", "# 第一条\n<!-- loj:paragraph number=1 -->\n" + BODY + "<!-- loj:end-paragraph -->\n"),
      ("supp.md", "supplement/original", "# 附　則\n<!-- loj:paragraph number=1 -->\nこの法律は、公布の日から施行する。\n"
       "<!-- loj:end-paragraph -->\n")],
     {"ast": ast([article(MAIN, "1", "第一条", [lambda a: para(a, "1", BODY)])],
                 supplements=[node("SupplementaryProvision", SUPP, None, "附　則",
                                   [para(SUPP, "1", "この法律は、公布の日から施行する。\n")])])}, True,
     man_extra={"supplements": [{"key": "original", "title": "制定附則"}]})

case("無番号の項", ["PARA-01", "DISP-01", "ID-01"],
     [("main.md", "main", "# 第一条\n<!-- loj:paragraph number=1 numbering=implicit -->\n" + BODY +
       "<!-- loj:end-paragraph -->\n<!-- loj:paragraph number=2 numbering=implicit -->\n2099年までに返す。\n"
       "<!-- loj:end-paragraph -->\n")],
     {"ast": ast([article(MAIN, "1", "第一条", [lambda a: para(a, "1", BODY, numbering="implicit"),
                                                lambda a: para(a, "2", "2099年までに返す。\n", numbering="implicit")])])},
     True)


def table_children(p):
    t = p + "/table/1"
    r1, r2 = t + "/row/k3v9", t + "/row/b6gr"
    return [node("Table", t, "1", "", [
        node("Row", r1, None, "", [node("Cell", r1 + "/cell/1", "1", "", [text("白雲\n")]),
                                   node("Cell", r1 + "/cell/2", "2", "", [text("一号倉庫\n")])], key="k3v9"),
        node("Row", r2, None, "", [node("Cell", r2 + "/cell/1", "1", "", [text("雨雲\n")], colspan=2)], key="b6gr")]),
        text("前項の表は、保管の場所を定める。\n")]


TABLE_MD = ("# 第一条\n<!-- loj:paragraph number=1 -->\n雲の保管の場所は、次の表のとおりとする。\n"
            "<!-- loj:table number=1 -->\n<!-- loj:row key=k3v9 -->\n<!-- loj:cell -->\n白雲\n<!-- loj:end-cell -->\n"
            "<!-- loj:cell -->\n一号倉庫\n<!-- loj:end-cell -->\n<!-- loj:end-row -->\n<!-- loj:row key=b6gr -->\n"
            "<!-- loj:cell colspan=2 -->\n雨雲\n<!-- loj:end-cell -->\n<!-- loj:end-row -->\n<!-- loj:end-table -->\n"
            "前項の表は、保管の場所を定める。\n<!-- loj:end-paragraph -->\n")
case("項の本文の中の表", ["TABLE-01", "TABLE-02", "TABLE-03", "ID-01", "AST-01"],
     [("main.md", "main", TABLE_MD)],
     {"ast": ast([article(MAIN, "1", "第一条",
                          [lambda a: para(a, "1", "雲の保管の場所は、次の表のとおりとする。\n", children=table_children)])])},
     True)

case("制定文と前文", ["PRE-01", "PRE-02", "ID-01", "AST-01"],
     [("main.md", "main", "<!-- loj:enact-statement -->\n内閣は、架空の法律に基づき、この政令を制定する。\n"
       "<!-- loj:end-enact-statement -->\n<!-- loj:preamble -->\n雲は、すべての者の共有である。\n\nここに、この法律を制定する。\n"
       "<!-- loj:end-preamble -->\n# 第一条\n<!-- loj:paragraph number=1 -->\n" + BODY + "<!-- loj:end-paragraph -->\n")],
     {"ast": ast([article(MAIN, "1", "第一条", [lambda a: para(a, "1", BODY)])],
                 lead=[node("EnactStatement", LID + "/enact-statement", None, "",
                            [text("内閣は、架空の法律に基づき、この政令を制定する。\n")]),
                       node("Preamble", LID + "/preamble", None, "",
                            [text("雲は、すべての者の共有である。\n\nここに、この法律を制定する。\n")])])}, True)

# --- negative (L1 definitions; executed by a validator, not by verify.py) ---
ART = "# 第一条\n"
P1 = "<!-- loj:paragraph number=1 -->\n" + BODY + "<!-- loj:end-paragraph -->\n"
case("無番号の項と番号のある項の混在", ["PARA-01"],
     [("main.md", "main", ART + "<!-- loj:paragraph number=1 numbering=implicit -->\n" + BODY + "<!-- loj:end-paragraph -->\n"
       "<!-- loj:paragraph number=2 -->\n２　2099年までに返す。\n<!-- loj:end-paragraph -->\n")], fail("PARA-01"), False)
case("項が一つの親での無番号の項", ["PARA-01"],
     [("main.md", "main", ART + "<!-- loj:paragraph number=1 numbering=implicit -->\n" + BODY + "<!-- loj:end-paragraph -->\n")],
     fail("PARA-01"), False)
case("項の本文の中のGFMの表", ["TABLE-01", "MD-02"],
     [("main.md", "main", ART + "<!-- loj:paragraph number=1 -->\n次の表のとおりとする。\n\n| 雲 | 倉庫 |\n|---|---|\n| 白雲 | 一号 |\n"
       "<!-- loj:end-paragraph -->\n")], fail("TABLE-01"), False)
case("行のkeyの重複", ["TABLE-02", "ID-02"],
     [("main.md", "main", TABLE_MD.replace("row key=b6gr", "row key=k3v9"))], fail("TABLE-02"), False)
case("行のkeyの形式（大文字）", ["TABLE-02", "DIR-01"],
     [("main.md", "main", TABLE_MD.replace("row key=b6gr", "row key=B6GR"))], fail("TABLE-02"), False)
case("セルの結合に値1を書く", ["TABLE-03"],
     [("main.md", "main", TABLE_MD.replace("cell colspan=2", "cell colspan=1"))], fail("TABLE-03"), False)
case("セルの中の項", ["TABLE-03", "DIR-02"],
     [("main.md", "main", TABLE_MD.replace("<!-- loj:cell -->\n白雲\n<!-- loj:end-cell -->",
                                           "<!-- loj:cell -->\n白雲\n<!-- loj:item number=1 -->\n一　雲\n<!-- loj:end-item -->\n"
                                           "<!-- loj:end-cell -->"))], fail("TABLE-03"), False)
case("表の直下の本文", ["DIR-02", "TABLE-01"],
     [("main.md", "main", TABLE_MD.replace("<!-- loj:table number=1 -->\n", "<!-- loj:table number=1 -->\n表の説明\n"))],
     fail("DIR-02"), False)
case("見出しの後の前文", ["PRE-01"],
     [("main.md", "main", ART + P1 + "<!-- loj:preamble -->\n雲は、すべての者の共有である。\n<!-- loj:end-preamble -->\n")],
     fail("PRE-01"), False)
case("前文の後の制定文", ["PRE-02"],
     [("main.md", "main", "<!-- loj:preamble -->\n雲は、すべての者の共有である。\n<!-- loj:end-preamble -->\n"
       "<!-- loj:enact-statement -->\n内閣は、この政令を制定する。\n<!-- loj:end-enact-statement -->\n" + ART + P1)],
     fail("PRE-02"), False)
case("表にない字体の条ラベル", ["HEAD-01"],
     [("main.md", "main", "# 第一絛\n" + P1)], fail("HEAD-01"), False)
case("附則の見出しの半角空白", ["HEAD-03"],
     [("main.md", "main", ART + P1),
      ("supp.md", "supplement/original", "# 附 則\n<!-- loj:paragraph number=1 -->\nこの法律は、公布の日から施行する。\n"
       "<!-- loj:end-paragraph -->\n")], fail("HEAD-03"), False,
     man_extra={"supplements": [{"key": "original", "title": "制定附則"}]})
case("v1alpha1のschemaVersion", ["BASIC-01"], [("main.md", "main", ART + P1)], fail("BASIC-01"), False, check="L0",
     man_extra={"schemaVersion": "loj/v1alpha1"})
# 2026-11-11 (#25): spaces in markers, character kinds of display numbers.
case("マーカーの属性の間の二つの空白", ["DIR-01"],
     [("main.md", "main", ART + "<!-- loj:paragraph number=1  numbering=explicit -->\n" + BODY + "<!-- loj:end-paragraph -->\n")],
     fail("DIR-01"), False)
case("属性のないセルのマーカーの二つの空白", ["DIR-01", "TABLE-03"],
     [("main.md", "main", TABLE_MD.replace("<!-- loj:cell -->\n白雲", "<!-- loj:cell  -->\n白雲"))], fail("DIR-01"), False)
case("号の表示番号に全角の十進", ["DISP-01"],
     [("main.md", "main", ART + "<!-- loj:paragraph number=1 -->\n" + BODY + "<!-- loj:item number=1 -->\n１　白雲\n"
       "<!-- loj:end-item -->\n<!-- loj:end-paragraph -->\n")], fail("DISP-01"), False)
case("条の番号の成分の間の字種の混在", ["NUM-01", "HEAD-01"], [("main.md", "main", "# 第十二条の２\n" + P1)], fail("NUM-01"), False)


def main():
    index_path = DST / "manifest.json"
    index = json.loads(index_path.read_text(encoding="utf-8"))
    kept = [c for c in index["cases"] if int(c["id"][4:]) < FIRST]
    index["cases"] = kept + CASES
    write(index_path, json.dumps(index, ensure_ascii=False, indent=2) + "\n")
    print(f"Authored {len(CASES)} v1alpha2 cases by hand; no parser invoked.")


if __name__ == "__main__":
    main()
