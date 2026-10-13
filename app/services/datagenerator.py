from flask import current_app
from faker import Faker
from app.models.user import User
from app.extensions import get_google_service_client
import random


class DataGenerator:
    def generate_data(self, source= "internal", toDb=False):
        fake = Faker()
        data = {}
        if (source == "internal"):
            while len(data) < 10:
                name = self.__generate_name(fake)
                domains = self.__generate_domain(fake)
                if name not in data.keys():
                    data[name] = domains
        else:
            data = self.__load_spreadsheet_data()


        if toDb:
            self.__clear_database()
            return self.__load_database(data)
        else:
            return {"status": "Success", "target": "page", "data": data}

    def __generate_name(self, fake: Faker):
        return fake.name()

    def __generate_domain(self, fake: Faker):
        list_domain = []
        for _ in range(random.randint(1, 5)):
            list_domain.append(fake.domain_name(levels=2))

        return list_domain

    def __load_spreadsheet_data(self):
        sheet_id = current_app.config.get('GOOGLE_SPREADSHEET_ID')
        sheet_client = get_google_service_client()
        spreadsheet = sheet_client.open_by_key(sheet_id)
        spreadsheet_data = spreadsheet.sheet1.get_all_values()
        rawdata = {}
        current_name = 'unknown'

        print(spreadsheet_data)
        for row in spreadsheet_data:
            # Name will be set to unknown if the first row is blank
            current_name = row[0] if len(row[0]) > 0 else current_name
            domains = list(filter(None, (item.strip() for item in row[1].split(","))))

            if current_name in rawdata.keys():
                rawdata[current_name].extend(domains)
            else:
                rawdata[current_name] = domains

        return rawdata

        return spreadsheet_data


    def __load_database(self, data_to_load: dict):
        for username, user_domains in data_to_load.items():
            user = User(name=username, domains=user_domains)
            user.save()

        return {"status": "Success", "target": "database", "message": "Database loaded"}

    def __clear_database(self):
        User.objects.all().delete()

