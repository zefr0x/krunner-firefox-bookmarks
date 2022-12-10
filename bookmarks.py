"""Access the bookmarks database and query the data."""
# The next imports are on-time import in the middle of the file to save memory.
# from pathlib import Path
# import sqlite3
# import tempfile
# import shutil
# import configparser

MAX_RESULTS = 13


class FirefoxBookMarks:
    """BookMarks class for the FireFox browser."""

    def __init__(self) -> None:
        """Create temp file and copy the database to it."""
        # Temporary file
        self.temporary_database_location = __import__("tempfile").mktemp()
        self.fetch_database()
        return None

    def fetch_database(self) -> None:
        """Fetch database to temp file."""
        # Using FireFox63 the DB was locked for exclusive use of FireFox,
        # so we need to create a copy of it to a temp file.
        __import__("shutil").copyfile(
            self.get_database_location(), self.temporary_database_location
        )
        return None

    def get_database_location(self) -> str:
        """Get bookmarks database path."""
        from pathlib import Path

        # Firefox folder path
        firefox_path = Path.joinpath(Path.home(), ".mozilla/firefox/")

        # Read Firefox profiles configuration file to get the database file path.
        from configparser import RawConfigParser

        profiles = RawConfigParser()
        profiles.read(Path.joinpath(firefox_path, "profiles.ini"))

        (
            first_default,
            esr_version_default,
            dev_version_default,
        ) = ("", "", "")

        for profile in profiles.sections():
            if profile.startswith("Install"):
                try:
                    dir = profiles[profile]["Default"]
                except KeyError:
                    continue

                if not dir.endswith(".dev-edition-default") and not dir.endswith(
                    ".default-esr"
                ):
                    # First non esr or dev default profile.
                    first_default = dir
                    break
                elif dir.endswith(".default-esr"):
                    esr_version_default = dir
                elif dir.endswith(".dev-edition-default"):
                    dev_version_default = dir

        for profile_path in (
            first_default,
            esr_version_default,
            dev_version_default,
        ):
            if profile_path:
                break

        # Sqlite db directory path
        return str(
            Path.joinpath(
                Path.joinpath(
                    firefox_path,
                    # Fallback to Profile0.
                    profile_path or profiles.get("Profile0", "Path"),
                ),
                "places.sqlite",
            )
        )

    def connect_to_database(self) -> None:
        """Create a database connection if there was not."""
        if not hasattr(self, "conn"):
            # Connect to Firefox bookmarks database in temp file.
            self.con = __import__("sqlite3").connect(self.temporary_database_location)
            self.cursor = self.con.cursor()
        return None

    def search(self, term = "") -> list:
        """Search for a term in the database and return the results."""
        query = (
            "SELECT A.title, B.url FROM moz_bookmarks AS A"
            + " JOIN moz_places AS B ON(A.fk = B.id)"
        )

        if term == "":
            query += "ORDER BY visit_count DESC, A.lastModified DESC"
            args = ()
        else:
            query += " WHERE A.title LIKE ? "
            query += "ORDER BY instr(LOWER(A.title), LOWER(?)) ASC, visit_count DESC"
            args = ('%'+term+'%', term)

        query += " LIMIT %d" % MAX_RESULTS

        self.connect_to_database()

        # Query execution
        self.cursor.execute(query, args)
        return self.cursor.fetchall()

    def close(self):
        """Close the database to save memory while not using it."""
        del self.cursor
        self.conn.close()
        del self.conn
