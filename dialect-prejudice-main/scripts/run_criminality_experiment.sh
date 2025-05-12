#!/bin/bash

parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"

for model in deepseek-ai/deepseek-llm-7b-base meta-llama/Meta-Llama-3-8B
do
    for variable in arb_Arab fra_Latn heb_Hebr jpn_Jpan spa_Latn zho_Hans
    do
        python3.10 -u ../probing/mgp.py \
        --model $model \
        --variable $variable \
        --attribute penalty \
        --calibrate \
        --device 0
    done

done

for model in meta-llama/Meta-Llama-3-8B deepseek-ai/deepseek-llm-7b-base
do
    for variable in arb_Arab fra_Latn heb_Hebr jpn_Jpan spa_Latn zho_Hans
    do
        python3.10 -u ../probing/mgp.py \
        --model $model \
        --variable $variable \
        --attribute guilt \
        --calibrate \
        --device 0
    done

done
