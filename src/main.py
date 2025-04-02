from textnode import TextType, TextNode 


def main() -> None:
  textNode = TextNode("This is some anchor text", TextType.LINK.value, "https://www.boot.dev")
  print(textNode)

main()