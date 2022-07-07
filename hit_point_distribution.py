class HitPointDistribution:
    def __init__(self, constitution_bonus, hit_point_die, possible_die_outcome_distribution):
        self._constitution_bonus = constitution_bonus
        self._hit_point_die = hit_point_die
        self._possible_die_outcome_distribution = possible_die_outcome_distribution

        # To confirm a level has not been added more than once.
        self._level_set = set()

        # A distribution of all possible hp amounts and their numbers of occurrences.
        self._hp_occurrence_count = {0: 1}

    def add_level(self, level):
        if level < 1 or level > 20:
            raise Exception('Invalid level {}.'.format(level))

        if level in self._level_set:
            raise Exception('Already included level {}.'.format(level))

        if level == 1:
            self._add_level_one()
        else:
            self._add_level_aside_from_one()

        self._level_set.add(level)

    def _add_level_one(self):
        new_hp_occurence_count = {}

        for current_hp in self._hp_occurrence_count:
            current_count = self._hp_occurrence_count[current_hp]

            new_key = current_hp + self._hit_point_die + self._constitution_bonus

            if new_key in new_hp_occurence_count:
                new_hp_occurence_count[new_key] += current_count
            else:
                new_hp_occurence_count[new_key] = current_count

        self._hp_occurrence_count = new_hp_occurence_count

    def _add_level_aside_from_one(self):
        new_hit_point_possibilities = {}

        for current_hp in self._hp_occurrence_count:
            for roll_outcome in self._possible_die_outcome_distribution:
                current_count = self._hp_occurrence_count[current_hp]

                new_key = current_hp + roll_outcome + self._constitution_bonus

                if new_key in new_hit_point_possibilities:
                    new_hit_point_possibilities[new_key] += current_count
                else:
                    new_hit_point_possibilities[new_key] = current_count

        self._hp_occurrence_count = new_hit_point_possibilities

    def print_result(self):
        print('HP\tPercentile')

        total = 0
        for c in self._hp_occurrence_count:
            total += self._hp_occurrence_count[c]

        cumulative_sum = 0
        for c in self._hp_occurrence_count:
            cumulative_sum += self._hp_occurrence_count[c]
            cumulative_percentage = round(cumulative_sum/total * 10000) / 100

            print(f'{c}\t{self._hp_occurrence_count[c]}\t\t{cumulative_percentage}')


def Jasira():
    hp_dist = HitPointDistribution(constitution_bonus=4,
                                   hit_point_die=8,
                                   possible_die_outcome_distribution=[2, 3, 4, 5, 6, 7, 8])

    for level in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]:
        hp_dist.add_level(level)

    hp_dist.print_result()


if __name__ == "__main__":
    Jasira()
