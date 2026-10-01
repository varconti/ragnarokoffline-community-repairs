# Ragnarok Offline community repairs

English code, evidence and local recovery recipes from an extensively customized Renewal setup. This repository complements focused contributions to [Flux159/roBrowserLegacy](https://github.com/Flux159/roBrowserLegacy), the client fork used by [Ragnarok Offline](https://github.com/Flux159/ragnarokoffline.app).

## Client contributions

- [PR #42](https://github.com/Flux159/roBrowserLegacy/pull/42): effect duration, repeat termination and attachment direction.
- [PR #43](https://github.com/Flux159/roBrowserLegacy/pull/43): missing skill-icon alias fallback, including Etc rows.
- [PR #44](https://github.com/Flux159/roBrowserLegacy/pull/44): later item-metadata overrides can repair descriptions, image links and weapon views.
- [PR #45](https://github.com/Flux159/roBrowserLegacy/pull/45): global/relative sound volume and explicit silence.
- A separate broad draft carries accumulated skill mappings and lifecycle controllers for maintainer review. It is not a fully certified replacement client or an application vendor-pin update.

## What is included

- [Repair coverage and limitations](docs/BUG_FIXES.md), an English skill-mapping inventory and a repair ledger.
- [All 26 local mods classified](docs/MOD_INVENTORY.md). Stock packs keep their original authorship; custom progression/economy is not proposed as default game balance.
- Twenty resource-recovery recipes with 6,088 entries across overlapping mods. 4,198 entries matched the original resource at the same path in the available reference; duplicate entries are not distinct recovered files. Remaining entries have unresolved, different or unsupported source resources and are explicitly marked.
- Two optional source/configuration mods: `crowded-world` and `siroma-no-orc`.
- Native Kisul/Lauda source proposals and a route-population policy reference. [Integration limits](docs/NATIVE_AND_POPULATION.md) explain why these are not automatic stock-server installations.
- A dependency-free Python extraction tool for compatible, unencrypted GRF 2.0 / 3.0 resources, including a GRF inside an uncompressed TAR.

## Recover resources locally

Supply your own compatible reference client. This repository includes no game assets and does not download them. Use a separate output folder first:

```sh
python3 tools/recover_resources.py \
  --source /path/to/your/data.grf \
  --manifest manifests/skill-closeout-pneuma-audio.json \
  --output ./recovered \
  --verify-only
```

Remove `--verify-only` to build the local mod. Copy the generated mod directory into your installation's `state/mods`, then enable it in Settings > Mods and apply. Restore/disable through the app's normal mod workflow. The generated metadata starts disabled.

The tool writes only files with the expected SHA-256. Unresolved or mismatched files are skipped, listed in `RECOVERY.json`, and produce exit status 2. A partial recovery must not be called complete. Encrypted resources, a different reference version, and genuinely absent files need a compatible source or separate investigation.

Some resource names contain legacy Korean bytes represented as Latin-1 characters. They are exact identifiers, not untranslated public UI, and must remain unchanged.

## Validation and scope

Run the extractor regression tests with `python3 -m unittest discover -s tests`. They cover synthetic GRF reading, successful recovery, reference-hash mismatch, verify-only behavior and path traversal. The extractor was also checked against a real local GRF 3.0 TAR without writing game files.

Client PRs contain their own source tests and build results. Prior local checks and newly run public-fork checks are distinguished in the reports. Sound association and in-game audiovisual fidelity were not newly certified. This work improves compatibility but does not establish that every skill is identical to the official client.

The custom Builder, leveling guide and several NPC packs still need a complete English menu/configuration port before they can be released as source mods. They are inventoried here; their Portuguese source is not uploaded. Other candidates such as the larger Web Audio rewrite and companion/UI changes remain local review candidates. This repository does not represent them as merged upstream.

## Attribution

Ragnarok Offline, roBrowserLegacy, rAthena and the Population Engine retain their original authorship. The source mods and derivative patch proposals are distributed under GPL-3.0 with their upstream notices preserved. No Gravity sprites, textures, WAVs, GRFs, executables, account data or character databases are included.
