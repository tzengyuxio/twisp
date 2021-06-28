def minguo_to_ad(s):
    words = s.split("/")
    words[0] = str(int(words[0]) + 1911)
    return "-".join(words)
