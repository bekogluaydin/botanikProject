# 🌱 Botanik Kayıt Sistemi – Proje Dökümantasyonu

Bu proje, herbaryum, tohum bankası ve diğer botanik verilerin yönetimi için geliştirilmiştir.


## 📌 Proje Özeti

**Botanik Kayıt Sistemi**, Nezahat Gökyiğit Botanik Bahçesi gibi kurumların botanik verilerini (herbaryum, tohum bankası, DNA bankası vb.) merkezi, güvenli ve kontrollü bir şekilde yönetmesini sağlayan bir yazılım projesidir.

---

## 🎯 Projenin Amacı

- Bitki örneklerine ait kayıtların dijital ortamda tutulması.
- Kullanıcıların sadece yetkili oldukları alanlarda işlem yapabilmesi.
- Verilerin kalıcılığını korumak için “soft delete” (pasif hâle getirme) mantığı uygulanması.
- Accession (aksesyon) numaralandırma ile arşivsel bütünlük sağlanması.

---

## 📂 Proje Yapısı

- Ortak şablonlar templates/ klasöründe tutulur.
- Ortak statik dosyalar (css, js- görseller vb.) static/ klasöründe tutulur.
- Her app kendi işlemlerinden sorumludur.
- account uygulaması: Giriş, kullanıcı yetkileri(Kullanıcı Yetkileri Tablosu, Kullanıcı Grubu vb.), toplayıcı yönetimi(Collector).

| Uygulama | Açıklama |
|----------|----------|
| `botanik` | Ana proje yapılandırması (`settings.py`, `urls.py`, Diğer uygulamları entegre etmek vb.) |
| `botanik_core` | Proje genelinde kullanılacak Yetkilendirme, temel modeller, tablo yönetimi |
| `account` | Giriş, Kayıt Olma, Şifremi Değiştir, kullanıcı yetkileri (Kullanıcı Yetkileri Tablosu, Kullanıcı Grubu vb.), toplayıcı defteri (Collector) işlemleri |
| `accession_record` | Aksesyon numaralı kayıtların yönetimi - CRUD işlemleri ve yetki kontrolü |

---

## 🧰 Teknik Detaylar

- Django 4.x
- SQLite (DB için)
- Pillow (görsel işleme desteği, fotoğraf ekleme vb.)
- django-phonenumber-field
- Bootstrap 5 ile responsive arayüz
- Soft delete ve custom permission sistemleri entegre

---

## 🚀 Projeyi Başlatma


### 1. Reposu Klonla

git clone <repo_link>
cd <proje_dizini>


### 2. Sanal Ortam Oluştur ve Aktifleştir

```python
python -m venv .venv
source .venv/bin/activate     # Mac/Linux
.venv\Scripts\activate        # Windows
```

### 3. Gerekli Paketleri Yükle

```python
pip install -r requirements.txt
```

### 4. Veritabanı Kurulumu ve Migrasyonlar

```python
python manage.py makemigrations
python manage.py migrate
```


### 5. Süper Kullanıcı Oluştur

```python
python manage.py createsuperuser
```

### 6. Bahçe Lokasyonları için Seeder Çalıştır

```python
python manage.py seed_garden_locations
```

### 7. Geliştirme Sunucusunu Başlat

```python
python manage.py runserver
```

###  8. Normal Giriş

```python
http://127.0.0.1:8000/account/login/
```

### 9. Super Admin Giriş (Super User için)

```python
http://127.0.0.1:8000/admin/
```

---

## ✅ Ek Bilgiler

- Bahçe Lokasyonlarını proje başlangıcında otomatik sisteme kayıt etmek için seed_garden_locations adında Seeder oluşturdum.
  - botanik_core>management>commands altında.

### 📘 TablePermissionArea

- Projedeki tablo isimleri bu modelle yönetilir (örnek: Herbarium, TohumBankasi).
- Yeni model eklendiğinde otomatik olarak bu listeye eklenir.
- Blacklist uygulanarak `Session`, `LogEntry` gibi sistem tabloları hariç bırakıldı.

### 🔐 Kullanıcı Yetki Sistemi

- Django `auth.User` modeline entegre edildi.
- Yetkilendirme, soft delete, Collector ilişkisi, role-based sistem, erişim kontrolü gibi yapılar kurdum.
- Her kullanıcıya **UserPermission** modeli ile tablo bazlı yetkiler tanımlandı:
  - Görüntüleme (can_view_tables)
  - Kayıt Ekleme (can_add_tables)
  - Silme Yetkisi (deletion_permission: hayır / evet / yönetici onayıyla)
- Backend kısmında yetkilendirmeleri otomatik kontrol etmek için botanik_core>utils altında permissionh.py dosyası oluşturdum. Önyüz(FrontEnd) kısmında da aynı kontrolü hme nav(menü) kısmında kontroller ettirdim hem de kayıt ekleme silme ve düzenleme kısmında. Kullanıcın elinde ilgili URL olsa bile yetkisi yoksa ana sayfaya yönlendirip yetkiniz yok hatası verdirdim.
  - Kullanıcı yetkileri tablosunda ki giriş yapan kullanıcıların yetkilerini bu fonksiyonlar ile kontrol ettim. has_permission_to_view (Görebileceği Tablolar), has_permission_to_add(Kayıte Ekleyebileceği ve Düzenleyebileceği Tablolar), has_delete_permission(Silme Yetkisi var mı yok mu?), has_delete_approval_required(Admin Onaylı Silme Yetkisi mi Mevcut?)
- Giriş yaptıktan sonra kullanıcı yetkilerine göre sadece izin verilen tablolar görüntülenebilir ve bu tablolar üzerinde düzenle, ekleme ve silme yapılabilir.
  - Bu yüzden proje ilk başta ayağa kaldırılmadan önce "python manage.py createsuperuser" ile süper kullanıcı oluşturuyoruz. Süper Kullanıcı olduğu için her şeye yetkisi var. Super Admine giriş yapıp yeni kullanıcı oluşturup yetki atanması gerekiyor normal kullanıcıların yetkisini test edebilmek için.
- Kullanıcılara yetki tanımlama işlemi ister süperadmin üzerinden ister normal site üzerinden gerçekleştirilebilir. eğer giriş yapan kullanıcının admin veya süperadmin yetkisi var ise.

- Grup bazlı yetkilendirme için `UserGroup` modeli tanımlandı.

### ❌ Soft Delete (Pasifleştirme)

- Silme işlemleri doğrudan veritabanından silme değil, `is_active=False` olarak pasifleştirme ile yapılır.
- Bu sayede verilerin geçmişi korunur.
- Silme işlemleri sistemde "pasif hale getirme (soft delete)" ile yapılır, fiziksel silme yoktur.

### 🧩 Account Uygulaması

- Giriş, çıkış, kayıt işlemleri ayrı bir uygulamada yönetilir.
- Yetkisi olmayan kullanıcılar mesajla ana sayfaya yönlendirilir.
- - Kullanıcı Kayıt Olma, Giriş Yapma ve Giriş yaptıysa şifresini değiştirme geliştirmeleri tamamlandı.

### 📒 Collector (Toplayıcılar)

- Kayıt yapan kişiler bu modelde tutulur.
- Sisteme giriş yapan kullanıcı, ilk kez kayıt yaparsa Collector kaydı otomatik oluşturulur.
- Admin panel üzerinden manuel ekleme de yapılabilir.

### 🔢 Accession Record

- Bitki kayıtları accession number ile tutulur (örnek: 2025-00015).
- Eğer Accession Number kayıt esnasında manuel olarak girilmez ise bu alan otomatik olarak yıl + sıra numarası ile oluşturulur (2025-00001 sonraki kayıtta 2025-00002 gibi).
- Kullanıcı numara girdiyse çakışma kontrolü yapılır.

---

## 🚧 Yetiştirilemeyen / Planlanan Özellikler

### 🧬 Bilimsel İsim (Taxon Name) Doğrulaması

- Herbaryum kayıtlarında girilen taksonomik isimler dış veritabanlarıyla doğrulanacak.

🔗 **Planlanan kaynaklar:**
- GBIF (www.gbif.org)
- World Flora Online (www.worldfloraonline.org)
- Tropicos (www.tropicos.org)
- Catalogue of Life (www.catalogueoflife.org)

### 📊 Raporlama & Sorgulama

- Yetkili kullanıcıların Excel/PDF çıktısı alabileceği sorgu sayfaları planlandı.

### 🧾 Kayıt Versiyonlama & Loglama

- Kim, ne zaman, hangi değişikliği yaptı bilgisinin tutulması (audit trail).

### 📱 Mobil Uyum & Toplu Veri Girişi

- Gönüllüler için mobil uyumlu arayüz.
- Excel/CSV ile toplu kayıt yükleme desteği.
