from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.feature_extraction import DictVectorizer
from operator import itemgetter
from nltk.tokenize import word_tokenize
import pandas as pd
import numpy as np
import os, re


def extract_feat_vocab(csv_file):
    data_frame = pd.read_csv(csv_file, encoding='latin1', error_bad_lines=False)
    feat_vocab = dict()
    for index,row in data_frame[data_frame['type'] == 'silver'].iterrows():
        for token in word_tokenize(row['event_timex']):
            feat_vocab[token] = feat_vocab.get(token,0) + 1
    return feat_vocab


def select_features(feat_vocab, most_freq=100, least_freq=5000):
    sorted_feat_vocab = sorted(feat_vocab.items(), key=itemgetter(1), reverse=True)
    feat_dict = dict(sorted_feat_vocab[most_freq:len(sorted_feat_vocab)-least_freq])
    return set(feat_dict.keys())


def featurize(csv_file, feat_vocab):
    cols = ['_type_', '_label_']
    cols.extend(list(feat_vocab))
    data_frame = pd.read_csv(csv_file, encoding='latin1', error_bad_lines=False)
    row_count = data_frame.shape[0]
    print(row_count)
    feat_data_frame = pd.DataFrame(index=np.arange(row_count), columns=cols)
    feat_data_frame.fillna(0, inplace=True)  # inplace: mutable
    for index, row in data_frame.iterrows():
        feat_data_frame.loc[index, '_type_'] = row['type']
        feat_data_frame.loc[index, '_label_'] = row['tlink_label']
        for token in word_tokenize(row['event_timex']):
            if token in feat_vocab:
                feat_data_frame.loc[index, token] += 1
    return feat_data_frame


def vectorize(feature_csv, split="silver"):
    df = pd.read_csv(feature_csv, encoding='latin1', error_bad_lines=False)
    df = df[df['_type_'] == split]
    df.fillna(0, inplace=True)
    data = list()
    for index, row in df.iterrows():
        datum = dict()
        datum['bias'] = 1
        for col in df.columns:
            if not (col == "_type_" or col == "_label_" or col == 'index'):
                datum[col] = row[col]
        data.append(datum)
    vec = DictVectorizer()
    data = vec.fit_transform(data).toarray()
    print(data.shape)
    labels = df._label_.as_matrix()
    print(labels.shape)
    return data, labels


def train_model(X_train,y_train, model):
    model.fit(X_train,y_train)
    print ("Shape of model coefficients and intercepts: {} {}".format(model.coef_.shape, model.intercept_.shape))
    return model


def test_model(X_test, y_test, model):
    predictions = model.predict(X_test)
    report = classification_report(predictions, y_test)
    accuracy = accuracy_score(predictions, y_test)
    return accuracy, report


def classify(feat_csv):
    X_train, y_train = vectorize(feat_csv)
    X_test, y_test = vectorize(feat_csv, split='gold')
    model = LogisticRegression(multi_class='multinomial',penalty='l2', solver='lbfgs', max_iter=100, verbose=1)
    model = train_model(X_train, y_train, model)
    accuracy, report = test_model(X_test, y_test, model)
    print(report)


if __name__ == '__main__':
    f_all_path = "features_all.csv"
    # select_rows(csv_path,hw1_path)
    feat_vocab = extract_feat_vocab(f_all_path)
    print(len(feat_vocab))
    # print(feat_vocab)
    selected_feat_vocab = select_features(feat_vocab, 100, 1000)
    print(len(selected_feat_vocab))
    feat_data_frame = featurize(f_all_path, selected_feat_vocab)
    featfile = os.path.join(os.path.curdir, "features.csv")
    feat_data_frame.to_csv(featfile, encoding='latin1', index=False)
    classify('features.csv')