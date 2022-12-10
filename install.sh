#!/bin/bash

# Exit if something fails
set -e

mkdir -p ~/.local/share/kservices5/
mkdir -p ~/.local/share/dbus-1/services/

cat "plasma-runner-firefox-bookmarks.desktop" > ~/.local/share/kservices5/plasma-runner-firefox-bookmarks.desktop
sed "s|%{PROJECTDIR}/%{APPNAMELC}.py|${PWD}/main.py|" "io.github.zer0-x.krunner-firefox-bookmarks.service" > ~/.local/share/dbus-1/services/io.github.zer0-x.krunner-firefox-bookmarks.service

kquitapp5 krunner
