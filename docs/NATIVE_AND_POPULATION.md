# Native server and population repair references

The three native patches are small source changes from the local rAthena setup. Kisul Water Spraying emits its dedicated application packet for solo casts once, while recursive party healing retains ordinary heal-value packets. Successful Lauda Agnus and Lauda Ramus cleansing emits the application-effect packet as well.

Local evidence included incremental compilation and isolated behavior checks. These patches have not been rebased and rebuilt against the current public rAthena fork in this package. Review them against the pinned server before applying; they are not compiled binaries or an automatic server installer.

The population policy patch is reference material from a custom route-aware engine. It includes finite healing supplies/reagents, safer resting and class-aware combat decisions. It depends on earlier custom route flags and profiles and is not a standalone patch for the stock engine. Its local simulations do not establish natural-looking gameplay or balanced map-clearing speed.

Accounts, characters, databases, container state and executables are absent. The client draft separately documents native skill-unit identity compatibility; do not globally reassign a shared unit ID to make one effect appear.

Original rAthena and Ragnarok Offline code retains its authorship and GPL terms. These references are derivative repair proposals, not a claim of authorship of the underlying server or population engine.
