#!/bin/bash

parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"
#arb_Arab fra_Latn heb_Hebr jpn_Jpan rus_Cyrl spa_Latn zho_Hans
#google/gemma-2b deepseek-ai/deepseek-llm-7b-base meta-llama/Meta-Llama-3-8B
for model in google/gemma-2b deepseek-ai/deepseek-llm-7b-base meta-llama/Meta-Llama-3-8B
    do
    for variable in arabic chinese french hebrew japanese russian spanish
    do
        python -u ../probing/mgp.py \
        --model $model \
        --variable $variable \
        --attribute katz \
        --device 0 \
        --calibrate
    done
done
