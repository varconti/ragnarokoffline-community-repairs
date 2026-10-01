# Repair coverage and contribution status

## Shared client defects

| Defect | Public material |
|---|---|
| Culled STR expiration; targeted repeat termination; attachment duration; undefined frame suppressing direction | Client PR #42 |
| Skill tree / Etc / level-up icon resource-name mismatch | Client PR #43 |
| Later item-description/icon/weapon-view overrides skipped by a global deduplication guard | Client PR #44 |
| Relative volume scaled twice and explicit zero ignored | Client PR #45 |
| Skill cast/success/hit separation, status variants, ground-unit cleanup, portal/ground audio, original references, color pulses and sphere counters | Broad client draft with an English scope note |
| Item icons, collection artwork, expanded skill icons, Spirit Handler body/weapon files, status-panel labels and palettes | Recovery manifests; not all absent or transformed resources are recoverable from this reference |
| Solo Kisul and successful Lauda cleanse application packets | Native source patches, not yet rebased public-server builds |
| Pet/random-option/footprint enum mismatches and navigation resources | Inventory and recipes; original tables remain user supplied |
| Companion replacement, storage/UI and account-deletion compatibility, weapon paths, broader sound scheduling and Web Audio changes | Local candidates in the repair ledger; not all have been ported or submitted |

The local item-artwork audit covered 402 equipment/card/ammunition IDs and 804 decoded images. These were local checks, not a public asset bundle.

## Class coverage

Accumulated local work covers Dragon Knight, Meister, Shadow Cross, Arch Mage, Cardinal, Windhawk, Imperial Guard, Biolo, Abyss Chaser, Elemental Master, Inquisitor, Troubadour, Trouvere, Sky Emperor, Soul Ascetic, Shinkiro, Shiranui, Night Watch, Hyper Novice and Spirit Handler, including relevant earlier jobs. `skill-mapping-inventory.json` and `repair-ledger.json` identify mappings and overlapping stages. They include NPC constants and aliases and are not a count of fully repaired player skills or a completion percentage.

A failed cast is inconclusive when weapon type, ammunition, reagents, SP/AP, party/duet state, target, map or prerequisites are unmet. It does not establish a missing animation or sound.

## Remaining uncertainty

Procedural visuals, clones/particles, halos, some direction/phase/variant behavior and dedicated visuals remain incomplete. Unknown original variant selection was deliberately skipped. Some effects are browser adaptations. `bash3d.wav` was not located; its invalid call was removed locally while retaining the visual.

The local comparison found 569 WAV files byte-identical to the available kRO reference. This does not verify skill association or official timing. Further association review and in-game audiovisual acceptance were excluded from this contribution round. Passing unit tests does not certify original-client fidelity.

## Distribution

Public explanatory text and contributed menus/configuration are English. Sprites, textures, audio, original client archives and private installation reports are not published. Resource paths may contain legacy Korean byte names; these are identifiers and must not be translated.
