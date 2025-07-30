import json

# get number of narratives 
def get_narratives(number):
    # Load heartfelt_selected.json and store it in a variable
    with open("dataset/heartfelt_selected.json", "r", encoding="utf-8") as f:
        narratives = json.load(f)
        
    if (number == -1 ):
        return narratives
    
    return narratives[:number]

def count_narratives():
    with open("dataset/heartfelt_selected.json", "r", encoding="utf-8") as f:
        narratives = json.load(f)
    return len(narratives)

if __name__ == "__main__":
    print("testing functions")
    print(count_narratives())