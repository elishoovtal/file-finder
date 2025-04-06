import re
from pathlib import Path
from typing import Any, Callable, Iterable

from tag_database import FileTag

EXPORT_REGEX = re.compile(r'export\s+(const)|(function)|(class)\s+(\w+)')
IMPORT_REGEX = re.compile(r'import\s+(\w+)\s+from\s+["\']([^"\']+)["\']')
EXPORT_TAG_STRENGTH = 10
IMPORT_TAG_STRENGTH = 5

REGEX_TO_EXTRACTOR: dict[re.Pattern, tuple[int, Callable[[re.Match[str]], str | Any]]] = {
    EXPORT_REGEX: (EXPORT_TAG_STRENGTH, lambda x: x.group(4)),
    IMPORT_REGEX: (IMPORT_TAG_STRENGTH, lambda x: x.group(1)),
}

def typescript_content_generator(file_path: Path) -> Iterable[FileTag]:
    """
    Generates tags based on the content of TypeScript files.

    Args:
        file_path (Path): The path to the TypeScript file.

    Returns:
        Iterable[FileTag]: An iterable of FileTag objects.
    """
    if file_path.suffix != '.ts':
        return []
    try:
        # Read the content of the TypeScript file
        path_content = file_path.read_text()
    except UnicodeDecodeError:
        # Handle files that cannot be decoded as text
        return []
    tags = []
    # Example: Add a tag for each exported member from file.
    for line in path_content.splitlines():
        for regex, (strength, extractor) in REGEX_TO_EXTRACTOR.items():
            matches = regex.search(line)
            if matches:
                # Extract the member name using the provided extractor function
                class_name = extractor(matches)
                # Add a tag for the exported member
                tags.append(FileTag(file_path=str(file_path), tag_description=class_name, tag_strength=strength))
    return tags