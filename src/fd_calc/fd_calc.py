from itertools import combinations
from fd import FD
from pandas_reader import pandas_reader


def calc_final_dets(dets_collection):
    if len(dets_collection) == 0:
        return []
    elif len(dets_collection) == 1:
        return list(dets_collection[0].keys())
    min_overlap = set(dets_collection[0].keys())
    for i in range(1, len(dets_collection)):
        d = dets_collection[i]
        new_min_overlap = set()
        for key in d:
            if key in min_overlap:
                new_min_overlap.add(key)
        if len(new_min_overlap) == 0:
            return []
        if len(new_min_overlap) < len(min_overlap):
            min_overlap = new_min_overlap
    return list(min_overlap)


def calc_unique_fds(res):
    global fd_index
    global super_keys
    res_non_unique = {}
    for t in res:
        previous_rows = {}
        previous_vals = {}
        for _, row in data.iterrows():
            key_row = str([val for _, val in row.items()])
            if key_row in previous_rows:
                continue
            temp = []
            for elem in t:
                temp.append(row[elem])
            key = str(temp)
            if key in previous_vals:
                key_t = str(t)
                res_non_unique[key_t] = ""
                break
            previous_vals[key] = ""
            previous_rows[key_row] = ""

    res_unique = {}
    if len(res) > 0:
        for t in res:
            if str(t) not in res_non_unique:
                right_side = [attr for attr in attributes if attr not in t]
                fd = FD(t, right_side, True)
                res_unique[str(t)] = ""
                to_continue = False

                # if a previous superkey is subset of the new calculated superkey then ignore (redundant)
                for sup_key in super_keys:
                    nb_left_side = len(sup_key.left_side)
                    count = 0
                    for elem in sup_key.left_side:
                        if elem in fd.left_side:
                            count += 1
                    # print(count, l)
                    if count == nb_left_side:
                        to_continue = True
                        break
                if to_continue:
                    continue

                super_keys.append(fd)
                fd_index += 1
                print(f"({fd_index}) {fd.to_string()}")
    return res_unique


def calc_repeating_fds(res, res_unique):
    global fd_index
    global super_keys
    for temp in res:
        calc = {}
        previously_seen = {}
        str_temp = str(temp)
        if str_temp in res_unique:
            continue
        calc[str_temp] = {}
        for _, row in data.iterrows():
            # update(dict, row)
            vals = [str(row[elem]) for elem in temp]
            str_vals = str(vals)
            if "nan" in vals:
                continue
            for attr, val in row.items():
                str_val = str(val)

                if str_val == "nan":
                    continue

                str_attr = str(attr)
                if str_attr not in temp:
                    # print(attr, "not in", temp)
                    # update(calc, previously_seen, temp, vals, attr, val)
                    if str_vals not in calc[str_temp]:
                        calc[str_temp][str_vals] = {}
                    if str_attr not in calc[str_temp][str_vals]:
                        calc[str_temp][str_vals][str_attr] = {}
                    if str_val not in calc[str_temp][str_vals][str_attr]:
                        calc[str_temp][str_vals][str_attr][str_val] = 1
                    else:
                        calc[str_temp][str_vals][str_attr][str_val] += 1

            if str_temp not in previously_seen:
                previously_seen[str_temp] = {}
            if str_vals not in previously_seen[str_temp]:
                previously_seen[str_temp][str_vals] = 1
            else:
                previously_seen[str_temp][str_vals] += 1

        fds = {}

        for left_side in calc:
            dets_collection = []
            seen = {}
            was_empty = False
            for vals in calc[left_side]:
                dets = {}
                for attr in calc[left_side][vals]:
                    for val in calc[left_side][vals][attr]:
                        if (
                            calc[left_side][vals][attr][val]
                            == previously_seen[left_side][vals]
                        ):  # appeared same amount of times as the left side
                            dets[attr] = ""
                if len(dets) == 0:
                    was_empty = True
                    break
                else:
                    key_temp = str(sorted(dets))
                    if key_temp not in seen:
                        dets_collection.append(dets)
                        seen[key_temp] = ""
            if not was_empty:
                res_dets = calc_final_dets(dets_collection)
                if len(res_dets) > 0:
                    fds[left_side] = res_dets

        if len(fds) > 0:
            for left_side in fds:
                fd = FD(left_side, fds[left_side], False)
                fd_index += 1
                print(f"({fd_index}) {fd.to_string()}")


data = pandas_reader.read_pandas()

super_keys = []
fd_index = 0

attributes = list(data)
N = len(attributes)
# print(N)
for i in range(1, N):
    print("length of left side:", i)
    res = [comb for comb in combinations(attributes, i)]

    res_unique = calc_unique_fds(res)

    if len(res_unique) < len(res):
        calc_repeating_fds(res, res_unique)


# calculate candidate key
if len(super_keys) == 0:
    print("no candidate keys")
else:
    print("candidate keys")
    min_len = len(super_keys[0].left_side)
    for fd in super_keys:
        if len(fd.left_side) > min_len:
            break
        print(f"{fd.left_side}")
