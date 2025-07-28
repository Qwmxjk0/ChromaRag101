import chromadb
import re
from rag.chroma_store import get_client

client = get_client()
collection = client.get_or_create_collection(name="weather") 

def ask(query):
    print(f"🔍 คำถาม: {query}")
    
    # ปรับปรุง regex ให้จับได้หลายรูปแบบ
    patterns = [
        r"จังหวัด:?\s*([ก-๙]+)",  # จังหวัด: ชลบุรี หรือ จังหวัดชลบุรี
        r"จ\.?\s*([ก-๙]+)",       # จ.ชลบุรี หรือ จ ชลบุรี
        r"([ก-๙]+)"               # ชลบุรี (fallback)
    ]
    
    province = None
    for pattern in patterns:
        match = re.search(pattern, query)
        if match:
            province = match.group(1)
            break
    
    print(f"🏛️ จังหวัดที่ตรวจจับได้: {province}")
    
    # ค้นหาแบบไม่มี filter ก่อน (เพื่อดูว่ามีข้อมูลไหม)
    all_results = collection.query(
        query_texts=[query],
        n_results=10
    )
    print(f"📊 ผลการค้นหาทั้งหมด: {len(all_results['documents'][0])} ผลลัพธ์")
    
    # ถ้าระบุจังหวัด ให้ filter ด้วย
    if province:
        results = collection.query(
            query_texts=[query],
            n_results=3,
            where={"province": province}
        )
        print(f"📊 ผลการค้นหาสำหรับ {province}: {len(results['documents'][0])} ผลลัพธ์")
    else:
        results = all_results
        results['documents'] = [results['documents'][0][:3]]  # เอาแค่ 3 ตัวแรก
    
    if not results["documents"][0]:
        print("❌ ไม่พบข้อมูลที่ตรงกับคำค้นหา")
        
        # แสดงจังหวัดที่มีในระบบ
        all_data = collection.get()
        provinces = set(meta['province'] for meta in all_data['metadatas'])
        print(f"🗺️ จังหวัดที่มีในระบบ: {', '.join(sorted(provinces))}")
        return
    
    print(f"\n✅ พบ {len(results['documents'][0])} ผลลัพธ์:")
    for i, doc in enumerate(results["documents"][0]):
        print(f"🔹 ตอบ {i+1}:")
        print(doc)
        print()