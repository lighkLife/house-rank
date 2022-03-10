from math import ceil

from mako.template import Template


class House:
    def __init__(self, number, level, direction, area, apartment, courtyard, total):
        self.number = number
        self.level = level
        self.direction = direction
        self.area = round(float(area))
        self.apartment = apartment == "true"
        self.courtyard = courtyard == "true"
        self.total = total
        self.score = self.compute_score()
        self.sort = 0
        self.red = 0
        self.green = 0
        self.blue = 0
        self.alpha = 0

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"number={self.number}, level={self.level}, direction={self.direction}, area={self.area}, apartment={self.apartment}" \
               + f"courtyard={self.courtyard}, total={self.total}, score={self.total}, score={self.score}, sort={self.sort}" + \
               f"red={self.red}, green={self.green}, blue={self.blue}, alpha={self.alpha}"

    def compute_score(self):
        return self.score_of_level() \
               + self.score_of_direction() \
               + self.score_of_area() \
               + self.score_of_apartment() \
               + self.score_of_courtyard()

    def score_of_level(self):
        level = int(self.level)
        score_map = {
            33: 0,
            32: 0,
            31: 20,
            30: 30,
            29: 40,
            28: 50,
            27: 70,
            26: 70,
            25: 80,
            24: 80,
            23: 80,
            22: 90,
            21: 90,
            20: 90,
            19: 100,
            18: 100,
            17: 100,
            16: 100,
            15: 100,
            14: 90,
            13: 90,
            12: 90,
            11: 90,
            10: 80,
            9: 80,
            8: 80,
            7: 80,
            6: 70,
            5: 40,
            4: 10,
            3: 0,
            2: 0
        }
        return score_map.get(level)

    def score_of_direction(self):
        if self.direction == '东':
            return 60
        elif self.direction == '南':
            return 80
        elif self.direction == '西':
            return 40
        elif self.direction == '北':
            return 10
        else:
            raise RuntimeError

    def score_of_area(self):
        area = round(float(self.area))
        if area == 108:
            return 90
        elif area == 115:
            return 100
        elif area == 131:
            return 60
        elif area == 132:
            return 60
        elif area == 138:
            return 80
        elif area == 137:
            return 80
        elif area == 139:
            return 80
        elif area == 140:
            return 70
        else:
            raise RuntimeError

    def score_of_apartment(self):
        if self.apartment:
            return 0
        else:
            return 100

    def score_of_courtyard(self):
        if self.courtyard:
            return 100
        else:
            return 50

    def score_of_total(self):
        return self.total


def read_file(name):
    data = []
    with open(name, "r", encoding='utf8') as f:
        for row in range(33):
            line = f.readline(200)
            if len(line) <= 0:
                continue
            level_map = {}
            for item in line.split("||"):
                content = item.replace("\n", "").replace("\r", "").replace(" ", "")
                if len(content) <= 0:
                    continue
                it = content.split(",")
                house = House(it[0], it[1], it[2], it[3], it[4], it[5], it[6])
                level_map[house.direction] = house
            data.append(level_map)
    return data


def write_file(name, html):
    with open(name, "w", encoding="utf8") as f:
        f.write(html)


def generate_html(data):
    template = Template(filename='template.html')
    return template.render(data=data)


def compute_color(data):
    size = 0

    score_list = []
    for building in data.values():
        for level in building:
            for house in level.values():
                size += 1
                score_list.append(house.score)
    score_set = list(set(score_list))
    score_set.sort(reverse=True)
    score_list.sort(reverse=True)

    first_index = int(ceil(len(score_list) * 0.3))
    second_index = int(ceil(len(score_list) * 0.6))

    for building in data.values():
        for level in building:
            for house in level.values():
                current_index = score_list.index(house.score)
                house.sort = score_set.index(house.score) + 1
                if house.score >= score_list[first_index]:
                    house.alpha = (first_index - current_index + 1) / float(first_index + 1)
                    house.green = 255
                    house.red = 50
                elif house.score >= score_list[second_index]:
                    house.alpha = (second_index - current_index + 1) / float(second_index - first_index + 1)
                    house.blue = 255
                    house.green = 50
                else:
                    house.alpha = 1 - (len(score_list) - current_index) / float(len(score_list) - second_index + 4)
                    house.red = 255
    return data


def run():
    all = {
        '1': read_file("file/1.csv"),
        '2-1': read_file("file/2-1.csv"),
        '2-2': read_file("file/2-2.csv"),
        '6': read_file("file/6.csv"),
        '7': read_file("file/7.csv"),
        '8': read_file("file/8.csv")
    }
    html = generate_html(compute_color(all))
    write_file("result.html", html)


if __name__ == '__main__':
    run()
