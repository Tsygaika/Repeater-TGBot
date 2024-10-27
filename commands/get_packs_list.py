#используется только тогда, когда есть хотя бы одна колода
import pandas as pd

def get_packs_list(message, way_to_data):
    df = pd.read_csv(way_to_data, converters={'pack_name' : str,'front_word' : str,'back_word' : str})
    df = df.loc[df['tg_id'] == message.chat.id]    #оставляем колоды только этого пользователя
    packs_list = df['pack_name'].astype('str').unique() #читает столбец с типом str
    return packs_list