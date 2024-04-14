import torch
from torch.nn.functional import normalize
from transformers import AutoModel, AutoTokenizer
from flask import Flask
app = Flask(__name__)
from flask import request


device = "cuda" if torch.cuda.is_available() else "cpu"
model_id = "thenlper/gte-base"

tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModel.from_pretrained(model_id).to(device)
model.eval()

def embed(docs: list[str]) -> list[list[float]]:
    tokens = tokenizer(
            docs, padding=True, max_length=512, truncation=True, return_tensors="pt"
    ).to(device)
    with torch.no_grad():
        out = model(**tokens)
        last_hidden = out.last_hidden_state.masked_fill(
                ~tokens["attention_mask"][..., None].bool(), 0.0
        )
        doc_embeds = last_hidden.sum(dim=1) / \
            tokens["attention_mask"].sum(dim=1)[..., None]
    return doc_embeds.cpu().numpy().tolist()

@app.route('/search', methods=['GET'])
def my_python_function():
    string_param = request.args.get('term')
    
    result = embed([string_param])
    
    return result


if __name__ == '__main__':
    app.run(debug=True)