# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "pdbpp>=0.12.1",
#     "pyqt6-qlementine",
# ]
#
# [tool.uv.sources]
# pyqt6-qlementine = { path = "../packages/PyQt6-Qlementine" }
# ///
from PyQt6 import QtWidgets
from PyQt6.QtCore import QJsonDocument, Qt
from PyQt6Qlementine import QlementineStyle, Theme

app = QtWidgets.QApplication([])

style = QlementineStyle(app)
app.setStyle(style)

# Load theme from a JSON string
theme_dict = {
    "meta": {"author": "Olivier Cléro", "name": "Light", "version": "1.5.0"},
    "backgroundColorMain1": "#2d1b4e",
    "backgroundColorMain2": "#3a2560",
    "backgroundColorMain3": "#4a3070",
    "backgroundColorMain4": "#5a3b80",
    "backgroundColorWorkspace": "#1a0f30",
    "backgroundColorTabBar": "#5a3b80",
    "borderColor": "#ff6600",
    "borderColorDisabled": "#804020",
    "borderColorHovered": "#ff8833",
    "borderColorPressed": "#ffaa55",
    "focusColor": "#00ff0066",
    "neutralColor": "#6b4d8a",
    "neutralColorHovered": "#7b5d9a",
    "neutralColorPressed": "#8b6daa",
    "neutralColorDisabled": "#4a3070",
    "primaryColor": "#ff00ff",
    "primaryColorHovered": "#ff44ff",
    "primaryColorPressed": "#ff88ff",
    "primaryColorDisabled": "#662266",
    "primaryAlternativeColor": "#cc00cc",
    "primaryAlternativeColorDisabled": "#551155",
    "primaryAlternativeColorHovered": "#dd22dd",
    "primaryAlternativeColorPressed": "#ee44ee",
    "primaryColorForeground": "#00ff00",
    "primaryColorForegroundDisabled": "#005500",
    "primaryColorForegroundHovered": "#33ff33",
    "primaryColorForegroundPressed": "#66ff66",
    "secondaryColor": "#ff4400",
    "secondaryColorHovered": "#ff6622",
    "secondaryColorPressed": "#ff8844",
    "secondaryColorDisabled": "#663311",
    "secondaryAlternativeColor": "#cc5500",
    "secondaryAlternativeColorDisabled": "#552200",
    "secondaryAlternativeColorHovered": "#dd6611",
    "secondaryAlternativeColorPressed": "#ee7722",
    "secondaryColorForeground": "#00ffff",
    "secondaryColorForegroundDisabled": "#005555",
    "secondaryColorForegroundHovered": "#33ffff",
    "secondaryColorForegroundPressed": "#66ffff",
    "semiTransparentColor1": "#ff00ff0a",
    "semiTransparentColor2": "#ff00ff19",
    "semiTransparentColor3": "#ff00ff21",
    "semiTransparentColor4": "#ff00ff28",
    "shadowColor1": "#ff000020",
    "shadowColor2": "#ff000040",
    "shadowColor3": "#ff000060",
    "statusColorError": "#ff0000",
    "statusColorErrorHovered": "#ff3333",
    "statusColorErrorPressed": "#ff6666",
    "statusColorErrorDisabled": "#660000",
    "statusColorForeground": "#ffff00",
    "statusColorForegroundHovered": "#ffff33",
    "statusColorForegroundPressed": "#ffff66",
    "statusColorForegroundDisabled": "#ffff0099",
    "statusColorInfo": "#00ffff",
    "statusColorInfoHovered": "#33ffff",
    "statusColorInfoPressed": "#66ffff",
    "statusColorInfoDisabled": "#006666",
    "statusColorSuccess": "#00ff00",
    "statusColorSuccessHovered": "#33ff33",
    "statusColorSuccessPressed": "#66ff66",
    "statusColorSuccessDisabled": "#006600",
    "statusColorWarning": "#ffff00",
    "statusColorWarningHovered": "#ffff33",
    "statusColorWarningPressed": "#ffff66",
    "statusColorWarningDisabled": "#666600",
    "useSystemFont": False,
    "fontSize": 12,
    "fontSizeMonospace": 13,
    "fontSizeH1": 34,
    "fontSizeH2": 26,
    "fontSizeH3": 22,
    "fontSizeH4": 18,
    "fontSizeH5": 14,
    "fontSizeS1": 10,
    "spacing": 8,
    "iconExtent": 16,
    "animationDuration": 192,
    "focusAnimationDuration": 384,
    "sliderAnimationDuration": 96,
    "borderRadius": 6.0,
    "checkBoxBorderRadius": 14.0,
    "menuItemBorderRadius": 14.0,
    "menuBarItemBorderRadius": 12.0,
    "borderWidth": 1,
    "focusBorderWidth": 2,
    "controlHeightLarge": 28,
    "controlHeightMedium": 24,
    "controlHeightSmall": 16,
    "controlDefaultWidth": 96,
    "dialMarkLength": 4,
    "dialMarkThickness": 2,
    "dialTickLength": 4,
    "dialTickSpacing": 4,
    "dialGrooveThickness": 4,
    "sliderTickSize": 3,
    "sliderTickSpacing": 2,
    "sliderTickThickness": 1,
    "sliderGrooveHeight": 4,
    "progressBarGrooveHeight": 6,
    "scrollBarThicknessFull": 12,
    "scrollBarThicknessSmall": 6,
    "scrollBarMargin": 0,
    "tabBarPaddingTop": 4,
    "tabBarTabMaxWidth": 0,
    "tabBarTabMinWidth": 0,
}
doc = QJsonDocument.fromVariant(theme_dict)
theme = Theme.fromJsonDoc(doc)  # raises ValueError on failure

# style.setTheme(theme)

sample_widget = QtWidgets.QWidget()
sample_widget.setWindowTitle("Sample Widget")

layout = QtWidgets.QVBoxLayout(sample_widget)
button = QtWidgets.QPushButton("Sample Button")
layout.addWidget(button)
combo = QtWidgets.QComboBox()
combo.addItems(["Option 1", "Option 2", "Option 3"])
layout.addWidget(combo)

slider = QtWidgets.QSlider(Qt.Orientation.Horizontal)
layout.addWidget(slider)
check_box = QtWidgets.QCheckBox("Sample Check Box")
layout.addWidget(check_box)
int_spin = QtWidgets.QSpinBox()
layout.addWidget(int_spin)
float_spin = QtWidgets.QDoubleSpinBox()
layout.addWidget(float_spin)
dial = QtWidgets.QDial()
layout.addWidget(dial)


sample_widget.resize(400, 300)
sample_widget.show()

app.exec()
