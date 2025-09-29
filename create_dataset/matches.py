import os
"""
    Goes through the OpenSubtitles files for the specified language pairs,
    and finds sentences that have perfect matches across all languages.

 """
PAIR_FOLDERS = [
    'ar-en.txt', 'en-es.txt', 'en-fr.txt', 'en-he.txt', 'en-ja.txt', 'en-zh.txt'
]
PAIR_CODES = [f.replace('.txt', '').split('-') for f in PAIR_FOLDERS]
ALL_LANGS = [p[0] if p[0] != 'en' else p[1] for p in PAIR_CODES]
JAPAN_IDX = ALL_LANGS.index('ja')
REQUIRED_PAIRS = 1000

def get_eng_offsets(folder, code):
    lang_pair = folder.replace('.txt', '')
    en_path = os.path.join(folder, f'OpenSubtitles.{lang_pair}.en')
    fo_path = os.path.join(folder, f'OpenSubtitles.{lang_pair}.{code}')
    offset_dict = {}
    with open(en_path, encoding='utf-8') as en_f, open(fo_path, encoding='utf-8') as fo_f:
        pos = 0
        while True:
            en_line = en_f.readline()
            fo_line = fo_f.readline()
            if not en_line:
                break
            en_clean = en_line.strip()
            if not en_clean or en_clean == "-":
                pos += 1
                continue
            # Only record the first occurrence of each unique sentence for efficiency
            if en_clean not in offset_dict:
                offset_dict[en_clean] = pos
            pos += 1
    return offset_dict

def get_foreign_at(folder, code, offset):
    lang_pair = folder.replace('.txt', '')
    fo_path = os.path.join(folder, f'OpenSubtitles.{lang_pair}.{code}')
    with open(fo_path, encoding='utf-8') as fo_f:
        for i, line in enumerate(fo_f):
            if i == offset:
                return line.strip()
    return None  # Fallback, should not be needed if offset is correct

def main():
    print("Building English->line indexes for all languages except Japanese...")
    eng_offset_dicts = []
    for idx, (folder, lang) in enumerate(zip(PAIR_FOLDERS, ALL_LANGS)):
        if lang == 'ja':
            eng_offset_dicts.append(None)
            continue
        print(f"  {lang}: {folder}")
        eng_offset_dicts.append(get_eng_offsets(folder, lang))
    
    # Now scan Japanese file line by line.
    print("Scanning Japanese lines and matching for all languages...")
    ja_folder = PAIR_FOLDERS[JAPAN_IDX]
    ja_pair = ja_folder.replace('.txt', '')
    ja_en_path = os.path.join(ja_folder, f'OpenSubtitles.{ja_pair}.en')
    ja_fo_path = os.path.join(ja_folder, f'OpenSubtitles.{ja_pair}.ja')

    out_fhs = {}
    out_dir = "combined_output"
    os.makedirs(out_dir, exist_ok=True)
    for idx, lang in enumerate(ALL_LANGS):
        out_file = os.path.join(out_dir, f"en-{lang}_combined.txt")
        out_fhs[lang] = open(out_file, 'w', encoding='utf-8')

    num_written = 0

    with open(ja_en_path, encoding='utf-8') as je, open(ja_fo_path, encoding='utf-8') as jf:
        for ja_offset, (en_line, ja_line) in enumerate(zip(je, jf)):
            en_clean = en_line.strip()
            if not en_clean or en_clean == "-":
                continue

            match_offsets = []
            for idx, (eng_offsets, lang) in enumerate(zip(eng_offset_dicts, ALL_LANGS)):
                if lang == 'ja':
                    match_offsets.append(ja_offset)
                    continue
                # Not present as a translation in this language
                offset = eng_offsets.get(en_clean)
                if offset is None:
                    break
                match_offsets.append(offset)
            else:  # All languages matched; write out
                # For each language, get the foreign translation at offset
                for idx, (folder, code, offset, lang) in enumerate(zip(PAIR_FOLDERS, ALL_LANGS, match_offsets, ALL_LANGS)):
                    lang_pair = folder.replace('.txt', '')
                    fo_path = os.path.join(folder, f'OpenSubtitles.{lang_pair}.{code}')
                    with open(fo_path, encoding='utf-8') as f_f:
                        # Seek to offset
                        for i, line in enumerate(f_f):
                            if i == offset:
                                foreigntxt = line.strip()
                                out_fhs[lang].write(f"{foreigntxt}\t{en_clean}\n")
                                break
                num_written += 1

                if num_written % 100 == 0:
                    print(f"Wrote {num_written} lines...")
                if num_written == REQUIRED_PAIRS:
                    break

    for fh in out_fhs.values():
        fh.close()
    print(f"\nDone! Wrote {num_written} perfectly aligned pairs to {out_dir}")

if __name__ == "__main__":
    main()