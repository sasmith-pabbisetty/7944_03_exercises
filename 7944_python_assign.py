# import pandas, numpy and datetime
import pandas as pd
import numpy as np
from datetime import datetime 


# To read the 'SaleData'
df = pd.read_excel('SaleData.xlsx')

# To read the 'imdb.csv'
df= pd.read_csv("imdb.csv",escapechar="\\")

#To read 'diamonds.csv'
df = pd.read_csv("diamonds.csv")



# Q1 Find least sales amount for each item
def least_sales(df):
    ls = df.groupby(["Item"])["Sale_amt"].min()
    return ls


#question 2
def sales_year_region(df):
    df_copy = df.copy()
    df_copy['year'] = df_copy['OrderDate'].apply(lambda x:x.year)
    ls = df_copy.groupby(["year","Region"])["Sale_amt"].sum()
    return ls


# Q3 append column with no of days difference from present date to each order date
def days_diff(df,date):
    df['OrderDate'] = pd.to_datetime(df['OrderDate'])
    df['days_diff'] = df['OrderDate'].apply(lambda x:(date-x).days)
    return df


# Q4 get dataframe with manager as first column and  salesman under them as lists in rows in second column.
def mgr_slsmn(df):
    df_copy = df.groupby(["Manager","SalesMan"]).describe()
    df_copy.drop(columns=['Units','Unit_price','Sale_amt'],inplace=True)
    return df_copy



# Q5 For all regions find number of salesman and number of units
def slsmn_units(df):
    df_copy = df.groupby(["Region"]).agg({'SalesMan':'count','Sale_amt':'sum'}).reset_index().rename(columns={'SalesMan':'SalesMan_count','Sale_amt':'Total_Sales'})
    return df_copy



# Q6 Find total sales as percentage for each manager
def sales_pct(df):
    total_sales = df["Sale_amt"].sum()
    df_copy = df.groupby(["Manager"])["Sale_amt"].sum()
    df_copy = (df_copy/total_sales)*100
    return df_copy



# Q7 get imdb rating for fifth movie of dataframe
def fifth_movie(df):
    return df[df['type'] == 'video.movie'].reset_index().iloc[4]['imdbRating']



# Q8 return titles of movies with shortest and longest run time
def movies(df):
    df_copy = df[df["type"] == 'video.movie']
    ls = df_copy[(df_copy["duration"] == df_copy["duration"].min()) | (df_copy["duration"] == df_copy["duration"].max())]['title']
    return ls



# Q9 sort by two columns - release_date (earliest) and Imdb rating(highest to lowest)
def sort_df(df):
    df_copy = df.sort_values(by=['year','imdbRating'],ascending=[True,False])
    return df_copy



# Q10 subset revenue more than 2 million and spent less than 1 million & duration between 30 mintues to 180 minutes
def subset_df(df):
    df_copy = df[(df['duration']>30) & (df['duration'] < 180) & (df['gross'] < 2000000) & (df['budget] < 1000000)]
    return df_copy



# Q11 count the duplicate rows of diamonds DataFrame.
def dupl_rows(df):
    c = len(df) - len(df.drop_duplicates())
    return c




# Q12 droping those rows where any value in a row is missing in carat and cut columns
def drop_row(df):
    df = df.dropna(how='any',subset=['carat','cut'])
    print(df.head())



# Q13 subset only numeric columns
def sub_numeric(df):
    df = df._get_numeric_data()
    print(df.head())




def vol(df1):
    if df1['depth'] > 60:
        x = pd.to_numeric(df1['x'],errors='coerce')
        y = pd.to_numeric(df1['y'],errors='coerce')
        z = pd.to_numeric(df1['z'],errors='coerce')
        return x*y*z
    else:
        return 8
    

# Q14 compute volume as (x*y*z) when depth > 60 else 8
def volume(df):
    df['volume'] = df.apply(vol,axis = 1)
    print(df.head())



# Q15 impute missing price values with mean
def impute(df):
    df['price'].fillna(value = df['price'].mean()) 
    print(df.head())



############################Bonus questions#################################################


"""
Q1
Generate a report that tracks the various Genere combinations for each type year on year. The result
data frame should contain type, Genere_combo, year, avg_rating, min_rating, max_rating,
total_run_time_mins
"""

def bonus1(df):
    df1 = df.groupby('year').sum()
    df1.drop(columns={'imdbRating', 'ratingCount', 'duration', 'nrOfWins', 'nrOfNominations',
       'nrOfPhotos', 'nrOfNewsArticles', 'nrOfUserReviews', 'nrOfGenre'},inplace=True)
    df1['genre_combo'] = df1.apply(lambda x: '|'.join(x.index[x>= 1]), axis=1)
    df2=df.groupby(['year','type'])['imdbRating'].agg([('avg_rating','mean'),('min_rating','min'),('max_rating','max')])
    df3=df.groupby(['year','type'])['duration'].agg([('total_run_time_mins','sum')])
    df4=pd.merge(df2,df3,on=['year','type'])
    df1.reset_index()
    res=pd.merge(df4,df1['genre_combo'],on=['year'])
    return res

"""
Q2
Is there a realation between the length of a movie title and the ratings ? Generate a report that captures
the trend of the number of letters in movies titles over years. We expect a cross tab between the year of
the video release and the quantile that length fall under. The results should contain year, min_length,
max_length, num_videos_less_than25Percentile, num_videos_25_50Percentile ,
num_videos_50_75Percentile, num_videos_greaterthan75Precentile
"""
def bonus2(df):
    df1 = df.copy()
    df1['title_len'] = df['wordsInTitle'].str.len()
    df['title_len'].corr(df['imdbRating'])
    df2=df1.groupby('year')['title_len'].agg([('min_length','min'),('max_length','max')])
    df3=df1.groupby('year')['title_len'].describe().drop(['count','mean','std','min','max'],axis=1).reset_index()
    df4= pd.merge(df2,df3,on='year')
    df4= pd.merge(df1,df4,on='year')
    df4['num_videos_less_than25Percentile']=(df4['title_len']<df4['25%'])*1
    df4['num_videos_25_50Percentile']=((df4['title_len']>=df4['25%'])&(df4['title_len']<=df4['50%']))*1
    df4['num_videos_50_75Percentile']=((df4['title_len']>df4['50%'])&(df4['title_len']<=df4['75%']))*1
    df4['num_videos_greaterthan75Precentile']=(df4['title_len']>df4['75%'])*1
    df5=df4.groupby('year')['num_videos_less_than25Percentile','num_videos_25_50Percentile','num_videos_50_75Percentile','num_videos_greaterthan75Precentile'].agg([('count','sum')])
    res=pd.merge(df2,df5,on='year').reset_index()
    return res


"""
Q3
In diamonds data set Using the volumne calculated above, create bins that have equal population within
them. Generate a report that contains cross tab between bins and cut. Represent the number under
each cell as a percentage of total.
"""
def bonus3(df):
    df['bins'] = pd.qcut(df['volume'],q=4)
    df1 = pd.crosstab(df.bins,df.cut,normalize=True)
    return df1

"""
Q4
Generate a report that tracks the Avg. imdb rating quarter on quarter, in the last 10 years, for movies
that are top performing. You can take the top 10% grossing movies every quarter. Add the number of top
performing movies under each genere in the report as well
"""
def bonus4(df):
   df1=(df.groupby('title_year',group_keys=False).apply(lambda x: x.nlargest(int(len(x)*0.1),'gross'))).reset_index()
   df2=df1.groupby('title_year')['imdb_score'].mean().reset_index()
   df2.rename(columns={'imdb_score':'Avg_imdb_score'},inplace=True)
   df3=df1.genres.str.get_dummies('|')
   df4=pd.merge(df1.title_year,df3,on=None,left_index=True,right_index=True)
   df4=df4.groupby('title_year').sum()
   df5=pd.merge(df2,df4,on='title_year')
   df5=(df5[df5.title_year>df5.title_year.max()-10]).reset_index()
   return df5


"""
Q5
Bucket the movies into deciles using the duration. Generate the report that tracks various features like
nomiations, wins, count, top 3 geners in each decile.
"""
def bonus5(df):
   df['deciles']=pd.qcut(df['duration'], 10)
   df1=df.iloc[:,17:]
   df2=df1.groupby('deciles')[df1.columns.tolist()[1:28]].sum()
   df3=df2.T
   df3=df3.apply(lambda x: x.nlargest(3).index).T
   df3.columns=['Top1','Top2','Top3']
   df4=df.groupby('deciles')['nrOfNominations','nrOfWins'].sum()
   df5=pd.merge(df3,df4,on='deciles')
   return df5
