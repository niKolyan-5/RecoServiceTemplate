import dill
import pickle


class LGBMRankerModel():
    def __init__(self):
        super().__init__()

        self.model = dill.load(open('service/weights/lgbm_ranker_model.dill', 'rb'))
        self.popular_model = dill.load(open('service/weights/pop_model.dill', 'rb'))
        self.dataset = pickle.load(open('service/weights/dataset.pickle', 'rb'))

    def recommend_(self, user_id: int, k: int = 10):

        try:
            reco = self.model.predict([user_id])[:k]
            # reco = list(reco['item_id'])
            # print(reco)
        except:
            # reco = self.popular_recs_all_time
            reco = self.popular_model.recommend([user_id], 
                                                dataset=self.dataset, 
                                                k=k, 
                                                filter_viewed=False)

        return reco
