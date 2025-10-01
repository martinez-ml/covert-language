
# Language Prejudice Prejudice in Language Models




## Overview

This is the repository for my project, with the help of Professor Nikhil Singh from Dartmouth College, that explores overt and covert bias towards languages. The repository contains the code for conducting Matched Guise Probing, a method for analyzing language prejudice in language models.


## Setup

All requirements can be found in `requirements.txt`. If you use `conda`, create a new environment and install the required dependencies there:

```
conda create -n dialect-prejudice python=3.10
conda activate dialect-prejudice
git clone https://github.com/valentinhofmann/dialect-prejudice.git
cd dialect-prejudice
pip install -r requirements.txt
```

## Usage

Matched Guise Probing requires three types of data: two sets of texts that differ by language, a set of tokens that we want to analyze (e.g., trait adjectives), and a set of prompts. Put the two sets of texts as a tab-separated text file into `data/pairs`. Put the set of tokens as a text file into `data/attributes`. `data/attributes` contains several example files (e.g., the trait adjectives from the Princeton Trilogy used in the paper). Finally, define the set of prompts in `probing/prompting.py`. `probing/prompting.py` contains all prompts used.

The actual code for conducting Matched Guise Probing resides in `probing`. Simply run the following command:

```
python3.10 mgp.py \
--model $model \
--variable $variable \
--attribute $attribute \
--device $device
```

The meaning of the individual arguments is as follow:

- `$model` is the name of the model being used (e.g., `t5-large`).
- `$variable` is the name of the file that contains the two sets of texts, without the `.txt` extension.
- `$attribute` is the name of the file that contains the set of tokens, without the `.txt` extension.
- `$device` specifies the device on which to run the code.



## Citation

Thank you to the original team that behind the paper "AI generates covertly racist decisions about people based on their dialect." I used their repo and made changes suited for language tests.

Hofmann, V., Kalluri, P. R., Jurafsky, D., & King, S. (2024). AI generates covertly racist decisions about people based on their dialect. Nature, 633(633), 1–8. https://doi.org/10.1038/s41586-024-07856-5


## Questions

Have any question? Feel free to email me at cs.martinez22@outlook.com