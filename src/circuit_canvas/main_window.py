import math
import ttg
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from main_widget import MainScreenWidget
from configuration import *

mime_type = "application/x-item"

class CircuitBuilder(QMainWindow):
    def __init__(self, main_window):
        '''
        This is the main circuit builder class; this initilaizes
        the canvas we see on screen.
        main_window: Main GeneTech window from which the circuit buidler is called
        '''
        super().__init__()
        self.main_window = main_window
        self.file_name_image = None
        self.tool_name = 'GeneTech'
        self.plugin_name = 'Circuit Builder'
        self.loadStylesheet("./icons/ssheet.qss")
        self.initUI()
        self.show()

    def loadStylesheet(self, filename):
        '''
        Loads the style sheet at {filename}
        '''
        file = QFile(filename)
        file.open(QFile.ReadOnly | QFile.Text)
        stylesheet = file.readAll()
        QApplication.instance().setStyleSheet(str(stylesheet, encoding='utf-8'))

    def initUI(self):
        '''
        Helper function to set some flags and overall user interface
        of the canvas
        '''
        self.setGeometry(100, 100, 800, 600)
        self.__title = "GeneTech - Circuit Builder"
        self.setWindowTitle(self.__title)
        self.setWindowIcon(QIcon('./icons/SmallLogo.png'))
        #This is to initialize a multi window comprising of drawing like canvas
        self.mdiArea = QMdiArea()
        self.mdiArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.mdiArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.mdiArea.setViewMode(QMdiArea.TabbedView)
        self.mdiArea.setDocumentMode(True)
        self.mdiArea.setTabsClosable(True)
        self.mdiArea.setTabsMovable(True)
        self.setCentralWidget(self.mdiArea)
        self.mdiArea.subWindowActivated.connect(self.updateMenus)
        self.windowMapper = QSignalMapper(self)
        self.windowMapper.mapped[QWidget].connect(self.setActiveSubWindow)
        self.createActions()
        self.createMenus()
        self.createToolBars()
        self.createStatusBar()
        self.updateMenus()
        self.createNodesDock()
        self.readSettings()

    def closeEvent(self, event):
        '''
        Closes the window, and shows the main genetech window
        also writes the position and size of the window so the
        same is loaded next time.
        '''
        self.mdiArea.closeAllSubWindows()
        if self.mdiArea.currentSubWindow():
            event.ignore()
        else:
            self.writeSettings()
            self.main_window.show()
            event.accept()

    def updateMenus(self):
        pass

    def createActions(self):
        '''
        All the actions that appear in the toolbar on the top.
        '''
        #This saves the circuit as an image
        self.capture_action = QAction("Save Image", self)
        self.capture_action.setShortcut("Ctrl+S")
        self.capture_action.setToolTip("Capture image of the circuit you have drawn")
        self.capture_action.triggered.connect(self.captureCircuit)
        #This triggers the converstion of circuit to boolean and exports it back to GeneTech
        self.export_action = QAction("&Export", self)
        self.export_action.setShortcut("Ctrl+E")
        self.export_action.setToolTip("Export Equation of the circuit you have drawn")
        self.export_action.triggered.connect(self.exportCircuit)
        #About and New tabs as usual
        self.about_act = QAction("&About", self, statusTip="Show the application's About box", triggered=self.about)
        self.act_new = QAction('&New', self, shortcut='Ctrl+N', statusTip="Create new graph", triggered=self.onFileNew)

    def getCurrentNodeEditorWidget(self):
        return self.centralWidget()

    def onFileNew(self):
        try:
            subwnd = self.createMdiChild()
            subwnd.show()
        except Exception as e:
            print(e)

    def about(self):
        QMessageBox.about(self, "GeneTech Circuit Builder")

    def setTitle(self):
        title = self.__title + " New Circuit"
        self.setWindowTitle(title)

    def createMenus(self):
        '''
        Creates menus in the toolbar on the top, there are two
        menus currently namely File and Help
        '''
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("File")
        self.statusBar().showMessage("Ready")
        self.file_menu.addAction(self.capture_action)
        self.file_menu.addAction(self.export_action)
        self.file_menu.addAction(self.act_new)
        self.help_menu = self.menuBar().addMenu("&Help")
        self.help_menu.addAction(self.about_act)

    def updateWindowMenu(self):
        pass

    def createToolBars(self):
        pass

    def createNodesDock(self):
        '''
        Creates a moving dock on the right containing drag drop parts.
        The dock can be adjusted and moved anywhere on the canvas.
        '''
        #this contains all the draggable parts
        self.list_box = MyDraggableBox()
        self.items = QDockWidget("Circuit Parts")
        self.items.setWidget(self.list_box)
        self.items.setFloating(False)
        self.addDockWidget(Qt.RightDockWidgetArea, self.items)

    def createMdiChild(self):
        '''
        Creates a new circuit builder canvas on screen.
        '''
        self.circuit_builder = MainScreenWidget(self)
        subwnd = self.mdiArea.addSubWindow(self.circuit_builder)
        return subwnd

    def activeMdiChild(self):
        '''
        This returns the Circuit Builder Widget
        '''
        activeSubWindow = self.mdiArea.activeSubWindow()
        if activeSubWindow:
            return activeSubWindow.widget()
        return None

    def setActiveSubWindow(self, window):
        if window:
            self.mdiArea.setActiveSubWindow(window)

    def createStatusBar(self):
        self.statusBar().showMessage("Ready")

    def setActiveSubWindow(self, window):
        if window:
            self.mdiArea.setActiveSubWindow(window)

    def captureCircuit(self):
        '''
        To save the image of the circuit: This calculates the bounding
        rect that encompasses all the circuit parts on the screen and
        then captures them in the form of an image.
        '''
        if not self.file_name_image:
            filename, filter = QFileDialog.getSaveFileName(self, "Save Circuit To Image")
            self.file_name_image = filename
            self.circuit_builder.scene.grScene.save(filename)
            self.statusBar().showMessage("Saved Successfuly")
        else:
            self.circuit_builder.scene.grScene.save(self.file_name_image)
            self.statusBar().showMessage("Saved Successfuly")

    def exportCircuit(self):
        '''
        Exports the drawn circuit to the main GeneTech window:
        This evaluates the output of the circuit and converts it into boolean form.
        '''
        #Evaluate each part as each part has its own boolean expression
        [part.evaluate_output() for part in self.circuit_builder.scene.parts]
        #Evaluate the output of the output part
        output = self.circuit_builder.circuit_output.evaluate_output() if self.circuit_builder.circuit_output else ''
        if not output: #if no output part is selected
            QMessageBox.critical(self, "Error", "Please select an output node")
        #### This transforms the output into standard sum of product form
        output = output.replace("''", "")
        output = output[1:-1] if output[0] == "(" and output[-1] == ")" else output
        # This creates the truth table
        table_val = ttg.Truths(['IPTG', 'aTc', 'Arabinose'], [output])
        table = table_val.as_pandas()
        #Only select those rows which amount to True
        only_ones = table.loc[table.iloc[:, 3] == 1]
        sop = []
        #All the product terms
        for itr, row in only_ones.iterrows():
            #formatting the product term
            string_ = "IPTG{0}.aTc{1}.Arabinose{2}".format("'"*row[0], "'"*row[1], "'"*row[2])
            sop.append(string_)
        #Sum of all the products
        sop = "+".join(sop)
        #Hide the current window and show the main window, also process the expression
        self.hide()
        self.main_window.show()
        self.main_window.processDrawEquation(sop)

    def readSettings(self):
        '''
        To show the window in the same way as it was shown last time
        '''
        settings = QSettings(self.tool_name, self.plugin_name)
        pos = settings.value('pos', QPoint(200, 200))
        size = settings.value('size', QSize(400, 400))
        self.move(pos)
        self.resize(size)

    def writeSettings(self):
        '''
        Saves the settings of the window to show it at the
        same place and of the size size next time its opened.
        '''
        settings = QSettings(self.tool_name, self.plugin_name)
        settings.setValue('pos', self.pos())
        settings.setValue('size', self.size())


class MyDraggableBox(QListWidget):
    def __init__(self, parent=None):
        '''
        This class concerns the draggable parts that we see on the right
        '''
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        '''
        Helper function to setup the draggable box Widget
        '''
        self.setIconSize(QSize(48, 48))
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setDragEnabled(True)
        self.addMyItems()

    def addMyItems(self):
        '''
        This adds the different draggable items to the QListWidget
        '''
        self.addMyItem("AND", "./icons/AND.svg", AND_GATE)
        self.addMyItem("NOR", "./icons/NOR.svg", NOR_GATE)
        self.addMyItem("NAND", "./icons/NAND.svg", NAND_GATE)
        self.addMyItem("NOT", "./icons/NOT.svg", NOT_GATE)
        self.addMyItem("OR", "./icons/OR.svg", OR_GATE)
        self.addMyItem("INPUT", "./icons/input.png", INPUT_GATE)
        self.addMyItem("OUTPUT", "./icons/output.png", OUTPUT_GATE)

    def addMyItem(self, name, icon=None, part_type=0):
        '''
        Function to add the draggable part to the QListWidget
        name: name of the part
        icon: icon corresponding the part, in case of output its none
        part_type: a number signifying the part type, will help with drag/drop
        [Different parts and their corresponding part type numbers]
        INPUT_GATE = 0
        OUTPUT_GATE = 1
        NOT_GATE = 2
        OR_GATE = 3
        AND_GATE = 4
        NAND_GATE = 5
        NOR_GATE = 6
        '''
        item = QListWidgetItem(name, self)
        pixmap = QPixmap(icon if icon is not None else ".")
        item.setIcon(QIcon(icon))
        item.setSizeHint(QSize(48, 48))
        item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsDragEnabled)
        # setup data
        item.setData(Qt.UserRole, pixmap)
        item.setData(Qt.UserRole + 1, part_type)


    def startDrag(self, *args, **kwargs):
        '''
        Function that enables the dragging of the circuit part.
        '''
        try:
            #gets the item being dragged
            item = self.currentItem()
            #part type of the part, a number signifying what part it is
            part_type = item.data(Qt.UserRole + 1)
            #icon corresponding to the part
            pixmap = QPixmap(item.data(Qt.UserRole))
            itemData = QByteArray()
            dataStream = QDataStream(itemData, QIODevice.WriteOnly)
            dataStream << pixmap
            dataStream.writeInt(part_type)
            dataStream.writeQString(item.text())
            mimeData = QMimeData()
            mimeData.setData(mime_type, itemData)
            drag = QDrag(self)
            drag.setMimeData(mimeData)
            drag.setHotSpot(QPoint(pixmap.width() / 2, pixmap.height() / 2))
            drag.setPixmap(pixmap)
            drag.exec_(Qt.MoveAction)

        except Exception as e:
            print(e)
