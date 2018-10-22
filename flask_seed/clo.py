import re
from functools import reduce
from pydoc import locate

__all__ = ['register']

TYPE_REGEX = re.compile(":type (?P<name>[\*\w]+): (?P<type>\w+)", re.S)
PARAM_REGEX = re.compile(
    ":param (?P<name>[\*\w]+): (?P<doc>.*?)(?:(?=:params)|(?=:type)|\Z)", re.S)


def parse_params(docstring):
    desc = docstring.strip().split('\n', 1)[0]
    types = {name: locate(tpe.strip()) for name, tpe in
             TYPE_REGEX.findall(docstring)}
    return desc, [
        {'name': name, 'doc': doc.strip(), 'type': types.get(name, str)} for
        name, doc in PARAM_REGEX.findall(docstring)]


def optionize(option, clo):
    arg = '--' + clo['name']
    short = arg[1:3]
    return option(short, arg, default=clo['type'](), help=clo['doc'],
                  type=clo['type'])


def flip_partial(inner, wrapper):
    return wrapper(inner)


def register(command, option, *wrappers):
    def dec(f):
        desc, clos = parse_params(f.__doc__ or "")
        options = [optionize(option, clo) for clo in clos] + list(wrappers)
        options.reverse()
        func = reduce(flip_partial, options, f)
        func.__doc__ = desc
        return command()(func)

    return dec
