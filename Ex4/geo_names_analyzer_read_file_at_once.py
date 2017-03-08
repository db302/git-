#!/usr/bin/env python3
import zipfile
import operator
import time
import timeit


def tst():
    """ Test fp doctest
    >>> type(tst())
    <type 'generator'>
    >>> tst = tst()
    >>> tst.next()
    ('a', 'b')
    """
    yield "a", "b"


def read_info_from_file(filename):
    """ Gets a list with name and countrycode for each line in file with
        entry P and more then 0 inhbitants
        filename:     String with zip file name without .zip
    >>> read_info_from_file(123)
    Traceback (most recent call last):
        ...
    TypeError: filename musst be a string!
    """
    if not type(filename) == str:
        raise TypeError("filename musst be a string!")
    NameAndCountry = []
    with zipfile.ZipFile(filename + ".zip", 'r') as myzip:
        with myzip.open(filename + ".txt") as f:
            for line in f:  # O(n) assumed
                line = line.decode("utf8")
                data = line.split("\t")
                if data[6] == "P" and int(data[14]) > 0:
                    # print(data[1])
                    NameAndCountry.append((data[1], data[8]))
    # print(NameAndCountry)
    return NameAndCountry


def compute_most_frequent_city_names_by_sorting(NameList):
    """ Computes he most fequent citynames in file by sorting
        NameList:   List with the Names
    >>> compute_most_frequent_city_names_by_sorting(123)
    Traceback (most recent call last):
        ...
    TypeError: Name list musst be a list!
    >>> lst = read_info_from_file("TEST")
    >>> lst2 = []
    >>> for k in range(len(lst)):
    ...     lst2.append(lst[k][0])
    >>> compute_most_frequent_city_names_by_sorting(lst2)
    [(u'Hittisau', 3), (u'Wien', 2), (u'Insbruck', 1), (u'Linz', 1)]
    """
    if not type(NameList) == list:
        raise TypeError("Name list musst be a list!")
    nameAndCount = []
    NameList.sort()  # O(n*log(n)) assumed
    sameNameFound = 0
    j = 0
    for i in range(len(NameList)-1):  # O(n) assumed
        # print i, j
        if NameList[i] == NameList[i + 1]:
            sameNameFound = 1
            j = j + 1
            # print NameList[i]
            # print NameList[i+1]
        else:
            if sameNameFound == 1:
                nameAndCount.append((NameList[i], j+1))
                j = 0
                sameNameFound = 0
            else:
                nameAndCount.append((NameList[i], j+1))
    nameAndCount.append((NameList[i+1], j+1))
    # print(nameAndCount)
    sorted_nameAndCount = sorted(nameAndCount, key=operator.itemgetter(1),
                                 reverse=True)  # O((j+1)*log(j+1)) assumed
    # print sorted_nameAndCount
    return sorted_nameAndCount


def compute_most_frequent_city_names_by_map(NameList):
    """ Computes the most fequent citynames in file by map
        filename:   Name of th zipfile (withou .zip)
    >>> compute_most_frequent_city_names_by_map(123)
    Traceback (most recent call last):
        ...
    TypeError: Name list musst be a list!
    >>> lst = read_info_from_file("TEST")
    >>> lst2 = []
    >>> for k in range(len(lst)):
    ...     lst2.append(lst[k][0])
    >>> compute_most_frequent_city_names_by_map(lst2)
    [(u'Hittisau', 3), (u'Wien', 2), (u'Insbruck', 1), (u'Linz', 1)]
    """
    # name_dict = {"Test": 0, "Test2": 10}
    # print(NameList)
    nameAndCount_dict = {}
    if not type(NameList) == list:
        raise TypeError("Name list musst be a list!")
    for j in range(len(NameList)):  # O(n) assumed
        # print("Test")
        # print(str(j) + "\t" + NameList[j])
        if NameList[j] in nameAndCount_dict:
            nameAndCount_dict[NameList[j]] += 1
        else:
            nameAndCount_dict[NameList[j]] = 1
    # print(len(NameList))
    # print(nameAndCount_dict.items())
    # print(tst[0])
    # print(tst[len(tst)-1])
    # print(len(tst))
    # O(j*log(j)) assumed
    sorted_nameAndCount = sorted(nameAndCount_dict.items(),
                                 key=operator.itemgetter(1), reverse=True)
    return sorted_nameAndCount


def compare_runtime(filename):
    Names = []
    lst = []
    print("Read info From File...")
    NamesAndCountry = read_info_from_file(filename)
    print("Done")
    # print(NamesAndCountry)
    for i in range(len(NamesAndCountry)):
        Names.append(NamesAndCountry[i][0])
    # Names = NamesAndCountry[][1]
    # print(Names)
    print("Compare runtime: %s" % filename)
    print("Most frequent city names by sorting:")
    tic = time.time()
    tic2 = timeit.default_timer()
    lst = compute_most_frequent_city_names_by_sorting(Names)
    toc = time.time()
    toc2 = timeit.default_timer()
    runtime = toc - tic
    runtime2 = toc2 - tic2
    print("%d Cities checked, runtime was %f %f s\n" % (len(lst), runtime,
                                                        runtime2))
    for i in range(3):
        print(lst[i][0] + "\t" + str(lst[i][1]))
    print("\n")
    print("Most frequent city names by map:")
    tic = time.time()
    lst2 = compute_most_frequent_city_names_by_map(Names)
    toc = time.time()
    runtime = toc - tic
    # print(lst2)
    print("%d Cities checked, runtime was %f s\n" % (len(lst2), runtime))
    for i in range(3):
        print(lst2[i][0] + "\t" + str(lst2[i][1]))


def compute_most_frequent_city_names_by_sorting_DE(NameCountList):
    """ Computes he most fequent citynames in file by sorting
        NameCountList:   list with Tupple Name Countrcode
    >>> compute_most_frequent_city_names_by_sorting_DE(123)
    Traceback (most recent call last):
        ...
    TypeError: NameCountList must be a list!
    >>> lst = read_info_from_file("TEST")
    >>> compute_most_frequent_city_names_by_sorting_DE(lst)
    [(u'Wien', 2), (u'Insbruck', 1)]
    """
    if not type(NameCountList) == list:
        raise TypeError("NameCountList must be a list!")
    nameAndCount = []
    # print lst
    NameCountList = sorted(NameCountList, key=operator.itemgetter(0))
    # print lst
    sameNameFound = 0
    j = 0
    DE_found = 0
    for i in range(len(NameCountList)-1):
        # print i, j
        if NameCountList[i][1] == "DE":
            DE_found = 1
        if NameCountList[i][0] == NameCountList[i + 1][0]:
            sameNameFound = 1
            j = j + 1
            # print lst[i]
            # print lst[i+1]
        else:
            if sameNameFound == 1:
                if DE_found == 1:
                    nameAndCount.append((NameCountList[i][0], j+1))
                    DE_found = 0
                j = 0
                sameNameFound = 0
            else:
                if DE_found == 1:
                    nameAndCount.append((NameCountList[i][0], j+1))
                    DE_found = 0
    if DE_found == 1:
        nameAndCount.append((NameCountList[i+1][0], j+1))
        DE_found = 0
    # print(nameAndCount)
    sorted_nameAndCount = sorted(nameAndCount, key=operator.itemgetter(1),
                                 reverse=True)
    # print sorted_nameAndCount
    return sorted_nameAndCount


def compute_most_frequent_city_names_by_map_DE(NameCountList):
    """ Computes he most fequent citynames in file by map
        NameCountList:   list with Tupple Name Countrcode
    >>> compute_most_frequent_city_names_by_map_DE(123)
    Traceback (most recent call last):
        ...
    TypeError: NameCountList musst be a list!
    >>> lst = read_info_from_file("TEST")
    >>> compute_most_frequent_city_names_by_map_DE(lst)
    [(u'Wien', 2), (u'Insbruck', 1)]
    """
    if not type(NameCountList) == list:
        raise TypeError("NameCountList musst be a list!")
    # name_dict = {"Test": 0, "Test2": 10}
    nameAndCount_dict = {}
    citiesInDE = {}
    nameAndCount_dictDE = {}
    for j in range(len(NameCountList)):
        # print name, countrycode
        if NameCountList[j][0] in nameAndCount_dict:
            nameAndCount_dict[NameCountList[j][0]] += 1
            # print(name)
        else:
            nameAndCount_dict[NameCountList[j][0]] = 1
        if NameCountList[j][1] == "DE" and NameCountList[j][0]:
            if NameCountList[j][1] not in citiesInDE:
                citiesInDE[NameCountList[j][0]] = 1
    for key in citiesInDE.iterkeys():
        if key in nameAndCount_dict:
            nameAndCount_dictDE[key] = nameAndCount_dict[key]
    # print(nameAndCount_dictDE)
    # nameAndCount_dict.items()
    # print(tst[len(tst)-1])
    # print(len(tst))
    sorted_nameAndCount = sorted(nameAndCount_dictDE.items(),
                                 key=operator.itemgetter(1), reverse=True)
    return sorted_nameAndCount


def compare_runtimeDE(filename):
    print("Read info From File...")
    NamesAndCountry = read_info_from_file(filename)
    print("Done")
    print("Compare runtime DE: %s" % filename)
    print("Most frequent city names by sorting:")
    tic = time.time()
    lst = compute_most_frequent_city_names_by_sorting_DE(NamesAndCountry)
    toc = time.time()
    runtime = toc - tic
    print("%d Cities checked, runtime was %f s\n" % (len(lst), runtime))
    for i in range(3):
        print(lst[i][0] + "\t" + str(lst[i][1]))
    print("\n")
    print("Most frequent city names by map:")
    tic = time.time()
    lst = compute_most_frequent_city_names_by_map_DE(NamesAndCountry)
    toc = time.time()
    runtime = toc - tic
    print("%d Cities checked, runtime was %f s\n" % (len(lst), runtime))
    for i in range(3):
        print(lst[i][0] + "\t" + str(lst[i][1]))


if __name__ == "__main__":
    # How can I pipe the output in a file
    #    python geo_names_analyzer.py > output.txt
    # is not working for AT:ZIP. Error:
    # "UnicodeEncodeError: 'ascii' codec can't encode ...
    # ordinal not in range(128)"
    compare_runtime("allCountries")
    compare_runtimeDE("allCountries")
