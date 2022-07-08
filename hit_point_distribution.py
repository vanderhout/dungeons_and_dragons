class HitPointDistribution:
    def __init__(self, constitution_bonus, is_tough=False):
        '''

        :param constitution_bonus: CON bonus.
        :param is_tough: True iff character has the Tough feat, adding two extra hit points per level.
        '''
        self._constitution_bonus = constitution_bonus

        # To confirm a level has not been added more than once.
        self._level_set = set()

        # A distribution of all possible hp amounts and their numbers of occurrences.
        self._hp_occurrence_count = {0: 1}

        self._is_tough = is_tough

    def add_level(self, level: int, possible_die_outcome_distribution: list):
        '''

        :param level: What level does the hit point increase correspond to?
        :param possible_die_outcome_distribution: List containing the possible die roll outcomes. For level one, this
        list generally has a single value. CON bonus and Tough are added as specified in __init__.
        :return:
        '''
        if level < 1 or level > 20:
            raise Exception('Invalid level {}.'.format(level))

        if level in self._level_set:
            raise Exception('Already included level {}.'.format(level))

        new_hit_point_possibilities = {}

        for current_hp in self._hp_occurrence_count:
            for roll_outcome in possible_die_outcome_distribution:
                current_count = self._hp_occurrence_count[current_hp]

                new_key = current_hp + int(roll_outcome) + self._constitution_bonus
                if self._is_tough:
                    new_key += 2

                if new_key in new_hit_point_possibilities:
                    new_hit_point_possibilities[new_key] += current_count
                else:
                    new_hit_point_possibilities[new_key] = current_count

        self._hp_occurrence_count = new_hit_point_possibilities

        self._level_set.add(level)

    def print_hit_point_percentiles(self, percentile_decimal_place=2):
        max_specified_level = max(self._level_set)
        for level in range(1, max_specified_level + 1):
            if level not in self._level_set:
                raise Exception(f'Level {level} has not been specified despite a max specified level of {max_specified_level}.')

        print('HP\tPercentile')

        total = 0
        for c in self._hp_occurrence_count:
            total += self._hp_occurrence_count[c]

        cumulative_sum = 0
        for c in self._hp_occurrence_count:
            cumulative_sum += self._hp_occurrence_count[c]
            cumulative_percentage = round(cumulative_sum/total * 100, percentile_decimal_place)
            #cumulative_percentage = cumulative_sum/total * 100

            print(f'{c}\t{cumulative_percentage}')

def Jasira():
    hp_dist = HitPointDistribution(constitution_bonus=4)

    #Level 1 is a guaranteed 8 hit points
    hp_dist.add_level(1, [8])

    #Level 2 to 14:
    for level in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]:

        # 1s are rerolled, so the only possibilities are 2 through 8
        hp_dist.add_level(level, [2, 3, 4, 5, 6, 7, 8])

    hp_dist.print_hit_point_percentiles()

if __name__ == "__main__":
    Jasira()
