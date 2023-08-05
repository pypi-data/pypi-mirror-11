A Colorful Theme for Hieroglyph
-------------------------------

To make go:
```
$ pip install colorful-hieorglyph-theme
```

In your conf.py::

    import colorful_hieroglyph_theme
    html_theme = 'colorful'  ##(must be changed in file)!
    html_theme_path = colorful.get_html_theme_path()
    html_static_path = ['_static', html_theme_path + '/colorful/static/'] ##(must be changed in file)
    slide_theme_options = {'custom_css' : 'colorful.css'}

