#!/usr/bin/env python3
import os, re
from datasets import load_dataset

def main():
    languages = [
      "arb_Arab","fra_Latn","heb_Hebr",
      "spa_Latn","jpn_Jpan","rus_Cyrl","zho_Hans"
    ]

    # load both splits at once
    ds = load_dataset("Muennighoff/flores200", "all", split="dev+devtest")
    out_root = "dev_devtest"
    os.makedirs(out_root, exist_ok=True)

    for lang in languages:
        lang_folder = os.path.join(out_root, lang)
        os.makedirs(lang_folder, exist_ok=True)

        handles = {}
        for ex in ds:
            foreign = ex.get(f"sentence_{lang}")
            english = ex.get("sentence_eng_Latn")
            topic   = ex.get("topic", "").strip()
            if not (foreign and english and topic):
                continue

            t = topic.lower()
            parts = re.split(r'[^0-9a-z]+', t)
            first = parts[0] if parts and parts[0] else "unknown"
            group = re.sub(r'[^0-9a-z\-_]', '_', first)

            if group not in handles:
                fpath = os.path.join(lang_folder, f"{group}.txt")
                handles[group] = open(fpath, "w", encoding="utf-8")

            handles[group].write(f"{foreign}\t{english}\n")

        for fh in handles.values():
            fh.close()

        print(f"Written {lang_folder}")

    print("All done.")

if __name__ == "__main__":
    main()