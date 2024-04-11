# -*- coding: utf-8 -*-
"""Mistral-7b-AutoTrain_Q&A-LLM.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1w4qvJIva_8M5Xo_s1qTBkSZKQz-XGWAm
"""

#@title 🤗 AutoTrain LLM
#@markdown In order to use this colab
#@markdown - upload train.csv to a folder named `data/`
#@markdown - train.csv must contain a `text` column
#@markdown - choose a project name if you wish
#@markdown - change model if you wish, you can use most of the text-generation models from Hugging Face Hub
#@markdown - add huggingface information (token and repo_id) if you wish to push trained model to huggingface hub
#@markdown - update hyperparameters if you wish
#@markdown - click `Runtime > Run all` or run each cell individually
#@markdown - report issues / feature requests here: https://github.com/huggingface/autotrain-advanced/issues

import os
!pip install -U autotrain-advanced > install_logs.txt
!autotrain setup --colab > setup_logs.txt

import os

#In general, there are two foundational models that Mistral released: Mistral 7B v0.1 and Mistral 7B Instruct v0.1. The Mistral 7B v0.1 is the base foundation model, and the Mistral 7B Instruct v0.1 is a Mistral 7B v0.1 model that has been fine-tuned for conversation and question answering.

#We would need a CSV file containing a text column for the fine-tuning with Hugging Face AutoTrain. However, we would use a different text format for the base and instruction models during the fine-tuning.
from datasets import load_dataset
import pandas as pd

# Load the dataset
train= load_dataset("tatsu-lab/alpaca",split='train[:10%]')
train = pd.DataFrame(train)
train

train['text'][5196], train['text'][0]

#The dataset already contains the text columns with a format we need to fine-tune our LLM model. That’s why we don’t need to perform anything. However, I would provide a code if you have another dataset that needs the formatting.

def text_formatting(data):

    # If the input column is not empty
    if data['input']:

        text = f"""Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.\n\n### Instruction:\n{data["instruction"]} \n\n### Input:\n{data["input"]}\n\n### Response:\n{data["output"]}"""

    else:

        text = f"""Below is an instruction that describes a task. Write a response that appropriately completes the request.\n\n### Instruction:\n{data["instruction"]}\n\n### Response:\n{data["output"]}"""

    return text

train['text'] = train.apply(text_formatting, axis =1)

train

train['text'][5196], train['text'][0]

##If you want to fine-tune the Mistral 7B Instruct v0.1 for conversation and question answering, we need to follow the chat template format provided by Mistral, shown in the code block below.

#<s>[INST] Instruction [/INST] Model answer</s>[INST] Follow-up instruction [/INST]


#If we use our previous example dataset, we need to reformat the text column. We would use only the data without any input for the chat model.

train_chat = train[train['input'] == ''].reset_index(drop = True).copy()
print("1111111111111", train_chat)

#Then, we could reformat the data with the following code.

def chat_formatting(data):

  text = f"<s>[INST] {data['instruction']} [/INST] {data['output']} </s>"

  return text

train_chat['text'] = train_chat.apply(chat_formatting, axis =1)
train_chat.to_csv('train_QA_chat.csv', index =False)
print("22222222222", train_chat)

train_chat['text'][0], train_chat

train_qa_chat =train_chat.copy()
train_qa_chat.to_csv('data/train_QA_chat.csv', index =False)
print("33333333", train_qa_chat)

#@markdown ---
#@markdown #### Project Config
#@markdown Note: if you are using a restricted/private model, you need to enter your Hugging Face token in the next step.
project_name = 'Mistral-7B-autotrain-finetune-QA-project-vx' # @param {type:"string"}
model_name = 'mistralai/Mistral-7B-Instruct-v0.1' # @param {type:"string"}

#@markdown ---
#@markdown #### Push to Hub?
#@markdown Use these only if you want to push your trained model to a private repo in your Hugging Face Account
#@markdown If you dont use these, the model will be saved in Google Colab and you are required to download it manually.
#@markdown Please enter your Hugging Face write token. The trained model will be saved to your Hugging Face account.
#@markdown You can find your token here: https://huggingface.co/settings/tokens
push_to_hub = True # @param ["False", "True"] {type:"raw"}
hf_token = "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" #@param {type:"string"}
repo_id = "kr-manish/Mistral-7B-autotrain-finetune-QA-vx" #@param {type:"string"}

#@markdown ---
#@markdown #### Hyperparameters
learning_rate = 2e-4 # @param {type:"number"}
num_epochs = 3 #@param {type:"number"}
batch_size = 1 # @param {type:"slider", min:1, max:32, step:1}
block_size = 1024 # @param {type:"number"}
trainer = "sft" # @param ["default", "sft"] {type:"raw"}
warmup_ratio = 0.1 # @param {type:"number"}
weight_decay = 0.01 # @param {type:"number"}
gradient_accumulation = 4 # @param {type:"number"}
mixed_precision = "fp16" # @param ["fp16", "bf16", "none"] {type:"raw"}
peft = True # @param ["False", "True"] {type:"raw"}
quantization = "int4" # @param ["int4", "int8", "none"] {type:"raw"}
lora_r = 16 #@param {type:"number"}
lora_alpha = 32 #@param {type:"number"}
lora_dropout = 0.05 #@param {type:"number"}

os.environ["PROJECT_NAME"] = project_name
os.environ["MODEL_NAME"] = model_name
os.environ["PUSH_TO_HUB"] = str(push_to_hub)
os.environ["HF_TOKEN"] = hf_token
os.environ["REPO_ID"] = repo_id
os.environ["LEARNING_RATE"] = str(learning_rate)
os.environ["NUM_EPOCHS"] = str(num_epochs)
os.environ["BATCH_SIZE"] = str(batch_size)
os.environ["BLOCK_SIZE"] = str(block_size)
os.environ["WARMUP_RATIO"] = str(warmup_ratio)
os.environ["WEIGHT_DECAY"] = str(weight_decay)
os.environ["GRADIENT_ACCUMULATION"] = str(gradient_accumulation)
os.environ["MIXED_PRECISION"] = str(mixed_precision)
os.environ["PEFT"] = str(peft)
os.environ["QUANTIZATION"] = str(quantization)
os.environ["LORA_R"] = str(lora_r)
os.environ["LORA_ALPHA"] = str(lora_alpha)
os.environ["LORA_DROPOUT"] = str(lora_dropout)

from huggingface_hub import notebook_login
notebook_login()

!autotrain llm --help

!autotrain llm \
--train \
--model ${MODEL_NAME} \
--project-name ${PROJECT_NAME} \
--data-path data/ \
--text-column text \
--lr ${LEARNING_RATE} \
--batch-size ${BATCH_SIZE} \
--epochs ${NUM_EPOCHS} \
--block-size ${BLOCK_SIZE} \
--warmup-ratio ${WARMUP_RATIO} \
--lora-r ${LORA_R} \
--lora-alpha ${LORA_ALPHA} \
--lora-dropout ${LORA_DROPOUT} \
--weight-decay ${WEIGHT_DECAY} \
--gradient-accumulation ${GRADIENT_ACCUMULATION} \
--quantization ${QUANTIZATION} \
--mixed-precision ${MIXED_PRECISION} \
--merge_adapter \
$( [[ "$PEFT" == "True" ]] && echo "--peft" ) \
$( [[ "$PUSH_TO_HUB" == "True" ]] && echo "--push-to-hub --token ${HF_TOKEN} --repo-id ${REPO_ID}" )

from transformers import AutoModelForCausalLM, AutoTokenizer

model_path = "kr-manish/Mistral-7B-autotrain-finetune-QA-vx"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(model_path)

input_text = "What is the scientific name of the honey bee?"
# Tokenize input text
input_ids = tokenizer.encode(input_text, return_tensors="pt")

# Generate output text
output = model.generate(input_ids, max_length=100, num_return_sequences=1, do_sample=True)

# Decode and print output
generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
print(generated_text)

from transformers import AutoModelForCausalLM, AutoTokenizer

model_path = "kr-manish/Mistral-7B-autotrain-finetune-QA-vx"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(model_path)

# Generate response
input_text = "Give three tips for staying healthy."
input_ids = tokenizer.encode(input_text, return_tensors="pt")
output = model.generate(input_ids, max_new_tokens = 200)
predicted_text = tokenizer.decode(output[0], skip_special_tokens=True)
print(predicted_text)



