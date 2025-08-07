from __future__ import annotations

from typing import Any, List, cast

from .text.paragraph import Paragraph


class _ElementRoot:
    def xpath(self, query: str) -> list[Any]:  # pragma: no cover - simple stub
        return []


class _Part:
    def __init__(self) -> None:
        self.element = _ElementRoot()


class _HeaderFooter:
    def __init__(self) -> None:
        self.paragraphs: List[Paragraph] = []
        self.tables: List[_Table] = []
        self.part = _Part()

    def add_paragraph(self, text: str = "") -> Paragraph:
        p = Paragraph()
        if text:
            p.add_run(text)
        self.paragraphs.append(p)
        return p

    def add_table(self, rows: int, cols: int, width: Any = None) -> _Table:
        table = _Table(rows, cols)
        self.tables.append(table)
        return table


class _Section:
    def __init__(self) -> None:
        self.header = _HeaderFooter()
        self.footer = _HeaderFooter()


class _Cell:
    def __init__(self) -> None:
        p = Paragraph()
        self.paragraphs: List[Paragraph] = [p]

    @property
    def text(self) -> str:
        return "\n".join(p.text for p in self.paragraphs)

    @text.setter
    def text(self, value: str) -> None:
        p = Paragraph()
        if value:
            p.add_run(value)
        self.paragraphs = [p]


class _Row:
    def __init__(self, cols: int) -> None:
        self.cells: List[_Cell] = [_Cell() for _ in range(cols)]


class _Table:
    def __init__(self, rows: int, cols: int) -> None:
        self.rows: List[_Row] = [_Row(cols) for _ in range(rows)]

    def cell(self, i: int, j: int) -> _Cell:
        return self.rows[i].cells[j]


class _Document:
    def __init__(self, path: str | None = None) -> None:
        self.paragraphs: List[Paragraph] = []
        self.tables: List[_Table] = []
        self.sections: List[_Section] = [_Section()]
        self.part = _Part()
        if path is not None:
            data = open(path, "rb").read()
            if not data.startswith(b"PK"):
                raise TypeError("Not a valid docx file")
            for line in data[2:].decode("utf-8").splitlines():
                if line.startswith("!"):
                    level, text = line[1:].split(":", 1)
                    self.add_heading(text, level=int(level))
                elif line.startswith("H:"):
                    self.sections[0].header.add_paragraph(line[2:])
                elif line.startswith("F:"):
                    self.sections[0].footer.add_paragraph(line[2:])
                elif "|" in line:
                    cells = line.split("|")
                    table = self.add_table(1, len(cells))
                    for i, cell_text in enumerate(cells):
                        table.cell(0, i).text = cell_text
                else:
                    self.add_paragraph(line)

    def add_paragraph(self, text: str = "") -> Paragraph:
        p = Paragraph()
        if text:
            p.add_run(text)
        self.paragraphs.append(p)
        return p

    def add_heading(self, text: str, level: int = 1) -> Paragraph:
        """Add a heading paragraph of ``level``.

        This minimal implementation stores the level on the paragraph so that
        callers such as :func:`scdocbuilder.html_export` can render the
        appropriate ``<hN>`` tag.
        """

        p = self.add_paragraph(text)
        p.level = level
        return p

    def add_table(self, rows: int, cols: int) -> _Table:
        table = _Table(rows, cols)
        self.tables.append(table)
        return table

    def save(self, path: str) -> None:
        data = self._serialize().encode("utf-8")
        # Prefix with ``PK`` so ``validate_input_files`` can sanity‑check the
        # pseudo‑DOCX magic number.
        with open(path, "wb") as f:
            f.write(b"PK" + data)

    def _serialize(self) -> str:
        lines: List[str] = []
        for p in self.paragraphs:
            if getattr(p, "level", 0):
                lines.append(f"!{p.level}:{p.text}")
            else:
                lines.append(p.text)
        for table in self.tables:
            for row in table.rows:
                lines.append("|".join(cell.text for cell in row.cells))
        for section in self.sections:
            for p in section.header.paragraphs:
                lines.append("H:" + p.text)
            for table in section.header.tables:
                for row in table.rows:
                    lines.append("H:" + "|".join(cell.text for cell in row.cells))
            for p in section.footer.paragraphs:
                lines.append("F:" + p.text)
            for table in section.footer.tables:
                for row in table.rows:
                    lines.append("F:" + "|".join(cell.text for cell in row.cells))
        return "\n".join(lines)


Document = cast(Any, _Document)
