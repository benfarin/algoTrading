import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import yfinance as yf



#function get correlation table and target symbol and return sort columns of the correlation matrix
def sort_correlaion(correlations,target_symbol):
    correlations_TRAGET_SYMBOL = correlations[target_symbol]
    best_correlated_stocks = correlations_TRAGET_SYMBOL.sort_values(ascending=False)
    return best_correlated_stocks




#function clean nan values 
def fill_nan_with_array(df, array1,columns):
    array1 = array1.flatten()
    for i  in range(len(array1)):
        df[columns[i]] = df[columns[i]].fillna(array1[i])
    df = df.dropna(axis=1)
    return df

#function to replace smaller number in an array
def replace_smaller_numbers( array,number):
    for i in range(len(array)):
        if array[i] < number:
            array[i] = number
            return array
    return array


# Function to replace stock name of smaller numbers in an array
def replace_stock_namke_of_smaller_numbers( array_max_stocks ,array , number,stock_name):
    for i in range(len(array)):
        if array[i] < number:
            array_max_stocks[i] = stock_name
            return array_max_stocks
    return array_max_stocks



# Function to find stocks with the best correlation
def find_stocks_with_best_correaltion(number_of_stocks , stock_names ):
        max_stocks = [0]*number_of_stocks
        max_stock_names = ["first"]*number_of_stocks
        for target_stock in stock_names : 
            try:
                sort_correaltion = sort_correlaion(correlations,target_stock)
                
                sort_correaltion = sort_correaltion.dropna()
                best_correlated_stocks_names= map( lambda x: symbols[x] , sort_correaltion.index)
                best_correlated_stocks_names = list(best_correlated_stocks_names)
                best_correlated_stocks_names = best_correlated_stocks_names[:number_of_positive_stocks_correlation]
                sort_correaltion_positive = sort_correaltion[:number_of_positive_stocks_correlation]
                correlations_sum_of_n_stocks = sum(sort_correaltion_positive.values)
                if correlations_sum_of_n_stocks < 0.93*number_of_stocks :
                    max_stock_names = replace_stock_namke_of_smaller_numbers( max_stock_names ,max_stocks,correlations_sum_of_n_stocks,target_stock)

                    max_stocks = replace_smaller_numbers(max_stocks, correlations_sum_of_n_stocks)
                
                

            except :
                print("error_stock")
        return max_stocks


# Function to draw stock price graphs
def draw_graphs(close):

    plt.style.use("seaborn")
    normclose = close.div(close.iloc[0]).mul(100)
    normclose.plot(figsize=(15,8), fontsize= 12 )
    plt.legend(fontsize =12)
    plt.show()


# Function to create a graph    
def make_graph(symbols_nodes, edges, G):

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
    if len(edge_colors) == len(G.edges):
        nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color=edge_colors, arrows=True)
    else:
        nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color=default_edge_color, arrows=True)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    # Show the graph on the screen
    plt.show()
    plt.pause(100)




# Function to build a graph of correlations based on target stocks, depth, and wide

def correlation_graph_builder(correlations, target_stocks, number_of_positive_stocks_correlation, depth ):

    number_of_positive_stocks_correlation  = number_of_positive_stocks_correlation +1
    G = nx.DiGraph()
    symbols_nodes = []
    symbols = correlations.iloc[...,0]
    edges = []
    # Add nodes to the graph
    for i in range(depth):
        for target_stock in target_stocks :  #each stock of target stocks
            try:
                sort_correaltion = sort_correlaion(correlations,target_stock) #bring the columns sorted
                sort_correaltion = sort_correaltion.dropna() #clean data
                best_correlated_stocks_names= map( lambda x: symbols[x] , sort_correaltion.index)  #bring the names of the correlations values
                best_correlated_stocks_names = list(best_correlated_stocks_names)
                best_correlated_stocks_names = best_correlated_stocks_names[:number_of_positive_stocks_correlation]  #slice the array  of the stocks names just for the number_of_positive_stocks_correlation first values which were given
                sort_correaltion_positive = sort_correaltion[:number_of_positive_stocks_correlation] #slice the array of the values just for the number_of_positive_stocks_correlation first values which were given
                print(f"Stocks with the best correlation to {target_stock}:")
                print(best_correlated_stocks_names)
                stocks_best_correlated = yf.download(best_correlated_stocks_names,start="2018-01-01", end="2023-01-01")
                close = stocks_best_correlated.loc[:,"Close"]

                #Notice : if you want draw the close prices graphs 
                #draw_graphs(close)
                
                symbols_nodes = symbols_nodes + best_correlated_stocks_names
                # Add weighted edges to the graph
                i=0
                for stock in  best_correlated_stocks_names:
                    if stock == target_stock : 
                        i+=1
                        continue
                    edges.append((target_stock,stock,round(sort_correaltion_positive.values[i],3)))
                    i+=1
                i=0
            except :
                print("error_stock")
        
        target_stocks_temp = symbols_nodes

        for element in target_stocks:
            if element in target_stocks_temp:
                target_stocks_temp.remove(element)

        target_stocks = target_stocks_temp
        
        
    make_graph(symbols_nodes, edges, G)




path = "c:\\Users\\Win10\\Desktop\\VirtualFiltration_Students_AY2023\\check_out.csv"
number_of_positive_stocks_correlation = 3  #Number of neighbors for each stock 
depth = 2  # the depth of   each refernce stock
target_stocks =['AAPL','TSLA']# reference stocks to start from 
correlations = pd.read_csv("c:\\Users\\Win10\\Desktop\\VirtualFiltration_Students_AY2023\\Corelations.csv")
correlation_graph_builder(correlations, target_stocks, number_of_positive_stocks_correlation, depth)

