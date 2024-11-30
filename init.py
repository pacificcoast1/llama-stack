from llama_stack_client import LlamaStackClient
from llama_stack_client.types.memory_insert_params import Document
from counter import get_counter

client = LlamaStackClient(
    base_url="http://localhost:5001",
)

providers = client.providers.list()
memory_banks_response = client.memory_banks.list()

provider = providers["memory"][0]

print("using provider: ", provider)

counter = get_counter()
bank_id = f"bank_pdf_paper{counter}"
print("bank_id: ", bank_id)
client.memory_banks.register(
    memory_bank_id=bank_id,
    params={
        "embedding_model": "all-MiniLM-L6-v2",
        "chunk_size_in_tokens": 512,
        "overlap_size_in_tokens": 64,
    },
    provider_id=provider.provider_id,
)

documents = [
    Document(
        document_id=f"num-0",
        content="https://arxiv.org/pdf/2407.21783",
        mime_type="application/pdf",
        metadata={},
    ),
    Document(
        document_id=f"num-1",
        content={
          "uri": "https://raw.githubusercontent.com/py-pdf/sample-files/86217754b5056f02ed51d66ebd42d699df700bc1/011-google-doc-document/google-doc-document.pdf",
        },
        mime_type="application/pdf",
        metadata={},
    ),
]

client.memory.insert(
    bank_id=bank_id,
    documents=documents,
)

