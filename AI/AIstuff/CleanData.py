import pandas as pd
import hashlib
from sklearn.preprocessing import OneHotEncoder,MinMaxScaler

inputfile = './Results/Joined/combined_final.csv'
outputfile = './Results/Cleaned/final_final_df.csv'


#need to do
# normalize integer data
# remove unwanted features
# convert text based feature



#   Column                        Non-Null Count  Dtype
# ---  ------                        --------------  -----
#  0   URL                           464 non-null    object
#  1   Total URL length              464 non-null    int64
#  2   netloc length                 464 non-null    int64
#  3   Query Length                  464 non-null    int64
#  4   count digits                  464 non-null    int64
#  5   count reserved char           464 non-null    int64
#  6   has https                     464 non-null    int64
#  7   Country Code TLD              464 non-null    object
#  8   Generic TLD                   464 non-null    object
#  9   is shortened TLD              464 non-null    int64
#  10  has Port                      464 non-null    int64
#  11  has username                  464 non-null    int64
#  12  has fragments                 464 non-null    int64
#  13  num queries (count =)         464 non-null    int64
#  14  URL encoding                  464 non-null    int64
#  15  Path length                   464 non-null    int64
#  16  Path depth                    464 non-null    int64
#  17  Path digit counts             464 non-null    int64
#  18  Path special character count  464 non-null    int64
#  19  Page title                    444 non-null    object
#  20  mimeType                      464 non-null    object
#  21  status                        464 non-null    float64
#  22  redirected                    376 non-null    object
#  23  ranking                       425 non-null    float64
#  24  country                       432 non-null    object
#  25  server                        340 non-null    object
#  26  tlsIssuer                     463 non-null    object
#  27  tlsValidDays                  463 non-null    float64
#  28  numRequest                    464 non-null    float64
#  29  num Links                     464 non-null    float64
#  30  num Cookies                   464 non-null    float64
#  31  num Console Msg               464 non-null    float64
#  32  urlscan Score                 464 non-null    float64
#  33  urlscan category              464 non-null    object

def featureHashing(word):
    hashed_value = int(hashlib.sha256(word.encode('utf-8')).hexdigest(), 16) % 10 ** 8
    return hashed_value


def check_extension(url):
    if url.endswith('.exe') or url.endswith('.php'):
        return 1
    else:
        return 0

normalize = ['Total URL length',
             'netloc length',
             'Query Length',
             'count digits',
             'count reserved char',
             'num queries (count =)',
             'URL encoding',
             'Path length',
             'Path depth',
             'Path digit counts',
             'Path special character count',
             'ranking',
             'tlsValidDays',
             'numRequest',
             'num Links',
             'num Cookies',
             'num Console Msg',
             ]

scaler = MinMaxScaler()

def clean_data(inputfile):
    df = pd.read_csv(inputfile)

    df['exe_or_php'] = df['URL'].apply(check_extension)
    # drop unwanted columns
    df = df.drop(columns=['URL',
                      # 'Country Code TLD',
                      'Generic TLD',
                      'server',
                      'tlsIssuer',
                      'urlscan Score',
                      'urlscan category'
                      ])

    #change some types
    # page title to binary if exist
    # mimeType if it is text/html
    # redirected if it exist
    df['Page title'] = df['Page title'].notnull().astype(int)

    df['mimeType'] = (df['mimeType'] == 'text/html').astype(int)
    df['redirected'] = df['redirected'].notnull().astype(int)
    df['tlsValidDays'].fillna(0, inplace=True)
    df['ranking'].fillna(999999, inplace=True)

    df[normalize] = scaler.fit_transform(df[normalize])


    #hash country
    df['country'].fillna('NaN',inplace=True)
    df['country'] = df['country'].apply(featureHashing)
    df['Country Code TLD'] = df['Country Code TLD'].apply(featureHashing)



    #run check
    print(df.isnull().sum())
    print('-'*25)
    print(df.head())
    print(df.shape)

    return df


def clean_data_test(df):
    # drop unwanted columns
    df['exe_or_php'] = df['URL'].apply(check_extension)

    df = df.drop(columns=['URL',
                          # 'Country Code TLD',
                          'Generic TLD',
                          'server',
                          'tlsIssuer',
                          'urlscan Score',
                          'urlscan category'
                          ])

    df['Page title'] = df['Page title'].notnull().astype(int)
    df['mimeType'] = (df['mimeType'] == 'text/html').astype(int)
    df['redirected'] = df['redirected'].notnull().astype(int)
    df['tlsValidDays'].fillna(0, inplace=True)
    df['ranking'].fillna(999999, inplace=True)
    # hash country
    df['country'].fillna('NaN', inplace=True)
    df['country'] = df['country'].apply(featureHashing)
    df['Country Code TLD'] = df['Country Code TLD'].apply(featureHashing)
    return df


if __name__ == '__main__':
    clean_data(inputfile).to_csv(outputfile, index=False)