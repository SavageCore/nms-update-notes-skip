# Update Notes Skip

Skips the No Man's Sky update notes page that opens automatically on
startup after a game update.

A [Nozavolochen](https://github.com/Nozavolochen/framework) mod:
the runtime patch is declared in `mod.toml` and applied by the
shared host DLL at game boot.

## Install

Requires the **Nozavolochen Framework** file (required dependency,
provides `Binaries/xinput9_1_0.dll`).

Install `dist/Update Notes Skip.zip` as a normal mod into `GAMEDATA/MODS`
([Amethyst](https://github.com/ChrisDKN/Amethyst-Mod-Manager)) so you end
up with `GAMEDATA/MODS/Update Notes Skip/mod.toml`. The framework file provides
the host DLL.

You should then have:

- `Binaries/xinput9_1_0.dll`: the Nozavolochen host, from the framework
  file (Windows DLL, runs under Proton with
  `WINEDLLOVERRIDES="xinput9_1_0=n,b" %command%`).
- `GAMEDATA/MODS/Update Notes Skip/`: `mod.toml` with the patch spec
  and toggles.

After launch, `Binaries/nozavolochen.log` is created to help with
debugging.

## Build (on Linux)

Requires a Rust toolchain with the `x86_64-pc-windows-gnu` target and
mingw for the host DLL, plus a checkout of the framework repo (override
with `FRAMEWORK_HOME=...`).

```sh
make release      # verify spec + pack dist/ zip (default)
make loader       # build the Nozavolochen host DLL via the framework (dev testing)
make rootzip      # pack the root-install archive (no re-verify)
make assets       # regenerate the Nexus page images (needs Pillow)
make clean        # remove build/ and dist/
```
