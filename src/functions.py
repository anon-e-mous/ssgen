import re
from textnode import TextType, TextNode
from blocknode import BlockType
from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode


def text_node_to_html_node(text_node):
    text = text_node.text
    type = text_node.text_type
    url = text_node.url

    match type:
        case TextType.TEXT:
            return LeafNode(None, text, None)
        case TextType.BOLD:
            return LeafNode("b", text, None)
        case TextType.ITALIC:
            return LeafNode("i", text, None)
        case TextType.CODE:
            return LeafNode("code", text, None)
        case TextType.LINK:
            return LeafNode("a", text, {"href": url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": url, "alt": text})
        case _:
            raise Exception("no such text type")
        
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        splits = []
        if delimiter == "**":
            splits = node.text.split("**")
            if len(splits) % 2 != 1:
                raise Exception("invalid Markdown text")
            new_text_type = TextType.BOLD
        elif delimiter == "*":
            splits = node.text.split("*")
            if len(splits) % 2 != 1:
                raise Exception("invalid Markdown text")
            new_text_type = TextType.ITALIC
        elif delimiter == "_":
            splits = node.text.split("_")
            if len(splits) % 2 != 1:
                raise Exception("invalid Markdown text")
            new_text_type = TextType.ITALIC
        else:
            splits = node.text.split("`")
            if len(splits) % 2 != 1:
                raise Exception("invalid Markdown text")
            new_text_type = TextType.CODE
        if len(splits) == 1:
            new_nodes.append(node)
            continue
        new_split_nodes = []
        for i, split in enumerate(splits):
            if i % 2 == 0:
                new_split_nodes.append(TextNode(split, TextType.TEXT))
            else:
                new_split_nodes.append(TextNode(split, new_text_type))
        new_nodes.extend(new_split_nodes)
    return new_nodes


def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        captures = extract_markdown_images(node.text)
        if not captures:
            new_nodes.append(node)
            continue
        new_captured_nodes = []
        text_remaining = node.text
        for i, capture in enumerate(captures):
            sections = text_remaining.split(f"![{capture[0]}]({capture[1]})", 1)
            if len(sections) == 1:
                # the entire remainder of text is just text so add a text node and exit this loop
                new_captured_nodes.append(TextNode(sections[0], TextType.TEXT))
                break
            if sections[0] != "":
                # there is text before the image so add a text node
                new_captured_nodes.append(TextNode(sections[0], TextType.TEXT))
            # add the image node for this capture
            new_captured_nodes.append(TextNode(f"{capture[0]}", TextType.IMAGE, f"{capture[1]}"))
            text_remaining = sections[1]
            if text_remaining != "" and i == len(captures) - 1:
                # add a text node for text after the last capture
                new_captured_nodes.append(TextNode(text_remaining, TextType.TEXT))
        new_nodes.extend(new_captured_nodes)
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        captures = extract_markdown_links(node.text)
        if not captures:
            new_nodes.append(node)
            continue
        new_captured_nodes = []
        text_remaining = node.text
        for i, capture in enumerate(captures):
            sections = text_remaining.split(f"[{capture[0]}]({capture[1]})", 1)
            if len(sections) == 1:
                # the entire remainder of text is just text so add a text node and exit this loop
                new_captured_nodes.append(TextNode(sections[0], TextType.TEXT))
                break
            if sections[0] != "":
                # there is text before the link so add a text node
                new_captured_nodes.append(TextNode(sections[0], TextType.TEXT))
            # add the link node for this capture
            new_captured_nodes.append(TextNode(f"{capture[0]}", TextType.LINK, f"{capture[1]}"))
            text_remaining = sections[1]
            if text_remaining != "" and i == len(captures) - 1:
                # add a text node for text after the last capture
                new_captured_nodes.append(TextNode(text_remaining, TextType.TEXT))
        new_nodes.extend(new_captured_nodes)
    return new_nodes


def text_to_textnodes(text):
    text_node = TextNode(text, TextType.TEXT)
    text_nodes = split_nodes_delimiter([text_node], '**', TextType.BOLD)
    text_nodes = split_nodes_delimiter(text_nodes, '*', TextType.ITALIC)
    text_nodes = split_nodes_delimiter(text_nodes, '_', TextType.ITALIC)
    text_nodes = split_nodes_delimiter(text_nodes, '`', TextType.CODE)
    text_nodes = split_nodes_image(text_nodes)
    text_nodes = split_nodes_link(text_nodes)
    return text_nodes


def markdown_to_blocks(markdown):
    markdown = markdown.strip()
    raw_blocks = markdown.split("\n\n")
    blocks = []
    for block in raw_blocks:
        block = block.strip(' \t\v\n\r\f')
        if block != "":
            blocks.append(block)
    return blocks


def block_to_block_type(block):
    pattern = r"^#{1,6} "
    if re.match(pattern, block):
        return BlockType.HEAD
    pattern = r"^```.*```$"
    if re.match(pattern, block, re.DOTALL):
        return BlockType.CODE
    pattern = r"^>.*$"
    if re.match(pattern, block, re.MULTILINE):
        return BlockType.QUOTE
    pattern = r"^- .*"
    if re.match(pattern, block, re.MULTILINE):
        return BlockType.UL
    
    lines = block.split("\n")
    start_num_match = re.match(r"^(\d+)\. ", lines[0])
    if not start_num_match:
        return BlockType.PARA
    start_num = int(start_num_match.group(1))
    for line in lines:
        pattern = f"^{start_num}\\. "
        if not re.match(pattern, line):
            return BlockType.PARA
        start_num += 1
    return BlockType.OL

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for node in text_nodes:
        html_node = text_node_to_html_node(node)
        html_nodes.append(html_node)
    return html_nodes

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    div_children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARA:
                p_block = ' '.join(block.split("\n"))
                children = text_to_children(p_block)
                block_node = ParentNode("p", children, None)
            case BlockType.HEAD:
                h_stripped = block.lstrip("#")
                h_num = len(block) - len(h_stripped)
                h_stripped = h_stripped.strip()
                head_tag = f"h{h_num}"
                children = text_to_children(h_stripped)
                block_node = ParentNode(head_tag, children, None)
            case BlockType.CODE:
                c_stripped = block.strip("`")
                c_block = f"<pre>{c_stripped}</pre>"
                block_node = text_node_to_html_node(TextNode(c_block, TextType.CODE, None))
            case BlockType.QUOTE:
                q_stripped = "".join(block[1:].split("\n>"))
                q_stripped = q_stripped.strip()
                print(q_stripped)
                children = text_to_children(q_stripped)
                print(children)
                block_node = ParentNode("blockquote", children, None)
            case BlockType.UL:
                ul_stripped = block[1:].split("\n- ")
                ul_block = ""
                for item in ul_stripped:
                    ul_block += f"<li>{item}</li>"
                children = text_to_children(ul_block)
                block_node = ParentNode("ul", children, None)
            case BlockType.OL:
                ol_stripped = block.split("\n")
                ol_block = ""
                for item in ol_stripped:
                    num_end = block.index(". ")
                    ol_block += f"<li>{item[num_end + 2:]}</li>"
                children = text_to_children(ol_block)
                block_node = ParentNode("ol", children, None)
            case _:
                raise Exception("no such block type")
        div_children.append(block_node)
    return ParentNode("div", div_children, None)

def extract_title(markdown):
    h1_pattern = "(^# .+)"
    h1_match = re.match(h1_pattern, markdown)
    if not h1_match:
        raise Exception("no h1 in markdown")
    heading = h1_match.group(0)[2:]
    return heading.strip()