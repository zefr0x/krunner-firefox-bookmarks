"""Access the bookmarks database and query the data."""

import sqlite3
import tempfile
import shutil
import configparser
from pathlib import Path

MAX_RESULTS = 13


class FirefoxBookMarks:
    """History class for the FireFox browser."""

    def __init__(self) -> None:
        """Find the database location and create temp file."""
        # Set history location
        self.history_location = self.search_places()

        # Temporary file
        # Using FF63 the DB was locked for exclusive use of FF
        self.temporary_history_location = tempfile.mktemp()

    def fetch_database(self):
        """Fetch database to temp file."""
        shutil.copyfile(self.history_location, self.temporary_history_location)

    def connect_to_database(self):
        """Create a database connection if there was not."""
        try:
            self.conn
        except AttributeError:
            # Open Firefox history database
            self.conn = sqlite3.connect(self.temporary_history_location)

    def search_places(self) -> Path:
        """Get history database path."""
        #   Firefox folder path
        firefox_path = Path.joinpath(Path.home(), ".mozilla/firefox/")
        #   Firefox profiles configuration file path
        conf_path = Path.joinpath(firefox_path, "profiles.ini")
        #   Profile config parse
        profile = configparser.RawConfigParser()
        profile.read(conf_path)
        prof_path = profile.get("Profile0", "Path")
        #   Sqlite db directory path
        sql_path = Path.joinpath(firefox_path, prof_path)
        #   Sqlite db path
        return Path.joinpath(sql_path, "places.sqlite")

    def search(self, term):
        """Search for a term in the database and return a result."""
        # VULN sql injection.
        query = (
            "SELECT A.title, url FROM moz_bookmarks AS A"
            + " JOIN moz_places AS B ON(A.fk = B.id)"
            + ' WHERE A.title LIKE "%%%s%%"'
        ) % term

        if term == "":
            query += " ORDER BY A.lastModified DESC"
        else:
            # VULN sql injection.
            query += ' ORDER BY instr(LOWER(A.title), LOWER("%s")) ASC' % term

        query += " LIMIT %d" % MAX_RESULTS

        self.connect_to_database()

        # Query execution
        cursor = self.conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows

    def close(self):
        """Close the database to save memory while not using it."""
        self.conn.close()
        del self.conn
