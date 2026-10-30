"""Real one-step CPU SFT + LoRA save/reload. No pretrained downloads or GPU claim."""
import json
import tempfile
from pathlib import Path
from importlib.metadata import version
import torch
from tokenizers import Tokenizer
from tokenizers.models import WordLevel
from tokenizers.pre_tokenizers import Whitespace
from transformers import PreTrainedTokenizerFast, Qwen2Config, Qwen2ForCausalLM
from peft import LoraConfig, get_peft_model, PeftModel
from datasets import Dataset
from trl import SFTConfig, SFTTrainer

torch.manual_seed(42)
torch.set_num_threads(2)
vocabulary={word:i for i,word in enumerate(['[PAD]','[UNK]','[EOS]','user','assistant','crack','visible','cause','unknown','inspect','evidence','report',':','.'])}
raw=Tokenizer(WordLevel(vocabulary,unk_token='[UNK]'));raw.pre_tokenizer=Whitespace()
tokenizer=PreTrainedTokenizerFast(tokenizer_object=raw,pad_token='[PAD]',unk_token='[UNK]',eos_token='[EOS]')
tokenizer.chat_template="{% for m in messages %}{{ m['role'] + ': ' + m['content'] + ' ' + eos_token + ' ' }}{% endfor %}{% if add_generation_prompt %}assistant: {% endif %}"
config=Qwen2Config(vocab_size=len(vocabulary),hidden_size=32,intermediate_size=64,num_hidden_layers=1,
    num_attention_heads=2,num_key_value_heads=2,max_position_embeddings=128,
    pad_token_id=tokenizer.pad_token_id,eos_token_id=tokenizer.eos_token_id,
    tie_word_embeddings=True,attention_dropout=0.0)
with tempfile.TemporaryDirectory() as directory:
    root=Path(directory)
    base=Qwen2ForCausalLM(config)
    base.save_pretrained(root/'base')
    model=get_peft_model(base,LoraConfig(r=4,lora_alpha=8,lora_dropout=0.0,target_modules=['q_proj','v_proj'],task_type='CAUSAL_LM'))
    before={name:p.detach().clone() for name,p in model.named_parameters() if p.requires_grad}
    data=Dataset.from_list([{'messages':[{'role':'user','content':'crack visible evidence'},{'role':'assistant','content':'cause unknown inspect'}]} for _ in range(4)])
    args=SFTConfig(output_dir=str(root/'train'),max_steps=1,per_device_train_batch_size=2,
        learning_rate=.001,max_length=64,packing=False,assistant_only_loss=False,completion_only_loss=False,
        loss_type='nll',use_cpu=True,bf16=False,fp16=False,gradient_checkpointing=False,
        save_strategy='no',eval_strategy='no',report_to='none',logging_steps=1,seed=42)
    trainer=SFTTrainer(model=model,args=args,train_dataset=data,processing_class=tokenizer)
    batch=next(iter(trainer.get_train_dataloader()))
    assert (batch['labels'][batch['attention_mask']==0]==-100).all()
    assert (batch['labels']!=-100).any()
    result=trainer.train()
    changed=[name for name,p in model.named_parameters() if name in before and not torch.equal(before[name],p.detach())]
    assert changed, 'No trainable parameter changed'
    model.eval();model.config.use_cache=True
    inputs=tokenizer.apply_chat_template([{'role':'user','content':'crack visible'}],add_generation_prompt=True,return_dict=True,return_tensors='pt')
    with torch.inference_mode():
        logits_before=model(**inputs).logits.detach().clone()
        tokens_before=model.generate(**inputs,max_new_tokens=5,do_sample=False)
    model.save_pretrained(root/'adapter');tokenizer.save_pretrained(root/'adapter')
    del trainer,model,base
    reloaded=PeftModel.from_pretrained(Qwen2ForCausalLM.from_pretrained(root/'base'),root/'adapter')
    reloaded.eval();reloaded.config.use_cache=True
    with torch.inference_mode():
        logits_after=reloaded(**inputs).logits
        tokens_after=reloaded.generate(**inputs,max_new_tokens=5,do_sample=False)
    assert torch.allclose(logits_before,logits_after,atol=1e-6,rtol=1e-6)
    assert torch.equal(tokens_before,tokens_after)
    print(json.dumps({'status':'PASS','training_steps':1,'changed_parameter_tensors':len(changed),
        'loss':result.training_loss,'reload_logits_equal':True,'reload_generated_ids_equal':True,
        'scope':'tiny random Qwen2 CPU; not pretrained quality or GPU QLoRA validation',
        'packages':{name:version(name) for name in ['torch','transformers','peft','trl','datasets']}},indent=2))
