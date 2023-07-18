import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

def find_best_correlated_stocks(path, target_symbol, path_anuual):
    df = pd.read_csv(path)
    df_annual = pd.read_csv(path_anuual)

    df = df.drop("Date", axis=1)
    columns = df.columns
    #df = df.T
    df_annual = df_annual.iloc[:,1:]
    #df_annual = df_annual.T

    #df = df.dropna(axis=1)  # Drop columns with NaN values
    df = fill_nan_with_array(df, df_annual.values,columns)
    correlations = df.corr()
    pd.DataFrame(correlations).to_csv("Corelations.csv")

    print(correlations)


    sort_correlation = []
    for i in range(2) :
        correlations_TRAGET_SYMBOL = correlations[target_symbol].drop(target_symbol)
        best_correlated_stocks = correlations_TRAGET_SYMBOL.sort_values(ascending=False)
        sort_correlation.append(best_correlated_stocks)
    return sort_correlaion



    

    


    return best_correlated_stocks

def sort_correlaion(correlations,target_symbol):
    
    

    correlations_TRAGET_SYMBOL = correlations[target_symbol]
    best_correlated_stocks = correlations_TRAGET_SYMBOL.sort_values(ascending=False)
    symbols = correlations.iloc[..., 0]
    return best_correlated_stocks





def fill_nan_with_array(df, array1,columns):
    array1 = array1.flatten()
    for i  in range(len(array1)):
        df[columns[i]] = df[columns[i]].fillna(array1[i])
    df = df.dropna(axis=1)
    return df



number_of_positive_stocks_correlation = 5 #can be changed
path = "c:\\Users\\Win10\\Desktop\\VirtualFiltration_Students_AY2023\\check_out1.csv"
target_stocks = ['MSFT','A','AAPL'] #can add whatever stocks you want
path_annual = "c:\\Users\\Win10\\Desktop\\VirtualFiltration_Students_AY2023\\check_return_annual.csv"


correlations = pd.read_csv("c:\\Users\\Win10\\Desktop\\VirtualFiltration_Students_AY2023\\Corelations.csv")
# Create a directed graph
G = nx.DiGraph()
symbols_nodes = []
symbols = correlations.iloc[...,0]
edges = []


# Add nodes to the graph

for target_stock in target_stocks : 
    try:
        sort_correaltion = sort_correlaion(correlations,target_stock)
        sort_correaltion = sort_correaltion.dropna()
        best_correlated_stocks_names= map( lambda x: symbols[x] , sort_correaltion.index)
        best_correlated_stocks_names = list(best_correlated_stocks_names)
        best_correlated_stocks_names = best_correlated_stocks_names[:number_of_positive_stocks_correlation]
        sort_correaltion_positive = sort_correaltion[:number_of_positive_stocks_correlation]
        sort_correaltion_nagative =  sort_correaltion[-5:]


        print(f"Stocks with the best correlation to {target_stock}:")
        print(best_correlated_stocks_names)
        symbols_nodes = symbols_nodes + best_correlated_stocks_names

        # Add weighted edges to the graph
        i=0
        for stock in  best_correlated_stocks_names:
            if stock == target_stock : 
                i+=1
                continue
            edges.append((target_stock,stock,sort_correaltion_positive.values[i]))
            i+=1
        i=0
        #for stock in  best_correlated_stocks_names:
        #    if stock == target_stock : 
        #        i+=1
        #        continue
        #    edges.append((target_stock,stock,sort_correaltion_nagative.values[i]))
        #    i+=1

    except :
        print("error_stock")


G.add_nodes_from(symbols_nodes)
G.add_weighted_edges_from(edges)

# Create a layout for the graph
pos = nx.spring_layout(G)

# Extract edge weights
edge_labels = nx.get_edge_attributes(G, 'weight')

        # Define edge colors based on weights
edge_colors = ['red' if weight < 0 else 'blue' for weight in edge_labels.values()]

        # Draw the graph with labels, edge weights, and colors
default_edge_color = 'black'

# Draw the graph with labels, edge weights, and colors
#best_correlated_stocks = find_best_correlated_stocks(path, target_stock,path_annual)
#print(f"Stocks with the best correlation to {target_stock}:")
#print(best_correlated_stocks)

