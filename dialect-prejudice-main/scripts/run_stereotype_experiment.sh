#!/bin/bash

parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"
#arb_Arab fra_Latn heb_Hebr jpn_Jpan rus_Cyrl spa_Latn zho_Hans
#arabic chinese french hebrew japanese russian spanish
#google/gemma-2b deepseek-ai/deepseek-llm-7b-base meta-llama/Meta-Llama-3-8B microsoft/Phi-4-reasoning
for model in microsoft/Phi-4-reasoning
    do
    for variable in jpn_Jpan spa_Latn zho_Hans
    do
        python -u ../probing/mgp.py \
        --model $model \
        --variable $variable \
        --attribute occupations \
        --device 0 \
        --calibrate
    done
done
