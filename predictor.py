import numpy
import pandas
from sklearn import tree, preprocessing


path_to_file = "./results.csv"
teams = []
match_types = ["normal", "neutral"]
labels = []
features = []
labelDict = {}


def parse_internationals(file_path, feat, lab):
    key = 0
    df = pandas.read_csv(file_path)
    for index, match in df.iterrows():
        home = match['home_team'].casefold() 
        away = match['away_team'].casefold() 
        home_score = match['home_score']
        away_score = match['away_score']
        # match_type = "normal"
        
        if match['neutral']:
            # match_type = "neutral"
            feat.append([away, home])
            lab.append([away_score, home_score])

        feat.append([home, away])
        lab.append([home_score, away_score])

        if not home in teams:
            teams.append(home)
        if not away in teams:
            teams.append(away)
    return feat, lab


features, labels = parse_internationals(path_to_file, features, labels)

le = preprocessing.LabelEncoder()
le.fit(teams+match_types)

for i in range(len(features)):
    features[i] = le.transform(features[i])

clf = tree.DecisionTreeClassifier()
clf = clf.fit(features, labels)

while True:
    h = input("Home Team: ").strip().casefold()
    a = input("Away Team: ").strip().casefold()
    # neutral = input("y for neutral match, any ohter key for normal match: ") \
        # .strip().casefold()
    # if neutral == "y":
    #     match_type = "neutral"
    # else:
    #     match_type = "normal"
    try:
        # t = le.transform([h, a, match_type])
        t = le.transform([h, a])
        print(t)
        res = clf.predict([t])
        print("{} {}-{} {}" \
            .format(h.upper(), int(res[0][0]), int(res[0][1]), a.upper()))
    except:
        print("INVALID TEAM ENTRY. VALID TEAMS ARE: ")
        print(teams)
        
    q = input("q to quit, any other key to continue: ").strip()
    if q == "q":
        break

