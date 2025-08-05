import re
from pathlib import Path


def sync_versions():
    pyproject = Path("pyproject.toml")
    version = re.search(r'version = "(.+?)"', pyproject.read_text()).group(1)

    init_file = Path("src/sudoq/__init__.py")
    content = init_file.read_text()
    updated = re.sub(r'__version__ = ".+?"', f'__version__ = "{version}"', content)
    init_file.write_text(updated)


if __name__ == "__main__":
    sync_versions()
