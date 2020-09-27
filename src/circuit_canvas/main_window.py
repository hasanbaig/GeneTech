import math
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from main_widget import MainScreenWidget

mime_type = "application/x-item"

class CircuitBuilder(QMainWindow):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.file_name_image = None
        self.name_company = 'GeneTech'
        self.name_product = 'Circuit Builder'
        self.loadStylesheet("./icons/ssheet.qss")
        self.initUI()
        self.show()

    def loadStylesheet(self, filename):
        file = QFile(filename)
        file.open(QFile.ReadOnly | QFile.Text)
        stylesheet = file.readAll()
        QApplication.instance().setStyleSheet(str(stylesheet, encoding='utf-8'))

    def initUI(self):
        self.setGeometry(100, 100, 800, 600)
        self.__title = "GeneTech - Circuit Builder"
        self.setWindowTitle(self.__title)


        self.setWindowIcon(QIcon('./icons/SmallLogo.png'))

        #self.captureCircuit()
        #self.show()


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
        self.capture_action = QAction("Save Image", self)
        self.capture_action.setShortcut("Ctrl+S")
        self.capture_action.setToolTip("Capture image of the circuit you have drawn")
        self.capture_action.triggered.connect(self.captureCircuit)

        self.export_action = QAction("&Export", self)
        self.export_action.setShortcut("Ctrl+E")
        self.export_action.setToolTip("Export Equation of the circuit you have drawn")
        self.export_action.triggered.connect(self.exportCircuit)

        self.about_act = QAction("&About", self, statusTip="Show the application's About box", triggered=self.about)

        self.act_new = QAction('&New', self, shortcut='Ctrl+N', statusTip="Create new graph", triggered=self.onFileNew)

    def getCurrentNodeEditorWidget(self):
        return self.centralWidget()

    def onFileNew(self):
        try:
            print("here")
            subwnd = self.createMdiChild()
            subwnd.show()
        except Exception as e: print(e)


    def about(self):
        QMessageBox.about(self, "GeneTech Circuit Builder")

    def setTitle(self):
        title = self.__title + " New Circuit"
        self.setWindowTitle(title)

    def createMenus(self):
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
        self.list_box = MyDraggableBox()
        self.items = QDockWidget("Circuit Parts")
        self.items.setWidget(self.list_box)
        self.items.setFloating(False)
        self.addDockWidget(Qt.RightDockWidgetArea, self.items)

    def createMdiChild(self):
        self.circuit_builder = MainScreenWidget(self)
        subwnd = self.mdiArea.addSubWindow(self.circuit_builder)
        return subwnd

    def activeMdiChild(self):
        """ we're returning NodeEditorWidget here... """
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
        if not self.file_name_image:
            filename, filter = QFileDialog.getSaveFileName(self, "Save Circuit To Image")
            self.file_name_image = filename
            self.circuit_builder.scene.grScene.save(filename)
            self.statusBar().showMessage("Saved Successfuly")
        else:
            self.circuit_builder.scene.grScene.save(self.file_name_image)
            self.statusBar().showMessage("Saved Successfuly")

    def exportCircuit(self):
        [part.evaluate_output() for part in self.circuit_builder.scene.parts]
        output = self.circuit_builder.circuit_output.evaluate_output() if self.circuit_builder.circuit_output else ''
        if not output:
            print("output not set ")
            QMessageBox.critical(self, "Error", "Please select an output node")
        output = output.replace("''", "")
        output = output[1:-1] if output[0] == "(" and output[-1] == ")" else output
        import ttg

        table_val = ttg.Truths(['IPTG', 'aTc', 'Arabinose'], [output])
        table = table_val.as_pandas()
        only_ones = table.loc[table.iloc[:, 3] == 1]
        sop = []
        for itr, row in only_ones.iterrows():
            string_ = "IPTG{0}.aTc{1}.Arabinose{2}".format("'"*row[0], "'"*row[1], "'"*row[2])
            sop.append(string_)
        sop = "+".join(sop)
        self.hide()
        self.main_window.show()
        self.main_window.processDrawEquation(sop)
        print("YES")

    def readSettings(self):
        settings = QSettings(self.name_company, self.name_product)
        pos = settings.value('pos', QPoint(200, 200))
        size = settings.value('size', QSize(400, 400))
        self.move(pos)
        self.resize(size)

    def writeSettings(self):
        settings = QSettings(self.name_company, self.name_product)
        settings.setValue('pos', self.pos())
        settings.setValue('size', self.size())




input_gate = 0
output_gate = 1
NOT_gate = 2
OR_gate = 3
AND_gate = 4
NAND_gate = 5
NOR_gate = 6

class MyDraggableBox(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        # init
        self.setIconSize(QSize(48, 48))
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setDragEnabled(True)

        self.addMyItems()


    def addMyItems(self):
        self.addMyItem("AND", "./icons/AND.svg", AND_gate)
        self.addMyItem("NOR", "./icons/NOR.svg", NOR_gate)
        self.addMyItem("NAND", "./icons/NAND.svg", NAND_gate)
        self.addMyItem("NOT", "./icons/NOT.svg", NOT_gate)
        self.addMyItem("OR", "./icons/OR.svg", OR_gate)
        self.addMyItem("INPUT", "./icons/input.png", input_gate)
        self.addMyItem("OUTPUT", "./icons/output.png", output_gate)

    def addMyItem(self, name, icon=None, op_code=0):
        item = QListWidgetItem(name, self) # can be (icon, text, parent, <int>type)
        pixmap = QPixmap(icon if icon is not None else ".")
        item.setIcon(QIcon(icon))
        item.setSizeHint(QSize(48, 48))

        item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsDragEnabled)

        # setup data
        item.setData(Qt.UserRole, pixmap)
        item.setData(Qt.UserRole + 1, op_code)


    def startDrag(self, *args, **kwargs):
        print("ListBox::startDrag")

        try:
            item = self.currentItem()
            op_code = item.data(Qt.UserRole + 1)
            print("dragging item <%d>" % op_code, item)

            pixmap = QPixmap(item.data(Qt.UserRole))


            itemData = QByteArray()
            dataStream = QDataStream(itemData, QIODevice.WriteOnly)
            dataStream << pixmap
            dataStream.writeInt(op_code)
            dataStream.writeQString(item.text())

            mimeData = QMimeData()
            mimeData.setData(mime_type, itemData)

            drag = QDrag(self)
            drag.setMimeData(mimeData)
            drag.setHotSpot(QPoint(pixmap.width() / 2, pixmap.height() / 2))
            drag.setPixmap(pixmap)

            drag.exec_(Qt.MoveAction)

        except Exception as e: print(e)
