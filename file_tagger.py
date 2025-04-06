from pathlib import Path

from tag_database import TagDatabase
from tag_generators import generate_tags


def tag_all_files(parent_path: Path, tag_database: TagDatabase) -> None:
    """
    Tag all files in the given directory and its subdirectories.

    Args:
        parent_path (Path): The path to the directory containing files to tag.
    """
    # Iterate through all files in the directory and its subdirectories
    with tag_database as connection:
      for file_path in parent_path.rglob('*'):
          if file_path.is_file():
              connection.add_file_tags(list(generate_tags(file_path)))

if __name__ == "__main__":
    tag_all_files(Path('.'), TagDatabase(Path('file_tags.db')))