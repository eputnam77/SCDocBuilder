from __future__ import annotations

from typing import Any, List, cast


class OxmlElement:
    def __init__(self, tag: str):
        self.tag = tag
        self.attrib: dict[str, str] = {}

    def set(self, key: str, value: str) -> None:
        self.attrib[key] = value

    def to_xml(self) -> str:
        attrs = " ".join(f'{k}="{v}"' for k, v in self.attrib.items())
        return f"<{self.tag} {attrs}/>" if attrs else f"<{self.tag}/>"


class _RunElement:
    def __init__(self, run: _Run):
        self.run = run
        self.children: List[Any] = []

    def append(self, element: Any) -> None:
        self.children.append(element)
        if self.run.parent is not None:
            self.run.parent._p.xml += getattr(element, "to_xml", lambda: str(element))()


class _ParagraphElement:
    def __init__(self, paragraph: _Paragraph | None = None):
        self.paragraph = paragraph
        self.xml = ""

    def remove(self, run_element: _RunElement) -> None:
        run = run_element.run
        if self.paragraph and run in self.paragraph.runs:
            self.paragraph.runs.remove(run)

    def xpath(
        self, query: str
    ) -> list[_ParagraphElement]:  # pragma: no cover - simple stub
        return [self]


class _Run:
    def __init__(self, text: str = "", parent: _Paragraph | None = None):
        self.text = text
        self.bold = False
        self.italic = False
        self.parent = parent
        self._r = _RunElement(self)


class _Paragraph:
    def __init__(
        self, element: _ParagraphElement | None = None, parent: Any | None = None
    ) -> None:
        if element is not None and element.paragraph is not None:
            self._p = element
            self.runs: List[_Run] = element.paragraph.runs
            self._p.paragraph = self
        elif element is not None:
            self._p = element
            self.runs = []
            self._p.paragraph = self
        else:
            self._p = _ParagraphElement(self)
            self.runs = []
        # record heading level if used via Document.add_heading
        self.level = 0

    def add_run(self, text: str = "") -> _Run:
        run = _Run(text, self)
        self.runs.append(run)
        return run

    @property
    def text(self) -> str:
        return "".join(run.text for run in self.runs)


Paragraph = cast(Any, _Paragraph)
