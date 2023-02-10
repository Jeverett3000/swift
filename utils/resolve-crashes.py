#!/usr/bin/env python3

# A small utility to take the output of a Swift validation test run
# where some compiler crashers have been fixed, and move them into the
# "fixed" testsuite, removing the "--crash" in the process.

import os
import re
import sys


def execute_cmd(cmd):
    print(cmd)
    os.system(cmd)


# The regular expression we use to match compiler-crasher lines.
regex = re.compile(
    r'.*Swift(.*) :: '
    r'(compiler_crashers|compiler_crashers_2|IDE/crashers|SIL/crashers)'
    r'/(.*\.swift|.*\.sil).*')

# Take the output of lit as standard input.
for line in sys.stdin:
    if match := regex.match(line):
        suffix = match[2]
        filename = match[3]

        # Move the test over to the fixed suite.
        from_filename = f'validation-test/{suffix}/{filename}'
        to_filename = f'validation-test/{suffix}_fixed/{filename}'
        git_mv_cmd = f'git mv {from_filename} {to_filename}'
        execute_cmd(git_mv_cmd)

        # Replace "not --crash" with "not".
        sed_replace_not_cmd = f'sed -e "s/not --crash/not/" -i "" {to_filename}'
        execute_cmd(sed_replace_not_cmd)

        # Remove "// XFAIL: whatever" lines.
        sed_remove_xfail_cmd = f'sed -e "s|^//.*XFAIL.*$||g" -i "" {to_filename}'
        execute_cmd(sed_remove_xfail_cmd)

        # Remove "// REQUIRES: asserts" lines.
        sed_remove_requires_asserts_cmd = (
            f'sed -e "s|^//.*REQUIRES: asserts.*$||g" -i "" {to_filename}'
        )
        execute_cmd(sed_remove_requires_asserts_cmd)

        # "git add" the result.
        git_add_cmd = f'git add {to_filename}'
        execute_cmd(git_add_cmd)
