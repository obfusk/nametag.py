<!-- {{{1

    File        : README.md
    Maintainer  : FC Stegerman <flx@obfusk.net>
    Date        : 2022-06-10

    Copyright   : Copyright (C) 2022  FC Stegerman
    Version     : v0.1.0
    License     : GPLv3+

}}}1 -->

[![GitHub Release](https://img.shields.io/github/release/obfusk/nametag.py.svg?logo=github)](https://github.com/obfusk/nametag.py/releases)
[![PyPI Version](https://img.shields.io/pypi/v/nametag.svg)](https://pypi.python.org/pypi/nametag)
[![Python Versions](https://img.shields.io/pypi/pyversions/nametag.svg)](https://pypi.python.org/pypi/nametag)
[![CI](https://github.com/obfusk/nametag.py/workflows/CI/badge.svg)](https://github.com/obfusk/nametag.py/actions?query=workflow%3ACI)
[![GPLv3+](https://img.shields.io/badge/license-GPLv3+-blue.svg)](https://www.gnu.org/licenses/gpl-3.0.html)

## nametag - set audio file tags based on file name

nametag uses regular expressions to parse paths of audio files and
then sets the file tags based on the parsed data.  This allows you to
keep paths and tags in sync by creating the tags from the paths.

Everything is configurable with some custom python code: the path
regexes, the character substitution, and the handling of special
cases.  For example, the album `if_then_else` by The Gathering should
not have its underscores changed to spaces.

## Examples

```bash
# dry run (do not modify files) + verbose (shows info)
$ nametag -v --dry-run Between_the_Buried_and_Me/04-Colors_\(2007\)/05-Ants_of_the_Sky.mp3
/.../Between_the_Buried_and_Me/04-Colors_(2007)/05-Ants_of_the_Sky.mp3:
  artist='Between the Buried and Me' album='Colors' track='05' title='Ants of the Sky' ext='mp3' album_n='04' year='2007'

# extra verbose (shows info before and after processing)
$ nametag -vv Between_the_Buried_and_Me/04-Colors_\(2007\)/05-Ants_of_the_Sky.mp3
/.../Between_the_Buried_and_Me/04-Colors_(2007)/05-Ants_of_the_Sky.mp3:
  - artist='Between_the_Buried_and_Me' album='Colors' track='05' title='Ants_of_the_Sky' ext='mp3' album_n='04' year='2007'
  + artist='Between the Buried and Me' album='Colors' track='05' title='Ants of the Sky' ext='mp3' album_n='04' year='2007'
```

## Configuration

Example `~/.nametagrc.py`:

```python
# regexes array; each one is tried in turn to match the path; the
# default regex (nametag.RX) matches paths as in the examples above.
regexes.append(re.compile(r"""..."""))

# character substitutions; the default is { "_|": " /" }
tr["~"] = "_"

# custom processing rules; each one is tried in turn until one returns a value
@rule
def if_then_else(info, tr):
  if info.artist == "The_Gathering" and info.album == "if_then_else":
    return info._map_values(lambda k, v: v if k == "album" else tr(v))
```

```bash
$ nametag --show-config
=== config ===
regexes:
  '/(?P<artist>[^/]*)/(?:(?P<album_n>\\d+)-)?(?P<album>[^/]*?)(?:_\\((?P<year>\\d{4})\\))?/(?P<track>\\d+)(?:-(?P<title>[^/]*))?\\.(?P<ext>mp3|ogg|flac)\\Z'
  '...'
tr: {'_|': ' /', '~': '_'}
rules: if_then_else
```

## Help

```bash
$ nametag --help
```

## Tab Completion

For Bash, add this to `~/.bashrc`:

```bash
eval "$(_NAMETAG_COMPLETE=source_bash nametag)"
```

For Zsh, add this to `~/.zshrc`:

```zsh
eval "$(_NAMETAG_COMPLETE=source_zsh nametag)"
```

For Fish, add this to `~/.config/fish/completions/nametag.fish`:

```fish
eval (env _NAMETAG_COMPLETE=source_fish nametag)
```

## Requirements

* Python >= 3.8 + click + pytaglib.

### Debian/Ubuntu

```bash
$ apt install python3-click python3-taglib
```

## Installing

### Using pip

```bash
$ pip install nametag
```

NB: depending on your system you may need to use e.g. `pip3 --user`
instead of just `pip`.

### From git

NB: this installs the latest development version, not the latest
release.

```bash
$ git clone https://github.com/obfusk/nametag.py.git
$ cd nametag
$ pip install -e .
```

NB: you may need to add e.g. `~/.local/bin` to your `$PATH` in order
to run `nametag`.

To update to the latest development version:

```bash
$ cd nametag
$ git pull --rebase
```

## License

[![GPLv3+](https://www.gnu.org/graphics/gplv3-127x51.png)](https://www.gnu.org/licenses/gpl-3.0.html)

<!-- vim: set tw=70 sw=2 sts=2 et fdm=marker : -->
