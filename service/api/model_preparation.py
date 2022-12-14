import dill

#загрузка моделей из файлов
with open('service/api/models/popular_model.dill', 'rb') as f:
    popular_recos = dill.load(f)

with open('service/api/models/bm25userknn.dill', 'rb') as f:
    bm25model = dill.load(f)

bm25model = bm25model['item_id']
