import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLineEdit, QFormLayout, QMessageBox, QComboBox, QLabel, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt
from datetime import datetime, timedelta
import random

class BiletDetayWidget(QWidget):
    def __init__(self, ad, soyad, etkinlik_adi, tarih, yer, etkinlik_tarihi, iptal_durumu):
        super().__init__()
        self.setWindowTitle('Bilet Detayları')
        
        layout = QFormLayout()
        
        ad_label = QLabel('Ad:')
        ad_value = QLabel(ad)
        layout.addRow(ad_label, ad_value)
        
        soyad_label = QLabel('Soyad:')
        soyad_value = QLabel(soyad)
        layout.addRow(soyad_label, soyad_value)
        
        etkinlik_label = QLabel('Etkinlik Adı:')
        etkinlik_value = QLabel(etkinlik_adi)
        layout.addRow(etkinlik_label, etkinlik_value)
        
        tarih_label = QLabel('Tarih:')
        tarih_value = QLabel(tarih)
        layout.addRow(tarih_label, tarih_value)
        
        yer_label = QLabel('Yer:')
        yer_value = QLabel(yer)
        layout.addRow(yer_label, yer_value)
        
        etkinlik_tarihi_label = QLabel('Etkinlik Tarihi:')
        etkinlik_tarihi_value = QLabel(etkinlik_tarihi)
        layout.addRow(etkinlik_tarihi_label, etkinlik_tarihi_value)
        
        iptal_durumu_label = QLabel('İptal Durumu:')
        iptal_durumu_value = QLabel(iptal_durumu)
        layout.addRow(iptal_durumu_label, iptal_durumu_value)
        
        self.setLayout(layout)

class Etkinlik:
    def __init__(self, adi, tarih, yer, fiyat, etkinlik_tarihi):
        self.adi = adi
        self.tarih = tarih
        self.yer = yer
        self.fiyat = fiyat
        self.etkinlik_tarihi = etkinlik_tarihi

class Katilimci:
    def __init__(self, ad, soyad, dogum_tarihi, kredi_karti_bilgileri):
        self.ad = ad
        self.soyad = soyad
        self.dogum_tarihi = dogum_tarihi
        self.kredi_karti_bilgileri = kredi_karti_bilgileri

class Bilet:
    def __init__(self, etkinlik, katilimci):
        self.etkinlik = etkinlik
        self.katilimci = katilimci

    def satin_al(self):
        # Bilet satın alma işlemleri burada gerçekleştirilir
        pass

class EtkinlikSistemiGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.etkinlikler = []
        self.biletler = []
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle('Etkinlik Yönetim Sistemi')
        self.setGeometry(100, 100, 600, 400)
        
        layout = QVBoxLayout()
        
        formLayout = QFormLayout()
        
        self.etkinlikAdiListesi = QComboBox(self)
        self.etkinlikAdiListesi.addItem('Konser')
        self.etkinlikAdiListesi.addItem('Tiyatro')
        self.etkinlikAdiListesi.addItem('Spor Müsabakası')
        
        self.etkinlikAdiListesi.currentIndexChanged.connect(self.etkinlik_seceneklerini_goster)
        
        formLayout.addRow('Etkinlik Türü Seçimi:', self.etkinlikAdiListesi)
        
        self.etkinlikSecenegiLabel = QLabel(self)
        self.etkinlikSecenegiListesi = QComboBox(self)
        
        formLayout.addRow('Etkinlik Seçimi:', self.etkinlikSecenegiListesi)
        
        self.etkinlikFiyatYeriTarihLabel = QLabel(self)  # Fiyat, Yer ve Tarih etiketi
        formLayout.addRow('Fiyat, Yer ve Tarih:', self.etkinlikFiyatYeriTarihLabel)  # Fiyat, Yer ve Tarih etiketini ekle
        
        layout.addLayout(formLayout)
        
        formLayout2 = QFormLayout()
        
        self.katilimciAdiInput = QLineEdit(self)
        self.katilimciSoyadiInput = QLineEdit(self)
        self.dogumTarihiInput = QLineEdit(self)
        self.krediKartiBilgileriInput = QLineEdit(self)
        
        formLayout2.addRow('Adı:', self.katilimciAdiInput)
        formLayout2.addRow('Soyadı:', self.katilimciSoyadiInput)
        formLayout2.addRow('Doğum Tarihi:', self.dogumTarihiInput)
        formLayout2.addRow('Kredi Kartı Bilgileri:', self.krediKartiBilgileriInput)
        
        layout.addLayout(formLayout2)
        
        self.biletSatinAlBtn = QPushButton('Bilet Satın Al', self)
        self.biletSatinAlBtn.clicked.connect(self.bilet_satin_al)
        
        layout.addWidget(self.biletSatinAlBtn)
        
        # Bilet iptal düğmesi
        self.biletIptalBtn = QPushButton('Bilet İptal', self)
        self.biletIptalBtn.clicked.connect(self.bilet_iptal_et)
        layout.addWidget(self.biletIptalBtn)
        
        # Tablo açma/kapatma düğmesi
        self.tabloAcKapatBtn = QPushButton('Tabloyu Aç/Kapat', self)
        self.tabloAcKapatBtn.setCheckable(True)
        self.tabloAcKapatBtn.setChecked(True)
        self.tabloAcKapatBtn.clicked.connect(self.tabloyu_ac_kapat)
        layout.addWidget(self.tabloAcKapatBtn)
        
        self.setLayout(layout)
        
        # Bilet kayıtlarını tutacak tablo
        self.biletTablosu = QTableWidget()
        self.biletTablosu.setColumnCount(7)  # 7 sütun: Ad, Soyad, Etkinlik Adı, Tarih, Yer, Etkinlik Tarihi, İptal Durumu
        self.biletTablosu.setHorizontalHeaderLabels(['Ad', 'Soyad', 'Etkinlik Adı', 'Tarih', 'Yer', 'Etkinlik Tarihi', 'İptal Durumu'])
        self.biletTablosu.cellClicked.connect(self.tablo_satir_tiklandi)
        layout.addWidget(self.biletTablosu)
    
    def etkinlik_seceneklerini_goster(self):
        etkinlik_turu = self.etkinlikAdiListesi.currentText()
        
        self.etkinlikSecenegiListesi.clear()
        
        if etkinlik_turu == 'Konser':
            self.etkinlikSecenegiListesi.addItems(['Adele Konseri', 'U2 Konseri', 'Ed Sheeran Konseri'])
            tarih = datetime.now() + timedelta(days=random.randint(1, 30))  # Rastgele bir tarih oluşturun
            self.etkinlikFiyatYeriTarihLabel.setText('Fiyat: 200 TL, Yer: Stadyum, Tarih: ' + tarih.strftime('%d/%m/%Y'))  # Konser fiyatı, yeri ve tarihini ekleyin
        elif etkinlik_turu == 'Tiyatro':
            self.etkinlikSecenegiListesi.addItems(['Hamlet Oyunu', 'Çılgın Kalabalık Oyunu', 'Kral Lear Oyunu'])
            tarih = datetime.now() + timedelta(days=random.randint(1, 30))  # Rastgele bir tarih oluşturun
            self.etkinlikFiyatYeriTarihLabel.setText('Fiyat: 120 TL, Yer: Tiyatro Salonu, Tarih: ' + tarih.strftime('%d/%m/%Y'))  # Tiyatro fiyatı, yeri ve tarihini ekleyin
        elif etkinlik_turu == 'Spor Müsabakası':
            self.etkinlikSecenegiListesi.addItems(['Basketbol Maçı', 'Futbol Maçı', 'Tenis Turnuvası'])
            tarih = datetime.now() + timedelta(days=random.randint(1, 30))  # Rastgele bir tarih oluşturun
            self.etkinlikFiyatYeriTarihLabel.setText('Fiyat: 50 TL, Yer: Spor Salonu, Tarih: ' + tarih.strftime('%d/%m/%Y'))  # Spor müsabakası fiyatı, yeri ve tarihini ekleyin
    
        self.etkinlikSecenegiLabel.setText('Etkinlik Seçimi:')
    
    def bilet_satin_al(self):
        etkinlik_adi = self.etkinlikSecenegiListesi.currentText()
        adi = self.katilimciAdiInput.text()
        soyadi = self.katilimciSoyadiInput.text()
        dogum_tarihi = self.dogumTarihiInput.text()
        kredi_karti_bilgileri = self.krediKartiBilgileriInput.text()
        etkinlik_tarihi = datetime.now() + timedelta(days=random.randint(1, 30))  # Rastgele bir tarih oluşturun
        etkinlik = Etkinlik(etkinlik_adi, datetime.now(), 'Yer', 0, etkinlik_tarihi)  # Etkinlik tarihini ekleyin
        katilimci = Katilimci(adi, soyadi, dogum_tarihi, kredi_karti_bilgileri)
    
        bilet = Bilet(etkinlik, katilimci)
        bilet.satin_al()
    
        # Bilet bilgilerini tabloya ekle
        self.biletTablosu.insertRow(self.biletTablosu.rowCount())
        self.biletTablosu.setItem(self.biletTablosu.rowCount() - 1, 0, QTableWidgetItem(adi))
        self.biletTablosu.setItem(self.biletTablosu.rowCount() - 1, 1, QTableWidgetItem(soyadi))
        self.biletTablosu.setItem(self.biletTablosu.rowCount() - 1, 2, QTableWidgetItem(etkinlik_adi))
        self.biletTablosu.setItem(self.biletTablosu.rowCount() - 1, 3, QTableWidgetItem(str(datetime.now())))
        self.biletTablosu.setItem(self.biletTablosu.rowCount() - 1, 4, QTableWidgetItem('Yer'))
        self.biletTablosu.setItem(self.biletTablosu.rowCount() - 1, 5, QTableWidgetItem(str(etkinlik_tarihi)))  # Etkinlik tarihi
        self.biletTablosu.setItem(self.biletTablosu.rowCount() - 1, 6, QTableWidgetItem('Aktif'))  # İptal durumu
        self.biletTablosu.item(self.biletTablosu.rowCount() - 1, 6).setBackground(Qt.green)  # Arka plan rengini yeşil yap
    
        QMessageBox.information(self, 'Bilet Satın Alındı', 'Bizi seçtiğiniz için teşekkür ederiz!', QMessageBox.Ok)
        self.show()  # Pencereyi tekrar göster

    def bilet_iptal_et(self):
        # Seçili satırı bul
        secili_satir = self.biletTablosu.currentRow()
        if secili_satir != -1:  # Eğer bir satır seçilmişse
            self.biletTablosu.setItem(secili_satir, 6, QTableWidgetItem('İptal Edildi'))  # İptal durumunu güncelle
            self.biletTablosu.item(secili_satir, 6).setBackground(Qt.red)  # Arka plan rengini kırmızı yap
    
    def tablo_satir_tiklandi(self, row, column):
        # Tıklanan satırın verilerini al
        ad = self.biletTablosu.item(row, 0).text()
        soyad = self.biletTablosu.item(row, 1).text()
        etkinlik_adi = self.biletTablosu.item(row, 2).text()
        tarih = self.biletTablosu.item(row, 3).text()
        yer = self.biletTablosu.item(row, 4).text()
        etkinlik_tarihi = self.biletTablosu.item(row, 5).text()
        iptal_durumu = self.biletTablosu.item(row, 6).text()
        
        # Bilet detaylarını gösteren pencereyi oluştur
        dialog = BiletDetayWidget(ad, soyad, etkinlik_adi, tarih, yer, etkinlik_tarihi, iptal_durumu)
        dialog.show()  # Artık bu bir pencere olduğu için exec_() yerine show() kullanıyoruz
    
    def tabloyu_ac_kapat(self):
        if self.tabloAcKapatBtn.isChecked():
            self.biletTablosu.show()
        else:
            self.biletTablosu.hide()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = EtkinlikSistemiGUI()
    ex.show()
    sys.exit(app.exec_())

