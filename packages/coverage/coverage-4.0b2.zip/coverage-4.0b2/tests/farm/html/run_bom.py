# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://bitbucket.org/ned/coveragepy/src/default/NOTICE.txt

import sys

def html_it():
    """Run coverage.py and make an HTML report for bom.py."""
    import coverage
    cov = coverage.Coverage()
    cov.start()
    import bom          # pragma: nested
    cov.stop()          # pragma: nested
    cov.html_report(bom, directory="../html_bom")

runfunc(html_it, rundir="src")

# HTML files will change often.  Check that the sizes are reasonable,
#   and check that certain key strings are in the output.
compare("gold_bom", "html_bom", size_within=10, file_pattern="*.html")
contains("html_bom/bom_py.html",
    '<span class="str">&quot;3&#215;4 = 12, &#247;2 = 6&#177;0&quot;</span>',
    )

clean("html_bom")
