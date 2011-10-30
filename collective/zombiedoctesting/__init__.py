# -*- coding: utf-8 -*-
"""Zombie.js-doctesting decorator"""
import doctest
import subprocess

def browser(url,
            options=doctest.NORMALIZE_WHITESPACE + doctest.ELLIPSIS,
            mapping={},
            debug=False):

    def decorator(func):
        def wrapper(*args):
            parser = doctest.DocTestParser()
            checker = doctest.OutputChecker()

            test = doctest.DocTest(
                parser.get_examples(func.__doc__ % mapping), {},
                func.func_name, func.__code__.co_filename,
                func.__code__.co_firstlineno, func.__doc__)

            beginning = u"""\
async = require "async"
zombie = require "zombie"
browser = new zombie.Browser
browser.setMaxListeners(100)
# on every 'all events done', update globals from browser.window
do ->
  global_keys = []
  browser.on "done", (browser) ->
      for own key in global_keys
          global[key] = undefined
          delete global[key]
      global_keys = []
      for own key of browser.window
          global[key] = browser.window[key]
          global_keys.push key
# perform serial processing of doctest examples
async.series [
    (async_callback) ->
        browser.location = "%s"
        do async_callback
""" % url
            step_sep = ("-" * 80)
            step_start = u"""\
    (async_callback) ->
        console.log "%s"
        browser.wait (err, browser, status) ->
""" % step_sep
            step_end = u"do async_callback\n"
            end = u"""\
]
"""

            def indent(s, n):
                return "\n".join([line and (" " * n) + line or line
                                  for line in s.split("\n")])

            story = beginning
            for example in test.examples:
                story += step_start
                story += indent(example.source, 12)
                last_line = story.split("\n")[-2]
                last_indent = len(last_line) - len(last_line.lstrip())
                story += indent(step_end, last_indent)
            story += end

            if debug:
                print story

            coffee = subprocess.Popen(["coffee", "-s"], shell=False,
                stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            out, err = coffee.communicate(story)

            for example in test.examples:
                try:
                    if step_sep in out:
                        results = out.split(step_sep + "\n")[1:]
                        got = results[test.examples.index(example)]
                    else:
                        got = out
                except IndexError:
                    got = "undefined"
                if not checker.check_output(example.want, got, options):
                    raise doctest.DocTestFailure(test, example, got)

            return func(*args)
        return wrapper
    return decorator
