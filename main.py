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
        score = 0
        if level >= 32:
            score = 0
        elif level >= 31:
            score = 0
        elif level >= 30:
            score = 70
        elif level >= 25:
            score = 80
        elif level >= 20:
            score = 90
        elif level >= 16:
            score = 100
        elif level >= 10:
            score = 90
        elif level >= 6:
            score = 80
        elif level >= 4:
            score = 70
        else:
            score = 0
        return score

    def score_of_direction(self):
        if self.direction == '东':
            return 80
        elif self.direction == '南':
            return 100
        elif self.direction == '西':
            return 60
        elif self.direction == '北':
            return 20
        else:
            raise RuntimeError

    def score_of_area(self):
        area = round(float(self.area))
        if area == 108:
            return 100
        elif area == 107:
            return 100
        elif area == 115:
            return 90
        elif area == 130:
            return 80
        elif area == 131:
            return 80
        elif area == 132:
            return 80
        elif area == 138:
            return 70
        elif area == 137:
            return 70
        elif area == 139:
            return 70
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
    score_set = set()
    for building in data.values():
        for level in building:
            for house in level.values():
                size += 1
                score_set.add(house.score)
    sorted_score = list(score_set)
    sorted_score.sort(reverse=True)

    first_index = int(ceil(len(sorted_score) * 0.3))
    second_index = int(ceil(len(sorted_score) * 0.6))

    for building in data.values():
        for level in building:
            for house in level.values():
                current_index = sorted_score.index(house.score)
                house.sort = current_index + 1
                if house.score >= sorted_score[first_index]:
                    house.alpha = (first_index - current_index + 1) / float(first_index + 1)
                    house.green = 255
                    house.red = 50
                elif house.score >= sorted_score[second_index]:
                    house.alpha = (second_index - current_index + 1) / float(second_index - first_index + 1)
                    house.blue = 255
                    house.green = 50
                else:
                    house.alpha = 1 - (len(sorted_score) - current_index) / float(len(sorted_score) - second_index)
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
