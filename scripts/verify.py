"""Audit specification artifacts; NOT a general loj L1 validator.

Positive source traces are compared with independently authored expected trees.
Negative L1 fixture semantics require a future implementation adapter/review.
"""
import json
import re
import unicodedata
from pathlib import Path
from urllib.parse import unquote, urlsplit

import yaml
from jsonschema import Draft202012Validator, FormatChecker
from markdown_it import MarkdownIt
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[1]
MD = MarkdownIt("commonmark")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_json(path):
    def pairs(values):
        result = {}
        for key, value in values:
            require(key not in result, "Duplicate JSON key: " + key)
            result[key] = value
        return result
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=pairs)


def load_yaml(raw):
    """A deliberately restricted YAML 1.2 JSON-data-model loader, not PyYAML 1.1 resolution."""
    for token in yaml.scan(raw):
        require(not isinstance(token, (yaml.tokens.AliasToken, yaml.tokens.AnchorToken,
                                       yaml.tokens.TagToken, yaml.tokens.DirectiveToken)), "MAN-01: YAML extension")
    root = yaml.compose(raw, Loader=yaml.BaseLoader)

    def convert(node):
        if isinstance(node, yaml.MappingNode):
            result = {}
            for key, value in node.value:
                require(isinstance(key, yaml.ScalarNode), "MAN-01: non-string key")
                require(key.value not in result and key.value != "<<", "MAN-01: duplicate/merge key")
                result[key.value] = convert(value)
            return result
        if isinstance(node, yaml.SequenceNode):
            return [convert(value) for value in node.value]
        require(isinstance(node, yaml.ScalarNode), "MAN-01: empty document")
        value = node.value
        if node.style is None:
            require(not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value), "MAN-01: quote dates")
            if value in ("true", "false", "null") or re.fullmatch(r"-?(0|[1-9][0-9]*)(\.[0-9]+)?([eE][+-]?[0-9]+)?", value):
                return json.loads(value)
        return value
    return convert(root)


def check_bytes(raw):
    text = raw.decode("utf-8", errors="strict")
    require(bool(raw) and not raw.startswith(b"\xef\xbb\xbf") and "\x00" not in text,
            "BASIC-02: empty/BOM/NUL")
    require("\r" not in text.replace("\r\n", ""), "BASIC-02: bare CR")
    return text


def path_ok(path):
    if not re.fullmatch(r"(?:[A-Za-z0-9_.-]+/)*[A-Za-z0-9_.-]+\.md", path):
        return False
    reserved = re.compile(r"^(con|prn|aux|nul|com[1-9]|lpt[1-9])(?:\.|$)", re.I)
    return all(part not in (".", "..") and not part.endswith(".") and not reserved.match(part)
               for part in path.split("/"))


def inspect_manifest(path, validator, version="loj/v1alpha1"):
    try:
        text = check_bytes(path.read_bytes())
    except (ValueError, UnicodeError):
        return ["BASIC-02"], None
    try:
        man = load_yaml(text)
    except (ValueError, yaml.YAMLError):
        return ["MAN-01"], None
    if isinstance(man, dict) and man.get("schemaVersion") != version:
        return ["BASIC-01"], man
    if list(validator.iter_errors(man)):
        return ["MAN-01"], man
    issues, seen, inodes, parents = [], set(), set(), []
    declared = ["main"]
    for field, prefix in [("supplements", "supplement/"), ("appendices", "appendix/")]:
        keys = [value["key"] for value in man.get(field, [])]
        if len(keys) != len(set(keys)):
            issues.append("MAN-03")
        declared += [prefix + key for key in keys]
    for doc in man["documents"]:
        name = doc["path"]
        if not path_ok(name) or name.lower() in seen:
            issues.append("MAN-02")
            continue
        seen.add(name.lower())
        target = path.parent / name
        # Check each component for both POSIX symlinks and Windows reparse points.
        current = path.parent
        bad = False
        for part in name.split("/"):
            current = current / part
            if current.exists() or current.is_symlink():
                stat = current.lstat()
                bad |= current.is_symlink() or bool(getattr(stat, "st_file_attributes", 0) & 0x400)
        if bad or not target.is_file() or path.parent.resolve() not in target.resolve().parents:
            issues.append("MAN-02")
            continue
        stat = target.stat()
        inode = (stat.st_dev, stat.st_ino)
        if inode in inodes:
            issues.append("MAN-02")
        inodes.add(inode)
        try:
            check_bytes(target.read_bytes())
        except (UnicodeError, ValueError):
            issues.append("BASIC-02")
        if not parents or parents[-1] != doc["parent"]:
            parents.append(doc["parent"])
    if parents != declared:
        issues.append("MAN-03")
    return issues, man


RANK = {"Part": 1, "Chapter": 2, "Section": 3, "Subsection": 4, "Division": 5, "Article": 6}
TEXT_KINDS = {"Paragraph", "Item", "Subitem", "AppendedMaterial"}
TEXT_KINDS_V2 = TEXT_KINDS | {"Cell", "Preamble", "EnactStatement", "Toc"}
CONTAINERS_V2 = {"paragraph": "Paragraph", "item": "Item", "subitem": "Subitem", "table": "Table", "row": "Row",
                 "cell": "Cell", "preamble": "Preamble", "enact-statement": "EnactStatement", "toc": "Toc"}
# DISP-01: iroha subitem display numbers, valued by their position in this sequence (1..47).
IROHA = "イロハニホヘトチリヌルヲワカヨタレソツネナラムウヰノオクヤマケフコエテアサキユメミシヱヒモセス"


def japanese(value):
    digits = "一二三四五六七八九"
    result = ""
    for unit, glyph in [(1000, "千"), (100, "百"), (10, "十"), (1, "")]:
        digit, value = divmod(value, unit)
        if digit:
            result += ("" if digit == 1 and unit > 1 else digits[digit - 1]) + glyph
    return result


JAPANESE = {japanese(value): str(value) for value in range(1, 10000)}


def subitem_display_kind(value):
    """DISP-01 (v1alpha2): kind of an iroha or parenthesized subitem display number, else None."""
    if len(value) == 1 and value in IROHA:
        return "iroha"
    if re.fullmatch(r"（[1-9][0-9]{0,3}）", value):
        return "parenAscii"
    if re.fullmatch(r"（[１-９][０-９]{0,3}）", value):
        return "parenFullwidth"
    return None


def normalized_display(value, kind, v2=False):
    if v2 and kind == "Subitem":
        display_kind = subitem_display_kind(value)
        if display_kind == "iroha":
            return str(IROHA.index(value) + 1)
        if display_kind:
            return str(int(value[1:-1]))
    parts = []
    for part in re.split("[のノ]" if v2 else "の", value):
        if re.fullmatch(r"[1-9][0-9]{0,3}", part):
            parts.append(part)
        elif kind != "Subitem" and re.fullmatch(r"[１-９][０-９]{0,3}", part):
            parts.append(str(int(part)))
        elif kind not in ("Paragraph", "Subitem") and part in JAPANESE:
            parts.append(JAPANESE[part])
        else:
            raise ValueError("Invalid display number: " + value)
    return "-".join(parts)


def caption_balanced(value):
    """HEAD-01 (v1alpha2): the opening "（" pairs with the final "）" and every parenthesis nests."""
    depth = 0
    for i, char in enumerate(value):
        depth += {"（": 1, "）": -1}.get(char, 0)
        if depth < 0 or depth == 0 and i < len(value) - 1:
            return False
    return depth == 0 and len(value) > 2


def nodes(node):
    yield node
    for child in node["content"]:
        if "kind" in child:
            yield from nodes(child)


def check_tree(ast, man, v2=False):
    require(ast["law"] == man["law"], "AST metadata differs from Manifest")
    seen = set()
    lid = ast["law"]["id"]
    scopes = [("MainProvision", lid + "/main")]
    scopes += [("SupplementaryProvision", lid + "/supplement/" + x["key"]) for x in man.get("supplements", [])]
    scopes += [("AppendedMaterial", lid + "/appendix/" + x["key"]) for x in man.get("appendices", [])]
    root = ast["root"]
    require(root["kind"] == "Law" and root["id"] == lid and root["display"] == ast["law"]["title"], "Bad root")
    top = [(c.get("kind"), c.get("id")) for c in root["content"]]
    if v2:
        lead = [x for x in [("EnactStatement", lid + "/enact-statement"), ("Toc", lid + "/toc"),
                            ("Preamble", lid + "/preamble")] if x in top]
        scopes = lead + scopes
    require(top == scopes, "Scope order")
    text_kinds = TEXT_KINDS_V2 if v2 else TEXT_KINDS

    def visit(node, parent=None, scope=None):
        kind, ident = node["kind"], node["id"]
        require(ident not in seen, "Duplicate ID: " + ident)
        seen.add(ident)
        if kind in ("MainProvision", "SupplementaryProvision", "AppendedMaterial"):
            scope = ident
        elif kind in ("EnactStatement", "Preamble", "Toc"):
            require(node["number"] is None and node["display"] == "", "Preamble/enact/toc fields")
        elif kind == "Row":
            require(ident == parent["id"] + "/row/" + node["key"] and node["number"] is None, "Row ID: " + ident)
        elif kind == "Cell":
            position = str([c["id"] for c in parent["content"] if "kind" in c].index(ident) + 1)
            require(node["number"] == position and ident == parent["id"] + "/cell/" + position, "Cell ID: " + ident)
        elif parent:
            prefix = scope if kind == "Article" else parent["id"]
            level = str(node["level"]) + "/" if kind == "Subitem" else ""
            require(ident == prefix + "/" + kind.lower() + "/" + level + node["number"], "ID derivation: " + ident)
        content = node["content"]
        children = [c for c in content if "kind" in c]
        texts = [c["text"] for c in content if "text" in c]
        require(not texts or kind in text_kinds, "Text in structural parent")
        require(all(not ("text" in x and "text" in y) for x, y in zip(content, content[1:])), "Adjacent text")
        if kind in text_kinds:
            require(bool("".join(texts).strip()), "Empty body")
        if kind in ("Cell", "Preamble", "EnactStatement", "Toc"):
            require(not children and len(texts) == 1, "Text-only container")
        if kind in ("Table", "Row"):
            require(bool(children) and all(c["kind"] == ("Row" if kind == "Table" else "Cell") for c in children),
                    "Table rows/cells")
            require(node["display"] == "", "Table display")
        if kind in RANK and kind != "Article" or kind in ("MainProvision", "SupplementaryProvision"):
            require(bool(children), "Empty structural container")
        child_kinds = [c["kind"] for c in children]
        if kind in RANK and kind != "Article":
            require(all(RANK.get(k, 0) > RANK[kind] for k in child_kinds), "Rank constraint")
        elif kind == "MainProvision":
            require(all(k in RANK for k in child_kinds), "Main children")
        elif kind == "SupplementaryProvision":
            require(all(k in RANK for k in child_kinds) or all(k == "Paragraph" for k in child_kinds), "Supplement mode")
            require(bool(re.fullmatch("附\u3000*則", node["display"])) if v2 else node["display"] == "附則",
                    "Supplement label")
        elif kind == "Article":
            require((node["status"] == "deleted" and not content) or
                    (node["status"] == "active" and bool(children) and all(k == "Paragraph" for k in child_kinds)), "Article children")
        elif kind == "Paragraph":
            require(all(k == "Item" or v2 and k == "Table" for k in child_kinds), "Paragraph children")
        elif kind in ("Item", "Subitem"):
            next_level = 1 if kind == "Item" else node["level"] + 1
            require(all(c["kind"] == "Subitem" and c["level"] == next_level or v2 and c["kind"] == "Table"
                        for c in children), "Subitem children")
            if v2:
                kinds = {subitem_display_kind(c["display"]) or "decimal" for c in children if c["kind"] == "Subitem"}
                require(len(kinds) <= 1, "Sibling subitem displays mix character kinds (DISP-01): " + ident)
        elif kind == "AppendedMaterial":
            require(not children, "Opaque appendix children")
        if kind == "MainProvision":
            require(node["display"] == "", "Main display")
        if kind in RANK:
            unit = {"Part": "編", "Chapter": "章", "Section": "節", "Subsection": "款", "Division": "目", "Article": "条"}[kind]
            if v2 and kind == "Article":
                unit = "[条條]"
            sep = "[のノ]" if v2 else "の"
            tail = r"(（[^\r\n]+）)?" if kind == "Article" else r"[ 　][^\r\n]+"
            match = re.fullmatch("第(.+?)" + unit + r"((?:" + sep + r"[^ 　（）]+)*)" + tail, node["display"])
            require(bool(match), "Invalid heading display")
            if kind == "Article" and match[3]:
                if v2:
                    require(caption_balanced(match[3]),
                            "Article caption: the opening parenthesis must pair with the final one, all nested")
                else:
                    require(bool(re.fullmatch(r"（[^（）]+）", match[3])), "Article caption: no parentheses inside (v1alpha1)")
            require(normalized_display(match[1] + match[2], kind, v2) == node["number"], "Heading number mismatch")
        if kind == "Paragraph" and v2:
            require(node["numbering"] in ("explicit", "implicit"), "Paragraph numbering")
        if kind == "Table":
            require(ident == parent["id"] + "/table/" + node["number"], "Table ID: " + ident)
        if kind in ("Paragraph", "Item", "Subitem"):
            first = texts[0].lstrip("\r\n")
            if "caption" in node:
                # PARA-02: the caption line is the first nonblank line of the text; the display is checked on the next one.
                line, _, rest = first.partition("\n")
                require(line.rstrip("\r") == node["caption"] and caption_balanced(node["caption"]),
                        "Paragraph caption must be the balanced first line of the text (PARA-02): " + ident)
                first = rest.lstrip("\r\n")
                require(first.strip() != "", "Paragraph caption needs a body line before any child (PARA-02): " + ident)
            if node.get("numbering") == "implicit":
                require(node["display"] == "", "Implicit paragraph display")
            elif node["display"]:
                require(first.startswith(node["display"] + " ") or first.startswith(node["display"] + "　"), "Display/body differs")
                require(normalized_display(node["display"], kind, v2) == node["number"], "Display number mismatch")
            else:
                require(kind == "Paragraph" and node["number"] == "1", "Required display")
        for child in children:
            visit(child, node, scope)
    visit(root)
    return seen


def marker_attrs(kind, node):
    """Attributes a v1alpha2 marker carries for this node (defaults omitted)."""
    attrs = {}
    if kind in ("Paragraph", "Item", "Subitem", "Table"):
        attrs["number"] = node["number"]
    if kind == "Subitem":
        attrs["level"] = str(node["level"])
    if kind == "Paragraph" and node["numbering"] == "implicit":
        attrs["numbering"] = "implicit"
    if kind == "Paragraph" and "caption" in node:
        attrs["caption"] = "present"
    if kind == "Row":
        attrs["key"] = node["key"]
    for span in ("rowspan", "colspan"):
        if span in node:
            attrs[span] = str(node[span])
    return attrs


def expected_trace(node, v2=False):
    """Linear observations of a hand-authored tree, not an inferred AST."""
    result = []
    kind = node["kind"]
    names = {v: k for k, v in CONTAINERS_V2.items()}
    if kind in RANK or kind in ("SupplementaryProvision", "AppendedMaterial"):
        result.append(("heading", node["display"], node["id"]))
    if v2 and kind in names:
        result.append(("open", (names[kind], marker_attrs(kind, node)), node["id"]))
    elif kind in ("Paragraph", "Item", "Subitem"):
        result.append(("open", (kind.lower(), node["number"], node.get("level")), node["id"]))
    if node.get("status") == "deleted":
        result.append(("deleted", "削除", node["id"]))
    for child in node["content"]:
        if "text" in child:
            result.append(("text", child["text"], None))
        else:
            result += expected_trace(child, v2)
    if v2 and kind in names:
        result.append(("close", names[kind], node["id"]))
    elif kind in ("Paragraph", "Item", "Subitem"):
        result.append(("close", kind.lower(), node["id"]))
    return result


def source_trace(path, man, v2=False):
    """Bounded positive-fixture audit. Does not diagnose arbitrary invalid L1 input."""
    trace, spans, open_stack = [], [], []
    seen_scopes = set()
    for doc in man["documents"]:
        raw = (path.parent / doc["path"]).read_bytes()
        text = raw.decode("utf-8")
        lines = text.splitlines(keepends=True)
        offsets, at = [], 0
        for line in lines:
            offsets.append(at)
            at += len(line.encode("utf-8"))
        protected, depth = set(), 0
        for token in MD.parse(text):
            if token.type in ("blockquote_open", "bullet_list_open", "ordered_list_open"):
                if token.map:
                    protected.update(range(*token.map))
            if token.type in ("fence", "code_block"):
                protected.update(range(*token.map))
            if token.type == "html_block" and not re.match(r"<!--\s*loj:", token.content, re.I):
                protected.update(range(*token.map))
        appendix = doc["parent"].startswith("appendix/")
        first_scope = doc["parent"] not in seen_scopes
        seen_scopes.add(doc["parent"])
        for i, line in enumerate(lines):
            clean = line.rstrip("\r\n")
            span = {"path": doc["path"], "start": offsets[i], "end": offsets[i] + len(line.encode("utf-8"))}
            heading = re.fullmatch(r"#{1,6} (.+)", clean) if i not in protected else None
            names = "|".join(CONTAINERS_V2) if v2 else "paragraph|item|subitem"
            marker = re.fullmatch(r"<!-- loj:(" + names + r")((?: [^ ]+)*) -->", clean) if i not in protected else None
            close = re.fullmatch(r"<!-- loj:end-(" + names + r") -->", clean) if i not in protected else None
            if appendix and not (first_scope and i == 0):
                heading = marker = close = None
            if heading:
                trace.append(("heading", heading[1])); spans.append(span)
            elif marker:
                attrs = dict(pair.split("=", 1) for pair in marker[2].split(" ") if pair)
                if v2:
                    trace.append(("open", (marker[1], attrs)))
                else:
                    trace.append(("open", (marker[1], attrs["number"], int(attrs["level"]) if "level" in attrs else None)))
                spans.append(span)
                open_stack.append(len(spans) - 1)
            elif close:
                trace.append(("close", close[1])); spans.append(span)
                require(bool(open_stack), "Positive source has extra close")
                spans[open_stack.pop()]["end"] = span["end"]
            elif clean == "削除" and not open_stack and not appendix:
                trace.append(("deleted", clean)); spans.append(span)
            elif open_stack or appendix:
                if trace and trace[-1][0] == "text":
                    trace[-1] = ("text", trace[-1][1] + line)
                else:
                    trace.append(("text", line)); spans.append(span)
            else:
                require(not clean.strip(), "Positive source has unowned body: " + clean)
        require(not open_stack, "Positive source crosses file boundary")
    return trace, spans


def check_positive(path, man, expected, v2=False):
    ids = check_tree(expected["ast"], man, v2)
    want = expected_trace(expected["ast"]["root"], v2)
    observed, spans = source_trace(path, man, v2)
    require(observed == [(k, value) for k, value, _ in want], "Source/expected trace mismatch: " + str(path))
    by_id = {ident: span for (kind, _, ident), span in zip(want, spans) if kind in ("heading", "open")}
    for position in expected.get("positions", []):
        ident = position["nodeId"]
        require(ident in ids, "Position ID missing")
        require(by_id[ident] == {k: v for k, v in position.items() if k != "nodeId"},
                "Fixed byte position mismatch: " + str(position) + "; observed " + str(by_id[ident]))
    return len(ids)


def location_problem(law_path, man, location):
    """SRC-01/CONF-01: an expected diagnostic location names a listed document, stays inside it,
    and covers one whole line (its line break included).
    Returns None when the location is well formed; does not decide which line the rule points at.
    law.yaml is never named: its violations are Manifest violations, whose location SRC-01 does not fix.
    Empty files and bare CR line breaks never reach here (BASIC-02 rejects them at L0), so start < end and LF suffice."""
    name = location["path"]
    if name == "law.yaml":
        return "law.yaml has no fixed location (SRC-01: Manifest violations)"
    if name not in [doc["path"] for doc in man["documents"]]:
        return "unknown path " + name
    raw = (law_path.parent / name).read_bytes()
    start, end = location["start"], location["end"]
    if not 0 <= start < end <= len(raw):
        return "out of range"
    if (start and raw[start - 1:start] != b"\n") or (end < len(raw) and raw[end - 1:end] != b"\n"):
        return "not at line boundaries"
    if b"\n" in raw[start:end - 1]:
        return "more than one line"
    return None


L0_PASS = {"check": "L0", "result": "pass"}


SUITES = {"loj/v1alpha2": ("v1alpha2", "pkg"), "common/v1alpha1": ("common/v1alpha1", "common"),
          "loj-history/v1alpha1": ("loj-history/v1alpha1", "hist"), "loj-glyphs/v1alpha1": ("loj-glyphs/v1alpha1", "glyph"),
          "loj-registry/v1alpha1": ("loj-registry/v1alpha1", "reg"), "loj-rebuild/v1alpha1": ("loj-rebuild/v1alpha1", "rebuild")}
KIND_SCHEMAS = {"loj/v1alpha2": "v1alpha2/manifest.schema.json", "loj-history/v1alpha1": "loj-history/v1alpha1/history.schema.json",
                "loj-glyphs/v1alpha1": "loj-glyphs/v1alpha1/glyphs.schema.json",
                "loj-registry/v1alpha1": "loj-registry/v1alpha1/record.schema.json",
                "loj-rebuild/v1alpha1": "loj-rebuild/v1alpha1/rebuild.schema.json"}


def all_schemas():
    schemas = {path.relative_to(ROOT / "schemas").as_posix(): read_json(path) for path in (ROOT / "schemas").rglob("*.json")}
    registry = Registry().with_resources((s["$id"], Resource.from_contents(s)) for s in schemas.values())
    validators = {}
    for name, value in schemas.items():
        Draft202012Validator.check_schema(value)
        validators[name] = Draft202012Validator(value, registry=registry, format_checker=FormatChecker())
    return validators


def next_rules():
    rules = set()
    for path in (ROOT / "spec").rglob("*.md"):
        if "v1alpha1" in path.relative_to(ROOT / "spec").parts[:1]:
            continue
        rules.update(re.findall(r"^## ([A-Z]+-\d+) ", path.read_text(encoding="utf-8"), re.M))
    return rules


def input_files(case):
    spec = case["input"]
    paths = [spec[key] for key in ("path", "registry", "bundle") if key in spec] + spec.get("repositories", [])
    return [ROOT / value for value in paths]


def schema_failures(folder, validators):
    """Schema-check every LoJ YAML file below a repository/registry input.

    Returns the number of files checked and, for each file that breaks the schema of its
    schemaVersion, its path and the first error message.
    """
    count, failures = 0, []
    # CORE-03: LoJ YAML files use the .yaml extension (load_yaml rejects other YAML forms).
    for path in sorted(folder.rglob("*.yaml")):
        data = load_yaml(check_bytes(path.read_bytes()))
        version = data.get("schemaVersion") if isinstance(data, dict) else None
        count += 1
        if version not in KIND_SCHEMAS:
            # A missing or unknown schemaVersion has no schema to fit, so it counts as a schema failure.
            failures.append((path, "unknown schemaVersion: " + repr(version)))
            continue
        errors = list(validators[KIND_SCHEMAS[version]].iter_errors(data))
        if errors:
            failures.append((path, errors[0].message))
    return count, failures


def check_schema_mark(ident, case, inputs, validators):
    """CONF-01: a case marked rejectedBy: schema has an input YAML file that breaks its schema;
    every input YAML file of any other case conforms to its schema. Returns the files checked."""
    count, failures = 0, []
    # Directory inputs hold the YAML files; file inputs are git bundles, whose YAML is not unpacked here.
    for path in inputs:
        if path.is_dir():
            checked, failed = schema_failures(path, validators)
            count += checked
            failures += failed
    if case.get("rejectedBy") == "schema":
        require(bool(failures), ident + " is marked rejectedBy: schema, but every input YAML file fits its schema")
    else:
        require(not failures, ident + " input fails its schema without rejectedBy: schema (" + str(len(failures))
                + " files): " + "; ".join(str(path) + ": " + message for path, message in failures))
    return count


def tree_bytes(path):
    """The files below a directory by their relative path, or a single file under the empty name.

    Only files are compared (CONF-01 compares the set of files); Git keeps no empty directories.
    Symbolic links are rejected: Git on Windows may check them out as plain files."""
    entries = [path] + (sorted(path.rglob("*")) if path.is_dir() else [])
    links = [p for p in entries if p.is_symlink()]
    require(not links, "symbolic link in a copied input or its source: " + ", ".join(map(str, links)))
    if path.is_file():
        return {"": path.read_bytes()}
    return {p.relative_to(path).as_posix(): p.read_bytes() for p in entries[1:] if p.is_file()}


def derivation_problem(entry):
    """CONF-01: applying the edits in order to a copy of from gives path, byte for byte. Returns the problem or None."""
    # The index schema's path pattern admits "." and ".." segments; a copy and its source stay inside the repository.
    for name in [entry["from"], entry["path"]] + [edit["file"] for edit in entry["edits"]]:
        if any(part in (".", "..") for part in name.split("/")):
            return "path with a . or .. segment: " + name
    source, target = ROOT / entry["from"], ROOT / entry["path"]
    if not source.exists():
        return "missing source " + entry["from"]
    if source.is_file() and entry["edits"]:
        return "edits on a file source"
    built = tree_bytes(source)
    for number, edit in enumerate(entry["edits"], 1):
        name = edit["file"]
        if "content" in edit:
            built[name] = edit["content"].encode("utf-8")
            continue
        text = built[name].decode("utf-8") if name in built else None
        if text is None or edit["old"] not in text:
            return "edit %d: old text not found in %s" % (number, name)
        built[name] = text.replace(edit["old"], edit["new"], 1).encode("utf-8")
    actual = tree_bytes(target) if target.exists() else {}
    if set(built) != set(actual):
        return "file set differs: " + ", ".join(sorted(set(built) ^ set(actual)))
    changed = sorted(name for name in built if built[name] != actual[name])
    if changed:
        return "content differs from the source with the edits: " + ", ".join(changed)
    return None


def check_derivations(ident, case):
    """CONF-01: each listed copy is an input of the case inside the case's own directory, and matches its source."""
    match = re.fullmatch(r"(conformance/.+)/expected/" + re.escape(ident) + r"\.json", case["expected"])
    require(match is not None, ident + " expected path is not <suite folder>/expected/<case ID>.json: " + case["expected"])
    own = match.group(1) + "/" + ("valid" if case["success"] else "invalid") + "/" + ident + "/"
    paths = [path.relative_to(ROOT).as_posix() for path in input_files(case)]
    seen = set()
    for entry in case.get("derivedFrom", []):
        require(entry["path"] in paths and entry["path"].startswith(own) and entry["path"] not in seen,
                ident + " derivedFrom path is not an own input of the case: " + entry["path"])
        seen.add(entry["path"])
        problem = derivation_problem(entry)
        require(problem is None, ident + " derivedFrom " + entry["path"] + ": " + str(problem))
    return len(seen)


# CONF-01: these checks list their own result. Version package cases (L0-L2) compare the AST and diagnostics,
# and reference cases compare references.
OWN_RESULT_CHECKS = ("L3", "L4", "change", "registry", "rebuild")


def own_result_listed(case, expected):
    """CONF-01: L3/L4, change, registry and rebuild cases list their own check (and category) exactly once."""
    if case["check"] not in OWN_RESULT_CHECKS:
        return True
    own = [r for r in expected.get("results", [])
           if r["check"] == case["check"] and r.get("category") == case.get("category")]
    return len(own) == 1


def audit_suite(name, validators, rules):
    folder, prefix = SUITES[name]
    base = ROOT / "conformance" / folder
    index = read_json(base / "manifest.json")
    validators["common/v1alpha1/conformance.schema.json"].validate(index)
    require(index["suite"] == name, "Suite mismatch: " + folder)
    seen, covered, expected_paths = set(), set(), set()
    stats = {"positive": 0, "negative": 0, "files": 0, "derived": 0}
    for case in index["cases"]:
        ident = case["id"]
        require(ident.startswith(prefix + "-") and ident not in seen, "Bad or duplicate case ID: " + ident)
        seen.add(ident)
        unknown = set(case["requirements"]) - rules
        require(not unknown, ident + " unknown requirement: " + str(unknown))
        covered.update(case["requirements"])
        require(case["normative"] == (case["check"] != "L2"), ident + " normative/check mismatch")
        group = "/valid/" if case["success"] else "/invalid/"
        inputs = input_files(case)
        for path in inputs:
            require(path.exists(), ident + " missing input: " + str(path))
        stats["derived"] += check_derivations(ident, case)
        # Inputs may share checked-in positive fixtures; the case's own input must sit in its group.
        require(any(group in "/" + path.relative_to(ROOT).as_posix() for path in inputs), ident + " case directory mismatch")
        exp_path = ROOT / case["expected"]
        require(exp_path.is_file() and case["expected"] not in expected_paths, ident + " expected file")
        expected_paths.add(case["expected"])
        expected = read_json(exp_path)
        validators["common/v1alpha1/expected.schema.json"].validate(expected)
        failed = any(r["result"] == "fail" for r in expected.get("results", []))
        errors = [d for d in expected.get("diagnostics", []) if d["class"] == "error"]
        require(all(d["rule"] in rules for d in expected.get("diagnostics", [])), ident + " unknown diagnostic rule")
        require(own_result_listed(case, expected), ident + " expected result must list the case's own check once")
        if case["success"]:
            # CONF-01: notApplicable and incomplete are allowed; the result values themselves are left to the schema.
            require(not failed and not errors, ident + " positive case expects failure")
        else:
            require(bool(errors), ident + " negative case needs an error diagnostic")
        located = [d["location"] for d in expected.get("diagnostics", []) if "location" in d]
        if case["input"]["kind"] == "package":
            v2 = name == "loj/v1alpha2"
            # CONF-01: L1/L2 positives carry the full AST; L0 positives carry the L0 pass result and no AST.
            require(("ast" in expected) == (case["success"] and v2 and case["check"] != "L0"), ident + " AST presence")
            path = ROOT / case["input"]["path"]
            issues, man = inspect_manifest(path, validators["v1alpha2/manifest.schema.json"], "loj/v1alpha2")
            for location in located:
                problem = location_problem(path, man, location)
                require(problem is None, ident + " diagnostic location " + str(location) + ": " + str(problem))
            if case["success"] and case["check"] == "L0":
                # unsupportedFeatures may be declared: it fails L1 (BASIC-03), not L0.
                require(not issues, ident + " invalid L0 positive Manifest: " + str(issues))
                require(L0_PASS in expected.get("results", []), ident + " L0 positive must list the L0 pass result")
            elif case["success"]:
                require(not issues and not man.get("unsupportedFeatures"), ident + " invalid positive Manifest: " + str(issues))
                validators["v1alpha2/ast.schema.json"].validate(expected["ast"])
                check_positive(path, man, expected, v2=True)
            elif case["check"] == "L0":
                wanted = {d["rule"] for d in errors}
                require(wanted <= set(issues), ident + " expected L0 rejection absent: " + str(issues))
            elif case["check"] == "L1":
                require(not issues, ident + " unexpected L0 failure: " + str(issues))
        else:
            # CONF-01: only SRC-01 (version packages) fixes diagnostic locations.
            require(not located, ident + " diagnostic location outside a version package case")
            # Version package cases (L0-L2) never carry the mark: their schema violations are L0 failures,
            # checked through inspect_manifest above, and the index schema rejects the mark there.
            stats["files"] += check_schema_mark(ident, case, inputs, validators)
        stats["positive" if case["success"] else "negative"] += 1
    on_disk = {p.relative_to(ROOT).as_posix() for p in (base / "expected").glob("*.json")}
    require(expected_paths == on_disk, folder + " orphan expected file")
    return len(seen), covered, stats


def audit_next(validators):
    rules = next_rules()
    covered, lines = set(), []
    for name, (folder, _) in SUITES.items():
        if not (ROOT / "conformance" / folder / "manifest.json").is_file():
            continue
        count, cov, stats = audit_suite(name, validators, rules)
        covered |= cov
        lines.append(f"{folder}: {count} cases ({stats['positive']} positive, {stats['negative']} negative; "
                     f"{stats['files']} input YAML files schema-checked; {stats['derived']} copied inputs match their source)")
    return lines, sorted(rules - covered)


ROOT_DOCS = ("README.md", "CONTRIBUTING.md", "CHANGELOG.md", "AGENTS.md")


def check_links():
    count = 0
    files = [ROOT / name for name in ROOT_DOCS]
    files += list((ROOT / "spec").rglob("*.md")) + list((ROOT / "docs").rglob("*.md"))
    for path in files:
        for block in MD.parse(path.read_text(encoding="utf-8")):
            for token in block.children or []:
                if token.type not in ("link_open", "image"):
                    continue
                href = token.attrGet("href") or token.attrGet("src")
                parsed = urlsplit(href)
                if parsed.scheme:
                    continue
                target = (path.parent / unquote(parsed.path)).resolve() if parsed.path else path
                require(target == ROOT or ROOT in target.parents, "Link escapes repository: " + href)
                require(target.exists(), "Broken link in " + str(path) + ": " + href)
                if parsed.fragment:
                    content = target.read_text(encoding="utf-8")
                    require('id="' + parsed.fragment + '"' in content or any(
                        re.sub(r"[^\w\- ]", "", h).lower().replace(" ", "-") == unquote(parsed.fragment)
                        for h in re.findall(r"^#+ (.+)$", content, re.M)), "Broken fragment: " + href)
                count += 1
    return count


ARCHIVE = ROOT / "docs/archive"
ID_HEADING = re.compile(r"^#+ ([A-Z]+)-\d+(?:\s|$)", re.M)


def local_link_targets(path):
    for block in MD.parse(path.read_text(encoding="utf-8")):
        for token in block.children or []:
            if token.type in ("link_open", "image"):
                parsed = urlsplit(token.attrGet("href") or token.attrGet("src"))
                if not parsed.scheme and parsed.path:
                    yield (path.parent / unquote(parsed.path)).resolve()


def check_archive():
    """Keep settled documents (docs/archive) from being read as normative."""
    archived = sorted(ARCHIVE.rglob("*.md"))
    require(archived, "docs/archive has no documents")
    for path in archived:
        lines = [line for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
        require(len(lines) > 1 and lines[0].startswith("# ") and lines[1].startswith("状態:"),
                "Archived document needs a 状態: line after its title: " + str(path))
    for path in (ROOT / "spec").rglob("*.md"):
        for target in local_link_targets(path):
            require(target != ARCHIVE and ARCHIVE not in target.parents,
                    "Normative text links to an archived document: " + str(path))
    outside = [ROOT / name for name in ROOT_DOCS]
    outside += list((ROOT / "docs").rglob("*.md")) + list((ROOT / "examples").rglob("*.md"))
    for path in outside:
        series = set(ID_HEADING.findall(path.read_text(encoding="utf-8"))) - {"DDR"}
        require(not series, "Requirement ID heading outside spec/ (prefix it with 案): "
                + str(path) + ": " + ", ".join(sorted(series)))
    return len(archived)


# 「字（U+XXXX）」「字 U+XXXX」: one character immediately before a code point notation.
CODEPOINT_NOTE = re.compile(r"(.)(?:（| )U\+([0-9A-F]{4,6})(?![0-9A-F])")


def codepoint_mismatches(text):
    """(line, actual, written) for each character written next to a code point that is not its own,
    e.g. a compatibility ideograph silently normalized to the unified one.

    The character must be a letter, digit or symbol standing alone: one that ends a word
    (空白（U+3000）), punctuation and range marks (U+F900〜U+FAFF) are not targets.
    Limitation: a character directly after another letter is never checked, so an example must be
    set off by a space or punctuation, and the notation must use a full-width parenthesis or a space
    and upper-case hex (half-width "(U+...)" and "u+..." are not checked) (「例: 神 U+FA19」, not 「互換漢字神（U+FA19）」) to be checked.
    """
    found = []
    for match in CODEPOINT_NOTE.finditer(text):
        char, point = match[1], int(match[2], 16)
        category = unicodedata.category(char)
        before = text[match.start() - 1] if match.start() else " "
        if category[0] not in "LNS" or category == "Sm" or unicodedata.category(before)[0] == "L":
            continue
        if ord(char) != point:
            found.append((text.count("\n", 0, match.start()) + 1, f"U+{ord(char):04X}", match[2]))
    return found


def check_codepoints():
    """Code point notations in spec/ and docs/ must match their characters.

    docs/archive is skipped: its content is fixed, and it keeps characters that were normalized
    before this check existed.
    """
    files = [ROOT / name for name in ROOT_DOCS]
    files += list((ROOT / "spec").rglob("*.md")) + list((ROOT / "docs").rglob("*.md"))
    files = [path for path in files if ARCHIVE not in path.resolve().parents]
    for path in files:
        problems = codepoint_mismatches(path.read_text(encoding="utf-8"))
        require(not problems, "Character does not match its code point notation in " + str(path) + ": "
                + ", ".join(f"line {line}: {actual} written as U+{written}" for line, actual, written in problems))
    return len(files)


def table_rows(text, heading):
    """Rows of the first Markdown table in the `## heading` section, as dicts keyed by header cell.

    Cells are split on every `|`, so a cell must not contain one (not even escaped as `\\|`).
    A row broken that way fails check_states() instead of passing silently.
    """
    section = re.search(r"^## " + re.escape(heading) + r"\n(.*?)(?=^## |\Z)", text, re.M | re.S)
    require(bool(section), "spec/README.md has no section: " + heading)
    lines = [line for line in section[1].splitlines() if line.startswith("|")]
    require(len(lines) > 2, "spec/README.md section has no table: " + heading)
    cells = [[cell.strip() for cell in line.strip().strip("|").split("|")] for line in lines]
    for row in cells[1:]:
        require(len(row) == len(cells[0]), "spec/README.md table row has " + str(len(row)) + " cells, header has "
                + str(len(cells[0])) + ": " + heading + ": " + row[0])
    return [dict(zip(cells[0], row)) for row in cells[2:]]


def check_states():
    """Version states (spec/README.md) must be well-formed and cover every spec directory exactly once."""
    spec = ROOT / "spec"
    text = (spec / "README.md").read_text(encoding="utf-8")
    states = {}
    for heading, allowed in [("規範とするもの", ("草案", "公開")), ("凍結した版", ("凍結",))]:
        for row in table_rows(text, heading):
            name = re.match(r"\[([^\]]+)\]", next(iter(row.values())))
            require(bool(name), "Version table row needs a linked directory: " + heading)
            state = row.get("状態", "")
            if heading == "凍結した版":
                # The frozen table writes the state as a sentence followed by notes ("凍結。内容を変えない…");
                # only the part before the first "。" is the state.
                state = state.split("。")[0]
            require(state in allowed, "Bad version state for " + name[1] + ": " + (state or "(none)"))
            require(name[1] not in states, "Version listed twice: " + name[1])
            states[name[1]] = state
    # Deliberately strict: every directory under spec/ that holds Markdown is a version and needs a state.
    # A subdirectory inside a version (e.g. an appendix folder) fails here until this rule is revisited.
    folders = {path.parent.relative_to(spec).as_posix() for path in spec.rglob("*.md") if path.parent != spec}
    require(folders == set(states), "Version tables and spec/ directories differ: "
            + ", ".join(sorted(folders ^ set(states))))
    return states


REQUIREMENT_HEADING = re.compile(r"^## ([A-Z]+-\d+) ", re.M)
# ASCII boundaries: \b would fail next to Japanese letters (「MUST等」).
REQUIREMENT_WORD = re.compile(r"(?<![A-Za-z0-9_])(?:MUST|SHOULD|MAY)(?![A-Za-z0-9_])")
REQUIREMENT_REF = re.compile(r"(?<![A-Z])([A-Z]+-\d+)")


def sentences(line):
    """Split a line at 。 outside full-width parentheses (「（MUST NOT。HIST-12）」 is one sentence).

    Parentheses are counted by depth; an unpaired ） is ignored, so it cannot join later sentences.
    """
    parts, depth, start = [], 0, 0
    for index, char in enumerate(line):
        if char == "（":
            depth += 1
        elif char == "）":
            depth = max(0, depth - 1)
        elif char == "。" and depth == 0:
            parts.append(line[start:index + 1])
            start = index + 1
    parts.append(line[start:])
    return [part for part in parts if part]


def restated_requirement_words(texts):
    """Sentences that use a requirement word (MUST, MUST NOT, SHOULD, MAY) and also cite another
    requirement ID, as (name, line, own ID, cited IDs).

    A rule's requirement word belongs to one requirement, its source; other requirements summarize it
    without a requirement word and link to the source (DDR-022). A hit is a warning, not a failure:
    a sentence may rightly set its own rule and cite a related one (e.g. "satisfy TYPE-05"). Only
    sentences under a requirement heading are read; citations of unknown IDs are ignored.
    """
    ids = set()
    for text in texts.values():
        ids.update(REQUIREMENT_HEADING.findall(text))
    found = []
    for name, text in sorted(texts.items()):
        own = None
        for number, line in enumerate(text.splitlines(), 1):
            heading = REQUIREMENT_HEADING.match(line)
            if heading or line.startswith("## ") or line.startswith("# "):
                own = heading[1] if heading else None
                continue
            if own is None:
                continue
            for sentence in sentences(line):
                if REQUIREMENT_WORD.search(sentence):
                    cited = sorted({ref for ref in REQUIREMENT_REF.findall(sentence) if ref in ids and ref != own})
                    if cited:
                        found.append((name, number, own, cited))
    return found


def check_restatements():
    """Warn about requirement words restated outside their source requirement (frozen versions excluded)."""
    spec = ROOT / "spec"
    texts = {path.relative_to(ROOT).as_posix(): path.read_text(encoding="utf-8")
             for path in spec.rglob("*.md") if (spec / "v1alpha1") not in path.parents}
    return restated_requirement_words(texts)


# 「CHAR-02〜CHAR-04」「FIXREF-03」: one ID or an inclusive range within one series.
ID_OR_RANGE = re.compile(r"([A-Z]+)-(\d+)(?:〜(?:\1-)?(\d+))?")
ADDRESSEE_HEADING = "要件の名宛人と確かめ方"


def addressee_table_ids(text):
    """Requirement IDs named in the first column of the docs/coverage.md addressee table."""
    section = re.search(r"^## " + ADDRESSEE_HEADING + r"\n(.*?)(?=^## |\Z)", text, re.M | re.S)
    require(bool(section), "docs/coverage.md has no section: " + ADDRESSEE_HEADING)
    rows = [line for line in section[1].splitlines() if line.startswith("|")][2:]
    require(rows, "docs/coverage.md addressee table is empty")
    ids = set()
    for row in rows:
        for series, first, last in ID_OR_RANGE.findall(row.strip("|").split("|")[0]):
            for number in range(int(first), int(last or first) + 1):
                ids.add("%s-%02d" % (series, number))
    return ids


def check_addressees():
    """Every requirement ID of the non-frozen versions appears in the addressee table, and no other ID does.

    The classification itself is a human judgment (reference only); this keeps the list from going stale
    when requirements are added or removed.
    """
    spec = ROOT / "spec"
    wanted = set()
    for path in spec.rglob("*.md"):
        if (spec / "v1alpha1") not in path.parents:
            wanted.update(REQUIREMENT_HEADING.findall(path.read_text(encoding="utf-8")))
    listed = addressee_table_ids((ROOT / "docs/coverage.md").read_text(encoding="utf-8"))
    compare_addressees(listed, wanted)
    return len(wanted)


def compare_addressees(listed, wanted):
    """Fail when the table misses a requirement ID (wanted - listed) or names an unknown one (listed - wanted)."""
    require(listed == wanted, "docs/coverage.md addressee table and spec/ requirement IDs differ: missing "
            + ", ".join(sorted(wanted - listed)) + "; unknown " + ", ".join(sorted(listed - wanted)))


def main():
    schemas = {path.name: read_json(path) for path in (ROOT / "schemas/v1alpha1").glob("*.json")}
    registry = Registry().with_resources((s["$id"], Resource.from_contents(s)) for s in schemas.values())
    validators = {}
    for name, value in schemas.items():
        Draft202012Validator.check_schema(value)
        validators[name] = Draft202012Validator(value, registry=registry, format_checker=FormatChecker())
    index = read_json(ROOT / "conformance/v1alpha1/manifest.json")
    validators["conformance.schema.json"].validate(index)
    rules = set()
    for path in (ROOT / "spec/v1alpha1").glob("*.md"):
        rules.update(re.findall(r"^## ([A-Z]+-\d+)$", path.read_text(encoding="utf-8"), re.M))
    seen, covered, expected_paths, input_paths = set(), set(), set(), set()
    positive, negative_l0, negative_l1, illustrative = 0, 0, 0, 0
    for case in index["cases"]:
        ident = case["id"]
        require(ident not in seen, "Duplicate test ID: " + ident)
        seen.add(ident)
        require(set(case["requirements"]) <= rules, "Unknown requirement: " + ident)
        covered.update(case["requirements"])
        require(case["normative"] == (case["level"] in ("L0", "L1")), "Level/status mismatch")
        require(("/valid/" if case["success"] else "/invalid/") in case["input"], "Case directory mismatch")
        path, exp_path = ROOT / case["input"], ROOT / case["expected"]
        require(path.is_file() and exp_path.is_file(), "Missing case files")
        require(case["expected"] not in expected_paths, "Shared expected path")
        expected_paths.add(case["expected"]); input_paths.add(case["input"])
        expected = read_json(exp_path)
        validators["expected.schema.json"].validate(expected)
        require(("ast" in expected) == case["success"], "Outcome mismatch")
        issues, man = inspect_manifest(path, validators["manifest.schema.json"])
        if case["success"]:
            require(not issues, ident + " invalid positive Manifest: " + str(issues))
            require(not man.get("unsupportedFeatures"), "Unsupported positive")
            check_positive(path, man, expected)
            positive += 1
        elif not case["normative"]:
            illustrative += 1
        elif case["level"] == "L0":
            wanted = {x["rule"] for x in expected["diagnostics"]}
            require(wanted <= set(issues), ident + " expected L0 rejection absent: " + str(issues))
            negative_l0 += 1
        else:
            require(not issues, ident + " unexpected L0 failure: " + str(issues))
            require(all(d["rule"] in case["requirements"] for d in expected["diagnostics"]), "Diagnostic rule mismatch")
            negative_l1 += 1
    require(expected_paths == {p.relative_to(ROOT).as_posix() for p in (ROOT / "conformance/v1alpha1/expected").glob("*.json")}, "Orphan expected file")
    require(input_paths == {p.relative_to(ROOT).as_posix() for p in (ROOT / "conformance/v1alpha1").glob("*/T*/law.yaml")}, "Orphan input case")
    require(read_json(ROOT / "conformance/v1alpha1/expected/T016.json")["ast"] ==
            read_json(ROOT / "conformance/v1alpha1/expected/T017.json")["ast"], "Split/whole AST differs")
    sample_path = ROOT / "examples/fictional-law/law.yaml"
    issues, sample = inspect_manifest(sample_path, validators["manifest.schema.json"])
    require(not issues, "Sample Manifest invalid")
    sample_ast = read_json(sample_path.parent / "expected.ast.json")
    validators["ast.schema.json"].validate(sample_ast)
    node_count = check_positive(sample_path, sample, {"ast": sample_ast})
    next_lines, uncovered_next = audit_next(all_schemas())
    links = check_links()
    archived = check_archive()
    noted = check_codepoints()
    states = check_states()
    addressed = check_addressees()
    print(f"Artifact audit PASS: {len(schemas)} schemas; {len(seen)} case definitions; {links} local links.")
    labels = {"草案": "draft", "公開": "published", "凍結": "frozen"}  # ASCII: stdout may not encode Japanese
    print("Version states: " + "; ".join(name + "=" + labels[state] for name, state in sorted(states.items()))
          + " (tables only; publication tags are not checked).")
    print(f"Code point notations match their characters in {noted} documents (docs/archive excluded).")
    print(f"Addressee table lists all {addressed} requirement IDs (the classification itself is not checked).")
    print(f"Archived documents: {archived} (status lines present; not linked from spec/).")
    print(f"Positive source/tree audits: {positive}; executed L0 negatives: {negative_l0}.")
    print(f"L1 negative definitions only (NOT executed): {negative_l1}; informative L2: {illustrative}.")
    print(f"Fictional sample: {node_count} nodes. Uncovered requirement IDs: {', '.join(sorted(rules - covered))}.")
    for line in next_lines:
        print("Next spec suite " + line + ".")
    print("Next spec requirement IDs without a case: " + (", ".join(uncovered_next) or "none") + ".")
    print("L1 negatives and L3/L4/registry/rebuild/change/reference cases are checked for shape only; "
          "their outcomes need a validator.")
    print("This is not full L1 conformance certification or an egov round-trip test.")
    restated = check_restatements()
    print(f"WARNING (not a failure): {len(restated)} sentences use a requirement word and cite another "
          "requirement; keep the requirement word only in the source requirement (DDR-022).")
    for name, number, own, cited in restated:
        print(f"  {name}:{number} {own} cites {', '.join(cited)}")


if __name__ == "__main__":
    main()
