from pathlib import Path
from typing import Iterable

from tag_database import FileTag

DIRECT_PARENT_STRENGTH = 5

def extension_generator(file_path: Path) -> Iterable[FileTag]:
    """
    Generates a tag based on the file extension.

    Args:
        file_path (str): The path to the file.

    Returns:
        str: The generated tag.
    """
    return [FileTag(file_path=str(file_path), tag_description=file_path.suffix, tag_strength=1)]

def filename_generator(file_path: Path) -> Iterable[FileTag]:
    """
    Generates a tag based on the file name.

    Args:
        file_path (str): The path to the file.

    Returns:
        str: The generated tag.
    """
    return [FileTag(file_path=str(file_path), tag_description=file_path.stem, tag_strength=1)]

def directory_generator(file_path: Path) -> Iterable[FileTag]:
    """
    Generates a tag based on the directory name.

    Args:
        file_path (str): The path to the file.

    Returns:
        str: The generated tag.
    """
    return [FileTag(file_path=str(file_path), tag_description=str(parent), tag_strength=DIRECT_PARENT_STRENGTH - i) for i, parent in enumerate(file_path.parents)]