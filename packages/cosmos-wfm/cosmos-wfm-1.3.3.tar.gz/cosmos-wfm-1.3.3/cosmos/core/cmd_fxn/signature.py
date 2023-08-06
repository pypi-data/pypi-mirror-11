from inspect import getargspec
import re
from ... import NOOP
import funcsigs


def call(cmd_fxn, task):
    sig = funcsigs.signature(cmd_fxn)

    #TODO remoe argspec in favor of funcsigs
    argspec = getargspec(cmd_fxn)

    def get_params():
        for k in argspec.args:
            if k in task.tags:
                yield k, task.tags[k]

    params = dict(get_params())

    def validate_params():
        ndefaults = len(argspec.defaults) if argspec.defaults else 0
        for arg in argspec.args[1:-1 * ndefaults]:
            if arg not in params:
                raise AttributeError(
                    '%s requires the parameter `%s`, are you missing a tag?  Either provide a default in the cmd() '
                    'method signature, or pass a value for `%s` with a tag' % (cmd_fxn, arg, arg))

    validate_params()

    kwargs = dict()
    kwargs.update(task.input_map)
    kwargs.update(task.output_map)
    kwargs.update(params)

    out = cmd_fxn(**kwargs)

    assert isinstance(out, basestring), '%s did not return a str' % cmd_fxn
    return out


import decorator


def default_prepend(task):
    o = '#!/bin/bash\n' \
        'set -e\n' \
        'set -o pipefail\n' \
        'cd %s\n' % task.execution.output_dir

    if task.output_dir:
        o += 'mkdir -p %s\n' % task.output_dir

    # assert task.cmd_fxn == task

    # o += '\n#' + str(task.cmd_fxn.input_map)
    # o += '\n#' + str(task.cmd_fxn.output_map)
    # o += '\n# cmd fxn ' + str(task.cmd_fxn)
    # o += '\n# tags ' + str(task.tags)
    # o += '\n'
    o += "\n"
    return o


# def default_cmd_append(task):
#     return ''


def default_cmd_fxn_wrapper(task):
    def real_decorator(fxn, *args, **kwargs):
        r = fxn(*args, **kwargs)
        if r == NOOP:
            return NOOP
        else:
            return default_prepend(task) + r

    return decorator.decorator(real_decorator)
