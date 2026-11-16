import aiosqlite

class Data:

    @staticmethod
    async def setup_tables():
        async with aiosqlite.connect("database.db") as db:
            await db.execute("""CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    balance FLOAT,
                    level INTEGER
                )
            """)
            await db.commit()
            print("Created users table")

    @staticmethod
    async def register_user(id):
        async with aiosqlite.connect("database.db") as db:
            user_data = (id, 0.0, 0)
            await db.execute("INSERT OR IGNORE INTO users VALUES (?, ?, ?)", user_data) 
            await db.commit()
            print(f"Registered user: {id} successfully")

    @staticmethod
    async def remove_user(id):
        async with aiosqlite.connect("database.db") as db:
            await db.execute("DELETE FROM users WHERE id = ?", (id))
            await db.commit()
            print(f"Removed user: {id} successfully")

    @staticmethod
    async def get_value(value_name, table_name, identifier_name, identifier_value):
        async with aiosqlite.connect("database.db") as db:
            db.row_factory = aiosqlite.Row

            async with db.cursor() as cursor:
                await cursor.execute(f"SELECT {value_name} FROM {table_name} WHERE {identifier_name} = ?", ( identifier_value,))
                row = await cursor.fetchone()
                if row:
                    return row[value_name]
                else:
                    print("No record found")
    @staticmethod
    async def set_value(value_name, table_name, identifier_name, identifier_value, new_value):
        async with aiosqlite.connect("database.db") as db:
            async with db.cursor() as cursor:
                await cursor.execute(f"UPDATE {table_name} SET {value_name} = ? WHERE {identifier_name} = ?", (new_value, identifier_value))
                await db.commit()

                if cursor.rowcount == 0:
                    print(f"Update failed: No row found with the identifier {identifier_value}")
                else:
                    print(f"Updated {cursor.rowcount} row(s) successfully")