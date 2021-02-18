import sys
import typing
sys.path.append('../')


class Bag:

    def __init__(self, color: str, bags_inside: typing.List[dict]):
        self.color = color
        self.bags_inside = bags_inside
        self.stored_in = []

    def is_stored_inside(self, color: str) -> bool:
        bags = [bag for bag in self.bags_inside if bag.get('color', '') == color]
        return len(bags) != 0

    def __str__(self):
        return format('\n**********\ncolor: {}\nbags_inside: {}\nstored_in: {}\n***********\n'.format(self.color, self.bags_inside, self.stored_in))

    def __repr__(self):
        return self.__str__()


class BagStorageCounter:
    def get_all_number_of_bags_in_bag(self, bag_color: str, bags: typing.List[Bag]) -> int:
        bag = self.get_bag(bag_color=bag_color, bags=bags)
        return self.get_number_of_bags_in(bag, bags)

    def get_number_of_bags_in(self, bag: Bag, bags: typing.List[Bag]) -> int:
        cur_sum = 0
        for bag_inside in bag.bags_inside:
            bag = self.get_bag(bag_inside.get('color', ''), bags)
            cur_sum += self.get_number_of_bags_in(bag, bags) * bag_inside.get('quantity', 1)
            cur_sum += bag_inside.get('quantity', 0)

        return cur_sum

    def get_number_of_colors_that_contains_eventually(self, bag_color: str, bags: typing.List[Bag]) -> int:
        bag = self.get_bag(bag_color, bags)

        if not bag:
            return 0

        contained_in = self.get_colors_that_contains_bag_eventually(bag_color, bags)

        return len(contained_in)

    def get_bag(self, bag_color: str, bags: typing.List[Bag]) -> Bag:
        for bag in bags:
            if bag.color == bag_color:
                return bag
        return None

    def get_colors_that_contains_bag_eventually(self, bag_color: str, bags: typing.List[Bag], result_list: typing.List[str] = []) -> typing.List[str]:
        bag = self.get_bag(bag_color, bags)

        if len(bag.stored_in) == 0:
            return result_list

        for bag_in in bag.stored_in:
            if bag_in not in result_list:
                result_list.append(bag_in)
                self.get_colors_that_contains_bag_eventually(bag_in, bags, result_list)

        return result_list



class RulesToBagConverter:
    def get_bags_from_rules(self, raw_rules: typing.List[str]):
        bags = list(map(self.get_bag_from_rule, raw_rules))
        updated_bags = []
        for bag in bags:
            updated_bag = self.add_contained_in(bag, bags)
            updated_bags.append(updated_bag)

        return updated_bags

    def get_bag_from_rule(self, rule: str):
        splited_rule = rule.split('contain')

        color = self.extract_color(splited_rule[0])
        bags_inside = self.extract_contains_bags(splited_rule[1])

        bag = Bag(color=color, bags_inside=bags_inside)
        return bag

    def extract_color(self, rule_first_part: str) -> str:
        return rule_first_part.replace(' bags ', '')

    def extract_contains_bags(self, contains_bags_rule_part: str) -> typing.List[dict]:
        if 'no other' in contains_bags_rule_part:
            return []

        raw_bags_contained = contains_bags_rule_part.split(',')
        bags_contained = []

        for bag in raw_bags_contained:
            number = [int(word) for word in bag.split() if word.isdigit()][0]
            color = ' '.join([word for word in bag.split() if word.isalpha() and 'bag' not in word])
            bags_contained.append({'color': color, 'quantity': number})

        return bags_contained

    def add_contained_in(self, bag: Bag, bags: typing.List[Bag]) -> Bag:
        for searched_bag in bags:
            if searched_bag.color == bag.color:
                continue
            elif searched_bag.is_stored_inside(bag.color) and searched_bag.color not in bag.stored_in:
                bag.stored_in.append(searched_bag.color)

        return bag


with open('input.txt') as file:
    rules = file.read().split('\n')

    converter = RulesToBagConverter()
    counter = BagStorageCounter()

    bags = converter.get_bags_from_rules(rules)
    # number_of_colors = counter.get_number_of_colors_that_contains_eventually(bag_color='shiny gold', bags=bags)

    number_of_bags_inside = counter.get_all_number_of_bags_in_bag(bag_color='shiny gold', bags=bags)
    print(number_of_bags_inside)

