"""Mutation/regression checks for the artifact auditor, not L1 conformance tests."""
import copy
import json
import re
import sys
import tempfile
import unicodedata
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import verify as v


class ArtifactAuditTests(unittest.TestCase):
    def setUp(self):
        self.path = v.ROOT / "conformance/v1alpha1/valid/T001/law.yaml"
        self.man = v.load_yaml(self.path.read_text(encoding="utf-8"))
        self.expected = v.read_json(v.ROOT / "conformance/v1alpha1/expected/T001.json")

    def test_split_appendix_expected_text_is_audited(self):
        path = v.ROOT / "conformance/v1alpha1/valid/T076/law.yaml"
        man = v.load_yaml(path.read_text(encoding="utf-8"))
        expected = v.read_json(v.ROOT / "conformance/v1alpha1/expected/T076.json")
        v.check_positive(path, man, expected)
        expected["ast"]["root"]["content"][1]["content"][0]["text"] = "本文。\n\n"
        with self.assertRaises(ValueError):
            v.check_positive(path, man, expected)

    def test_duplicate_yaml_keys_rejected(self):
        with self.assertRaises(ValueError):
            v.load_yaml("a: 1\na: 2\n")

    def test_yaml_extensions_rejected(self):
        for raw in ("a: &x 1\nb: *x\n", "a: !!str value\n", "a: 1\n---\nb: 2\n"):
            with self.subTest(raw=raw), self.assertRaises((ValueError, v.yaml.YAMLError)):
                v.load_yaml(raw)

    def test_yaml12_not_yaml11(self):
        self.assertEqual(v.load_yaml("a: yes\nb: on\nc: true\nd: 12\n"),
                         {"a": "yes", "b": "on", "c": True, "d": 12})

    def test_date_requires_quotes(self):
        with self.assertRaises(ValueError):
            v.load_yaml("a: 2099-01-01\n")

    def test_unsafe_paths(self):
        for name in ("../x.md", "/x.md", "C:/x.md", "x\\y.md", "./x.md", "CON.md", "dir./x.md", "x//y.md"):
            with self.subTest(path=name):
                self.assertFalse(v.path_ok(name))
        self.assertTrue(v.path_ok("provisions/chapter-1.md"))

    def test_input_bytes(self):
        for raw in (b"", b"\xef\xbb\xbftext", b"x\ry", b"x\x00y", b"\xff"):
            with self.subTest(raw=raw), self.assertRaises((ValueError, UnicodeError)):
                v.check_bytes(raw)
        self.assertEqual(v.check_bytes("雲\r\n".encode()), "雲\r\n")

    def test_duplicate_id_mutation(self):
        ast = copy.deepcopy(self.expected["ast"])
        main = ast["root"]["content"][0]
        main["content"].append(copy.deepcopy(main["content"][0]))
        with self.assertRaises(ValueError):
            v.check_tree(ast, self.man)

    def test_wrong_id_mutation(self):
        ast = copy.deepcopy(self.expected["ast"])
        ast["root"]["content"][0]["content"][0]["id"] += "-2"
        with self.assertRaises(ValueError):
            v.check_tree(ast, self.man)

    def test_wrong_parent_mutation(self):
        ast = copy.deepcopy(self.expected["ast"])
        article = ast["root"]["content"][0]["content"][0]
        article["content"][0]["kind"] = "Item"
        article["content"][0]["id"] = article["id"] + "/item/1"
        with self.assertRaises(ValueError):
            v.check_tree(ast, self.man)

    def test_expected_text_mutation(self):
        expected = copy.deepcopy(self.expected)
        expected["ast"]["root"]["content"][0]["content"][0]["content"][0]["content"][0]["text"] = "変更された本文。\n"
        with self.assertRaises(ValueError):
            v.check_positive(self.path, self.man, expected)

    def test_fixed_position_mutation(self):
        expected = v.read_json(v.ROOT / "conformance/v1alpha1/expected/T018.json")
        expected["positions"][0]["start"] += 1
        with self.assertRaises(ValueError):
            v.check_positive(self.path, self.man, expected)

    def test_source_mutation(self):
        build = v.ROOT / ".build"
        build.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=build) as folder:
            path = Path(folder) / "law.yaml"
            path.write_text(self.path.read_text(encoding="utf-8"), encoding="utf-8")
            (path.parent / "main.md").write_text("# 第一条\n本文だけ。\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                v.check_positive(path, self.man, self.expected)

    def test_heading_number_mutation(self):
        ast = copy.deepcopy(self.expected["ast"])
        ast["root"]["content"][0]["content"][0]["display"] = "第二条"
        with self.assertRaises(ValueError):
            v.check_tree(ast, self.man)

    def test_number_forms(self):
        self.assertEqual(v.normalized_display("十二の二の三", "Article"), "12-2-3")
        self.assertEqual(v.normalized_display("千十", "Article"), "1010")
        self.assertEqual(v.normalized_display("１２", "Paragraph"), "12")
        for value in ("一十", "一二", "０１", "１2", "10000", "零", "壱"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                v.normalized_display(value, "Article")

    def test_non_decimal_subitem_display(self):
        for value in ("イ", "一", "１", "(1)"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                v.normalized_display(value, "Subitem")

    def test_v1alpha2_subitem_display(self):
        for value, number in (("イ", "1"), ("ノ", "26"), ("ス", "47"), ("（１）", "1"), ("（12）", "12"), ("1の2", "1-2")):
            with self.subTest(value=value):
                self.assertEqual(v.normalized_display(value, "Subitem", v2=True), number)
        for value in ("い", "ｲ", "(1)", "（０１）", "（1２）", "イの二", "（ｉ）", "一"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                v.normalized_display(value, "Subitem", v2=True)
        with self.assertRaises(ValueError):
            v.normalized_display("イ", "Item", v2=True)

    def test_v1alpha2_subitem_display_kind(self):
        for value, kind in (("イ", "iroha"), ("（１）", "parenFullwidth"), ("（1）", "parenAscii"), ("1", None), ("(1)", None)):
            with self.subTest(value=value):
                self.assertEqual(v.subitem_display_kind(value), kind)

    def test_v1alpha2_sibling_subitem_kinds(self):
        path = v.ROOT / "conformance/v1alpha2/valid/pkg-130/law.yaml"
        man = v.load_yaml(path.read_bytes())
        ast = v.read_json(v.ROOT / "conformance/v1alpha2/expected/pkg-130.json")["ast"]
        v.check_tree(ast, man, v2=True)
        level2 = ast["root"]["content"][0]["content"][0]["content"][0]["content"][1]["content"][2]["content"][1]
        level2["display"], level2["content"][0]["text"] = "イ", "イ　小さな積雲\n"
        with self.assertRaises(ValueError):
            v.check_tree(ast, man, v2=True)

    def test_v1alpha2_caption_parentheses(self):
        for value in ("（定義）", "（雲（白雲を除く。）の保管）", "（a(b)）"):
            with self.subTest(value=value):
                self.assertTrue(v.caption_balanced(value))
        for value in ("（）", "（雲（白雲の保管）", "（定義）（略）", "（定義））", "（定義"):
            with self.subTest(value=value):
                self.assertFalse(v.caption_balanced(value))

    def test_manifest_metadata_mutation(self):
        ast = copy.deepcopy(self.expected["ast"])
        ast["law"]["title"] = "別法令"
        with self.assertRaises(ValueError):
            v.check_tree(ast, self.man)


class ArchiveAuditTests(unittest.TestCase):
    """docs/archive must stay distinguishable from the normative spec/."""

    FILES = {
        "spec/a.md": "# A\n\n## VIEW-01 定義\n\n本文。\n",
        "docs/archive/old.md": "# 古い案\n\n状態: 経緯の記録。規範ではない。\n\n#### 案VIEW-01 定義\n",
        "docs/design-decisions/001.md": "# DDR-001 見出し\n",
        "README.md": "# R\n", "CONTRIBUTING.md": "# C\n", "CHANGELOG.md": "# L\n",
        "AGENTS.md": "# G\n",
    }

    def run_check(self, changes):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for name, text in {**self.FILES, **changes}.items():
                (root / name).parent.mkdir(parents=True, exist_ok=True)
                (root / name).write_text(text, encoding="utf-8")
            saved = v.ROOT, v.ARCHIVE
            v.ROOT, v.ARCHIVE = root.resolve(), (root / "docs/archive").resolve()
            try:
                return v.check_archive()
            finally:
                v.ROOT, v.ARCHIVE = saved

    def test_valid_layout_passes(self):
        self.assertEqual(self.run_check({}), 1)

    def test_rejections(self):
        cases = {
            "missing status": {"docs/archive/old.md": "# 古い案\n\n本文。\n"},
            "spec links archive": {"spec/a.md": "# A\n\n[案](../docs/archive/old.md)\n"},
            "bare ID heading in archive": {"docs/archive/old.md": "# 古い案\n\n状態: 記録。\n\n#### VIEW-01 定義\n"},
            "ID heading in docs": {"docs/guide.md": "# ガイド\n\n### HIST-01 履歴\n"},
        }
        for label, change in cases.items():
            with self.subTest(label), self.assertRaises(ValueError):
                self.run_check(change)


class CodePointNotationTests(unittest.TestCase):
    """A character written next to its code point must be that code point (DDR-021: silent normalization)."""

    COMPAT, UNIFIED = chr(0xFA19), chr(0x795E)

    def test_matching_notations_pass(self):
        texts = [
            f"例: {self.COMPAT} U+FA19。",
            f"{self.COMPAT}（U+FA19）／{self.UNIFIED}（U+795E）",
            "〓（U+3013）を置く。",
            "全角空白（U+3000）を置く。",  # 白 ends the word 空白, not a character example
            "互換漢字（U+F900〜U+FAFF、U+2F800〜U+2FA1F）",
            "私用領域の文字、U+FFFD、画像",
            "例: 〜（U+FF5E）、＋（U+002B）",  # punctuation (〜 is Pd) and math symbols (Sm) are never checked
        ]
        for text in texts:
            with self.subTest(text):
                self.assertEqual(v.codepoint_mismatches(text), [])

    def test_mismatches_reported(self):
        cases = {
            f"例: {self.UNIFIED} U+FA19。": [(1, "U+795E", "FA19")],
            f"一行目\n{self.UNIFIED}（U+FA19）／{self.UNIFIED}（U+795E）": [(2, "U+795E", "FA19")],
            "髙（U+9AD8）": [(1, "U+9AD9", "9AD8")],
            "例: 〓（U+3012）": [(1, "U+3013", "3012")],  # other symbols (So) are checked
        }
        for text, wanted in cases.items():
            with self.subTest(text):
                self.assertEqual(v.codepoint_mismatches(text), wanted)

    def run_check(self, files):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for name, text in {**{n: "# T\n" for n in v.ROOT_DOCS}, **files}.items():
                (root / name).parent.mkdir(parents=True, exist_ok=True)
                (root / name).write_text(text, encoding="utf-8")
            saved = v.ROOT, v.ARCHIVE
            v.ROOT, v.ARCHIVE = root.resolve(), (root / "docs/archive").resolve()
            try:
                return v.check_codepoints()
            finally:
                v.ROOT, v.ARCHIVE = saved

    def test_check_scope(self):
        bad = f"{self.UNIFIED} U+FA19\n"
        # ROOT_DOCS and spec/a/01.md are checked; docs/archive/old.md is skipped.
        self.assertEqual(self.run_check({"spec/a/01.md": f"{self.COMPAT} U+FA19\n", "docs/archive/old.md": bad}),
                         len(v.ROOT_DOCS) + 1)
        for name in ("spec/a/01.md", "docs/guide.md", "CHANGELOG.md"):
            with self.subTest(name), self.assertRaises(ValueError):
                self.run_check({name: bad})

    def test_repository_notations(self):
        self.assertGreater(v.check_codepoints(), 0)


class VersionStateTests(unittest.TestCase):
    """The state tables in spec/README.md are the source of truth for draft/published/frozen."""

    README = ("# 入口\n\n## 規範とするもの\n\n| ディレクトリ | 対象 | 状態 |\n|---|---|---|\n"
              "| [common/v1alpha1](common/v1alpha1/01.md) | 共通 | 草案 |\n"
              "| [v1alpha2](v1alpha2/01.md) | 版パッケージ | 公開 |\n\n- 注記。\n\n"
              "## 凍結した版\n\n| 版 | 状態 | 後継 |\n|---|---|---|\n"
              "| [v1alpha1](v1alpha1/01.md)（`loj/v1alpha1`） | 凍結。内容を変えない | `loj/v1alpha2` |\n")
    FOLDERS = ("common/v1alpha1", "v1alpha2", "v1alpha1")

    def run_check(self, readme=None, folders=None):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for name in self.FOLDERS if folders is None else folders:
                (root / "spec" / name).mkdir(parents=True)
                (root / "spec" / name / "01.md").write_text("# 本文\n", encoding="utf-8")
            (root / "spec/README.md").write_text(readme or self.README, encoding="utf-8")
            saved = v.ROOT
            v.ROOT = root.resolve()
            try:
                return v.check_states()
            finally:
                v.ROOT = saved

    def test_valid_tables_pass(self):
        self.assertEqual(self.run_check(), {"common/v1alpha1": "草案", "v1alpha2": "公開", "v1alpha1": "凍結"})

    def test_repository_states(self):
        states = v.check_states()
        self.assertEqual(states["v1alpha1"], "凍結")
        self.assertTrue(set(states.values()) <= {"草案", "公開", "凍結"})

    def test_rejections(self):
        cases = {
            "unknown state": {"readme": self.README.replace("| 草案 |", "| 未公開 |")},
            "frozen in active table": {"readme": self.README.replace("| 草案 |", "| 凍結 |")},
            "draft in frozen table": {"readme": self.README.replace("| 凍結。内容を変えない |", "| 草案 |")},
            "missing state column": {"readme": self.README.replace(" | 状態 |\n|---|---|---|\n| [common", " |\n|---|---|\n| [common")
                                     .replace(" | 草案 |", " |").replace(" | 公開 |", " |")},
            "listed twice": {"readme": self.README.replace("[v1alpha2](v1alpha2/01.md) | 版パッケージ | 公開",
                                                           "[v1alpha1](v1alpha1/01.md) | 版パッケージ | 公開"),
                             "folders": ("common/v1alpha1", "v1alpha1")},
            "row shorter than header": {"readme": self.README.replace("| [v1alpha2](v1alpha2/01.md) | 版パッケージ | 公開 |",
                                                                      "| [v1alpha2](v1alpha2/01.md) | 公開 |")},
            "missing section": {"readme": self.README.replace("## 凍結した版", "## 古い版")},
            "section without table": {"readme": self.README.split("## 凍結した版")[0] + "## 凍結した版\n\nなし。\n",
                                      "folders": ("common/v1alpha1", "v1alpha2")},
            "directory not listed": {"folders": self.FOLDERS + ("loj-history/v1alpha1",)},
            "listed directory missing": {"folders": ("common/v1alpha1", "v1alpha1")},
        }
        for label, change in cases.items():
            with self.subTest(label), self.assertRaises(ValueError):
                self.run_check(**change)


class OwnResultTests(unittest.TestCase):
    """CONF-01: the expected result lists the case's own check (and category) once."""

    CASE = {"check": "L4", "category": "relationConsistency"}

    @staticmethod
    def result(category, value="pass"):
        return {"check": "L4", "category": category, "result": value}

    def test_own_result_with_others_passes(self):
        expected = {"results": [self.result("relationResolution"), self.result("relationConsistency")]}
        self.assertTrue(v.own_result_listed(self.CASE, expected))

    def test_missing_or_duplicated_own_result_rejected(self):
        for results in ([], [self.result("relationResolution")],
                        [self.result("relationConsistency"), self.result("relationConsistency", "fail")]):
            with self.subTest(results=results):
                self.assertFalse(v.own_result_listed(self.CASE, {"results": results}))

    def test_checks_match_index_schema(self):
        schema = json.loads((v.ROOT / "schemas/common/v1alpha1/conformance.schema.json").read_text(encoding="utf-8"))
        checks = set()

        def walk(node):
            if isinstance(node, dict):
                enum = node.get("properties", {}).get("check", {}).get("enum")
                if enum:
                    checks.update(enum)
                for value in node.values():
                    walk(value)
            elif isinstance(node, list):
                for value in node:
                    walk(value)

        walk(schema)
        self.assertEqual(checks, set(v.OWN_RESULT_CHECKS) | {"L0", "L1", "L2", "reference"})

    def test_every_listed_check_requires_its_result(self):
        for check in v.OWN_RESULT_CHECKS:
            with self.subTest(check=check):
                case = {"check": check}
                self.assertFalse(v.own_result_listed(case, {"results": []}))
                self.assertTrue(v.own_result_listed(case, {"results": [{"check": check, "result": "pass"}]}))

    def test_category_must_match_absence(self):
        case = {"check": "change"}
        stray = {"check": "change", "category": "historyStructure", "result": "pass"}
        self.assertFalse(v.own_result_listed(case, {"results": [stray]}))

    def test_package_and_reference_cases_exempt(self):
        for check in ("L0", "L1", "L2", "reference"):
            with self.subTest(check=check):
                self.assertTrue(v.own_result_listed({"check": check}, {}))


class CompatibilityIdeographTests(unittest.TestCase):
    """GLYPH-11 lists the code points in the compatibility blocks that have no canonical decomposition.

    VAL-08 fixes Unicode 15.1, but this test reads the running Python's unicodedata (13.0 on 3.9,
    15.0 on 3.12). No character was added to or changed in these blocks after Unicode 6.1, so any of
    those versions gives the same answer; the version actually used is in the failure message.
    """

    def test_listed_characters_match_unicode_data(self):
        blocks = list(range(0xF900, 0xFB00)) + list(range(0x2F800, 0x2FA20))
        expected = {c for c in blocks
                    if unicodedata.name(chr(c), None) and not unicodedata.decomposition(chr(c))}
        text = (v.ROOT / "spec/loj-glyphs/v1alpha1/01-glyphs.md").read_text(encoding="utf-8")
        sentence = text[text.index("12字は、"):].split("である。")[0]
        listed = {int(h, 16) for h in re.findall(r"U\+([0-9A-F]{4,6})", sentence)}
        self.assertEqual(len(listed), 12)
        self.assertEqual(listed, expected, "unicodedata " + unicodedata.unidata_version)


class RestatementTests(unittest.TestCase):
    """DDR-022: a requirement word next to another requirement's ID is reported as a warning."""

    TEXTS = {
        "a.md": "# A\n\n## AAA-01 正\n\n- 項は表示番号を置いてはならない（MUST NOT）。\n\n"
                "## AAA-02 要約\n\n- 項は表示番号を置かない（[AAA-01](a.md)）。\n"
                "- 項は表示番号を置いてはならない（MUST NOT。AAA-01）。\n"
                "- 別の規則がある（MAY）。番号はAAA-01による。\n"
                "- 自身の番号AAA-02を引く（MUST）。未知のZZZ-09を引く（MUST）。\n\n"
                "## 要件の外\n\n- AAA-01を引く（MUST）。\n",
    }

    def test_restatement_reported(self):
        found = v.restated_requirement_words(self.TEXTS)
        self.assertEqual(found, [("a.md", 10, "AAA-02", ["AAA-01"])])

    def test_parenthesized_period_stays_in_sentence(self):
        text = {"b.md": "## BBB-01 x\n\nx\n\n## BBB-02 y\n\n- 写さない（MUST NOT。BBB-01）。次の文。\n"}
        self.assertEqual(v.restated_requirement_words(text), [("b.md", 7, "BBB-02", ["BBB-01"])])

    def test_sentence_split_by_parenthesis_depth(self):
        self.assertEqual(v.sentences("甲（乙。丙）。丁。"), ["甲（乙。丙）。", "丁。"])
        # An unpaired ） does not join the following sentences.
        self.assertEqual(v.sentences("甲）。乙（MUST）。丙"), ["甲）。", "乙（MUST）。", "丙"])

    def test_requirement_word_boundary(self):
        self.assertTrue(v.REQUIREMENT_WORD.search("要求の語（MUST等）"))
        self.assertFalse(v.REQUIREMENT_WORD.search("MUSTARD、MAYBE、XMAY"))

    def test_addressee_table_ids(self):
        text = ("## 要件の名宛人と確かめ方\n\n| 要件 | 対象 |\n|---|---|\n"
                "| CHAR-02〜CHAR-04 | 全体 |\n| VAL-01、VAL-06 | 定義 |\n| REB-01〜08 | x |\n\n## 次\n\n| CORE-09 | y |\n")
        expected = {"CHAR-02", "CHAR-03", "CHAR-04", "VAL-01", "VAL-06"} | {"REB-%02d" % n for n in range(1, 9)}
        self.assertEqual(v.addressee_table_ids(text), expected)
        with self.assertRaises(ValueError):
            v.addressee_table_ids("## 別の節\n")

    def test_addressee_mismatch_rejected(self):
        v.compare_addressees({"AAA-01"}, {"AAA-01"})
        with self.assertRaisesRegex(ValueError, "missing AAA-02; unknown $"):
            v.compare_addressees({"AAA-01"}, {"AAA-01", "AAA-02"})
        with self.assertRaisesRegex(ValueError, "missing ; unknown ZZZ-01"):
            v.compare_addressees({"AAA-01", "ZZZ-01"}, {"AAA-01"})

    def test_repository_addressee_table(self):
        self.assertGreater(v.check_addressees(), 100)

    def test_repository_check_runs(self):
        for name, number, own, cited in v.check_restatements():
            self.assertNotIn(own, cited)
            self.assertFalse(name.startswith("spec/v1alpha1/"), name)


class SchemaMarkTests(unittest.TestCase):
    """CONF-01: rejectedBy: schema matches whether an input YAML file breaks its schema."""

    @classmethod
    def setUpClass(cls):
        cls.validators = v.all_schemas()
        cls.good = v.ROOT / "conformance/loj-history/v1alpha1/valid/hist-001/repo"
        cls.bad = v.ROOT / "conformance/loj-history/v1alpha1/invalid/hist-005/repo"

    def test_marked_case_needs_schema_failure(self):
        marked = {"rejectedBy": "schema"}
        self.assertGreater(v.check_schema_mark("x", marked, [self.bad], self.validators), 0)
        with self.assertRaisesRegex(ValueError, "marked rejectedBy: schema"):
            v.check_schema_mark("x", marked, [self.good], self.validators)

    def test_unmarked_case_must_fit_schema(self):
        self.assertGreater(v.check_schema_mark("x", {}, [self.good], self.validators), 0)
        with self.assertRaisesRegex(ValueError, "without rejectedBy: schema"):
            v.check_schema_mark("x", {}, [self.bad], self.validators)

    def test_unknown_schema_version_counts_as_failure(self):
        with tempfile.TemporaryDirectory() as folder:
            base = Path(folder)
            (base / "good.yaml").write_bytes((self.good / "history.yaml").read_bytes())
            (base / "bare.yaml").write_bytes(b"record: x\n")
            count, failures = v.schema_failures(base, self.validators)
            self.assertEqual(count, 2)
            self.assertEqual([path.name for path, _ in failures], ["bare.yaml"])
            self.assertIn("unknown schemaVersion", failures[0][1])
            self.assertGreater(v.check_schema_mark("x", {"rejectedBy": "schema"}, [base], self.validators), 0)

    def test_index_schema_limits_mark(self):
        index = v.read_json(v.ROOT / "conformance/loj-history/v1alpha1/manifest.json")
        validator = self.validators["common/v1alpha1/conformance.schema.json"]
        validator.validate(index)
        positive = copy.deepcopy(index)
        positive["cases"][0]["rejectedBy"] = "schema"
        self.assertFalse(validator.is_valid(positive))
        package = copy.deepcopy(index)
        case = next(c for c in package["cases"] if c.get("rejectedBy"))
        case["input"] = {"kind": "package", "path": "x/law.yaml"}
        self.assertFalse(validator.is_valid(package))


class DiagnosticLocationTests(unittest.TestCase):
    """CONF-01/SRC-01: the shape of expected diagnostic locations (not which line a rule points at)."""

    def setUp(self):
        self.path = v.ROOT / "conformance/v1alpha2/invalid/pkg-146/law.yaml"
        self.man = v.load_yaml(self.path.read_text(encoding="utf-8"))

    def at(self, start, end, path="main.md"):
        return v.location_problem(self.path, self.man, {"path": path, "start": start, "end": end})

    def test_whole_line_with_crlf_passes(self):
        self.assertIsNone(self.at(139, 160))
        self.assertIsNone(self.at(0, 13))

    def test_whole_manifest_passes(self):
        self.assertIsNone(self.at(0, self.path.stat().st_size, "law.yaml"))

    def test_partial_or_multiple_lines_rejected(self):
        for start, end, reason in [(139, 159, "boundaries"), (139, 158, "boundaries"), (140, 160, "boundaries"),
                                   (106, 160, "more than one line"), (160, 160, "out of range"), (0, 999, "out of range")]:
            with self.subTest(start=start, end=end):
                self.assertIn(reason, self.at(start, end))

    def test_unknown_path_rejected(self):
        self.assertIn("unknown path", self.at(0, 13, "other.md"))

    def test_expected_schema_requires_full_location(self):
        validator = v.all_schemas()["common/v1alpha1/expected.schema.json"]
        diagnostic = {"rule": "DISP-01", "schemaVersion": "loj/v1alpha2", "class": "error",
                      "location": {"path": "main.md", "start": 139, "end": 160}}
        self.assertTrue(validator.is_valid({"diagnostics": [diagnostic]}))
        for drop in ("path", "start", "end"):
            broken = copy.deepcopy(diagnostic)
            del broken["location"][drop]
            with self.subTest(drop=drop):
                self.assertFalse(validator.is_valid({"diagnostics": [broken]}))
        extra = copy.deepcopy(diagnostic)
        extra["location"]["line"] = 6
        self.assertFalse(validator.is_valid({"diagnostics": [extra]}))


class DerivationTests(unittest.TestCase):
    """CONF-01: a copied input listed in derivedFrom is its source with the listed edits, byte for byte."""

    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        base = Path(self.folder.name)
        self.source, self.copy = base / "source", base / "copy"
        for folder, body in ((self.source, b"a: 1\r\nb: 2\r\n"), (self.copy, b"a: 1\r\nb: 3\r\n")):
            (folder / "sub").mkdir(parents=True)
            (folder / "sub/data.yaml").write_bytes(body)
            (folder / "same.md").write_bytes("雲\n".encode("utf-8"))
        self.entry = {"path": self.copy.as_posix(), "from": self.source.as_posix(),
                      "edits": [{"file": "sub/data.yaml", "old": "b: 2", "new": "b: 3"}]}

    def tearDown(self):
        self.folder.cleanup()

    def test_matching_copy_passes(self):
        self.assertIsNone(v.derivation_problem(self.entry))
        (self.copy / "new.yaml").write_bytes(b"c: 4\n")
        entry = dict(self.entry, edits=self.entry["edits"] + [{"file": "new.yaml", "content": "c: 4\n"}])
        self.assertIsNone(v.derivation_problem(entry))

    def test_changed_source_rejected(self):
        # The source was edited after the copy was made, and the copy was not made again.
        (self.source / "same.md").write_bytes("雲。\n".encode("utf-8"))
        self.assertIn("content differs", v.derivation_problem(self.entry))

    def test_unlisted_change_or_file_rejected(self):
        self.assertIn("content differs", v.derivation_problem(dict(self.entry, edits=[])))
        (self.copy / "extra.yaml").write_bytes(b"x: 1\n")
        self.assertIn("file set differs", v.derivation_problem(self.entry))

    def test_missing_old_text_rejected(self):
        for file, old in (("sub/data.yaml", "b: 9"), ("none.yaml", "b: 2")):
            entry = dict(self.entry, edits=[{"file": file, "old": old, "new": "b: 3"}])
            with self.subTest(file=file):
                self.assertIn("old text not found", v.derivation_problem(entry))

    def test_line_endings_compared_as_bytes(self):
        (self.copy / "sub/data.yaml").write_bytes(b"a: 1\nb: 3\n")
        self.assertIn("content differs", v.derivation_problem(self.entry))

    def test_file_source(self):
        source, target = (self.source / "same.md").as_posix(), (self.copy / "same.md").as_posix()
        self.assertIsNone(v.derivation_problem({"path": target, "from": source, "edits": []}))
        edits = [{"file": "", "old": "雲", "new": "雨"}]
        self.assertIn("edits on a file", v.derivation_problem({"path": target, "from": source, "edits": edits}))
        self.assertIn("missing source", v.derivation_problem({"path": target, "from": "none.md", "edits": []}))

    def test_path_must_be_own_input(self):
        index = v.read_json(v.ROOT / "conformance/loj-glyphs/v1alpha1/manifest.json")
        case = copy.deepcopy(next(c for c in index["cases"] if c["id"] == "glyph-002"))
        self.assertEqual(v.check_derivations("glyph-002", case), 1)
        # The shared positive is an input of other cases too, not a copy owned by this case.
        case["derivedFrom"][0]["path"] = "conformance/loj-history/v1alpha1/valid/hist-001/repo"
        with self.assertRaisesRegex(ValueError, "not an own input"):
            v.check_derivations("glyph-002", case)

    def test_duplicate_or_broken_entry_rejected(self):
        index = v.read_json(v.ROOT / "conformance/loj-glyphs/v1alpha1/manifest.json")
        case = copy.deepcopy(next(c for c in index["cases"] if c["id"] == "glyph-002"))
        twice = copy.deepcopy(case)
        twice["derivedFrom"].append(copy.deepcopy(case["derivedFrom"][0]))
        with self.assertRaisesRegex(ValueError, "not an own input"):
            v.check_derivations("glyph-002", twice)
        case["derivedFrom"][0]["edits"] = []
        with self.assertRaisesRegex(ValueError, "content differs"):
            v.check_derivations("glyph-002", case)

    def test_dot_segments_rejected(self):
        for key, value in (("from", "conformance/../../x"), ("path", "./copy"), ("file", "../x.yaml")):
            entry = copy.deepcopy(self.entry)
            if key == "file":
                entry["edits"][0]["file"] = value
            else:
                entry[key] = value
            with self.subTest(key=key):
                self.assertIn(". or .. segment", v.derivation_problem(entry))
        validator = v.all_schemas()["common/v1alpha1/conformance.schema.json"]
        index = v.read_json(v.ROOT / "conformance/loj-glyphs/v1alpha1/manifest.json")
        self.assertTrue(validator.is_valid(index))
        case = next(c for c in index["cases"] if "derivedFrom" in c)
        for value in ("../x", "a/../x", "a/./x", ".", "a/.."):
            case["derivedFrom"][0]["from"] = value
            with self.subTest(value=value):
                self.assertFalse(validator.is_valid(index))
        case["derivedFrom"][0]["from"] = "a/.hidden/x..y"
        self.assertTrue(validator.is_valid(index))

    def test_repository_copies_match(self):
        count = 0
        for folder, _ in v.SUITES.values():
            index = v.read_json(v.ROOT / "conformance" / folder / "manifest.json")
            count += sum(v.check_derivations(case["id"], case) for case in index["cases"])
        self.assertGreater(count, 0)


if __name__ == "__main__":
    unittest.main()

