import aiosqlite
from typing import Any, List, Tuple, Optional
from config import get_db_path
import csv


class AsyncDatabase:
    """
    Asynchronous SQLite database helper using aiosqlite.

    This base class provides the fundamental CRUD operations and serves as
    the foundation for table-specific repository classes. It manages opening
    and closing database connections for each query, ensuring safe and
    isolated operations in an async environment.

    Typical usage:
        db = AsyncDatabase()
        await db.execute("INSERT INTO Users (id) VALUES (?)", (123,))
        row = await db.fetchone("SELECT * FROM Users WHERE id = ?", (123,))
    """

    def __init__(self, db_path: Optional[str] = None) -> None:
        """
        Initialize the database handler.

        Args:
            db_path (str, optional): Path to the SQLite database file.
                If omitted, the path is loaded from the app config via get_db_path().
        """
        self.db_path = db_path or get_db_path()

    async def execute(self, query: str, params: Tuple = ()) -> None:
        """
        Execute a write/query command such as INSERT, UPDATE, DELETE, or CREATE.

        Opens a new connection, executes the statement, and commits changes.

        Args:
            query (str): SQL query string.
            params (tuple): Parameters for the SQL query (default: empty tuple).

        Returns:
            None
        """
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(query, params)
            await db.commit()

    async def fetchone(self, query: str, params: Tuple = ()) -> Optional[Tuple[Any]]:
        """
        Execute a SELECT query and fetch a single row.

        Args:
            query (str): SQL SELECT statement.
            params (tuple): Query parameters.

        Returns:
            Optional[Tuple]: The first row found, or None if no results.
        """
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(query, params) as cursor:
                return await cursor.fetchone()

    async def fetchall(self, query: str, params: Tuple = ()) -> List[Tuple[Any]]:
        """
        Execute a SELECT query and fetch all rows.

        Args:
            query (str): SQL SELECT statement.
            params (tuple): Query parameters.

        Returns:
            list[Tuple]: All returned rows.
        """
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(query, params) as cursor:
                return await cursor.fetchall()

    # ---- Helper Methods ----

    async def get_table(self, table_name: str) -> List[Tuple[Any]]:
        """
        Retrieve all rows from a table.

        Args:
            table_name (str): Name of the table.

        Returns:
            list[Tuple]: All rows in the table.
        """
        return await self.fetchall(f"SELECT * FROM {table_name}")

    async def get_row(self, table_name: str, condition: str, params: Tuple = ()) -> Optional[Tuple[Any]]:
        """
        Retrieve a single row matching the SQL condition.

        Args:
            table_name (str): Table to query.
            condition (str): SQL condition after WHERE (e.g. "id = ?").
            params (tuple): Parameters for the condition.

        Returns:
            Optional[Tuple]: The row found, or None.
        """
        query = f"SELECT * FROM {table_name} WHERE {condition}"
        return await self.fetchone(query, params)

    async def insert(self, table_name: str, columns: list[str], values: Tuple) -> None:
        """
        Insert a new row into a table.

        Args:
            table_name (str): Table name.
            columns (list[str]): Column names for the insert.
            values (tuple): Values matching the given columns.

        Returns:
            None
        """
        cols = ", ".join(columns)
        placeholders = ", ".join("?" for _ in columns)
        query = f"INSERT INTO {table_name} ({cols}) VALUES ({placeholders})"
        await self.execute(query, values)

    async def update(self, table_name: str, updates: str, condition: str, params: Tuple = ()) -> None:
        """
        Update rows that match a condition.

        Args:
            table_name (str): Table name.
            updates (str): SET clause, e.g. "name = ?, age = ?".
            condition (str): WHERE condition, e.g. "id = ?".
            params (tuple): Values used in both SET and WHERE.

        Returns:
            None
        """
        query = f"UPDATE {table_name} SET {updates} WHERE {condition}"
        await self.execute(query, params)

    async def delete(self, table_name: str, condition: str, params: Tuple = ()) -> None:
        """
        Delete rows matching a condition.

        Args:
            table_name (str): Table name.
            condition (str): WHERE condition.
            params (tuple): Parameters for the condition.

        Returns:
            None
        """
        query = f"DELETE FROM {table_name} WHERE {condition}"
        await self.execute(query, params)

    async def export_table_to_csv(self, table_name: str, csv_path: str) -> str:
        """
        Export an entire table to a CSV file.

        Args:
            table_name (str): Name of the table to export.
            csv_path (str): File path where CSV will be saved.

        Returns:
            str: The file path to the created CSV.
        """
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(f"SELECT * FROM {table_name}")
            rows = await cursor.fetchall()
            col_names = [description[0] for description in cursor.description]
            await cursor.close()

        # Write the CSV file
        with open(csv_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(col_names)
            writer.writerows(rows)

        return csv_path

