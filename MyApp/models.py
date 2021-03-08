from django.db import models
from django.db.models.functions import datetime

# Create your models here.
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



class National_ID(models.Model):
    #national_id = models.BigIntegerField(max_length=14)
    national_id = "29001011234567"

    '''National ID class, will include the skelton of it's properties
    and verification.
    '''
    # class Meta:
    #     verbose_name = 'the one person id'
    #     verbose_name_plural = 'people IDs'



    def __init__(self , national_id):
    ## national_id (int): Egyptian national id number 
        self.national_id = national_id

    def _validate(self):
        # Validates the id number parts
        # Returns:
        # bool: True if it is a valid egyptian id number, False if not
        
        if not all([self.national_id.isdigit(), len(self.national_id) == 14]):
            return False

        self.century = int(self.national_id[0])
        self.year = int(self.national_id[1:3])
        self.month = int(self.national_id[3:5])
        self.day = int(self.national_id[5:7])
        self.governorate = int(self.national_id[7:9])
        self.unique_num = int(self.national_id[9:13])
        self.verification_digit = int(self.national_id[13])

        current_datetime = datetime.now()

        century_check = self.century in [2, 3]  # we will deal with 1900 ~ 2099
        year_check = (
            (self.year <= current_datetime.year - 2000) if self.century == 3 else True)  # can't be in the future
        month_check = self.month in range(1, 13)

        # check for months that have 31 day and febuary which is 28 or 29
        if self.month in [1, 3, 5, 7, 8, 10, 12]:
            day_check = self.day in range(1, 32)
        elif self.month in [4, 6, 9, 11]:
            day_check = self.day in range(1, 31)
        elif self.month == 2:
            day_check = self.day in range(30) if self.year % 4 == 0 else self.day in range(29)
        else:
            day_check = False

        governorate_check = self.governorate in governorates_code
        return all([century_check, year_check, month_check, day_check, governorate_check])

    def get_info(self):
        # Process the data from the id number into readable format
        # Returns:
        # tuple(bool, str): True if valid_id else False, json string for the collective information that will return to user
        
        id_owner_data = {}
        if not self._validate():
            number_error_msg = f"Invalid national ID number: {self.id_number}. Please enter the correct one"
            return False, {"error": number_error_msg}

        id_owner_data["year_of_birth"] = f"20{self.year}" if self.century == 3 else f"19{self.year}"
        id_owner_data["month_of_birth"] = f"{self.month}"
        id_owner_data["day_of_birth"] = f"{self.day}"
        id_owner_data["governorate"] = governorates_code[self.governorate]
        id_owner_data["type"] = "Male" if self.unique_num % 2 != 0 else "Female"

        return True, id_owner_data
