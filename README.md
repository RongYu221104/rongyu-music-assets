# RongYu's Notes — Music Assets

Media repository for RongYu's Notes. It stores the MP3 audio files served by
the website player and the independently sourced background-reading archive.

## Layout

- `public/audio/*.mp3` — audio tracks, published at
  `https://rongyu221104.github.io/rongyu-music-assets/audio/<filename>.mp3`
- `public/music-context/` — verified Chinese artist, album, and track notes,
  including licensed portraits, source links, and a machine-readable index

## Deployment

Pushed to `main`, the `Deploy assets to GitHub Pages` workflow publishes the
`public/` directory through GitHub Pages (Source: GitHub Actions). The
website repository is `RongYu221104/RongYu221104.github.io`; player code and
its own UI metadata stay there. Research notes and their attributed images
remain in this music repository.

## Adding Music

1. Put the original MP3 into the website repo's local `input/music/` (ignored).
2. Run `scripts/prepare_assets.py` in the website repo; it writes the MP3 here
   and the cover into the website repo.
3. Commit and deploy this repository first, then the website repository.
