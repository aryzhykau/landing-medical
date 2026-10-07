"""Check the deployable HTML and references, using only the Python standard library."""

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent.parent / "dist"


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = set()
        self.references = []
        self.headings = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        identifier = attrs.get("id")
        if identifier:
            if identifier in self.ids:
                raise ValueError(f"Duplicate id: {identifier}")
            self.ids.add(identifier)
        if tag == "h1":
            self.headings += 1
        for attribute in ("src", "href"):
            if attrs.get(attribute):
                self.references.append(attrs[attribute])


def main():
    entry = ROOT / "index.html"
    if not entry.is_file() or not entry.stat().st_size:
        raise ValueError("Missing or empty dist/index.html")
    pages = sorted(ROOT.rglob("*.html"))
    for page in pages:
        parser = PageParser()
        parser.feed(page.read_text(encoding="utf-8"))
        if parser.headings != 1:
            raise ValueError(f"{page.name}: expected one main heading")
        for reference in parser.references:
            url = urlsplit(reference)
            if url.scheme or url.netloc:
                continue
            if url.path.startswith("/"):
                raise ValueError(f"{page.name}: root-relative URL will break project Pages: {reference}")
            target = (page.parent / unquote(url.path)).resolve() if url.path else page
            if not target.is_relative_to(ROOT.resolve()) or not target.is_file():
                raise ValueError(f"{page.name}: missing local file: {reference}")
            if target == page and url.fragment and unquote(url.fragment) not in parser.ids:
                raise ValueError(f"{page.name}: missing section: {reference}")
    print(f"Validated {len(pages)} HTML page(s): headings, anchors and local assets are valid.")


if __name__ == "__main__":
    main()
