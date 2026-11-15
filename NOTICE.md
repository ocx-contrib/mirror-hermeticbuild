# NOTICE

This repository packages and redistributes prebuilt `bsdtar` binaries published
by the [hermeticbuild/bsdtar-prebuilt](https://github.com/hermeticbuild/bsdtar-prebuilt)
project. The Apache-2.0 license in [`LICENSE`](LICENSE) covers the OCX pipeline
files authored here. It does **not** cover any redistributed binary, whose
licenses are recorded below.

The package logo reproduces the **hermeticbuild** organisation's own GitHub
avatar, traced and scaled to 512 px, solely to identify the distributor being
mirrored. No endorsement or affiliation is implied and no trademark right is
claimed.

| Package | GHCR path | Upstream SPDX |
|---|---|---|
| `bsdtar` | `ghcr.io/ocx-contrib/hermeticbuild/bsdtar` | `Apache-2.0` (packaging), `BSD-2-Clause` (libarchive) |

---

## `bsdtar`

Distributor: <https://github.com/hermeticbuild/bsdtar-prebuilt>
Published to `ghcr.io/ocx-contrib/hermeticbuild/bsdtar`.

This is a redistribution of third-party code that is itself a build of someone
else's code, so two licenses apply to the bytes.

| Component | SPDX | Holder |
|---|---|---|
| bsdtar-prebuilt (build scripts and patches) | **Apache-2.0** | Copyright the hermeticbuild authors |
| libarchive and its `bsdtar` front end (the code in the binary) | **BSD-2-Clause** | Copyright (c) 2003-2018 Tim Kientzle and the libarchive contributors |

Verified with `gh api repos/hermeticbuild/bsdtar-prebuilt/license --jq
.license.spdx_id`, which answers `Apache-2.0`. GitHub answers `NOASSERTION` for
libarchive because its `COPYING` is a multi-part file, so the license was
identified by hand from that file
(<https://github.com/libarchive/libarchive/blob/master/COPYING>): the bulk of
the code, including the `tar/` front end, is under the two-clause BSD license
reproduced at the bottom of it. A few files carry other permissive terms:
3-clause BSD (UC Regents), public domain, and a CC0 / OpenSSL / Apache-2.0
choice for the BLAKE2 sources. Only the build scripts have mixed terms, and
they are not redistributed. No license in play is copyleft.

The binary also statically links xz (liblzma) and bzip2, both permissively
licensed, as listed in upstream's `MODULE.bazel`. The build applies two small
patches to libarchive (Windows CRLF mtree handling and MinGW build fixes),
kept in upstream's `patches/` directory. This repository adds nothing.

Both main licenses allow binary redistribution on condition that the copyright
notice and license text accompany it. This notice and the links above meet that.
The binaries are republished byte for byte inside an OCX bundle.

The image annotation `org.opencontainers.image.licenses` is
`BSD-2-Clause AND Apache-2.0`. The source for each mirrored revision is the
tagged tree at <https://github.com/hermeticbuild/bsdtar-prebuilt> together with
libarchive at the version in the package version (`3.8.1+03` is libarchive
3.8.1).
