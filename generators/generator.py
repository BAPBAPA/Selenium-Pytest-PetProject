from faker import Faker


class Fake:

    def __init__(self, lang):
        self.fake = Faker(lang)

    def create_full_name(self):

        return ' '.join([self.fake.first_name(), self.fake.last_name()])

    def create_email(self):

        return self.fake.email()

    def create_password(self):

        return self.fake.password()
