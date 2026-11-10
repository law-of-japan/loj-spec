"""Mutation/regression checks for the artifact auditor, not L1 conformance tests."""
import copy
import sys
import tempfile
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


if __name__ == "__main__":
    unittest.main()
