# StateModMain - StateMod main program

# NoticeStart
# StateMod Java
# StateMod Java is a part of Colorado's Decision Support Systems (CDSS)
# Copyright (C) 2019 Colorado Department of Natural Resources
# StateMod Java is free software:  you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
# StateMod Java is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
#     along with StateMod Java.  If not, see <https://www.gnu.org/licenses/>.
# NoticeEnd

import logging
import os
import sys

import RTi.Util.Logging.log_util as log_util

from DWR.StateMod.StateMod_DataSet import StateMod_DataSet
from RTi.Util.IO.IOUtil import IOUtil
from src.cdss.statemod.app.StateModRunner import StateModRunner


class StateModMain:
    # Program Name and Version
    PROGRAM_NAME = "StateMod (Java)"
    PROGRAM_VERSION = "0.1.0 (2019-03-14)"

    # StateMod response file, which is the starting point for reading a StateMod dataset.
    _responseFile = None
    # STateMod dataset object that manages all the data files in a dataset.
    _dataset = None
    # Run mode.
    _runMode = None

    # Working directory, which is the location of the response file.
    # There is no reason to run StateMod very far if a response file is not given.
    _workingDir = None

    def __init__(self):
        pass

    @staticmethod
    def main():
        """
        StateMod main program entry point.
        """
        routine = "StateMod.main"
        logger = logging.getLogger("StateMod")

        args = sys.argv[1:]



        try:
            # Set program name and version
            IOUtil.setProgramData(StateModMain.PROGRAM_NAME, StateModMain.PROGRAM_VERSION, args)

            # Set the initial working directory based on user's starting location
            # - this is used to determine the absolute path for the response file
            StateModMain.setWorkingDirInitial()

            # Determine the response file and working directory so that the log file
            # can be opened.
            # - do this by parsing the command line arguments and detecting response file.
            try:
                initialChecks = True
                StateModMain.parseArgs(args, initialChecks)
            except Exception as e2:
                logger.warning("Error parsing command line. Exiting.")
                logger.warning(e2)
                StateModMain.quitProgram(1)

            # If a response file was not specified, print the usage and exit
            if StateModMain._responseFile is None:
                print("")
                print("No response file was specified")
                print("")
                StateModMain.printUsage()
                StateModMain.quitProgram(1)

            # If a response file was specified but does not exist, print an error and exit
            if not os.path.isfile(StateModMain._responseFile):
                print("")
                print("Response file \"" + str(StateModMain._responseFile) + "\" does not exist.")
                print("")
                StateModMain.printUsage()
                StateModMain.quitProgram(1)

            # Initialize logging
            initializeLogging()

            # Now parse the command line arguments
            # - the response file is determined first so that the working directory is determined
            # - and then other actions are taken
            try:
                initialChecks = False
                StateModMain.parseArgs(args, initialChecks)
            except Exception as e2:
                logger.warning("Error parsing command line. Exiting.")
                logger.warning(e2)
                StateModMain.quitProgram(1)

            if StateModMain._runMode is None:
                print("")
                print("No run mode was specified.")
                print("")
                StateModMain.printUsage()
                StateModMain.quitProgram(1)
            else:
                print("Run mode is " + str(StateModMain._runMode))

            # Error indicator
            error = False

            dataset = None

            # Open the dataset by reading the response file.
            # - try reading dataset files
            try:
                readData = True
                readTimeSeries = True
                useGUI = False
                # TODO @jurentie 04/14/2019 - need to work out GUI components for python
                parent = None
                dataset = StateMod_DataSet()
                dataset.readStateModFile(StateModMain._responseFile, readData, readTimeSeries, useGUI, parent)
            except Exception as e2:
                logger.warning("Error reading response file. See the log file.")
                logger.warning(e2)
                pass

            if not error:
                # Run StateMod for the requested run mode, consistent with the original software
                # but will enhance for additional command line options
                try:
                    StateModMain.runStateMod(dataset, StateModMain._runMode)
                    pass
                except Exception as e2:
                    logger.warning("Error running StateMod. See the log file.")
                    logger.warning(e2)
                    pass
        except Exception as e:
            # Main catch
            logger.warning("Error starting StateMod.")
            logger.warning(e)
            StateModMain.quitProgram(1)

    @staticmethod
    def parseArgs(args, initialChecks):
        """
        Parse command line arguments
        :param args: command line arguments
        :param initialChecks: if true, only parse arguments relevant to initialization
        If false, parse arguments relevant to dataset and simulation.
        """

        # Loop through the arguments twice
        # - the first pass is concerned only with determining the response file and
        # working directory so that the log file can be opened, and some trivial actions
        # like printing usage and version
        # - the second pass processes all the other arguments.

        if initialChecks:
            # Only check command line arguments that result in immediate action (usage, version)
            # and determine the response file and working directory
            ipassToCheck = 0
        else:
            ipassToCheck = 1
        for ipass in range(2):
            for arg in args:
                if arg.upper() == "-BASEFLOWS" or arg.upper() == "--BASEFLOWS":
                    # runMode = StateModRunModType.BASEFLOWS
                    StateModMain._runMode = "BASEFLOWS"
                    pass
                if arg.upper() == "-CHECK" or arg.upper() == "--CHECK":
                    # runMode = StateModRunModeType.CHECK
                    StateModMain._runMode = "CHECK"
                    pass
                elif ipass == ipassToCheck and (arg.upper() == "-H" or arg.upper() == "--HELP"):
                    StateModMain.printUsage()
                    StateModMain.quitProgram(0)
                elif arg.upper() == "-SIM" or arg.upper() == "--SIM":
                    # runMode = StateModRunModeType.SIMULATE
                    StateModMain._runMode = "SIMULATE"
                    pass
                elif arg.startswith("-"):
                    print("Unrecognized option \"" + arg + "\"")
                    StateModMain.printUsage()
                    StateModMain.quitProgram(1)
                elif ipass == ipassToCheck:
                    # The 'response file' that contains a last of all StateMod input files
                    # - allow it to include .rsp or not on command line
                    StateModMain.setResponseFile(arg)

    @staticmethod
    def printUsage():
        """
        Print the program usage. Print the bare minimum.
        """
        nl = os.linesep
        print(nl +
              "statemod-java [options] dataset.rsp" + nl + nl +
              "dataset.rsp             \"response files\" that provides a list of dataset input files. " + nl +
              "-baseflow, --baseflow   Run the baseflow mode with standard options." + nl +
              "-h, --help              Print program usage" + nl +
              "-sim, --sim             Run the simulation with standard options." + nl +
              "-v, --version           Print program version." + nl)

    @staticmethod
    def quitProgram(status):
        """
        Clean up and quit the program
        :param status: Program exit status.
        """
        routine = "StateModMain.quitProgram"
        logger = logging.getLogger("StateMod")
        logger.info("Exiting with status " + str(status) + ".")

        nl = os.linesep
        print("STOP " + str(status) + nl)
        sys.exit()

    @staticmethod
    def runStateMod(datasetToRun, runMode):
        """
        Run StateMod for the provided dataset based on the run mode from the command line.
        :param datasetToRun: the dataset to run
        :param runMode: the run mode to execute
        """
        stateModRunner = StateModRunner(datasetToRun, None)
        if runMode == "BASEFLOWS":
            stateModRunner.runBaseFlows()
        elif runMode == "CHECK":
            stateModRunner.runCheck()
        elif runMode == "SIMULATE":
            stateModRunner.runSimulation()

    @staticmethod
    def setResponseFile(responseFileReq):
        """
        Set the response file name.
        :param responseFileReq: name of the response file.
        If an absolute path, use it. If a relative path, convert to absolute path.
        If the file exists, use the path specified.
        If the '.rsp' exists, use that.
        Consequently the final value is full path that matches an existing file.
        """
        routine = "StateModMain.setResponseFile"
        logger = logging.getLogger("StateMod")
        # First convert the file to absolute path.
        message = "Response file (from command line): " + responseFileReq
        print(message)
        # Message.printStatus(2, routine, message)
        # responseFileAbsolute = IOUtil.verifyPathForOS(IOUtil.toAbsolutePath(IOUtil.getProgramWorkingDir(),
        #                                                                    responseFileReq), True)
        responseFileAbsolute = os.path.abspath(responseFileReq)
        message = "Response file (absolute path): " + responseFileAbsolute
        print(message)
        # Message.printStatus(2, routine, message)
        try:
            f = open(responseFileAbsolute)
            StateModMain._responseFile = responseFileAbsolute
            # Reset the working directory to that of the response file, in case it changed
            # from above logic
            StateModMain._workingDir = os.path.abspath(os.path.join(responseFileAbsolute, os.pardir))
        except FileNotFoundError:
            # Try adding the extension
            responseFileAbsolute2 = responseFileAbsolute + ".rsp"
            f2 = open(responseFileAbsolute2)
            try:
                message = "Response file (with .rsp appended): " + responseFileAbsolute2
                print(message)
                # Message.printStatus(2, routine, message)
                StateModMain._responseFile = responseFileAbsolute2
                # Reset the working directory to that of the response file, in case it changed from
                # above logic
                StateModMain._workingDir = os.path.join(responseFileAbsolute)
            except Exception as e:
                logger.warning(e)

    @staticmethod
    def setWorkingDirInitial():
        routine = "StateModMain.setWorkingDirInitial"
        # The following DOES NOT have slash at the end of the working directory
        workingDir = os.getcwd()
        IOUtil.setProgramWorkingDir(workingDir)
        # Set the dialog because if the running in batch mode and interaction with the
        # graph occurs, this default for dialogs should be the home of the command file.
        message = "Setting working directory to user directory \"" + workingDir + "\"."
        print(message)


def initializeLogging():
    if StateModMain._responseFile is not None:
        print("Setting up customized app logging config")
        logFile = StateModMain._responseFile + ".sim.log"
        initial_file_log_level = logging.DEBUG
        logger = log_util.initialize_logging(app_name="StateMod", logfile_name=logFile,
                                             logfile_log_level=initial_file_log_level)

        # Test some logging messages
        message = "Opened initial log file: '" + logFile + "'"
        logger.info(message)
        # Also print to the console because normally the console should only have error messages
        print(message)


if __name__ == '__main__':
    StateModMain().main()
