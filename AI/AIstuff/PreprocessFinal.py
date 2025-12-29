import pandas as pd

import LexicalFeature
import HostBasedFeature

INPUTFILE = "./Data/CLeanURL.csv"
OUTPUTFILE = "./Cleaned_URL_1.csv"

def get_features(url):
    Features = {}
    Lexical = LexicalFeature.lexical_feature(url)
    Host = HostBasedFeature.run_urlscan_api(url)

    Features.update(Lexical)
    Features.update(Host)

    df = pd.DataFrame([Features])

    return df


def process_url(inputFile, outputFile):
    print("running...")
    url_df = pd.read_csv(inputFile)
    url_df = url_df.rename(columns={"Domain": 'url'})

    all_features_df = pd.DataFrame()  # DataFrame to store all features
    print(len(url_df))
    for url in url_df['url'].iloc[500:700]: #.iloc[500:1000]
        features_df = get_features(url)
        all_features_df = pd.concat([all_features_df, features_df], ignore_index=True)
    all_features_df.to_csv(outputFile, index=False)


def test_process_url(inputFile):
    print("running... (return DF)")
    url_df = pd.read_csv(inputFile, header=None, names=['url'])

    all_features_df = pd.DataFrame()  # DataFrame to store all features
    print(len(url_df))
    for url in url_df['url']:
        features_df = get_features(url)
        all_features_df = pd.concat([all_features_df, features_df], ignore_index=True)

    return all_features_df



if __name__ == '__main__':
    process_url(INPUTFILE,OUTPUTFILE)
