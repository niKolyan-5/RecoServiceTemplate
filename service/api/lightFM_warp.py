import pickle


class LightFM_warp_64_05_16():

    def __init__(self):
        super().__init__()

        self.model = pickle.load(open('service/api/weights/LightFM_warp_64_05_16.pickle', 'rb'))
        self.dataset = pickle.load(open('service/api/weights/dataset.pickle', 'rb'))
        
        self.popular_recs_all_time = [202457, 193123, 132865, 122119, 91167, 74803, 68581, 55043, 45367, 40372]
        self.popular_recs_month  = [59226, 54373, 54115, 27752, 23812, 23253, 20967, 18909, 18878, 13305]


    def recommend_(self, user_id: int, k: int = 10):

        try:
            reco = self.model.recommend([user_id], dataset=self.dataset, k=k, filter_viewed=True)
            reco = list(reco['item_id'])
            # print(reco)
        except:
            # reco = self.popular_recs_all_time
            reco = self.popular_recs_month

        return reco


class LightFM_off:
    def __init__(self):
        super().__init__()

        with open('service/api/weights/LFM_model.pickle', 'rb') as f:
            self.model = pickle.load(f)

    def recommend_(self, user_id: int, k: int = 10):
        
        # print(self.model)
        try:
            reco = self.model['item_id'][user_id]
        except:
            reco = [10440, 9728, 15297, 13865, 12192, 341, 4151, 3734, 12360, 7793]

        print('RECO', reco)

        return reco