"""Hand-authored MAN-03 cases; no parser/validator output is used."""


def add_cases(add, manifest, tree, a, n, t, base):
    def case(title, first, second, success=True):
        # These are authored body literals and a hand-defined semantic tree.
        # Sharing literal text is not a parse or a snapshot of validator output.
        expected = tree([a()], [n("AppendedMaterial", display="別表", key="table",
                                  content=[t(first + second)])]) if success else None
        add(title, "MAN-03 HEAD-03 AST-01 SRC-01", files={
            "main.md": base, "one.md": "# 別表\n" + first, "two.md": second,
        }, man=manifest([("main.md", "main"), ("one.md", "appendix/table"),
                         ("two.md", "appendix/table")],
                        appendices=[{"key": "table", "title": "別表"}]),
            ast_value=expected, failure=None if success else "MAN-03",
            positions=[{"nodeId": "20990101-act-1/appendix/table", "path": "one.md",
                        "start": 0, "end": 9}] if success else None)

    case("附属資料の段落・見出し・リスト分割", "本文。\n\n", "## 任意\n- 項目\n\n> 引用\n")
    case("附属資料の空白だけの後続を拒否", "本文。\n", " \n\t\n", False)
    case("非最終の明示閉鎖フェンス", "```text\ncode\n```\n", "次。\n")
    case("非最終の未閉鎖フェンスを拒否", "```\ncode\n", "次。\n", False)
    case("短い閉じフェンスを拒否", "````\ncode\n```\n", "次。\n", False)
    case("異なる文字種の閉じフェンスを拒否", "```\ncode\n~~~\n", "次。\n", False)
    case("引用内のチルダフェンス閉鎖", "> ~~~\n> code\n> ~~~\n", "次。\n")
    case("引用終了だけのフェンスを拒否", "> ```\n> code\n\n通常本文。\n", "次。\n", False)
    case("最終ファイルの未閉鎖フェンスを許可", "本文。\n", "```\ncode\n")
    html = [
        ("種類1", "<script>\ncode\n</script>\n", "<script>\ncode\n"),
        ("種類2", "<!-- ordinary\ncomment -->\n", "<!-- ordinary\ncomment\n"),
        ("種類3", "<?proc\n?>\n", "<?proc\n"),
        ("種類4", "<!DOCTYPE\nhtml>\n", "<!DOCTYPE\nhtml\n"),
        ("種類5", "<![CDATA[\nbody\n]]>\n", "<![CDATA[\nbody\n"),
        ("種類6", "<div>\nbody\n</div>\n\n", "<div>\nbody\n</div>\n"),
        ("種類7", "<custom>\nbody\n</custom>\n\n", "<custom>\nbody\n</custom>\n"),
    ]
    for kind, closed, unclosed in html:
        case("非最終HTML" + kind + "の終端", closed, "次。\n")
        case("非最終HTML" + kind + "の暗黙終端を拒否", unclosed, "次。\n", False)
    case("最終HTMLのEOF終端を許可", "本文。\n", "<div>\nbody\n")
    # A reserved marker is HEAD-03, independent of the new MAN-03 rule.
    add("分割附属資料でも予約マーカー禁止", "HEAD-03 MAN-03", files={
        "main.md": base, "one.md": "# 別表\n本文。\n", "two.md": "<!-- loj:item number=1 -->\n",
    }, man=manifest([("main.md", "main"), ("one.md", "appendix/table"),
                     ("two.md", "appendix/table")], appendices=[{"key": "table", "title": "別表"}]),
        failure="HEAD-03")
    case("CRLF明示閉鎖フェンス", "```\r\ncode\r\n```\r\n", "次。\n")
    case("CRLF未閉鎖フェンスを拒否", "```\r\ncode\r\n", "次。\n", False)
    case("附属資料のファイル別参照定義", "[label]: https://example.com\n", "[label]\n")
    case("インデントコードのフェンス風本文", "    ```\n    code\n", "次。\n")
    case("後続の先頭空行を本文保存", "本文。\n", "\n\n次。\n")
