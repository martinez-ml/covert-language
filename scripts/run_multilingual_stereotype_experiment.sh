#!/bin/bash

parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"
#arb_Arab fra_Latn heb_Hebr jpn_Jpan rus_Cyrl spa_Latn zho_Hans
#arabic chinese french hebrew japanese russian spanish
#google/gemma-2b deepseek-ai/deepseek-llm-7b-base meta-llama/Meta-Llama-3-8B

declare -A lang_map
lang_map["arb_Arab"]="arabic"
lang_map["fra_Latn"]="french"
lang_map["jpn_Jpan"]="japanese"
lang_map["spa_Latn"]="spanish"
lang_map["zho_Hans"]="chinese"
lang_map["heb_Hebr"]="hebrew"
lang_map["hebrew"]="hebrew"
lang_map["arabic"]="arabic"
lang_map["chinese"]="chinese"
lang_map["french"]="french"
lang_map["japanese"]="japanese"
lang_map["spanish"]="spanish"

for model in google/gemma-2b microsoft/Phi-4-reasoning
    do
    for variable in arb_Arab fra_Latn jpn_Jpan heb_Hebr spa_Latn zho_Hans arabic_translated chinese_translated french_translated japanese_translated spanish_translated hebrew_translated
    do
        lang=${lang_map[$variable]}
        katz_attribute="katz_${lang}"
        python -u ../probing/mgp_multilingual.py \
        --model $model \
        --variable $variable \
        --attribute $katz_attribute \
        --device 0 \
        --calibrate
    done
done
