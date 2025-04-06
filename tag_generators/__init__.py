import itertools
from pathlib import Path
from typing import Callable, Iterable

from tag_database import FileTag

from .content_tag_generators import typescript_content_generator
from .metadata_tag_generators import (
    directory_generator,
    extension_generator,
    filename_generator,
)

type TagGenerator = Callable[[Path], Iterable[FileTag]]

ALL_GENERATORS: list[TagGenerator] = [
    typescript_content_generator,
    extension_generator,
    filename_generator,
    directory_generator,
]

def generate_tags(file_path: Path) -> Iterable[FileTag]:
    """
    Generate tags for a given file using all available tag generators.

    Args:
        file_path (Path): The path to the file.

    Returns:
        Iterable[FileTag]: An iterable of FileTag objects.
    """
    return itertools.chain(
        *(generator(file_path) for generator in ALL_GENERATORS)
    )