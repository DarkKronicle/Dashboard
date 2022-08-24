import importlib
from pathlib import Path


def load_widgets():
    paths = Path('display/screen/widgets').glob('**/*.py')
    for p in paths:
        importlib.import_module(str(p).split('.')[0].replace('/', '.').replace('\\', '.'))
