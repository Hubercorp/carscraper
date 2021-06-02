from fuzzywuzzy import fuzz
import pandas as pd

df1 = pd.read_csv('dataframe2.csv')
df2 = pd.read_csv('dataframe2.csv')


# Create a function that takes two lists of strings for matching
def match_name(name, list_names, min_score=0):
    # -1 score incase we don't get any matches
    max_score = -1
    # Returning empty name for no match as well
    max_name = ""
    # Iterating over all names in the second list
    for name2 in list_names:
        #Finding fuzzy match score
        score = fuzz.ratio(name, name2)
        # Checking if we are above our threshold and have a better score
        if (score > min_score) & (score > max_score):
            max_name = name2
            max_score = score
    return (max_name, max_score)


# List for dicts for easy DataFrame creation
dict_list = []
# iterating over df with more strains
for name in df1.quote_model:
    # Use our method to find best match, we can set a threshold here
    match = match_name(name, df2.auction_model, 80)
    
    # New dict for storing data
    dict_ = {}
    dict_.update({"quote" : name})
    dict_.update({"name" : match[0]})
    dict_list.append(dict_)
    
merge_table = pd.DataFrame(dict_list)
print(merge_table)

merge_table.to_csv("fuzzy_matching.csv", encoding='utf-8', index=False)