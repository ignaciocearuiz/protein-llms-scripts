import argparse
import json, os
import torch
from transformers import LlamaForCausalLM, LlamaTokenizer, GenerationConfig
from peft import PeftModel, PeftConfig  # Import for LoRA models
from tqdm import tqdm

# Existing generation config
generation_config = GenerationConfig(
  temperature=0.2,
  top_k=40,
  top_p=0.9,
  do_sample=True,
  num_beams=1,
  repetition_penalty=1.2,
  max_new_tokens=400
)

# Argument parser
parser = argparse.ArgumentParser()
parser.add_argument('--model', default=None, type=str, help="The local path of the model. If None, the model will be downloaded from HuggingFace")
parser.add_argument('--interactive', action='store_true', help="If True, you can input instructions interactively.")
parser.add_argument('--input_file', default=None, help="You can put all your input instructions in this file (one instruction per line).")
parser.add_argument('--output_file', default=None, help="All the outputs will be saved in this file (one output per line).")
args = parser.parse_args()

if __name__ == '__main__':
  if args.interactive and args.input_file:
    raise ValueError("interactive is True, but input_file is not None.")
  if (not args.interactive) and (args.input_file is None):
    raise ValueError("interactive is False, but input_file is None.")
  if args.input_file and (args.output_file is None):
    raise ValueError("input_file is not None, but output_file is None.")

  # Load the tokenizer
  tokenizer = LlamaTokenizer.from_pretrained(args.model)

  # Load the fine-tuned model with LoRA adapters
  adapter_config = PeftConfig.from_pretrained(args.model)
  base_model = LlamaForCausalLM.from_pretrained(adapter_config.base_model_name_or_path)
  model = PeftModel.from_pretrained(base_model, args.model)

  # Move model to the appropriate device
  device = "cuda" if torch.cuda.is_available() else "cpu"
  model.to(device)

  model.eval()
  with torch.no_grad():
    if args.interactive:
      while True:
        raw_input_text = input("Input:")
        if len(raw_input_text.strip())==0:
          break
        input_text = raw_input_text
        input_text = tokenizer(input_text, return_tensors="pt")

        generation_output = model.generate(
          input_ids = input_text["input_ids"].to(device),
          attention_mask = input_text['attention_mask'].to(device),
          eos_token_id=tokenizer.eos_token_id,
          pad_token_id=tokenizer.pad_token_id,
          generation_config = generation_config,
          output_attentions=False
        )
        s = generation_output[0]
        output = tokenizer.decode(s,skip_special_tokens=True)
        print("Output:",output)
        print("\n")
    else:
      outputs = []
      with open(args.input_file, 'r') as f:
        examples =f.read().splitlines()
      print("Start generating...")
      for index, example in tqdm(enumerate(examples),total=len(examples)):
        input_text = tokenizer(example,return_tensors="pt")  #add_special_tokens=False ?

        generation_output = model.generate(
          input_ids = input_text["input_ids"].to(device),
          attention_mask = input_text['attention_mask'].to(device),
          eos_token_id=tokenizer.eos_token_id,
          pad_token_id=tokenizer.pad_token_id,
          generation_config = generation_config
        )
        s = generation_output[0]
        output = tokenizer.decode(s,skip_special_tokens=True)
        outputs.append(output)
      with open(args.output_file,'w') as f:
        f.write("\n".join(outputs))
      print("All the outputs have been saved in",args.output_file)
