#!/usr/bin/python
# -*- coding: utf-8 -*-
from .tinytag import TinyTag, StringWalker, ID3, Ogg, Wave, Flac


__version__ = '0.9.3'

if __name__ == '__main__':
    print(TinyTag.get(sys.argv[1]))