import chromadb
import re
from chroma_store import get_client
from difflib import SequenceMatcher

client = get_client()
collection = client.get_or_create_collection(name="weather") 

def fuzzy_match_province(query, provinces, threshold=0.6):
    """หาจังหวัดที่ใกล้เคียงที่สุด"""
    best_match = None
    best_score = 0
    
    for province in provinces:
        # ลบคำว่า "จังหวัด" และช่องว่าง
        clean_query = re.sub(r'จังหวัด:?\s*', '', query).strip()
        
        # คำนวณความคล้าย
        score = SequenceMatcher(None, clean_query.lower(), province.lower()).ratio()
        
        if score > best_score and score >= threshold:
            best_score = score
            best_match = province
    
    return best_match, best_score

def extract_province_from_query(query):
    """ดึงชื่อจังหวัดจาก query"""
    # รูปแบบต่างๆ ของการระบุจังหวัด
    patterns = [
        r'จังหวัด:?\s*([ก-๙\s]+?)(?:\s|$|เป็น|อากาศ|อุณหภูมิ|ความชื้น)',
        r'จ\.?\s*([ก-๙\s]+?)(?:\s|$|เป็น|อากาศ|อุณหภูมิ|ความชื้น)',
        r'^([ก-๙]+?)(?:\s|$|เป็น|อากาศ|อุณหภูมิ|ความชื้น)',
        r'([ก-๙]+?)(?:อากาศ|เป็นอย่างไร|อุณหภูมิ|ความชื้น)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, query)
        if match:
            return match.group(1).strip()
    
    return None

def hybrid_search(query, n_results=3):
    """ค้นหาแบบ Hybrid: Exact + Semantic"""
    
    print(f"🔍 กำลังค้นหา: '{query}'")
    
    # 1. ดึงรายชื่อจังหวัดทั้งหมด
    all_data = collection.get()
    provinces = list(set(meta['province'] for meta in all_data['metadatas']))
    
    # 2. หาจังหวัดจาก query
    extracted_province = extract_province_from_query(query)
    print(f"🏛️ จังหวัดที่ดึงได้: {extracted_province}")
    
    # 3. Fuzzy matching ถ้าไม่เจอ exact match
    target_province = None
    if extracted_province:
        if extracted_province in provinces:
            target_province = extracted_province
            print(f"✅ เจอจังหวัดตรงกัน: {target_province}")
        else:
            fuzzy_province, score = fuzzy_match_province(extracted_province, provinces)
            if fuzzy_province:
                target_province = fuzzy_province
                print(f"🎯 Fuzzy match: {fuzzy_province} (คะแนน: {score:.2f})")
    
    # 4. ค้นหาข้อมูล
    results = None
    
    if target_province:
        # ค้นหาแบบ exact match metadata ก่อน
        exact_results = collection.query(
            query_texts=[query],
            n_results=n_results,
            where={"province": target_province}
        )
        
        if exact_results['documents'][0]:
            print(f"📍 เจอข้อมูล exact match: {len(exact_results['documents'][0])} รายการ")
            results = exact_results
        else:
            print("❌ ไม่เจอข้อมูล exact match")
    
    # 5. ถ้าไม่เจอ exact match ให้ใช้ semantic search
    if not results or not results['documents'][0]:
        print("🔄 ใช้ semantic search")
        semantic_results = collection.query(
            query_texts=[query],
            n_results=n_results * 2  # เอามากกว่าเพื่อกรอง
        )
        
        # กรองผลลัพธ์ให้ดีขึ้น
        if target_province and semantic_results['documents'][0]:
            # หาเอกสารที่มีจังหวัดที่เกี่ยวข้อง
            filtered_docs = []
            filtered_meta = []
            filtered_distances = []
            
            for i, (doc, meta, dist) in enumerate(zip(
                semantic_results['documents'][0],
                semantic_results['metadatas'][0],
                semantic_results.get('distances', [[]])[0]
            )):
                if meta['province'] == target_province:
                    filtered_docs.append(doc)
                    filtered_meta.append(meta)
                    filtered_distances.append(dist)
                    if len(filtered_docs) >= n_results:
                        break
            
            if filtered_docs:
                results = {
                    'documents': [filtered_docs],
                    'metadatas': [filtered_meta],
                    'distances': [filtered_distances]
                }
                print(f"🎯 กรองแล้ว: {len(filtered_docs)} รายการ")
        
        if not results or not results['documents'][0]:
            results = semantic_results
            # จำกัดผลลัพธ์
            if results['documents'][0]:
                results['documents'] = [results['documents'][0][:n_results]]
                if 'metadatas' in results:
                    results['metadatas'] = [results['metadatas'][0][:n_results]]
                if 'distances' in results:
                    results['distances'] = [results['distances'][0][:n_results]]
    
    return results, target_province

def ask(query):
    """ฟังก์ชันถาม-ตอบที่ปรับปรุงแล้ว"""
    
    results, target_province = hybrid_search(query)
    
    if not results or not results['documents'][0]:
        print("❌ ไม่พบข้อมูลที่เกี่ยวข้อง")
        
        # แสดงจังหวัดที่มีในระบบ
        all_data = collection.get()
        provinces = sorted(set(meta['province'] for meta in all_data['metadatas']))
        print(f"\n🗺️ จังหวัดที่มีในระบบ ({len(provinces)} จังหวัด):")
        for i, province in enumerate(provinces, 1):
            print(f"   {i:2d}. {province}")
        return
    
    print(f"\n✅ พบ {len(results['documents'][0])} ผลลัพธ์:")
    
    # แสดงคะแนนความเกี่ยวข้อง
    distances = results.get('distances', [[]])[0]
    
    for i, doc in enumerate(results['documents'][0]):
        score_text = f" (คะแนน: {distances[i]:.3f})" if i < len(distances) else ""
        print(f"\n🔹 ตอบ {i+1}{score_text}:")
        print(doc)
        print("-" * 50)

def test_improved_system():
    """ทดสอบระบบที่ปรับปรุงแล้ว"""
    print("🧪 ทดสอบระบบ QA ที่ปรับปรุงแล้ว")
    print("=" * 60)
    
    test_queries = [
        "ชลบุรี",
        "จังหวัดชลบุรี", 
        "ชลบุรีอากาศเป็นอย่างไร",
        "อุณหภูมิชลบุรี",
        "กรุงเทพฯ",
        "กรุงเทพมหานคร",
        "เชียงใหม่อากาศ",
        "ภูเก็ตอากาศเป็นอย่างไร"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{i}️⃣ ทดสอบ: {query}")
        print("-" * 40)
        ask(query)
        
        if i < len(test_queries):
            input("\nกด Enter เพื่อทดสอบต่อ...")

if __name__ == "__main__":
    test_improved_system()