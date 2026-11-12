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


if __name__ == "__main__":
    unittest.main()

