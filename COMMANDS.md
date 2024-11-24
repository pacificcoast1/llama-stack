```bash

# Using Conda now
python -m venv .venv
source $STORAGE_DIR/llama-stack/.venv/bin/activate


conda create --name llama-stack python=3.10

conda activate llama-stack


pip install -e .

huggingface-cli login

export $(cat .env | xargs)

Env vars:
OLLAMA_INFERENCE_MODEL="llama3.2:3b-instruct-fp16"
LLAMA_STACK_PORT=5001
INFERENCE_MODEL=meta-llama/Llama-3.2-3B-Instruct
INFERENCE_PORT=8000
VLLM_URL=http://localhost:8000

# vLLM server
export $(cat .env | xargs)
sudo docker run --gpus all \
    -v $STORAGE_DIR/.cache/huggingface:/root/.cache/huggingface \
    --env "HUGGING_FACE_HUB_TOKEN=$(cat ~/.cache/huggingface/token)" \
    -p 8000:$INFERENCE_PORT \
    --ipc=host \
    --net=host \
    vllm/vllm-openai:v0.6.3.post1 \
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



# Install the stack
llama stack build --template remote-vllm --image-type conda
# Run the stack
export $(cat .env | xargs)
conda activate llamastack-remote-vllm 
llama stack run distributions/remote-vllm/run.yaml \
  --port 5001 \
  --env INFERENCE_MODEL=meta-llama/Llama-3.2-3B-Instruct
```