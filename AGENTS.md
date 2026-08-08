# Music Asset Repository Guidance

This public repository is the MP3 storage and GitHub Pages deployment for
RongYu's Notes. The sibling website repository is
`../RongYu221104.github.io`.

- Keep only MP3 media under `public/audio/`; website code, covers, and metadata
  belong in the website repository.
- Prepare delivered music by running `scripts/prepare_assets.py` from the
  sibling website repository. Do not edit files in its ignored `input/` area.
- Before committing, reconcile filenames with the website's
  `src/data/tracks.json` by running `pnpm verify:assets` there.
- Commit and deploy this repository before publishing website metadata that
  references a new or replaced track.
- Monitor `Deploy assets to GitHub Pages` and verify the exact production MP3
  URL returns `200`, the expected audio content type, and byte-range support.
- Remove an obsolete MP3 from current `HEAD` when it is replaced. Git history
  rewriting or a force push requires separate explicit approval.
- Never commit credentials, raw input files, covers, PDFs, or unrelated assets.
