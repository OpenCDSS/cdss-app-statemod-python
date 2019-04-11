@echo off
rem Batch file to set the environment for and run PyCharm.
rem - Start PyCharm with the configured environment.

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

:run

rem Echo environment variables for troubleshooting
echo.
echo PATH=%PATH%
rem echo PYTHONHOME=%PYTHONHOME%
rem echo PYTHONPATH=%PYTHONPATH%
echo.

rem Start the PyCharm IDE, /B indicates to use the same windows
rem - command line parameters passed to this script will be passed to PyCharm 
rem - PyCharm will use the Python interpreter configured for the project
echo Starting PyCharm using %PYCHARM% - prompt will display and PyCharm may take a few seconds to start.
start "PyCharm aware of" /B %PYCHARM% %*
goto end

:nopycharm

rem Expected PyCharm was not found
echo Pycharm was not found: %PYCHARM%
exit /b 1

:end