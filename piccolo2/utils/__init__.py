# Copyright 2018- The Piccolo Team
#
# This file is part of piccolo2-utils.
#
# piccolo2-client is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# piccolo2-utils is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with piccolo2-utils.  If not, see <http://www.gnu.org/licenses/>.

from pkg_resources import get_distribution, DistributionNotFound
try:
    __version__ = get_distribution('piccolo2-utils').version
except DistributionNotFound:
    # package is not installed
    pass


from calibrateConfig import *
from calibrateData import *
