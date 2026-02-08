#!/usr/bin/env python3
"""Fetch the latest blog post from maxdaten.io RSS and update README.md."""

import re
import sys
import xml.etree.ElementTree as ET
from urllib.request import urlopen

RSS_URL = "https://www.maxdaten.io/rss.xml"
LATEST_POST_PATTERN = re.compile(r"- 📝 Latest post: \[.*?\]\(.*?\)")


def fetch_latest_post(rss_url: str = RSS_URL) -> tuple[str, str]:
    """Return (title, link) of the most recent RSS item."""
    with urlopen(rss_url) as resp:
        rss = resp.read()
    return parse_latest_post(rss)


def parse_latest_post(rss_bytes: bytes) -> tuple[str, str]:
    """Parse RSS bytes and return (title, link) of the first item."""
    root = ET.fromstring(rss_bytes)
    item = root.find(".//item")
    if item is None:
        raise ValueError("No items found in RSS feed")
    title = item.find("title").text.strip()
    link = item.find("link").text.strip()
    return title, link


def update_readme(content: str, title: str, link: str) -> str | None:
    """Replace the latest-post line in README content. Returns None if unchanged."""
    new_line = f"- 📝 Latest post: [{title}]({link})"
    updated = LATEST_POST_PATTERN.sub(new_line, content)
    if updated == content:
        return None
    return updated


def main() -> None:
    title, link = fetch_latest_post()

    with open("README.md") as f:
        content = f.read()

    updated = update_readme(content, title, link)
    if updated is None:
        print("Already up to date")
        return

    with open("README.md", "w") as f:
        f.write(updated)

    print(f"Updated: {title} — {link}")


if __name__ == "__main__":
    main()
