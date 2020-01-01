# StateModRunner - run StateMod for requested run mode

# NoticeStart
#
# StateMod Java
# StateMod Java is a part of Colorado's Decision Support Systems (CDSS)
# Copyright (C) 2019 Colorado Department of Natural Resources
#
# StateMod Java is free software:  you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
# StateMod Java is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
#     along with StateMod Java.  If not, see <https://www.gnu.org/licenses/>.
#
# NoticeEnd


class StateModRunner:
    """
    StateModRunner runs a StateMod simulation or other run mode.
    """

    def __init__(self, dataset, response_file):
        """
        Constructor. Only need specifiy one of the parameters below.
        :param dataset: if dataset set _dataset to existing dataset
        :param response_file: response file to read dataset.
        """
        if dataset:
            self.dataset = dataset
        if response_file:
            try:
                read_data = True
                read_time_series = True
                use_gui = True
                # TODO @jurentie 04/14/2019 - need to add GUI elements to Python
                parent = None
                dataset.read_statemod_file(response_file, read_data, read_time_series, use_gui, parent)
                self.dataset = dataset
            except Exception as e:
                pass

    def run_baseflows(self):
        """
        Run the baseflow mode.
        """
        print("Running baseflow mode - not enabled.")

    def run_check(self):
        """
        Run the check.
        """
        print("Running check mode - not enabled.")

    def run_simulation(self):
        """
        Run the simulation.
        """
        print("Running simulation - not enabled.")