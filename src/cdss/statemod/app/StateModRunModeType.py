# StateModRunModeType - StateMod run modes

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

from enum import Enum


class StateModRunModeType(Enum):
    """
    Enumeration for StateMod run mode types.
    """
    BASEFLOWS = 1
    CHECK = 2
    SIMULATE = 3

    def __str__(self):
        """
        Format the enumeration as a string - just return the name.
        @returns Enumeration as a string.
        """
        return self.name