import random
from app.models.user import User

class DataManager:
    def getQuestion(self, subject="name"):
        rawdata = self.__getdata()
        question = self.__formatdata(rawdata, subject)
        return question

    def __getdata(self):
        pipeline = [{"$match": {"domains": {"$exists": True, "$ne": [] }}}, {"$sample": {"size": 4}}]
        random_users = list(User.objects.aggregate(*pipeline))
        return random_users

    def __formatdata(self, data: list, view: str):
        holdingcell = []
        for row in data:
            name_domain = (row['name'], random.choice(row['domains']))
            holdingcell.append(name_domain)

        if not holdingcell:
            return {'status': False, 'message': 'No data found'}

        random_row = random.choice(holdingcell)
        index = holdingcell.index(random_row)

        if view == "name":
            subject = random_row[0]
            choices = [tup[1] for tup in holdingcell]
            question = f"Select the domain owned by {subject}"
        else:
            subject = random_row[1]
            choices = [tup[0] for tup in holdingcell]
            question = f"Select the owner of domain {subject}"

        return {"status": True, "subject": subject, "choices": choices, "index": index, "question": question}