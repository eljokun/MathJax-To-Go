from PySide6.QtCore import Qt, QMimeData, QByteArray
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QLabel, QPushButton, QWidget, QApplication, QMainWindow, QTextEdit, QVBoxLayout, \
    QHBoxLayout, QFileDialog

ver = "v1.5"
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle(f"MathJax To Go - {ver}")

        # Properties and equation init
        self.svgData = ""
        self.equation = r"\Large \text{you gonna type something or what?}"
        self.autoCopy = False
        self.physicsEnabled = False
        self.colorsv2Enabled = False
        self.displayStyle = True
        self.equation_edit = QTextEdit()
        self.equation_edit.setPlaceholderText("Type Equation Here")
        self.equation_edit.setAcceptRichText(False)

        # Create layout
        layout = QVBoxLayout()
        interactiveWindowLayout = QHBoxLayout()
        interactiveWindowLayout.addWidget(self.equation_edit)
        optionInsertionLayout = QVBoxLayout()
        interactiveWindowLayout.addLayout(optionInsertionLayout)
        optionLowerLayout = QHBoxLayout()

        # Load webengine
        self.mathjax_script = r'<script type="text/javascript" async src = "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg-full.js"> </script>'
        self.view = QWebEngineView()
        self.load_mathjax()
        self.view.loadFinished.connect(self.update_mathjax)
        interactiveWindowLayout.addWidget(self.view)

        # Add svg copy button
        self.copyButton = QPushButton("Copy SVG")
        self.copyButton.setStyleSheet("background-color: darkgreen")
        self.copyButton.clicked.connect(self.copySvg)

        # Add svg auto-copy button
        self.autoCopyButton = QPushButton("Auto-Copy")
        self.autoCopyButton.setStyleSheet("background-color: darkred")
        self.autoCopyButton.clicked.connect(self.toggleAutoCopy)

        # Add button to save svg as file
        self.saveButton = QPushButton("Save SVG")
        self.saveButton.setStyleSheet("background-color: #222288")
        self.saveButton.clicked.connect(self.saveSvg)

        # Add button to toggle using physics package
        self.usePhysicsButton = QPushButton("Physics")
        self.usePhysicsButton.setStyleSheet("background-color: darkred")
        self.usePhysicsButton.clicked.connect(self.togglePhysics)

        # Add button to toggle colorsv2 pkg
        self.useColorsv2Button = QPushButton("Colorsv2")
        self.useColorsv2Button.setStyleSheet("background-color: darkred")
        self.useColorsv2Button.clicked.connect(self.toggleColorsv2)

        # Add preamble label
        self.preambleLabel = QLabel("ⓘ Optional Preamble: ")
        # Add hover details for preamble label
        self.preambleLabel.setToolTip('By default, tex2svg adds in all TeX packages except physics and colorsv2.'
                                      '\n You can choose to use them.'
                                      '\n If you use \\color or anything that uses commands from the color package,'
                                      '\n the tex autoloader will automatically load it.')
        # Add developer label :3
        self.developerLabel = QLabel("ⓘ Developed with love by github.com/eljokun")

        # Add preamble button toggles to layout
        optionLowerLayout.addWidget(self.preambleLabel)
        optionLowerLayout.addWidget(self.usePhysicsButton)
        optionLowerLayout.addWidget(self.useColorsv2Button)
        optionLowerLayout.addStretch()
        optionLowerLayout.addWidget(self.developerLabel)
        optionLowerLayout.addStretch()
        optionLowerLayout.addWidget(self.saveButton)
        optionLowerLayout.addWidget(self.autoCopyButton)
        optionLowerLayout.addWidget(self.copyButton)

        # Add button to make window always on top
        self.alwaysOnTopButton = QPushButton("Always On Top")
        self.alwaysOnTopButton.setStyleSheet("background-color: darkred")
        self.alwaysOnTopButton.clicked.connect(self.toggleAlwaysOnTop)
        optionInsertionLayout.addWidget(self.alwaysOnTopButton)

        # Display style toggle
        self.displayStyleButton = QPushButton("Display Style")
        self.displayStyleButton.setStyleSheet("background-color: darkgreen")
        self.displayStyleButton.clicked.connect(self.toggleDisplayStyle)
        optionInsertionLayout.addWidget(self.displayStyleButton)

        # Clear contents
        self.clearButton = QPushButton("Clear")
        self.clearButton.setStyleSheet("background-color: #442222")
        self.clearButton.clicked.connect(lambda: self.equation_edit.clear())
        optionInsertionLayout.addWidget(self.clearButton)

        # Insert label
        self.insertLabel = QLabel("ⓘ Insert")
        self.insertLabel.setToolTip('Insert LaTeX classics at your caret position.')
        optionInsertionLayout.addWidget(self.insertLabel)

        # Add dfrac
        self.addDFracButton = QPushButton("dfrac")
        self.addDFracButton.setStyleSheet("background-color: #444444")
        self.addDFracButton.clicked.connect(lambda: self.addTextAtCursorPosition(r"\dfrac{ }{ }"))
        optionInsertionLayout.addWidget(self.addDFracButton)

        # Add text
        self.addTextButton = QPushButton("text")
        self.addTextButton.setStyleSheet("background-color: #444444")
        self.addTextButton.clicked.connect(lambda: self.addTextAtCursorPosition(r"\text{  }"))
        optionInsertionLayout.addWidget(self.addTextButton)

        # Add cases(system)
        self.addCasesButton = QPushButton("cases (system)")
        self.addCasesButton.setStyleSheet("background-color: #444444")
        self.addCasesButton.clicked.connect(lambda: self.addTextAtCursorPosition(r"\begin{cases}    \end{cases}"))
        optionInsertionLayout.addWidget(self.addCasesButton)

        # Add partial derivative
        self.addPartialDerivativeButton = QPushButton("partial derivative")
        self.addPartialDerivativeButton.setStyleSheet("background-color: #444444")
        self.addPartialDerivativeButton.clicked.connect(lambda: self.addTextAtCursorPosition(r"\dfrac{\partial }{\partial }"))
        optionInsertionLayout.addWidget(self.addPartialDerivativeButton)

        # Add tex array button
        self.addTexArrayButton = QPushButton("array")
        self.addTexArrayButton.setStyleSheet("background-color: #444444")
        self.addTexArrayButton.clicked.connect(lambda: self.addTextAtCursorPosition(r"\begin{array}{c}  \end{array}"))
        optionInsertionLayout.addWidget(self.addTexArrayButton)

        # Add aligned
        self.addAlignedButton = QPushButton("aligned")
        self.addAlignedButton.setStyleSheet("background-color: #444444")
        self.addAlignedButton.clicked.connect(lambda: self.addTextAtCursorPosition(r"\begin{aligned}  \end{aligned}"))
        optionInsertionLayout.addWidget(self.addAlignedButton)

        # Add limit
        self.addLimitButton = QPushButton("lim")
        self.addLimitButton.setStyleSheet("background-color: #444444")
        self.addLimitButton.clicked.connect(lambda: self.addTextAtCursorPosition(r"\lim_{x \to }"))
        optionInsertionLayout.addWidget(self.addLimitButton)

        # Add sum and limits
        self.addSumButton = QPushButton("sum")
        self.addSumButton.setStyleSheet("background-color: #444444")
        self.addSumButton.clicked.connect(lambda: self.addTextAtCursorPosition(r"\sum\limits_{ }^{ }"))
        optionInsertionLayout.addWidget(self.addSumButton)

        # Add 3x3 matrix
        self.addMatrixButton = QPushButton("matrix")
        self.addMatrixButton.setStyleSheet("background-color: #444444")
        self.addMatrixButton.clicked.connect(lambda: self.addTextAtCursorPosition(r"\left[\begin{matrix} \end{matrix}\right]"))
        optionInsertionLayout.addWidget(self.addMatrixButton)

        # Add underbrace
        self.addUnderbraceButton = QPushButton("underbrace selection")
        self.addUnderbraceButton.setStyleSheet("background-color: #444444")
        self.addUnderbraceButton.clicked.connect(lambda: self.wrapSelectedText(r"\underbrace{", "}_{ }"))

        # Finalize insertions layout
        optionInsertionLayout.addWidget(self.addUnderbraceButton)
        optionInsertionLayout.addStretch()

        # Add layouts to main layout
        layout.addLayout(interactiveWindowLayout)
        layout.addLayout(optionLowerLayout)

        # Confirm layout and initialize central widget
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        self.update_mathjax()
        self.equation_edit.textChanged.connect(self.update_mathjax)

    def toggleDisplayStyle(self):
        self.displayStyle = not self.displayStyle
        self.displayStyleButton.setStyleSheet("background-color: darkgreen" if self.displayStyle else "background-color: darkred")
        self.update_mathjax()

    def toggleAlwaysOnTop(self):
        wasMaximized = self.isMaximized()
        if self.windowFlags() & Qt.WindowStaysOnTopHint:
            self.setWindowFlags((self.windowFlags() & ~Qt.WindowStaysOnTopHint) | Qt.WindowCloseButtonHint)
            self.alwaysOnTopButton.setStyleSheet("background-color: darkred")
        else:
            self.setWindowFlags((self.windowFlags() | Qt.WindowStaysOnTopHint) | Qt.WindowCloseButtonHint)
            self.alwaysOnTopButton.setStyleSheet("background-color: darkgreen")
        self.show()
        if wasMaximized:
            self.showMaximized()

    def togglePhysics(self):
        self.physicsEnabled = not self.physicsEnabled
        self.usePhysicsButton.setStyleSheet(
            "background-color: darkgreen" if self.physicsEnabled else "background-color: darkred")
        self.load_mathjax()

    def toggleColorsv2(self):
        self.colorsv2Enabled = not self.colorsv2Enabled
        self.useColorsv2Button.setStyleSheet(
            "background-color: darkgreen" if self.colorsv2Enabled else "background-color: darkred")
        self.load_mathjax()

    def getSvg(self, callback):
        self.view.page().toHtml(callback)

    def handleSvg(self, svg):
        self.svgData = svg

    def copySvg(self):
        def callback(html):
            # Extract the SVG data from the HTML content
            start = html.find('<svg')
            end = html.find('</svg>', start)
            svg = html[start:end + 6]
            svg = svg.replace('currentColor', 'black')
            clipboard = QApplication.clipboard()
            mimeData = QMimeData()
            mimeData.setData('image/svg+xml', QByteArray(svg.encode()))
            clipboard.setMimeData(mimeData)
        self.getSvg(callback)

    def saveSvg(self):
        def callback(html):
            start = html.find('<svg')
            end = html.find('</svg>', start)
            svg = html[start:end + 6]
            svg = svg.replace('currentColor', 'black')
            # File dialog
            savefile, _ = QFileDialog.getSaveFileName(self, 'Save SVG', '', 'SVG files (*.svg)')
            if savefile and not len(self.equation)==0:
                with open(savefile, 'w') as f:
                    f.write(svg)
        self.getSvg(callback)

    def toggleAutoCopy(self):
        self.autoCopy = not self.autoCopy
        self.autoCopyButton.setStyleSheet("background-color: green" if self.autoCopy else "background-color: darkred")
        self.copyButton.setEnabled(not self.autoCopy)
        self.copyButton.setStyleSheet("background-color: gray" if self.autoCopy else "background-color: darkgreen")

    def addTextAtCursorPosition(self, text):
        self.equation_edit.textCursor().insertText(text)

    def wrapSelectedText(self, left, right):
        cursor = self.equation_edit.textCursor()
        selected_text = cursor.selectedText()
        cursor.insertText(left + selected_text + right)
        self.equation_edit.setTextCursor(cursor)

    # MathJax loading for webengine
    # Preamble and allat stuff goes here
    # The idea is to load the script then for every text change update the math content, schedule mathjax render and
    # render/extract (copy if enabled) svg.
    def load_mathjax(self):
        base_packages = ['base', 'ams', 'bbox', 'boldsymbol', 'braket', 'cancel', 'color', 'enclose', 'extpfeil',
                         'html', 'mhchem', 'newcommand', 'noerrors', 'unicode', 'verb', 'autoload', 'require',
                         'configmacros', 'tagformat', 'action', 'bbox', 'boldsymbol', 'colorv2', 'enclose', 'extpfeil',
                         'html', 'mhchem', 'newcommand', 'noerrors', 'unicode', 'verb', 'autoload', 'require',
                         'configmacros', 'tagformat', 'action']

        if self.physicsEnabled:
            base_packages.append('physics')
        else:
            try:
                base_packages.remove('physics')
            except ValueError:
                pass

        # Convert the list of packages to a string
        packages_str = ', '.join(f"'{pkg}'" for pkg in base_packages)

        # Define the loader packages
        loader_packages = ['[tex]/physics'] if self.physicsEnabled else ['[tex]/autoload']
        loader_packages_str = ', '.join(f"'{pkg}'" for pkg in loader_packages)

        html = """
        <!DOCTYPE html>
        <html>
        <style>
        body {{
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                background-color: darkgray;
            }}
        </style>
        <head>
            <script type="text/x-mathjax-config">
                MathJax = {{
                    loader: {{
                        load: [{loader_packages}]
                    }},
                    svg: {{
                        fontCache: 'global'
                        stroke: 'black'
                    }},
                    tex: {{
                        displayMath: [['$$','$$']],
                        packages: {{'[+]': [{packages}]}}
                    }}
                }};
            </script>
            {mathjax_script}
        </head>
        <body>
            <p id="math-content">
            </p>
            <script>
                var svg;
                var isDragging = false;
                var previousMousePosition;

                document.addEventListener('mousedown', function(event) {{
                    svg = document.querySelector('svg');
                    if (svg) {{
                        isDragging = true;
                        previousMousePosition = {{ x: event.clientX, y: event.clientY }};
                    }}
                }});

                document.addEventListener('mousemove', function(event) {{
                    if (isDragging && svg) {{
                        var dx = event.clientX - previousMousePosition.x;
                        var dy = event.clientY - previousMousePosition.y;
                        var transform = svg.getAttribute('transform') || '';
                        transform += ' translate(' + dx + ' ' + dy + ')';
                        svg.setAttribute('transform', transform);
                        previousMousePosition = {{ x: event.clientX, y: event.clientY }};
                    }}
                }});
                document.addEventListener('mouseup', function(event) {{
                    isDragging = false;
                }});
            </script>
        </body>
        </html>
        """.format(packages=packages_str, loader_packages=loader_packages_str, mathjax_script=self.mathjax_script)
        self.update_mathjax()
        self.view.setHtml(html)

    def update_mathjax(self):
        plainTextEquation = self.equation_edit.toPlainText()
        def formatted(plainTxtEq):
            if not plainTxtEq:
                plainTxtEq = r"\Large \text{you gonna type something or what?}"
            return plainTxtEq.replace("\\", "\\\\").replace("\n","\\n").replace("'", "\\'")
        physicsPreamble = formatted(r"\require{physics} ") if self.physicsEnabled else r""
        displayStylePreamble = formatted(r"\displaystyle ") if self.displayStyle else r""
        self.equation = f"{displayStylePreamble}{physicsPreamble}{formatted(plainTextEquation)}"
        script = r"""
        var element = document.getElementById('math-content');
        var svg = MathJax.tex2svg('{}').outerHTML;
        element.innerHTML = svg;
        """.format(self.equation)
        self.view.page().runJavaScript(script)
        if self.autoCopy:
            self.copySvg()


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
