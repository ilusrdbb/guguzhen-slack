import os

import yaml
from lxml import html


def read():
    config_data = []
    config_dir = "./config"
    for filename in os.listdir(config_dir):
        if filename.endswith(".yaml"):
            with open(os.path.join(config_dir, filename), 'r', encoding='utf-8') as f:
                config_data.append(yaml.safe_load(f))
    return config_data


def format_html(text: str):
    if not text:
        return ""
    try:
        page_body = html.fromstring(text)
        content_list = page_body.xpath("//text()")
        return " ".join(content_list)
    except:
        return text