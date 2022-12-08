import dill
import pandas as pd
from rectools import Columns
from rectools.dataset import Dataset

#подготовка датасета
interactions = pd.read_csv('interactions.csv')
users = pd.read_csv('users.csv')
items = pd.read_csv('items.csv')

interactions.rename(columns={'last_watch_dt': Columns.Datetime,
                            'total_dur': Columns.Weight}, 
                    inplace=True) 

interactions['datetime'] = pd.to_datetime(interactions['datetime'])


_, bins = pd.qcut(items["release_year"], 10, retbins=True)
labels = bins[:-1]

year_feature = pd.DataFrame(
    {
        "id": items["item_id"],
        "value": pd.cut(items["release_year"], bins=bins, labels=labels),
        "feature": "release_year",
    }
)

items["genre"] = items["genres"].str.split(",")
items[["genre", "genres"]].head(3)

genre_feature = items[["item_id", "genre"]].explode("genre")
genre_feature.columns = ["id", "value"]
genre_feature["feature"] = "genre"

item_feat = pd.concat([genre_feature, year_feature])
item_feat = item_feat[item_feat['id'].isin(interactions['item_id'])]

dataset = Dataset.construct(
      interactions_df=interactions,
      user_features_df=None,
      item_features_df=item_feat,
      cat_item_features=['genre', 'release_year']
)

#загрузка модели из pop.dill
with open('pop.dill', 'rb') as f:
    ordinary_popular = dill.load(f)
