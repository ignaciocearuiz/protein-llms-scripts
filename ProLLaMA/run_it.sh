# MODIFIED TO EXECUTE ON GOOGLE COLAB
# the codes are based on Chinese-LLaMA-Alpaca-2
# Read the wiki(https://github.com/ymcui/Chinese-LLaMA-Alpaca-2/wiki/sft_scripts_zh) carefully before running the script
export CUDA_VISIBLE_DEVICES=0
export WANDB_PROJECT="instruction_tuning"
lr=5e-5
lora_rank=64
lora_alpha=128
lora_trainable="q_proj,v_proj,k_proj,o_proj,gate_proj,down_proj,up_proj"
lora_dropout=0.05

pretrained_model=GreatCaptainNemo/ProLLaMA_Stage_1 #or your local path
dataset_dir=/content/ProLLaMA/scripts/instruction_tuning_dataset #your dataset path
per_device_train_batch_size=144
gradient_accumulation_steps=4
max_seq_length=256
output_dir=save_dir/
deepspeed_config_file=/content/ProLLaMA/scripts/ds_zero2_no_offload.json
torchrun --nproc_per_node 1 /content/ProLLaMA/scripts/instruction_tune.py \
    --deepspeed ${deepspeed_config_file} \
    --model_name_or_path ${pretrained_model} \
    --tokenizer_name_or_path ${pretrained_model} \
    --dataset_dir ${dataset_dir} \
    --per_device_train_batch_size ${per_device_train_batch_size} \
    --do_train \
    --seed 42 \
    --fp16 \
    --num_train_epochs 2 \
    --lr_scheduler_type cosine \
    --learning_rate ${lr} \
    --warmup_ratio 0.03 \
    --weight_decay 0 \
    --logging_strategy steps \
    --logging_steps 2 \
    --save_strategy steps \
    --save_total_limit 3 \
    --save_steps 1000 \
    --gradient_accumulation_steps ${gradient_accumulation_steps} \
    --preprocessing_num_workers 32 \
    --max_seq_length ${max_seq_length} \
    --output_dir ${output_dir} \
    --ddp_timeout 30000 \
    --logging_first_step True \
    --lora_rank ${lora_rank} \
    --lora_alpha ${lora_alpha} \
    --trainable ${lora_trainable} \
    --lora_dropout ${lora_dropout} \
    --torch_dtype float16 \
    --save_safetensors False \
    --ddp_find_unused_parameters False \
    --gradient_checkpointing \
    --overwrite_output_dir
