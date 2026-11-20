"""GitHub Pages용 docs/ 폴더를 만든다.

- index.html(아티팩트 원본, 문서 골격 없음)을 완전한 HTML 문서로 감싸 docs/index.html 로 저장
- data/items.json, data/meta.json 을 docs/data/ 로 복사 (items는 날짜 내림차순 정렬)

사용: python build.py
"""
import json
import pathlib
import shutil

ROOT = pathlib.Path(__file__).resolve().parent
DOCS = ROOT / "docs"

HEAD = (
    '<!doctype html><html lang="ko"><head><meta charset="utf-8">'
    '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
    "<style>:root{color-scheme:light;padding-top:env(safe-area-inset-top,0px);"
    "padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0;font-size:14px;"
    "font-family:system-ui,sans-serif}img{max-width:100%}[hidden]{display:none!important}</style>"
    "</head><body>"
)
TAIL = "</body></html>\n"


def main():
    (DOCS / "data").mkdir(parents=True, exist_ok=True)
    page = (ROOT / "index.html").read_text(encoding="utf-8")
    (DOCS / "index.html").write_text(HEAD + page + TAIL, encoding="utf-8")

    items = json.loads((ROOT / "data" / "items.json").read_text(encoding="utf-8"))
    ids = [i["id"] for i in items]
    assert len(ids) == len(set(ids)), "중복 id가 있습니다"
    items.sort(key=lambda i: i.get("date") or "", reverse=True)
    (DOCS / "data" / "items.json").write_text(json.dumps(items, ensure_ascii=False, indent=1), encoding="utf-8")
    shutil.copyfile(ROOT / "data" / "meta.json", DOCS / "data" / "meta.json")
    (DOCS / ".nojekyll").write_text("", encoding="utf-8")
    print(f"docs/ 생성 완료: {len(items)}건")


if __name__ == "__main__":
    main()
