import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTextEdit, QVBoxLayout, 
                             QHBoxLayout, QWidget, QPushButton, QFontComboBox, 
                             QSpinBox, QColorDialog, QFileDialog, QMessageBox,
                             QToolBar, QAction, QLabel, QComboBox)
from PyQt5.QtGui import QFont, QTextCursor, QImage, QTextImageFormat, QIcon, QColor, QTextCharFormat, QPainter
from PyQt5.QtCore import Qt, QUrl, QMimeData, QBuffer, QIODevice, QSettings
from PyQt5.QtPrintSupport import QPrinter
import os
from datetime import datetime

class NotTutmaUygulamasi(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = QSettings('NotDefteri', 'NotDefteri')
        self.initUI()
        self.dosya_yolu = None
        self.otomatik_kayit_dosyasi = self.getOtomatikKayitYolu()
        self.otomatikKayitYukle()
        
    def getOtomatikKayitYolu(self):
        # Kullanici belgeler klasorunde otomatik kayit dosyasi olustur
        belgeler_klasoru = os.path.expanduser('~')
        uygulama_klasoru = os.path.join(belgeler_klasoru, '.notdefteri')
        if not os.path.exists(uygulama_klasoru):
            os.makedirs(uygulama_klasoru)
        return os.path.join(uygulama_klasoru, 'otomatik_kayit.html')
        
    def initUI(self):
        self.setWindowTitle('Not Defteri Pro')
        
        # Onceki pencere konumu ve boyutunu yukle
        geometry = self.settings.value('geometry')
        if geometry:
            self.restoreGeometry(geometry)
        else:
            self.setGeometry(100, 100, 1000, 700)
        
        # Ana widget ve layout
        ana_widget = QWidget()
        self.setCentralWidget(ana_widget)
        layout = QVBoxLayout()
        ana_widget.setLayout(layout)
        
        # Arac cubugu olustur
        self.aracCubuguOlustur()
        
        # Metin editori
        self.metin_editori = QTextEdit()
        self.metin_editori.setFont(QFont('Arial', 11))
        self.metin_editori.setAcceptDrops(True)
        self.metin_editori.textChanged.connect(self.metinDegisti)
        layout.addWidget(self.metin_editori)
        
        # Yapistirma icin ozel olay yakalama
        self.metin_editori.installEventFilter(self)
        
        # Durum cubugu
        self.statusBar().showMessage('Hazir')
        
        # Stil
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QTextEdit {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QToolBar {
                background-color: #2c3e50;
                spacing: 5px;
                padding: 5px;
            }
            QToolButton {
                background-color: #34495e;
                color: white;
                border: none;
                padding: 8px;
                border-radius: 4px;
            }
            QToolButton:hover {
                background-color: #4a6278;
            }
        """)
        
    def aracCubuguOlustur(self):
        toolbar = QToolBar()
        toolbar.setMovable(False)
        self.addToolBar(toolbar)
        
        # Yeni dosya
        yeni_action = QAction('Yeni', self)
        yeni_action.triggered.connect(self.yeniDosya)
        toolbar.addAction(yeni_action)
        
        # Dosya ac
        ac_action = QAction('Ac', self)
        ac_action.triggered.connect(self.dosyaAc)
        toolbar.addAction(ac_action)
        
        # Kaydet
        kaydet_action = QAction('Kaydet', self)
        kaydet_action.triggered.connect(self.kaydet)
        toolbar.addAction(kaydet_action)
        
        # PDF olarak kaydet
        pdf_action = QAction('PDF Kaydet', self)
        pdf_action.triggered.connect(self.pdfKaydet)
        toolbar.addAction(pdf_action)
        
        toolbar.addSeparator()
        
        # Font ailesi
        self.font_combo = QFontComboBox()
        self.font_combo.currentFontChanged.connect(self.fontDegistir)
        toolbar.addWidget(self.font_combo)
        
        # Font boyutu
        self.font_boyut = QSpinBox()
        self.font_boyut.setValue(11)
        self.font_boyut.setRange(8, 72)
        self.font_boyut.valueChanged.connect(self.fontBoyutuDegistir)
        toolbar.addWidget(self.font_boyut)
        
        toolbar.addSeparator()
        
        # Kalin
        kalin_action = QAction('Kalin', self)
        kalin_action.setCheckable(True)
        kalin_action.triggered.connect(self.kalinYap)
        toolbar.addAction(kalin_action)
        
        # Italik
        italik_action = QAction('Italik', self)
        italik_action.setCheckable(True)
        italik_action.triggered.connect(self.italikYap)
        toolbar.addAction(italik_action)
        
        # Alti cizili
        alticizili_action = QAction('Alti Cizili', self)
        alticizili_action.setCheckable(True)
        alticizili_action.triggered.connect(self.altiCiziliYap)
        toolbar.addAction(alticizili_action)
        
        toolbar.addSeparator()
        
        # Renk secici
        renk_action = QAction('Renk', self)
        renk_action.triggered.connect(self.renkSec)
        toolbar.addAction(renk_action)
        
        # Resim ekle
        resim_action = QAction('Resim Ekle', self)
        resim_action.triggered.connect(self.resimEkle)
        toolbar.addAction(resim_action)
        
        toolbar.addSeparator()
        
        # Hizalama
        self.hizalama_combo = QComboBox()
        self.hizalama_combo.addItems(['Sola', 'Ortala', 'Saga', 'Iki Yana'])
        self.hizalama_combo.currentIndexChanged.connect(self.hizalamaDegistir)
        toolbar.addWidget(self.hizalama_combo)
        
    def metinDegisti(self):
        # Her metin degisiminde otomatik kaydet
        self.otomatikKaydet()
        
    def otomatikKaydet(self):
        try:
            with open(self.otomatik_kayit_dosyasi, 'w', encoding='utf-8') as f:
                f.write(self.metin_editori.toHtml())
        except Exception as e:
            pass  # Sessizce basarisiz ol
            
    def otomatikKayitYukle(self):
        if os.path.exists(self.otomatik_kayit_dosyasi):
            try:
                with open(self.otomatik_kayit_dosyasi, 'r', encoding='utf-8') as f:
                    icerik = f.read()
                    if icerik.strip():  # Bos degilse yukle
                        self.metin_editori.setHtml(icerik)
                        self.statusBar().showMessage('Onceki oturum yuklendi', 3000)
            except Exception as e:
                pass
        
    def eventFilter(self, obj, event):
        # Ctrl+V ile resim yapistirma
        from PyQt5.QtGui import QKeySequence
        if obj == self.metin_editori and event.type() == event.KeyPress:
            if event.matches(QKeySequence.Paste):
                clipboard = QApplication.clipboard()
                mime_data = clipboard.mimeData()
                
                if mime_data.hasImage():
                    image = clipboard.image()
                    self.resimYerlestir(image)
                    return True
                    
        return super().eventFilter(obj, event)
    
    def resimYerlestir(self, image):
        if image.isNull():
            return
            
        # Resmi yeniden boyutlandir (maksimum genislik 600px)
        if image.width() > 600:
            image = image.scaledToWidth(600, Qt.SmoothTransformation)
        
        # Resmi base64'e cevir
        ba = QBuffer()
        ba.open(QIODevice.WriteOnly)
        image.save(ba, 'PNG')
        ba.close()
        
        import base64
        image_data = base64.b64encode(ba.data()).decode('utf-8')
        
        # HTML img etiketi olarak ekle
        cursor = self.metin_editori.textCursor()
        html_img = f'<img src="data:image/png;base64,{image_data}" />'
        cursor.insertHtml(html_img)
        
        self.statusBar().showMessage('Resim eklendi!', 3000)
    
    def resimEkle(self):
        dosya_adi, _ = QFileDialog.getOpenFileName(
            self, 'Resim Sec', '', 
            'Resim Dosyalari (*.png *.jpg *.jpeg *.bmp *.gif)'
        )
        
        if dosya_adi:
            image = QImage(dosya_adi)
            self.resimYerlestir(image)
    
    def fontDegistir(self, font):
        self.metin_editori.setCurrentFont(font)
        
    def fontBoyutuDegistir(self, size):
        self.metin_editori.setFontPointSize(size)
        
    def kalinYap(self, checked):
        if checked:
            self.metin_editori.setFontWeight(QFont.Bold)
        else:
            self.metin_editori.setFontWeight(QFont.Normal)
            
    def italikYap(self, checked):
        self.metin_editori.setFontItalic(checked)
        
    def altiCiziliYap(self, checked):
        self.metin_editori.setFontUnderline(checked)
        
    def renkSec(self):
        renk = QColorDialog.getColor()
        if renk.isValid():
            self.metin_editori.setTextColor(renk)
            
    def hizalamaDegistir(self, index):
        hizalamalar = [
            Qt.AlignLeft,
            Qt.AlignCenter,
            Qt.AlignRight,
            Qt.AlignJustify
        ]
        self.metin_editori.setAlignment(hizalamalar[index])
    
    def yeniDosya(self):
        if self.metin_editori.document().isModified():
            cevap = QMessageBox.question(
                self, 'Kaydet?', 
                'Degisiklikleri kaydetmek istiyor musunuz?',
                QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel
            )
            
            if cevap == QMessageBox.Yes:
                self.kaydet()
            elif cevap == QMessageBox.Cancel:
                return
                
        self.metin_editori.clear()
        self.dosya_yolu = None
        self.setWindowTitle('Not Defteri Pro - Yeni Dosya')
        # Otomatik kayit dosyasini temizle
        if os.path.exists(self.otomatik_kayit_dosyasi):
            os.remove(self.otomatik_kayit_dosyasi)
        
    def dosyaAc(self):
        dosya_adi, _ = QFileDialog.getOpenFileName(
            self, 'Dosya Ac', '', 
            'HTML Dosyalari (*.html);;Metin Dosyalari (*.txt);;Tum Dosyalar (*)'
        )
        
        if dosya_adi:
            with open(dosya_adi, 'r', encoding='utf-8') as f:
                icerik = f.read()
                self.metin_editori.setHtml(icerik)
                self.dosya_yolu = dosya_adi
                self.setWindowTitle(f'Not Defteri Pro - {os.path.basename(dosya_adi)}')
                
    def kaydet(self):
        if self.dosya_yolu:
            self.dosyayaKaydet(self.dosya_yolu)
        else:
            self.farkliKaydet()
            
    def farkliKaydet(self):
        dosya_adi, _ = QFileDialog.getSaveFileName(
            self, 'Farkli Kaydet', '', 
            'HTML Dosyalari (*.html);;Metin Dosyalari (*.txt)'
        )
        
        if dosya_adi:
            self.dosyayaKaydet(dosya_adi)
            
    def dosyayaKaydet(self, dosya_adi):
        with open(dosya_adi, 'w', encoding='utf-8') as f:
            f.write(self.metin_editori.toHtml())
        self.dosya_yolu = dosya_adi
        self.metin_editori.document().setModified(False)
        self.setWindowTitle(f'Not Defteri Pro - {os.path.basename(dosya_adi)}')
        self.statusBar().showMessage('Kaydedildi!', 3000)
        
    def pdfKaydet(self):
        dosya_adi, _ = QFileDialog.getSaveFileName(
            self, 'PDF Olarak Kaydet', '', 
            'PDF Dosyalari (*.pdf)'
        )
        
        if dosya_adi:
            if not dosya_adi.endswith('.pdf'):
                dosya_adi += '.pdf'
                
            printer = QPrinter(QPrinter.HighResolution)
            printer.setOutputFormat(QPrinter.PdfFormat)
            printer.setOutputFileName(dosya_adi)
            
            self.metin_editori.document().print_(printer)
            self.statusBar().showMessage(f'PDF kaydedildi: {dosya_adi}', 3000)
            QMessageBox.information(self, 'Basarili', f'PDF basariyla kaydedildi:\n{dosya_adi}')
    
    def closeEvent(self, event):
        # Pencere konumu ve boyutunu kaydet
        self.settings.setValue('geometry', self.saveGeometry())
        
        if self.metin_editori.document().isModified():
            cevap = QMessageBox.question(
                self, 'Cikis', 
                'Degisiklikleri PDF olarak kaydetmek istiyor musunuz?',
                QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel
            )
            
            if cevap == QMessageBox.Yes:
                self.pdfKaydet()
                event.accept()
            elif cevap == QMessageBox.No:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    pencere = NotTutmaUygulamasi()
    pencere.show()
    sys.exit(app.exec_())
