

History
=======

GitHub Log
----------

* Aug 30, 2015
    - (by: sonofeft) 
        - Version 0.0.6
            Added AUTHORS.rst, fixed history script bug, and link error
* Aug 29, 2015
    - (by: sonofeft) 
        - fixed doc error on PyHatch.cfg location
        - Added ``Making History`` page
            In sphinx docs, described how to run history_from_github_api.py python
            script.
            Also added a little doc cleanup.
* Aug 28, 2015
    - (by: sonofeft) 
        - Added HISTORY.rst generation from GitHub API
            Included all the scripts and templates to make a History page in the
            Sphinx docs.  Also added build_all_html.py in /docs/ subdirectory to
            ``touch`` all rst files such that sphinx will rebuild the whole site.
        - Update docs and tox
            Lots of tweeks to new project checklist and quickstart as well as adding
            coverage to tox.ini and tox.ini templates
* Aug 27, 2015
    - (by: sonofeft) 
        - After pylint
* Aug 26, 2015
    - (by: sonofeft) 
        - Added Example Usage, Made GUI Smaller
* Aug 25, 2015
    - (by: sonofeft) 
        - Fixed broken tox
            Moving PyHatch.cfg to user home directory and adding image shields to
            README.rst broke tox
        - added generic img shields
        - fixed "python setup.py test"
        - doc and version cleanup
* Aug 23, 2015
    - (by: sonofeft) 
        - fixed setup.py
        - first commit of existing code base
