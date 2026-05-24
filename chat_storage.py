"""Chat storage layer for persisting conversation messages in SQLite."""

import sqlite3
from pathlib import Path
from utils.set_config import set_conversation_id


class ChatStorage:
    """Handles SQLite-backed storage for chat messages."""

    def __init__(self, storage_path: str | Path):
        """Initialize the database connection and ensure schema exists."""
        # Ensure storage_path is a Path object
        storage_path = Path(storage_path)

        # Create parent directory if it does not exist
        assert isinstance(storage_path, Path)
        storage_path.parent.mkdir(parents=True, exist_ok=True)

        self.conn = sqlite3.connect(storage_path)
        self.conn.execute("PRAGMA foreign_keys = ON;")

        self._init_db()

    def _init_db(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        existing_tables = {row[0] for row in cursor.fetchall()}

        expected_tables = {"messages", "conversations", "sqlite_sequence"}

        if existing_tables and existing_tables != expected_tables:
            raise RuntimeError(
                "Database structure mismatch. "
                f"Expected tables: {expected_tables}, "
                f"found: {existing_tables}"
            )
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                conversation_id INTEGER PRIMARY KEY,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                last_modified DATETIME DEFAULT CURRENT_TIMESTAMP,
                title TEXT,
                is_deleted BOOLEAN DEFAULT 0,
                deleted_at DATETIME
            );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id INTEGER NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                role TEXT NOT NULL,
                message TEXT NOT NULL,

                raw_output TEXT,
                metadata JSON,

                FOREIGN KEY (conversation_id) REFERENCES conversations(conversation_id)
            )
        """)
        self.conn.commit()

        expected_columns = {
            "conversations": {
                "conversation_id",
                "created_at",
                "last_modified",
                "title",
                "is_deleted",
                "deleted_at",
            },
            "messages": {
                "id",
                "conversation_id",
                "timestamp",
                "role",
                "message",
                "raw_output",
                "metadata",
            },
        }

        for table_name, expected in expected_columns.items():
            cursor.execute(f"PRAGMA table_info({table_name})")
            actual = {row[1] for row in cursor.fetchall()}

            if actual != expected:
                raise RuntimeError(
                    f"Column mismatch in '{table_name}'. "
                    f"Expected: {expected}, "
                    f"found: {actual}"
                )

    def append(
        self,
        conversation_id: int,
        role: str,
        content: str,
        raw_output: str = None,
        metadata: str = None,
        timestamp=None,
    ):
        """Insert a new message into the database."""
        cursor = self.conn.cursor()
        conversation_id = self.ensure_conversation(conversation_id)
        self.update_last_modified(conversation_id)

        columns = ["conversation_id", "role", "message"]
        values = [conversation_id, role, content]

        if raw_output is not None:
            columns.append("raw_output")
            values.append(raw_output)

        if metadata is not None:
            columns.append("metadata")
            values.append(metadata)

        if timestamp is not None:
            columns.append("timestamp")
            values.append(timestamp)

        placeholders = ", ".join(["?"] * len(values))
        column_string = ", ".join(columns)

        cursor.execute(
            f"INSERT INTO messages ({column_string}) VALUES ({placeholders})", values
        )

        self.conn.commit()

    def update_last_modified(self, conversation_id: int):
        """Update last_modified in conversation table."""
        cursor = self.conn.cursor()
        cursor.execute(
            """
            UPDATE conversations
            SET last_modified = CURRENT_TIMESTAMP
            WHERE conversation_id = ?
            """,
            (conversation_id,),
        )
        self.conn.commit()

    def ensure_conversation(self, conversation_id):
        """Ensure conversation exists; create it if it does not.

        If conversation_id is 0, generate a new incremental conversation id.
        """
        cursor = self.conn.cursor()

        # Auto-create new conversation id if 0 is passed
        if conversation_id in (0, None):
            cursor.execute(
                "SELECT MAX(CAST(conversation_id AS INTEGER)) FROM conversations"
            )
            result = cursor.fetchone()[0]
            new_id = 1 if result is None else int(result) + 1
            conversation_id = new_id
            set_conversation_id(conversation_id)

        cursor.execute(
            "INSERT OR IGNORE INTO conversations (conversation_id) VALUES (?)",
            (conversation_id,),
        )
        self.conn.commit()

        return conversation_id

    def fetch_conversation_history(self, conversation_id: int, turns: int):
        """Print the most recent conversation history in a readable format."""
        cursor = self.conn.cursor()

        cursor.execute(
            """
            SELECT role, message
            FROM messages
            WHERE conversation_id = ?
            ORDER BY id DESC
            LIMIT ?
            """,
            (conversation_id, turns),
        )

        rows = cursor.fetchall()

        if not rows:
            print(f"No messages found for conversation {conversation_id}")
            return

        rows.reverse()

        role_map = {
            "user": "User",
            "assistant": "Kokoro",
        }

        for role, message in rows:
            display_role = role_map.get(role.lower(), role.title())
            print(f"{display_role}: {message}\n")

    def close(self):
        """Close the database connection."""
        self.conn.close()


if __name__ == "__main__":
    BASE_DIR = Path(__file__).resolve().parents[1]
    db_path = BASE_DIR / "logs" / "chat_storage" / "memory.db"
    chat = ChatStorage(db_path)

    convo = 1

    print("Conversation ID: ", convo, "\n")
    chat.fetch_conversation_history(convo, 5)
