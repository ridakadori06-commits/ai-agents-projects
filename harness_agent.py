# harness_agent.py
# مشروع 4: وكيل Harness - وكيل آمن وموثوق

import os
import json
import time
from datetime import datetime
from groq import Groq

def get_api_key():
    with open(".env", "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("GROQ_API_KEY="):
                return line.strip().split("=", 1)[1]
    return None

client = Groq(api_key=get_api_key())

# ============ الجزء 1: Logging - الدفتر ============
def log(message):
    """
    يكتب رسالة في ملف harness.log مع الوقت
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {message}\n"
    print(line.strip())
    with open("harness.log", "a", encoding="utf-8") as f:
        f.write(line)

# ============ الجزء 2: الأدوات ============
def calculator(expression):
    try:
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"خطأ في الحساب: {e}"

def read_file(filename):
    try:
        path = os.path.join("notes", filename)
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"لم أجد الملف: {e}"

def send_email(to, subject):
    """
    هذه أداة خطيرة - ترسل إيميلاً
    في الحقيقة، نحن لن نرسل إيميلاً حقيقياً، فقط سنحاكي ذلك
    """
    return f"تم إرسال إيميل إلى {to} بعنوان: {subject}"
def delete_file(filename):
    """
    أداة خطيرة - تحذف ملف
    في الحقيقة، نحن لن نحذف حقيقياً، فقط نحاكي الحذف
    """
    return f"تم حذف الملف: {filename} (محاكاة فقط - لم يتم الحذف الحقيقي)"

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "حساب عملية رياضية",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string", "description": "العملية مثل 45 + 67"}
                },
                "required": ["expression"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "قراءة ملف من مجلد notes",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {"type": "string", "description": "اسم الملف"}
                },
                "required": ["filename"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "send_email",
            "description": "إرسال إيميل إلى عميل. هذا عمل خطير، يجب أن تسأل الإنسان أولاً.",
            "parameters": {
                "type": "object",
                "properties": {
                    "to": {"type": "string", "description": "البريد الإلكتروني للمستقبل"},
                    "subject": {"type": "string", "description": "عنوان الإيميل"}
                },
                "required": ["to", "subject"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_file",
            "description": "حذف ملف من مجلد notes. هذا عمل خطير، يجب أن تسأل الإنسان أولاً.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {"type": "string", "description": "اسم الملف"}
                },
                "required": ["filename"]
            }
        }
    }
]

# الأدوات الخطيرة التي تحتاج موافقة الإنسان
DANGEROUS_TOOLS = ["send_email", "delete_file"]

def run_tool(name, args):
    if name == "calculator":
        return calculator(args.get("expression", ""))
    elif name == "read_file":
        return read_file(args.get("filename", ""))
    elif name == "send_email":
        return send_email(args.get("to", ""), args.get("subject", ""))
    elif name == "delete_file":
        return delete_file(args.get("filename", ""))
    else:
        return "أداة غير موجودة"

# ============ الجزء 3: Retry - إعادة المحاولة ============
def call_llm_with_retry(messages, max_retries=3):
    """
    يحاول الاتصال بالنموذج حتى 3 مرات إذا فشل
    """
    for attempt in range(1, max_retries + 1):
        try:
            log(f"محاولة الاتصال بالنموذج - المحاولة {attempt}")
            response = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=messages,
                tools=TOOLS,
                tool_choice="auto"
            )
            log("تم الاتصال بالنموذج بنجاح")
            return response
        except Exception as e:
            log(f"فشل الاتصال في المحاولة {attempt}: {e}")
            if attempt == max_retries:
                raise e
            log("سأحاول مرة أخرى بعد ثانيتين...")
            time.sleep(2)

# ============ الجزء 4: وكيل Harness ============
def ask_harness_agent(user_question):
    log(f"=== سؤال جديد من المستخدم: {user_question} ===")
    messages = [
       {"role": "system", "content": "أنت وكيل آمن. عندما يطلب منك المستخدم عملاً، استدعِ الأداة المناسبة فوراً ولا تسأله بنفسك. لا تقل 'هل أنت متأكد؟' ولا تطلب تأكيداً. نظام Harness هو الذي سيسأل الإنسان عن الموافقة. مهمتك هي استدعاء الأداة فقط."},
        {"role": "user", "content": user_question}
    ]

    for step in range(5):
        response = call_llm_with_retry(messages)
        message = response.choices[0].message

        if not message.tool_calls:
            log(f"الجواب النهائي: {message.content}")
            return message.content

        messages.append(message)

        for tool_call in message.tool_calls:
            func_name = tool_call.function.name
            func_args = json.loads(tool_call.function.arguments)
            log(f"الوكيل يريد استخدام الأداة: {func_name} مع {func_args}")

            # Human-in-the-loop: إذا كانت الأداة خطيرة، اسأل الإنسان
            if func_name in DANGEROUS_TOOLS:
                log(f"تحذير: {func_name} أداة خطيرة!")
                print(f"\n⚠️ تحذير: الوكيل يريد تنفيذ عمل خطير: {func_name}")
                print(f"التفاصيل: {func_args}")
                approval = input("هل توافق؟ اكتب yes للموافقة أو no للرفض: ")
                if approval.lower() != "yes":
                    log("الإنسان رفض تنفيذ العمل الخطير. توقف الوكيل.")
                    return "تم رفض العمل الخطير من طرف الإنسان. لم يتم التنفيذ."
                log("الإنسان وافق على العمل الخطير.")

            result = run_tool(func_name, func_args)
            log(f"نتيجة الأداة {func_name}: {result}")
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result
            })

    return "وصل الوكيل إلى الحد الأقصى من الخطوات"

if __name__ == "__main__":
    print("=== تجربة 1: عمل آمن - حساب ===")
    print(ask_harness_agent("كم يساوي 20 + 30 ؟"))
    print("\n=== تجربة 2: عمل آمن - قراءة ملف ===")
    print(ask_harness_agent("ما هو سعر المنتج في company.txt ؟"))
    print("\n=== تجربة 3: عمل خطير - إرسال إيميل ===")
    print(ask_harness_agent("أرسل إيميلاً إلى client@example.com بعنوان السعر الجديد"))
    print(ask_harness_agent("احذف ملف company.txt الآن باستخدام أداة delete_file"))
    print(ask_harness_agent("احذف ملف company.txt"))
    print("\n=== انتهى. افتح ملف harness.log لترى الدفتر ===")
