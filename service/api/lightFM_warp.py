import pickle


class LightFM_warp_64_05_16():
    
    def __init__(self):
        super().__init__()

        self.model = pickle.load(open('service/api/weights/LightFM_warp_64_05_16.pickle', 'rb'))
        self.dataset = pickle.load(open('service/api/weights/dataset.pickle', 'rb'))


    def recommend(self, user_id: int, k: int = 10):

        reco = self.model.recommend_to_items([user_id], dataset=self.dataset, k=k)
        reco = list(reco['item_id'])
        print(reco)

        return reco