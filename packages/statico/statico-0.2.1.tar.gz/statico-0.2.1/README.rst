
|PyPI version| |License| |Supported Python| |Format| |Landscape| |Requires|

statico
=======
A simple and extensible static site generator in Python

Install
-------
:code:`pip install statico`

Documentation
-------------

Check the `wiki <https://github.com/oss6/statico/wiki>`_ for the complete documentation.

Commands
--------

+-----------------------------------------------+-------------------------------------------------------+
|                Command                        |                   Description                         |
+-----------------------------------------------+-------------------------------------------------------+
| statico                                       | Creates a website                                     |
+-----------------------------------------------+-------------------------------------------------------+
| statico -c/--clear                            | Clears the workspace (deletes the website)            |
+-----------------------------------------------+-------------------------------------------------------+
| statico -a/--article "My new article"         | Creates a new article                                 |
+-----------------------------------------------+-------------------------------------------------------+
| statico -p/--page "Projects"                  | Creates a new page                                    |
+-----------------------------------------------+-------------------------------------------------------+
| statico -g/--generate                         | Generate the site to the output directory             |
+-----------------------------------------------+-------------------------------------------------------+
| statico -P/--preview                          | Preview your website on 127.0.0.1:8000                |
+-----------------------------------------------+-------------------------------------------------------+
| statico -w/--watch                            | Watch for changes in the content directory            |
+-----------------------------------------------+-------------------------------------------------------+
| statico -r/-rss http://example.com/atom.xml   | Loads posts from a RSS feed                           |
+-----------------------------------------------+-------------------------------------------------------+
| statico -s/--setup-gh-deploy                  | Setup GitHub Pages details                            |
+-----------------------------------------------+-------------------------------------------------------+
| statico -d/--gh-deploy                        | Deploys to GitHub                                     |
+-----------------------------------------------+-------------------------------------------------------+
| statico -i/--isolate <partial_name>           | Isolate articles for fast rebuild times               |
+-----------------------------------------------+-------------------------------------------------------+
| statico -I/--integrate                        | Integrates the isolated articles                      |
+-----------------------------------------------+-------------------------------------------------------+


Web site structure
------------------
* atom.xml
* content/
    - articles/       
    - index.md
    - pages/
* output/
* settings.json
* static/
    - css/
    - images/
    - js/
* templates/
    - article.html
    - base.html
    - default.html
    - includes/
        - after_footer.html
        - asides/
        - footer.html
        - header.html
        - head.html
        - navigation.html
    - page.html

Changelog
---------
See the CHANGES file.

License
-------
MIT © `Ossama Edbali
<http://oss6.github.io>`_.


.. |PyPI version| image:: https://img.shields.io/pypi/v/statico.svg
    :target: https://pypi.python.org/pypi/statico
    :alt: Latest PyPI Version
.. |License| image:: https://img.shields.io/pypi/l/statico.svg
    :target: https://pypi.python.org/pypi/statico
    :alt: License
.. |Supported Python| image:: https://img.shields.io/pypi/pyversions/statico.svg
    :target: https://pypi.python.org/pypi/statico
    :alt: Supported Python Versions
.. |Format| image:: https://img.shields.io/pypi/format/statico.svg
    :target: https://pypi.python.org/pypi/statico
    :alt: Format
.. |Landscape| image:: https://landscape.io/github/oss6/statico/master/landscape.svg?style=flat
   :target: https://landscape.io/github/oss6/statico/master
   :alt: Code Health
.. |Requires| image:: https://requires.io/github/oss6/statico/requirements.svg?branch=master
    :target: https://requires.io/github/oss6/statico/requirements/?branch=master
    :alt: Requirements Status
