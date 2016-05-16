#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#MIT License

#Copyright (c) 2016 Eric Beanland

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

# I could have just used configParser, but this was way more fun.

__author__ = 'Eric Beanland'
__date__ = '2016-05-15'
__version__ = '0.1'
__license__ = 'MIT'


import collections
import shlex


def parse_file(fileobj, config):
    """Parse the given fileobj and store the results in config."""
    tokenizer = shlex.shlex(fileobj, posix=True)
    tokenizer.wordchars += '.:'
    tokenizer.whitespace = tokenizer.whitespace.replace('\n', ',=')
    opts = {opt.name:opt for key, opt in config._opts.items()}
    for token in tokenizer:
        # skip newlines
        if token  != '\n':
            if token in opts:
                for t in _consume(tokenizer):
                    config[token] = opts[token].accumulate(config[token], t)
            else:
                config[token] = _last(tokenizer)


def _consume(tokenizer):
    for token in tokenizer:
        if token in {'\n', None}:
            raise StopIteration
        yield token


def _last(tokenizer):
    prev = None
    for token in tokenizer:
        if token in {'\n', None}:
            return prev
        prev = token


class Option:
    def __init__(self, default, name=None, type=str, required=False):
        self.name = name
        self.type = type
        self.default = default
        self.required = required

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__, self.name)

    def accumulate(self, initial, new):
        new = self.type(new)
        # don't modify initial, it belongs to the class not the instance!
        if initial is self.default:
            initial = initial.__class__()

        if hasattr(initial, 'append'):
            initial.append(new)
            return initial
        elif hasattr(initial, 'add'):
            initial.add(new)
            return initial

        return new


class ConfigMeta(type):
    @classmethod
    def __prepare__(metacls, name, bases, **kwds):
        return {}

    def __new__(cls, name, bases, namespace, **kwds):
        opts = {}
        # move Options to their own dict
        for key, val in list(namespace.items()):
            if isinstance(val, Option):
                opts[key] = val
                del namespace[key]
                # set name attr if it's not set
                if opts[key].name == None:
                    opts[key].name = key

        result = type.__new__(cls, name, bases, namespace)
        result._opts = opts
        return result


class ConfigDict(dict, metaclass=ConfigMeta):
    def __init__(self):
        dict.__init__(self)
        # set all the defaults
        for key, opt in self._opts.items():
            self[key] = opt.default


def boolean(string):
    if string.lower() in {'true', 'on', '1', 'yes'}:
        return True

    return False

