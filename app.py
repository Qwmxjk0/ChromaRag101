from rag.chroma_store import store_to_chroma
# from rag.qa import ask
from rag.improved_qa_system import ask

if __name__ == "__main__":
    store_to_chroma()
    ask("กำแพง")

    

    # ทดสอบด่วน
    print("🚀 ทดสอบระบบใหม่")
    print("=" * 50)

    # ทดสอบกรณีที่เคยเป็นปัญหา
    test_cases = [
        "ชลบุรี",
        "จังหวัด: ชลบุรี เป็นอย่างไร", 
        "สมุทรปราการ",
        "กรุงเทพมหานคร",
        "เชียงใหม่อากาศ"
    ]

    for query in test_cases:
        print(f"\n{'='*60}")
        ask(query)
        print(f"{'='*60}")
