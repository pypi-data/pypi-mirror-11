from pygments.token import Token
from pygments.style import Style
from pygments.util import ClassNotFound
from prompt_toolkit.styles import default_style_extensions
import pygments.styles


def style_factory(name):
    try:
        style = pygments.styles.get_style_by_name(name)
    except ClassNotFound:
        style = pygments.styles.get_style_by_name('native')

    class CLIStyle(Style):
        styles = {}

        styles.update(style.styles)
        styles.update(default_style_extensions)
        styles.update({
            Token.Menu.Completions.Completion.Current: 'bg:#00aaaa #000000',
            Token.Menu.Completions.Completion: 'bg:#008888 #ffffff',
            Token.Menu.Completions.ProgressButton: 'bg:#003333',
            Token.Menu.Completions.ProgressBar: 'bg:#00aaaa',
            Token.SelectedText: '#ffffff bg:#6666aa',
            Token.IncrementalSearchMatch: '#ffffff bg:#4444aa',
            Token.IncrementalSearchMatch.Current: '#ffffff bg:#44aa44',
            Token.Toolbar: 'bg:#440044 #ffffff',
            Token.Toolbar: 'bg:#222222 #aaaaaa',
            Token.Toolbar.Off: 'bg:#222222 #888888',
            Token.Toolbar.On: 'bg:#222222 #ffffff',
        })

    return CLIStyle
