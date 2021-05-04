from scraper import *
from api import split_address
from data_collector import get_data_vector


def silverback(unread_email, sender, subject):
    title, customer_first_name, customer_last_name = customer_names(unread_email)
    address = get_address(unread_email)
    value = get_secondary_address_2(unread_email)
    address_street, address_county, address_city, address_postcode = split_address(address)
    address_street_2, address_county_2, address_city_2, address_postcode_2 = split_secondary_address(value)
    fixed_costs_as_shown_on_judgement = solicitors_fixed_costs_on_claim_form(unread_email) + court_fee_on_claim_form(unread_email) + solicitors_fixed_costs_on_judgment(unread_email)
    client_contact_id = client_contact(sender)
    data = get_data_vector(
                           trace_instruction(),
                           client(),
                           client_contact_id,
                           county_court(unread_email),
                           customer_type(unread_email),
                           customer_name_input_corporate(unread_email),
                           customer_first_name,
                           customer_last_name,
                           creditor_name(unread_email),
                           defendant_name_per_judgement(unread_email),
                           creditor_ref(subject),
                           county_court_reference(unread_email),
                           customer_mobile(unread_email),
                           customer_landline(unread_email),
                           address_street,
                           address_county,
                           address_city,
                           address_postcode,
                           address_street_2,
                           address_county_2,
                           address_city_2,
                           address_postcode_2,
                           judgement_date(unread_email),
                           judgment_amount(unread_email),
                           fixed_costs_as_shown_on_judgement,
                           interest_on_judgement(unread_email),
                           payments_made(unread_email),
                           outstanding_balance(unread_email),
                           customer_email(unread_email))

    return(data)