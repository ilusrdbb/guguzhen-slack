import sqlite3


def init_db():
    conn = sqlite3.connect('slack.db')
    cursor = conn.cursor()
    create_table_script = """
    CREATE TABLE IF NOT EXISTS "battle_log" (
      "id" text NOT NULL,
      "username" text NOT NULL,
      "enemyname" text,
      "char" text,
      "charlevel" text,
      "weapon" text,
      "armor" text,
      "attrs" text,
      "halos" text,
      "log" text NOT NULL,
      "isWin" text NOT NULL,
      "rank" text,
      "time" integer NOT NULL,
      "type" text NOT NULL,
      PRIMARY KEY ("id")
    );
    
    CREATE INDEX IF NOT EXISTS "idx_username" ON "battle_log" (
      "username" COLLATE BINARY ASC
    );
    
    CREATE INDEX IF NOT EXISTS "idx_time" ON "battle_log" (
      "time" COLLATE BINARY ASC
    );
    """
    cursor.executescript(create_table_script)
    conn.commit()
    conn.close()