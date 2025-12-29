import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import make_classification
from sklearn.metrics import confusion_matrix
import numpy as np
from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler()
df = pd.read_csv('./final_final_df.csv')
normalize = ['country',
             'Country Code TLD'
             ]

df = df.drop(columns=['status'])
df[normalize] = scaler.fit_transform(df[normalize])

plt.figure(figsize=(10, 15))
sns.stripplot(data=df, orient='h', jitter=True, alpha=0.5)
plt.tight_layout()
plt.show()
