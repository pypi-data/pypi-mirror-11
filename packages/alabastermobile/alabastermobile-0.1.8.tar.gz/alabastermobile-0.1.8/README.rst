# alabastermobile

This theme is a modified "alabaster" Sphinx theme (https://github.com/bitprophet/alabaster)

Add sidebar top in mobile view

# Installation

```
    pip install alabastermobile
```

Or

```
    git clone https://github.com/fraoustin/alabastermobile.git
    cd alabastermobile
    python setup.py install
```

# Use

In your conf.py

```
    import alabastermobile
    html_theme = 'alabastermobile'
    html_theme_path = [alabastermobile.get_path()]
    extensions = ['alabaster']

    html_sidebars = {
        '**': [ 'about.html',
                'postcard.html', 'navigation.html',
                'tagcloud.html',
                'categories.html',  'archives.html',
                'searchbox.html',
                ],
        }
```
