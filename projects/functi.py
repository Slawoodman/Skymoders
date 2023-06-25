def pretyoutput(lst):
    res = []
    for i in lst:
        tmp = {}
        for key, value in i.items():
            if key == "description" and len(value) >= 50:
                value = f'{".".join(value.split(".")[:-1])}...'
                print(key, value)
            tmp.setdefault(key, value)
        res.append(tmp)
    return res
