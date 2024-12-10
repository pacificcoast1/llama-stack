```bash
source ~/miniconda3/bin/activate
conda create --prefix ./envs python=3.10

source ~/miniconda3/bin/activate
conda activate ./envs

llama stack build --template groq --image-type conda \
&& track llama stack run ./run.yaml \
  --port 5001 \
  --env INFERENCE_MODEL=meta-llama/Llama-3.2-11B-Vision-Instruct
```