from PyQt6.QtWidgets import QDialog, QVBoxLayout, QComboBox, QPushButton, QLabel, QFileDialog, QMessageBox
import os
from services.document_service import DocumentService

class PrintTemplateDialog(QDialog):
    def __init__(self, context, parent=None):
        super().__init__(parent)
        self.setWindowTitle("In mẫu Word/PDF")
        self.resize(400, 200)
        layout = QVBoxLayout(self)

        # Danh sách template
        self.template_combo = QComboBox()
        self.template_files = [f for f in os.listdir("assets/templates") if f.endswith(".docx")]
        self.template_combo.addItems(self.template_files)
        layout.addWidget(QLabel("Chọn mẫu:"))
        layout.addWidget(self.template_combo)

        # Nút tạo Word
        self.word_btn = QPushButton("Tạo file Word")
        self.word_btn.clicked.connect(self.create_word)
        layout.addWidget(self.word_btn)

        # Nút xuất PDF
        self.pdf_btn = QPushButton("Xuất PDF")
        self.pdf_btn.clicked.connect(self.create_pdf)
        layout.addWidget(self.pdf_btn)

        # Lưu context (dữ liệu điền vào mẫu)
        self.context = context
        self.output_word = ""
        self.output_pdf = ""

    def create_word(self):
        template = os.path.join("assets/templates", self.template_combo.currentText())
        save_path, _ = QFileDialog.getSaveFileName(self, "Lưu file Word", "", "Word Files (*.docx)")
        if save_path:
            DocumentService.export_to_word(template, self.context, save_path)
            self.output_word = save_path
            QMessageBox.information(self, "Thành công", "Đã tạo file Word!")
            try:
                os.startfile(save_path)
            except Exception:
                pass

    def create_pdf(self):
        if not self.output_word:
            QMessageBox.warning(self, "Chưa có file Word", "Hãy tạo file Word trước!")
            return
        save_path, _ = QFileDialog.getSaveFileName(self, "Lưu file PDF", "", "PDF Files (*.pdf)")
        if save_path:
            ok = DocumentService.export_to_pdf(self.output_word, save_path)
            if ok:
                self.output_pdf = save_path
                QMessageBox.information(self, "Thành công", "Đã xuất file PDF!")
                try:
                    os.startfile(save_path)
                except Exception:
                    pass
            else:
                QMessageBox.critical(self, "Lỗi", "Không thể xuất PDF!") 