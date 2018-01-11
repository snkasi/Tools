#!/usr/bin/python
# -*- coding: UTF-8 -*-


def wildcard(string, pattern):
    def _init(string):
        ret_list, ret_string = [], ''
        skip, num = False, 0
        for sub_string in string:
            if skip is True:
                skip = False
                ret_string += sub_string
            else:
                if sub_string == '\\':
                    skip = True
                else:
                    ret_string += sub_string
                    if sub_string in ['*', '?']:
                        ret_list.append(num)
                num += 1
        return ret_string, ret_list

    def _findall(string, sub_string):
        ret, num = [], 0
        while num <= len(string):
            fresult = string[num:].find(sub_string)
            if fresult == -1:
                return ret
            else:
                ret.append(fresult + num)
                num += fresult + 1
        return ret

    def _travel(list_list):
        ret, row = {}, 0
        while row >= 0 and row <= len(list_list):
            if row == len(list_list):
                yield [list_list[num][ret[num]] for num in range(len(ret))]
                row -= 1
            else:
                last_column = ret.get(row) if ret.get(row) is not None else -1
                ret[row], add = (last_column + 1, 1) if last_column + \
                    1 < len(list_list[row]) else (None, -1)
                row += add

    def _match(string, pattern, plist):
        begin, run_list, match_list = 0, [], []
        for sub_list in plist:
            run_list.append((pattern[begin:sub_list], pattern[sub_list]))
            match_list.append(_findall(string, pattern[begin:sub_list]))
            begin = sub_list + 1
        run_list.append((pattern[begin:], None))
        match_list.append(_findall(string, pattern[begin:]))
        for pat in _travel(match_list):
            is_ok = True
            num = 0
            if pat[num] != 0:
                continue
            if len(run_list) > 1:
                for num in range(1, len(run_list)):
                    extra = pat[num] - (len(run_list[num-1][0]) + pat[num-1])
                    if extra < 0 or run_list[num-1][1] == '?' and extra > 1 or run_list[num-1][1] is None and extra != 0:
                        is_ok = False
                        break
            extra = len(string) - (len(run_list[num][0]) + pat[num])
            if is_ok and extra == 0:
                return True
        return False

    format_string, format_list = _init(pattern)
    return _match(string, format_string, format_list)
