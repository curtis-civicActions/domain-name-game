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

    def insertdata(self, data: dict):
        # Check if this user exists
        response = {'status': False, 'message': f"{data['name']} failed to be inserted or updates!"}

        # Explicitly calling .filter() forces MongoEngine to construct a standard
        # QuerySet rather than falling back on an overridden __call__ method
        if User.objects.filter(name=data["name"]).count() > 0:
            user = User.objects.get(name=data["name"])
            # Update the domain list making sure the resulting array has unique values
            User.objects(id=user.id).update(add_to_set__domains=data['domains'])
            user.reload()
            message = f"{data['name']} was successfully updated."
            response = {'status': True, 'message': message}
        else:
            user = User(name=data["name"], domains=data["domains"])
            user.save()
            message = f"{data['name']} was successfully added."
            response = {'status': True, 'message': message}

        return response
