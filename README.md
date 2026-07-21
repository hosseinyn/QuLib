<div align="center">

# QuLib | کولیب

### شبکه اجتماعی و پلتفرم هوشمند نمونه سوال و کتاب‌ های کمک درسی مبتنی بر **AI**

<br>

<img src="https://skillicons.dev/icons?i=python,django,sqlite,postgresql,tailwindcss,js,html,css,git,github,docker,redis,elasticsearch,nginx" />

<br><br>

<img src="https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white" />
<img src="https://img.shields.io/badge/Django-6.x-092E20?logo=django&logoColor=white" />
<img src="https://img.shields.io/badge/SQLite-003B57?logo=sqlite&logoColor=white" />
<img src="https://img.shields.io/badge/AI-OpenRouter-8A2BE2" />
<img src="https://img.shields.io/badge/GPT--OSS-120B-74AA9C?logo=openai&logoColor=white" />
<img src="https://img.shields.io/badge/Status-MVP-success" />

</div>


## 📖 درباره پروژه

**کولیب** یک پلتفرم آموزشی مبتنی بر هوش مصنوعی است که دانش‌ آموزان، معلمان و نوجوانان میتوانند در آن:

- کتاب‌ های درسی را مشاهده و دانلود کنند.
- نمونه‌ سوال‌ های آموزشی را جستجو کنند.
- برای کتاب‌ ها و سوالات نظر ثبت کنند.
- به محتوای آموزشی امتیاز دهند.
- از قابلیت‌ های هوش مصنوعی برای تحلیل، تولید و حل سوالات استفاده کنند.


# ✨ قابلیت ها

- 🔐 سیستم احراز هویت
- 👤 پروفایل کاربر
- 📚 کتابخانه کتاب های کمک درسی
- ❓ بانک نمونه سوال
- 🤖 دستیار هوش مصنوعی شخصی
- 🧠 هوش مصنوعی آزمون ساز
- ✅ حل سوال و ساخت پاسخنامه با هوش مصنوعی
- 👁 پردازش تصویر و استخراج متن
- 📄 پردازش PDF
- 🎯 سیستم پیشنهادگر
- ❤️ سیستم لایک و کامنت و تعامل
- ⭐ سیستم امتیاز دهی منابع
- 🛠 پنل ادمین
- 🏆 لیدربرد و جدول دانش آموزان برتر
- 📑 تبدیل نمونه سوالات از پی دی اف به ورد
- 🎖 بازی وار سازی و نشان در پروفایل کاربر
- 📰 خبرنامه
- 📱 PWA برای موبایل
- 🛜 کامند مدیریت Custom Management Commands
- 🪪 لاگ فعالیت ها / لاگین ها
- 🧪 تست پذیری بخش های اصلی
- 🔍 جستجوی هوشمند (Elasticsearch)
- 🗄️ ذخیره سازی در Object Storage


# 🚀 دسترسی سریع (در نسخه ارسالی خوارزمی)

برای سهولت بررسی پروژه، یک دیتابیس نمونه همراه پروژه قرار گرفته است.

```text
Username : admin
Password : admin
```

همچنین فایل (در نسخه ارسالی خوارزمی)

```text
.env.local
و
.env.production
```

شامل نمونه‌ای از متغیرهای محیطی مورد نیاز است.


# 💻 سیستم مورد نیاز

## حداقل

| ابزار | مورد نیاز |
| :-------- | :---------- |
| Python | 3.12+ |
| Docker | اختیاری |
| CPU | Intel Gen 8+ / Ryzen 3000+ |
| GPU | اختیاری |

## سرویس های مورد نیاز

- OpenRouter API Key
- SMTP Server (Mailpit for local development)

# 📥 دریافت پروژه

ابتدا پروژه را دریافت کرده و وارد پوشه آن شوید.

```bash
git clone https://github.com/hosseinyn/QuLib.git

cd QuLib
```

در صورتی که از نسخه ارسالی خوارزمی استفاده می‌کنید، فایل ZIP را استخراج کرده و وارد پوشه پروژه شوید.


# 🐳 نصب و اجرای پروژه با Docker (پیشنهادی)

### 1. اگر Docker روی سیستم شما نصب نیست، می‌توانید از راهنماهای رسمی زیر استفاده کنید:

- 🐧 Linux (Ubuntu)
  https://docs.docker.com/engine/install/ubuntu/

- 🪟 Windows
  https://docs.docker.com/desktop/setup/install/windows-install/

### 2. تنظیم متغیر های محیطی

> **Windows**

```bash
copy .env.example .env
```

> **Linux**

```bash
cp .env.example .env
```

برای نصب با داکر، حتما مطمئن شوید مواردی که تحت عنوان 
Docker 
نشانه گذاری شده اند فعال باشند و مواردی که تحت عنوان
Local dev
نشانه گذاری شده اند کامنت شده باشند


### 3. اجرای کولیب با داکر

```bash
docker compose -f docker-compose.dev.yml up --build

و برای اجرا های بعدی

docker compose -f docker-compose.dev.yml up
```

### 4. ایندکس Elasticsearch

```bash
docker exec -it qulib_django python manage.py search_index --rebuild -f 
```

### 5. ساخت اکانت ادمین

```bash
docker exec -it qulib_django python manage.py createsuperuser
```

#### برای اجرای کولیب با داکر در محیط پروداکشن، فایل DEPLOYMENT.md را مطالعه کنید



# ⚙ نصب پروژه (بدون داکر)

## 1. ساخت محیط مجازی

> **Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

> **Linux**

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 2. نصب نیازمندی ها

```bash
pip install -r requirements.txt
```

یا

```bash
pip install uv

uv pip sync requirements.txt
```

---

## 3. پیکربندی متغیر های محیطی

> **Windows**

```bash
copy .env.example .env
```

> **Linux**

```bash
cp .env.example .env
```

برای نصب بدون داکر، حتما مطمئن شوید مواردی که تحت عنوان 
Docker 
نشانه گذاری شده اند کامنت باشند و مواردی که تحت عنوان
Local dev 
نشانه گذاری شده اند کامنت نباشند


## 4. دیتابیس و فایل های استاتیک

در صورت استفاده از دیتابیس نمونه نیازی به اجرای مراحل زیر نیست.

```bash
python manage.py migrate

python manage.py createsuperuser

python manage.py collectstatic
```

## 5. اجرا

```bash
python manage.py runserver
یا
python3 manage.py runserver
```

## تداخل django ninja و کتابخانه ninja
در صورتی که به ارور تداخل کتابخانه ninja و django ninja برخورد کردید، دستور زیر را اجرا کنید : 

```bash
pip uninstall -y ninja django-ninja
pip install django-ninja
```


# 🧠 ارائه دهنده هوش مصنوعی

🌐 [openrouter.ai](https://openrouter.ai/ "openrouter.ai")

کولیب از این سرویس برای دریافت API رایگان مدل های زبانی بزرگ استفاده میکند

برای دریافت کلید API و تنظیم آن در متغیر های محیطی، احتیاج به ثبت نام در این سایت دارید.

⚠️ نکته : در برخی مواقع ممکن است OpenRouter با آی پی ایران کار نکند. در صورت دریافت ارور 403، از ابزار های تغییر آی پی استفاده کنید


# 📧 SMTP

برای قابلیت‌هایی مانند:

- بازیابی رمز عبور
- ارسال ایمیل

می‌توانید در محیط توسعه از

**Mailpit**

استفاده کنید.

نسخه ویندوز در پوشه

```text
softwares/
```

قرار گرفته است.

# 🤖 نیازمندی های هوش مصنوعی

در صورت بروز خطا هنگام نصب کتابخانه ‌های هوش مصنوعی، فایل

```text
softwares/VC_redist.x64.exe
```

را نصب کنید.

# 🗄️ Redis (بدون داکر)
کولیب برای کش کردن و انتقال پیام ها نیاز به ردیس دارد.

در لینوکس : 
```bash
sudo apt install redis
redis-server
```

در ویندوز :
```batch
cd softwares
cd redis
redis-server
```

# 🛠️ دستورات مدیریتی


| Command | توضیحات |
|---------|---------|
| `python manage.py clear_admin_logs` | پاکسازی لاگ های پنل مدیریت Django برای کاهش حجم دیتابیس و حذف سوابق قدیمی. |
| `python manage.py reset_logs` | حذف تمامی لاگ های ثبت شده مربوط به فعالیت کاربران در سیستم. |
| `python manage.py truncate_axes` | پاکسازی اطلاعات مربوط به تلاش های ناموفق ورود (django-axes) و ریست محدودیت های امنیتی ورود. |
| `python manage.py reset_scores` | بازنشانی امتیاز تمامی کاربران و محاسبات مربوط به سیستم امتیازدهی و لیدربرد. |

# 💉 مستندات تست ها
تمامی مستندات و اطلاعات مورد نیاز برای تست خودکار پروژه در فایل
TESTING.md
قرار گرفته است


# 📂 مستندات / تجاری سازی (در نسخه ارسالی خوارزمی)

مستندات تکمیلی پروژه در پوشه

```text
مستندات/
تجاری سازی/
مقیاس پذیری/
بلاکچین/
الگوریتم ها/
اسکرام/
```

قرار دارند.

- 🗺 نقشه سفر مشتری / پروژه
- 🚀 سند استراتژی ورود به بازار
- 🎯 سند چشم انداز محصول
- 📄 شناسنامه اثر
- 📊 دیاگرام دیتابیس
- 📺 ارائه پاورپوینت
- 🎥 ویدیو ارائه
- ⚠️ سند SWOT
- 💵 سند Lean Startup Canvas
- 👥 گانت چارت برای اجایل و اسکرام
- 🏢 تیم استارتاپی اجایل
- 🪙 سند نقشه ورود کولیب به بلاکچین
---
- فلوچارت الگوریتم پردازش تصویر
- فلوچارت الگوریتم جستجو
- فلوچارت الگوریتم ردیابی رفتار کاربر
- فلوچارت سیستم پیشنهادگر

# 📌 نقشه راه فنی کولیب

 برنامه توسعه و بهبود زیرساخت پروژه در نسخه های آینده

- [] مهاجرت از Redis به RabbitMQ برای صف بندی Task های غیرهمزمان در مقیاس بالا
- [ ] اتصال پروژه به Sentry برای مانیتورینگ، ردیابی و گزارش خودکار خطاها
- [ ] پیاده سازی Replication برای PostgreSQL
- [ ] پیاده سازی Replication برای Redis
- [ ] پیاده سازی Replication برای Object Storage (MinIO)
- [ ] کانفیگ Kubernetes برای استقرار و Orchestration در مقیاس بالا
- [ ] پیاده سازی ELK Stack (Elasticsearch + Logstash + Kibana) برای مدیریت و تحلیل لاگ ها


# 🙂 توسعه دهنده

**حسین یادگارنیانائینی**

### GitHub

https://github.com/hosseinyn

### LinkedIn

https://www.linkedin.com/in/hossein-yadegarnia-1b3675392

---

<div align="center">

Made with ❤️ by <strong>Hossein Yadegarnia</strong> · 1405

</div>
