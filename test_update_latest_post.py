"""Tests for update_latest_post."""

from update_latest_post import parse_latest_post, update_readme

SAMPLE_RSS = b"""\
<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>maxdaten.io</title>
    <item>
      <title>Ship Your Toolchain, Not Just Infrastructure</title>
      <link>https://maxdaten.io/2026-01-31-ship-your-toolchain</link>
    </item>
    <item>
      <title>Older Post</title>
      <link>https://maxdaten.io/older-post</link>
    </item>
  </channel>
</rss>
"""

README_TEMPLATE = """\
# Profile

## Currently

- 🏗️ Building stuff
- 📝 Latest post: [{title}]({link})
- ✍️ Writing about things
"""


def test_parse_latest_post():
    title, link = parse_latest_post(SAMPLE_RSS)
    assert title == "Ship Your Toolchain, Not Just Infrastructure"
    assert link == "https://maxdaten.io/2026-01-31-ship-your-toolchain"


def test_parse_latest_post_empty_feed():
    rss = b'<rss version="2.0"><channel></channel></rss>'
    try:
        parse_latest_post(rss)
        assert False, "Expected ValueError"
    except ValueError:
        pass


def test_update_readme_changes():
    old = README_TEMPLATE.format(title="Old Post", link="https://maxdaten.io/old")
    result = update_readme(old, "New Post", "https://maxdaten.io/new")
    assert result is not None
    assert "[New Post](https://maxdaten.io/new)" in result
    assert "[Old Post]" not in result


def test_update_readme_unchanged():
    current = README_TEMPLATE.format(title="Same Post", link="https://maxdaten.io/same")
    result = update_readme(current, "Same Post", "https://maxdaten.io/same")
    assert result is None


def test_update_readme_preserves_surrounding():
    old = README_TEMPLATE.format(title="Old", link="https://maxdaten.io/old")
    result = update_readme(old, "New", "https://maxdaten.io/new")
    assert "Building stuff" in result
    assert "Writing about things" in result
