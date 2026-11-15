# /// script
# requires-python = ">=3.13"
# dependencies = ["ocx-mirror-sdk~=0.6.0"]
# ///
# SPDX-License-Identifier: Apache-2.0
"""Generate url_index JSON for hermeticbuild/bsdtar-prebuilt.

Upstream tags are irregular packaging revisions over a libarchive version:

    v3.7.2  v3.7.2-1  v3.7.4  v3.7.4-2  v3.7.4-3  v3.7.4-4  v3.7.5  v3.7.5-1
    v3.7.5-2  v3.7.9  v3.8.1  v3.8.1-fix.1  v3.8.1-3

Each revision ships different bytes (a rebuild, not a re-label), so every tag
is mirrored. The ocx version is `<libarchive>+<NN>` with NN the packaging
revision zero-padded to two digits (plain tag -> `00`, `-N`/`-fix.N` -> `N`).
Build metadata is what ocx orders as a tiebreak after the semver triple, and it
compares as a STRING, so the padding keeps `+10` above `+09`. Plain tags get
`+00` rather than a bare `3.8.1` so they never collide with the rolling cascade
tag `3.8.1`. A prerelease mapping (`3.8.1-3`) was rejected: it sorts BELOW
`3.8.1`, so the newest rebuild would never become the cascade head.

Each asset carries the sha256 from the release's own SHA256.txt, checked by
`verify.url_index_digest: require` in mirror.yml.
"""

from __future__ import annotations

import json
import re
import sys
import urllib.request

from ocx_mirror_sdk import github

REPO = "hermeticbuild/bsdtar-prebuilt"
TAG_RE = re.compile(r"^v(?P<ver>\d+\.\d+\.\d+)(?:-(?:fix\.)?(?P<rev>\d+))?$")
# Assets whose bytes do not match their name, measured with `file` on the
# downloaded release assets (not guessed). Emitting them would publish a wrong
# binary under a platform key, and the CI leg either fails to spawn it or passes
# it under emulation and verifies the wrong architecture.
#   v3.7.5   tar_windows_amd64.exe  ELF 64-bit LSB executable (a Linux binary)
#   v3.7.9, v3.8.1, v3.8.1-fix.1
#            tar_windows_arm64.exe  PE32+ x86-64 (not ARM64)
# The first genuine ARM64 PE is v3.8.1-3 (`file`: PE32+ ... ARM64).
MISLABELED = {
    ("v3.7.5", "tar_windows_amd64.exe"),
    ("v3.7.9", "tar_windows_arm64.exe"),
    ("v3.8.1", "tar_windows_arm64.exe"),
    ("v3.8.1-fix.1", "tar_windows_arm64.exe"),
}
ASSET_RE = re.compile(r"^tar_(linux|darwin|windows)_[a-z0-9_]+(\.exe)?$")


def log(msg: str) -> None:
    sys.stderr.write(f"generate: {msg}\n")


def checksums(url: str) -> dict[str, str]:
    """Parse a `sha256sum`-format sidecar into {asset name: hex}."""
    with urllib.request.urlopen(url, timeout=60) as resp:  # noqa: S310 - fixed https URL
        text = resp.read().decode()
    out = {}
    for line in text.splitlines():
        parts = line.split()
        if len(parts) == 2:
            out[parts[1].lstrip("*")] = parts[0]
    return out


def main() -> int:
    versions: dict[str, dict] = {}
    for rel in github.list_releases(REPO, include_prereleases=False, include_drafts=False):
        m = TAG_RE.match(rel.tag_name)
        if m is None:
            log(f"skip unrecognised tag {rel.tag_name}")
            continue
        version = f"{m['ver']}+{int(m['rev'] or 0):02d}"
        if version in versions:
            log(f"collision: {rel.tag_name} maps to {version} twice")
            return 1
        urls = {a.name: a.browser_download_url for a in rel.assets}
        sums_url = urls.get("SHA256.txt")
        if sums_url is None:
            log(f"{rel.tag_name}: no SHA256.txt, refusing to emit unverified assets")
            return 1
        sums = checksums(sums_url)
        assets = {}
        for name, url in urls.items():
            if not ASSET_RE.match(name):
                continue
            if (rel.tag_name, name) in MISLABELED:
                log(f"{rel.tag_name}: skip mislabeled {name}")
                continue
            if name not in sums:
                log(f"{rel.tag_name}: {name} missing from SHA256.txt")
                return 1
            assets[name] = {"url": url, "sha256": sums[name]}
        if assets:
            versions[version] = {"prerelease": False, "assets": assets}
            log(f"  {version} <- {rel.tag_name} ({len(assets)} assets)")

    if not versions:
        log("no versions generated")
        return 1
    json.dump({"versions": versions}, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
