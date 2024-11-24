```bash

python -m venv .venv

pip install -e .

source $STORAGE_DIR/llama-stack/.venv/bin/activate

huggingface-cli login

# vLLM server
export INFERENCE_PORT=8000
export INFERENCE_MODEL=meta-llama/Llama-3.2-3B-Instruct
export CUDA_VISIBLE_DEVICES=0
sudo docker run --gpus all \
    -v $STORAGE_DIR/.cache/huggingface:/root/.cache/huggingface \
    --env "HUGGING_FACE_HUB_TOKEN=$(cat ~/.cache/huggingface/token)" \
    -p 8000:$INFERENCE_PORT \
    --ipc=host \
    vllm/vllm-openai:latest \
    --model $INFERENCE_MODEL

llama model download --model-id meta-llama/Llama-3.2-3B-Instruct

With signed URL: https://llama3-2-lightweight.llamameta.net/*?Policy=eyJTdGF0ZW1lbnQiOlt7InVuaXF1ZV9oYXNoIjoiZGNubGlrczQzdmJ3bDlwaHhubGFsYmNwIiwiUmVzb3VyY2UiOiJodHRwczpcL1wvbGxhbWEzLTItbGlnaHR3ZWlnaHQubGxhbWFtZXRhLm5ldFwvKiIsIkNvbmRpdGlvbiI6eyJEYXRlTGVzc1RoYW4iOnsiQVdTOkVwb2NoVGltZSI6MTczMjYxMzAwOX19fV19&Signature=OpxDUyU40ZbJsx1RE4rNRDXEIhyPuFJDaM4O-wEiXBYXWRXt16Bo9L9HgEpEhMnPicSsZmjMcr5-zVoIIbItWWphbURcCMmUUm3lwUaRAaMKVd%7Eu92lscYpW7PjNC9r2yKUYs-PCSaqSrBeWuJ0eB1cqqabPnVa90If0ADpLlc8EQQHT8BflrZbfCC3shrbcoBAkrMSsGhZjgNumuaKsg6Gt8jen6MIGbaZfypZY2uSQFRAaw67Uu7-w2YmtkMhjqibH5zMwN6yt-ParNXwJ59oU2shy3o9es3O8060aZUL2lHaGCMKeGG6s9qRZAaI9qe8g4roJDJ31thk7AiaKsw__&Key-Pair-Id=K15QRJLYKIFSLZ&Download-Request-ID=1459276644742760

# Meta reference gpu server
LLAMA_STACK_PORT=5001
docker run \
  -it \
  -p $LLAMA_STACK_PORT:$LLAMA_STACK_PORT \
  llamastack/distribution-meta-reference-gpu \
  --port $LLAMA_STACK_PORT \
  --env INFERENCE_MODEL=meta-llama/Llama-3.2-3B-Instruct

```