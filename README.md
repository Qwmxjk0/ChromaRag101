# 🌦️ ChromaRag101 – ระบบถาม-ตอบพยากรณ์อากาศด้วย RAG + ChromaDB

**ChromaRag101** เป็นโปรเจกต์ตัวอย่าง Retrieval-Augmented Generation (RAG) ที่ใช้ [ChromaDB](https://docs.trychroma.com/) ในการเก็บข้อมูลพยากรณ์อากาศรายชั่วโมงจาก [กรมอุตุนิยมวิทยา (TMD)](https://data.tmd.go.th) พร้อมระบบถาม-ตอบที่รองรับคำถามด้วยภาษาธรรมชาติ เช่น `"เชียงใหม่อากาศเป็นอย่างไร"` หรือ `"จังหวัด: สุราษฎร์ธานี"`

---

### 🧠 ความสามารถหลัก

- ✅ ดึงข้อมูลจาก TMD API และบันทึกเป็น JSON
- ✅ แปลงข้อมูลให้เป็นเอกสาร vector แล้วเก็บใน ChromaDB
- ✅ ระบบถาม-ตอบที่รองรับ exact match, fuzzy match และ semantic search
- ✅ สื่อสารกับผู้ใช้เป็นภาษาไทย พร้อมระบุคะแนนความเกี่ยวข้อง

---

### 📁 โครงสร้างโปรเจกต์

```bash
ChromaRag101/
├── chroma_db/              # ChromaDB เก็บเวกเตอร์ฝั่ง local
├── data/
│   └── tmd_forecast.json   # ไฟล์ข้อมูลพยากรณ์จาก TMD (หลัง fetch)
├── rag/
│   ├── chroma_store.py     # จัดการ ChromaDB client และ insert ข้อมูล
│   ├── loader.py           # แปลงข้อมูล JSON เป็นเอกสาร
│   ├── qa.py               # ระบบ QA พื้นฐาน
│   └── improved_qa_system.py  # ระบบ QA ขั้นสูง (hybrid + fuzzy)
├── tmd_data/
│   ├── __init__.py
│   └── fetch.py            # ดึงข้อมูลพยากรณ์จาก TMD API
├── .env                    # เก็บ API Key สำหรับใช้งาน TMD API
├── .gitignore              # ไม่รวมไฟล์ที่ไม่จำเป็นเข้า git
├── app.py                  # สคริปต์หลักสำหรับรัน QA
├── requirements.txt        # รายการไลบรารีที่ต้องติดตั้ง
└── README.md               # ไฟล์แนะนำโปรเจกต์นี้
---

```

### 🚀 วิธีใช้งาน
1. ติดตั้งไลบรารี
```bash
pip install -r requirements.txt
```
2. สร้างไฟล์ .env
สร้างไฟล์ชื่อ .env ในไดเรกทอรีหลักของโปรเจกต์และเพิ่ม API Key ของคุณ:

```Code snippet

TMD_DATA_API_KEY=your_token_here
```
🔑 สมัคร API Key ได้ที่: TMD Developer Portal

3. ดึงข้อมูลล่าสุดจาก TMD API
รันสคริปต์เพื่อดึงข้อมูลพยากรณ์อากาศล่าสุด

```bash
python tmd_data/fetch.py
```
4. โหลดข้อมูลและเริ่มระบบถาม-ตอบ (QA)
โหลดข้อมูลเข้าสู่ Vector Database (ChromaDB) และเปิดใช้งานเซิร์ฟเวอร์สำหรับตอบคำถาม

```Bash
python app.py
```
หรือหากต้องการทดสอบระบบ QA ที่ปรับปรุงแล้ว:

```Bash
python rag/improved_qa_system.py
```
💬 ตัวอย่างคำถามที่รองรับ

- เชียงใหม่
- จ.ขอนแก่น
- จังหวัด: นครราชสีมา
- กรุงเทพอากาศเป็นยังไง
- ภูเก็ตอุณหภูมิ


### 🧪 ผลลัพธ์การทดสอบ
ในแต่ละคำถาม ผลลัพธ์จะแสดงข้อมูลต่อไปนี้:
- 🔹 เอกสารตอบกลับ: เนื้อหาข้อมูลพยากรณ์อากาศที่เกี่ยวข้องที่สุด
- 📍 จังหวัดที่ระบบจับได้: ชื่อจังหวัดที่ตรงกับคำถาม
- 📊 คะแนนความใกล้เคียง: ค่า Semantic Distance เพื่อดูความเกี่ยวข้องของผลลัพธ์
- ❌ รายชื่อจังหวัดทั้งหมด: แสดงในกรณีที่ระบบไม่พบผลลัพธ์ที่ตรงกัน

### 📦 Dependencies
โปรเจกต์นี้ใช้ไลบรารีหลักดังนี้ (ดูทั้งหมดได้ใน requirements.txt):

```Plaintext
chromadb
python-dotenv
requests
```
### 🧠 เหมาะสำหรับใคร?
- นักพัฒนา/นักศึกษา ที่ต้องการทดลองสร้างระบบ RAG (Retrieval-Augmented Generation) แบบ offline
- ผู้ที่สนใจเรียนรู้ เกี่ยวกับ Vector Database (เช่น ChromaDB) และการค้นหาด้วย Embedding
- ผู้ที่ต้องการเชื่อมต่อ Chatbot กับข้อมูลที่มีโครงสร้าง (Structured/Semi-structured Data)

### 🔧 การต่อยอดในอนาคต
ChromaRag101 ถูกออกแบบให้สามารถขยายและต่อยอดได้ เช่น:
- 🤖 เชื่อมต่อกับ LLM (เช่น GPT-4, Claude, LLaMA) เพื่อให้ระบบสรุปหรืออธิบายข้อมูลเพิ่มเติม
- 🔗 ใช้งานร่วมกับ LangChain หรือ LlamaIndex เพื่อจัดการ Pipeline แบบ RAG เต็มรูปแบบ
- 💬 สร้าง Chatbot แบบโต้ตอบ สำหรับผู้ใช้งานทั่วไป เช่น ระบบแจ้งเตือนอากาศ
- 🌐 สร้าง API ด้วย FastAPI/Flask หรือ Deploy ด้วย Streamlit/HuggingFace Spaces

### 📄 License
โค้ดนี้จัดทำขึ้นเพื่อการศึกษาเท่านั้น
ข้อมูลพยากรณ์อากาศที่ใช้ในโปรเจกต์นี้ นำมาจาก กรมอุตุนิยมวิทยา (TMD)

### 🙌 ขอบคุณ
- TMD Open API สำหรับการให้บริการข้อมูล
- ChromaDB สำหรับเครื่องมือ Vector Database ที่ยอดเยี่ยม
