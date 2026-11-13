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


def para(parent, number, body, display="", numbering="explicit", children=None, caption=None):
    ident = parent + "/paragraph/" + number
    content = [text(body)] + (children(ident) if children else [])
    extra = {"caption": caption} if caption is not None else {}
    return node("Paragraph", ident, number, display, content, numbering=numbering, **extra)


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
# An unknown schemaVersion is unprocessable: L0 is incomplete, with BASIC-01 as the reason (VAL-04).
case("v1alpha1のschemaVersion", ["BASIC-01", "VAL-04"], [("main.md", "main", ART + P1)],
     {"results": [{"check": "L0", "result": "incomplete"}], **fail("BASIC-01")}, False, check="L0",
     man_extra={"schemaVersion": "loj/v1alpha1"})
# 2026-11-11 (#25): spaces in markers, character kinds of display numbers.
case("マーカーの属性の間の二つの空白", ["DIR-01"],
     [("main.md", "main", ART + "<!-- loj:paragraph number=1  numbering=explicit -->\n" + BODY + "<!-- loj:end-paragraph -->\n")],
     fail("DIR-01"), False)
case("属性のないセルのマーカーの二つの空白", ["DIR-01"],
     [("main.md", "main", TABLE_MD.replace("<!-- loj:cell -->\n白雲", "<!-- loj:cell  -->\n白雲"))], fail("DIR-01"), False)
case("号の表示番号に全角の十進", ["DISP-01"],
     [("main.md", "main", ART + "<!-- loj:paragraph number=1 -->\n" + BODY + "<!-- loj:item number=1 -->\n１　白雲\n"
       "<!-- loj:end-item -->\n<!-- loj:end-paragraph -->\n")], fail("DISP-01"), False)
case("条の番号の成分の間の字種の混在", ["NUM-01", "HEAD-01"], [("main.md", "main", "# 第十二条の２\n" + P1)], fail("NUM-01"), False)

# 2026-11-12 (#27): table of contents, iroha / parenthesized subitem displays, parentheses in article captions.
ENACT_MD = "<!-- loj:enact-statement -->\n内閣は、架空の法律に基づき、この政令を制定する。\n<!-- loj:end-enact-statement -->\n"
TOC_BODY = "目次\n第一章　総則（第一条）\n附則\n"
TOC_MD = "<!-- loj:toc -->\n" + TOC_BODY + "<!-- loj:end-toc -->\n"
PREAMBLE_MD = "<!-- loj:preamble -->\n雲は、すべての者の共有である。\n<!-- loj:end-preamble -->\n"
CHAPTER = MAIN + "/chapter/1"
case("目次（制定文と前文の間）", ["TOC-01", "PRE-01", "PRE-02", "ID-01", "AST-01"],
     [("main.md", "main", ENACT_MD + TOC_MD + PREAMBLE_MD + "# 第一章　総則\n## 第一条\n" + P1)],
     {"ast": ast([node("Chapter", CHAPTER, "1", "第一章　総則",
                       [node("Article", MAIN + "/article/1", "1", "第一条", [para(MAIN + "/article/1", "1", BODY)],
                             status="active")])],
                 lead=[node("EnactStatement", LID + "/enact-statement", None, "",
                            [text("内閣は、架空の法律に基づき、この政令を制定する。\n")]),
                       node("Toc", LID + "/toc", None, "", [text(TOC_BODY)]),
                       node("Preamble", LID + "/preamble", None, "", [text("雲は、すべての者の共有である。\n")])])}, True)

A1 = MAIN + "/article/1"
P1ID = A1 + "/paragraph/1"
I1 = P1ID + "/item/1"
S1, S2 = I1 + "/subitem/1/1", I1 + "/subitem/1/2"
SUBITEM_MD = ("<!-- loj:paragraph number=1 -->\n雲の種類は、次のとおりとする。\n<!-- loj:item number=1 -->\n一　白雲\n"
              "<!-- loj:subitem level=1 number=1 -->\nイ　巻雲\n<!-- loj:end-subitem -->\n"
              "<!-- loj:subitem level=1 number=2 -->\nロ　積雲\n"
              "<!-- loj:subitem level=2 number=1 -->\n（１）　小さな積雲\n<!-- loj:end-subitem -->\n"
              "<!-- loj:subitem level=2 number=2 -->\n（２）　大きな積雲\n<!-- loj:end-subitem -->\n"
              "<!-- loj:end-subitem -->\n<!-- loj:end-item -->\n<!-- loj:end-paragraph -->\n")
case("いろはと括弧付きの十進の細分の表示", ["DISP-01", "ID-01"],
     [("main.md", "main", ART + SUBITEM_MD)],
     {"ast": ast([node("Article", A1, "1", "第一条", [node("Paragraph", P1ID, "1", "", [
         text("雲の種類は、次のとおりとする。\n"),
         node("Item", I1, "1", "一", [
             text("一　白雲\n"),
             node("Subitem", S1, "1", "イ", [text("イ　巻雲\n")], level=1),
             node("Subitem", S2, "2", "ロ", [
                 text("ロ　積雲\n"),
                 node("Subitem", S2 + "/subitem/2/1", "1", "（１）", [text("（１）　小さな積雲\n")], level=2),
                 node("Subitem", S2 + "/subitem/2/2", "2", "（２）", [text("（２）　大きな積雲\n")], level=2)], level=1)])],
         numbering="explicit")], status="active")])}, True)

case("括弧書きを含む条の見出し", ["HEAD-01", "AST-01"],
     [("main.md", "main", "# 第一条（雲（白雲を除く。）の保管）\n" + P1)],
     {"ast": ast([article(MAIN, "1", "第一条（雲（白雲を除く。）の保管）", [lambda a: para(a, "1", BODY)])])}, True)

case("目次の後の制定文", ["TOC-01"], [("main.md", "main", TOC_MD + ENACT_MD + ART + P1)], fail("TOC-01"), False)
case("前文の後の目次", ["TOC-01"], [("main.md", "main", PREAMBLE_MD + TOC_MD + ART + P1)], fail("TOC-01"), False)
case("附則の中の目次", ["TOC-01"],
     [("main.md", "main", ART + P1),
      ("supp.md", "supplement/original", "# 附則\n" + TOC_MD + "<!-- loj:paragraph number=1 -->\nこの法律は、公布の日から施行する。\n"
       "<!-- loj:end-paragraph -->\n")], fail("TOC-01"), False,
     man_extra={"supplements": [{"key": "original", "title": "制定附則"}]})
case("目次の中の項", ["TOC-01", "DIR-02"],
     [("main.md", "main", "<!-- loj:toc -->\n目次\n" + P1 + "<!-- loj:end-toc -->\n" + ART + P1)], fail("DIR-02"), False)
case("細分の兄弟の表示番号の字種の混在", ["DISP-01"],
     [("main.md", "main", ART + SUBITEM_MD.replace("（１）　小さな", "イ　小さな"))], fail("DISP-01"), False)
case("いろはの表示番号と番号の不一致", ["DISP-01"],
     [("main.md", "main", ART + SUBITEM_MD.replace("ロ　積雲", "ハ　積雲"))], fail("DISP-01"), False)
case("細分の表示番号にASCIIの括弧", ["DISP-01"],
     [("main.md", "main", ART + SUBITEM_MD.replace("（１）　小さな", "(1)　小さな").replace("（２）　大きな", "(2)　大きな"))],
     fail("DISP-01"), False)
case("号の表示番号にいろは", ["DISP-01"],
     [("main.md", "main", ART + "<!-- loj:paragraph number=1 -->\n" + BODY + "<!-- loj:item number=1 -->\nイ　白雲\n"
       "<!-- loj:end-item -->\n<!-- loj:end-paragraph -->\n")], fail("DISP-01"), False)
case("条の見出しの対応しない括弧", ["HEAD-01"], [("main.md", "main", "# 第一条（雲（白雲の保管）\n" + P1)], fail("HEAD-01"), False)
case("条の見出しの後に続く括弧", ["HEAD-01"], [("main.md", "main", "# 第一条（定義）（略）\n" + P1)], fail("HEAD-01"), False)
# Review of #54: iroha values around ヰ・ヱ with gaps, parenthesized ASCII decimal, a second table of contents.
IROHA_CASE = [("24", "ウ"), ("26", "ノ"), ("43", "ヱ"), ("47", "ス")]
case("ヰを使わないいろはの欠番と、括弧付きのASCIIの十進", ["DISP-01", "HEAD-02"],
     [("main.md", "main", ART + "<!-- loj:paragraph number=1 -->\n" + BODY + "<!-- loj:item number=1 -->\n一　白雲\n" +
       "".join("<!-- loj:subitem level=1 number=%s -->\n%s　雲\n<!-- loj:end-subitem -->\n" % (n, d) for n, d in IROHA_CASE[:-1]) +
       "<!-- loj:subitem level=1 number=47 -->\nス　雲\n<!-- loj:subitem level=2 number=12 -->\n（12）　小さな雲\n"
       "<!-- loj:end-subitem -->\n<!-- loj:end-subitem -->\n<!-- loj:end-item -->\n<!-- loj:end-paragraph -->\n")],
     {"ast": ast([node("Article", A1, "1", "第一条", [node("Paragraph", P1ID, "1", "", [
         text(BODY),
         node("Item", I1, "1", "一", [text("一　白雲\n")] + [
             node("Subitem", I1 + "/subitem/1/" + n, n, d, [text(d + "　雲\n")], level=1) for n, d in IROHA_CASE[:-1]] + [
             node("Subitem", I1 + "/subitem/1/47", "47", "ス", [
                 text("ス　雲\n"),
                 node("Subitem", I1 + "/subitem/1/47/subitem/2/12", "12", "（12）", [text("（12）　小さな雲\n")], level=2)],
                  level=1)])], numbering="explicit")], status="active")])}, True)
case("二つの目次", ["TOC-01"], [("main.md", "main", TOC_MD + TOC_MD + ART + P1)], fail("TOC-01"), False)

# 2026-11-12 (#1): L0 positives (no AST; CONF-01) and diagnostics with fixed locations (SRC-01).
L0_PASS = {"results": [{"check": "L0", "result": "pass"}]}
case("L0: 未対応の構造を申告した版パッケージ", ["BASIC-03", "VAL-01", "CONF-01"],
     [("main.md", "main", ART + "<!-- loj:paragraph number=1 -->\n雲の種類は、次のとおりとする。\n<!-- loj:item number=1 -->\n"
       "一　白雲\n<!-- loj:subitem level=1 number=1 -->\n（ｉ）　巻雲\n<!-- loj:end-subitem -->\n<!-- loj:end-item -->\n"
       "<!-- loj:end-paragraph -->\n")],
     L0_PASS, True, check="L0", man_extra={"unsupportedFeatures": ["ローマ数字の細分の表示"]})
case("L0: L1の違反（項の未閉鎖、DIR-02）を含む本文", ["VAL-02", "CONF-01"],
     [("main.md", "main", ART + "<!-- loj:paragraph number=1 -->\n" + BODY)], L0_PASS, True, check="L0")


def fail_at(rule, path, start, end):
    """One expected diagnostic with its location. The offsets are counted by hand (UTF-8 bytes, [start, end))."""
    return {"diagnostics": [{"rule": rule, "schemaVersion": "loj/v1alpha2", "class": "error",
                             "location": {"path": path, "start": start, "end": end}}]}


# CRLF; the body line is ３(3) 　(3) 本(3) 文(3) U+1F600(4) 。(3) CRLF(2) = 21 bytes after 13+33+32+28+33 = 139.
CRLF_P1 = "<!-- loj:paragraph number=1 -->\r\n架空の雲を保管する。\r\n<!-- loj:end-paragraph -->\r\n"
case("表示の不一致の位置（CRLFと4バイトの文字）", ["DISP-01", "SRC-01"],
     [("main.md", "main", "# 第一条\r\n" + CRLF_P1 + "<!-- loj:paragraph number=2 -->\r\n３　本文" + chr(0x1F600) + "。\r\n"
       "<!-- loj:end-paragraph -->\r\n")], fail_at("DISP-01", "main.md", 139, 160), False)
# LF; the unclosed start marker (32 bytes) follows 12+32+31+27 = 102 bytes.
case("未閉鎖の位置（開始のマーカーの行）", ["DIR-02", "SRC-01"],
     [("main.md", "main", ART + P1 + "<!-- loj:paragraph number=2 -->\n２　雲を返す。\n")],
     fail_at("DIR-02", "main.md", 102, 134), False)
# LF; the extra end marker (22 bytes) follows 12+32+26+27 = 97 bytes (雲(3) U+1F600(4) を保管する。(18) LF(1) = 26).
case("対応しない終了の位置（4バイトの文字の後）", ["DIR-02", "SRC-01"],
     [("main.md", "main", ART + "<!-- loj:paragraph number=1 -->\n雲" + chr(0x1F600) + "を保管する。\n"
       "<!-- loj:end-paragraph -->\n<!-- loj:end-item -->\n")],
     fail_at("DIR-02", "main.md", 97, 119), False)
# LF; the marker with an unknown attribute (白 is 3 bytes; 42 bytes with LF) follows 102 bytes.
case("属性の不正の位置", ["DIR-01", "SRC-01"],
     [("main.md", "main", ART + P1 + "<!-- loj:paragraph number=2 color=白 -->\n２　雲を返す。\n<!-- loj:end-paragraph -->\n")],
     fail_at("DIR-01", "main.md", 102, 144), False)
# LF; the extra end marker is the last line without a line break (21 bytes, to the end of the file) after 102 bytes.
case("対応しない終了の位置（改行のない最後の行）", ["DIR-02", "SRC-01"],
     [("main.md", "main", ART + P1 + "<!-- loj:end-item -->")], fail_at("DIR-02", "main.md", 102, 123), False)

# 2026-11-12 (#57): a column that continues into the next row is a merged cell (TABLE-03), not an empty one.
READ_LEAD = "雲の保管の規定の適用については、次の表の上欄に掲げる規定中同表の中欄に掲げる字句は、それぞれ同表の下欄に掲げる字句とする。\n"
ROWSPAN_MD = (ART + "<!-- loj:paragraph number=1 -->\n" + READ_LEAD +
              "<!-- loj:table number=1 -->\n<!-- loj:row key=m4qa -->\n<!-- loj:cell rowspan=2 -->\n第二条第一項\n<!-- loj:end-cell -->\n"
              "<!-- loj:cell -->\n白雲\n<!-- loj:end-cell -->\n<!-- loj:cell -->\n白雲（巻雲を含む。）\n<!-- loj:end-cell -->\n"
              "<!-- loj:end-row -->\n<!-- loj:row key=7tzd -->\n<!-- loj:cell -->\n倉庫\n<!-- loj:end-cell -->\n"
              "<!-- loj:cell -->\n倉庫（国内にあるものに限る。）\n<!-- loj:end-cell -->\n<!-- loj:end-row -->\n"
              "<!-- loj:end-table -->\n<!-- loj:end-paragraph -->\n")


def rowspan_children(p):
    t = p + "/table/1"
    r1, r2 = t + "/row/m4qa", t + "/row/7tzd"
    return [node("Table", t, "1", "", [
        node("Row", r1, None, "", [node("Cell", r1 + "/cell/1", "1", "", [text("第二条第一項\n")], rowspan=2),
                                   node("Cell", r1 + "/cell/2", "2", "", [text("白雲\n")]),
                                   node("Cell", r1 + "/cell/3", "3", "", [text("白雲（巻雲を含む。）\n")])], key="m4qa"),
        node("Row", r2, None, "", [node("Cell", r2 + "/cell/1", "1", "", [text("倉庫\n")]),
                                   node("Cell", r2 + "/cell/2", "2", "", [text("倉庫（国内にあるものに限る。）\n")])],
             key="7tzd")])]


case("上の欄が続く読替えの表（rowspan）", ["TABLE-03", "ID-01", "AST-01"],
     [("main.md", "main", ROWSPAN_MD)],
     {"ast": ast([article(MAIN, "1", "第一条", [lambda a: para(a, "1", READ_LEAD, children=rowspan_children)])])}, True)
case("空のセル（L1の診断はDIR-02だけ。続く欄の結合はL3）", ["DIR-02", "TABLE-03"],
     # The continued column is written as an empty cell instead of rowspan=2 on the cell above.
     [("main.md", "main", ROWSPAN_MD.replace("<!-- loj:cell rowspan=2 -->", "<!-- loj:cell -->")
       .replace("<!-- loj:row key=7tzd -->\n", "<!-- loj:row key=7tzd -->\n<!-- loj:cell -->\n\n<!-- loj:end-cell -->\n"))],
     fail("DIR-02"), False)


# 2026-11-13 (#50): the pair of pkg-074 (no declaration; DISP-01 only) and pkg-144 (declared; L0 pass).
ROMAN_MD = (ART + "<!-- loj:paragraph number=1 -->\n雲の種類は、次のとおりとする。\n<!-- loj:item number=1 -->\n"
            "一　白雲\n<!-- loj:subitem level=1 number=1 -->\n（ｉ）　巻雲\n<!-- loj:end-subitem -->\n<!-- loj:end-item -->\n"
            "<!-- loj:end-paragraph -->\n")
case("申告したローマ数字の細分の表示（L1の診断はBASIC-03だけ）", ["BASIC-03", "DISP-01"],
     [("main.md", "main", ROMAN_MD)], fail("BASIC-03"), False,
     man_extra={"unsupportedFeatures": ["ローマ数字の細分の表示"]})
case("L0: 空のunsupportedFeatures", ["MAN-01", "BASIC-03"],
     [("main.md", "main", ART + P1)], fail("MAN-01"), False, check="L0", man_extra={"unsupportedFeatures": []})


# 2026-11-13 (#56): paragraph captions (PARA-02). The caption line stays in the text; caption copies it.
ORIGINAL = {"supplements": [{"key": "original", "title": "制定附則"}]}
SUPP_HEAD = "# 附　則\n"
CAP1 = "（施行期日）\n１　この法律は、公布の日から施行する。\n"
CAP2 = "（経過措置）\n２　この法律の施行前に保管した雲については、なお従前の例による。\n"
CAPTION_SUPP = (SUPP_HEAD + "<!-- loj:paragraph number=1 caption=present -->\n" + CAP1 + "<!-- loj:end-paragraph -->\n"
                "<!-- loj:paragraph number=2 caption=present -->\n" + CAP2 + "<!-- loj:end-paragraph -->\n")
MAIN_A1 = [("main.md", "main", ART + P1)]
MAIN_A1_AST = [article(MAIN, "1", "第一条", [lambda a: para(a, "1", BODY)])]


def supp_case(title, requirements, body, expected, success):
    case(title, requirements, MAIN_A1 + [("supp.md", "supplement/original", body)], expected, success, man_extra=ORIGINAL)


supp_case("附則の項の見出し", ["PARA-02", "DISP-01", "DIR-01", "AST-01"], CAPTION_SUPP,
          {"ast": ast(MAIN_A1_AST, supplements=[node("SupplementaryProvision", SUPP, None, "附　則", [
              para(SUPP, "1", CAP1, display="１", caption="（施行期日）"),
              para(SUPP, "2", CAP2, display="２", caption="（経過措置）")])])}, True)
CAP_ART_P1 = "（保管の義務）\n架空の雲を保管する。\n"
case("条の項の見出し（表示番号を省略した第1項と号、見出しのない第2項）", ["PARA-02", "DISP-01", "HEAD-01", "AST-01"],
     [("main.md", "main", "# 第一条（雲の保管）\n<!-- loj:paragraph number=1 caption=present -->\n" + CAP_ART_P1 +
       "<!-- loj:item number=1 -->\n一　白雲\n<!-- loj:end-item -->\n<!-- loj:end-paragraph -->\n"
       "<!-- loj:paragraph number=2 -->\n２　2099年までに返す。\n<!-- loj:end-paragraph -->\n")],
     {"ast": ast([article(MAIN, "1", "第一条（雲の保管）", [
         lambda a: para(a, "1", CAP_ART_P1, caption="（保管の義務）",
                        children=lambda p: [node("Item", p + "/item/1", "1", "一", [text("一　白雲\n")])]),
         lambda a: para(a, "2", "２　2099年までに返す。\n", display="２")])])}, True)
IMP1 = "（経過措置）\n架空雲保管令は、廃止する。\n"
IMP2 = "架空雲保管令の規定による保管は、この法律の規定による保管とみなす。\n"
# One caption over two paragraphs is written on the first only (PARA-02); attributes in another order (DIR-01).
supp_case("無番号の項の見出し（続く項にかかる見出し）", ["PARA-02", "PARA-01", "DIR-01", "AST-01"],
          SUPP_HEAD + "<!-- loj:paragraph caption=present numbering=implicit number=1 -->\n" + IMP1 +
          "<!-- loj:end-paragraph -->\n<!-- loj:paragraph number=2 numbering=implicit -->\n" + IMP2 + "<!-- loj:end-paragraph -->\n",
          {"ast": ast(MAIN_A1_AST, supplements=[node("SupplementaryProvision", SUPP, None, "附　則", [
              para(SUPP, "1", IMP1, numbering="implicit", caption="（経過措置）"),
              para(SUPP, "2", IMP2, numbering="implicit")])])}, True)

# LF; supp.md starts with 附　則 (12 bytes) and the start marker (48 bytes), so the line checked as the caption line
# starts at 60: １　この法律は、公布の日から施行する。 is 19 x 3 + LF = 58 bytes.
supp_case("見出しの行のない項にcaption=present", ["PARA-02", "SRC-01"],
          CAPTION_SUPP.replace("（施行期日）\n", ""), fail_at("PARA-02", "supp.md", 60, 118), False)
# （施行期日）この法律は、公布の日から施行する。 is 23 x 3 + LF = 70 bytes.
supp_case("見出しの行の後に続く本文", ["PARA-02", "SRC-01"],
          CAPTION_SUPP.replace("（施行期日）\n１　", "（施行期日）"), fail_at("PARA-02", "supp.md", 60, 130), False)
# （施行期日） plus an ASCII space is 6 x 3 + 1 + LF = 20 bytes.
supp_case("見出しの行の末尾の空白", ["PARA-02", "SRC-01"],
          CAPTION_SUPP.replace("（施行期日）\n", "（施行期日） \n"), fail_at("PARA-02", "supp.md", 60, 80), False)
supp_case("属性のない第2項の見出しの行", ["PARA-02", "DISP-01"],
          CAPTION_SUPP.replace("<!-- loj:paragraph number=2 caption=present -->", "<!-- loj:paragraph number=2 -->"),
          fail("DISP-01"), False)
supp_case("captionの属性の値absent", ["DIR-01", "PARA-02"],
          CAPTION_SUPP.replace("number=2 caption=present", "number=2 caption=absent"), fail("DIR-01"), False)
# LF; the caption line （保管の義務） (7 x 3 + LF = 22 bytes) follows 12 + 48 = 60 bytes.
case("見出しの行の後に本文の行がなく号が続く", ["PARA-02", "SRC-01"],
     [("main.md", "main", ART + "<!-- loj:paragraph number=1 caption=present -->\n（保管の義務）\n"
       "<!-- loj:item number=1 -->\n一　白雲\n<!-- loj:end-item -->\n<!-- loj:end-paragraph -->\n")],
     fail_at("PARA-02", "main.md", 60, 82), False)
# LF; the caption line （雲の返還 (5 x 3 bytes + LF = 16) follows 12+32+31+27+48 = 150 bytes.
case("対応しない括弧の見出しの行の位置", ["PARA-02", "SRC-01"],
     [("main.md", "main", ART + P1 + "<!-- loj:paragraph number=2 caption=present -->\n（雲の返還\n２　雲を返す。\n"
       "<!-- loj:end-paragraph -->\n")], fail_at("PARA-02", "main.md", 150, 166), False)

# CRLF: the caption excludes the CR as well as the LF; the text keeps both.
CRLF_CAP = "（施行期日）\r\n１　この法律は、公布の日から施行する。\r\n"
case("CRLFの附則の項の見出し", ["PARA-02", "AST-01", "BASIC-02"],
     MAIN_A1 + [("supp.md", "supplement/original", "# 附則\r\n<!-- loj:paragraph number=1 caption=present -->\r\n" + CRLF_CAP +
                 "<!-- loj:end-paragraph -->\r\n")],
     {"ast": ast(MAIN_A1_AST, supplements=[node("SupplementaryProvision", SUPP, None, "附則", [
         para(SUPP, "1", CRLF_CAP, display="１", caption="（施行期日）")])])}, True, man_extra=ORIGINAL)

# 2026-11-13 (#67): locations of duplicates and heading violations (SRC-01). Offsets are counted by hand.
# 雲 U+1F600 を保管する。 is 3 + 4 + 18 = 25 bytes; with LF 26, with CRLF 27.
EMOJI_BODY = "雲" + chr(0x1F600) + "を保管する。"
EMOJI_P1 = "<!-- loj:paragraph number=1 -->\n" + EMOJI_BODY + "\n<!-- loj:end-paragraph -->\n"  # 32 + 26 + 27 = 85
EMOJI_P1_CRLF = "<!-- loj:paragraph number=1 -->\r\n" + EMOJI_BODY + "\r\n<!-- loj:end-paragraph -->\r\n"  # 33 + 27 + 28 = 88
# documents lists b.md before a.md, so the later article is in a.md (reading order, not file names).
# a.md (CRLF): 第二章　雑則 (2 + 9 + 3 + 6 + CRLF 2 = 22 bytes), then the duplicate 第一条 (2 + 9 + 2 = 13 bytes).
case("章をまたぐ条の重複の位置（後のファイル、読み込みの順）", ["HEAD-02", "MAN-03", "SRC-01"],
     [("b.md", "main", "# 第一章　総則\n" + ART + P1),
      ("a.md", "main", "# 第二章　雑則\r\n# 第一条\r\n" + CRLF_P1)], fail_at("HEAD-02", "a.md", 22, 35), False)
# two.md (CRLF): 第二条 (13) + EMOJI_P1_CRLF (88) = 101 bytes, then 第一章　総則 again (2 + 18 + 2 = 22 bytes).
case("分類の番号の重複の位置（別のファイル、4バイトの文字の後）", ["HEAD-02", "MAN-03", "SRC-01"],
     [("one.md", "main", "# 第一章　総則\n" + ART + P1),
      ("two.md", "main", "# 第二条\r\n" + EMOJI_P1_CRLF + "# 第一章　総則\r\n# 第三条\r\n" + CRLF_P1)],
     fail_at("HEAD-02", "two.md", 101, 123), False)
# LF: 第一条 (12) + EMOJI_P1 (85) = 97 bytes, then the later start marker (32 bytes). The container would end at 187.
case("項の番号の重複の位置（後の開始のマーカーの行）", ["DIR-02", "SRC-01"],
     [("main.md", "main", ART + EMOJI_P1 + P1)], fail_at("DIR-02", "main.md", 97, 129), False)
# tables.md (LF): 第二条 12, paragraph 32, lead 61, table 28, row 26, cell 18, 白雲 7, end-cell 22, cell 18, 一号倉庫 13,
# end-cell 22, end-row 21 = 280 bytes, then the second row start marker (26 bytes).
case("行のkeyの重複の位置（main.mdでないファイル）", ["TABLE-02", "SRC-01"],
     [("main.md", "main", ART + P1),
      ("tables.md", "main", TABLE_MD.replace("# 第一条", "# 第二条").replace("row key=b6gr", "row key=k3v9"))],
     fail_at("TABLE-02", "tables.md", 280, 306), False)
# LF: 第一条 (12) + 第一条's paragraph (90) = 102 bytes, then the marker with number twice (41 bytes).
case("属性の重複の位置", ["DIR-01", "SRC-01"],
     [("main.md", "main", ART + P1 + "<!-- loj:paragraph number=2 number=2 -->\n２　雲を返す。\n<!-- loj:end-paragraph -->\n")],
     fail_at("DIR-01", "main.md", 102, 143), False)
# CRLF: 第一条 (13) + EMOJI_P1_CRLF (88) = 101 bytes, then 第二絛 (2 + 9 + 2 = 13 bytes).
case("表にない字体の条ラベルの位置（CRLFと4バイトの文字）", ["HEAD-01", "SRC-01"],
     [("main.md", "main", "# 第一条\r\n" + EMOJI_P1_CRLF + "# 第二絛\r\n" + CRLF_P1)],
     fail_at("HEAD-01", "main.md", 101, 114), False)
# LF: 97 bytes, then 第二条（雲（白雲の保管） (2 + 9 + 27 + 1 = 39 bytes).
case("条の見出しの対応しない括弧の位置（4バイトの文字の後）", ["HEAD-01", "SRC-01"],
     [("main.md", "main", ART + EMOJI_P1 + "# 第二条（雲（白雲の保管）\n" + P1)],
     fail_at("HEAD-01", "main.md", 97, 136), False)
# supp.md (CRLF): 附 則 with an ASCII space (2 + 3 + 1 + 3 + 2 = 11 bytes) is the first line.
supp_case("附則の見出しの半角空白の位置（CRLF）", ["HEAD-03", "SRC-01"],
          "# 附 則\r\n<!-- loj:paragraph number=1 -->\r\nこの法律は、公布の日から施行する。\r\n<!-- loj:end-paragraph -->\r\n",
          fail_at("HEAD-03", "supp.md", 0, 11), False)


def main():
    index_path = DST / "manifest.json"
    index = json.loads(index_path.read_text(encoding="utf-8"))
    kept = [c for c in index["cases"] if int(c["id"][4:]) < FIRST]
    index["cases"] = kept + CASES
    write(index_path, json.dumps(index, ensure_ascii=False, indent=2) + "\n")
    print(f"Authored {len(CASES)} v1alpha2 cases by hand; no parser invoked.")


if __name__ == "__main__":
    main()
