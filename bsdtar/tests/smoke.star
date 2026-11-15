# bsdtar/tests/smoke.star — stable across upstream revisions.
# Asserts the contract (the executable is a libarchive bsdtar, and a hermetic
# create -> list -> extract round trip reproduces the written content), never
# help/version prose beyond the stable identity token below.
#
# The binary on PATH is `tar` (`tar.exe` on Windows) — upstream's own name, see
# asset_type in mirror.yml. That name is shared with every host's tar, so a
# green round trip alone would also pass for a host GNU tar if PATH resolution
# ever skipped the package. Two checks make the package's own binary the thing
# under test:
#   1. `--version` names `libarchive` — GNU tar never prints that token.
#   2. A zip round trip (`--format zip`) — GNU tar cannot write zip at all.
# (Windows ships its own bsdtar as System32\tar.exe, so there the identity
# checks are weaker; the package-first PATH composition is what ocx guarantees.)
#
# Everything the tool reads is written to scratch first; every path is relative
# so the same script runs on Windows. Extraction goes to a fresh directory so a
# pass proves bytes came out of the archive, not that the input was still there.
TAR = "tar.exe" if ocx.target_platform.os == ocx.os.Windows else "tar"

# Tier 1 + 2: liveness and identity.
r_version = ocx.run(TAR, "--version")
expect.ok(r_version)
expect.contains(r_version.stdout, "libarchive")
expect.matches(r_version.stdout, r"\d+\.\d+\.\d+")

ALPHA = "alpha content\nline two\n"
BETA = "beta: éè unicode and spaces  \n"
ocx.mkdir("src/sub")
ocx.write_file("src/alpha.txt", ALPHA)
ocx.write_file("src/sub/beta.txt", BETA)

# Tier 3a: tar (ustar/pax) create -> list -> extract.
r_create = ocx.run(TAR, "-cf", "out.tar", "-C", "src", "alpha.txt", "sub")
expect.ok(r_create)

r_list = ocx.run(TAR, "-tf", "out.tar")
expect.ok(r_list)
expect.contains(r_list.stdout, "alpha.txt")
expect.contains(r_list.stdout, "sub/beta.txt")

ocx.mkdir("extracted")
r_extract = ocx.run(TAR, "-xf", "out.tar", "-C", "extracted")
expect.ok(r_extract)
expect.eq(ocx.read_file("extracted/alpha.txt"), ALPHA)
expect.eq(ocx.read_file("extracted/sub/beta.txt"), BETA)

# Tier 3b: zip round trip — a format only a libarchive tar can write.
r_zip = ocx.run(TAR, "--format", "zip", "-cf", "out.zip", "-C", "src", "alpha.txt", "sub")
expect.ok(r_zip)
r_ziplist = ocx.run(TAR, "-tf", "out.zip")
expect.ok(r_ziplist)
expect.contains(r_ziplist.stdout, "sub/beta.txt")

ocx.mkdir("extracted_zip")
r_unzip = ocx.run(TAR, "-xf", "out.zip", "-C", "extracted_zip")
expect.ok(r_unzip)
expect.eq(ocx.read_file("extracted_zip/alpha.txt"), ALPHA)
expect.eq(ocx.read_file("extracted_zip/sub/beta.txt"), BETA)
