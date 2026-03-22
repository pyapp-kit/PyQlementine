"""Tests for QlementineStyle."""

from __future__ import annotations

from _qt_compat import Qlementine

QlementineStyle = Qlementine.QlementineStyle
Theme = Qlementine.Theme
AutoIconColor = Qlementine.AutoIconColor


def test_create_style(qapp):
    style = QlementineStyle()
    assert style is not None


def test_animations_enabled_by_default(qapp):
    style = QlementineStyle()
    assert style.animationsEnabled() is True


def test_set_animations_disabled(qapp):
    style = QlementineStyle()
    style.setAnimationsEnabled(False)
    assert style.animationsEnabled() is False


def test_default_auto_icon_color(qapp):
    style = QlementineStyle()
    assert style.autoIconColor() == AutoIconColor.None_


def test_set_auto_icon_color(qapp):
    style = QlementineStyle()
    style.setAutoIconColor(AutoIconColor.ForegroundColor)
    assert style.autoIconColor() == AutoIconColor.ForegroundColor

    style.setAutoIconColor(AutoIconColor.TextColor)
    assert style.autoIconColor() == AutoIconColor.TextColor


def test_theme_returns_theme_object(qapp):
    style = QlementineStyle()
    theme = style.theme()
    assert isinstance(theme, Theme)


def test_set_theme(qapp):
    style = QlementineStyle()
    theme = Theme()
    theme.meta.name = "Custom"
    theme.borderRadius = 20.0
    style.setTheme(theme)
    assert style.theme().borderRadius == 20.0


def test_trigger_complete_repaint(qapp):
    """Just verify it doesn't crash."""
    style = QlementineStyle()
    style.triggerCompleteRepaint()


def test_theme_all_public_fields(qapp):
    """Verify all public fields from Theme.hpp are accessible."""
    theme = Theme()

    # Colors
    assert theme.backgroundColorMain1.isValid()
    assert theme.backgroundColorMain2.isValid()
    assert theme.backgroundColorMain3.isValid()
    assert theme.backgroundColorMain4.isValid()
    assert theme.backgroundColorMainTransparent is not None
    assert theme.backgroundColorWorkspace.isValid()
    assert theme.backgroundColorTabBar.isValid()
    assert theme.neutralColor.isValid()
    assert theme.neutralColorHovered.isValid()
    assert theme.neutralColorPressed.isValid()
    assert theme.neutralColorDisabled.isValid()
    assert theme.neutralColorTransparent is not None
    assert theme.focusColor is not None
    assert theme.primaryColor.isValid()
    assert theme.primaryColorHovered.isValid()
    assert theme.primaryColorPressed.isValid()
    assert theme.primaryColorDisabled.isValid()
    assert theme.primaryColorTransparent is not None
    assert theme.primaryColorForeground.isValid()
    assert theme.primaryColorForegroundHovered.isValid()
    assert theme.primaryColorForegroundPressed.isValid()
    assert theme.primaryColorForegroundDisabled.isValid()
    assert theme.primaryColorForegroundTransparent is not None
    assert theme.primaryAlternativeColor.isValid()
    assert theme.primaryAlternativeColorHovered.isValid()
    assert theme.primaryAlternativeColorPressed.isValid()
    assert theme.primaryAlternativeColorDisabled.isValid()
    assert theme.primaryAlternativeColorTransparent is not None
    assert theme.secondaryColor.isValid()
    assert theme.secondaryColorHovered.isValid()
    assert theme.secondaryColorPressed.isValid()
    assert theme.secondaryColorDisabled.isValid()
    assert theme.secondaryColorTransparent is not None
    assert theme.secondaryColorForeground.isValid()
    assert theme.secondaryColorForegroundHovered.isValid()
    assert theme.secondaryColorForegroundPressed.isValid()
    assert theme.secondaryColorForegroundDisabled.isValid()
    assert theme.secondaryColorForegroundTransparent is not None
    assert theme.secondaryAlternativeColor.isValid()
    assert theme.secondaryAlternativeColorHovered.isValid()
    assert theme.secondaryAlternativeColorPressed.isValid()
    assert theme.secondaryAlternativeColorDisabled.isValid()
    assert theme.secondaryAlternativeColorTransparent is not None
    assert theme.statusColorSuccess.isValid()
    assert theme.statusColorSuccessHovered.isValid()
    assert theme.statusColorSuccessPressed.isValid()
    assert theme.statusColorSuccessDisabled.isValid()
    assert theme.statusColorInfo.isValid()
    assert theme.statusColorInfoHovered.isValid()
    assert theme.statusColorInfoPressed.isValid()
    assert theme.statusColorInfoDisabled.isValid()
    assert theme.statusColorWarning.isValid()
    assert theme.statusColorWarningHovered.isValid()
    assert theme.statusColorWarningPressed.isValid()
    assert theme.statusColorWarningDisabled.isValid()
    assert theme.statusColorError.isValid()
    assert theme.statusColorErrorHovered.isValid()
    assert theme.statusColorErrorPressed.isValid()
    assert theme.statusColorErrorDisabled.isValid()
    assert theme.statusColorForeground.isValid()
    assert theme.statusColorForegroundHovered.isValid()
    assert theme.statusColorForegroundPressed.isValid()
    assert theme.statusColorForegroundDisabled is not None
    assert theme.shadowColor1 is not None
    assert theme.shadowColor2 is not None
    assert theme.shadowColor3 is not None
    assert theme.shadowColorTransparent is not None
    assert theme.borderColor.isValid()
    assert theme.borderColorHovered.isValid()
    assert theme.borderColorPressed.isValid()
    assert theme.borderColorDisabled.isValid()
    assert theme.borderColorTransparent is not None
    assert theme.semiTransparentColor1 is not None
    assert theme.semiTransparentColor2 is not None
    assert theme.semiTransparentColor3 is not None
    assert theme.semiTransparentColor4 is not None
    assert theme.semiTransparentColorTransparent is not None

    # Scalar values
    assert isinstance(theme.useSystemFonts, bool)
    assert isinstance(theme.fontSize, int)
    assert isinstance(theme.fontSizeMonospace, int)
    assert isinstance(theme.fontSizeH1, int)
    assert isinstance(theme.fontSizeH2, int)
    assert isinstance(theme.fontSizeH3, int)
    assert isinstance(theme.fontSizeH4, int)
    assert isinstance(theme.fontSizeH5, int)
    assert isinstance(theme.fontSizeS1, int)
    assert isinstance(theme.animationDuration, int)
    assert isinstance(theme.focusAnimationDuration, int)
    assert isinstance(theme.sliderAnimationDuration, int)
    assert isinstance(theme.borderRadius, float)
    assert isinstance(theme.checkBoxBorderRadius, float)
    assert isinstance(theme.menuItemBorderRadius, float)
    assert isinstance(theme.menuBarItemBorderRadius, float)
    assert isinstance(theme.borderWidth, int)
    assert isinstance(theme.controlHeightLarge, int)
    assert isinstance(theme.controlHeightMedium, int)
    assert isinstance(theme.controlHeightSmall, int)
    assert isinstance(theme.controlDefaultWidth, int)
    assert isinstance(theme.dialMarkLength, int)
    assert isinstance(theme.dialMarkThickness, int)
    assert isinstance(theme.dialTickLength, int)
    assert isinstance(theme.dialTickSpacing, int)
    assert isinstance(theme.dialGrooveThickness, int)
    assert isinstance(theme.focusBorderWidth, int)
    assert theme.iconSize is not None
    assert theme.iconSizeMedium is not None
    assert theme.iconSizeLarge is not None
    assert theme.iconSizeExtraSmall is not None
    assert isinstance(theme.sliderTickSize, int)
    assert isinstance(theme.sliderTickSpacing, int)
    assert isinstance(theme.sliderTickThickness, int)
    assert isinstance(theme.sliderGrooveHeight, int)
    assert isinstance(theme.progressBarGrooveHeight, int)
    assert isinstance(theme.spacing, int)
    assert isinstance(theme.scrollBarThicknessFull, int)
    assert isinstance(theme.scrollBarThicknessSmall, int)
    assert isinstance(theme.scrollBarMargin, int)
    assert isinstance(theme.tabBarPaddingTop, int)
    assert isinstance(theme.tabBarTabMaxWidth, int)
    assert isinstance(theme.tabBarTabMinWidth, int)
