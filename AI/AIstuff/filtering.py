import pandas as pd

combined_csv_file = "Results/Joined/combined_final.csv"

good_file = "Results/URL_features.csv"

good_file_2 = "Results/Cleaned_URL_1.csv"

bad_file_1 = "Results/phishlinkresult.csv"
bad_file_2 = "Results/phishtankresult.csv"
bad_file_3 = "Results/urlhausresult.csv"



bad_file_4 = "Results/OpenPhish_1Result.csv"
bad_file_5 = "Results/OpenPhish_2Result.csv"
bad_file_6 = "Results/OpenPhish_3Result.csv"
bad_file_7 = "Results/OpenPhish_4Result_2.csv"
bad_file_8 = "Results/OpenPhish_5Result.csv"

##
bad_file_9 = "Results/OpenPhish_6Result.csv"
bad_file_10 = "Results/OpenPhish_7Result.csv"
bad_file_11 = "Results/OpenPhish_8Result.csv"


good_df = pd.read_csv(good_file)
good_df_2 = pd.read_csv(good_file_2)

bad_df_1 = pd.read_csv(bad_file_1)
bad_df_2 = pd.read_csv(bad_file_2)
bad_df_3 = pd.read_csv(bad_file_3)
bad_df_4 = pd.read_csv(bad_file_4)
bad_df_5 = pd.read_csv(bad_file_5)
bad_df_6 = pd.read_csv(bad_file_6)
bad_df_7 = pd.read_csv(bad_file_7)
bad_df_8 = pd.read_csv(bad_file_8)

bad_df_9 = pd.read_csv(bad_file_9)
bad_df_10 = pd.read_csv(bad_file_10)
bad_df_11 = pd.read_csv(bad_file_11)


good_df = good_df[good_df['status'] == 200]
bad_df_1 = bad_df_1[bad_df_1['status'] == 200]
bad_df_2 = bad_df_2[bad_df_2['status'] == 200]
bad_df_3 = bad_df_3[bad_df_3['status'] == 200]

malicious_counts = len(bad_df_3)
print("malicious count: ", malicious_counts)

bad_df_4 = bad_df_4[bad_df_4['status'] == 200]
bad_df_5 = bad_df_5[bad_df_5['status'] == 200]
bad_df_6 = bad_df_6[bad_df_6['status'] == 200]
bad_df_7 = bad_df_7[bad_df_7['status'] == 200]
bad_df_8 = bad_df_8[bad_df_8['status'] == 200]


bad_df_9 = bad_df_9[bad_df_9['status'] == 200]
bad_df_10 = bad_df_10[bad_df_10['status'] == 200]
bad_df_11 = bad_df_11[bad_df_11['status'] == 200]
good_df_2 = good_df_2[good_df_2['status'] == 200]



missing_columns = ["JS_count_link", "JS_count_eval", "JS_count_exec",
                   "JS_count_unescape", "JS_count_search", "JS_count_find",
                   "JS_count_escape", "JS_presence_iframe", "presence_window.open"]

bad_df_9.drop(columns=missing_columns, inplace=True)
bad_df_10.drop(columns=missing_columns, inplace=True)
bad_df_11.drop(columns=missing_columns, inplace=True)

good_df_2.drop(columns=missing_columns, inplace=True)

# testcombined = pd.concat([good_df, bad_df_1], ignore_index=True)
# print(testcombined.info())
good_df['label'] = 0
good_df_2['label'] = 0
bad_df_1['label'] = 1
bad_df_2['label'] = 1
bad_df_3['label'] = 1
bad_df_4['label'] = 1
bad_df_5['label'] = 1
bad_df_6['label'] = 1
bad_df_7['label'] = 1
bad_df_8['label'] = 1
bad_df_9['label'] = 1
bad_df_10['label'] = 1
bad_df_11['label'] = 1



combined_df = pd.concat([good_df, good_df_2,bad_df_1, bad_df_2, bad_df_3,
                         bad_df_4, bad_df_5, bad_df_6,bad_df_7, bad_df_8, bad_df_9,
                        bad_df_10, bad_df_11
                         ], ignore_index=True)


combined_df.to_csv(combined_csv_file, index=False)

# Print the number of total samples in combined_df
print("Total samples in combined_df:", len(combined_df))

# Print the number of label 1 and label 0
label_counts = combined_df['label'].value_counts()
print("Number of label 1 (malicious URLs):", label_counts[1])
print("Number of label 0 (benign URLs):", label_counts[0])