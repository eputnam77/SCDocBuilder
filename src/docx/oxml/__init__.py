from __future__ import annotations


class OxmlElement:
    def __init__(self, tag: str) -> None:
        self.tag = tag
        self.attrib: dict[str, str] = {}

    def set(self, key: str, value: str) -> None:
        self.attrib[key] = value

    def to_xml(self) -> str:
        attrs = " ".join(f'{k}="{v}"' for k, v in self.attrib.items())
        return f"<{self.tag} {attrs}/>" if attrs else f"<{self.tag}/>"
