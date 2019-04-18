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

    def __init__(self, dataset, responseFile):
        """
        Constructor. Only need specifiy one of the parameters below.
        :param dataset: if dataset set _dataset to existing dataset
        :param responseFile: response file to read dataset.
        """
        if dataset:
            self.dataset = dataset
        if responseFile:
            try:
                readData = True
                readTimeSeries = True
                useGUI = True
                # TODO @jurentie 04/14/2019 - need to add GUI elements to Python
                parent = None
                dataset.readStateModFile(responseFile, readData, readTimeSeries, useGUI, parent)
                self.dataset = dataset
            except Exception as e:
                pass

    def runBaseFlows(self):
        """
        Run the baseflow mode.
        """
        print("Running baseflow mode.")

    def runCheck(self):
        """
        Run the check.
        """
        print("Running check mode.")

    def runSimulation(self):
        """
        Run the simulation.
        """
        print("Running simulation.")