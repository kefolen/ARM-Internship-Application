import pandas as pd


# Read in the dataset and the rules file
def read_data(path_dataset, path_rules):
    dataset = pd.read_csv(path_dataset, sep='\t')
    rules = []
    with open(path_rules, 'r', encoding='utf-8') as f:
        for line in f:
            read = list(line.split(' '))
            rule = []
            flag = True
            for predicate in read:
                match predicate:
                    case '=>':
                        break
                    case 'NOT':
                        flag = False
                    case 'AND':
                        flag = True
                    case _:
                        rule.append([predicate, flag])  # flag=True means the predicate is not negated
            rules.append(rule)

    return dataset, rules


# Filter dataframe to the rows that match the given rule
def cover(rule, df):
    for predicate in rule:
        df = df[df[predicate[0]] == predicate[1]]
    return df


# Compute the probability that the rule correctly predicts 'donor_is_old'
def probability(rule, df):
    df = cover(rule, df)
    pos = df[df['donor_is_old'] == True].shape[0]
    neg = df[df['donor_is_old'] == False].shape[0]
    p = pos / (pos + neg) if (pos + neg) > 0 else 0
    return p


# Evaluate how well a set of rules covers the dataset
def check_covering(df, rules, rules_info):
    pos = 0
    covers = [set(cover(rules_info[i], df).index) for i in rules]
    cover_space = {a for b in covers for a in b}
    for i in df.index:
        if (i in cover_space) == df.iloc[i].loc['donor_is_old']: pos += 1

    return pos / df.shape[0]


# Main algorithm for selecting a compressed ruleset
def generate_ruleset(dataset, rules_info):
    total_covered = set()
    need_to_cover = set(dataset[dataset['donor_is_old'] == True].index)
    rules = [i for i in range(len(rules_info))]
    df = dataset.copy()
    ans = []

    while total_covered < need_to_cover and rules:
        cover_spaces = {i: set(cover(rules_info[i], df).index) for i in rules}
        prob = {i: probability(rules_info[i], df) for i in rules}

        # Rank rules based on how well they cover needed examples and their correctness
        rules.sort(key=lambda x: [len(need_to_cover.intersection(cover_spaces[x])) / len(need_to_cover) + prob[x]])

        # Pick best rule and update state
        ans.append(rules.pop())
        total_covered = total_covered.union(need_to_cover.intersection(cover_spaces[ans[-1]]))
        df = df[~df.index.isin(total_covered)]  # remove covered rows

    return ans


# Write the selected rules to a file
def write_ans(ans, grade):
    with open('Data/ans.txt', 'w', encoding='utf-8') as f:
        for rule in ans:
            to_write = ''
            for predicate in rule:
                if to_write != '':
                    to_write += 'AND '
                to_write += 'NOT ' * (not predicate[1]) + predicate[0] + ' '
            to_write += '=> donor_is_old\n'
            f.write(to_write)
        f.write('\nOverall probability of correctness with this ruleset: ' + str(round(grade, 3)))

# Main entry point
def main():
    dataset, rules_info = read_data('Data/dataset.tsv', 'Data/rules.txt')
    solution = generate_ruleset(dataset, rules_info)
    write_ans([rules_info[i] for i in solution], check_covering(dataset, solution, rules_info))


if __name__ == '__main__':
    main()
