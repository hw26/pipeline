#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, ipinfo,json,os.path
from collections import defaultdict
from math import sin, cos, sqrt, atan2, radians

"""
Fraud Detection Pipeline
Hao Wang
01/17/2019

For instructions to use the program, 
go to README.md
"""


def add_record(filename, handler):
    """
    Given a valid input file,
    whith each line corresponding to 
    an authenticity and IP address, record
    the entry into the distance_matrix table

    """

    distance_matrix = defaultdict(lambda: defaultdict(int))
    
    ### process the input file line
    ### by line and record the info
    with open(filename, 'r') as f:
        for line_terminated in f:
            line = line_terminated.rstrip('\n')
            auth, ip = line.split(' ') 
            details = handler.getDetails(ip)
            location = details.loc
            distance_matrix[location]["authenticity"] = auth
            distance_matrix[location]["login_times"] += 1
            distance_matrix[location]["ip"] = ip
    return distance_matrix


def query_result(distance_matrix, ip_address, handler):
    """
    Given an IP address and the distance matrix
    of recorded logins, find the mile distance between the new 
    login IP and the closest IP found in the input distance matrix
    """
    
    ### get location info from IPinfo handler
    details = handler.getDetails(ip_address)
    lat, lon = details.loc.split(',')
    location = (float(lat), float(lon))
    mindist = float('inf')
    score = 0
    closest_ip = ""

    ### iterate through the matrix and 
    ### find the closest previous record
    for each in distance_matrix:
        lat, lon = each.split(",")
        each_float = (float(lat), float(lon))
        distance = calculate_distance(each_float, location)
        if distance < mindist:
            mindist = distance
            score = mindist
            if distance_matrix[each]["authenticity"] == "FRAUD":
                score *= 2
            closest_ip = distance_matrix[each]["ip"]
    sys.stdout.write("Score of input IP address is " + str(score) + "\n")
    sys.stdout.write("Closest IP address is " + str(closest_ip) + "\n")


def calculate_distance(source,dest):


    """
    Given a pair of latitude, longitude
    coordinate pairs, compute the distance
    in miles of two locations
    """

    ### Earth radius in miles
    R = 3960.0

    lat1, lon1 = source
    lat2, lon2 = dest
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    ### compute distance in spherical coordinates

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    return distance

def main():

    ### global IPinfo ACCESS_TOKEN
    
    ACCESS_TOKEN = "035abffa9e7bda"
    handler = ipinfo.getHandler(ACCESS_TOKEN)

    ### train the model
    if sys.argv[1] ==  "-train":
        ### error handling

        if len(sys.argv) < 3:
            sys.stdout.write("Please provide a valid input file path")
            return

        filename = sys.argv[2]
        if not os.path.exists(filename):
            sys.stdout.write("File path " + filename + " invalid")
            return 

        distance_matrix = add_record(filename, handler)
        ### store results
        with open('distance_matrix.json', 'w') as outfile:  
            json.dump(distance_matrix, outfile)
    
    ### query result
    if sys.argv[1] ==  "-query":

        ### error handling
        try:
            with open('distance_matrix.json') as json_file:  
                distance_matrix = json.load(json_file)
        except IOError:
            sys.stdout.write("Please add record first using $ pipeline -train <filepath>")
            return 
        if len(distance_matrix) == 0:
            sys.stdout.write("No record in input file to complete query")
        else:
            ip_address = sys.argv[2]
            query_result(distance_matrix, ip_address, handler)






    
if __name__ == "__main__":
    main()
