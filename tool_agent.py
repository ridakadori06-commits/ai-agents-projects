# tool_agent.py
# مشروع 3: وكيل الأدوات - النسخة النهائية مع count_words

import os
import json
from groq import Groq

def get_api_key():
    with open(".env", "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("GROQ_API_KEY="):
                return line.strip().split("=", 1)[1]
    return None

client = Groq(api_key=get_api_key())

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

def count_words(filename):
    try:
        path = os.path.join("notes", filename)
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
            words = text.split()
            return f"عدد الكلمات في ملف {filename} هو {len(words)} كلمة. النص هو: {text}"
    except Exception as e:
        return f"لم أجد الملف: {e}"

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "استخدمها لحساب أي عملية رياضية مثل الجمع والطرح والضرب والقسمة",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string", "description": "العملية الرياضية مثل 45 + 67"}
                },
                "required": ["expression"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "استخدمها لقراءة ملف من مجلد notes",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {"type": "string", "description": "اسم الملف مثل company.txt"}
                },
                "required": ["filename"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "count_words",
            "description": "استخدمها لحساب عدد الكلمات في ملف من مجلد notes",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {"type": "string", "description": "اسم الملف مثل company.txt"}
                },
                "required": ["filename"]
            }
        }
    }
]

def run_tool(name, args):
    if name == "calculator":
        return calculator(args.get("expression", ""))
    elif name == "read_file":
        return read_file(args.get("filename", ""))
    elif name == "count_words":
        return count_words(args.get("filename", ""))
    else:
        return "أداة غير موجودة"

def ask_agent(user_question):
    messages = [
        {"role": "system", "content": "أنت وكيل أدوات ذكي. استخدم الأدوات عندما تحتاج إليها. لا تخمن الأرقام."},
        {"role": "user", "content": user_question}
    ]

    for step in range(5):
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=messages,
            tools=TOOLS,
            tool_choice="auto"
        )

        message = response.choices[0].message

        if not message.tool_calls:
            return message.content

        messages.append(message)

        for tool_call in message.tool_calls:
            func_name = tool_call.function.name
            func_args = json.loads(tool_call.function.arguments)
            print(f"--> الوكيل يستخدم الأداة: {func_name} مع {func_args}")
            result = run_tool(func_name, func_args)
            print(f"--> نتيجة الأداة: {result}")
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result
            })

    return "وصل الوكيل إلى الحد الأقصى من الخطوات"

if __name__ == "__main__":
    print("=== تجربة 1: حساب ===")
    print(ask_agent("كم يساوي 45 + 67 ؟"))
    print("\n=== تجربة 2: قراءة ملف ===")
    print(ask_agent("ما هو سعر المنتج في ملف company.txt ؟"))
    print("\n=== تجربة 3: حساب مع ملف ===")
    print(ask_agent("اقرأ سعر المنتج من company.txt ثم احسب السعر مع ضريبة 20%"))
    print("\n=== تجربة 4: حساب عدد الكلمات ===")
    print(ask_agent("كم عدد الكلمات في ملف company.txt ؟"))
