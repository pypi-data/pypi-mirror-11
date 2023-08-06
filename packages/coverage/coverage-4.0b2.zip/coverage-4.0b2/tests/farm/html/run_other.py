# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://bitbucket.org/ned/coveragepy/src/default/NOTICE.txt

def html_it():
    """Run coverage.py and make an HTML report for everything."""
    import coverage
    cov = coverage.Coverage(include=["./*", "../othersrc/*"])
    cov.start()
    import here         # pragma: nested
    cov.stop()          # pragma: nested
    cov.html_report(directory="../html_other")

runfunc(html_it, rundir="src", addtopath="../othersrc")

# Different platforms will name the "other" file differently. Rename it
import os, glob

for p in glob.glob("html_other/*_other_py.html"):
    os.rename(p, "html_other/blah_blah_other_py.html")

# HTML files will change often.  Check that the sizes are reasonable,
#   and check that certain key strings are in the output.
compare("gold_other", "html_other", size_within=10, file_pattern="*.html")
contains("html_other/index.html",
    '<a href="here_py.html">here.py</a>',
    'other_py.html">', 'other.py</a>',
    )

clean("html_other")
