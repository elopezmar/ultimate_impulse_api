def dict_to_dot_notation(d, prefix=None):
    dic_doted = {}
    for k in d:
        if isinstance(d[k], dict):
            p = f'{prefix}.{k}' if prefix else k
            dic_doted.update(dict_to_dot_notation(d[k], p))
        else:
            dic_doted[f'{prefix}.{k}' if prefix else k] = d[k]
    return dic_doted