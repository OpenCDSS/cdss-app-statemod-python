# StateModMain - StateMod main program

# NoticeStart
# StateMod Python
# StateMod Python is a part of Colorado's Decision Support Systems (CDSS)
# Copyright (C) 2019 Colorado Department of Natural Resources
# StateMod Python is free software:  you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
# StateMod Python is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
#     along with StateMod Python.  If not, see <https://www.gnu.org/licenses/>.
# NoticeEnd

import logging
import os
from pathlib import Path
import psutil
import sys

import RTi.Util.Logging.log_util as log_util

from cdss.statemod.app.StateModRunModeType import StateModRunModeType
from cdss.statemod.app.StateModRunner import StateModRunner
from DWR.StateMod.StateMod_DataSet import StateMod_DataSet
from DWR.StateMod.StateMod_DataSetComponentType import StateMod_DataSetComponentType
from DWR.StateMod.StateMod_Diversion import StateMod_Diversion
from DWR.StateMod.StateMod_TS import StateMod_TS
from RTi.Util.IO.IOUtil import IOUtil
from RTi.Util.IO.PropList import PropList


class StateModMain:
    """
    Main StateMod program class.
    """

    # Program Name and Version
    PROGRAM_NAME = "StateMod (Java)"
    PROGRAM_VERSION = "0.1.0 (2019-12-30)"

    # StateMod response file from command line, which is the starting point for reading a StateMod dataset.
    response_file = None

    # StateMod response file as Path
    response_file_path = None

    # StateMod dataset object that manages all the data files in a dataset.
    dataset = None

    # Run mode.
    run_mode = None

    # Working directory, which is the location of the response file.
    # There is no reason to run StateMod very far if a response file is not given.
    working_dir = None

    def __init__(self):
        """
        Constructor.
        """
        pass

    def main(self):
        """
        StateMod main program entry point.
        """
        logger = logging.getLogger(__name__)

        args = sys.argv[1:]

        try:
            # Set program name and version
            print("Setting program data...")
            IOUtil.set_program_data(self.PROGRAM_NAME, self.PROGRAM_VERSION, args)
            print("...back from setting program data.")

            # Set the initial working directory based on user's starting location
            # - this is used to determine the absolute path for the response file
            self.set_working_dir_initial()

            # Determine the response file and working directory so that the log file
            # can be opened.
            # - do this by parsing the command line arguments and detecting response file.
            try:
                initial_checks = True
                self.parse_args(args, initial_checks)
            except Exception as e2:
                logger.warning("Error parsing command line. Exiting.", exc_info=True)
                self.quit_program(1)

            # If a response file was not specified, print the usage and exit
            if self.response_file is None:
                print("")
                print("No response file was specified")
                print("")
                self.print_usage()
                self.quit_program(1)

            # If a response file was specified but does not exist, print an error and exit
            if not self.response_file_path.exists():
                print("")
                print("Response file as absolute path could not be determined from \"" +
                      str(self.response_file) + "\".")
                print("")
                self.print_usage()
                self.quit_program(1)

            # Initialize logging
            # - do after parsing command line parameters because need to determine run mode
            # - the response file will exist so the path will also be defined
            self.initialize_logging()
            logger.info("Back from initializing logging.")

            # Print memory usage to log file
            process = psutil.Process(os.getpid())
            logging.info("Memory use after startup:  " + str(process.memory_info().rss))

            # Now parse the command line arguments
            # - the response file is determined first so that the working directory is determined
            # - and then other actions are taken
            try:
                initial_checks = False
                self.parse_args(args, initial_checks)
            except Exception as e2:
                logger.warning("Error parsing command line. Exiting.", exc_info=True)
                self.quit_program(1)

            if self.run_mode is None:
                print("")
                print("No run mode was specified.")
                print("")
                self.print_usage()
                self.quit_program(1)
            else:
                message = "Run mode is " + str(self.run_mode)
                print(message)
                logger.info(message)

            # Error indicator
            error = False

            self.dataset = None

            # Open the dataset by reading the response file.
            # - try reading dataset files
            try:
                read_data = True
                read_time_series = True
                use_gui = False
                # TODO @jurentie 04/14/2019 - need to work out GUI components for python
                parent = None
                self.dataset = StateMod_DataSet()
                self.dataset.read_statemod_file(self.response_file_path, read_data, read_time_series, use_gui, parent)

            except Exception as e2:
                message = "Error reading response file. See the log file."
                logger.warning(message, exc_info=True)
                print(message + "  See log file.")
                pass

            # Print memory usage
            process = psutil.Process(os.getpid())
            logging.info("Memory use after reading dataset:  " + str(process.memory_info().rss))

            # For testing, output the diversion stations and diversion historical monthly time series
            # - use kdiff3 to do visual comparison of data lines
            dds_comp = self.dataset.get_component_for_component_type(StateMod_DataSetComponentType.DIVERSION_STATIONS)
            dds_infile = None
            dds_outfile = dds_comp.get_data_file_name() + ".testout"
            new_comments = []
            use_daily_data = True
            StateMod_Diversion.write_statemod_file(dds_infile, dds_outfile,
                                                   dds_comp.get_data(), new_comments, use_daily_data)

            ddh_comp = self.dataset.get_component_for_component_type(
                StateMod_DataSetComponentType.DIVERSION_TS_MONTHLY)
            ddh_infile = None
            ddh_outfile = ddh_comp.get_data_file_name() + ".testout"
            props = PropList("")
            props.set(key="CalendarType", value="Water")
            props.set(key="OutputFile", value=ddh_outfile)
            props.set(key="OutputPrecision", value="0")
            # Write using properties, which will open the output file.
            StateMod_TS.write_time_series_list_props(ddh_comp.get_data(), props)

            if not error:
                # Run StateMod for the requested run mode, consistent with the original software
                # but will enhance for additional command line options
                try:
                    self.run_statemod(self.dataset, self.run_mode)
                    pass
                except Exception as e2:
                    message = "Error running StateMod."
                    logger.warning(message, exc_info=True)
                    print(message + "  See log file.")
                    self.quit_program(1)
                    pass
        except Exception as e:
            # Main catch
            message = "Error running StateMod."
            logger.warning(message, exc_info=True)
            print(message + "  See log file.")
            self.quit_program(1)

    def parse_args(self, args, initial_checks):
        """
        Parse command line arguments
        :param args: command line arguments
        :param initial_checks: if true, only parse arguments relevant to initialization
        If false, parse arguments relevant to dataset and simulation.
        """

        # Loop through the arguments twice
        # - the first pass is concerned only with determining the response file and
        # working directory so that the log file can be opened, and some trivial actions
        # like printing usage and version
        # - the second pass processes all the other arguments.

        if initial_checks:
            # Only check command line arguments that result in immediate action (usage, version)
            # and determine the response file and working directory
            ipass_to_check = 0
        else:
            ipass_to_check = 1
        for ipass in range(2):
            for arg in args:
                if arg.upper() == "-BASEFLOWS" or arg.upper() == "--BASEFLOWS":
                    self.run_mode = StateModRunModeType.BASEFLOWS
                    pass
                if arg.upper() == "-CHECK" or arg.upper() == "--CHECK":
                    self.run_mode = StateModRunModeType.CHECK
                    pass
                elif ipass == ipass_to_check and (arg.upper() == "-H" or arg.upper() == "--HELP"):
                    self.print_usage()
                    self.quit_program(0)
                elif arg.upper() == "-SIM" or arg.upper() == "--SIM":
                    self.run_mode = StateModRunModeType.SIMULATE
                    pass
                elif arg.startswith("-"):
                    print("Unrecognized option \"" + arg + "\"")
                    self.print_usage()
                    self.quit_program(1)
                elif ipass == ipass_to_check:
                    # The 'response file' that contains a last of all StateMod input files
                    # - allow it to include .rsp or not on command line
                    self.set_response_file(arg)

    def print_usage(self):
        """
        Print the program usage. Print the bare minimum.
        """
        nl = os.linesep
        print(nl +
              "statemod-java [options] dataset.rsp" + nl + nl +
              "dataset.rsp             \"Response file\" that provides a list of dataset input files. " + nl +
              "-baseflow, --baseflow   Run the baseflow mode with standard options." + nl +
              "-h, --help              Print program usage" + nl +
              "-sim, --sim             Run the simulation with standard options." + nl +
              "-v, --version           Print program version." + nl)

    def quit_program(self, status):
        """
        Clean up and quit the program
        :param status: Program exit status.
        """
        logger = logging.getLogger(__name__)
        logger.info("Exiting with status " + str(status) + ".")

        nl = os.linesep
        print("STOP " + str(status) + nl)
        sys.exit(status)

    def run_statemod(self, dataset_to_run, run_mode):
        """
        Run StateMod for the provided dataset based on the run mode from the command line.
        :param dataset_to_run: the dataset to run
        :param run_mode: the run mode to execute
        """
        statemod_runner = StateModRunner(dataset_to_run, None)
        if run_mode == StateModRunModeType.BASEFLOWS:
            statemod_runner.run_baseflows()
        elif run_mode == StateModRunModeType.CHECK:
            statemod_runner.run_check()
        elif run_mode == StateModRunModeType.SIMULATE:
            statemod_runner.run_simulation()

    def set_response_file(self, response_file_req):
        """
        Set the response file name.
        :param response_file_req: name of the response file.
        If an absolute path, use it. If a relative path, convert to absolute path.
        If the file exists, use the path specified.
        If the '.rsp' exists, use that.
        Consequently the final value is full path that matches an existing file.
        """
        logger = logging.getLogger(__name__)
        # Save the user input, may or may not have path, used for loggin messages
        self.response_file = response_file_req
        # First convert the file to absolute path.
        message = "Response file (from command line): " + response_file_req
        print(message)
        logger.info(message)
        # Message.printStatus(2, routine, message)
        # response_file_absolute = IOUtil.verifyPathForOS(IOUtil.toAbsolutePath(IOUtil.getProgramWorkingDir(),
        #                                                                    responseFileReq), True)
        # TODO smalers 2019-12-31 the following may or may not work in all cases depending on starting folder
        # - need to run more tests
        response_file_absolute = os.path.abspath(response_file_req)
        message = "Response file (absolute path): " + response_file_absolute
        print(message)
        logger.info(message)
        # Message.printStatus(2, routine, message)
        self.response_file_path = Path(response_file_absolute)
        if self.response_file_path.exists():
            # Reset the working directory to that of the response file, in case it changed
            # from above logic
            message = "Response file (with .rsp) exists:  " + str(self.response_file_path)
            print(message)
            logger.info(message)
            self.working_dir = self.response_file_path.parent
        elif not response_file_absolute.endswith(".rsp"):
            # Try adding the extension
            response_file_absolute2 = response_file_absolute + ".rsp"
            self.response_file_path = Path(response_file_absolute2)
            if self.response_file_path.exists():
                message = "Response file (with .rsp appended) exists: " + response_file_absolute2
                print(message)
                logger.info(message)
                # Reset the working directory to that of the response file, in case it changed from
                # above logic
                self.working_dir = self.response_file_path.parent
            else:
                # Reset the path to None since did not find a valid path
                message = "Response file (with .rsp appended) does not exist: " + response_file_absolute2
                print(message)
                logger.warning(message)
                self.response_file_path = None
        else:
            message = "Response file (with .rsp) does not exist:  " + str(self.response_file_path)
            print(message)
            logger.warning(message)

    def set_working_dir_initial(self):
        # The following DOES NOT have slash at the end of the working directory
        working_dir = os.getcwd()
        IOUtil.set_program_working_dir(working_dir)
        # Set the dialog because if the running in batch mode and interaction with the
        # graph occurs, this default for dialogs should be the home of the command file.
        message = "Setting working directory to user directory \"" + working_dir + "\"."
        print(message)
        logger = logging.getLogger(__name__)
        logger.info(message)

    def initialize_logging(self):
        if self.response_file is not None:
            print("Setting up customized app logging configuration.")
            run_mode_string = "unknown"
            if self.run_mode == StateModRunModeType.BASEFLOWS:
                run_mode_string = "baseflows"
            elif self.run_mode == StateModRunModeType.CHECK:
                run_mode_string = "check"
            elif self.run_mode == StateModRunModeType.SIMULATE:
                run_mode_string = "sim"
            log_file = self.response_file_path.as_posix() + "." + run_mode_string + ".log"
            # Log level that is finest level to print
            initial_file_log_level = logging.DEBUG
            logger = log_util.initialize_logging(app_name="StateMod", logfile_name=log_file,
                                                 logfile_log_level=initial_file_log_level)

            # Test some logging messages
            message = "Opened initial log file: '" + log_file + "'"
            logger.info(message)
            # Also print to the console because normally the console should only have error messages
            print(message)


if __name__ == '__main__':
    # Declare an instance of the main program
    statemod_main = StateModMain()
    statemod_main.main()
