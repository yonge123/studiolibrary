# Copyright 2019 by Kurt Rathjen. All Rights Reserved.
#
# This library is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version. This library is distributed in the
# hope that it will be useful, but WITHOUT ANY WARRANTY; without even the
# implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Lesser General Public License for more details.
# You should have received a copy of the GNU Lesser General Public
# License along with this library. If not, see <http://www.gnu.org/licenses/>.
"""
Example:
    
    from PySide2 import QtGui
    import studiolibrary.widgets
    menu = studiolibrary.widgets.LibrariesMenu()
    point = QtGui.QCursor.pos()
    menu.exec_(point)
"""
from functools import partial

from studioqt import QtWidgets

import studiolibrary


class LibrariesMenu(QtWidgets.QMenu):

    def __init__(self, libraryWindow=None):
        super(LibrariesMenu, self).__init__(libraryWindow)

        self.setTitle('Libraries')

        libraries = self.libraries()

        for name in libraries:

            library = libraries[name]

            path = library.get('path', '')
            kwargs = library.get('kwargs', {})

            enabled = True
            if libraryWindow:
                enabled = name != libraryWindow.name()

            action = QtWidgets.QAction(name, self)
            action.setEnabled(enabled)
            callback = partial(self.showLibrary, name, path, **kwargs)
            action.triggered.connect(callback)
            self.addAction(action)

    def showLibrary(self, name, path, **kwargs):
        """
        Show the library window which has given name and path.
        
        :type name: str
        :type path: str 
        :type kwargs: dict 
        """
        studiolibrary.main(name, path, **kwargs)

    def settingsPath(self):
        """
        Get the settings path for the LibraryWindow.

        :rtype: str
        """
        formatString = studiolibrary.config().get('settingsPath')
        return studiolibrary.formatPath(formatString)

    def libraries(self):
        """
        Get all the libraries as a dictionary indexed by name.
        
        :rtype: dict 
        """
        path = self.settingsPath()
        data = studiolibrary.readJson(path)

        return data
