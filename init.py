# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the terms described in the LICENSE file in
# the root directory of this source tree.

from counter import get_and_increment_counter
from llama_stack_client import LlamaStackClient
from llama_stack_client.types.memory_insert_params import Document

client = LlamaStackClient(
    base_url="http://localhost:5001",
)

providers = client.providers.list()
memory_banks_response = client.memory_banks.list()

print(providers)

provider = providers["memory"][0]

print("using provider: ", provider)

bank_id = f"bank_pdf_paper_{get_and_increment_counter()}"
print("bank_id: ", bank_id)
client.memory_banks.register(
    memory_bank_id=bank_id,
    params={
        "embedding_model": "all-MiniLM-L6-v2",
        "chunk_size_in_tokens": 100,
        "overlap_size_in_tokens": 10,
    },
    provider_id=provider.provider_id,
)

documents = [
    Document(
        document_id="num-0",
        content="Hello, world!",
        mime_type="text/plain",
        metadata={},
    ),
]

client.memory.insert(
    bank_id=bank_id,
    documents=documents,
)
