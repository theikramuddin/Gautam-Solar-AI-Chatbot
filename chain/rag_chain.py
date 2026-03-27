# chain/rag_chain.py — LangChain RAG chain with conversation memory
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.documents import Document
from typing import List, Dict, Any
from config import MISTRAL_API_KEY, LLM_MODEL, LLM_TEMPERATURE, COMPANY_EMAIL, COMPANY_PHONE
from vectorstore.chroma_store import get_retriever

# ── System Prompt ─────────────────────────────────────────────────────────────
SYSTEM_PROMPT = f"""You are Surya — an expert AI assistant for Gautam Solar, one of India's Top 4 solar module manufacturers.

Your role is to help customers, farmers, installers, and businesses with:
- Solar panel product information (TOPCon, Mono PERC specifications)
- PM-KUSUM Yojana eligibility and application guidance
- ROI calculations and savings estimates
- Installation and maintenance guidance
- Certifications, quality standards, and compliance
- Pricing guidance and system sizing

RULES:
1. Answer ONLY from the provided context. Do not hallucinate facts.
2. If the answer is not in the context, say: "I don't have that specific information. Please contact our team at {COMPANY_EMAIL} or call {COMPANY_PHONE} for expert assistance."
3. For PM-KUSUM questions, always mention state-specific nodal agencies when relevant.
4. For technical specs, be precise with numbers.
5. Always be warm, helpful, and professional — like a knowledgeable solar advisor.
6. When recommending products, explain WHY it suits their need.
7. Keep answers concise but complete. Use bullet points for lists.

Context from Gautam Solar knowledge base:
{{context}}
"""

PROMPT = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{question}"),
])


def format_docs(docs: List[Document]) -> str:
    """Format retrieved documents into a context string."""
    parts = []
    for i, doc in enumerate(docs, 1):
        source = doc.metadata.get("filename", doc.metadata.get("source", "unknown"))
        src_type = doc.metadata.get("source_type", "")
        parts.append(f"[Source {i} — {src_type.upper()} | {source}]\n{doc.page_content}")
    return "\n\n---\n\n".join(parts)


def format_history(history: List[Dict]) -> List:
    """Convert session chat history to LangChain message objects."""
    messages = []
    for msg in history:
        if msg["role"] == "user":
            messages.append(HumanMessage(content=msg["content"]))
        elif msg["role"] == "assistant":
            messages.append(AIMessage(content=msg["content"]))
    return messages


class GautamSolarRAGChain:
    """
    Full RAG chain with:
    - Mistral LLM
    - ChromaDB retrieval
    - Conversation memory
    - Source attribution
    """

    def __init__(self):
        self.retriever = get_retriever()
        self.llm = ChatMistralAI(
            model=LLM_MODEL,
            api_key=MISTRAL_API_KEY,
            temperature=LLM_TEMPERATURE,
        )
        self.output_parser = StrOutputParser()

    def get_relevant_docs(self, question: str) -> List[Document]:
        """Retrieve top-k relevant documents for a question."""
        return self.retriever.invoke(question)

    def invoke(self, question: str, chat_history: List[Dict] = None) -> Dict[str, Any]:
        """
        Run the RAG chain.
        Returns: { "answer": str, "sources": List[dict] }
        """
        history = chat_history or []

        # 1. Retrieve relevant docs
        docs = self.get_relevant_docs(question)
        context = format_docs(docs)

        # 2. Format chat history
        messages = format_history(history)

        # 3. Build & run chain
        chain = PROMPT | self.llm | self.output_parser
        answer = chain.invoke({
            "context": context,
            "question": question,
            "chat_history": messages,
        })

        # 4. Build source metadata for display
        sources = []
        seen = set()
        for doc in docs:
            fname = doc.metadata.get("filename", "")
            stype = doc.metadata.get("source_type", "")
            key = f"{fname}_{stype}"
            if key not in seen:
                seen.add(key)
                sources.append({
                    "filename": fname,
                    "source_type": stype,
                    "category": doc.metadata.get("category", ""),
                    "product_name": doc.metadata.get("product_name", ""),
                })

        return {"answer": answer, "sources": sources, "docs": docs}


# Singleton for Streamlit caching
_chain_instance = None

def get_chain() -> GautamSolarRAGChain:
    global _chain_instance
    if _chain_instance is None:
        _chain_instance = GautamSolarRAGChain()
    return _chain_instance