from llama_stack_client import LlamaStackClient
from counter import last_counter

bank_id = f"bank_pdf_paper{last_counter()}"

client = LlamaStackClient(
    base_url="http://localhost:5001",
)

def query2context_pdf(query, bank_id):
  response = client.memory.query(
      bank_id=bank_id,
      query=[query],
  )

  context = ""
  for chunk, score in zip(response.chunks, response.scores):
      context += str(chunk) + str(score) + "\n" # chunk.content
  print(context)
  return context

query = "How big is the context window?"
query2context_pdf(query, bank_id)