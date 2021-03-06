#!/usr/bin/env python3

'''
Preprocessing script for LHCb Glossary gitbook.

'''

from pathlib import Path
import re

title_pattern = re.compile(r'''
    ^\#\#            # Starting two #
    \w*              # Optional unlimited whitespace
(?P<name> [^\{]*)    # Non-greedy anything but {
(?: \{\#
  (?P<link> .*)
\}  )?               # Links (Optional)
    \w*$             # End of string and optional whitespace

''', re.VERBOSE)

DIR = Path(__file__).resolve().parent
base = './glossary'

with open('gitbook_readme.md', 'w') as out:
    print("# LHCb Glossary\n", file=out)
    print("Glossary of HEP and LHCb-specific terms and concepts - make a pull request at <https://github.com/lhcb/glossary>.\n", file=out)
    print("Contributions to the glossary are highly encouraged. Please see the [contributing guide](https://github.com/lhcb/glossary/blob/master/CONTRIBUTING.md) for details.\n", file=out)
    print("## Terms:\n", file=out)

    for fn in sorted((DIR.parent / 'glossary').glob('?.md')):
        letter = fn.stem
        with open(fn) as f:
            for line in f:
                if line.startswith('##'):
                    d = title_pattern.match(line).groupdict()
                    name = d['name'].strip()
                    link = d['link'] if d['link'] is not None else (name.replace(' ', '-')
                                                                        .replace(':', '')
                                                                        .replace('(', '')
                                                                        .replace(')','')
                                                                        .lower())

                    print(f"* [{name}]({base}/{letter}.md#{link})", file=out)
