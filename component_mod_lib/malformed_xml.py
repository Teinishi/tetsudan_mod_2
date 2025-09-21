import re

pattern_malformed_attr = re.compile(r'\s+([0-9][^="])*="([^"]*)"')


def fix_malformed_attributes(content):
    """
    数字で始まる属性名に正規表現で無理矢理アンダースコアをつける
    """
    return pattern_malformed_attr.sub(
        lambda m: f' _{m.group(1)}="{m.group(2)}"', content)
