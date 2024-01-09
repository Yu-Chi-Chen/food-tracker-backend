class DataService:
    def __init__(self, firebase):
        self.firebase = firebase

    def get_food_data(self, food_id):
        return self.firebase.get_food_data(food_id)

    def get_user_data(self, uid):
        return self.firebase.get_user_data(uid)

    def get_user_info(self, uid):
        user_data = self.firebase.get_user_data(uid)
        food_to_avoid = self.firebase.get_disease_info(user_data['disease'])

        return dict(food_to_avoid), user_data['disease']
