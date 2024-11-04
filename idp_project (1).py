# -*- coding: utf-8 -*-
"""IDP PROJECT

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1O7aPn_IPZw3gm7EXS41GSY7agaDk2Ros
"""

# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 20GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All"
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session



!pip install catboost

!pip install "dask[dataframe]"

!pip install category_encoders

!pip install optuna

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report, roc_auc_score
import warnings
import category_encoders as ce  # Ensure this is installed with 'pip install category_encoders'
import optuna

# Suppress warnings
warnings.filterwarnings('ignore')

path = '/content/dataset[1].csv'

# Load dataset from Excel file
df = pd.read_csv(path)

# Set option to display all columns
pd.set_option('display.max_columns', None)

#Display the loaded dataset
df

df.select_dtypes('object').columns

df.select_dtypes('object').columns

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report, roc_auc_score
import warnings
import category_encoders as ce  # Ensure this is installed with 'pip install category_encoders'
import optuna

# Suppress warnings
warnings.filterwarnings('ignore')

path = '/content/dataset[1].csv'

# Load dataset from Excel file
df = pd.read_csv(path)

# Set option to display all columns
pd.set_option('display.max_columns', None)

# Display the loaded dataset
#df

# Assuming you want to create a copy of 'df' for encoding
df_cat = df.copy()  # Create a copy of df and assign it to df_cat

# Now you can use df_cat in your code
numerical_cols = df_cat.select_dtypes(include=['int64', 'float64']).columns.tolist()
numerical_cols.remove('Target')

# Perform Weight of Evidence Encoding on numerical columns
cat_encoder = ce.WOEEncoder(cols=numerical_cols)
df_cat[numerical_cols] = cat_encoder.fit_transform(df_cat[numerical_cols], df_cat['Target'])

models = []

xgb_model_def = XGBClassifier()
lgb_model_def = LGBMClassifier()
catboost_model_def = CatBoostClassifier()
catboost_model_custom = CatBoostClassifier(cat_features=['Income_type', 'Education_type', 'Family_status', 'Housing_type',
       'Occupation_type'])

models.extend([
    ('XGBoost', xgb_model_def),
    ('LightGBM', lgb_model_def),
    ('CatBoost', catboost_model_def),
    ('CatBoost_Custom', catboost_model_custom),
])

def train_and_evaluate_model(model_name, model, X_train, y_train, X_test, y_test):
    """
    Train and evaluate the given model on the training and testing data.

    Parameters:
    model_name (str): Name of the model for display purposes.
    model : Machine learning model object.
    X_train : Features of the training data.
    y_train : Target labels of the training data.
    X_test : Features of the testing data.
    y_test : Target labels of the testing data.

    Returns:
    float, float: Gini coefficients calculated from the model's predictions on training and testing data.
    """

    # Fit the model on the training data
    model.fit(X_train, y_train)

    # Predict labels and probabilities on the testing data
    y_test_pred = model.predict(X_test)
    y_test_prob = model.predict_proba(X_test)[:, 1]

    # Predict labels and probabilities on the training data
    y_train_pred = model.predict(X_train)
    y_train_prob = model.predict_proba(X_train)[:, 1]

    # Calculate ROC AUC and Gini coefficient for testing data
    roc_test_prob = roc_auc_score(y_test, y_test_prob)
    gini_test_prob = roc_test_prob * 2 - 1

    # Calculate ROC AUC and Gini coefficient for training data
    roc_train_prob = roc_auc_score(y_train, y_train_prob)
    gini_train_prob = roc_train_prob * 2 - 1

    # Calculate confusion matrix and classification report for testing data
    confusion_matrix_test_result = confusion_matrix(y_test, y_test_pred)
    classification_report_test_result = classification_report(y_test, y_test_pred)

    # Calculate confusion matrix and classification report for training data
    confusion_matrix_train_result = confusion_matrix(y_train, y_train_pred)
    classification_report_train_result = classification_report(y_train, y_train_pred)

    # Print model performance metrics
    print(f'Model Performance for {model_name}')
    print('Gini prob for testing data is', gini_test_prob * 100)
    print('Gini prob for training data is', gini_train_prob * 100)
    print('Classification Report for Testing Data:')
    print(classification_report_test_result)
    print('Confusion Matrix for Testing Data:')
    print(confusion_matrix_test_result)
    print('Classification Report for Training Data:')
    print(classification_report_train_result)
    print('Confusion Matrix for Training Data:')
    print(confusion_matrix_train_result)

    return gini_train_prob, gini_test_prob

"""# Initialize the DataFrame to store Gini coefficients
gini_df = pd.DataFrame(columns=['Model', 'Gini_train_prob', 'Gini_test_prob'])

# Iterate through each model in the list of models
for model_name, model in models:
    # Train and evaluate the model, and calculate the Gini coefficient
    if model_name == 'CatBoost_Custom':
        gini_train_prob, gini_test_prob = train_and_evaluate_model(model_name, model, X_train_cat, y_train_cat, X_test_cat, y_test_cat)
    else:
        gini_train_prob, gini_test_prob = train_and_evaluate_model(model_name, model, X_train_boost, y_train_boost, X_test_boost, y_test_boost)

    # Add model name and Gini coefficients to the DataFrame
    gini_df = pd.concat([gini_df, pd.DataFrame({'Model': [model_name], 'Gini_train_prob': [gini_train_prob], 'Gini_test_prob': [gini_test_prob]})], ignore_index=True)

# Sort the DataFrame by Gini coefficient for testing data in descending order
gini_df_sorted = gini_df.sort_values(by='Gini_test_prob', ascending=False)
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report, roc_auc_score
import warnings
import category_encoders as ce
import optuna

# Suppress warnings
warnings.filterwarnings('ignore')

path = '/content/dataset[1].csv'

# Load dataset
df = pd.read_csv(path)

# Set option to display all columns
pd.set_option('display.max_columns', None)

# Create a copy of df for encoding
df_cat = df.copy()

# Select numerical columns (excluding 'Target')
numerical_cols = df_cat.select_dtypes(include=['int64', 'float64']).columns.tolist()
numerical_cols.remove('Target')

# Perform Weight of Evidence Encoding on numerical columns
cat_encoder = ce.WOEEncoder(cols=numerical_cols)
df_cat[numerical_cols] = cat_encoder.fit_transform(df_cat[numerical_cols], df_cat['Target'])

# Define models
models = []

xgb_model_def = XGBClassifier()
lgb_model_def = LGBMClassifier()
catboost_model_def = CatBoostClassifier()
catboost_model_custom = CatBoostClassifier(cat_features=['Income_type', 'Education_type', 'Family_status', 'Housing_type', 'Occupation_type'])

models.extend([
    ('XGBoost', xgb_model_def),
    ('LightGBM', lgb_model_def),
    ('CatBoost', catboost_model_def),
    ('CatBoost_Custom', catboost_model_custom),
])

# Define the train_and_evaluate_model function
def train_and_evaluate_model(model_name, model, X_train, y_train, X_test, y_test):
    """
    Train and evaluate the given model on the training and testing data.

    Parameters:
    model_name (str): Name of the model for display purposes.
    model : Machine learning model object.
    X_train : Features of the training data.
    y_train : Target labels of the training data.
    X_test : Features of the testing data.
    y_test : Target labels of the testing data.

    Returns:
    float, float: Gini coefficients calculated from the model's predictions on training and testing data.
    """
    # Train the model
    model.fit(X_train, y_train)

    # Predict probabilities
    train_probs = model.predict_proba(X_train)[:, 1]
    test_probs = model.predict_proba(X_test)[:, 1]

    # Calculate AUC for Gini coefficient
    gini_train_prob = 2 * roc_auc_score(y_train, train_probs) - 1
    gini_test_prob = 2 * roc_auc_score(y_test, test_probs) - 1

    return gini_train_prob, gini_test_prob

# Prepare data for modeling
X = df_cat.drop('Target', axis=1)
y = df_cat['Target']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train and evaluate models, store Gini coefficients
gini_results = []
for model_name, model in models:
    gini_train, gini_test = train_and_evaluate_model(model_name, model, X_train, y_train, X_test, y_test)
    gini_results.append((model_name, gini_train, gini_test))

# Display results
for result in gini_results:
    print(f"Model: {result[0]}, Gini Train: {result[1]:.4f}, Gini Test: {result[2]:.4f}")

from sklearn.metrics import roc_auc_score, accuracy_score
import pandas as pd

# Initialize the DataFrame to store Gini coefficients and accuracies
gini_df = pd.DataFrame(columns=['Model', 'Gini_train_prob', 'Gini_test_prob', 'Train_Accuracy', 'Test_Accuracy'])

# Function to train and evaluate the model, returning Gini and accuracy
def train_and_evaluate_model(model_name, model, X_train, y_train, X_test, y_test):
    # Train the model
    model.fit(X_train, y_train)

    # Predict probabilities for Gini calculation
    train_prob = model.predict_proba(X_train)[:, 1]
    test_prob = model.predict_proba(X_test)[:, 1]

    # Calculate Gini coefficients
    gini_train_prob = 2 * roc_auc_score(y_train, train_prob) - 1
    gini_test_prob = 2 * roc_auc_score(y_test, test_prob) - 1

    # Calculate accuracy
    train_acc = accuracy_score(y_train, model.predict(X_train))
    test_acc = accuracy_score(y_test, model.predict(X_test))

    return gini_train_prob, gini_test_prob, train_acc, test_acc

# Iterate through each model in the list of models
for model_name, model in models:
    # Train and evaluate the model
    if model_name == 'CatBoost_Custom':
        gini_train_prob, gini_test_prob, train_acc, test_acc = train_and_evaluate_model(model_name, model, X_train_cat, y_train_cat, X_test_cat, y_test_cat)
    else:
        gini_train_prob, gini_test_prob, train_acc, test_acc = train_and_evaluate_model(model_name, model, X_train_boost, y_train_boost, X_test_boost, y_test_boost)

    # Add model name, Gini coefficients, and accuracies to the DataFrame
    gini_df = pd.concat([gini_df, pd.DataFrame({
        'Model': [model_name],
        'Gini_train_prob': [gini_train_prob],
        'Gini_test_prob': [gini_test_prob],
        'Train_Accuracy': [train_acc],
        'Test_Accuracy': [test_acc]
    })], ignore_index=True)

# Sort the DataFrame by Gini coefficient for testing data in descending order
gini_df_sorted = gini_df.sort_values(by='Gini_test_prob', ascending=False)

# Display the sorted Gini DataFrame with accuracy values
print(gini_df_sorted)

import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Convert the necessary columns to 'category' dtype
df_categorical = df.copy()

categorical_columns = ['Income_type', 'Education_type', 'Family_status', 'Housing_type', 'Occupation_type']

# Convert these columns to category type
for col in categorical_columns:
    df_categorical[col] = df_categorical[col].astype('category')

# Splitting the data
X = df_categorical.drop('Target', axis=1)  # Independent features
y = df_categorical['Target']  # Dependent feature

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Defining the XGBoost model and enabling categorical support
xgboost_model = xgb.XGBClassifier(use_label_encoder=False, eval_metric='logloss', enable_categorical=True)

# Training the model
xgboost_model.fit(X_train, y_train)

# Predictions
y_train_pred = xgboost_model.predict(X_train)
y_test_pred = xgboost_model.predict(X_test)

# Accuracy
train_accuracy = accuracy_score(y_train, y_train_pred)
test_accuracy = accuracy_score(y_test, y_test_pred)

print(f"XGBoost Train Accuracy: {train_accuracy:.2f}")
print(f"XGBoost Test Accuracy: {test_accuracy:.2f}")

import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Copy the dataset to avoid modifying the original
df_categorical = df.copy()

# Identify the categorical columns
categorical_columns = ['Income_type', 'Education_type', 'Family_status', 'Housing_type', 'Occupation_type']

# Convert categorical columns to 'category' data type
for col in categorical_columns:
    df_categorical[col] = df_categorical[col].astype('category')

# Splitting the data
X = df_categorical.drop('Target', axis=1)  # Independent features
y = df_categorical['Target']  # Dependent feature

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Define the LightGBM model
lgbm_model = lgb.LGBMClassifier()

# Training the model
lgbm_model.fit(X_train, y_train, categorical_feature=categorical_columns)

# Predictions
y_train_pred = lgbm_model.predict(X_train)
y_test_pred = lgbm_model.predict(X_test)

# Accuracy
train_accuracy = accuracy_score(y_train, y_train_pred)
test_accuracy = accuracy_score(y_test, y_test_pred)

print(f"LightGBM Train Accuracy: {train_accuracy:.2f}")
print(f"LightGBM Test Accuracy: {test_accuracy:.2f}")

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
import catboost as cb

# Assuming 'df' is your original DataFrame

# Copy the dataset to avoid modifying the original
df_catboost = df.copy()

# List of categorical columns to encode
categorical_cols = ['Income_type', 'Education_type',
                    'Family_status', 'Housing_type',
                    'Occupation_type']

# Label encoding for categorical columns
label_encoders = {}
for col in categorical_cols:
    le = LabelEncoder()
    df_catboost[col] = le.fit_transform(df_catboost[col])
    label_encoders[col] = le  # Store the encoder for future reference

# Splitting the data
X = df_catboost.drop('Target', axis=1)  # Independent features
y = df_catboost['Target']  # Dependent feature

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Define the CatBoost model
catboost_model = cb.CatBoostClassifier(verbose=False)

# Training the model
catboost_model.fit(X_train, y_train)

# Predictions
y_train_pred = catboost_model.predict(X_train)
y_test_pred = catboost_model.predict(X_test)

# Accuracy
train_accuracy = accuracy_score(y_train, y_train_pred)
test_accuracy = accuracy_score(y_test, y_test_pred)

print(f"CatBoost Train Accuracy: {train_accuracy:.2f}")
print(f"CatBoost Test Accuracy: {test_accuracy:.2f}")

# Identifying categorical features
cat_features = ['Gender', 'Income_type', 'Education_type', 'Family_status', 'Housing_type', 'Occupation_type']

# Defining the model with custom settings
catboost_model = CatBoostClassifier(silent=True)

# Training the model with cat_features
catboost_model.fit(X_train, y_train, cat_features=cat_features)

# Predictions
y_train_pred = catboost_model.predict(X_train)
y_test_pred = catboost_model.predict(X_test)

# Accuracy
train_accuracy = accuracy_score(y_train, y_train_pred)
test_accuracy = accuracy_score(y_test, y_test_pred)

print(f"CatBoost (Custom) Train Accuracy: {train_accuracy:.2f}")
print(f"CatBoost (Custom) Test Accuracy: {test_accuracy:.2f}")

!pip install catboost

from catboost import CatBoostClassifier

!pip install optuna

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, roc_auc_score
from catboost import CatBoostClassifier
from lightgbm import LGBMClassifier
from sklearn.ensemble import VotingClassifier
from sklearn.preprocessing import LabelEncoder
import warnings

# Suppress warnings
warnings.filterwarnings('ignore')

# Load your dataset
path = '/content/dataset[1].csv'
df = pd.read_csv(path)

# Set option to display all columns
pd.set_option('display.max_columns', None)

# Display the loaded dataset
print(df.head())

# Define features and target
X = df.drop('Target', axis=1)
y = df['Target']

# Identify categorical columns
categorical_cols = X.select_dtypes(include=['object']).columns

# Apply Label Encoding to the categorical columns
label_encoders = {}
for col in categorical_cols:
    le = LabelEncoder()
    X[col] = le.fit_transform(X[col])
    label_encoders[col] = le  # Store the label encoder for future use (if needed)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Get the indices of the categorical columns (after label encoding)
categorical_indices = [X.columns.get_loc(col) for col in categorical_cols]

# Initialize the base models
catboost_model = CatBoostClassifier(cat_features=categorical_indices, silent=True)
lgb_model = LGBMClassifier()

# Define the ensemble model using VotingClassifier with soft voting
ensemble_model = VotingClassifier(
    estimators=[('catboost', catboost_model), ('lightgbm', lgb_model)],
    voting='soft'
)

# Function to train and evaluate models
def train_and_evaluate_model(model_name, model, X_train, y_train, X_test, y_test):
    model.fit(X_train, y_train)

    # Predict labels and probabilities on the testing data
    y_test_pred = model.predict(X_test)
    y_test_prob = model.predict_proba(X_test)[:, 1]

    # Predict labels and probabilities on the training data
    y_train_pred = model.predict(X_train)
    y_train_prob = model.predict_proba(X_train)[:, 1]

    # Calculate accuracy
    accuracy_train = accuracy_score(y_train, y_train_pred)
    accuracy_test = accuracy_score(y_test, y_test_pred)

    # Calculate ROC AUC and Gini coefficient for testing data
    roc_test_prob = roc_auc_score(y_test, y_test_prob)
    gini_test_prob = roc_test_prob * 2 - 1

    # Calculate ROC AUC and Gini coefficient for training data
    roc_train_prob = roc_auc_score(y_train, y_train_prob)
    gini_train_prob = roc_train_prob * 2 - 1

    # Print model performance metrics
    print(f'\nModel Performance for {model_name}')
    print(f'Accuracy for testing data: {accuracy_test * 100:.2f}%')
    print(f'Accuracy for training data: {accuracy_train * 100:.2f}%')
    print(f'Gini prob for testing data: {gini_test_prob * 100:.2f}')
    print(f'Gini prob for training data: {gini_train_prob * 100:.2f}')
    print('Classification Report for Testing Data:')
    print(classification_report(y_test, y_test_pred))
    print('Confusion Matrix for Testing Data:')
    print(confusion_matrix(y_test, y_test_pred))

    return gini_train_prob, gini_test_prob, accuracy_train, accuracy_test

# Train and evaluate the ensemble model
gini_train_prob, gini_test_prob, accuracy_train, accuracy_test = train_and_evaluate_model(
    'Ensemble (CatBoost + LightGBM)', ensemble_model, X_train, y_train, X_test, y_test
)

"""ADA BOOST"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import AdaBoostClassifier
from sklearn.metrics import accuracy_score, classification_report


# Load your dataset  (Add this line to define df)
path = '/content/dataset[1].csv'  # Replace with the correct path
df = pd.read_csv(path)

# Assuming 'df' is the DataFrame loaded in the previous cell
data = df.copy()  # Create a copy of df and assign it to data

# Encoding categorical variables
label_encoder = LabelEncoder()
data['Gender'] = label_encoder.fit_transform(data['Gender'])
data['Own_car'] = label_encoder.fit_transform(data['Own_car'])
data['Own_property'] = label_encoder.fit_transform(data['Own_property'])
data['Work_phone'] = label_encoder.fit_transform(data['Work_phone'])
data['Phone'] = label_encoder.fit_transform(data['Phone'])
data['Email'] = label_encoder.fit_transform(data['Email'])
data['Unemployed'] = label_encoder.fit_transform(data['Unemployed'])
data['Income_type'] = label_encoder.fit_transform(data['Income_type'])
data['Education_type'] = label_encoder.fit_transform(data['Education_type'])
data['Family_status'] = label_encoder.fit_transform(data['Family_status'])
data['Housing_type'] = label_encoder.fit_transform(data['Housing_type'])
data['Occupation_type'] = label_encoder.fit_transform(data['Occupation_type'])

# Splitting the data into features and target
X = data.drop(columns=['ID', 'Target'])  # Dropping ID and Target
y = data['Target']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize AdaBoost classifier
ada_clf = AdaBoostClassifier(n_estimators=100, random_state=42)

# Train the model
ada_clf.fit(X_train, y_train)

# Make predictions
y_pred = ada_clf.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)

print(f"Accuracy: {accuracy}")
print("Classification Report:")
print(report)

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
import xgboost as xgb
import lightgbm as lgb
import catboost as cb
from sklearn.ensemble import AdaBoostClassifier

# Load your dataset (Replace with the correct path)
path = '/content/dataset[1].csv'  # Adjust this path
df = pd.read_csv(path)

# Copy the dataset to avoid modifying the original
data = df.copy()

# Encoding categorical variables
categorical_columns = ['Income_type', 'Education_type', 'Family_status',
                       'Housing_type', 'Occupation_type']

# Label encoding for categorical columns
label_encoder = LabelEncoder()
for col in categorical_columns:
    data[col] = label_encoder.fit_transform(data[col])

# Splitting the data into features and target
X = data.drop(columns=['ID', 'Target'])  # Dropping ID and Target
y = data['Target']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Initialize a dictionary to store accuracies
accuracies = {}

# XGBoost
xgboost_model = xgb.XGBClassifier(use_label_encoder=False, eval_metric='logloss', enable_categorical=True)
xgboost_model.fit(X_train, y_train)
y_train_pred = xgboost_model.predict(X_train)
y_test_pred = xgboost_model.predict(X_test)
accuracies['XGBoost'] = {
    'Train Accuracy': accuracy_score(y_train, y_train_pred),
    'Test Accuracy': accuracy_score(y_test, y_test_pred)
}

# LightGBM
lgbm_model = lgb.LGBMClassifier()
lgbm_model.fit(X_train, y_train)
y_train_pred = lgbm_model.predict(X_train)
y_test_pred = lgbm_model.predict(X_test)
accuracies['LightGBM'] = {
    'Train Accuracy': accuracy_score(y_train, y_train_pred),
    'Test Accuracy': accuracy_score(y_test, y_test_pred)
}

# CatBoost
catboost_model = cb.CatBoostClassifier(verbose=False)
catboost_model.fit(X_train, y_train)
y_train_pred = catboost_model.predict(X_train)
y_test_pred = catboost_model.predict(X_test)
accuracies['CatBoost'] = {
    'Train Accuracy': accuracy_score(y_train, y_train_pred),
    'Test Accuracy': accuracy_score(y_test, y_test_pred)
}

# AdaBoost
ada_clf = AdaBoostClassifier(n_estimators=100, random_state=42)
ada_clf.fit(X_train, y_train)
y_train_pred = ada_clf.predict(X_train)
y_test_pred = ada_clf.predict(X_test)
accuracies['AdaBoost'] = {
    'Train Accuracy': accuracy_score(y_train, y_train_pred),
    'Test Accuracy': accuracy_score(y_test, y_test_pred)
}

# Convert the accuracies dictionary to a DataFrame for better visualization
accuracies_df = pd.DataFrame(accuracies).T
print(accuracies_df)

# Optionally print classification reports for each model
for model_name, acc in accuracies.items():
    print(f"\n{model_name} Classification Report (Test Set):")
    if model_name == 'AdaBoost':
        print(classification_report(y_test, y_test_pred))

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import xgboost as xgb
import lightgbm as lgb
import catboost as cb
from sklearn.ensemble import AdaBoostClassifier
import matplotlib.pyplot as plt
import seaborn as sns

# Load your dataset (Replace with the correct path)
path = '/content/dataset[1].csv'  # Adjust this path
df = pd.read_csv(path)

# Copy the dataset to avoid modifying the original
data = df.copy()

# Encoding categorical variables
categorical_columns = ['Income_type', 'Education_type', 'Family_status',
                       'Housing_type', 'Occupation_type']

# Label encoding for categorical columns
label_encoder = LabelEncoder()
for col in categorical_columns:
    data[col] = label_encoder.fit_transform(data[col])

# Splitting the data into features and target
X = data.drop(columns=['ID', 'Target'])  # Dropping ID and Target
y = data['Target']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Initialize a dictionary to store accuracies and predictions
accuracies = {}
predictions = {}

# XGBoost
xgboost_model = xgb.XGBClassifier(use_label_encoder=False, eval_metric='logloss', enable_categorical=True)
xgboost_model.fit(X_train, y_train)
y_train_pred = xgboost_model.predict(X_train)
y_test_pred = xgboost_model.predict(X_test)
accuracies['XGBoost'] = {
    'Train Accuracy': accuracy_score(y_train, y_train_pred),
    'Test Accuracy': accuracy_score(y_test, y_test_pred)
}
predictions['XGBoost'] = y_test_pred

# LightGBM
lgbm_model = lgb.LGBMClassifier()
lgbm_model.fit(X_train, y_train)
y_train_pred = lgbm_model.predict(X_train)
y_test_pred = lgbm_model.predict(X_test)
accuracies['LightGBM'] = {
    'Train Accuracy': accuracy_score(y_train, y_train_pred),
    'Test Accuracy': accuracy_score(y_test, y_test_pred)
}
predictions['LightGBM'] = y_test_pred

# CatBoost
catboost_model = cb.CatBoostClassifier(verbose=False)
catboost_model.fit(X_train, y_train)
y_train_pred = catboost_model.predict(X_train)
y_test_pred = catboost_model.predict(X_test)
accuracies['CatBoost'] = {
    'Train Accuracy': accuracy_score(y_train, y_train_pred),
    'Test Accuracy': accuracy_score(y_test, y_test_pred)
}
predictions['CatBoost'] = y_test_pred

# AdaBoost
ada_clf = AdaBoostClassifier(n_estimators=100, random_state=42)
ada_clf.fit(X_train, y_train)
y_train_pred = ada_clf.predict(X_train)
y_test_pred = ada_clf.predict(X_test)
accuracies['AdaBoost'] = {
    'Train Accuracy': accuracy_score(y_train, y_train_pred),
    'Test Accuracy': accuracy_score(y_test, y_test_pred)
}
predictions['AdaBoost'] = y_test_pred

# Convert the accuracies dictionary to a DataFrame for better visualization
accuracies_df = pd.DataFrame(accuracies).T
print(accuracies_df)

# Function to plot confusion matrix
def plot_confusion_matrix(y_true, y_pred, model_name):
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False,
                xticklabels=['Not Default', 'Default'],
                yticklabels=['Not Default', 'Default'])
    plt.title(f'Confusion Matrix for {model_name}')
    plt.xlabel('Predicted Label')
    plt.ylabel('True Label')
    plt.show()

# Plot confusion matrices for each model
for model_name, preds in predictions.items():
    plot_confusion_matrix(y_test, preds, model_name)

# Optionally print classification reports for each model
for model_name, acc in accuracies.items():
    print(f"\n{model_name} Classification Report (Test Set):")
    if model_name == 'AdaBoost':
        print(classification_report(y_test, predictions[model_name]))