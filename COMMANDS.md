```bash

python -m venv .venv

pip install -e .

source $STORAGE_DIR/llama-stack/.venv/bin/activate

huggingface-cli login

export $(cat .env | xargs)

Env vars:
LLAMA_STACK_PORT=5001
INFERENCE_MODEL=meta-llama/Llama-3.2-3B-Instruct
FIREWORKS_API_KEY=<api-key>

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

# Remote vLLM
export $(cat .env | xargs)
sudo docker run \
  -it \
  --net=host \
  -p $LLAMA_STACK_PORT:$LLAMA_STACK_PORT \
  -v ./run.yaml:/root/my-run.yaml \
  llamastack/distribution-remote-vllm \
  --yaml-config /root/my-run.yaml \
  --port $LLAMA_STACK_PORT \
  --env INFERENCE_MODEL=$INFERENCE_MODEL \
  --env VLLM_URL=http://localhost:$INFERENCE_PORT/v1

llama model download --model-id meta-llama/Llama-3.2-3B-Instruct
# Add in signed URL from email

# Meta reference gpu server
export $(cat .env | xargs)
sudo docker run \
  -it \
  -v ~/.llama:/root/.llama \
  --gpus all \
  -p $LLAMA_STACK_PORT:$LLAMA_STACK_PORT \
  llamastack/distribution-meta-reference-gpu \
  --port $LLAMA_STACK_PORT \
  --env INFERENCE_MODEL=meta-llama/Llama-3.2-3B-Instruct

# Fireworks server
sudo docker run \
    -it \
    -v ~/run.yaml:/root/run.yaml \
    --net=host \
    llamastack/distribution-fireworks \
    --env INFERENCE_MODEL=meta-llama/Llama-3.2-3B-Instruct \
    --env FIREWORKS_API_KEY=$FIREWORKS_API_KEY

llama-stack-client --endpoint http://localhost:$LLAMA_STACK_PORT   inference chat-completion   --message "hello, what model are you?"
```