from llama_stack_client import LlamaStackClient
from llama_stack_client.types.memory_insert_params import Document

client = LlamaStackClient(
    base_url="http://localhost:5001",
)

providers = client.providers.list()
memory_banks_response = client.memory_banks.list()

provider = providers["memory"][0]

print("using provider: ", provider)

counter = get_counter()
bank_id = f"bank_pdf_paper{counter}"
client.memory_banks.register(
    memory_bank_id=bank_id,
    params={
        "embedding_model": "all-MiniLM-L6-v2",
        "chunk_size_in_tokens": 512,
        "overlap_size_in_tokens": 64,
    },
    provider_id=provider.provider_id,
)

urls = ["https://arxiv.org/pdf/2407.21783"]

documents = [
    Document(
        document_id=f"num-{i}",
        content=url,
        mime_type="application/pdf",
        metadata={},
    )
    for i, url in enumerate(urls)
]

client.memory.insert(
    bank_id=bank_id,
    documents=documents,
)

def get_counter():
    with open("counter.txt", "r") as f:
        counter = int(f.read().strip())
    counter += 1
    with open("counter.txt", "w") as f:
        f.write(str(counter))
    return counter
