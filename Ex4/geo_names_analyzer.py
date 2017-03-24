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


def read_info_from_file(filehandle):
    """ Gets name and countrycode for each line in file with entry P and more
        then 0 inhbitants
        filehandle:     Handle to the file
    >>> type(read_info_from_file("ABC"))
    <type 'generator'>
    >>> tst = read_info_from_file("ABC")
    >>> tst.next()
    Traceback (most recent call last):
        ...
    TypeError: filehandle musst be a handle to a file!
    """
    # >>> with zipfile.ZipFile("TEST.zip", 'r') as myzip:
    # ...     with myzip.open("TEST.txt") as f:
    # ...         type(read_info_from_file(f))
    # ...         tst = read_info_from_file(f)
    # ...         tst.next()
    # Hittisau    AT
    # Test    AT
    # Test2   AT
    # Test2   AT
    # Hittisau    AT
    # Hittisau    AT
    # print type(filehandle)
    if not type(filehandle) == zipfile.ZipExtFile:
        raise TypeError("filehandle musst be a handle to a file!")
    for line in filehandle:
        line = line.decode("utf8")
        # print line
        data = line.split("\t")
        if data[6] == "P" and int(data[14]) > 0:
            # print(data[1])
            yield data[1], data[8]
        else:
            continue


def compute_most_frequent_city_names_by_sorting(filename):
    """ Computes he most fequent citynames in file by sorting
        filename:   Name of th zipfile (withou .zip)
    >>> compute_most_frequent_city_names_by_sorting(123)
    Traceback (most recent call last):
        ...
    TypeError: filename musst be a strig!
    >>> compute_most_frequent_city_names_by_sorting("TEST")
    [(u'Hittisau', 3), (u'Wien', 2), (u'Insbruck', 1), (u'Linz', 1)]
    """
    if not type(filename) == str:
        raise TypeError("filename musst be a strig!")
    lst = []
    nameAndCount = []
    with zipfile.ZipFile(filename + ".zip", 'r') as myzip:
        with myzip.open(filename + ".txt") as f:
            for (name, countrycode) in read_info_from_file(f):  # O(n) assumed
                # print name
                lst.append(name)
    # print lst
    lst.sort()  # O(n*log(n)) assumed
    # print lst
    sameNameFound = 0
    j = 0
    for i in range(len(lst)-1):  # O(n) assumed
        # print i, j
        if lst[i] == lst[i + 1]:
            sameNameFound = 1
            j = j + 1
            # print lst[i]
            # print lst[i+1]
        else:
            if sameNameFound == 1:
                nameAndCount.append((lst[i], j+1))
                j = 0
                sameNameFound = 0
            else:
                nameAndCount.append((lst[i], j+1))
    nameAndCount.append((lst[i+1], j+1))
    # print(nameAndCount)
    sorted_nameAndCount = sorted(nameAndCount, key=operator.itemgetter(1),
                                 reverse=True)  # O(n*log(n)) assumed
    # print sorted_nameAndCount
    return sorted_nameAndCount


def compute_most_frequent_city_names_by_map(filename):
    """ Computes he most fequent citynames in file by map
        filename:   Name of th zipfile (withou .zip)
    >>> compute_most_frequent_city_names_by_map(123)
    Traceback (most recent call last):
        ...
    TypeError: filename musst be a string!
    >>> compute_most_frequent_city_names_by_map("TEST")
    [(u'Hittisau', 3), (u'Wien', 2), (u'Insbruck', 1), (u'Linz', 1)]
    """
    if not type(filename) == str:
        raise TypeError("filename musst be a string!")
    # name_dict = {"Test": 0, "Test2": 10}
    nameAndCount_dict = {}
    with zipfile.ZipFile(filename + ".zip", 'r') as myzip:
        with myzip.open(filename + ".txt") as f:
            for (name, countrycode) in read_info_from_file(f):  # O(n) assumed
                if name in nameAndCount_dict:
                    nameAndCount_dict[name] += 1
                    # print(name)
                else:
                    nameAndCount_dict[name] = 1
    # nameAndCount_dict.items()
    # print(tst[0])
    # print(tst[len(tst)-1])
    # print(len(tst))
    sorted_nameAndCount = sorted(nameAndCount_dict.items(),  # O(n) assumed
                                 key=operator.itemgetter(1), reverse=True)
    return sorted_nameAndCount


def compare_runtime(filename):
    print("Compare runtime: %s" % filename)
    print("Most frequent city names by sorting:")
    tic = time.time()
    tic2 = timeit.default_timer()
    lst = compute_most_frequent_city_names_by_sorting(filename)
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
    lst = compute_most_frequent_city_names_by_map(filename)
    toc = time.time()
    runtime = toc - tic
    print("%d Cities checked, runtime was %f s\n" % (len(lst), runtime))
    for i in range(3):
        print(lst[i][0] + "\t" + str(lst[i][1]))


def compute_most_frequent_city_names_by_sorting_DE(filename):
    """ Computes he most fequent citynames in file by sorting
        filename:   Name of the zipfile (withou .zip)
    >>> compute_most_frequent_city_names_by_sorting_DE(123)
    Traceback (most recent call last):
        ...
    TypeError: filename musst be a string!
    >>> compute_most_frequent_city_names_by_sorting_DE("TEST")
    [(u'Wien', 2), (u'Insbruck', 1)]
    """
    if not type(filename) == str:
        raise TypeError("filename musst be a string!")
    lst = []
    nameAndCount = []
    with zipfile.ZipFile(filename + ".zip", 'r') as myzip:
        with myzip.open(filename + ".txt") as f:
            for (name, countrycode) in read_info_from_file(f):
                # print name
                lst.append((name, countrycode))
    # print lst
    lst = sorted(lst, key=operator.itemgetter(0))
    # print lst
    sameNameFound = 0
    j = 0
    DE_found = 0
    for i in range(len(lst)-1):
        # print i, j
        if lst[i][1] == "DE":
            DE_found = 1
        if lst[i][0] == lst[i + 1][0]:
            sameNameFound = 1
            j = j + 1
            # print lst[i]
            # print lst[i+1]
        else:
            if sameNameFound == 1:
                if DE_found == 1:
                    nameAndCount.append((lst[i][0], j+1))
                    DE_found = 0
                j = 0
                sameNameFound = 0
            else:
                if DE_found == 1:
                    nameAndCount.append((lst[i][0], j+1))
                    DE_found = 0
    if DE_found == 1:
        nameAndCount.append((lst[i+1][0], j+1))
        DE_found = 0
    # print(nameAndCount)
    sorted_nameAndCount = sorted(nameAndCount, key=operator.itemgetter(1),
                                 reverse=True)
    # print sorted_nameAndCount
    return sorted_nameAndCount


def compute_most_frequent_city_names_by_map_DE(filename):
    """ Computes he most fequent citynames in file by map
        filename:   Name of th zipfile (withou .zip)
    >>> compute_most_frequent_city_names_by_map_DE(123)
    Traceback (most recent call last):
        ...
    TypeError: filename musst be a string!
    >>> compute_most_frequent_city_names_by_map_DE("TEST")
    [(u'Wien', 2), (u'Insbruck', 1)]
    """
    if not type(filename) == str:
        raise TypeError("filename musst be a string!")
    # name_dict = {"Test": 0, "Test2": 10}
    nameAndCount_dict = {}
    citiesInDE = {}
    nameAndCount_dictDE = {}
    with zipfile.ZipFile(filename + ".zip", 'r') as myzip:
        with myzip.open(filename + ".txt") as f:
            for (name, countrycode) in read_info_from_file(f):
                # print name, countrycode
                if name in nameAndCount_dict:
                    nameAndCount_dict[name] += 1
                    # print(name)
                else:
                    nameAndCount_dict[name] = 1
                if countrycode == "DE" and name not in citiesInDE:
                    citiesInDE[name] = 1
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
    print("Compare runtime DE: %s" % filename)
    print("Most frequent city names by sorting:")
    tic = time.time()
    lst = compute_most_frequent_city_names_by_sorting_DE(filename)
    toc = time.time()
    runtime = toc - tic
    print("%d Cities checked, runtime was %f s\n" % (len(lst), runtime))
    for i in range(3):
        print(lst[i][0] + "\t" + str(lst[i][1]))
    print("\n")
    print("Most frequent city names by map:")
    tic = time.time()
    lst = compute_most_frequent_city_names_by_map_DE(filename)
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
