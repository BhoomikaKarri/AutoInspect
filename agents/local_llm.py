from transformers import AutoTokenizer, AutoModelForCausalLM


MODEL_NAME = "Qwen/Qwen2.5-1.5B-Instruct"


print("Loading local LLM...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)


messages = [
    {
        "role": "system",
        "content": "You are an infrastructure inspection assistant."
    },
    {
        "role": "user",
        "content": "In one sentence, explain why bridge inspection reports are useful."
    }
]

text = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True
)

inputs = tokenizer(
    text,
    return_tensors="pt"
)

outputs = model.generate(
    **inputs,
    max_new_tokens=60,
    do_sample=False
)

response = tokenizer.decode(
    outputs[0][inputs["input_ids"].shape[-1]:],
    skip_special_tokens=True
)

print("\n==============================")
print("LOCAL LLM TEST")
print("==============================")
print(response)