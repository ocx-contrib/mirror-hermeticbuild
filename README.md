# mirror-hermeticbuild

OCX mirror for [hermeticbuild/bsdtar-prebuilt](https://github.com/hermeticbuild/bsdtar-prebuilt),
statically linked builds of libarchive's `bsdtar`. One repository, one spec
directory per package.

| Package | Spec | Publishes to | Announced as | Upstream SPDX |
|---|---|---|---|---|
| [bsdtar](https://github.com/hermeticbuild/bsdtar-prebuilt) | [`bsdtar/mirror.yml`](bsdtar/mirror.yml) | `ghcr.io/ocx-contrib/hermeticbuild/bsdtar` | [`ocx.sh/hermeticbuild/bsdtar`](https://index.ocx.sh/hermeticbuild/bsdtar) | `Apache-2.0` (packaging), `BSD-2-Clause` (libarchive) |

The namespace names the distributor whose bytes are shipped, and the package
names what the bytes are. The executable on `PATH` keeps upstream's file name,
`tar` (`tar.exe` on Windows), so putting this package on `PATH` shadows the
host's `tar` on purpose.

## Layout

```
bsdtar/
├── mirror.yml          the spec, never at the repo root
├── metadata.json       bundle interface
├── CATALOG.md          published by ocx package describe
├── scripts/generate.py url_index generator, maps upstream tags to versions
└── tests/smoke.star    create, list and extract round trip
```

`logo.svg` and `logo.png` sit at the repo root and the spec names them through
`catalog.logo`. `LICENSE` and `NOTICE.md` are shared.

## Versions

Upstream tags are irregular packaging revisions (`v3.8.1`, `v3.8.1-fix.1`,
`v3.8.1-3`), and each ships different bytes. The generator turns the revision
into build metadata, so `v3.8.1-3` becomes `3.8.1+03` and the plain tag becomes
`3.8.1+00`. The two-digit padding is deliberate, because build metadata sorts as
a string. The reasoning and the alternatives measured are in the comment block of
[`bsdtar/mirror.yml`](bsdtar/mirror.yml).

## Editing

```sh
ocx exec -- task setup
ocx-mirror package validate bsdtar/mirror.yml
ocx-mirror package pipeline generate ci --spec bsdtar/mirror.yml
```

Never hand-edit `.github/workflows/`. Change the spec, then regenerate. The
`verify-generated` workflow fails on drift.
