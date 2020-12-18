from ast import literal_eval
import pandas as pd


def genres_process(Genres):
    # Transformar a list string to a string list and put it into another list
    flat_list = []
    for sublist in Genres:
        sublist = literal_eval(sublist)
        for item in sublist:
            flat_list.append(item)

    # get the unique genres
    generosUnicos = []
    for x in flat_list:
        # check if exists in unique_list or not
        if x not in generosUnicos:
            generosUnicos.append(x)
    # get the value_counts of the genres
    num = pd.Series(flat_list).value_counts()
    return num, generosUnicos

#combine two columns
def get_new_columns(l1,l2):
    l1[len(l1):len(l1)] = l2
    return l1

#Anilist data preprocess
def Anilist_process(df):
    df = df.rename(columns={'Unnamed: 0': 'rank'})
    df.loc[:, 'rank'] += 1
    df2=df.copy()
    #get the processed genres
    num,genres=genres_process(df.Genres)
    df2.loc[:,'Percentage']=df.loc[:,'Percentage'].apply(lambda x:int(x.replace('%','')))
    df2.loc[:,'episodes']=df.loc[:,'episodes'].apply(lambda x:x.split()[0])
    AnilistFinal=pd.DataFrame(columns=get_new_columns(list(df2.columns),genres))
    count = 0
    for index, row in df2.iterrows():
        count += 1
        for item in genres:
            if item in row.Genres:
                row[item] = 1
            else:
                row[item] = 0
        #form a new dataframe that store the processed data
        AnilistFinal = AnilistFinal.append(row, ignore_index=True)
        # print(count)
    AnilistFinal.to_csv('../data/processed_Anilist_Data.csv',index=False)
    return AnilistFinal

#Myanimelist anime data preprocess
def Myani_ani_process(df):
    df = df.rename(columns={'Unnamed: 0': 'rank'})
    df.loc[:, 'rank'] += 1
    df2 = df.copy()
    df2['eps'] = ''
    num, genres = genres_process(df.Genres)
    #process the data
    df2.loc[:, 'Favorites'] = df.loc[:, 'Favorites'].apply(lambda x: int(x.replace(',', '')))
    df2.loc[:, 'Watching'] = df.loc[:, 'Watching'].apply(lambda x: int(x.replace(',', '')))
    df2.loc[:, 'Completed'] = df.loc[:, 'Completed'].apply(lambda x: int(x.replace(',', '')))
    df2.loc[:, 'On-Hold'] = df.loc[:, 'On-Hold'].apply(lambda x: int(x.replace(',', '')))
    df2.loc[:, 'Dropped'] = df.loc[:, 'Dropped'].apply(lambda x: int(x.replace(',', '')))
    df2.loc[:, 'Plan_to_Watch'] = df.loc[:, 'Plan_to_Watch'].apply(lambda x: int(x.replace(',', '')))
    df2.loc[:, 'Total'] = df.loc[:, 'Total'].apply(lambda x: int(x.replace(',', '')))
    df2.loc[:, 'members'] = df.loc[:, 'members'].apply(lambda x: int(x.split()[0].replace(',', '')))
    df2.loc[:, 'type'] = df.loc[:, 'type'].apply(lambda x: x.split()[0])
    df2.loc[:,'eps']=df.loc[:,'type'].apply(lambda x:int(x.split()[1].replace('(','').replace('?','0')))
    # form a new dataframe that store the processed data
    AnimesFinal = pd.DataFrame(columns=get_new_columns(list(df2.columns), genres))
    count = 0
    for index, row in df2.iterrows():
        count += 1
        for item in genres:
            if item in row.Genres:
                row[item] = 1
            else:
                row[item] = 0
        #     print(row)
        AnimesFinal = AnimesFinal.append(row, ignore_index=True)
        #     print(AnimesFinal)
        # print(count)
    AnimesFinal.to_csv('../data/processed_Myanimelist_anime_Data.csv',index=False)
    return AnimesFinal

def manga_genres_process(x):
    l=literal_eval(x)
    genres=[]
    for i in l:
#         print(i)
        genres.append(i['name'])
    # print(genres)
    return genres


#Myanimelist manga data preprocess
def Myani_man_process(df):
    df=df.drop('Unnamed: 0', axis=1)
    flat_list = []
    df['Genres'] = ''
    for i in range(len(df.genres)):
        df['Genres'][i] = manga_genres_process(df['genres'][i])

    for l in df.Genres:
        for i in l:
            flat_list.append(i)
    genres_unique = []
    for i in flat_list:
        if i not in genres_unique:
            genres_unique.append(i)
    num=pd.Series(flat_list).value_counts()
    MymangaFinal = pd.DataFrame(columns=get_new_columns(list(df.columns), genres_unique))
    count = 0
    for index, row in df.iterrows():
        count += 1
        for item in genres_unique:
            if item in row.Genres:
                row[item] = 1
            else:
                row[item] = 0
        #     print(row)
        MymangaFinal = MymangaFinal.append(row, ignore_index=True)
        print(count)
    MymangaFinal.to_csv('../data/processed_Myanimelist_manga_Data.csv',index=False)
    return MymangaFinal




#Wikipedia manga sales data preprocess
def Wiki_man_sales_process(df):
    df = df.rename(columns={'Unnamed: 0': 'rank'})
    df.loc[:, 'rank'] += 1
    df.to_csv('../data/processed_Wikipedia_manga_sales_Data.csv',index=False)
    return df



