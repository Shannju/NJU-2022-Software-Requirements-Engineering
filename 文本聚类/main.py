import xiangshi as xs

fn = 'qa.txt'
doc = []
with open(fn, 'r', encoding='utf-8') as f:
    for line in f.readlines():
        doc.append(line)

res = xs.kmeans(10, doc, WithKeys=True)
fn = 'data_.txt'
fn1 = 'center.txt'
idx0 = ''
with open(fn, 'w', encoding='utf-8') as f:
    for idx, sentence in res.items():
        if idx != idx0:
            idx0 = idx
            f.write('\n')
            with open(fn1, 'a', encoding='utf-8') as f1:
                f1.write(idx)
                f1.write('\n')
        for i in range(len(sentence)):
            f.write(sentence[i])
            f.write('\n')
