"""Port the hand-authored v1alpha1 conformance cases to loj/v1alpha2.

Authoring helper (O-15, §16.5 of the integration proposal). It rewrites the
hand-authored v1alpha1 inputs and expected trees mechanically; it never runs a
parser or validator. CI reads the checked-in JSON; it does not run this script.

Changes applied:
- case IDs T001..T106 become pkg-001..pkg-106;
- law.yaml schemaVersion loj/v1alpha1 becomes loj/v1alpha2 (other values stay);
- expected AST: schemaVersion loj/v1alpha2, and numbering "explicit" on every Paragraph;
- expected diagnostics gain schemaVersion "loj/v1alpha2" and class "error".
"""
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "conformance/v1alpha1"
DST = ROOT / "conformance/v1alpha2"


def new_id(old):
    return "pkg-" + old[1:]


def port_tree(node):
    if node.get("kind") == "Paragraph":
        node["numbering"] = "explicit"
    for child in node.get("content", []):
        if isinstance(child, dict) and "kind" in child:
            port_tree(child)


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes((json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))


def port_case(case):
    ident = new_id(case["id"])
    old_dir = ROOT / Path(case["input"]).parent
    group = "valid" if case["success"] else "invalid"
    new_dir = DST / group / ident
    if new_dir.exists():
        shutil.rmtree(new_dir)
    shutil.copytree(old_dir, new_dir)
    law = new_dir / "law.yaml"
    raw = law.read_bytes()
    for old, new in [(b'"schemaVersion": "loj/v1alpha1"', b'"schemaVersion": "loj/v1alpha2"'),
                     (b"schemaVersion: loj/v1alpha1", b"schemaVersion: loj/v1alpha2")]:
        raw = raw.replace(old, new)
    law.write_bytes(raw)
    expected = json.loads((ROOT / case["expected"]).read_text(encoding="utf-8"))
    if "ast" in expected:
        expected["ast"]["schemaVersion"] = "loj/v1alpha2"
        port_tree(expected["ast"]["root"])
    if "diagnostics" in expected:
        expected["diagnostics"] = [{"rule": d["rule"], "schemaVersion": "loj/v1alpha2", "class": "error"}
                                   for d in expected["diagnostics"]]
    exp_path = "conformance/v1alpha2/expected/" + ident + ".json"
    write_json(ROOT / exp_path, expected)
    return {"id": ident, "title": case["title"], "requirements": case["requirements"], "check": case["level"],
            "normative": case["normative"],
            "input": {"kind": "package", "path": (new_dir / "law.yaml").relative_to(ROOT).as_posix()},
            "expected": exp_path, "success": case["success"]}


def main():
    index = json.loads((SRC / "manifest.json").read_text(encoding="utf-8"))
    cases = [port_case(case) for case in index["cases"]]
    write_json(DST / "manifest.json", {"suite": "loj/v1alpha2", "cases": cases})
    print(f"Ported {len(cases)} hand-authored v1alpha1 cases; no parser invoked.")


if __name__ == "__main__":
    main()
