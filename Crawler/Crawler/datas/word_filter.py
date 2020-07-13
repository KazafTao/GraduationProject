final = []

with open("./asciiKeyword.txt", "r", encoding='utf-8') as f:
    for tag in f.readlines():
        tag = tag.strip()
        if tag:
            final.append(tag)

with open("./hotwords.txt", "r", encoding="utf-8") as hotwords:
    for word in hotwords.readlines():
        final.append(word.strip())

final = list(set(final))

with open("./final.txt", "w", encoding='utf-8') as f:
    for word in final:
        f.writelines(word + '\n')

with open("./final.txt", "r", encoding='utf-8') as f:
    for word in f.readlines():
        print(word)
