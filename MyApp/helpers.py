from _datetime import datetime

governorates_code = {
                '01': 'Cairo',
                '02': 'Alexandria',
                '03': 'Port Said',
                '04': 'Suez',
                '11': 'Damietta',
                '12': 'Dakahlia',
                '13': 'Ash Sharqia',
                '14': 'Kaliobeya',
                '15': 'Kafr El - Sheikh',
                '16': 'Gharbia',
                '17': 'Monoufia',
                '18': 'El Beheira',
                '19': 'Ismailia',
                '21': 'Giza',
                '22': 'Beni Suef',
                '23': 'Fayoum',
                '24': 'El Menia',
                '25': 'Assiut',
                '26': 'Sohag',
                '27': 'Qena',
                '28': 'Aswan',
                '29': 'Luxor',
                '31': 'Red Sea',
                '32': 'New Valley',
                '33': 'Matrouh',
                '34': 'North Sinai',
                '35': 'South Sinai',
                '88': 'Foreign'
                }

def validate(national_id):
    # Validates the id number parts
    # Returns:
    # bool: True if it is a valid egyptian id number, False if not
    
    if not all([national_id.isdigit(), len(national_id) == 14]):
        return False

    

    century = int(national_id[0])
    year = int(national_id[1:3])
    month = int(national_id[3:5])
    day = int(national_id[5:7])
    governorate = int(national_id[7:9])
    unique_num = int(national_id[9:13])
    verification_digit = int(national_id[13])
     
    current_datetime = datetime.now()

    century_check = century in [2, 3]  # we will deal with 1900 ~ 2099
    #year_check = (
        #(year <= current_datetime.year - 2000) if century == 3 else True)  # can't be in the future
    month_check = month in range(1, 12)
    if not month in range(1,13):
        return False
    
    # check for months that have 31 day and febuary which is 28 or 29
    if month in [1, 3, 5, 7, 8, 10, 12]:
        if not day in range(1, 32):
            return False
        #day_check = day in range(1, 32)
    

    elif month in [4, 6, 9, 11]:
        if not day in range(1, 31):
            return False
        #day_check = day in range(1, 31)
    

    elif month == 2:
        if not day in range(29):
            return False
        #day_check = day in range(30) if year % 4 == 0 else day in range(29)
    

    else:
        return False
    
    if not f'{governorate}' in governorates_code:
        return False

    # Process the data from the id number into readable format
    # Returns:
    # tuple(bool, str): True if valid_id else False, json string for the collective information that will return to user
     
    id_owner_data = {}
    id_owner_data["year_of_birth"] = f"20{year}" if century == 3 else f"19{year}"
    id_owner_data["month_of_birth"] = f"{month}"
    id_owner_data["day_of_birth"] = f"{day}"
    id_owner_data["governorate"] = governorates_code[f'{governorate}']
    id_owner_data["type"] = "Male" if unique_num % 2 != 0 else "Female"

    return id_owner_data