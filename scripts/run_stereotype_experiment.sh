#!/bin/bash

parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"
#arb_Arab fra_Latn heb_Hebr jpn_Jpan spa_Latn zho_Hans
#arabic chinese french hebrew japanese spanish
#en-ar_combined en-es_combined en-fr_combined en-he_combined en-ja_combined en-zh_combined 
#google/gemma-2b deepseek-ai/deepseek-llm-7b-base meta-llama/Meta-Llama-3-8B microsoft/Phi-4-reasoning
for model in meta-llama/Meta-Llama-3-8B
    do
    for variable in en-ar_combined en-es_combined en-fr_combined en-he_combined en-ja_combined en-zh_combined 
    do
        python -u ../probing/mgp.py \
        --model $model \
        --variable $variable \
        --attribute occupations \
        --device 0 \
        --calibrate
    done
done
