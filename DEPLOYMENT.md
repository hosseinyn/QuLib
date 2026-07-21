# استقرار کولیب در محیط پروداکشن با داکر

این راهنما نحوه دیپلوی نسخه پروداکشن پروژه کولیب را روی سرور لینوکس توضیح میدهد.

کولیب به صورت کامل با **Docker Compose** اجرا میشود و تمامی سرویس های مورد نیاز به جز **Nginx** را به صورت خودکار راه اندازی میکند.


# 📋 پیش نیازها

قبل از شروع، موارد زیر باید روی سرور نصب باشند.

* Docker Engine
* Docker Compose Plugin
* Git
* Nginx (خارج از Docker)

راهنمای نصب Docker:

🐧 Linux (Ubuntu)

https://docs.docker.com/engine/install/ubuntu/


# 🧩 سرویس های مورد نیاز

در هنگام اجرای فایل `docker-compose.yml` سرویس های زیر به صورت خودکار اجرا خواهند شد.

|  سرویس ها               
| -------------------- 
| Django + Daphne
| Celery Worker
| PostgreSQL
| Redis
| Elasticsearch
MinIO Object Storage
Mailpit

**Redis** و **Elasticsearch** برای اجرای صحیح پروژه اجباری هستند.

---

# 📂 دریافت پروژه

```bash
git clone https://github.com/hosseinyn/QuLib.git

cd QuLib
```

یا نسخه ارسالی خوارزمی را استخراج کنید.

# ⚙ تنظیم متغیرهای محیطی

ابتدا فایل تنظیمات را ایجاد کنید.

```bash
cp .env.example .env
```

سپس فایل `.env` را متناسب با سرور خود ویرایش کنید.

مهمترین متغیرهایی که باید بررسی شوند:

* SECRET_KEY
* DEBUG=False
* ALLOWED_HOSTS
* DOMAIN
* OPENROUTER_API_KEY
* POSTGRES_PASSWORD
* REDIS_PASSWORD
* MINIO_ROOT_PASSWORD

در محیط Docker، تنظیمات بخش های **Docker** باید فعال باشند و بخش های **Local dev** کامنت باشند.


# 🐳 ساخت و اجرای پروژه

ساخت ایمیج:

```bash
docker compose build
```

اجرای پروژه:

```bash
docker compose up -d
```

یا به صورت همزمان:

```bash
docker compose up --build -d
```


# 📚 ساخت Elasticsearch Index

پس از اولین اجرا، ایندکس های Elasticsearch را ایجاد کنید.

```bash
docker exec qulib_django python manage.py search_index --rebuild -f
```

این دستور فقط یکبار بعد از اولین استقرار لازم است.

در صورت تغییر ساختار Document های Elasticsearch نیز باید مجددا اجرا شود.


# 👤 ساخت Superuser

برای ورود به پنل مدیریت Django:

```bash
docker exec -it qulib_django python manage.py createsuperuser
```


# 🌐 تنظیم Nginx

Nginx داخل Docker اجرا نمیشود.

یک فایل نمونه با نام

```text
nginx.conf
```

در روت پروژه قرار گرفته است.

کافی است آن را متناسب با دامنه خود ویرایش کرده و در تنظیمات Nginx سرور قرار دهید.

نمونه:

* server_name
* SSL
* Certificate
* مسیر فایل های لاگ

همگی باید متناسب با سرور شما تنظیم شوند.

پس از اعمال تنظیمات:

```bash
sudo nginx -t
```

```bash
sudo systemctl reload nginx
```

# 🔒 HTTPS

برای فعال سازی HTTPS میتوانید از Let's Encrypt استفاده کنید.

نمونه:

```bash
sudo certbot --nginx
```

# 📦 Object Storage

کولیب برای ذخیره فایل ها از **MinIO** استفاده میکند.

پس از اجرای Docker، پنل مدیریت تحت وب MinIO در آدرس زیر در دسترس خواهد بود.
در محیط پروداکشن، از باز یا بسته بودن این پورت در فایروال سرور مطلع شوید

```text
http://SERVER_IP:9001
```

نام کاربری و رمز عبور از فایل `.env` خوانده میشوند.

```text
MINIO_ROOT_USER

MINIO_ROOT_PASSWORD
```


# 📧 Mailpit

Mailpit فقط برای محیط توسعه در نظر گرفته شده است.

رابط وب:

```text
http://SERVER_IP:8025
```

در محیط پروداکشن پیشنهاد میشود از SMTP واقعی استفاده شود.

# 🩺 بررسی وضعیت سرویس ها

نمایش وضعیت:

```bash
docker compose ps
```

مشاهده لاگ ها:

```bash
docker compose logs
```

لاگ لحظه ای:

```bash
docker compose logs -f
```

# 🔄 بروزرسانی پروژه

دریافت آخرین تغییرات:

```bash
git pull
```

ساخت مجدد:

```bash
docker compose build
```

اجرای نسخه جدید:

```bash
docker compose up -d
```

در صورت تغییر مدل های دیتابیس، Migration ها به صورت خودکار هنگام اجرای کانتینر Django اعمال خواهند شد.

# 🧹 توقف پروژه

توقف سرویس ها:

```bash
docker compose stop
```

خاموش کردن کامل:

```bash
docker compose down
```

حذف Volume ها:

```bash
docker compose down -v
```

⚠️ دستور آخر اطلاعات PostgreSQL، Redis، Elasticsearch و MinIO را حذف میکند.

# 📁 ساختار استقرار

```text
Server
│
├── Nginx
│
├── Docker
│   ├── Django (Daphne)
│   ├── Celery
│   ├── PostgreSQL
│   ├── Redis
│   ├── Elasticsearch
│   ├── MinIO
│   └── Mailpit
│
└── Internet
```

# 🔒 بررسی نهایی

قبل از قرار دادن پروژه در دسترس کاربران، موارد زیر را بررسی کنید.

* DEBUG=False
* SECRET_KEY تغییر داده شده باشد.
* ALLOWED_HOSTS تنظیم شده باشد.
* DOMAIN صحیح باشد.
* SSL فعال باشد.
* Elasticsearch Index ساخته شده باشد.
* Superuser ایجاد شده باشد.
* Nginx به درستی تنظیم شده باشد.
* OpenRouter API Key معتبر باشد.
* رمزهای PostgreSQL، Redis و MinIO تغییر داده شده باشند.
* بکاپ گیری از Volume های Docker انجام شود.

پس از انجام مراحل بالا، پروژه آماده استفاده در محیط پروداکشن خواهد بود.
