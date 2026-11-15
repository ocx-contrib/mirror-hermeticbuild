---
title: bsdtar
description: libarchive's bsdtar as one static binary, prebuilt by hermeticbuild — creates, lists and extracts tar, zip, 7z and other archive formats
keywords: bsdtar,libarchive,tar,zip,archive,compression,static,hermetic,cli
---

# bsdtar

A prebuilt, statically linked [bsdtar](https://www.libarchive.org/), the `tar`
front end of libarchive, published by
[hermeticbuild](https://github.com/hermeticbuild/bsdtar-prebuilt) for Linux,
macOS and Windows on amd64 and arm64. It reads and writes tar, pax, cpio, zip
and 7z archives and detects compression (gzip, bzip2, xz, zstd) on its own, so
the same command behaves the same on every platform.

## What's included

- **tar** — the executable. It keeps upstream's file name, so with this package
  on `PATH` the command `tar` is bsdtar, not the host's tar. On Windows the file
  is `tar.exe`.

Versions read `<libarchive version>+<NN>`, where `NN` is upstream's packaging
revision of that libarchive release (`3.8.1+03` is the third rebuild of
libarchive 3.8.1). The `3.8.1` tag always follows the newest revision.

## Usage notes

Format is chosen with `--format`, and `-a` picks it from the file name:

```sh
tar -a -cf bundle.zip dir/      # zip, chosen by the .zip suffix
tar -tf bundle.zip              # list any supported archive
tar -xf bundle.zip -C out/      # extract into an existing directory
```
