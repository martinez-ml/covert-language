#!/usr/bin/env python3
"""
export_one_per_lang.py

Downloads Muennighoff/flores200 (all languages) for the
combined dev+devtest splits and writes out one .txt file per
language where each line is:

    [sentence_in_foreign_lang]\t[sentence_in_English]\n
"""

import os
from datasets import load_dataset

def main():
    # The seven target languages
    languages = [
        "arb_Arab",
        "fra_Latn",
        "heb_Hebr",
        "spa_Latn",
        "jpn_Jpan",
        "rus_Cyrl",
        "zho_Hans"
    ]

    # Load dev + devtest in one go
    ds = load_dataset(
        "Muennighoff/flores200",
        "all",
        split="dev+devtest"    # combine both splits
    )
    print(f"Loaded dev+devtest: {len(ds)} examples total.")

    # Prepare output directory
    out_dir = "dev_devtest_onefile"
    os.makedirs(out_dir, exist_ok=True)

    # Open one file-handle per language
    handles = {}
    for lang in languages:
        fname = f"{lang}.txt"
        path = os.path.join(out_dir, fname)
        handles[lang] = open(path, "w", encoding="utf-8")
        print(f"→ Will write {lang} → {path}")

    # Iterate and write
    for ex in ds:
        eng = ex.get("sentence_eng_Latn")
        for lang in languages:
            foreign = ex.get(f"sentence_{lang}")
            if foreign and eng:
                handles[lang].write(f"{foreign}\t{eng}\n")

    # Close all files
    for lang, fh in handles.items():
        fh.close()

    print("Done! Files in folder:", out_dir)

if __name__ == "__main__":
    main()