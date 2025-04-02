from enum import Enum


class TextType(Enum):
    NORMAL = "Normal text"
    BOLD = "Bold text"
    ITALIC = "Italic text"
    CODE = "Code text"
    LINK = "Link text"
    IMAGE = "Image text"


class TextNode():
    def __init__(self, text: str, text_type: TextType, url: str = None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, value) -> bool:
        if isinstance(value, TextNode):
            return self.text == value.text and self.text_type == value.text_type and self.url == value.url
        return False
    
    def __repr__(self) -> str:
        return f"TextNode(text={self.text!r}, text_type={self.text_type}, url={self.url!r})"