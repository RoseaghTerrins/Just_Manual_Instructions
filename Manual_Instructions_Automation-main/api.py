import googlemaps
import re
import settings


def split_address(address_line):
    global address_postcode, address_city, address_county, address_street

    api_key = "AIzaSyAxjysYM1gzpu9LJTJUcTxBy9lfoIb-Coo"

    gmaps = googlemaps.Client(key=api_key)
    location = gmaps.find_place(input=address_line, input_type="textquery", fields=['formatted_address'])
    if location['status'] == 'OK':
        x = location['candidates'][0]
        x = str(x)
        x = x.split(':')
        x = x[1]
        x = x.split(',')

        if len(x) == 3:
            address_street = x[0].replace("'", "")
            address_county = ""
            address_city_postcode = x[(len(x) - 2)]
            address_postcode = re.findall(r'\b[A-Z]{1,2}[0-9][A-Z0-9]? [0-9][ABD-HJLNP-UW-Z]{2}\b',
                                          address_city_postcode)
            address_city = address_city_postcode.replace(address_postcode[0], " ")
            address_postcode = address_postcode[0]

        elif len(x) == 4:
            address_street = x[0].replace("'", "") + x[1]
            address_county = ""
            address_city_postcode = x[(len(x) - 2)]
            address_postcode = re.findall(r'\b[A-Z]{1,2}[0-9][A-Z0-9]? [0-9][ABD-HJLNP-UW-Z]{2}\b',
                                          address_city_postcode)
            address_city = address_city_postcode.replace(address_postcode[0], " ")
            address_postcode = address_postcode[0]

        elif len(x) == 5:
            address_street = x[0].replace("'", " ") + x[1]
            address_county = x[2]
            address_city_postcode = x[(len(x) - 2)]
            address_postcode = re.findall(r'\b[A-Z]{1,2}[0-9][A-Z0-9]? [0-9][ABD-HJLNP-UW-Z]{2}\b',
                                          address_city_postcode)
            address_city = address_city_postcode.replace(address_postcode[0], " ")
            address_postcode = address_postcode[0]

        else:
            pass

    else:
        raise Exception("API call to Google Places unsuccessful")

    return address_street, address_county, address_city, address_postcode
