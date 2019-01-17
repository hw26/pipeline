import sys, ipinfo,json,os.path

from collections import defaultdict
from math import sin, cos, sqrt, atan2, radians

def calculate_distance(source,dest):


    # approximate radius of earth in miles
    R = 3960.0

    lat1, lon1 = source
    lat2, lon2 = dest
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    return distance


def add_record(filename, handler):
    

    distance_matrix = defaultdict(lambda: defaultdict(int))
    
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


    
    details = handler.getDetails(ip_address)
    lat, lon = details.loc.split(',')
    location = (float(lat), float(lon))
    mindist = float('inf')
    score = 0
    closest_ip = ""


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
    sys.stdout.write("Closest of IP address is " + str(closest_ip) + "\n")




def main():

    
    ACCESS_TOKEN = "035abffa9e7bda"
    handler = ipinfo.getHandler(ACCESS_TOKEN)

    if sys.argv[1] ==  "-train":

        if len(sys.argv) < 3:
            sys.stdout.write("Please provide a valid input file path")
            return

        filename = sys.argv[2]
        if not os.path.exists(filename):
            sys.stdout.write("File path " + filename + " invalid")
            return 

        distance_matrix = add_record(filename, handler)
        with open('distance_matrix.json', 'w') as outfile:  
            json.dump(distance_matrix, outfile)
    
    if sys.argv[1] ==  "-query":
        try:
            with open('distance_matrix.json') as json_file:  
                distance_matrix = json.load(json_file)
        except IOError:
            sys.stdout.write("Please add record first using $ pipelin -train <filepath>")
            return 
        if len(distance_matrix) == 0:
            sys.stdout.write("No record in input file to complete query")
        else:
            ip_address = sys.argv[2]
            query_result(distance_matrix, ip_address, handler)






    
if __name__ == "__main__":
    main()
