# -*- coding: utf-8 -*-
from plone.recipe.codeanalysis.analyser import console_factory
from plone.recipe.codeanalysis.clean_lines import CleanLines
import re


class Imports(CleanLines):

    name = 'imports'
    title = 'Check imports'
    message = '{0:s}:{1}: found {2:s}'
    checks = [
        {
            'extensions': ('py', ),
            'fail': {
                re.compile(r'^\s*(?:from\s+[^\s]+\s+)?import(?:\s|\().+,.+\)?$'): 'grouped import',  # noqa
                re.compile(r'^\s*from\s+[\.]{1,2}\s+import.+$'): 'relative import',  # noqa
                re.compile(r'^\s*from\s+[^\s]+\s+import\s+\*$'): 'wildcard import',  # noqa
            },
        }
    ]

    # This ignore imports in methods which start with spaces.
    passing_pattern = re.compile(
        r'^(?:from\s+[^\s]+\s+)?import\s+[^,\(\)]+|\\$'
    )

    multiline_pattern = re.compile(r'.*(?:\\|\()\s*$')

    def is_import(self, line):
        return self.passing_pattern.match(line) is not None

    def is_multiline_import(self, line):
        return self.multiline_pattern.match(line) is not None

    def check(self, file_path, fail={}, **kwargs):
        errors = []
        imports = []
        with open(file_path, 'r') as file_handle:
            previous_line = ''
            for linenumber, line in enumerate(file_handle.readlines()):
                if self.skip_line(line):
                    continue

                if self.is_multiline_import(line):
                    previous_line += line
                    continue

                if not self.is_multiline_import(line) and previous_line:
                    line = previous_line.strip('\\\n') + line.strip()
                    previous_line = ''

                # We should have full import statement in ``line`` now, even
                # if it was a multiline import.
                for check, message in fail.items():
                    if Imports.validate_line(check, line):
                        errors.append(self.message.format(
                            file_path, 1 + linenumber, message
                        ))

                if self.is_import(line):
                    imports.append((linenumber, line))

        # duplicate imports list and sort it
        imports_sorted = imports[:]
        imports_sorted.sort(key=lambda x: x[1])

        if imports_sorted != imports:
            errors.append(self.message.format(
                file_path, '{0:d}-{1:d}'.format(imports[0][0], imports[-1][0]),
                'unsorted imports'
            ))

        return errors


def console_script(options):
    console_factory(Imports, options)
