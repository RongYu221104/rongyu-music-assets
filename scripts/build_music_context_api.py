from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTEXT_ROOT = ROOT / "public" / "music-context"
OUTPUT = CONTEXT_ROOT / "api" / "v1" / "context.json"
PUBLIC_BASE = "/rongyu-music-assets/music-context"

ARTIST_IDS = {
    "Bill Evans": "bill-evans",
    "Miles Davis": "miles-davis",
    "Dave Brubeck": "dave-brubeck",
    "Paul Desmond": "paul-desmond",
    "Jim Hall": "jim-hall",
}

ALBUM_IDS = {
    "From Left to Right": "from-left-to-right",
    "Kind of Blue": "kind-of-blue",
    "Time Out": "time-out",
    "Undercurrent": "undercurrent",
    "Waltz for Debby": "waltz-for-debby",
    "You Must Believe in Spring": "you-must-believe-in-spring",
}

ALBUM_ARTISTS = {
    "from-left-to-right": ["bill-evans"],
    "kind-of-blue": ["miles-davis", "bill-evans"],
    "time-out": ["dave-brubeck", "paul-desmond"],
    "undercurrent": ["bill-evans", "jim-hall"],
    "waltz-for-debby": ["bill-evans"],
    "you-must-believe-in-spring": ["bill-evans"],
}

TRACK_IDS = {
    "from-left-to-right": [
        "what-are-you-doing-the-rest-of-your-life",
        "im-all-smiles",
        "why-did-i-choose-you",
        "soiree",
        "childrens-play-song",
    ],
    "kind-of-blue": [
        "so-what",
        "freddie-freeloader",
        "blue-in-green",
        "all-blues",
        "flamenco-sketches",
    ],
    "time-out": [
        "blue-rondo-a-la-turk",
        "strange-meadow-lark",
        "take-five",
        "three-to-get-ready",
        "kathys-waltz",
        "everybodys-jumpin",
        "pick-up-sticks",
    ],
    "undercurrent": [
        "my-funny-valentine",
        "i-hear-a-rhapsody",
        "dream-gypsy",
        "romain",
        "skating-in-central-park",
        "darn-that-dream",
    ],
    "waltz-for-debby": [
        "my-foolish-heart",
        "waltz-for-debby",
        "detour-ahead",
        "my-romance",
        "some-other-time",
        "milestones",
        "porgy",
    ],
    "you-must-believe-in-spring": [
        "you-must-believe-in-spring",
        "theme-from-mash",
    ],
}


def read(name: str) -> str:
    return (CONTEXT_ROOT / name).read_text(encoding="utf-8")


def sections(text: str, level: int) -> list[tuple[str, str]]:
    marker = "#" * level
    matches = list(re.finditer(rf"^{marker} (.+)$", text, flags=re.MULTILINE))
    result: list[tuple[str, str]] = []
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        result.append((match.group(1).strip(), text[start:end].strip()))
    return result


def plain(text: str) -> str:
    text = re.sub(r"!\[[^\]]*\]\([^)]+\)", "", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = text.replace("<br>", " ")
    text = text.replace("**", "").replace("*", "")
    return re.sub(r"\s+", " ", text).strip()


def paragraphs(body: str) -> list[str]:
    values: list[str] = []
    for block in re.split(r"\n\s*\n", body):
        value = plain(block)
        if not value or value == "---" or value.startswith("照片作者、许可"):
            continue
        if value.startswith("录音日期、地点") or value.startswith("各项事实与进一步阅读"):
            continue
        values.append(value)
    return values


def public_image(body: str) -> str | None:
    match = re.search(r"!\[[^\]]*\]\((images/[^)]+)\)", body)
    return f"{PUBLIC_BASE}/{match.group(1)}" if match else None


def parse_artists() -> list[dict[str, object]]:
    result: list[dict[str, object]] = []
    for heading, body in sections(read("artists.md"), 2):
        name, subtitle = (part.strip() for part in heading.split("｜", 1))
        entry_paragraphs = paragraphs(body)
        related = next((item.removeprefix("相关录音：") for item in entry_paragraphs if item.startswith("相关录音：")), "")
        entry_paragraphs = [item for item in entry_paragraphs if not item.startswith("相关录音：")]
        result.append({
            "kind": "artist",
            "id": ARTIST_IDS[name],
            "name": name,
            "subtitle": subtitle,
            "image": public_image(body),
            "paragraphs": entry_paragraphs,
            "meta": [{"label": "相关录音", "value": related}] if related else [],
            "sourceUrl": f"{PUBLIC_BASE}/sources.md",
        })
    return result


def parse_albums() -> list[dict[str, object]]:
    result: list[dict[str, object]] = []
    for heading, body in sections(read("albums.md"), 2):
        title, subtitle = (part.strip() for part in heading.split("｜", 1))
        album_id = ALBUM_IDS[title]
        result.append({
            "kind": "album",
            "id": album_id,
            "title": title,
            "subtitle": subtitle,
            "image": public_image(body),
            "artistIds": ALBUM_ARTISTS[album_id],
            "paragraphs": paragraphs(body),
            "meta": [],
            "sourceUrl": f"{PUBLIC_BASE}/sources.md",
        })
    return result


def parse_track_meta(body: str) -> tuple[list[dict[str, str]], str]:
    meta: list[dict[str, str]] = []
    remaining: list[str] = []
    for line in body.splitlines():
        match = re.match(r"\*\*(创作者|原作|录音|演奏)\*\*：(.*?)(?:<br>)?$", line.strip())
        if match:
            meta.append({"label": match.group(1), "value": plain(match.group(2))})
        else:
            remaining.append(line)
    return meta, "\n".join(remaining)


def parse_tracks() -> list[dict[str, object]]:
    result: list[dict[str, object]] = []
    for album_heading, album_body in sections(read("tracks.md"), 2):
        album_id = ALBUM_IDS[album_heading]
        track_sections = sections(album_body, 3)
        ids = TRACK_IDS[album_id]
        if len(track_sections) != len(ids):
            raise ValueError(f"{album_heading}: expected {len(ids)} tracks, found {len(track_sections)}")
        for track_id, (heading, body) in zip(ids, track_sections, strict=True):
            title = re.sub(r"^\d+\.\s*", "", heading)
            meta, prose = parse_track_meta(body)
            result.append({
                "kind": "track",
                "id": track_id,
                "title": title,
                "albumId": album_id,
                "paragraphs": paragraphs(prose),
                "meta": meta,
                "sourceUrl": f"{PUBLIC_BASE}/sources.md",
            })
    return result


def main() -> None:
    catalog = json.loads(read("catalog.json"))
    artists = parse_artists()
    albums = parse_albums()
    tracks = parse_tracks()
    payload = {
        "schemaVersion": 1,
        "verifiedAt": catalog["verifiedAt"],
        "language": "zh-CN",
        "sourcesUrl": f"{PUBLIC_BASE}/sources.md",
        "artists": artists,
        "albums": albums,
        "tracks": tracks,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(ROOT)}: {len(artists)} artists, {len(albums)} albums, {len(tracks)} tracks")


if __name__ == "__main__":
    main()
