@echo off
rem Batch file to set the environment for and run PyCharm.
rem - Start PyCharm with the configured environment.

rem Get the current folder of the script, used to specify the path to the project
rem - will have \ at the end
SET SM_CURRENT_DIR=%~dp0%
echo Script directory=%SM_CURRENT_DIR%

rem Set an environment variable to indicate that the environment is setup.
rem - this ensures that setup is done once
rem - then PyCharm can be restarted in the same window without reconfiguring the environment.

if "%PYCHARM_STATEMOD_ENV_SETUP%"=="YES" GOTO run
echo Setting up PyCharm environment to use Python environment

rem Set the absolute path to PyCharm program
rem - sort with most recent last so that the newest version is run 
rem - this assumes that the developer is using the newest version installed for development.
if exist "C:\Program Files\JetBrains\PyCharm Community Edition 2018.1.3\bin\pycharm64.exe" SET PYCHARM="C:\Program Files\JetBrains\PyCharm Community Edition 2018.1.3\bin\pycharm64.exe"
if exist "C:\Program Files\JetBrains\PyCharm Community Edition 2018.2.4\bin\pycharm64.exe" SET PYCHARM="C:\Program Files\JetBrains\PyCharm Community Edition 2018.2.4\bin\pycharm64.exe"
if exist "C:\Program Files\JetBrains\PyCharm Community Edition 2018.2.6\bin\pycharm64.exe" SET PYCHARM="C:\Program Files\JetBrains\PyCharm Community Edition 2018.2.6\bin\pycharm64.exe"
if not exist %PYCHARM% goto nopycharm

rem Set the Python to use
rem - list the following in order so most recent is at the end
rem if exist C:\Program Files\Python37 set PYTHONPATH=C:\Program Files\Python37

rem Set the environment variable that lets this batch file know that the environment is set up
set PYCHARM_STATEMOD_ENV_SETUP=YES

rem Set the libraries in the python path
set PYTHONPATH=%PYTHONPATH%;%USERPROFILE%\cdss-dev\StateMod-Python\git-repos\cdss-lib-cdss-python\src
set PYTHONPATH=%PYTHONPATH%;%USERPROFILE%\cdss-dev\StateMod-Python\git-repos\cdss-lib-common-python\src
set PYTHONPATH=%PYTHONPATH%;%USERPROFILE%\cdss-dev\StateMod-Python\git-repos\cdss-lib-models-python\src

:run

rem Echo environment variables for troubleshooting
echo.
echo PATH=%PATH%
rem echo PYTHONHOME=%PYTHONHOME%
echo PYTHONPATH=%PYTHONPATH%
echo.

rem Start the PyCharm IDE, /B indicates to use the same windows
rem - command line parameters passed to this script will be passed to PyCharm 
rem - PyCharm will use the Python interpreter configured for the project
rem - Specify the folder for the project so it does not default to some other project
rem   that was opened last
echo Starting PyCharm using %PYCHARM% - prompt will display and PyCharm may take a few seconds to start.
SET SM_PROJECT_DIR=%SM_CURRENT_DIR%..
if exist %SM_PROJECT_DIR% start "PyCharm aware of StateMod project" /B %PYCHARM% %SM_PROJECT_DIR% %*
if not exist %SM_PROJECT_DIR% goto noproject
goto endofbat

:noproject
rem No project directory (should not happen)
echo Project folder does not exist:  %SM_PROJECT_DIR%
echo Not starting PyCharm.
exit /b 1

:nopycharm

rem Expected PyCharm was not found
echo PyCharm was not found in expected location C:\Program Files\JetBrains\PyCharm Community Edition NNNN.N.N\bin\pycharm64.exe
echo May need to update this script for newer versions of PyCharm.
exit /b 1

:endofbat
