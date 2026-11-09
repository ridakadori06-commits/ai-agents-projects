import os, glob
from openai import OpenAI

# كنقراو المفتاح من .env بيدينا (بلا dotenv)
def load_env():
    if os.path.exists(".env"):
        with open(".env", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and "=" in line and not line.startswith("#"):
                    k, v = line.split("=", 1)
                    os.environ[k.strip()] = v.strip().strip('"').strip("'")
load_env()

client = OpenAI(
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
    timeout=30.0
)

# 1. كنقراو كل الملفات ف notes/
chunks = []
sources = []
for path in glob.glob("notes/*.txt"):
    with open(path, encoding="utf-8") as f:
        for para in f.read().split("\n\n"):
            if para.strip():
                chunks.append(para.strip())
                sources.append(path)

print(f"لقيت {len(chunks)} فقرة فالملاحظات!")

def ask(question):
    # 2. البحث: قلب على الفقرة اللي فيها كلمات مشتركة!
    best_chunk = None
    best_source = None
    best_score = 0
    
    q_words = set(question.lower().split())
    for chunk, src in zip(chunks, sources):
        c_words = set(chunk.lower().split())
        score = len(q_words & c_words)  # شحال من كلمة مشتركة؟
        if score > best_score:
            best_score = score
            best_chunk = chunk
            best_source = src
    
    # 3. إلا ما لقينا والو، قول لا أعرف!
    if best_score == 0 or not best_chunk:
        return "لا أعرف!", "لا يوجد مصدر"
    
    # 4. كنسيفطو الفقرة + السؤال للنموذج!
    prompt = f"""أجب من السياق فقط. إلا كان الجواب غير موجود، قول لا أعرف.
السياق: {best_chunk}
السؤال: {question}"""
    
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        max_tokens=400,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content, best_source

# جرب!
while True:
    q = input("\nسولني على ملاحظاتك (كتب exit باش تخرج): ")
    if q.strip().lower() == "exit":
        break
    answer, src = ask(q)
    print(f"\nالجواب: {answer}")
    print(f"المصدر: {src}")
