# GymScheduler Bot 🏋️‍♂️🤖

Hello! This is a simple and unique Telegram Bot built to create custom gym workout schedules and automatically embed them into personalized images for users. 

The project splits the work between two languages: **Python** handles the Telegram chat/bot interface, and **Go (Golang)** works in the background to handle the heavy image processing with maximum speed.



## English Documentation

### 👋 A Note from the Developer (Read This First!)
Let's be completely honest here: if you dive into the code, you will notice some rigidity. The number of workout days is fixed (6 days), the number of exercises is limited (7 per day), and the text coordinates on the images are hardcoded. On top of that, you will see some long conditional structures (`if/else`) inside the Python code.

**I apologize for this rigidity, but it was done on purpose.** This straightforward design ensures absolute stability and speed for this version, keeping it predictable with zero hidden crashes.

The best part? **You don't need to be a senior engineer to change this!** The code is so simple and linear that anyone with basic programming knowledge—and a slightly smart AI assistant—can easily change the number of days, modify the exercises, adjust the text coordinates, or even completely translate the bot's interface into English or any other language in a few minutes.



### 🛠️ How it Works
Instead of making Python do everything and slowing down the bot, the system is split into two parts:
1. **The Interface Layer (Python):** Manages the Telegram API, checks admin IDs for permission, and guides the user step-by-step to build their schedule. Once finished, it saves the data into `requests.json`.
2. **The Processing Layer (Go):** Runs silently in the background, constantly watching the `requests.json` file. The moment a user finishes their setup, Go wakes up, processes the image, renders the Arabic text perfectly, and saves the final PNG card instantly.



### ✨ Features
- **Secure Access:** Users are authenticated and allowed in strictly using their Telegram IDs.
- **Predictable Stability:** Simple line-by-line code execution means the chance of unexpected crashes is almost zero.
- **Flawless Arabic Text:** Texts drawn on images are fully connected and beautifully shaped without any broken or reversed lettering issues.



### 🚀 Step-by-Step Download and Setup Guide

#### Step 1: System Requirements (Prerequisites)
Before downloading, ensure you have both programming languages installed on your machine:
- **Python:** Version **3.10 or higher** must be installed.
- **Go (Golang):** Must be installed. *(The specific Go version required for this project is already mentioned inside the `go.mod` file)*.

#### Step 2: Download and Extract the Repository
1. Click on the green **"Code"** button at the top right of this GitHub page.
2. Select **"Download ZIP"** from the dropdown menu.
3. Once the download is finished, extract the ZIP file into a dedicated folder on your computer.
4. Make sure that all these essential files are together in that same folder:
   - `GymScheduler.py` (The Python interface script)
   - `GymScheduler.go` (The Go image processor script)
   - `go.mod` and `go.sum` (The automatic Go configuration files)
   - Your background image templates and required fonts.

#### Step 3: Configure and Run the Telegram Bot (Python)
1. Open your computer's **Command Prompt (cmd)** or **Terminal**.
2. Navigate to your project folder using the `cd` command (e.g., `cd path/to/your/folder`).
3. Install the required Python packages by running:
      pip install python-telegram-bot requests



4. Start the bot interface script:
python GymScheduler.py





*(Note: Keep this terminal window open; closing it will take the bot offline).*

#### Step 4: Run the Image Processor Microservice (Go)

1. Open a **completely new and separate terminal/cmd window**.
2. Navigate to the exact same project folder using `cd`.
3. You do not need to download or install any Go packages manually; since `go.mod` and `go.sum` are already included, Go will automatically fetch everything it needs. Just run:
go run GymScheduler.go





Now both environments are successfully running side-by-side, sharing information and processing your schedules seamlessly!



## جدولة التمارين  🏋️‍♂️🤖

مرحباً! هذا بوت تيليجرام (Telegram Bot) بسيط وفريد من نوعه، تَمّ بناؤه لإنشاء جداول تمارين رياضية مخصصة، ودمجها تلقائياً داخل صور شخصية للمستخدمين. 

ينقسم العمل في هذا المشروع بين لغتين: تتولى لغة **بايثون (Python)** إدارة واجهة البوت والمحادثات على تيليجرام، بينما تعمل لغة **جو (Go/Golang)** في الخلفية لمعالجة الصور الثقيلة بأقصى سرعة ممكنة.

### 👋 كلمة من المطور (اقرأني أولاً!)

دعنا نكون صريحين جداً؛ إذا دخلت إلى عمق الكود، ستلاحظ وجود بعض الجمود. عدد الأيام ثابت (6 أيام)، وعدد التمارين محدود (7 تمارين يومياً)، وإحداثيات وأماكن النصوص فوق الصور مكتوبة بأرقام ثابتة (Hardcoded)، بالإضافة إلى وجود شروط طويلة ومكررة في ملف بايثون.

**أنا أعتذر عن هذا الجمود في الكود، ولكن الأمر مقصود.** هذا التصميم المباشر والخطي يضمن لك أعلى درجات الاستقرار والسرعة في هذه النسخة، ويجعل الكود يعمل بشكل متوقع تماماً وبدون أخطاء أو كراشات مفاجئة.

الميزة العظمى هنا: **أنت لا تحتاج إلى خبرة خارقة لتعديل هذا!** بنية الكود واضحة وبسيطة للغاية، وأي شخص يملك أساسيات برمجية بسيطة—ومعه ذكاء اصطناعي ذكي قليلاً—يستطيع بسهولة زيادة عدد الأيام، تغيير عدد التمارين، تعديل أماكن النصوص على الصور، أو حتى تحويل واجهة البوت بالكامل لتدعم أي لغة أخرى (كالانجليزية وغيرها) في دقائق معدودة.



### 🛠️ كيف يعمل النظام؟

بدلاً من جعل لغة بايثون تقوم بكل شيء وتتسبب في بطء استجابة البوت، قمت بتقسيم الشغل بذكاء بين لغتين:

1. **طبقة الواجهة (Python):** تتولى التعامل مع تليجرام، والتحقق من صلاحيات المشرفين عبر الـ ID الخاص بهم، وتأخذ بيانات الجدول من المستخدم خطوة بخطوة، ثم تحفظها في ملف بسيط اسمه `requests.json`.
2. **طبقة المعالجة (Go):** سكربت سريع جداً يعمل في الخلفية ويراقب ملف `requests.json`. بمجرد أن ينتهي المستخدم من كتابة جدول تمرين، يتدخل سكربت Go فوراً ليرسم النصوص العربية بدقة ويصنع بطاقة التمرين النهائية بصيغة PNG بأجزاء من الثانية.



### ✨ مميزات البوت

* **حماية الدخول:** لا يمكن لأي شخص استخدام البوت إلا إذا كان مضافاً برقم الـ ID الخاص به لحماية الخصوصية.
* **استقرار تام:** الكود خطي ومباشر، مما يعني أن فرصة حدوث أخطاء مفاجئة أثناء التشغيل هي صفر تقريباً.
* **دعم حقيقي للعربية:** النصوص تظهر فوق الصور منسقة ومكتوبة بشكل متصل وصحيح تماماً، بدون مشكلة الحروف المتقطعة أو المعكوسة.



### 🚀 خطوات التنزيل والتشغيل بالتفصيل

#### الخطوة 1: متطلبات النظام الأساسية

قبل البدء في تحميل وتشغيل البوت، تأكد من تثبيت لغات البرمجة التالية على جهازك:

* **لغة بايثون (Python):** يجب أن تكون مثبتة بإصدار **3.10 أو أعلى**.
* **لغة جو (Go/Golang):** يجب أن تكون مثبتة على جهازك. *(رقم إصدار لغة Go المطلوب للمشروع مكتوب ومحدد بالفعل داخل ملف `go.mod`)*.

#### الخطوة 2: تحميل وفك ضغط المشروع

1. اضغط على الزر الأخضر المكتوب عليه **"Code"** في أعلى يمين هذه الصفحة على جيت هوب.
2. اختر **"Download ZIP"** من القائمة المنسدلة.
3. بعد اكتمال التحميل، فك ضغط الملف داخل مجلد مخصص على جهازك.
4. تأكد من أن المجلد يحتوي على الملفات الأساسية التالية معاً:
* ملف البوت `GymScheduler.py`
* ملف معالج الصور `GymScheduler.go`
* ملفات إعدادات الجو `go.mod` و `go.sum`
* الصور الخلفية الأساسية والخطوط المطلوبة لعمل الكود.



#### الخطوة 3: إعداد وتشغيل واجهة البوت (Python)

1. افتح التيرمنال (Terminal) أو موجه الأوامر (cmd) الخاص بجهازك.
2. انتقل إلى مجلد المشروع باستخدام أمر `cd` (مثال: `cd path/to/your/folder`).
3. قم بتنصيب الحزم المطلوبة للبايثون عبر تشغيل الأمر التالي:
pip install python-telegram-bot requests




4. قم بتشغيل سكربت البوت الآن:
python GymScheduler.py





*(تنبيه: اترك هذه الشاشة مفتوحة ولا تغلقها لكي يظل البوت يعمل أونلاين).*

#### الخطوة 4: تشغيل معالج الصور الخلفي (Go)

1. افتح **شاشة تيرمنال (Terminal/cmd) جديدة وثانية تماماً**.
2. انتقل بها إلى نفس مجلد المشروع باستخدام أمر `cd`.
3. لن تحتاج لتنصيب أي مكتبات لـ Go يدوياً؛ لأن ملفات الـ `go.mod` و `go.sum` المرفقة ستقوم بسحب كافة المكاتب المطلوبة تلقائياً بمجرد تشغيل المشروع. فقط اكتب الأمر التالي:
go run GymScheduler.go





الآن السكربتان يعملان معاً في نفس الوقت بانسجام تام ويتواصلان عبر ملف الـ JSON بنجاح!



## 📜 License / الرخصة البرمجية

This project is open-source and licensed under the **MIT License** - خذ الكود، عدله، وطوره بالطريقة التي تحبها!



