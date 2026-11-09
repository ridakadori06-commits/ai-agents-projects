# AI Agents Projects | مشاريع وكلاء الذكاء الاصطناعي

> 4 Projects I built while learning Agentic AI Engineering with Python & Groq.
> 4 مشاريع بنيتهم وأنا كنتعلم Agentic AI Engineering بـ Python و Groq.

---

## 🇬🇧 English

### 1. Chat App - `chat3.py`
A chat that answers in Moroccan Darija and remembers your name even after you close it, using `memory.json`.

### 2. RAG App - `rag.py`
Reads your files from `notes/` folder and answers ONLY from them. If it doesn't find the answer, it says "I don't know".

### 3. Tool Agent - `tool_agent.py`
An agent that uses 3 tools:
- `calculator`: Math
- `read_file`: Read a file
- `count_words`: Count words in a file
It can chain 2 tools: Read price then calculate tax `100 * 1.20 = 120`.

### 4. Harness Agent - `harness_agent.py`
A safe agent with Harness protection:
- **Retry:** If it fails, it tries again 3 times
- **Logging:** Logs everything in `harness.log`
- **Human-in-the-loop:** Asks human before any dangerous action like `send_email` and `delete_file`

## Tech Stack
Python - Groq API (`openai/gpt-oss-20b`) - Function Calling

## How to Run
1. Put your key in `.env`: `GROQ_API_KEY=...`
2. Run any project: `python harness_agent.py`

---

## 🇲🇦 العربية

### 1. شات - `chat3.py`
شات يجاوب بالدارجة ويتذكر اسمك حتى بعد ما تخرج، باستعمال `memory.json`

### 2. RAG - `rag.py`
يقرا ملفاتك من مجلد `notes/` ويجاوب غير منهم. إلا ما لقاش الجواب، كيقول "لا أعرف"

### 3. وكيل الأدوات - `tool_agent.py`
وكيل يستعمل 3 أدوات:
- `calculator`: حساب
- `read_file`: قراءة ملف
- `count_words`: حساب عدد الكلمات
يقدر يدير أداتين متتاليتين: يقرا السعر ثم يحسب الضريبة `100 * 1.20 = 120`

### 4. وكيل آمن Harness - `harness_agent.py`
وكيل مع حماية Harness:
- **Retry:** إلا فشل، يعاود المحاولة 3 مرات
- **Logging:** يسجل كلشي فـ `harness.log`
- **Human-in-the-loop:** يسول الإنسان قبل أي عمل خطير مثل `send_email` و `delete_file`

## التقنيات
Python - Groq API (`openai/gpt-oss-20b`) - Function Calling

## كيف تشغل؟
1. دير المفتاح ديالك فـ `.env`: `GROQ_API_KEY=...`
2. شغل أي مشروع: `python harness_agent.py`

---

Built by Rida | بناه رضا - Morocco 🇲🇦
