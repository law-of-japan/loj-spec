"""Materialize reviewed schema definitions and hand-authored fixture trees.

Not a parser. Never import a validator here or derive expected trees from Markdown.
CI reads the checked-in JSON; it does not run this authoring helper.
"""
import copy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def write(path, value):
    dest = ROOT / path
    dest.parent.mkdir(parents=True, exist_ok=True)
    if not isinstance(value, str):
        value = json.dumps(value, ensure_ascii=False, indent=2) + "\n"
    dest.write_bytes(value.encode("utf-8"))


def obj(properties, required=None):
    return {"type": "object", "properties": properties,
            "required": list(properties) if required is None else required,
            "additionalProperties": False}


def arr(items, minimum=0):
    return {"type": "array", "items": items, "minItems": minimum}


STRING = {"type": "string", "minLength": 1}
KEY = {"type": "string", "pattern": "^[a-z][a-z0-9-]*$"}
NUMBER = {"type": "string", "pattern": "^[1-9][0-9]{0,3}(-[1-9][0-9]{0,3})*$"}
LAW = obj({
    "id": {"type": "string", "pattern": "^[A-Za-z0-9][A-Za-z0-9-]*$"},
    "title": STRING,
    "type": {"enum": ["constitution", "act", "cabinetOrder", "imperialOrder",
                      "ministerialOrdinance", "rule", "ordinance", "other"]},
    "number": {"anyOf": [STRING, {"type": "null"}]},
    "promulgatedAt": {"anyOf": [{"type": "string", "format": "date",
        "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}$"}, {"type": "null"}]},
    "language": {"const": "ja"},
})
SCOPE = obj({"key": KEY, "title": STRING})
MANIFEST = obj({
    "schemaVersion": {"const": "loj/v1alpha1"}, "law": LAW,
    "documents": arr(obj({
        "path": {"type": "string", "pattern": "^(?:[A-Za-z0-9_.-]+/)*[A-Za-z0-9_.-]+\\.md$"},
        "parent": {"type": "string", "pattern": "^(main|supplement/[a-z][a-z0-9-]*|appendix/[a-z][a-z0-9-]*)$"},
    }), 1),
    "supplements": arr(SCOPE), "appendices": arr(SCOPE),
    "sources": arr({"type": "string", "format": "uri"}),
    "unsupportedFeatures": arr(STRING),
}, ["schemaVersion", "law", "documents"])


def schema(name, content):
    result = {"$schema": "https://json-schema.org/draft/2020-12/schema",
              "$id": "https://law-of-japan.github.io/loj-spec/schemas/v1alpha1/" + name,
              "$comment": "Canonical identifier only; publication at this URI is not required."}
    result.update(content)
    write("schemas/v1alpha1/" + name, result)


schema("manifest.schema.json", MANIFEST)
node = obj({
    "kind": {"enum": ["Law", "MainProvision", "Part", "Chapter", "Section", "Subsection",
                       "Division", "Article", "Paragraph", "Item", "Subitem",
                       "SupplementaryProvision", "AppendedMaterial"]},
    "id": STRING, "number": {"anyOf": [NUMBER, {"type": "null"}]},
    "display": {"type": "string"},
    "content": arr({"oneOf": [obj({"text": STRING}), {"$ref": "#/$defs/node"}]}),
    "status": {"enum": ["active", "deleted"]},
    "level": {"type": "integer", "minimum": 1, "maximum": 10},
}, ["kind", "id", "number", "display", "content"])
node["allOf"] = [
    {"if": {"properties": {"kind": {"const": "Article"}}},
     "then": {"required": ["status"]}, "else": {"not": {"required": ["status"]}}},
    {"if": {"properties": {"kind": {"const": "Subitem"}}},
     "then": {"required": ["level"]}, "else": {"not": {"required": ["level"]}}},
    {"if": {"properties": {"kind": {"enum": ["Law", "MainProvision", "SupplementaryProvision", "AppendedMaterial"]}}},
     "then": {"properties": {"number": {"type": "null"}}},
     "else": {"properties": {"number": NUMBER}}},
]
ast = obj({"schemaVersion": {"const": "loj/v1alpha1"}, "law": LAW,
           "root": {"$ref": "#/$defs/node"}})
ast["$defs"] = {"node": node}
schema("ast.schema.json", ast)
position = obj({"nodeId": STRING, "path": STRING,
                "start": {"type": "integer", "minimum": 0},
                "end": {"type": "integer", "minimum": 0}})
expected = obj({"ast": {"$ref": "ast.schema.json"},
                "diagnostics": arr(obj({"rule": STRING}), 1),
                "positions": arr(position)}, [])
expected["oneOf"] = [{"required": ["ast"], "not": {"required": ["diagnostics"]}},
                      {"required": ["diagnostics"], "not": {"required": ["ast"]}}]
schema("expected.schema.json", expected)
case = obj({"id": {"type": "string", "pattern": "^T[0-9]{3}$"}, "title": STRING,
            "requirements": arr(STRING, 1), "level": {"enum": ["L0", "L1", "L2"]},
            "normative": {"type": "boolean"}, "input": STRING, "expected": STRING,
            "success": {"type": "boolean"}})
schema("conformance.schema.json", obj({"schemaVersion": {"const": "loj/v1alpha1"},
                                      "cases": arr(case, 1)}))

LAW_VALUE = {"id": "20990101-act-1", "title": "架空雲保管法（実在しないサンプル）",
             "type": "act", "number": "架空法律第一号", "promulgatedAt": "2099-01-01", "language": "ja"}
LID = LAW_VALUE["id"]


def manifest(files, **extra):
    value = {"schemaVersion": "loj/v1alpha1", "law": copy.deepcopy(LAW_VALUE),
             "documents": [{"path": path, "parent": parent} for path, parent in files]}
    value.update(extra)
    return value


def n(kind, number=None, display="", content=None, **extra):
    return dict(kind=kind, number=number, display=display, content=content or [], **extra)


def t(text):
    return {"text": text}


def p(text="架空の雲を保管する。\n", number="1", display="", children=None):
    return n("Paragraph", number, display, [t(text)] + (children or []))


def a(number="1", display="第一条", children=None, deleted=False):
    return n("Article", number, display, [] if deleted else (children or [p()]),
             status="deleted" if deleted else "active")


def tree(children, extras=None):
    root = n("Law", display=LAW_VALUE["title"], content=[n("MainProvision", content=children)] + (extras or []))

    def ids(node, parent_id, scope):
        kind = node["kind"]
        if kind == "Law":
            ident = LID
        elif kind == "MainProvision":
            ident = scope = LID + "/main"
        elif kind in ("SupplementaryProvision", "AppendedMaterial"):
            prefix = "supplement" if kind == "SupplementaryProvision" else "appendix"
            ident = scope = LID + "/" + prefix + "/" + node.pop("key")
        elif kind == "Article":
            ident = scope + "/article/" + node["number"]
        else:
            suffix = str(node["level"]) + "/" if kind == "Subitem" else ""
            ident = parent_id + "/" + kind.lower() + "/" + suffix + node["number"]
        node["id"] = ident
        for child in node["content"]:
            if "kind" in child:
                ids(child, ident, scope)
    ids(root, "", "")
    return {"schemaVersion": "loj/v1alpha1", "law": copy.deepcopy(LAW_VALUE), "root": root}


def wrap(text="架空の雲を保管する。\n", number="1", kind="paragraph", level=None):
    attrs = ("level=" + str(level) + " ") if level is not None else ""
    return "<!-- loj:" + kind + " " + attrs + "number=" + number + " -->\n" + text + "<!-- loj:end-" + kind + " -->\n"


BASE = "# 第一条\n" + wrap()
CASES = []


def add(title, rules, text=BASE, ast_value=None, failure=None, level="L1", files=None, man=None,
        positions=None, normative=True):
    ident = "T%03d" % (len(CASES) + 1)
    success = failure is None
    folder = "conformance/" + ("valid/" if success else "invalid/") + ident
    files = files if files is not None else {"main.md": text}
    man = man if man is not None else manifest([(name, "main") for name in files])
    write(folder + "/law.yaml", man)  # JSON is deliberately valid YAML 1.2.
    for name, value in files.items():
        write(folder + "/" + name, value)
    expected_value = {"ast": ast_value or tree([a()])} if success else {"diagnostics": [{"rule": failure}]}
    if positions:
        expected_value["positions"] = positions
    expected_path = "conformance/expected/" + ident + ".json"
    write(expected_path, expected_value)
    CASES.append(dict(id=ident, title=title, requirements=rules.split(), level=level,
                      normative=normative, input=folder + "/law.yaml", expected=expected_path, success=success))


add("単一項", "DIR-01 DIR-02 AST-01", ast_value=tree([a()]))
add("複数項", "DIR-02 DISP-01", "# 第一条\n" + wrap() + wrap("2　雲は架空である。\n", "2"),
    tree([a(children=[p(), p("2　雲は架空である。\n", "2", "2")])]))
items = [n("Item", str(i), label, [t(label + "　架空の号。\n")]) for i, label in [(1, "一"), (2, "二")]]
item_md = wrap("一　架空の号。\n", "1", "item") + wrap("二　架空の号。\n", "2", "item")
add("複数号", "DIR-02 DISP-01", "# 第一条\n" + wrap("架空の雲を保管する。\n" + item_md),
    tree([a(children=[p(children=items)])]))
sub = n("Subitem", "1", "1", [t("1　架空の細分。\n")], level=1)
add("号の細分", "DIR-02 ID-01", "# 第一条\n" + wrap("架空の雲を保管する。\n" + wrap("一　架空の号。\n" + wrap("1　架空の細分。\n", "1", "subitem", 1), "1", "item")),
    tree([a(children=[p(children=[n("Item", "1", "一", [t("一　架空の号。\n"), sub])])])]))
add("複数段落", "MD-02 AST-01", "# 第一条\n" + wrap("架空の雲。\n\n次の段落。\n"), tree([a(children=[p("架空の雲。\n\n次の段落。\n")])]))
add("終了不一致", "DIR-02", BASE.replace("end-paragraph", "end-item"), failure="DIR-02")
add("項外の号", "DIR-02", "# 第一条\n" + wrap("一　本文。\n", kind="item"), failure="DIR-02")
add("項番号重複", "DIR-02 AST-02", BASE + wrap(), failure="DIR-02")
add("枝番号", "NUM-01 ID-01", "# 第十二条の二の三\n" + wrap(), tree([a("12-2-3", "第十二条の二の三")]))
add("表示番号不一致", "DISP-01", "# 第一条\n" + wrap("2　本文。\n"), failure="DISP-01")
code = "架空の例。\n\n```md\n<!-- loj:item number=1 -->\n# 第二条\n```\n"
add("コード内マーカー", "MD-01 MD-02", "# 第一条\n" + wrap(code), tree([a(children=[p(code)])]))
comment = "架空の例。\n<!-- 通常のコメント loj:example -->\n"
add("通常HTMLコメント", "MD-01 MD-02", "# 第一条\n" + wrap(comment), tree([a(children=[p(comment)])]))
add("属性欠落", "DIR-01", BASE.replace(" number=1", ""), failure="DIR-01")
add("属性重複", "DIR-01", BASE.replace("number=1", "number=1 number=1"), failure="DIR-01")
add("未知属性", "DIR-01 BASIC-04", BASE.replace("number=1", "number=1 label=x"), failure="DIR-01")
chapter = n("Chapter", "1", "第一章　総則", [a(), a("2", "第二条")])
whole = "# 第一章　総則\n" + BASE + "# 第二条\n" + wrap()
add("複数ファイル統合", "MAN-03 HEAD-02", files={"one.md": "# 第一章　総則\n" + BASE, "two.md": "# 第二条\n" + wrap()}, ast_value=tree([copy.deepcopy(chapter)]))
add("分割前と同じASTとID", "MAN-03 ID-01 ID-02", whole, tree([copy.deepcopy(chapter)]))
add("日本語UTF-8位置", "SRC-01", positions=[{"nodeId": LID + "/main/article/1/paragraph/1", "path": "main.md", "start": 12, "end": 102}])
add("CRLF位置", "BASIC-02 SRC-01", BASE.replace("\n", "\r\n"), tree([a(children=[p("架空の雲を保管する。\r\n")])]),
    positions=[{"nodeId": LID + "/main/article/1/paragraph/1", "path": "main.md", "start": 13, "end": 106}])
badman = manifest([("main.md", "main")]); badman["unexpected"] = True
add("Manifest未知フィールド", "MAN-01", man=badman, failure="MAN-01", level="L0")
supp = n("SupplementaryProvision", display="附則", content=[a()], key="original")
add("本則と附則の番号空間", "HEAD-03 ID-01 MAN-03", files={"main.md": BASE, "supp.md": "# 附則\n" + BASE},
    man=manifest([("main.md", "main"), ("supp.md", "supplement/original")], supplements=[{"key": "original", "title": "制定附則"}]),
    ast_value=tree([a()], [supp]))
add("不正Markdown見出し", "MD-03 HEAD-01", BASE.replace("# 第一条", "#第一条"), failure="MD-03")
add("マーカーなし本文", "MD-03", "# 第一条\n架空の雲を保管する。\n", failure="MD-03")
rich = "**架空**の雲。\n\n> 引用。\n\n- 通常リスト。\n\n[参照](https://example.org/) と `code`。\n"
add("引用リスト強調リンク", "MD-02 AST-01", "# 第一条\n" + wrap(rich), tree([a(children=[p(rich)])]))
reftext = "[存在しない条](loj:main/article/999)\n"
add("不正参照もL1では原文保持", "REF-01 MD-02", "# 第一条\n" + wrap(reftext), tree([a(children=[p(reftext)])]))
add("不正参照の将来L2例", "REF-01", "# 第一条\n" + wrap(reftext), failure="REF-01", level="L2", normative=False)
add("空ファイル", "BASIC-02", "", failure="BASIC-02", level="L0")
add("空項", "DIR-02", "# 第一条\n" + wrap(""), failure="DIR-02")
add("未閉鎖", "DIR-02 SRC-01", BASE.replace("<!-- loj:end-paragraph -->\n", ""), failure="DIR-02")
add("未知マーカー", "DIR-01 BASIC-04", BASE.replace("loj:paragraph", "loj:unknown"), failure="DIR-01")
add("引用符属性", "DIR-01", BASE.replace("number=1", 'number="1"'), failure="DIR-01")
add("先頭ゼロ", "DIR-01 NUM-01", BASE.replace("number=1", "number=01"), failure="DIR-01")
add("レベル飛越し", "DIR-02", "# 第一条\n" + wrap("本文。\n" + wrap("一　号。\n" + wrap("1　細分。\n", "1", "subitem", 2), "1", "item")), failure="DIR-02")
add("削除条", "HEAD-04 ID-02", "# 第一条\n削除\n", tree([a(deleted=True)]))
add("見出しレベルは所属と独立", "HEAD-01 HEAD-02", "###### 第一章　総則\n" + BASE,
    tree([n("Chapter", "1", "第一章　総則", [a()])]))
add("無番号見出し拒否", "HEAD-01 BASIC-03", "# 総則\n" + BASE, failure="HEAD-01")
add("親本文は子の後も保存", "AST-01 MD-02", "# 第一条\n" + wrap("前文。\n" + wrap("一　号。\n", "1", "item") + "後文。\n"),
    tree([a(children=[n("Paragraph", "1", "", [t("前文。\n"), n("Item", "1", "一", [t("一　号。\n")]), t("後文。\n")])])]))
add("パストラバーサル", "MAN-02", man=manifest([("../outside.md", "main")]), failure="MAN-02", level="L0")
add("ファイル重複", "MAN-02", man=manifest([("main.md", "main"), ("main.md", "main")]), failure="MAN-02", level="L0")
add("未定義附則キー", "MAN-03", man=manifest([("main.md", "supplement/missing")]), failure="MAN-03", level="L0")
add("存在しない日付", "MAN-01", man={**manifest([("main.md", "main")]), "law": {**LAW_VALUE, "promulgatedAt": "2099-02-30"}}, failure="MAN-01", level="L0")
add("未対応構造の申告", "BASIC-03", man=manifest([("main.md", "main")], unsupportedFeatures=["preamble"]), failure="BASIC-03")
add("ファイルを跨ぐ項を拒否", "MAN-03 DIR-02", files={"one.md": "# 第一条\n<!-- loj:paragraph number=1 -->\n本文。\n", "two.md": "<!-- loj:end-paragraph -->\n"}, failure="DIR-02")
add("Setext拒否", "HEAD-01", "第一条\n===\n" + wrap(), failure="HEAD-01")
raw = "本文。\n\n<div>\n<!-- loj:item number=1 -->\n</div>\n\n"
add("raw HTML内保護", "MD-01", "# 第一条\n" + wrap(raw), tree([a(children=[p(raw)])]))
add("複数行予約マーカー", "DIR-01 MD-01", BASE.replace("loj:paragraph number=1", "loj:paragraph\nnumber=1"), failure="DIR-01")
add("大文字予約マーカー", "DIR-01 MD-01", BASE.replace("loj:paragraph", "LOJ:paragraph"), failure="DIR-01")
add("全角番号", "NUM-01 DISP-01", "# 第１２条\n" + wrap("２　本文。\n", "2"), tree([a("12", "第１２条", [p("２　本文。\n", "2", "２")])]))
add("非標準漢数字", "NUM-01", "# 第一十条\n" + wrap(), failure="NUM-01")
add("章を跨ぐ条重複", "HEAD-02 AST-02", "# 第一章　甲\n" + BASE + "# 第二章　乙\n" + BASE, failure="HEAD-02")
direct = n("SupplementaryProvision", display="附則", content=[p()], key="original")
add("条のない附則", "HEAD-03 DIR-02", files={"main.md": BASE, "supp.md": "# 附則\n" + wrap()},
    man=manifest([("main.md", "main"), ("supp.md", "supplement/original")], supplements=[{"key": "original", "title": "制定附則"}]), ast_value=tree([a()], [direct]))
appendix_text = "| 雲 | 色 |\n| --- | --- |\n| 架空 | 青 |\n"
add("不透明な附属資料", "HEAD-03 MD-02 AST-01", files={"main.md": BASE, "table.md": "# 別表一\n" + appendix_text},
    man=manifest([("main.md", "main"), ("table.md", "appendix/table-1")], appendices=[{"key": "table-1", "title": "別表一"}]),
    ast_value=tree([a()], [n("AppendedMaterial", display="別表一", content=[t(appendix_text)], key="table-1")]))
deep = n("Subitem", "1", "1", [t("1　細分。\n")], level=10)
deep_md = wrap("1　細分。\n", "1", "subitem", 10)
for level in range(9, 0, -1):
    deep = n("Subitem", "1", "1", [t("1　細分。\n"), deep], level=level)
    deep_md = wrap("1　細分。\n" + deep_md, "1", "subitem", level)
add("細分10階層", "DIR-02 ID-01", "# 第一条\n" + wrap("本文。\n" + wrap("一　号。\n" + deep_md, "1", "item")),
    tree([a(children=[p("本文。\n", children=[n("Item", "1", "一", [t("一　号。\n"), deep])])])]))
allgroups = a()
for kind, label in reversed([("Part", "第一編　甲"), ("Chapter", "第一章　乙"), ("Section", "第一節　丙"), ("Subsection", "第一款　丁"), ("Division", "第一目　戊")]):
    allgroups = n(kind, "1", label, [allgroups])
add("分類全階層", "HEAD-02 AST-01 ID-01", "# 第一編　甲\n# 第一章　乙\n# 第一節　丙\n# 第一款　丁\n# 第一目　戊\n" + BASE, tree([allgroups]))
add("先頭空白マーカー", "MD-01 DIR-01", BASE.replace("<!-- loj:paragraph", " <!-- loj:paragraph"), failure="DIR-01")
add("BOM禁止", "BASIC-02", "\ufeff" + BASE, failure="BASIC-02", level="L0")
add("単独CR禁止", "BASIC-02", BASE.replace("\n", "\r"), failure="BASIC-02", level="L0")
add("未知バージョン", "BASIC-01", man={**manifest([("main.md", "main")]), "schemaVersion": "loj/v9"}, failure="BASIC-01", level="L0")
add("YAML重複キー", "MAN-01", man='schemaVersion: loj/v1alpha1\nschemaVersion: loj/v1alpha1\n', failure="MAN-01", level="L0")
add("別scopeから戻る順序", "MAN-03", files={"one.md": BASE, "supp.md": "# 附則\n" + BASE, "two.md": "# 第二条\n" + wrap()},
    man=manifest([("one.md", "main"), ("supp.md", "supplement/original"), ("two.md", "main")], supplements=[{"key": "original", "title": "制定附則"}]), failure="MAN-03", level="L0")

# A complete fictional law, with independently authored expected tree.
sample_one = "# 第一章　総則\n## 第一条（目的）\n" + wrap("この架空法は雲の保管を演習する。\n")
sample_one += "## 第二条（分類）\n" + wrap("雲は次のとおりとする。\n" + wrap("一　青い雲。\n" + wrap("1　淡い青。\n", "1", "subitem", 1), "1", "item") + wrap("二　白い雲。\n", "2", "item")) + wrap("2　分類は架空である。\n", "2")
sample_two = "# 第二章　保管\n## 第三条（保管）\n" + wrap("[第二条](loj:main/article/2)の雲を空想の箱に保管する。\n")
sample_supp = "# 附則\n## 第一条（演習）\n" + wrap("このサンプルは現実の権利義務を定めない。\n")
sample_man = manifest([("provisions/chapter1.md", "main"), ("provisions/chapter2.md", "main"), ("supplements/original.md", "supplement/original")], supplements=[{"key": "original", "title": "制定附則"}])
sample_tree = tree([
    n("Chapter", "1", "第一章　総則", [
        a("1", "第一条（目的）", [p("この架空法は雲の保管を演習する。\n")]),
        a("2", "第二条（分類）", [p("雲は次のとおりとする。\n", children=[
            n("Item", "1", "一", [t("一　青い雲。\n"), n("Subitem", "1", "1", [t("1　淡い青。\n")], level=1)]),
            n("Item", "2", "二", [t("二　白い雲。\n")])]), p("2　分類は架空である。\n", "2", "2")])]),
    n("Chapter", "2", "第二章　保管", [a("3", "第三条（保管）", [p("[第二条](loj:main/article/2)の雲を空想の箱に保管する。\n")])]),
], [n("SupplementaryProvision", display="附則", key="original", content=[a("1", "第一条（演習）", [p("このサンプルは現実の権利義務を定めない。\n")])])])
write("examples/fictional-law/law.yaml", '''schemaVersion: loj/v1alpha1
law:
  id: "20990101-act-1"
  title: "架空雲保管法（実在しないサンプル）"
  type: act
  number: "架空法律第一号"
  promulgatedAt: "2099-01-01"
  language: ja
supplements:
  - key: original
    title: "制定附則"
documents:
  - path: provisions/chapter1.md
    parent: main
  - path: provisions/chapter2.md
    parent: main
  - path: supplements/original.md
    parent: supplement/original
''')
for name, value in [("provisions/chapter1.md", sample_one), ("provisions/chapter2.md", sample_two), ("supplements/original.md", sample_supp)]:
    write("examples/fictional-law/" + name, value)
write("examples/fictional-law/expected.ast.json", sample_tree)
add("完全サンプル", "MAN-03 AST-01 ID-01 REF-01", files={"provisions/chapter1.md": sample_one, "provisions/chapter2.md": sample_two, "supplements/original.md": sample_supp}, man=sample_man, ast_value=sample_tree)
add("複数附則の独立キー", "HEAD-03 ID-01 MAN-03", files={"main.md": BASE, "original.md": "# 附則\n" + BASE, "amend.md": "# 附則\n" + BASE},
    man=manifest([("main.md", "main"), ("original.md", "supplement/original"), ("amend.md", "supplement/amend-1")],
                 supplements=[{"key": "original", "title": "制定附則"}, {"key": "amend-1", "title": "架空改正附則"}]),
    ast_value=tree([a()], [n("SupplementaryProvision", display="附則", key="original", content=[a()]), n("SupplementaryProvision", display="附則", key="amend-1", content=[a()])]))
quoted = "本文。\n\n> <!-- loj:item number=1 -->\n> # 第二条\n\n- <!-- loj:paragraph number=2 -->\n\n"
add("引用リスト内マーカー保護", "MD-01", "# 第一条\n" + wrap(quoted), tree([a(children=[p(quoted)])]))
indentcode = "本文。\n\n    <!-- loj:item number=1 -->\n\n"
add("インデントコード保護", "MD-01", "# 第一条\n" + wrap(indentcode), tree([a(children=[p(indentcode)])]))
add("末尾改行なし", "BASIC-02 SRC-01", BASE.rstrip("\n"), tree([a()]))
add("附則見出しでscopeを変えない", "HEAD-03", "# 附則\n" + BASE, failure="HEAD-03")
add("削除条の項を拒否", "HEAD-04", "# 第一条\n削除\n\n" + wrap(), failure="HEAD-04")
add("数字の幅混在を拒否", "NUM-01", "# 第１2条\n" + wrap(), failure="NUM-01")
add("マーカータブを拒否", "DIR-01", BASE.replace("paragraph number", "paragraph\tnumber"), failure="DIR-01")
add("終了属性を拒否", "DIR-01", BASE.replace("end-paragraph -->", "end-paragraph number=1 -->"), failure="DIR-01")
add("本文中の見出しを拒否", "DIR-02 MD-03", "# 第一条\n" + wrap("本文。\n# 第二条\n"), failure="DIR-02")
add("分類見出し再掲を拒否", "HEAD-02 MAN-03", files={"one.md": "# 第一章　総則\n" + BASE, "two.md": "# 第一章　総則\n# 第二条\n" + wrap()}, failure="HEAD-02")
add("欠番と逆順を保持", "HEAD-02 AST-01", "# 第三条\n" + wrap() + BASE, tree([a("3", "第三条"), a()]))
add("字母細分は未対応", "DISP-01 BASIC-03", "# 第一条\n" + wrap("本文。\n" + wrap("一　号。\n" + wrap("イ　細分。\n", "1", "subitem", 1), "1", "item")), failure="DISP-01")
add("属性順の交換", "DIR-01", "# 第一条\n" + wrap("本文。\n" + wrap("一　号。\n" + wrap("1　細分。\n", "1", "subitem", 1).replace("level=1 number=1", "number=1 level=1"), "1", "item")),
    tree([a(children=[p("本文。\n", children=[n("Item", "1", "一", [t("一　号。\n"), n("Subitem", "1", "1", [t("1　細分。\n")], level=1)])])])]))
from appendix_cases import add_cases
add_cases(add, manifest, tree, a, n, t, BASE)
write("conformance/manifest.json", {"schemaVersion": "loj/v1alpha1", "cases": CASES})
print("Materialized", len(CASES), "hand-authored cases and schemas; no parser invoked.")
