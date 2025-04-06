import sqlite3
from dataclasses import dataclass
from pathlib import Path


@dataclass
class FileTag:
    file_path: str
    tag_description: str
    tag_strength: int = 0
    id: int | None = None


class TagConnection:
  def __init__(self, db_path: Path) -> None:
      self.path = db_path
      self.connection = sqlite3.connect(self.path)
      self.cursor = self.connection.cursor()
  
     

  def create_database(self) -> None:
    """
    Create a SQLite database to store file tags.

    Args:
        db_path (Path): The path where the database will be created.
    """
    self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS file_tags (
            id INTEGER PRIMARY KEY,
            file_path TEXT,
            tag TEXT
            tag_strength INTEGER DEFAULT 0,
        )
    ''')

  def add_file_tags(self, file_tags: list[FileTag]) -> None:
    tag_parameters = [
        (tag.file_path, tag.tag_description, tag.tag_strength)
        for tag in file_tags
    ]
    self.cursor.executemany('''
        INSERT INTO file_tags (file_path, tag, tag_strength)
        VALUES (?, ?, ?)
    ''', tag_parameters)
    self.connection.commit()
  
  def get_tag_files(self, tag: str) -> list[FileTag]:
    self.cursor.execute('''
        SELECT id, file_path, tag, tag_strength
        FROM file_tags
        WHERE file_path = ?
        ORDER BY tag_strength DESC
    ''', (tag,))
    rows = self.cursor.fetchall()
    return [FileTag(*row) for row in rows]
     
   
class TagDatabase:
  def __init__(self, db_path: Path) -> None:
    self.path = db_path
    if not db_path.exists():
        with self as conn:
          conn.create_database()
    self.connection: TagConnection | None = None
  
  def __enter__(self) -> TagConnection:
      if self.connection:
          return self.connection
      tag_connection = TagConnection(self.path)
      self.connection = tag_connection
      return tag_connection
  
  def __exit__(self, exc_type, exc_value, traceback) -> None:
      if self.connection is not None:
          self.connection.connection.close()
          self.connection = None

 
