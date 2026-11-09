import os, json
from openai import OpenAI

# --- كنقراو المفتاح من ملف .env بيدينا! بلا dotenv! ---
def load_env():
    if os.path.exists(".env"):
        with open(".env", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and "=" in line and not line.startswith("#"):
                    key, value = line.split("=", 1)
                    os.environ[key.strip()] = value.strip().strip('"').strip("'")

load_env()

# دابا المفتاح كاين ف os.environ!
api_key = os.environ.get("GROQ_API_KEY")
print(f"لقيت المفتاح؟ {'آه!' if api_key else 'لا! شوف ملف .env'}")

client = OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1",
    timeout=30.0
)

FILE = "memory.json"

def load_memory():
    if os.path.exists(FILE):
        with open(FILE, encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_memory(mem):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(mem, f, ensure_ascii=False)

mem = load_memory()

SYSTEM = f"""أنت الأستاذ ديالي، معلم صبور وودود. جاوب بالدارجة المغربية البسيطة.
معلومات عن التلميذ: {mem}"""

history = []
print("أهلاً! أنا الأستاذ ديالي!")

if "user_name" in mem:
    print(f"أهلاً رجعتي {mem['user_name']}! توحشناك! 😊")

while True:
    user = input("أنت: ")
    if user.strip().lower() in ("exit", "quit"):
        print("بسلامة!")
        break
    
    history.append({"role": "user", "content": user})
    
    if "سميتي" in user:
        name = user.split()[-1]
        mem["user_name"] = name
        save_memory(mem)
        print(f"(حفظت سميتك: {name})")
    
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        max_tokens=500,
        messages=[
            {"role": "system", "content": SYSTEM},
            *history
        ]
    )
    
    answer = response.choices[0].message.content
    history.append({"role": "assistant", "content": answer})
    print(f"الأستاذ ديالي: {answer}\n")
