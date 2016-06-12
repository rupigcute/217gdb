#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import re

import pwndbg.memoize

NORMAL         = "\x1b[0m"
BLACK          = "\x1b[30m"
RED            = "\x1b[31m"
GREEN          = "\x1b[32m"
YELLOW         = "\x1b[33m"
BLUE           = "\x1b[34m"
PURPLE         = "\x1b[35m"
CYAN           = "\x1b[36m"
LIGHT_GREY = LIGHT_GRAY = "\x1b[37m"
FOREGROUND     = "\x1b[39m"
GREY = GRAY    = "\x1b[90m"
LIGHT_RED      = "\x1b[91m"
LIGHT_GREEN    = "\x1b[92m"
LIGHT_YELLOW   = "\x1b[93m"
LIGHT_BLUE     = "\x1b[94m"
LIGHT_PURPLE   = "\x1b[95m"
LIGHT_CYAN     = "\x1b[96m"
WHITE          = "\x1b[97m"
BOLD           = "\x1b[1m"
UNDERLINE      = "\x1b[4m"

def none(x): return str(x)
def normal(x): return colorize(x, NORMAL)
def black(x): return colorize(x, BLACK)
def red(x): return colorize(x, RED)
def green(x): return colorize(x, GREEN)
def yellow(x): return colorize(x, YELLOW)
def blue(x): return colorize(x, BLUE)
def purple(x): return colorize(x, PURPLE)
def cyan(x): return colorize(x, CYAN)
def light_gray(x): return colorize(x, LIGHT_GRAY)
def foreground(x): return colorize(x, FOREGROUND)
def gray(x): return colorize(x, GRAY)
def light_red(x): return colorize(x, LIGHT_RED)
def light_green(x): return colorize(x, LIGHT_GREEN)
def light_yellow(x): return colorize(x, LIGHT_YELLOW)
def light_blue(x): return colorize(x, LIGHT_BLUE)
def light_purple(x): return colorize(x, LIGHT_PURPLE)
def light_cyan(x): return colorize(x, LIGHT_CYAN)
def white(x): return colorize(x, WHITE)
def bold(x): return colorize(x, BOLD)
def underline(x): return colorize(x, UNDERLINE)
def colorize(x, color): return color + terminateWith(str(x), color) + NORMAL

@pwndbg.memoize.reset_on_stop
def generateColorFunctionInner(old, new):
    def wrapper(text):
        return new(old(text))
    return wrapper

def generateColorFunction(config):
    function = lambda x: x
    for color in str(config).split(','):
        function = generateColorFunctionInner(function, globals()[color.lower().replace('-', '_')])
    return function

def strip(x):
    return re.sub('\x1b\\[\d+m', '', x)

def terminateWith(x, color):
    return re.sub('\x1b\\[0m', NORMAL + color, x)

def ljust_colored(x, length, char=' '):
    return x + (length - len(strip(x))) * char


try:
    import pygments_arm
except ImportError:
    pygments_arm = None

try:
    import pygments.lexers
    import pygments.formatters
except ImportError:
    pygments = None


import pwndbg.config
syntax_highlight_style = pwndbg.config.Parameter('syntax-highlight-style', 'monokai', 'Source code / assembly syntax highlight stylename of pygments module')
def syntax_highlight(source, filename=None, language=None):
    # no syntax hightlight if pygment is not installed
    if not pygments:
        return False, source

    formatter_class = pygments.formatters.Terminal256Formatter
    formatter = formatter_class(style=str(syntax_highlight_style))

    lexer = None
    if language and language == 'ARM':
        if pygments_arm:
            lexer = pygments_arm.ArmLexer()

    try:
        if language:
            lexer = pygments.lexers.get_lexer_by_name(language)
        elif filename:
            lexer = pygments.lexers.get_lexer_for_filename(filename)
    except pygments.util.ClassNotFound:
        # no lexer for this file or invalid style
        pass

    if lexer:
        return True, pygments.highlight(source, lexer, formatter).rstrip()
    else:
        return False, source

