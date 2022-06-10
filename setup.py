from pathlib import Path
import setuptools

# from nametag import __version__                             #  FIXME
__version__ = "0.1.0"

info = Path(__file__).with_name("README.md").read_text(encoding = "utf8")

setuptools.setup(
  name              = "nametag",
  url               = "https://github.com/obfusk/nametag.py",
  description       = "set audio file tags based on file name",
  long_description  = info,
  long_description_content_type = "text/markdown",
  version           = __version__,
  author            = "FC Stegerman",
  author_email      = "flx@obfusk.net",
  license           = "GPLv3+",
  classifiers       = [
    "Development Status :: 4 - Beta",
    "Environment :: Console",
    "Intended Audience :: End Users/Desktop",
    "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
    "Operating System :: POSIX :: Linux",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: Implementation :: CPython",
    "Topic :: Multimedia :: Sound/Audio",
    "Topic :: Utilities",
  ],
  keywords          = "audio flac mp3 ogg regex tag",
  py_modules        = ["nametag"],
  entry_points      = dict(console_scripts = ["nametag = nametag:main"]),
  python_requires   = ">=3.8",
  install_requires  = ["click>=6.0", "pytaglib"],
)
