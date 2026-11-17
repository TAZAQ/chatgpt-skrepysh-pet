# Contributing

Thanks for helping give Skrepysh a little more personality.

Visual polish is currently paused, but focused improvements and clear bug reports are welcome.

## Report a problem

Include your operating system, app name and version, installation method, and what you expected to see. For visual issues, attach a screenshot or short recording and mention the pet size and display scaling.

## Change artwork

1. Start with the references in [`sources/`](sources/README.md).
2. Preserve the v2 grid: **1536 × 2288 px**, with **192 × 208 px** cells.
3. Keep a transparent background and consistent character size and placement across frames.
4. Update both `spritesheet.png` and `skrepysh/spritesheet.webp` when changing the final artwork. Keep their visible content aligned.
5. Refresh `demo.gif` if the preview no longer represents the animations.

Source rows are references and may need cleanup and alignment before assembly. This repository does not yet include a sprite generation or assembly pipeline.

## Change metadata or documentation

Use English for documentation, user-facing names, and descriptions. Keep the package ID and directory name `skrepysh` stable. Save text as UTF-8 without a BOM, with LF line endings and a final newline.

## Verify a change

When a file listed in `checksums.json` changes, update its SHA-256 entry. From the repository root, run:

```sh
python3 - <<'PY'
import hashlib
import json
from pathlib import Path

manifest = Path("checksums.json")
paths = json.loads(manifest.read_text(encoding="utf-8"))
hashes = {name: hashlib.sha256(Path(name).read_bytes()).hexdigest() for name in paths}
manifest.write_text(json.dumps(hashes, indent=2) + "\n", encoding="utf-8")
PY
python3 scripts/verify.py
```

The update snippet uses a POSIX shell; on Windows, run it in Git Bash or WSL. The verifier itself also works with `py -3 scripts/verify.py` in PowerShell.

For artwork changes, also inspect the result in a compatible app at normal and small pet sizes. A passing checksum check confirms file integrity, not rendering quality. Describe what changed and include a before/after preview in your pull request.
