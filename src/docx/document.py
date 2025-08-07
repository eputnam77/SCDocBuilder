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
    def __init__(self) -> None:
        self.paragraphs: List[Paragraph] = []
        self.tables: List[_Table] = []
        self.sections: List[_Section] = [_Section()]
        self.part = _Part()

    def add_paragraph(self, text: str = "") -> Paragraph:
        p = Paragraph()
        if text:
            p.add_run(text)
        self.paragraphs.append(p)
        return p

    def add_table(self, rows: int, cols: int) -> _Table:
        table = _Table(rows, cols)
        self.tables.append(table)
        return table

    def save(self, path: str) -> None:
        data = self._serialize().encode("utf-8")
        with open(path, "wb") as f:
            f.write(data)

    def _serialize(self) -> str:
        lines: List[str] = []
        lines.extend(p.text for p in self.paragraphs)
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
