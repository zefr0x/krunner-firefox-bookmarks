# Firefox Bookmarks runner
[![Get the runner from kde store](https://raw.githubusercontent.com/ZER0-X/badges/main/kde/store/get-the-app-runner.svg)](https://www.pling.com/p/1722801/)

A KRunner plugin for searching and opening Firefox bookmarks.

# Installation
## Install from git source code
Go to the directory that you want to keep the code in it, for example `/home/<username>/.local/share/krunner-sources/`.
```bash
$ git clone https://github.com/zer0-x/krunner-firefox-bookmarks.git
$ cd krunner-firefox-bookmarks
$ ./install.sh
```
🔴 Don't delete the source code after the installation.
### Uninstall
Go to the source code directory and run the uninstall script:
```bash
$ ./uninstall.sh
```

## Install from the kde store
1. Open system settings
2. Go to `search` > `KRunner`
3. Click on `Get New Plugins...`
4. Search for the Plugin
5. Click `Install`
### Uninstall
Please run the uninstall script manually, because the GUI will remove the script before running it.

# Usage & Configuration
> The key words are different depending on the language so check the list bellow.
1. Type the keyword `f` in KRunner.
2. type `<Space>` and search in your bookmarks.
3. Click `<Enter>` the open the bookmark in a new Firefox tab.
4. Also you are able use the actions to open the bookmark in a new window or copy the URL.
## Fetch the database
> The key words are different depending on the language so check the list bellow.
If want to update the cashed database after modifing your bookmarks.
1. Type the keyword `f` in KRunner.
2. type `<Space>` and then type `update`.
3. You should get a success message.

# Key words list
The key words are different form language to another so check the list bellow to find the appropriate key words for you.
- Arabic
    - `ف`
    - `تحديث`
- English
    - `f`
    - `update`
- ...
    - `f`
    - `update`


# Thanks to
- `Riccardo Massidda` since his extensions [ulauncher-firefox-history](https://github.com/rmassidda/ulauncher-firefox-history) was the base for this runner.
