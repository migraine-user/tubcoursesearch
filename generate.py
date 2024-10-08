from os import listdir
last_line = None
with open(f"output.csv", "w") as output_file:
    for file_name in listdir("fields"):
        with open(f"fields/{file_name}", "r") as file:
            for line in file:
                line = line.strip()
                if last_line:
                    line = last_line + " " + line
                    last_line = None
                if line.startswith("examination"):
                    continue
                words = [word.replace(",", "") for word in line.split()]
                for i, word in enumerate(words):
                    if word.isnumeric():
                        break
                else:
                    last_line = line
                    continue
                title = " ".join(words[:i])
                acc = []
                for word in words[i:]:
                    if word in ["ja", "1.0", "nein"] or word.isnumeric():
                        continue
                    acc.append(word)
                output_file.write(",".join([file_name[:-4], title, words[i], " ".join(acc)])+"\n")