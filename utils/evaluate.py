# utils/evaluate.py — Test RAG retrieval quality
"""
Run: python utils/evaluate.py
Tests the RAG chain against a set of ground-truth Q&A pairs.
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from chain.rag_chain import GautamSolarRAGChain

TEST_CASES = [
    {
        "question": "What is the efficiency of the G12 R TOPCon module?",
        "keywords": ["23.69", "22.95", "efficiency"],
    },
    {
        "question": "Who is eligible for PM-KUSUM scheme?",
        "keywords": ["farmer", "cooperative", "panchayat", "FPO"],
    },
    {
        "question": "What is the warranty on Gautam Solar panels?",
        "keywords": ["12", "30", "25", "warranty"],
    },
    {
        "question": "Which certifications does Gautam Solar have?",
        "keywords": ["BIS", "IEC", "TUV", "ALMM"],
    },
    {
        "question": "How much subsidy is available under PM-KUSUM?",
        "keywords": ["30%", "60%", "central", "state"],
    },
    {
        "question": "What is the degradation rate of Gautam Solar panels?",
        "keywords": ["0.4", "degradation", "1%"],
    },
    {
        "question": "How do I contact Gautam Solar?",
        "keywords": ["1800-532-0800", "info@gautamsolar.com"],
    },
]


def evaluate():
    print("\n" + "=" * 60)
    print("  🧪 GAUTAM SOLAR RAG — Evaluation Suite")
    print("=" * 60 + "\n")

    chain = GautamSolarRAGChain()
    passed = 0

    for i, tc in enumerate(TEST_CASES, 1):
        q = tc["question"]
        keywords = tc["keywords"]

        print(f"[{i}/{len(TEST_CASES)}] Q: {q}")
        result = chain.invoke(q)
        answer = result["answer"].lower()

        hits = [kw for kw in keywords if kw.lower() in answer]
        score = len(hits) / len(keywords)
        status = "✅ PASS" if score >= 0.5 else "⚠️  PARTIAL" if score > 0 else "❌ FAIL"
        if score >= 0.5:
            passed += 1

        print(f"   {status} — Keywords found: {hits} ({score:.0%})")
        print(f"   Sources: {[s['filename'] for s in result['sources']]}")
        print(f"   Answer preview: {result['answer'][:120]}...\n")

    print("=" * 60)
    print(f"  Result: {passed}/{len(TEST_CASES)} tests passed ({passed/len(TEST_CASES):.0%})")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    evaluate()