from flask import Flask, Response
from flask_cors import CORS
import torch
from gpt import GPTLanguageModel, decode
from train_gpt2 import GPT, GPTConfig
from tiktoken import get_encoding

app = Flask(__name__)
CORS(app, origins=[
    "http://localhost:3000",
    "https://icy-dune-00ee9d300.3.azurestaticapps.net/",
    "https://ebedes.com"
])

# Load model once at startup
device = 'cuda' if torch.cuda.is_available() else 'cpu'
model = GPTLanguageModel()
model.load_state_dict(torch.load('seinfeldGPT.pth', map_location=device))
model.to(device)
model.eval()

# Load checkpoint
checkpoint = torch.load('log/model_00999.pt', map_location=device, weights_only=False)
# Recreate model with config and load weights
model2 = GPT(checkpoint['config'])
model2.load_state_dict(checkpoint['model'])
model2.to(device)
model2.eval()

@app.route('/seinfeldGPT')
def seinfeld_gpt():
    def generate_stream():
        context = torch.zeros((1, 1), dtype=torch.long, device=device)
        with torch.no_grad():
            for _ in range(5000):  # or your desired max tokens
                generated = model.generate(context, max_new_tokens=1)
                token_id = generated[0, -1].item()
                text = decode([token_id])
                yield text  # send each token as soon as it's generated
                context = torch.cat([context, torch.tensor([[token_id]], device=device)], dim=1)
    return Response(generate_stream(), mimetype='text/plain')

@app.route('/seinfeldGPT2')
def seinfeld_gpt2():
    def generate_stream():
        # Start with a prompt, e.g. "JERRY: "
        enc = get_encoding("gpt2")
        prompt = "JERRY: "
        tokens = enc.encode(prompt)
        context = torch.tensor(tokens, dtype=torch.long, device=device).unsqueeze(0)
        block_size = model2.config.block_size

        with torch.no_grad():
            for _ in range(5000):  # generate 5000 tokens
                # Trim context if too long
                if context.size(1) > block_size:
                    context = context[:, -block_size:]
                logits, _ = model2(context)
                next_token_logits = logits[:, -1, :]
                probs = torch.softmax(next_token_logits, dim=-1)
                next_token = torch.multinomial(probs, num_samples=1)
                context = torch.cat([context, next_token], dim=1)
                text = enc.decode([next_token.item()])
                yield text
    return Response(generate_stream(), mimetype='text/plain')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=443, ssl_context=("backend.ebedes.com-chain.pem", "backend.ebedes.com-key.pem"))
