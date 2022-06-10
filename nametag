#!/usr/bin/python3
# encoding: utf-8
# SPDX-FileCopyrightText: 2022 FC Stegerman <flx@obfusk.net>
# SPDX-License-Identifier: GPL-3.0-or-later

# --                                                            ; {{{1
#
# File        : nametag
# Maintainer  : FC Stegerman <flx@obfusk.net>
# Date        : 2022-06-10
#
# Copyright   : Copyright (C) 2022  FC Stegerman
# Version     : v0.1.0
# License     : GPLv3+
#
# --                                                            ; }}}1

                                                                # {{{1
r"""

nametag - set audio file tags based on file name

nametag uses regular expressions to parse paths of audio files and
then sets the file tags based on the parsed data.  This allows you to
keep paths and tags in sync by creating the tags from the paths.

Everything is configurable with some custom python code: the path
regexes, the character substitution, and the handling of special
cases.  For example, the album "if_then_else" by The Gathering should
not have its underscores changed to spaces.


Examples
========

# dry run (do not modify files) + verbose (shows info)
$ nametag -v --dry-run Between_the_Buried_and_Me/04-Colors_\(2007\)/05-Ants_of_the_Sky.mp3
/.../Between_the_Buried_and_Me/04-Colors_(2007)/05-Ants_of_the_Sky.mp3:
  artist='Between the Buried and Me' album='Colors' track='05' title='Ants of the Sky' ext='mp3' album_n='04' year='2007'

# extra verbose (shows info before and after processing)
$ nametag -vv Between_the_Buried_and_Me/04-Colors_\(2007\)/05-Ants_of_the_Sky.mp3
/.../Between_the_Buried_and_Me/04-Colors_(2007)/05-Ants_of_the_Sky.mp3:
  - artist='Between_the_Buried_and_Me' album='Colors' track='05' title='Ants_of_the_Sky' ext='mp3' album_n='04' year='2007'
  + artist='Between the Buried and Me' album='Colors' track='05' title='Ants of the Sky' ext='mp3' album_n='04' year='2007'


Configuration
=============

$ bat ~/.nametagrc.py
───────┬──────────────────────────────────────────────────────────────────────────────────
       │ File: /.../.nametagrc.py
       │ Size: 501 B
───────┼──────────────────────────────────────────────────────────────────────────────────
   1   │ # regexes array; each one is tried in turn to match the path; the
   2   │ # default regex (nametag.RX) matches paths as in the examples above.
   3   │ regexes.append(re.compile(r'''...'''))
   4   │
   5   │ # character substitutions; the default is { "_|": " /" }
   6   │ tr["~"] = "_"
   7   │
   8   │ # custom processing rules; each one is tried in turn until one returns a value
   9   │ @rule
  10   │ def if_then_else(info, tr):
  11   │   if info.artist == "The_Gathering" and info.album == "if_then_else":
  12   │     return info._map_values(lambda k, v: v if k == "album" else tr(v))
───────┴──────────────────────────────────────────────────────────────────────────────────

$ nametag --show-config
=== config ===
regexes:
  '/(?P<artist>[^/]*)/(?:(?P<album_n>\\d+)-)?(?P<album>[^/]*?)(?:_\\((?P<year>\\d{4})\\))?/(?P<track>\\d+)(?:-(?P<title>[^/]*))?\\.(?P<ext>mp3|ogg|flac)\\Z'
  '...'
tr: {'_|': ' /', '~': '_'}
rules: if_then_else


Tests
=====

>>> regexes, tr_f, rules = configure()
>>> rule = rule_decorator()
>>> @rule
... def if_then_else(info, tr):
...   if info.artist == "The_Gathering" and info.album == "if_then_else":
...     return info._map_values(lambda k, v: v if k == "album" else tr(v))
>>> rules += rule.rules

>>> fn = ".../Between_the_Buried_and_Me/04-Colors_(2007)/05-Ants_of_the_Sky.mp3"
>>> RX.search(fn) is not None
True
>>> info = parse(fn, regexes)
>>> info
Info(artist='Between_the_Buried_and_Me', album='Colors', track='05', title='Ants_of_the_Sky', ext='mp3', album_n='04', year='2007')
>>> info_ = process(info, tr_f, rules)
>>> info_
Info(artist='Between the Buried and Me', album='Colors', track='05', title='Ants of the Sky', ext='mp3', album_n='04', year='2007')
>>> print(str(info_))
artist='Between the Buried and Me' album='Colors' track='05' title='Ants of the Sky' ext='mp3' album_n='04' year='2007'

>>> fn = ".../Opeth/08-Ghost_Reveries_(2005)/05-Reverie|Harlequin_Forest.mp3"
>>> RX.search(fn) is not None
True
>>> info = parse(fn, regexes)
>>> info
Info(artist='Opeth', album='Ghost_Reveries', track='05', title='Reverie|Harlequin_Forest', ext='mp3', album_n='08', year='2005')
>>> info_ = process(info, tr_f, rules)
>>> info_
Info(artist='Opeth', album='Ghost Reveries', track='05', title='Reverie/Harlequin Forest', ext='mp3', album_n='08', year='2005')
>>> print(str(info_))
artist='Opeth' album='Ghost Reveries' track='05' title='Reverie/Harlequin Forest' ext='mp3' album_n='08' year='2005'

>>> fn = ".../The_Gathering/03-if_then_else_(2000)/01-Rollercoaster.mp3"
>>> RX.search(fn) is not None
True
>>> info = parse(fn, regexes)
>>> info
Info(artist='The_Gathering', album='if_then_else', track='01', title='Rollercoaster', ext='mp3', album_n='03', year='2000')
>>> info_ = process(info, tr_f, rules)
>>> info_
Info(artist='The Gathering', album='if_then_else', track='01', title='Rollercoaster', ext='mp3', album_n='03', year='2000')
>>> print(str(info_))
artist='The Gathering' album='if_then_else' track='01' title='Rollercoaster' ext='mp3' album_n='03' year='2000'

"""                                                             # }}}1

import re, sys
from collections import namedtuple
from pathlib import Path

import click, taglib

__version__ = "0.1.0"
name        = "nametag"

RCFILE = Path.home() / ".nametagrc.py"

# default pattern; matches artist, album, track, title, ext;
# optionally: album_n, year; matches e.g.
# "Between_the_Buried_and_Me/04-Colors_(2007)/05-Ants_of_the_Sky.mp3"
RX = re.compile(r"""
  / (?P<artist> [^/]* )
  / (?: (?P<album_n> \d+ ) - )?
    (?P<album> [^/]*? )
    (?: _\( (?P<year> \d{4} ) \) )?
  / (?P<track> \d+ ) (?: - (?P<title> [^/]* ) )?
    \. (?P<ext> mp3 | ogg | flac ) \Z"""[3:], re.X)

# default character substitution
TR = { "_|": " /" }

Info = namedtuple("Info", "artist album track title ext album_n year".split(), defaults = (None, None))
Info._map_values = lambda self, f: type(self)(**{ k: f(k, v) for k, v in self._asdict().items() })
Info.__str__ = lambda self: " ".join(f"{k}={repr(v)}" for k, v in self._asdict().items())

@click.command(help = "set audio file tags based on file name")
@click.option("-c", "--config-file",
              type = click.Path(exists = True, path_type = Path),
              help = "Configuration file.  [default: ~/.nametagrc.py]")
@click.option("-n", "--dry-run", "--no-act", is_flag = True,
              help = "Do not modify files.")
@click.option("--show-config", is_flag = True,
              help = "Show config values before processing files (if any).")
@click.option("-v", "--verbose", count = True, help = "Be verbose.")
@click.argument("files", nargs = -1, type = click.Path(exists = True))
@click.version_option(__version__)
@click.pass_context
def cli(ctx, config_file, dry_run, show_config, verbose, files):
  if config_file is None and RCFILE.exists():
    config_file = RCFILE
  regexes, tr_f, rules = configure(config_file, show_config)
  for f in files:
    fn = str(Path(f).resolve())
    if info := parse(fn, regexes):
      info_ = process(info, tr_f, rules)
      if verbose:
        print(f"{fn}:")
        print(f"  - {info}\n  + {info_}" if verbose > 1 else f"  {info_}")
        print()
      if not dry_run:
        tag(fn, info_)
    else:
      print(f"parse failed for: {f}", file = sys.stderr)
      ctx.exit(1)

def configure(config_file = None, show_config = False):
  """
    Get config; executes config_file as python code w/ custom scope;
    returns (regexes, tr_f, rules).
  """
  cfg = dict(regexes = [RX], tr = TR.copy(), rule = rule_decorator())
  if config_file is not None:
    with config_file.open() as fh:
      exec(fh.read(), dict(re = re, **cfg))
  trans   = mktrans(cfg["tr"])
  tr_f    = lambda s: s and s.translate(trans)
  regexes = [ re.compile(r) if isinstance(r, str) else r for r in cfg["regexes"] ]
  rules   = cfg["rule"].rules
  if show_config:
    print("=== config ===")
    print("regexes:")
    for r in regexes:
      s = repr(r.pattern)       # FIXME: might remove spaces in classes
      print("  " + (re.sub(r"(\\n|\s)+", "", s) if r.flags & re.X else s))
    print("tr:", cfg["tr"])
    print("rules:", ", ".join(r.__code__.co_name for r in rules))
    print()
  return (regexes, tr_f, rules)

def rule_decorator():
  """Get @rule decorator that appends functions to .rules."""
  def decorator(f):
    decorator.rules.append(f)
    return f
  decorator.rules = []
  return decorator

def parse(fn, regexes):
  """
    Parse file path using regexes; returns Info object for first match
    (or None if all failed).
  """
  for rx in regexes:
    if m := rx.search(fn):
      return Info(**m.groupdict())
  return None

def process(info, tr_f, rules):
  """
    Apply rules (first that returns a value) or default character
    substitution.
  """
  for r in rules:
    if info_ := r(info, tr_f):
      return info_ if isinstance(info_, Info) else Info(**info_)
  return info._map_values(lambda k, v: tr_f(v))

def mktrans(tr):
  """Turn tr dictionary into one for str.translate."""
  d = {}
  for k, v in tr.items():
    d.update(str.maketrans(k, v))
  return d

def tag(fn, info):
  """Tag file based on Info object."""
  t = taglib.File(fn)
  t.tags["ARTIST"]      = [info.artist]
  t.tags["ALBUM"]       = [info.album]
  t.tags["TRACKNUMBER"] = [info.track]
  t.tags["TITLE"]       = [info.title or f"[track {info.track}]"]
  if info.year:
    t.tags["DATE"]      = [info.year]
  t.save()

def main():
  cli(prog_name = name)

if __name__ == "__main__":
  if "--doctest" in sys.argv:
    verbose = "--verbose" in sys.argv
    import doctest
    if doctest.testmod(verbose = verbose)[0]: sys.exit(1)
  else:
    main()

# vim: set tw=70 sw=2 sts=2 et fdm=marker :
