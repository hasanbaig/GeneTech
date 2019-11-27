import cx_Freeze
from cx_Freeze import *

setup(
    name = "GeneTech",
    options = {'build_exe':{'packages':['pyqt5', 'SchemDraw',
                                        'matplotlib', 'dnaplotlib',
                                        'py4j', 'sbol', 'PIL']}},
    executables = [
        Executable(
            "Genetech.py",
            )
        ] 


    )
