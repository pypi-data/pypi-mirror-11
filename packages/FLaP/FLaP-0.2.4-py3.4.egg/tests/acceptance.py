#
# This file is part of Flap.
#
# Flap is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Flap is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Flap.  If not, see <http://www.gnu.org/licenses/>.
#

from unittest import TestCase, main

from flap.ui import main
from flap.FileSystem import OSFileSystem
from flap.path import TEMP


class OSFileSystemTest(TestCase):
    
    def setUp(self):
        self.fileSystem = OSFileSystem()
        self.path = TEMP / "flap" / "test.txt"
        self.content = "blahblah blah"

        self.fileSystem.deleteDirectory(TEMP / "flap")
        self.fileSystem.deleteDirectory(TEMP / "flatexer_copy")
    
    def createAndOpenTestFile(self):
        self.fileSystem.createFile(self.path, self.content)
        return self.fileSystem.open(self.path)
    
    def testCreateAndOpenFile(self):
        file = self.createAndOpenTestFile()
        
        self.assertEqual(file.content(), self.content)

    def testCopyAndOpenFile(self):
        file = self.createAndOpenTestFile()
        
        copyPath = TEMP / "flatexer_copy"
        
        self.fileSystem.copy(file, copyPath)
        copy = self.fileSystem.open(copyPath / "test.txt")
        
        self.assertEqual(copy.content(), self.content)


class Test(TestCase):

    def setUp(self):
        self.fileSystem = OSFileSystem()
        self.workingDir = TEMP / "flap"
        self.source = self.workingDir / "project"
        self.output = self.workingDir / "output"
        self.fileSystem.deleteDirectory(self.workingDir)
        self.fileSystem.createFile(self.source / "main.tex", 
                """
                \\input{result}
                \\include{explanations}
                """)
        self.fileSystem.createFile(self.source / "result.tex", "\\includegraphics{img/plot}")
        self.fileSystem.createFile(self.source / "explanations.tex", "blablah")
        self.fileSystem.createFile(self.source / "img" / "plot.pdf", "\\input{result}")
        self.fileSystem.createFile(self.source / "style.sty", "some style crap")

    def test_flatten_latex_project(self):
        root = self.fileSystem.forOS(TEMP / "flap" / "project" / "main.tex")
        output = self.fileSystem.forOS(TEMP / "flap" / "output")
        main(["-v", root, output])
        
        file = self.fileSystem.open(self.output / "merged.tex")
        self.assertEqual(file.content(), 
                """
                \\includegraphics{plot}
                blablah\\clearpage 
                """)
        
        styFile = self.fileSystem.open(self.output / "style.sty")
        self.assertEqual(styFile.content(), "some style crap")


if __name__ == "__main__":
    main() 