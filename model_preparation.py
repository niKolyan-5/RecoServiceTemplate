import dill

#загрузка моделей из файлов
with open('popular_model.dill', 'rb') as f:
    popular_recos = dill.load(f)

with open('bm25userknn.dill', 'rb') as f:
    bm25model = dill.load(f)

bm25model = bm25model['item_id']

#with open('userknndict.dill', 'rb') as f:
#    userknndict = dill.load(f)
#userknndict = userknndict['item_id']
