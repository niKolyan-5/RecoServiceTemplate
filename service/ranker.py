import dill
import pickle
import pandas as pd

class LightFM_warp_64_05_16_:
    def __init__(self):
        super().__init__()

        with open('service/api/weights/LFM_model.pickle', 'rb') as f:
            self.model = pickle.load(f)

        self.popular_model = dill.load(open('service/weights/pop_model.dill', 'rb'))
        self.dataset = pickle.load(open('service/weights/dataset.pickle', 'rb'))

    def recommend_(self, user_id: int, k: int = 10):
 
        try:
            reco = self.model[user_id]
        except:
            reco = self.popular_model.recommend([user_id], 
                                                dataset=self.dataset, 
                                                k=k, 
                                                filter_viewed=False)

        # print('RECO', reco)

        return reco

class LGBMRankerModel():
    def __init__(self):
        super().__init__()

        self.model = dill.load(open('service/weights/lgbm_ranker_model.dill', 'rb'))
        self.ranker_data = pd.read_csv('service/weights/ranker_data.csv')

        self.cols = ['lfm_score', 'lfm_rank', 'als_score', 'als_rank', 'popular_score', 'popular_rank',  
                     'age', 'income', 'sex', 'kids_flg', 'user_hist', 'user_avg_pop', 'user_last_pop',
                     'content_type', 'release_year', 'for_kids', 'age_rating', 'studios', 'item_pop', 'item_avg_hist',
        ]

    def recommend_(self, user_id: int, k: int = 10):

        user_ranker_data = self.ranker_data[self.ranker_data['user_id'] == user_id]

        reco = self.model.predict(user_ranker_data[self.cols])[:k]

        return reco
