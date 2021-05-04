from simple_salesforce import Salesforce


def get_data_vector(trace_instruction, client, client_contact, county_court, customer_type, customer_name_input_corporate, customer_first_name, customer_last_name,
                    creditor_name, defendant_name, creditor_ref, county_court_reference, customer_mobile,
                    customer_landline, address_street, address_county, address_city, address_postcode,
                    address_street_2, address_county_2, address_city_2, address_postcode_2, judgement_date,
                    judgement_amount, fixed_costs_as_shown_on_judgement, interest_on_judgement, payments_made,
                    outstanding_balance, customer_email):
    data_vector = {'Client__c': client,
                   'Creditor_Reference__c': creditor_ref,
                   'Trace_Instruction__c': trace_instruction,
                   'Customer_Type__c': customer_type,
                   'Customer_Name_Input_Corporate__c': customer_name_input_corporate,
                   'Customer_First_Name__c': customer_first_name,
                   'Customer_Last_Name__c': customer_last_name,
                   'Creditor_Name__c': creditor_name,
                   'Defendant_Name_per_Judgment__c': defendant_name,
                   'County_Court__c': county_court,
                   'County_Court_Reference__c': county_court_reference,
                   'Customer_Supplied_Address_Street__c': address_street,
                   'Customer_Supplied_Address_City__c': address_city,
                   'Customer_Supplied_Address_County__c': address_county,
                   'Customer_Supplied_Postcode__c': address_postcode,
                   'Customer_Supplied_Address_Street_2__c': address_street_2,
                   'Customer_Supplied_Address_City_2__c': address_city_2,
                   'Customer_Supplied_Address_County_2__c': address_county_2,
                   'Customer_Supplied_Postcode_2__c': address_postcode_2,
                   'Customer_Supplied_Mobile__c': customer_mobile,
                   'Customer_Supplied_Landline__c': customer_landline,
                   'Customer_Supplied_Email__c': customer_email,
                   'Judgment_Date__c': judgement_date,
                   'Judgment_Amount__c': judgement_amount,
                   'Fixed_Costs_as_shown_on_Judgment__c': fixed_costs_as_shown_on_judgement,
                   'Interest_Awarded_on_Judgment__c': interest_on_judgement,
                   'Amount_Paid_Since_Judgment_if_any__c': payments_made,
                   'Supplied_Outstanding_Balance__c': outstanding_balance,
                   'Client_Contact__c': client_contact}
    return data_vector


def write_to_sf(username, pw, token, dict):
    sf = Salesforce(username= username, password= pw, security_token=token)
    sf.Instruction__c.create(dict)
