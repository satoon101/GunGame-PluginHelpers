# GunGame PluginHelpers

## Introduction
GunGame PluginHelpers is a set of tools to be used with [GunGame](https://github.com/GunGame-Dev-Team/GunGame-SP) sub-plugins.

These tools allow you to do the following:
* Create a new GunGame sub-plugin.
* Check your plugins for any standards issues.
* Link your plugins to GunGame.
* Create a release .zip file for your plugins.

## Notes
* It is best to use this in addition to [PluginHelpers](https://github.com/satoon101/PluginHelpers), which can help link GunGame to Source.Python and Source.Python to all of your servers.

<br>
## Pre-Setup
Before you get started, there are a few things you will need installed and a few guidelines you need to follow.
* Git
    * Obviously, since this is a git repository, this is going to be necessary.
    * On Windows, install either Git Bash or TortoiseGit (or both).
    * On Linux, use yum or apt-get to install 'git'.
* Python3.4 or newer
    * Python3.4 is required, as [contextlib.suppress](https://docs.python.org/3.4/library/contextlib.html#contextlib.suppress) is used.
    * If you will be using this on a Linux system, most distros come with some version of Python2.  When you install Python3.4, make sure you do not make it the system's default, as that can and will cause you issues.
    * I have found the following to be a good guide to installing Python3.4 on Linux:
        * http://www.unixmen.com/howto-install-python-3-x-in-ubuntu-debian-fedora-centos/
        * Though, the wget and tar lines should look more like:

            ```
wget https://www.python.org/ftp/python/3.4.2/Python-3.4.2.tgz
tar -xjf Python-3.4.2.tgz cd Python-3.4.2
            ```
* GunGame clone
    * Simply use git to clone [GunGame](https://github.com/GunGame-Dev-Team/GunGame-SP).

<br>
## Setup
The first thing you need to do after cloning the repository is to execute the setup file (.bat for Windows or .sh for Linux).
After you have done this, several new files will be created in the main directory.
Those files include the config.ini, which holds configuration values you need to set, and a .pylintrc file which can be used for different pylint settings when running the **plugin_checker** script.
A few platform-specific (.bat for Windows or .sh for Linux) files are also created:
* plugin_checker
* plugin_creater
* plugin_linker
* plugin_releaser
* prerequisites

<br>
## Configuration
The next step is to set up your configuration values.  Open the config.ini and set the values appropriately.
The following are the settings

* AUTHOR
    * used by **plugin_creater** to know what value to put as info.author for the plugin.
* GUNGAME_DIRECTORY
    * used by **plugin_linker** to know where the GunGame repository is located.
    * Defaults:
        * Windows: **C:\Plugins\GunGame**
        * Linux: **/media/GunGame**
* RELEASE_DIRECTORY
    * used by **plugin_releaser** to know where to copy your plugin releases to.
    * Defaults:
        * Windows: **C:\Releases**
        * Linux: **/media/Releases**
* PYTHON_EXECUTABLE
    * used by all of the executables (including prerequisites) to know where the Python executable is located.
    * This needs to be set to the executable file itself and not just its directory.
    * Defaults:
        * Windows: **C:\Python34\python**
        * Linux: **/opt/python3/bin/python3.4**

<br>
## Prerequisite packages
After you have your configuration set, execute the prerequisite script to install the required Python packages.

The required packages for this toolset include:
* [configobj](https://github.com/DiffSK/configobj)
    * used by the Python scripts to get your configuration values.
* [path.py](https://github.com/jaraco/path.py)
    * used by the Python scripts to more easily navigate directories and files on your system.
* [pep8](https://pypi.python.org/pypi/pep8)
    * used by the **plugin_checker** script to check for any PEP8 violations in your plugins.
* [pep257](https://pypi.python.org/pypi/pep257)
    * used by the **plugin_checker** script to check for any PEP257 violations in your plugins.
* [pyflakes](https://pypi.python.org/pypi/pyflakes)
    * used by the **plugin_checker** script to check your plugins for a few different issues.
* [pylint](https://pypi.python.org/pypi/pylint)
    * used by the **plugin_checker** script to check your plugins for a lot of different issues.

<br>
## Installing plugins
If you already have some plugins started, you can copy them into the GunGame PluginHelpers repository directory.  Though, they **must** adhere to some guidelines:
* The directory name needs to be the name of the plugin (the **gg plugin load** name).
* The internal directories need to match that of GunGame's (and Source.Python's) internal directory structure.
    * There must be a directory within the main directory that is named **addons** and contains the following directory structure **../addons/source-python/plugins/gungame/plugins/custom/&lt;plugin_name&gt;/**.
    * Within the above directory, there must be at least a **&lt;plugin_name&gt;.py** file, an **\_\_init\_\_.py** file, and an info.py file.
* It is recommended that you have a public or private repository to host your plugin, but that is not necessary.

<br>
## Creating plugins
GunGame PluginHelpers comes with a script that helps to start the creation of new plugins.  Execute the **plugin_creater** script and answer the questions that follow.

Once you have answered all the necessary questions, the appropriate directories/files will be created.

3 files will always be created:
* \_\_init\_\_.py
    * mandatory for the **plugin_checker** to work.
    * useful for verifying implementation on a server or game prior to loading your plugin.
* info.py
    * holds the [PluginInfo](http://wiki.sourcepython.com/pages/plugins.info#PluginInfo) instance for your plugin.
    * If you supplied an AUTHOR value in the config.ini, that value will be used as info.author.
* &lt;plugin_name&gt;.py
    * mandatory file when using the **gg plugin load** command on a server or game.

<br>
## Linking plugins
Now that you have one or more plugins inside the GunGame PluginHelpers repository directory, you will want to link them to the GunGame repository.

Linking your plugins to the GunGame repository (and with the help of [PluginHelpers](https://github.com/satoon101/PluginHelpers), GunGame to Source.Python) instead of each server/game individually allows you to only have to link them once and have them available on all of your test servers and games.

Execute the **plugin_linker** script and choose which plugin (or ALL plugins) to link.  If you have already linked a plugin, but have added new directories, running the linker again will link those directories.

<br>
## Checking plugins
At some point, or many different points, you might want to check your plugins to see if they match a set of standards (like PEP8 or PEP257).

Execute the **plugin_checker** script and choose which plugin (or ALL plugins) to check and all of the issues/errors/warnings will be shown.

<br>
## Creating a release
Once you get to a point where you think a plugin is ready to be released, execute the **plugin_releaser** script.

Select which plugin to release, or ALL plugins, if you wish to create a release for all of them.

The release .zip file location will be shown, and uses the RELEASEDIR value from the config.ini.

The **plugin_releaser** script does use the info.version value that needs to be set somewhere in your Python code for that script.

Each release is saved as **&lt;RELEASEDIR&gt;/&lt;plugin_name&gt;/&lt;plugin_name&gt;_v&lt;version&gt;.zip**, so that if you have a plugin named my_plugin and its version is 1.0, the file would be **&lt;RELEASEDIR&gt;/my_plugin/my_plugin_v1.0.zip**.
