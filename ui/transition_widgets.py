from PyQt6.QtWidgets import QStackedWidget, QWidget
from PyQt6.QtCore import QPropertyAnimation, QEasingCurve

class TransitionStackedWidget(QStackedWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._anim_duration = 220
        self._animating = False

    def setCurrentIndex(self, index: int):
        if self.currentIndex() == index or self._animating:
            super().setCurrentIndex(index)
            return
        old_widget = self.currentWidget()
        new_widget = self.widget(index)
        if old_widget and new_widget:
            self._animating = True
            old_widget.raise_()
            new_widget.setWindowOpacity(0)
            new_widget.show()
            anim_out = QPropertyAnimation(old_widget, b"windowOpacity")
            anim_out.setDuration(self._anim_duration)
            anim_out.setStartValue(1)
            anim_out.setEndValue(0)
            anim_out.setEasingCurve(QEasingCurve.Type.InOutQuad)
            anim_in = QPropertyAnimation(new_widget, b"windowOpacity")
            anim_in.setDuration(self._anim_duration)
            anim_in.setStartValue(0)
            anim_in.setEndValue(1)
            anim_in.setEasingCurve(QEasingCurve.Type.InOutQuad)
            def on_finished():
                super(TransitionStackedWidget, self).setCurrentIndex(index)
                old_widget.setWindowOpacity(1)
                new_widget.setWindowOpacity(1)
                self._animating = False
            anim_out.finished.connect(on_finished)
            anim_out.start()
            anim_in.start()
        else:
            super().setCurrentIndex(index) 