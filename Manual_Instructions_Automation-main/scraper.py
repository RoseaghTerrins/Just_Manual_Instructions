from email_account import get_text_between
import re
from datetime import datetime
import warnings


def client():
    client_record_id = "0013z00002QnmEVAAZ"
    return client_record_id


def trace_instruction():
    trace_instruction_value = 2
    return trace_instruction_value


def customer_type(text):
    value = get_text_between("Defendant Name -", "Court -", text)
    if "T/A" in value:
        val = "Sole Trader"
    elif "Ltd" in value:
        val = "Corporate"
    elif "Limited" in value:
        val = "Corporate"
    elif "LTD" in value:
        val = "Corporate"
    elif "LIMITED" in value:
        val = "Corporate"
    else:
        val = "Individual"
    return val


def customer_name_input_corporate(text):
    if customer_type(text) == "Corporate":
        value = get_text_between("Defendant Name -", "Court -", text)
    else:
        value = ""

    return value


def customer_names(text):
    global title, first_name, last_name
    value = get_text_between("Defendant Name -", "Court -", text)

    if "T/A" in value:
        title, first_name, last_name = trading_as(value)

    elif "Ltd" in value or "Limited" in value or "Limited." in value or "LTD" in value or "LIMITED" in value:
        title, first_name, last_name = limited()

    else:
        title, first_name, last_name = otherwise(value)

    return title, first_name, last_name


def trading_as(value):
    global title, last_name, first_name
    value = value.split("T/A")
    value = value[0]
    if len(re.findall(r'\w+', value)) == 3:
        value = value.split()
        title = value[0]
        first_name = value[1]
        last_name = value[2]
    elif len(re.findall(r'\w+', value)) == 4:
        title = value[0]
        first_name = value[1]
        last_name = value[3]
    else:
        pass
    return title, first_name, last_name


def limited():
    title = ""
    first_name = ""
    last_name = ""
    return title, first_name, last_name


def otherwise(value):
    global title, last_name
    if len(re.findall(r'\w+', value)) == 3:
        value = value.split()
        title = value[0]
        first_name = value[1]
        last_name = value[2]
    elif len(re.findall(r'\w+', value)) == 4:
        title = value[0]
        first_name = value[1]
        last_name = value[3]
    else:
        pass
    return title, first_name, last_name


def creditor_name(text):
    value = get_text_between("Claimant Name -", "Defendant Name -", text)
    return value


def creditor_ref(subject):
    value = get_text_between("Our Ref:", "- Instructions to Issue Writ of Fi Fa", subject)
    return value


def defendant_name_per_judgement(text):
    value = get_text_between("Defendant Name -", "Court -", text)
    return value


def county_court_reference(text):
    value = get_text_between("Claim Number - ", "Date of Judgment -", text)
    return value


def customer_mobile(text):
    try:
        value = get_text_between("Debtor Mob:", "Debtor Email:", text)
        if "/" in value:
            value = value.replace("/", "")
        if " " in value:
            value = value.replace(" ", "")
        else:
            pass
    except ValueError as e:
        warnings.warn(str(e))
        value = ""
    return value


def customer_landline(text):
    try:
        value = get_text_between("Debtor Tel:", "Debtor Mob:", text)
        if "/" in value:
            value = value.replace("/", "")
        if " " in value:
            value = value.replace(" ", "")
        else:
            pass
    except ValueError as e:
        warnings.warn(str(e))
        value = ""

    return value


def get_address(text):
    value = get_text_between("Execution Address -", "Other Addresses of note -", text)
    return value


def judgment_amount(text):
    value = get_text_between("Claim Sum -", "Solicitors Fixed Costs on claim form -", text)
    value = value.replace("=C2=A3", "")
    value = value.replace(",", "")
    value = value.replace("��", "")
    return value


def interest_on_judgement(text):
    value = get_text_between("Interest on Judgment -", "Solicitors Fixed Costs on judgment -", text)
    value = value.replace("=C2=A3", "")
    value = value.replace(",", "")
    value = value.replace("��", "")
    return value


def solicitors_fixed_costs_on_claim_form(text):
    value = get_text_between("Solicitors Fixed Costs on claim form - ", "Court Fee on claim form - ", text)
    value = value.replace("=C2=A3", "")
    value = value.replace(",", "")
    value = value.replace("��", "")
    value = float(value)
    value = round(value, 2)
    return value


def court_fee_on_claim_form(text):
    value = get_text_between("Court Fee on claim form - ", "Interest on Judgment ", text)
    value = value.replace("=C2=A3", "")
    value = value.replace(",", "")
    value = value.replace("��", "")
    value = float(value)
    value = round(value, 2)
    return value


def solicitors_fixed_costs_on_judgment(text):
    try:
        value = get_text_between("Solicitors Fixed Costs on judgment -", "Payments made - ", text)
        value = value.replace("=C2=A3", "")
        value = value.replace(",", "")
        value = value.replace("��", "")
        value = float(value)
        value = round(value, 2)
    except ValueError as e:
        warnings.warn(str(e))
        try:
            value = get_text_between("Solicitors Fixed Costs on judgment -", "Execution Address -", text)
            value = value.replace("=C2=A3", "")
            value = value.replace(",", "")
            value = value.replace("��", "")
            value = float(value)
            value = round(value, 2)
        except ValueError as e:
            warnings.warn(str(e))
            value = ''
    return value


def payments_made(text):
    try:
        value = get_text_between("Payments made - ", "Current Balance Due - ", text)
        value = value.replace("=C2=A3", "")
        value = value.replace(",", "")
        value = value.replace("��", "")
    except ValueError:
        value = ""
    return value


def outstanding_balance(text):
    try:
        value = get_text_between("Current Balance Due -", "Execution Address", text)
        value = value.replace("=C2=A3", "")
        value = value.replace(",", "")
        value = value.replace("*", "")
        value = value.replace("��", "")
        value = value.strip('\n')
        value = value.strip(" ")
    except ValueError as e:
        warnings.warn(str(e))
        value = ""
    return value


def customer_email(text):
    try:
        value = get_text_between("Debtor Email:", "Company Contact", text)
    except ValueError as e:
        warnings.warn(str(e))
        try:
            value = get_text_between("Debtor Email:", "If you require any further information", text)
        except ValueError as e:
            warnings.warn(str(e))
            value = ""
    return value


def judgement_date(text):
    value = get_text_between("Date of Judgment - ", "Total Sum of Judgment - ", text)
    value = datetime.strptime(value, '%d/%m/%Y').date()
    value = str(value)
    return value


def get_secondary_address_2(text):
    try:
        value = get_text_between("Other Addresses of note -", "Debtor Tel:", text)
    except ValueError as e:
        warnings.warn(str(e))
        try:
            value = get_text_between("Other Addresses of note -", "Debtor Mob:", text)
        except ValueError as e:
            warnings.warn(str(e))
            try:
                value = get_text_between("Other Addresses of note -", "Debtor Email:", text)
            except ValueError as e:
                warnings.warn(str(e))
                value = ""
    return value


def split_secondary_address(value):
    global address_street, address_city, address_postcode, address_county
    value = value.split('\n')
    if len(value) == 2:
        address_street = value[0]
        address_county = ""
        address_postcode = re.findall(r'\b[A-Z]{1,2}[0-9][A-Z0-9]? [0-9][ABD-HJLNP-UW-Z]{2}\b',
                                      value[len(value) - 1])
        if not address_postcode:
            address_city = value[len(value) - 1]
            address_postcode = ""
    elif len(value) == 3:
        address_street = value[0]
        address_county = ""
        address_postcode = re.findall(r'\b[A-Z]{1,2}[0-9][A-Z0-9]? [0-9][ABD-HJLNP-UW-Z]{2}\b',
                                      value[len(value) - 1])
        if not address_postcode:
            address_street = value[0] + ' ' + value[1]
            address_city = value[len(value) - 1]
            address_postcode = ""
        else:
            address_city = value[len(value) - 2]
            address_postcode = address_postcode[0]
    elif len(value) == 4:
        address_street = value[0]
        address_county = value[2]
        address_postcode = re.findall(r'\b[A-Z]{1,2}[0-9][A-Z0-9]? [0-9][ABD-HJLNP-UW-Z]{2}\b',
                                      value[len(value) - 1])
        if not address_postcode:
            address_city = value[len(value) - 1]
            address_postcode = ""
        else:
            address_city = value[len(value) - 2]
            address_postcode = address_postcode[0]
    elif len(value) == 5:
        address_street = value[0] + " " + value[1] + " " + value[2]
        address_county = value[3]
        address_postcode = re.findall(r'\b[A-Z]{1,2}[0-9][A-Z0-9]? [0-9][ABD-HJLNP-UW-Z]{2}\b',
                                      value[len(value) - 1])
        if not address_postcode:
            address_city = value[len(value) - 1]
            address_postcode = ""
        else:
            address_city = value[len(value) - 2]
            address_postcode = address_postcode[0]
    else:
        address_street = ""
        address_county = ""
        address_city = ""
        address_postcode = ""

    return address_street, address_county, address_city, address_postcode


def client_contact(from_):
    if "Lucy Taylor" in from_:
        value = "0033z00002gTwQAAA0"
    elif "Charlotte Lowe" in from_:
        value = "0033z00002gTwQBAA0"
    elif "Sladjana Ugrenovic" in from_:
        value = "0033z00002gTwPlAAK"
    elif "Victoria Rofe" in from_:
        value = "0033z00002gUX7HAAW"
    elif "Jon Tullock" in from_:
        value = "0033z00002gTn9XAAS"
    elif "Emma McGowan" in from_:
        value = "0033z00002gTn9YAAS"
    elif "Raj Ahmed" in from_:
        value = "0033z00002gTnE8AAK"
    elif "Zoe Sant" in from_:
        value = "0033z00002gTn8uAAC"
    elif 'Andrew Wilson' in from_:
        value = "0033z00002r8spUAAQ"
    else:
        raise Exception(" - Robot does not have Contact ID for Contact Name")
    return value


def county_court(text):
    value = get_text_between("Court - ", "Claim Number -", text)

    if "Aberystwyth Justice Centre" in value:
        value2 = "0013z00002PXZoqAAH"
    elif "Barnsley Law Courts" in value:
        value2 = "0013z00002PXZorAAH"
    elif "Barnstaple Magistrates, County and Family Court" in value:
        value2 = "0013z00002PXZosAAH"
    elif "Barrow-in-Furness County Court and Family Court" in value:
        value2 = "0013z00002PXZotAAH"
    elif "Basingstoke County Court and Family Court" in value:
        value2 = "0013z00002PXZouAAH"
    elif "Bedford County Court and Family Court" in value:
        value2 = "0013z00002PXZovAAH"
    elif "Birkenhead County Court and Family Court" in value:
        value2 = "0013z00002PXZowAAH"
    elif "Birmingham Civil and Family Justice Centre" in value:
        value2 = "0013z00002PXZoxAAH"
    elif "Blackpool County Court and Family Court" in value:
        value2 = "0013z00002PXZoyAAH"
    elif "Blackwood Civil and Family Court" in value:
        value2 = "0013z00002PXZozAAH"
    elif "Boston County Court and Family Court" in value:
        value2 = "0013z00002PXZp0AAH"
    elif "Bournemouth and Poole County Court and Family Court" in value:
        value2 = "0013z00002PXZp1AAH"
    elif "Brighton County and Family Court" in value:
        value2 = "0013z00002PXZp2AAH"
    elif "Bristol Civil and Family Justice Centre" in value:
        value2 = "0013z00002PXZp3AAH"
    elif "Bury St Edmunds County Court and Family Court" in value:
        value2 = "0013z00002PXZp4AAH"
    elif "Caernarfon Justice Centre" in value:
        value2 = "0013z00002PXZp5AAH"
    elif "Cambridge County Court and Family Court" in value:
        value2 = "0013z00002PXZp6AAH"
    elif "Canterbury Combined Court Centre" in value:
        value2 = "0013z00002PXZp7AAH"
    elif "Cardiff Civil and Family Justice Centre" in value:
        value2 = "0013z00002PXZp8AAH"
    elif "Carlisle Combined Court" in value:
        value2 = "0013z00002PXZp9AAH"
    elif "Carmarthen County Court and Family Court" in value:
        value2 = "0013z00002PXZpAAAX"
    elif "Chelmsford County and Family Court" in value:
        value2 = "0013z00002PXZpBAAX"
    elif "Chester Civil and Family Justice Centre" in value:
        value2 = "0013z00002PXZpCAAX"
    elif "Chesterfield County Court" in value:
        value2 = "0013z00002PXZpDAAX2"
    elif "Colchester County Court and Family Court" in value:
        value2 = "0013z00002PXZpEAAX"
    elif "Coventry Combined Court Centre" in value:
        value2 = "0013z00002PXZpFAAX"
    elif "Crewe County Court and Family Court" in value:
        value2 = "0013z00002PXZpGAAX"
    elif "Croydon County Court and Family Court" in value:
        value2 = "0013z00002PXZpHAAX"
    elif "Darlington County Court and Family Court" in value:
        value2 = "0013z00002PXZpIAAX"
    elif "Derby Combined Court Centre" in value:
        value2 = "0013z00002PXZpJAAX"
    elif "Doncaster Justice Centre North" in value:
        value2 = "0013z00002PXZpKAAX"
    elif "Dudley County Court and Family Court" in value:
        value2 = "0013z00002PXZpLAAX"
    elif "Durham Justice Centre" in value:
        value2 = "0013z00002PXZpMAAX"
    elif "Exeter Combined Court Centre" in value:
        value2 = "0013z00002PXZpNAAX"
    elif "Gloucester and Cheltenham County and Family Court" in value:
        value2 = "0013z00002PXZpOAAX"
    elif "Great Grimsby Combined Court Centre" in value:
        value2 = "0013z00002PXZpPAAX"
    elif "Guildford County Court and Family Court" in value:
        value2 = "0013z00002PXZpQAAX"
    elif "Harrogate Justice Centre" in value:
        value2 = "0013z00002PXZpRAAX"
    elif "Hastings County Court and Family Court" in value:
        value2 = "0013z00002PXZpSAAX"
    elif "Haverfordwest CountymCourt and Family Court" in value:
        value2 = "0013z00002PXZpTAAX"
    elif "Hereford County Court and Family Court" in value:
        value2 = "0013z00002PXZpUAAX"
    elif "Huddersfield County Court and Family Court" in value:
        value2 = "0013z00002PXZpVAAX"
    elif "Kingston - Upon - Hull Combined Court Centre" in value:
        value2 = "0013z00002PXZpWAAX"
    elif "Lancaster County Court and Family Court" in value:
        value2 = "0013z00002PXZpXAAX"
    elif "Leeds Combined Court Centre" in value:
        value2 = "0013z00002PXZpYAAX"
    elif "Leicester County Court and Family Court" in value:
        value2 = "0013z00002PXZpZAAX"
    elif "Lincoln County Court and Family Court" in value:
        value2 = "0013z00002PXZpaAAH"
    elif "Liverpool Civil and Family Court" in value:
        value2 = "0013z00002PXZpbAAH"
    elif "Luton County Court and Family Court" in value:
        value2 = "0013z00002PXZpcAAH"
    elif "Maidstone Combined Court Centre" in value:
        value2 = "0013z00002PXZpdAAH"
    elif "Manchester County and Family Court" in value:
        value2 = "0013z00002PXZpeAAH"
    elif "Mansfield Magistrates and County Court" in value:
        value2 = "0013z00002PXZpfAAH"
    elif "Medway County Court and Family Court" in value:
        value2 = "0013z00002PXZpgAAH"
    elif "Merthyr Tydfil Combined Court Centre" in value:
        value2 = "0013z00002PXZphAAH"
    elif "Middlesbrough County Court at Teesside Combined Court" in value:
        value2 = "0013z00002PXZpiAAH"
    elif "Milton Keynes County Court and Family Court" in value:
        value2 = "0013z00002PXZpjAAH"
    elif "Newcastle upon Tyne Combined Court Centre" in value:
        value2 = "0013z00002PXZpkAAH"
    elif "Newport (South Wales) County Court and Family Court" in value:
        value2 = "0013z00002PXZplAAH"
    elif "Northampton Crown Court, County Court and Family Court" in value:
        value2 = "0013z00002PXZpmAAH"
    elif "North Shields County Court and Family Court" in value:
        value2 = "0013z00002PXZpnAAH"
    elif "Norwich Combined Court Centre" in value:
        value2 = "0013z00002PXZpoAAH"
    elif "Nottingham County Court and Family Court" in value:
        value2 = "0013z00002PXZppAAH"
    elif "Oxford Combined Court Centre" in value:
        value2 = "0013z00002PXZpqAAH"
    elif "Peterborough Combined Court Centre" in value:
        value2 = "0013z00002PXZprAAH"
    elif "Plymouth Combined Court" in value:
        value2 = "z00002PXZpsAAH"
    elif "Pontypridd County Court and Family Court" in value:
        value2 = "0013z00002PXZptAAH"
    elif "Portsmouth Combined Court Centre" in value:
        value2 = "0013z00002PXZpuAAH"
    elif "Port Talbot Justice Centre" in value:
        value2 = "0013z00002PXZpvAAH"
    elif "Prestatyn Justice Centre" in value:
        value2 = "0013z00002PXZpwAAH"
    elif "Preston Combined Court Centre" in value:
        value2 = "0013z00002PXZpxAAH"
    elif "Reading County Court and Family Court" in value:
        value2 = "0013z00002PXZpyAAH"
    elif "Rolls Building" in value:
        value2 = "0013z00002PXZpzAAH"
    elif "Romford County Court and Family Court" in value:
        value2 = "0013z00002PXZq0AAH"
    elif "Salisbury Law Courts" in value:
        value2 = "0013z00002PXZq1AAH"
    elif "Scarborough Justice Centre" in value:
        value2 = "0013z00002PXZq2AAH"
    elif "Sheffield Combined Court Centre" in value:
        value2 = "0013z00002PXZq3AAH"
    elif "Skipton County Court and Family Court" in value:
        value2 = "0013z00002PXZq4AAH"
    elif "Southampton Combined Court Centre" in value:
        value2 = "0013z00002PXZq5AAH"
    elif "Southend County Court and Family Court" in value:
        value2 = "0013z00002PXZq6AAH"
    elif "South Shields County Court and Family Court" in value:
        value2 = "0013z00002PXZq7AAH"
    elif "Stafford Combined Court Centre" in value:
        value2 = "0013z00002PXZq8AAH"
    elif "St Helen's County Court and Family Court" in value:
        value2 = "0013z00002PXZq9AAH"
    elif "Stockport County Court and Family Court" in value:
        value2 = "0013z00002PXZqAAAX"
    elif "Stoke-on-Trent Combined Court" in value:
        value2 = "0013z00002PXZqBAAX"
    elif "Sunderland County, Family, Magistrates and Tribunal" in value:
        value2 = "0013z00002PXZqCAAX"
    elif "Hearings" in value:
        value2 = "0013z00002PXZqDAAX"
    elif "Swindon Combined Court" in value:
        value2 = "0013z00002PXZqEAAX"
    elif "Taunton Crown, County and Family Court" in value:
        value2 = "0013z00002PXZqFAAX"
    elif "Teesside Combined Court Centre" in value:
        value2 = "0013z00002PXZqGAAX"
    elif "Telford County Court and Family Court" in value:
        value2 = "0013z00002PXZqHAAX"
    elif "Thanet County Court and Family Court" in value:
        value2 = "0013z00002PXZqIAAX"
    elif "Truro County Court and Family Court" in value:
        value2 = "0013z00002PXZqJAAX"
    elif "Wakefield Civil and Family Justice Centre" in value:
        value2 = "0013z00002PXZqKAAX"
    elif "Walsall County and Family Court" in value:
        value2 = "0013z00002PXZqLAAX"
    elif "Weymouth Combined Court" in value:
        value2 = "0013z00002PXZqMAAX"
    elif "Winchester Combined Court Centre" in value:
        value2 = "0013z00002PXZqNAAX"
    elif "Wolverhampton Combined Court Centre" in value:
        value2 = "0013z00002PXZqOAAX"
    elif "Worcester Combined Court" in value:
        value2 = "0013z00002PXZqPAAX"
    elif "Worthing County Court and Family Court" in value:
        value2 = "0013z00002PXZqQAAX"
    elif "Yeovil County, Family and Magistrates' Court" in value:
        value2 = "0013z00002PXZqRAAX"
    elif "York County Court and Family Court" in value:
        value2 = "0013z00002PXZqSAAX"
    elif "Liverpool District Registry" in value:
        value2 = "0013z00002Q0n8cAAB"
    elif 'County Court Money Claims Centre ("CCMCC")' in value:
        value2 = "0013z00002QnrQwAAJ"
    elif 'County Court Bulk Centre ("CCBC")' in value:
        value2 = "0013z00002QnrR5AAJ"
    elif "Clerkenwell and Shoreditch County Court" in value:
        value2 = "0013z00002QoI8UAAV"
    elif "Gloucester and Cheltenham District Registry" in value:
        value2 = "0013z00002QoJCkAAN"
    elif "Central London County Court" in value:
        value2 = "0013z00002SlrpSAAR"
    elif "Royal Courts of Justice" in value:
        value2 = "0013z00002SnITqAAN"
    elif "Cardiff Employment Tribunal" in value:
        value2 = "0013z00002SwAe7AAF"
    elif "East London Tribunal Hearing Centre" in value:
        value2 = "0013z00002SwAmrAAF"
    elif "Exeter Employment Tribunal" in value:
        value2 = "0013z00002SwEtZAAV"
    elif "Bristol Employment Tribunal" in value:
        value2 = "0013z00002SwLlFAAV"
    elif "Bury St Edmunds Employment Tribunal" in value:
        value2 = "0013z00002SwLsIAAV"
    elif "London, Central Employment Tribunal" in value:
        value2 = "0013z00002SwLxzAAF"
    elif "Watford Tribunal Hearing Centre" in value:
        value2 = "0013z00002SwM2vAAF"
    elif "Midlands, East: hearing centre" in value:
        value2 = "0013z00002SwMGRAA3"
    elif "Ashford Tribunal Hearing Centre" in value:
        value2 = "0013z00002VFcKmAAL"
    elif "Boston Employment Tribunal" in value:
        value2 = "0013z00002VFcKwAAL"
    elif "Carlisle Employment Tribunal" in value:
        value2 = "0013z00002VFcLfAAL"
    elif "Leeds Employment Tribunal" in value:
        value2 = "0013z00002VFcLkAAL"
    elif "Leicester Employment Tribunal" in value:
        value2 = "0013z00002VFcMBAA1"
    elif "Manchester Employment Tribunal" in value:
        value2 = "0013z00002VFcOCAA1"
    elif "Newcastle Employment Tribunal" in value:
        value2 = "0013z00002VFcOWAA1"
    elif "Kingston upon Thames County Court and Family Court" in value:
        value2 = "0013z00002VH5Q2AAL"
    elif "Watford County Court and Family Court" in value:
        value2 = "0013z00002VH7snAAD"
    elif "Bristol District Registry" in value:
        value2 = "0013z00002VHc8CAAT"
    elif "Birmingham Employment Tribunal" in value:
        value2 = "0013z00002VHmNmAAL"
    elif "Cambridge Employment Tribunal" in value:
        value2 = "0013z00002VHmvLAAT"
    else:
        raise Exception(" - County Court is not in or does not match to look-up")

    return value2
