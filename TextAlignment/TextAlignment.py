# -*-coding:utf-8-*-


word_list_tuple = []

def  getwordtuple(en_path, zh_path):
    zh_file = open(zh_path)
    en_file = open(en_path)
    zh_line_list = zh_file.readlines()
    en_line_list = en_file.readlines()
    i = 0
    linetuple = []
    while i < len(zh_line_list):
        linetuple.append((zh_line_list[i], en_line_list[i]))
        i += 1
    wordtuple = []
    for _tuple in linetuple:
        ls1, ls2 = [], []
        zh_line = _tuple[0].rstrip()
        zh_word_list = zh_line.split(" ")
        for zh_word in zh_word_list:
            if zh_word == "，" or zh_word == "：" or zh_word == "；" or zh_word == '"' or zh_word == "？" or zh_word == "。" or zh_word == "！" or zh_word == "、" or zh_word == '':
                zh_word_list.remove(zh_word)
        en_line = _tuple[1].rstrip()
        en_word_list = en_line.split(" ")
        for en_word in en_word_list:
            if en_word == "." or en_word == '"' or en_word == "?" or en_word == "," or en_word == "!" or en_word == "-" or en_word == '':
                en_word_list.remove(en_word)
        for word in  en_word_list:
            word = word.rstrip('"')
            word = word.rstrip('.')
            word = word.rstrip('?')
            word = word.rstrip(',')
            if word == '':
                continue
            ls2.append(word)
        for new_zh_word in zh_word_list:
            new_zh_word = new_zh_word.rstrip('"')
            new_zh_word = new_zh_word.rstrip("。")
            new_zh_word = new_zh_word.rstrip("，")
            new_zh_word = new_zh_word.rstrip("？")
            new_zh_word = new_zh_word.rstrip("；")
            new_zh_word = new_zh_word.rstrip("：")
            new_zh_word = new_zh_word.rstrip("、")
            if new_zh_word == '':
                continue
            ls1.append(new_zh_word)
            for new_en_word in en_word_list:
                new_en_word = new_en_word.rstrip('"')
                new_en_word = new_en_word.rstrip('.')
                new_en_word = new_en_word.rstrip('?')
                new_en_word = new_en_word.rstrip(',')
                if new_en_word == '':
                    continue
                wordtuple.append((new_zh_word, new_en_word))
        word_list_tuple.append((ls1, ls2))

    # for key in wordtuple:
    #     print(key)
    # print(len(wordtuple))
    zh_file.close()
    en_file.close()
    return wordtuple

def getT(wordtuple):
    newwordtuple = list(set(wordtuple))
    k = 50
    t = {}
    single_total = {}
    pair_total = {}
    for key in newwordtuple:
        t[key] = 0.25
        single_total[key[1]] = 0
        pair_total[key] = 0
    for key in wordtuple:
        single_total[key[1]] +=1
        pair_total[key] += 1
    for key in newwordtuple:
        t[key] = pair_total[key] / single_total[key[1]]


    while k > 0:
        total = {}
        for key in newwordtuple:
            total[key[0]] = 0
        for key in wordtuple:
            total[key[0]] += t[key]
        for key in newwordtuple:
            pair_total[key] += t[key] / total[key[0]]
            single_total[key[1]] += t[key]/ total[key[0]]
        for key in newwordtuple:
            t[key] = pair_total[key] / single_total[key[1]]
        k = k - 1
        # s_total, total, count = {}, {}, {}
        # for key in newwordtuple:
        #     count[key] = 0
        #     s_total[key[1]] = 0
        #     total[key[0]] = 0
        # for key in wordtuple:
        #     s_total[key[1]] += t[key]
        # for key in wordtuple:
        #     total[key[0]] += t[key] / s_total[key[1]]
        #     count[key] += t[key] / s_total[key[1]]
        # for key in newwordtuple:
        #     t[key] = count[key] / total[key[0]]
        # k = k - 1
    for key in newwordtuple:
        print(key, end='')
        print(":", end='')
        print(t[key])
    print()
    print()
    print()
    return t

def getoptimalalignment(t, word_list_tuple):
    optimalalignment = {}
    bigestprobability = []
    bigestprobability.append(0)
    for _tuple in word_list_tuple:
        alignment_list, result, = [], [],
        i = 0
        while i < len(_tuple[0]):
            alignment_list.append(0)
            result.append(0)
            i += 1
        bigestprobability[0] = 0
        recursion(t, _tuple[0], 0, _tuple[1], alignment_list, 1, bigestprobability, result)
        optimalalignment[str(_tuple[0] + _tuple[1])] = result
    return optimalalignment



def recursion(t, zh_word_list, position, en_word_list, alignment_list, probability, bigestprobability, result):
    if position == len(zh_word_list):
        if probability > bigestprobability[0]:
            bigestprobability[0] = probability
            i = len(alignment_list) - 1
            while i >= 0:
                result[i] = alignment_list[i]
                i -= 1
    else:
        j = 0
        while j < len(en_word_list):
            alignment_list[position] = j
            newprobability = t[(zh_word_list[position], en_word_list[j])] * probability
            recursion(t, zh_word_list, position + 1, en_word_list, alignment_list, newprobability, bigestprobability, result)
            j += 1


enpath = "/Users/renhaoran/PycharmProjects/MachineTranslation/TextAlignment/testEN.txt"
zhpath = "/Users/renhaoran/PycharmProjects/MachineTranslation/TextAlignment/testZH.txt"
wordtuple = getwordtuple(enpath, zhpath)
print(word_list_tuple)
t = getT(wordtuple)
x = getoptimalalignment(t, word_list_tuple)
print(x)


