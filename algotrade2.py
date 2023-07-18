import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pandas_datareader import data as pdr
from sklearn.cluster import KMeans


def clustring_K_means(path):

        df = pd.read_csv(path)
        df = df.dropna(axis=1)  # Drop columns with NaN values
        df = df.drop("Date", axis=1)
        columns = df.columns
        df = df.T
        
        num_of_clusters = range(1,21)
        #kmeans = KMeans(n_clusters=5).fit(df)
        
        kmeans = [KMeans(n_clusters=i).fit(df) for i in num_of_clusters]
        scores = [kmeans[i].score(df) for i in range(len(kmeans))]
        scores = np.array(scores)
        dif_scores = scores / scores[0]
        dif_scores = np.diff(dif_scores)
        k = np.argwhere(dif_scores < np.quantile(dif_scores ,0.9))[-1][0]
        k=4
        kmeans = KMeans(n_clusters=k).fit(df)
        clusters = {}
        for i, label in enumerate(kmeans.labels_):
            print(f"Data point {i+1} {columns[i]}: Cluster {label}")
            if label not in clusters:
                clusters[label] = []  # Create an empty array for the cluster if it doesn't exist
            clusters[label].append(columns[i])
        print(clusters)
            # Calculate correlations with QQQ for each cluster
        qqq_correlations = {}
        for cluster_label, cluster_symbols in clusters.items():
            cluster_indices = [columns.get_loc(symbol) for symbol in cluster_symbols]  # Retrieve numeric indices
            cluster_df = df.iloc[cluster_indices, :]  # Access rows using numeric indices
            correlation_matrix = cluster_df.corr()
            if 'QQQ' in correlation_matrix.columns:
                qqq_correlations[cluster_label] = correlation_matrix['QQQ'].drop('QQQ')

        # Print the stocks with the highest correlations to QQQ for each cluster
        print("Stocks with highest correlation to QQQ (by cluster):")
        for cluster_label, correlations in qqq_correlations.items():
            correlations = correlations.sort_values(ascending=False)
            print(f"Cluster {cluster_label}:")
            print(correlations.head())
            print()

        return kmeans


path = "c:\\Users\\Win10\\Desktop\\VirtualFiltration_Students_AY2023\\check_out1.csv"
kmeans1 = clustring_K_means(path)
