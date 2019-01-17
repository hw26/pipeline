README.md
IP Fraud Detection

Hao Wang
Jan 17 2019


Use Case:
To read in the list of input IP information, use $ ./pipeline -train <inputfile> 

To query the score of an IP address, use $ ./pipeline -query <ip_address> 

Please train, i.e. input a list of valid IP login info, before using the query function



Follow Up Questions
What circumstances may lead to false positives or false negatives when using solely this score? 

False positives:
The pipeline may incorrectly predict a fraudulent IP when using solely this score when the input
IP is just unluckily in a bad geographical neighbourhood of frauds. For a real-world example, if a traveller is
stuck in a neighbourhood of hackers and he just logs into his online taxi account go home ASAP, this pipeline
may lock him out of his credit card and he is not able to call a cab, which makes it a very bad day!

False negatives:
False negatives may occur may occur for the opposite reason of false positives. Just because a person
is physically located in a good neighbourhood of faithful users with credible IP address does not mean
he/she is not going to use fraud login credentials. For a real-world example, a guy from a hot shot
tech company may just as well get crazy and decide to create a million fraud bots.

Since we are just using latitude and longitude, the pipeline also does not take into account of 
altitude.

What challenges are there with computing distances based on latitude/longitude? 
Since latitude and longitude are measurements in spherical coordinates, we need to apply
the equation from spherical to Cartesian coordinates. I had to refresh myself with some 
math from high school and confirm my calculation using some online tools such as 
https://www.movable-type.co.uk/scripts/latlong.html

Further Considerations
Since this is an open-ended project, I need to think carefully about the use cases and the
desired output for this pipeline.
I also need to implement some test cases in order to cover corner cases and handle bad input.
I also need to look through the documentation of IPinfo, as well as several other online resources
to make the pipeline simple and intuitive.

Future Improvements
Right now the pipeline is an offline tool where the user can only input the known list
of IPs and then input a single IP and get a single IP result. The input
lists are stored locally in a file that will be read as input separately. 
If we are able to store the input list in a backend, I think we can achieve faster lookup
of closest location to the input IP as databases generally optimize such queries using techniques
such as binary search and direct hashing. 

For extensibility of the metrics, right now all input info is stored in a json file. It is 
relatively easy to add other information provided by IPinfo, such as the name of the user, domain, 
company name, asn etc, and it should be very interesting to see how all these factors affect the
efficiency of the predictor pipeline.
