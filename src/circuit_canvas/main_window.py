import math
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from main_widget import MainScreenWidget


class MainCircuitWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.file_name_image = None
        self.name_company = 'GeneTech'
        self.name_product = 'Circuit Builder'
        self.initUI()
        self.show()
        
    def initUI(self):                
        self.setGeometry(100, 100, 800, 600)
        self.__title = "GeneTech - Circuit Builder"
        self.setWindowTitle(self.__title)
        
        
        self.setWindowIcon(QIcon('../SmallLogo.png'))
        
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
            event.accept()

    def updateMenus(self):
        pass

    def createActions(self):
        self.capture_action = QAction("Save Image", self)
        self.capture_action.setShortcut("Ctrl+S")
        self.capture_action.setToolTip("Capture image of the circuit you have drawn")
        self.capture_action.triggered.connect(self.captureCircuit)

        self.about_act = QAction("&About", self, statusTip="Show the application's About box", triggered=self.about)
    
        self.act_new = QAction('&New', self, shortcut='Ctrl+N', statusTip="Create new graph", triggered=self.onFileNew)
        
    def getCurrentNodeEditorWidget(self):
        return self.centralWidget()
    
    def onFileNew(self):
        try:
            print("here")
            subwnd = self.createMdiChild()
            subwnd.show()
        except Exception as e: dumpException(e)

    
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
        self.file_menu.addAction(self.act_new)
        self.help_menu = self.menuBar().addMenu("&Help")
        self.help_menu.addAction(self.about_act)

    def updateWindowMenu(self):
        pass
        
    def createToolBars(self):
        pass

    def createNodesDock(self):
        '''
        self.myListWidget1 = QListWidget()
        self.myListWidget1.setViewMode(QListWidget.IconMode)
        self.myListWidget1.setAcceptDrops(True)
        self.myListWidget1.setDragEnabled(True)
        
    
        l1 = QListWidgetItem(QIcon('AND.png'), "AND", self.myListWidget1)
        l5 = QListWidgetItem(QIcon('NAND.png'), "NAND", self.myListWidget1)
        l2 = QListWidgetItem(QIcon('OR.png'), "OR", self.myListWidget1)
        l3 = QListWidgetItem(QIcon('NOR.png'), "NOR", self.myListWidget1)
        l4 = QListWidgetItem(QIcon('NOT.png'), "NOT", self.myListWidget1)

        '''
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
        self.addMyItem("AND", "AND.png")
        self.addMyItem("NOR", "NOR.png")
        self.addMyItem("NAND", "NAND.png")
        self.addMyItem("NOT", "NOT.png")
        self.addMyItem("OR", "OR.png")

    def addMyItem(self, name, icon=None, op_code=0):
        item = QListWidgetItem(name, self) # can be (icon, text, parent, <int>type)
        pixmap = QPixmap(icon if icon is not None else ".")
        item.setIcon(QIcon(pixmap))
        item.setSizeHint(QSize(48, 48))

        item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsDragEnabled)

        # setup data
        item.setData(Qt.UserRole, pixmap)
        item.setData(Qt.UserRole + 1, op_code)
