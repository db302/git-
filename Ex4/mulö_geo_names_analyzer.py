#!/usr/bin/python3

import zipfile
import bisect
import time
import os

"""
Extract world-wide city information from zip files downloaded from
geonames.org. Read directly from zip file.
Link to allCountries.zip:
http://download.geonames.org/export/dump/allCountries.zip

Author: Michael Uhl, Bioinformatics Group Freiburg

"""


def read_info_from_zip_file(zip_file):
    """ Read in file content directly from zip file. """

    # Check if file exists.
    if not os.path.isfile(zip_file):
        raise OSError("file \"%s\" not found" % (zip_file))

    # Check if file is a zip file.
    if not zipfile.is_zipfile(zip_file):
        raise IOError("file \"%s\" not a valid zip file" % (zip_file))

    # Open first file in archive, read in line by line.
    with zipfile.ZipFile(zip_file) as z:
        txt_file = ""
        for f in z.namelist():
            if not f == "readme.txt":
                txt_file = f
        if not txt_file:
            raise Exception("Archive only contains readme.txt")

        with z.open(txt_file) as f:
            for line in f:
                cols = line.decode(encoding='UTF-8').strip().split("\t")
                feature_class = cols[6]
                # Skip entry if feature class not "P".
                if not feature_class == "P":
                    continue
                population = int(cols[14])
                # Skip entry if population size = 0.
                if not population > 0:
                    continue
                # Get city name and country code.
                name = cols[1]
                country_code = cols[8]
                # Use generator.
                yield (name, country_code)


def read_info_from_txt_file(txt_file):
    """ Read in file content. """

    # Check if file exists.
    if not os.path.isfile(zip_file):
        raise OSError("file \"%s\" not found" % (txt_file))

    with open(txt_file) as f:
        # Iterate over lines.
        for line in f:
            cols = line.strip().split("\t")
            feature_class = cols[6]
            # Skip entry if feature class not "P".
            if not feature_class == "P":
                continue
            population = int(cols[14])
            # Skip entry if population size = 0.
            if not population > 0:
                continue
            # Get city name and country code.
            name = cols[1]
            country_code = cols[8]
            # Use generator.
            yield (name, country_code)
    f.closed


def compute_names_by_sorting(iterable, top_x=3):
    """ Compute most frequent city names by sorting.

    >>> test_iter = [("n1", "A"), ("n2", "B"), ("n1", "C"), ("n2", "D"),
    ...              ("n1", "B"), ("n3", "A")]
    >>> compute_names_by_sorting(test_iter)
    [('n1', 3), ('n2', 2), ('n3', 1)]
    >>> compute_names_by_sorting(test_iter, top_x=2)
    [('n1', 3), ('n2', 2)]
    >>> compute_names_by_sorting([])
    []

    """
    lst = []
    # Read in names.
    for stats in iterable:
        lst.append(stats[0])
    # Sort.
    lst.sort()
    # Check if list is empty.
    if not lst:
        return lst
    # Count name occurences in a new list.
    new_lst = []
    prev_name = lst[0]
    i = 1
    for cur_name in lst[1:]:
        # Inside block.
        if cur_name == prev_name:
            i += 1
        # In a new block.
        else:
            # Store previous block count and name as tuple in list.
            new_lst.append((prev_name, i))
            i = 1
        prev_name = cur_name
    # Store last block count and name.
    new_lst.append((prev_name, i))
    # Sort unified list.
    new_lst.sort(key=lambda x: x[1], reverse=True)
    # Return top x counts.
    return new_lst[:top_x]


def compute_names_by_map(iterable, top_x=3):
    """ Compute most frequent city names by map.

    >>> test_iter = [("n1", "A"), ("n2", "B"), ("n1", "C"), ("n2", "D"),
    ...              ("n1", "B"), ("n3", "A")]
    >>> compute_names_by_map(test_iter)
    [('n1', 3), ('n2', 2), ('n3', 1)]
    >>> compute_names_by_map(test_iter, top_x=2)
    [('n1', 3), ('n2', 2)]
    >>> compute_names_by_map([])
    []

    """
    dic = {}
    for stats in iterable:
        if stats[0] in dic:
            dic[stats[0]] += 1
        else:
            dic[stats[0]] = 1
    # Check if dictionary is empty.
    if not dic:
        return []
    # Sort descending and return.
    sorted_dic_list = sorted(dic.items(), key=lambda dic: dic[1], reverse=True)
    return sorted_dic_list[:top_x]


def compute_names_by_map_set_country(iterable, c_code, top_x=3):
    """ Compute most frequent city names by map.
    Here we only return cities which appear at least once in a given country.

    >>> test_iter = [("n1", "A"), ("n2", "B"), ("n1", "C"), ("n2", "D"),
    ...              ("n1", "B"), ("n3", "A")]
    >>> compute_names_by_map_set_country(test_iter, c_code="A")
    [('n1', 3), ('n3', 1)]
    >>> compute_names_by_map_set_country([], c_code="A")
    []

    """
    dic = {}
    country_dic = {}
    for stats in iterable:
        if stats[0] in dic:
            dic[stats[0]] += 1
        else:
            dic[stats[0]] = 1
        # Remember city names that exist in given country.
        if stats[1] == c_code:
            country_dic[stats[0]] = 1
    # Check if dictionary is empty.
    if not dic:
        return []
    # Sort descending and return.
    sorted_dic_list = []
    for k, v in sorted(dic.items(), key=lambda dic: dic[1], reverse=True):
        if k in country_dic:
            sorted_dic_list.append((k, v))
    return sorted_dic_list[:top_x]


def compute_names_by_bisect_sorting(iterable, top_x=3):
    """ Compute most frequent city names by bisect sorting.

    >>> test_iter = [("n1", "A"), ("n2", "B"), ("n1", "C"), ("n2", "D"),
    ...              ("n1", "B"), ("n3", "A")]
    >>> compute_names_by_bisect_sorting(test_iter)
    [('n1', 3), ('n2', 2), ('n3', 1)]
    >>> compute_names_by_bisect_sorting(test_iter, top_x=2)
    [('n1', 3), ('n2', 2)]
    >>> compute_names_by_bisect_sorting([])
    []

    """
    lst = []
    # Read in names.
    for stats in iterable:
        # Keep list sorted with bisect.insort.
        bisect.insort(lst, stats[0])
    # Check if list is empty.
    if not lst:
        return lst
    # Count name occurences in a new list.
    new_lst = []
    prev_name = lst[0]
    i = 1
    for cur_name in lst[1:]:
        # Inside block.
        if cur_name == prev_name:
            i += 1
        # In a new block.
        else:
            # Store previous block count and name as tuple in list.
            new_lst.append((prev_name, i))
            i = 1
        prev_name = cur_name
    # Store last block count and name.
    new_lst.append((prev_name, i))
    # Sort unified list.
    new_lst.sort(key=lambda x: x[1], reverse=True)
    # Return top x counts.
    return new_lst[:top_x]


def measure_times(file_name, top_x=3):
    """
    Measure runtimes for the different approaches
    and output top_x city names.
    """
    # Sorting.
    iterable = read_info_from_zip_file(file_name)
    start = time.time()
    sort_results = compute_names_by_sorting(iterable, top_x=top_x)
    end = time.time()
    print("Time elapsed for sorting: %.1f ms" % ((end - start) * 1000))
    # Map.
    iterable = read_info_from_zip_file(file_name)
    start = time.time()
    map_results = compute_names_by_map(iterable, top_x=top_x)
    end = time.time()
    print("Time elapsed for map: %.1f ms" % ((end - start) * 1000))
    # Report results.
    print("Top %i city names from sorting:" % (top_x))
    for name, count in sort_results:
        print("%s -> %i" % (name, count))
    print("Top %i city names from map:" % (top_x))
    for name, count in map_results:
        print("%s -> %i" % (name, count))


if __name__ == "__main__":
    # Zipped files from geonames.org:
    # allCountries.zip, AT.zip
    zip_file = "allCountries.zip"
    measure_times(zip_file)
