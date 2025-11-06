import glob
import os
import pickle

import numpy as np
import pandas as pd

import ratings

# Define path to attribute lists
ATTRIBUTES_PATH = os.path.abspath("../data/attributes/{}.txt")

# Define path to variables
VARIABLES_PATH = os.path.abspath("../data/pairs/{}.txt")

# Define path to continuation probabilities
PROBS_PATH = os.path.abspath("../scripts/probs/")

# Define path to perplexity values
PPLS_PATH = os.path.abspath("../perplexity/ppls/")

# Define model groups
NEW_MODELS = [#"google/gemma-2b", 
              "meta-llama-Meta-Llama-3-8B", 
              #"deepseek-ai/deepseek-llm-7b-base", "microsoft/Phi-4-reasoning"
              ]

GEMMA_MODELS = ["google/gemma-2b"]
LLAMA3_MODELS = ["meta-llama-Meta-Llama-3-8B"]
DEEPSEEK_MODELS = ["deepseek-ai/deepseek-llm-7b-base"]
PHI_MODELS = ["microsoft/Phi-4-reasoning"]

NEW_MODEL_PRETTY = {
    "google/gemma-2b": "Gemma 2B",
    "meta-llama-Meta-Llama-3-8B": "Llama 3 (8B)",
    "deepseek-ai/deepseek-llm-7b-base": "DeepSeek LLM 7B (base)",
    "microsoft/Phi-4-reasoning": "Phi-4 (reasoning)",
}

FAMILIES = [#"gemma", 
            "llama3",
              #"deepseek", "phi4"
              ]
PRETTY_FAMILIES = ["Gemma", "Llama 3", "DeepSeek", "Phi-4"]

MODELS = NEW_MODELS
PRETTY_MODELS = [NEW_MODEL_PRETTY[m] for m in NEW_MODELS]

# Define variable groups
UNPOOLED_VARIABLES = [
    'spa_Latn',
    'spanish',
    'arabic',
    'arb_Arab',
    'en-ar_combined',
    'output2',
    'output',
]
POOLED_VARIABLES = ["blodgett"]


def model2model_size(model):
    model_sizes = {
        "google/gemma-2b": 2e9,
        "meta-llama-Meta-Llama-3-8B": 8e9,
        "deepseek-ai/deepseek-llm-7b-base": 7e9,
        "microsoft/Phi-4-reasoning": 70e9,
    }
    return model_sizes[model]


def size2class(size):
    if size <= 150e6:
        return "small"
    elif size <= 350e6:
        return "medium"
    elif size <= 10e9:
        return "large"
    else:
        return "xl"


def model2family(model):
    if model in GEMMA_MODELS:
        return "gemma"
    if model in LLAMA3_MODELS:
        return "llama3"
    if model in DEEPSEEK_MODELS:
        return "deepseek"
    if model in PHI_MODELS:
        return "phi4"    

def pretty_model2family(model):
    if model in GEMMA_MODELS:
        return "gemma"
    if model in LLAMA3_MODELS:
        return "llama3"
    if model in DEEPSEEK_MODELS:
        return "deepseek"
    if model in PHI_MODELS:
        return "phi4"    


def family2models(family):
    if family == "gemma":
        return GEMMA_MODELS
    elif family == "llama3":
        return LLAMA3_MODELS
    elif family == "deepseek":
        return DEEPSEEK_MODELS
    elif family == "phi4":
        return PHI_MODELS

    

def family2pretty_models(family):
    if family == "gemma":
        return GEMMA_MODELS
    elif family == "llama3":
        return LLAMA3_MODELS
    elif family == "deepseek":
        return DEEPSEEK_MODELS
    elif family == "phi4":
        return PHI_MODELS


def pretty_family(family):
    pretty_dict = {
        "gemma": "Gemma",
        "llama3": "Llama 3",
        "deepseek": "DeepSeek",
        "phi4": "Phi-4",
    }
    return pretty_dict[family]


def pretty_model(family, size):
    if family == "gpt3" or family == "gpt4":
        return pretty_family(family)
    return "{} ({})".format(pretty_family(family), size)


def model2size(model):
    if model == "gpt2":
        return "base"
    elif model == "gpt3" or model == "gpt4":
        return "xl"
    else:
        return model.split("-")[-1]


def results2df(
    prompt_results, 
    attributes, 
    model, 
    variable, 
    match=False
):
    if model == "gpt4":
        return results2df_gpt4(
            prompt_results, attributes, variable, match
        )
    if model == "gpt3":
        logprob = True
    else:
        logprob = False
    if variable in UNPOOLED_VARIABLES:
        results_df = results2df_unpooled(
            prompt_results, 
            attributes,
            model, 
            variable, 
            logprob, 
            match
        )
    elif variable in POOLED_VARIABLES:
        results_df = results2df_pooled(
            prompt_results, 
            attributes, 
            model, 
            variable, 
            logprob, 
            match
        )
    return results_df.groupby([
        "attribute", "prompt", "size", "family", "model", "variable"
    ], as_index=False)["ratio"].mean()


def results2df_unpooled(
    prompt_results, 
    attributes, 
    model, 
    variable, 
    logprob=False, 
    match=False
):
    ratio_list = []
    for prompt, result_list in prompt_results.items():
        if match:
            attributes_prompt = [
                a for a in attributes if is_match(prompt, a)
            ]
        else:
            attributes_prompt = attributes
        for a_idx in range(len(attributes_prompt)):  # Loop over attributes
            for i in range(0, len(result_list), 2):
                if logprob:
                    prob_aave = np.exp(result_list[i][3][a_idx])
                    prob_sae = np.exp(result_list[i+1][3][a_idx])
                else:
                    prob_aave = result_list[i][3][a_idx]
                    prob_sae = result_list[i+1][3][a_idx]

                with np.errstate(divide='ignore', invalid='ignore'):
                    ratio = np.log10(np.divide(prob_aave, prob_sae))
                ratio_list.append((
                    ratio, # Probability change for trait
                    result_list[i+1][0], # Variable word/tweet (given in standard form)
                    attributes_prompt[a_idx], # Attribute
                    prompt, # Prompt
                    model2size(model),
                    model2family(model),
                    pretty_model(model2family(model), model2size(model)),
                    variable
                ))
    return pd.DataFrame(
        ratio_list, 
        columns=[
            "ratio", 
            "example", 
            "attribute", 
            "prompt", 
            "size", 
            "family", 
            "model", 
            "variable"
        ]
    )


def results2df_pooled(
    prompt_results, 
    attributes, 
    model, 
    variable, 
    logprob=False, 
    match=False
):
    ratio_list = []
    for prompt, result_list in prompt_results.items():
        if match:
            attributes_prompt = [
                a for a in attributes if is_match(prompt, a)
            ]
        else:
            attributes_prompt = attributes
        for a_idx in range(len(attributes_prompt)):  # Loop over attributes
            aave_probs, sae_probs = [], []
            for i in range(len(result_list)):  # Pool AAVE and SAE examples for prompt
                if logprob:
                    prob = np.exp(result_list[i][3][a_idx])
                else:
                    prob = result_list[i][3][a_idx]
                if result_list[i][1] == "aave":
                    aave_probs.append(prob)
                else:
                    sae_probs.append(prob)
            aave_prob = np.mean(aave_probs)  # Compute pooled probability for AAVE examples
            sae_prob = np.mean(sae_probs)  # Compute pooled probability for SAE examples
            ratio_list.append((
                np.log10(aave_prob / sae_prob),  # Probability change for trait
                attributes_prompt[a_idx],  # Attribute
                prompt,  # Prompt
                model2size(model), 
                model2family(model), 
                pretty_model(model2family(model), model2size(model)),
                variable
            ))
    return pd.DataFrame(
        ratio_list, 
        columns=[
            "ratio", 
            "attribute", 
            "prompt", 
            "size", 
            "family", 
            "model", 
            "variable"
        ]
    )


def results2df_gpt4(
    prompt_results, 
    attributes, 
    variable, 
    match=False
):
    attributes = [a for a in attributes if a != "legislator"]  # "legislator" not in GPT-4 vocabulary
    results_data = []
    for prompt, result_list in prompt_results.items():
        if match:
            prompt_attributes = [
                a for a in attributes if is_match(prompt, a)
            ]
        else:
            prompt_attributes = attributes
        aae_weights = {a: 0 for a in prompt_attributes}
        sae_weights = {a: 0 for a in prompt_attributes}
        for i in range(0, len(result_list), 2):

            # AAE
            aae_attributes = [
                a.strip() for a in result_list[i][2] if a.strip() in prompt_attributes
            ]
            aae_probs = [
                np.exp(l_p) for a, l_p in zip(
                    result_list[i][2], 
                    result_list[i][3]
                ) if a.strip() in prompt_attributes
            ]
            aae_attribute2prob = dict(zip(aae_attributes, aae_probs))
            aae_prob_rest = (
                (1 - sum(aae_probs)) / 
                (len(prompt_attributes) - len(aae_attributes))
            )

            for a in prompt_attributes:
                if a in aae_attribute2prob:
                    aae_weights[a] = aae_weights[a] + aae_attribute2prob[a]
                else:
                    aae_weights[a] = aae_weights[a] + aae_prob_rest

            # SAE
            sae_attributes = [
                a.strip() for a in result_list[i+1][2] if a.strip() in prompt_attributes
            ]
            sae_probs = [
                np.exp(l_p) for a, l_p in zip(
                    result_list[i+1][2], 
                    result_list[i+1][3]
                ) if a.strip() in prompt_attributes
            ]
            sae_attribute2prob = dict(zip(sae_attributes, sae_probs))
            sae_prob_rest = (
                (1 - sum(sae_probs)) / 
                (len(prompt_attributes) - len(sae_attributes))
            )

            for a in prompt_attributes:
                if a in sae_attribute2prob:
                    sae_weights[a] = sae_weights[a] + sae_attribute2prob[a]
                else:
                    sae_weights[a] = sae_weights[a] + sae_prob_rest
            
        for a in aae_weights:
            results_data.append((
                prompt,
                variable,
                "gpt4",
                "GPT4",
                "xl",
                a,
                np.log10(aae_weights[a] / sae_weights[a])
            ))
    return pd.DataFrame(
        results_data,
        columns=[
            "prompt", 
            "variable", 
            "family", 
            "model", 
            "size", 
            "attribute", 
            "ratio"
        ]
    )


def results2predictions(
    prompt_results, 
    attributes, 
    attribute_a, 
    attribute_b, 
    model, 
    variable
):
    if model == "gpt4":
        return results2predictions_gpt4(
            prompt_results, 
            variable
        )
    predictions_list = []
    for prompt, result_list in prompt_results.items():
        for i in range(len(result_list)):
            values = result_list[i][3]
            value_a = values[attributes.index(attribute_a)]
            value_b = values[attributes.index(attribute_b)]
            if value_a > value_b:
                prediction = attribute_a
            else:
                prediction = attribute_b
            predictions_list.append((
                prediction,  # Prediction
                result_list[i][1],  # Dialect
                prompt,  # Prompt
                model2size(model), 
                model2family(model), 
                pretty_model(model2family(model), model2size(model)),
                variable
            ))
    return pd.DataFrame(
        predictions_list, 
        columns=[
            "prediction", 
            "dialect", 
            "prompt", 
            "size", 
            "family", 
            "model", 
            "variable"
        ]
    )


def results2predictions_gpt4(
    prompt_results, 
    variable, 
    model="gpt4"
):
    predictions_list = []
    for prompt, result_list in prompt_results.items():
        for i in range(len(result_list)):
            attributes = [a.strip() for a in result_list[i][2]]
            values = result_list[i][3]
            max_idx = values.index(max(values))
            prediction = attributes[max_idx]
            predictions_list.append((
                prediction,  # Prediction
                result_list[i][1],  # Dialect
                prompt,  # Prompt
                model2size(model), 
                model2family(model), 
                pretty_model(model2family(model), model2size(model)),
                variable
            ))
    return pd.DataFrame(
        predictions_list, 
        columns=[
            "prediction", 
            "dialect", 
            "prompt", 
            "size", 
            "family", 
            "model", 
            "variable"
        ]
    )


def precision(attributes_pred, attributes_true):
    attributes_pred = set(attributes_pred)
    attributes_true = set(attributes_true)
    return len(attributes_pred & attributes_true) / len(attributes_pred)


def average_precision(attributes_ranked, attributes_true):
    precisions = []
    for i in range(len(attributes_ranked)):
        if attributes_ranked[i] in attributes_true:
            precisions.append(precision(attributes_ranked[:i+1], attributes_true))
    return sum(precisions) / len(attributes_true)


def predictions2difs(
    predictions_df, 
    dialect_a, 
    dialect_b
):
    grouped = predictions_df.groupby([
        "prediction", 
        "dialect", 
        "prompt", 
        "size", 
        "family", 
        "model", 
        "variable"
    ])
    prediction_counts = grouped.size().reset_index(name="count")
    difs_df = pd.merge(
        prediction_counts[prediction_counts.dialect==dialect_a],
        prediction_counts[prediction_counts.dialect==dialect_b],
        on=[
            "prediction", 
            "prompt", 
            "size", 
            "family", 
            "model", 
            "variable"
        ], 
        suffixes=("_a", "_b")
    )
    difs_df["dif"] = (difs_df["count_a"] / difs_df["count_b"]) - 1
    return difs_df


def load_ppls(model, variable):
    with open(f"{PPLS_PATH}{os.path.sep}{model}_{variable}.p", "rb") as f:
        ppls = pickle.load(f)
    return ppls


def load_ratings(ratings_name):
    if ratings_name == "katz":
        attributes = ratings.ATTRIBUTES_KATZ
        scores = ratings.SCORES_KATZ
    elif ratings_name == "gilbert":
        attributes = ratings.ATTRIBUTES_GILBERT
        scores = ratings.SCORES_GILBERT
    elif ratings_name == "karlins":
        attributes = ratings.ATTRIBUTES_KARLINS
        scores = ratings.SCORES_KARLINS
    elif ratings_name == "bergsieker":
        attributes = ratings.ATTRIBUTES_BERGSIEKER
        scores = ratings.SCORES_BERGSIEKER
    assert len(attributes) == len(scores)
    attribute2score = dict(zip(attributes, scores))
    return attribute2score


def load_favorability_ratings():
    attributes = ratings.ATTRIBUTES_ALL
    favorabilities = ratings.FAVORABILITIES_ALL
    assert len(attributes) == len(favorabilities)
    attribute2favorability = dict(zip(attributes, favorabilities))
    return attribute2favorability


def mean_favorability(
    attributes, 
    attribute2favorability, 
    weights=None
):
    if weights is None:
        return np.mean([attribute2favorability[a] for a in attributes])
    else:
        return (
            sum([attribute2favorability[a] * w for a, w in zip(attributes, weights)]) / 
            sum(weights)
        )


def get_top_attributes(
    attributes, 
    attribute2score, 
    k
):
    sorted_attributes = sorted(
        [a for a in attributes if a in attribute2score], 
        key=lambda x: attribute2score[x],
        reverse=True
    )
    return sorted_attributes[:k]


def attribute2class(attribute, stereo_attributes):
    if attribute in stereo_attributes:
        return "stereo"
    else:
        return "general"
    

def is_match(prompt, attribute):
    vowel = ("a", "e", "i", "o", "u")
    if attribute.startswith(vowel) and (" a " in prompt or prompt.endswith(" a")):
        return False
    elif not attribute.startswith(vowel) and (" an " in prompt or prompt.endswith(" an")):
        return False
    return True


def load_results(
    model, 
    variable, 
    attribute_name, 
    calibrate=False
):
    if model == "gpt3" or model == "gpt3-davinci":
        return load_results_distributed(
            model=model, 
            variable=variable, 
            attribute_name=attribute_name, 
            calibrate=calibrate
        )
    if calibrate:
        with open(f"{PROBS_PATH}{os.path.sep}{model}_{variable}_{attribute_name}_cal.p", "rb") as f:
            prompt_results = pickle.load(f)
    else:
        with open(f"{PROBS_PATH}{os.path.sep}{model}_{variable}_{attribute_name}.p", "rb") as f:
            prompt_results = pickle.load(f)
    return prompt_results


def load_results_distributed(
    model, 
    variable, 
    attribute_name, 
    calibrate=False
):
    if calibrate:
        files = sorted(glob.glob(
            f"{PROBS_PATH}{os.path.sep}{model}_{variable}_{attribute_name}_cal_[0-9]*.p"
        ))
    else:
        files = sorted(glob.glob(
            f"{PROBS_PATH}{os.path.sep}{model}_{variable}_{attribute_name}_[0-9]*.p"
        ))
    prompt_results = {}
    for file in files:
        with open(file, "rb") as f:
            prompt_results_file = pickle.load(f)
        for prompt in prompt_results_file:
            if prompt in prompt_results:
                prompt_results[prompt].extend(prompt_results_file[prompt])
            else:
                prompt_results[prompt] = prompt_results_file[prompt]
    return prompt_results


def load_attributes(attribute_name):
    with open(ATTRIBUTES_PATH.format(attribute_name), "r") as f:
        attributes = f.read().strip().split("\n")
    return attributes


def get_dif(results_a, results_b):
    dif_mean = results_b.ratio.mean() - results_a.ratio.mean()
    return dif_mean


def get_occupation_ratings(occupations):
    occupation2rating = {
        o.strip().lower(): r for o, r in zip(
            ratings.GSS_OCCUPATIONS, 
            ratings.GSS_PRESTIGE_RATINGS
        )
    }
    o2r = {}
    for o in occupations:
        if o in occupation2rating:
            o2r[o] = occupation2rating[o]
        rs = []
        for o_ in occupation2rating:
            if o_.startswith(o) or o_.endswith(o):
                rs.append(occupation2rating[o_])
        if len(rs) > 0:
            o2r[o] = np.mean(rs)
    return o2r
