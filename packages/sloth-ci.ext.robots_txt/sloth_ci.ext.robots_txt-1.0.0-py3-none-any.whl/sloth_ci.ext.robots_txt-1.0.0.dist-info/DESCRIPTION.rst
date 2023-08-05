robots.txt for Sloth CI.

Extension params::

    # Use the sloth-ci.ext.robots_txt module.
    module: robots_txt

    # Absolute path to the custom robots.txt file.
    # If not given, the bundled one is used (disallows everything to everyone).
    # file: ~/robots.txt

    # URL path to robots.txt.
    # By default the file is available in the root: *http://example.com:8080/robots.txt*.
    # path: /static/robots.txt

File and path params are optional.


