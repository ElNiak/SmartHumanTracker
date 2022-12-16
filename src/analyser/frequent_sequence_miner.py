#!/usr/bin/env python3
import sys
import time


class Dataset:
    """Utility class to manage a dataset stored in a external file."""

    def __init__(self, filepath, filepath_neg):
        """reads the dataset file and initializes files"""
        self.items = {}
        self.items_neg = {}
        self.number_transaction = 0
        self.minimum_support = 1

        try:
            lines = [line.strip() for line in open(filepath, "r")]
            for line in lines:
                if line != '':
                    line_split = line.split()
                    if line_split[0] in self.items:
                        self.items[line_split[0]].append([self.number_transaction, int(line_split[1])])
                    else:
                        self.items[line_split[0]] = list()
                        self.items[line_split[0]].append([self.number_transaction, int(line_split[1])])
                else:
                    self.number_transaction = self.number_transaction + 1
        except IOError as e:
            print("Unable to read dataset file!\n" + e)
        # print(self.items)

        # negative
        self.number_transaction = 0
        try:
            lines = [line.strip() for line in open(filepath_neg, "r")]
            for line in lines:
                if line != '':
                    line_split = line.split()
                    if line_split[0] in self.items_neg:
                        self.items_neg[line_split[0]].append([self.number_transaction, int(line_split[1])])
                    else:
                        self.items_neg[line_split[0]] = list()
                        self.items_neg[line_split[0]].append([self.number_transaction, int(line_split[1])])
                else:
                    self.number_transaction = self.number_transaction + 1
        except IOError as e:
            print("Unable to read dataset file!\n" + e)
        # print("items neg", self.items_neg)


def main(data_file, top_k):
    pos_filepath = data_file  # filepath to positive class file
    neg_filepath = data_file  # filepath to negative class file
    k = top_k
    dataset = Dataset(pos_filepath, neg_filepath)
    top_support = set()
    dict_support = {}

    dict_item = dataset.items
    dict_item_neg = dataset.items_neg

    def check_top_support(support):
        top_support.add(support)
        if len(top_support) > k:
            #print(top_support)
            top_support.remove(min(top_support))
            dataset.minimum_support = max(dataset.minimum_support, min(top_support))

    def dfs(dataset,dataset_neg, node, dict_support, is_neg):
        #print("node : " + str(node))
        # print("db : ", dataset)
        #print("db_neg : ", dataset_neg)
        new_dict, new_dict_neg = update_db(dataset,dataset_neg, node, dict_support, is_neg)
        # print("new db :" + str(new_dict))
        list_candidat = create_neighbors(new_dict, node)
        for candidat in list_candidat:
            dfs(new_dict,new_dict_neg, candidat, dict_support, is_neg)

    def create_neighbors(new_dict, node):
        list_candidat = list()
        for candidat in new_dict:
            node_bis = node + [candidat]
            list_candidat.append(node_bis)
        return list_candidat

    def update_db(dict,dict_neg, key_elem, dict_support, is_neg):
        # print(dict[key_elem])
        # indicator to know if we already found a first element in the transaction
        first = 0
        first_neg = 0
        new_dict = {key_elem[-1]: list()}
        new_dict_neg = {key_elem[-1]: list()}
        # store position of all first elements to remove after all element before and remove them from the hashmap
        first_elem_transaction = list()
        # list of transaction where we have the node
        is_present = list()
        # key elem[-1] take last letter of the node eg : AAC will look at C in the hashmap
        is_present_neg = list()
        first_elem_transaction_neg = list()

        update_node(dict, dict_support, first, first_elem_transaction, False, is_present, key_elem, new_dict, new_dict_neg)

        # print(key_elem + str(key_elem[-1]) + " supporting " + str(len(is_present)))
        other_items_infrequent(dict, key_elem, new_dict, first_elem_transaction, dict_support, False, new_dict_neg)


        update_node(dict_neg, dict_support,first_neg,first_elem_transaction_neg,
                    True,is_present_neg,key_elem, new_dict_neg, new_dict)

        other_items_infrequent(dict_neg, key_elem, new_dict_neg, first_elem_transaction_neg, dict_support, True, new_dict)
        # print("ee")

        # print(first_elem_transaction)
        return new_dict, new_dict_neg

    def update_node(dict, dict_support, first, first_elem_transaction, is_neg, is_present, key_elem, new_dict, new_dict_to_update):
        #print("key elem", key_elem[-1])

        for elem in dict[key_elem[-1]]:
            if elem[0] > first:
                first_elem_transaction.append(elem)
                first = elem[0]
            else:
                if elem[0] not in is_present:
                    # avoid to count twice in the same transaction
                    is_present.append(elem[0])
                # create the new hashmap for the next nodes
                new_dict[key_elem[-1]].append(elem)
        key_elem_bis = key_elem + [key_elem[-1]]
        key_support = str('[%s]' % ', '.join(map(str, key_elem_bis)))
        if is_neg and (len(is_present) + dict_support.get(key_support)[0])< dataset.minimum_support:
            #print("delete", key_elem[-1])
            del new_dict[key_elem[-1]]
            del new_dict_to_update[key_elem[-1]]
        else:
            if is_neg:
                if key_support in dict_support:
                    dict_support[key_support] = (dict_support.get(key_support)[0], len(is_present),
                                                 len(is_present) + dict_support.get(key_support)[0])
                    check_top_support(len(is_present) + dict_support.get(key_support)[0])
                else:
                    dict_support[key_support] = (0, len(is_present), len(is_present))
                    check_top_support(len(is_present))
            else:
                if key_support in dict_support:
                    dict_support[key_support] = (len(is_present), dict_support.get(key_support)[1],
                                                 len(is_present) + dict_support.get(key_support)[1])
                    check_top_support(len(is_present) + dict_support.get(key_support)[1])
                else:
                    dict_support[key_support] = (len(is_present), 0, len(is_present))
                    check_top_support(len(is_present))

    def other_items_infrequent(dict, key_elem, new_dict, first_elem_transaction, dict_support, is_neg, new_dict_to_update):
        # dict : the db that we have
        # new_dict : the new db that we complete
        # first element  list of transaction that we must be after
        # dict_support save the pattern

        for transaction in dict.items():
            if transaction[0] != key_elem[-1]:
                new_dict[transaction[0]] = list()
                is_present = list()
                # transaction [0] is the key && transaction [1] is the values
                for elem in transaction[1]:
                    # look at the element from the transaction 1
                    filteri = [item for item in first_elem_transaction if item[0] == elem[0]]
                    # filteri to work only with transaction that already have the first element
                    if len(filteri) > 0:
                        # always size 1
                        filter_elem = filteri[0]
                        if elem[1] > filter_elem[1]:
                            # check if we are after
                            if elem[0] not in is_present:
                                # to avoid to count multiple times in the same transaction
                                is_present.append(elem[0])
                            new_dict[transaction[0]].append(elem)
                key_elem_bis = key_elem + [transaction[0]]
                key_support = str('[%s]' % ', '.join(map(str, key_elem_bis)))
                # print(key_support)
                if is_neg and (len(is_present) + dict_support.get(key_support)[0]) < dataset.minimum_support:
                    #print("delete", transaction[0])
                    del new_dict[transaction[0]]
                    del new_dict_to_update[transaction[0]]
                else:

                    if is_neg:
                        if key_support in dict_support:
                            dict_support[key_support] = (
                                dict_support.get(key_support)[0], len(is_present), len(is_present)
                                + dict_support.get(key_support)[0])
                            check_top_support(len(is_present) + dict_support.get(key_support)[0])
                        else:
                            dict_support[key_support] = (0, len(is_present), len(is_present))
                            check_top_support(len(is_present))
                    else:

                        if key_support in dict_support:
                            dict_support[key_support] = (
                                len(is_present), dict_support.get(key_support)[1], len(is_present)
                                + dict_support.get(key_support)[1])
                            check_top_support(len(is_present) + dict_support.get(key_support)[1])
                        else:
                            dict_support[key_support] = (len(is_present), 0, len(is_present))
                            check_top_support(len(is_present))
                # print(str(key_elem_bis) + " support " + str(len(is_present)))

    # continue main

    #dict_item['E'] = []
    visited = set()
    #print(dict_item)
    list_key_to_add = []
    for item_pos in dict_item.items():
        if item_pos[0] not in dict_item_neg:
            dict_item_neg[item_pos[0]] = []

    for item in list(dict_item.items()):
        visited.add(item[0])
        is_present = list()
        for item_transaction in item[1]:
            if item_transaction[0] not in is_present:
                is_present.append(item_transaction[0])
        key_start = str('[%s]' % ', '.join(map(str, [item[0]])))
        dict_support[key_start] = (len(is_present), 0, len(is_present))

        for item_neg in dict_item_neg.items():
            if item_neg[0] not in dict_item:
                dict_item[item_neg[0]] = []
                dict_support[str('[%s]' % ', '.join(map(str, [item_neg[0]])))] = (0,0,0)

        #dfs(dict_item,dict_item_neg, [item[0]], dict_support, False)
    #print(dict_support)
    # neg
    for item in dict_item_neg.items():
        is_present_neg = list()
        for item_transaction in item[1]:
            if item_transaction[0] not in is_present_neg:
                is_present_neg.append(item_transaction[0])
        key_start = str('[%s]' % ', '.join(map(str, list(item[0]))))
        if key_start in dict_support:
            dict_support[key_start] = (dict_support.get(key_start)[0], len(is_present_neg),
                                       len(is_present_neg) + dict_support.get(key_start)[0])
            check_top_support(len(is_present_neg) + dict_support.get(key_start)[0])
        else:
            dict_support[key_start] = (0, len(is_present_neg), len(is_present_neg))
        dfs(dict_item, dict_item_neg, [item[0]], dict_support, True)
    f = open("pattern.dat", "w+")

    #for filering unrelevant pattern of IR
    for result in list(dict_support):
        if result[1] == "0" or 40<len(result) or len(result) <10 or result[-2:-1]=="0":
            del dict_support[result]

    for item in list(dict_support):
        for item_inside in list(dict_support):
            # print(dict_support_closed)
            if item in dict_support and item_inside in dict_support:
                if len(item) < len(item_inside) and dict_support[item] == dict_support[item_inside]:

                    last_pos = -1
                    match = 0
                    for letter in item:  # [AAAA] -> A A A
                        pos = 0
                        for letter_inside in item_inside:
                            # print(item,item_inside,pos,last_pos)
                            pos = pos + 1
                            if letter == letter_inside and pos > last_pos:
                                #   print("match letter")
                                last_pos = pos
                                match = match + 1
                                break
                    if item in dict_support:
                        if match == len(item):
                            # print("delete", item, "Because", item_inside)
                            del dict_support[item]








    for result in dict_support.items():
        if (result[1][2]) >= dataset.minimum_support:
            print(result[0] + " " + str(' '.join(map(str, result[1]))))
            #for filering noise pattern
            #if result[0][1]!= "0" and 10<len(result[0])<20 and result[0][-2:-1]!="0":
            f.write('\n'+result[0] + " " + str(' '.join(map(str, result[1]))))
    f.close()


    #print(top_support)
    #print(dataset.minimum_support)


if __name__ == "__main__":
    startTime = time.perf_counter()
    main("data.dat", 16)
    endTime = time.perf_counter()
    print("Time :", endTime - startTime)
