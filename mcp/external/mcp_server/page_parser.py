from bs4 import BeautifulSoup


class PageParser:

    def interactive_parse(self, html) -> str:

        soup = self._get_soup(html)
        interactive_elems = soup.find_all(["button", "a", "input"])
        interactive_formatted = "".join(
            list(
                set(
                    [self._get_selectors(b) for b in interactive_elems if b.get_text(strip=True)][:160]
                )
            )
        )

        if not interactive_formatted:
            return "No interactive elements found."

        return f"ACTIVE ELEMENTS:{interactive_formatted}\n"

    def texts_parse(self, html) -> str:

        soup = self._get_soup(html)
        title = soup.title.text if soup.title else ""
        texts_elems = soup.find_all(["p", "h1", "h2", "span", "div"])
        texts_formatted = "".join(
            list(
                set(
                    [self._get_selectors(p) for p in texts_elems if len(p.get_text(strip=True)) > 200][:100]
                )
            )
        )
        if not title and not texts_formatted:
            return "No title or text elements found."

        return f"TITLE:\n{title}\nTEXTS:{texts_formatted}\n"

    def _get_soup(self, html):
        soup = BeautifulSoup(html, "html.parser")
        for tag in soup(["script", "style"]):
            tag.decompose()

        return soup

    def _get_selectors(self, e) -> str:
        tag = e.name
        text = e.get_text(strip=True)[:800] if e.get_text(strip=True) else "-"
        name = e.get("name", "-")
        id = e.get("id", "-")
        classes = " ".join(e.get("class", [])[:4])
        return f"\nTag: {tag}. Text: {text}. Name: {name}. ID: {id}. Classes: {classes}"
