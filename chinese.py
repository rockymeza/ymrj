# Very loosely based on
# http://www.iplaypy.com/code/base/b2600.html
#
# Definitely incomplete
import itertools

CN_NUM = {
  '〇': 0,
  '一': 1,
  '二': 2,
  '三': 3,
  '四': 4,
  '五': 5,
  '六': 6,
  '七': 7,
  '八': 8,
  '九': 9,

  '零': 0,
  '壹': 1,
  '贰': 2,
  '叁': 3,
  '肆': 4,
  '伍': 5,
  '陆': 6,
  '柒': 7,
  '捌': 8,
  '玖': 9,

  '貮': 2,
  '两': 2,
}

CN_UNIT = {
  '十': 10,
  '拾': 10,
  '百': 100,
  '佰': 100,
  '千': 1000,
  '仟': 1000,
  '万': 10000,
  '萬': 10000,
  '亿': 100000000,
  '億': 100000000,
  # '兆': 1000000000000,
}

CN_DIGITS = ''.join(itertools.chain(CN_NUM.keys(), CN_UNIT.keys()))


def get_unit(buffer):
    if buffer[0] in CN_UNIT:
        return CN_UNIT[buffer.pop(0)]


def group(input):
    tmp = 0
    buffer = list(input)

    while buffer:
        digit = buffer.pop(0)
        if digit in CN_UNIT:
            unit = CN_UNIT[digit]
            if unit >= 10000:
                yield tmp, unit
                tmp = 0
            else:
                tmp += CN_UNIT[digit]
        elif buffer:
            unit = get_unit(buffer)
            if unit is None:
                tmp += CN_NUM[digit]
            elif unit >= 10000:
                tmp += CN_NUM[digit]
                yield tmp, unit
                tmp = 0
            else:
                tmp += CN_NUM[digit] * unit
        else:
            tmp += CN_NUM[digit]

    yield tmp, 1


def cn2int(input):
    ret = 0

    for group_value, group_unit in group(input):
        ret += group_value * group_unit

    return ret
