#!/usr/bin/python3
"""Plasma runner for searching and opening firefox bookmarks."""

from gettext import gettext, bindtextdomain, textdomain
from webbrowser import get as get_webbrowser

import dbus
import dbus.service
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib

from bookmarks import FirefoxBookMarks


bindtextdomain("messages", "locales")
textdomain("messages")
_ = gettext

key_word = _("f")
key_word_length = len(key_word) + 1

icon_path = "firefox"

DBusGMainLoop(set_as_default=True)

objpath = "/krunnerFirefoxBookMarks"

iface = "org.kde.krunner1"


class Runner(dbus.service.Object):
    """Comunicate with KRunner, deal with queries, provide and run actions."""

    def __init__(self) -> None:
        """Create dbus service, fetch firefox database and connect to klipper."""
        dbus.service.Object.__init__(
            self,
            dbus.service.BusName(
                "com.github.zer0-x.krunner-firefox-bookmarks", dbus.SessionBus()
            ),
            objpath,
        )

        self.bookmarks = FirefoxBookMarks()
        self.bookmarks.fetch_database()
        return None

    @dbus.service.method(iface, in_signature="s", out_signature="a(sssida{sv})")
    def Match(self, query: str) -> list:
        """Get the matches and return a list of tupels."""
        returns: list = []

        if query.startswith(key_word + " ") or query == key_word:
            query = query[key_word_length:].strip()

            if query == _("update"):
                self.bookmarks.fetch_database()
                returns.append(
                    (
                        "",
                        _("Database fetched successfully!"),
                        icon_path,
                        100,
                        1.0,
                        {"actions": ""},
                    )
                )

            for bookmark in self.bookmarks.search(query):
                returns.append(
                    (
                        bookmark[1],
                        bookmark[0],
                        icon_path,
                        100,
                        1.0,
                        {},
                    )
                )

            return returns
        return []

    @dbus.service.method(iface, out_signature="a(sss)")
    def Actions(self) -> list:
        """Return a list of actions."""
        return [
            ("0", _("Open in new window"), "window-new"),
            ("1", _("Copy bookmark URL"), "edit-copy-symbolic"),
        ]

    @dbus.service.method(iface, in_signature="ss")
    def Run(self, data: str, action_id: str) -> None:
        """Handle actions calls."""
        firefox = get_webbrowser("firefox")

        if action_id == "":
            firefox.open_new_tab(data)
        elif action_id == "0":
            firefox.open_new(data)
        elif action_id == "1":
            # Connect to klipper to use the clipboard.
            klipper_iface = dbus.Interface(
                dbus.SessionBus().get_object("org.kde.klipper", "/klipper"),
                "org.kde.klipper.klipper",
            )

            klipper_iface.setClipboardContents(data)
        return None

    @dbus.service.method(iface)
    def Teardown(self):
        """Sava memory by closing database connection when not needed."""
        self.bookmarks.close()


runner = Runner()
loop = GLib.MainLoop()
loop.run()
