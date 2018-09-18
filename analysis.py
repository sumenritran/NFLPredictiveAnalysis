import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import GridSearchCV, cross_val_score

# Load preprocessed data for 2003-2017 game matchups
df = pd.read_csv('nfl_cleaned.csv')
df.describe()

# Specify non-predictive attributes and target variable
non_pred = ['year', 'week', 'h_team', 'a_team', 'temp']
target = ['h_wins', 'line_w', 'over_w']
h_wins = ['h_wins']

# Baseline (Naive approach): Determine winners by selecting the Vegas spread favorite
pred = df[df.year == 2017]
base = pd.to_numeric(np.array(np.where(pred['line'] < 0, 1, 0)))
base = pd.to_numeric(np.array(np.where(pred['h_wins'] == base, 1, 0)))
base = pd.Series(base)
base = base.value_counts()
base = base[1]/len(pred)



##### MODEL TRAINING #####

# Function to drop non-predictive attributes, scale features, partition data and create cv indexes
def get_idx(season):
    global df, non_pred
    split, train_idx, valid_idx = {}, {}, {}   
    
    training = df[df.year < season]
    testing = df[df.year == season]
    
    for week in range(1, 19):
        split[format(week)] = training.append(testing[testing.week < week]).drop(non_pred, axis=1)
        train_idx[format(week)] = training.append(testing[testing.week < week]).index.values
        valid_idx[format(week)] = testing[testing.week == week].index.values
    
    train_idx.pop('18', None)
    valid_idx.pop('18', None)
    
    # Seperate and scale features for training
    scale = MinMaxScaler()
    x_train, y_train = {}, {}
    
    for key, value in split.items():
        x_train[key] = scale.fit_transform(np.array(value.drop(target, axis=1)))
        y_train[key] = np.array(value[h_wins])
        
    x_train = x_train['18']
    y_train = y_train['18'].ravel()
    
    # Store index values used for cross-validation into an iterable list
    train_idx_val = [value for (key, value) in train_idx.items()]
    valid_idx_val = [value for (key, value) in valid_idx.items()]
    cv = [(train_idx_val[i], valid_idx_val[i]) for i in range(len(train_idx))]
    size = list(len(valid_idx_val[i]) for i in range(len(valid_idx_val)))
    
    return x_train, y_train, cv, size

# 2003-2015 used for training and 2016 for tuning
tuning = list(get_idx(2016))
x_train = tuning[0]
y_train = tuning[1]
cv = tuning[2]

# Set random seed and create a dataframe to store training results
np.random.seed(0)
tune, models, mod_name, param = [], [], [], []

# Specify grid search parameters
lr= {'penalty':['l1','l2'], 'C':[0.05, 0.1, 0.5]}
rf= {'n_estimators':[50,75,100], 'max_depth':[1,2,3], 'criterion':['gini','entropy']}
gb= {'n_estimators':[100,150,200], 'max_depth':[1,2,3]}
nn= {'hidden_layer_sizes': [(50,50), (75,75), (50,75,50)], 'activation': ['tanh', 'relu', 'logistic']}

models.append(('Logistic Regression', LogisticRegression(random_state=0), lr))
models.append(('Random Forests', RandomForestClassifier(random_state=0), rf))
models.append(('Gradient Boosting', GradientBoostingClassifier(random_state=0), gb))
models.append(('Neural Networks', MLPClassifier(random_state=0), nn))

# Model tuning
for name, model, par in models:
    grid = GridSearchCV(model, param_grid=par, scoring='accuracy', cv=cv)
    cv_results = grid.fit(x_train, y_train)
    tune.append(cv_results.best_score_)
    param.append(cv_results.best_params_)
    mod_name.append(name)

tune = np.column_stack((mod_name, tune, param))
tune = pd.DataFrame(tune, columns=['Model', 'Accuracy', 'Parameters'])
tune['Accuracy'] = tune['Accuracy'].astype(float)
tune['Accuracy'] = pd.Series(['{0:.1f}%'.format(val * 100) for val in tune['Accuracy']], index = tune.index)

del pred, tuning, x_train, y_train, lr, rf, gb, nn, param



##### MODEL TESTING #####

# 2003-2016 used for training and 2017 for testing
testing = list(get_idx(2017))
x_test = testing[0]
y_test = testing[1]
cv = testing[2]
size = testing[3]

# Storing results
results = []
results.append((base))

# The Gradient Boosting model will be used on the test set
models, mod_name = [], []
mod_name.append('Baseline')
models.append(('Gradient Boosting', GradientBoostingClassifier(random_state=0)))

for name, model in models:
    cv_results = cross_val_score(model, x_test, y_test, cv=cv, scoring="accuracy")
    results.append(sum((cv_results*size))/sum(size))
    mod_name.append(name)

results = np.column_stack((mod_name, results))
results = pd.DataFrame(results, columns=['Model', 'Accuracy'])
results['Accuracy'] = results['Accuracy'].astype(float)
results['Accuracy'] = pd.Series(['{0:.1f}%'.format(val * 100) for val in results['Accuracy']], index = results.index)
print(results)