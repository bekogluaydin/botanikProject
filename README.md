# Botanik Kayıt Sistemi

Bu proje, herbaryum, tohum bankası ve diğer botanik verilerin yönetimi için geliştirilmiştir.


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

## 🚀 Projeyi Başlatma


### 1. Reposu Klonla
git clone <repo_link>
cd <proje_dizini>


### 2. Sanal Ortam Oluştur ve Aktifleştir

python -m venv .venv
source .venv/bin/activate     # Mac/Linux
.venv\Scripts\activate        # Windows


### 3. Gerekli Paketleri Yükle
pip install -r requirements.txt


### 4. Veritabanı Kurulumu ve Migrasyonlar

python manage.py makemigrations
python manage.py migrate



### 5. Süper Kullanıcı Oluştur

python manage.py createsuperuser


### 6. Geliştirme Sunucusunu Başlat

python manage.py runserver


###  7. Giriş

http://127.0.0.1:8000/account/login/


### 8. Super Admin Giriş (Super User için)

http://127.0.0.1:8000/admin/

---

## ✅ Ek Bilgiler

- Giriş yaptıktan sonra kullanıcı yetkilerine göre sadece izin verilen tablolar görüntülenebilir.
  - Bu yüzden "python manage.py createsuperuser" ile süper kullanıcı oluşturuyoruz. Süper Kullanıcı olduğu için her şeye yetkisi var. Super Admine giriş yapıp yeni kullanıcı oluşturup yetki atanması gerekiyor normal kullanıcıların yetkisini test edebilmek için.
- Silme işlemleri sistemde "pasif hale getirme (soft delete)" ile yapılır, fiziksel silme yoktur.
- Eğer Accession Number kayıt esnasında manuel olarak girilmez ise bu alan otomatik olarak yıl + sıra numarası ile oluşturulur (2025-00001 sonraki kayıtta 2025-00002 gibi).