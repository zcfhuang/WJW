
from ast import Str
import random
import os
from re import S
_path = os.path.dirname(os.path.abspath(__file__)) +'\\data\\my_data\\word_2022.csv'
_path2 = os.path.dirname(os.path.abspath(__file__)) +'\\data\\my_data\\index.txt'
path2 = os.path.dirname(os.path.abspath(__file__))
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils import LogTime
from ItemCF import ItemBasedCF
from dataset import get_dataset
import logging
import utils
def run_model(sim,model_name, dataset_name, dataset_path, logger,train_set,test_size=0.3,clean=True,search=False,):
    print('*' * 70)
    print('\tThis is %s model trained on %s with test_size = %.2f' % (model_name, dataset_name, test_size))
    logger.info('\tThis is %s model trained on %s with test_size = %.2f' % (model_name, dataset_name, test_size))
    print('*' * 70 + '\n')
    model_manager = utils.ModelManager(sim,dataset_name, test_size)
    trainset,testset = get_dataset(dataset_path, 1-test_size)
    xx={-1:train_set[1]}
    trainset.update(xx)
    model_manager.save_model(trainset, 'trainset')
    model_manager.save_model(testset, 'testset')
    '''Do you want to clean workspace and retrain model again?'''
    '''if you want to change test_size or retrain model, please set clean_workspace True'''
    model_manager.clean_workspace(clean)

    i,j = 10,10
    if model_name == 'ItemCF':
                    model = ItemBasedCF(k_sim_movie = i, n_rec_movie = j )
                    logger.info('ItemBasedCF: k_sim_movie: {}, n_rec_movie:{},'.format(i,j))
    else:
        raise ValueError('No model named ' + model_name)
    
    model.fit(trainset)
    # recommend_test(model, [1,10,50,100])
    model.test(testset,logger)
    return model,testset



def recommend_test(model, user_list):
    for user in user_list:
        recommend = model.recommend(str(user))
        print("recommend for userid = %s:" % user)
        print(recommend)
        print()

def train(train_set):
    logger = logging.getLogger(__name__)
    logger.setLevel(level = logging.INFO)
    handler = logging.FileHandler("log2.txt")
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    for sim in ['cos']:
        for model_type in ['ItemCF-IUF']:
            main_time = LogTime(words="Main Function")
            dataset_name = 'my_data'
            dataset_path = _path
            model_type = 'ItemCF'
            test_size = 0.2
            logger.info('dataset_name: {}, sim:{}, model_type:{}, test_size:{} '.format(
                            dataset_name,sim,model_type,test_size))
            model,testset = run_model(sim, model_type, dataset_name,dataset_path, logger,train_set,test_size, False, False)
            main_time.finish()
    return model,logger,testset
    
def word_api(word):
    word_string = '丑军浑'
    train_set = index_pipei(word_string)
    model,logger,_ = train(train_set)
    # rec_movies = model.test(testset,logger)
    rec_movies = model.recommend(-1)
    rec_movies = index_pipei2(rec_movies)
    return rec_movies

def index_pipei(word_string):
    word_list = []
    pipei_list = []
    word_dit = {}
    with open(_path2,encoding="utf-8") as f:
        for line in f:
            word = line.split()
            pipei_list.append(word)
        print(pipei_list)
    for i in range(len(word_string)):
        word_list.append(word_string[i])
    print(word_list)
    for i in word_list:
        for j in pipei_list:
            if i ==j[1]:
                word_dit[j[0]]=1
    return {1:word_dit}

def index_pipei2(num_string):
    word_list = []
    pipei_list = []
    word_dit = {}
    with open(_path2,encoding="utf-8") as f:
        for line in f:
            word = line.split()
            pipei_list.append(word)
        print(pipei_list)
    print(word_list)
    for i in num_string:
        for j in pipei_list:
            if i ==j[0]:
                word_list.append(j[1])
    return word_list 

            
        



if __name__ == '__main__':
    word_string = '丑军浑'
    train_set = index_pipei(word_string)
    model,logger,_ = train(train_set)
    # rec_movies = model.test(testset,logger)
    rec_movies = model.recommend(-1)
    rec_movies = index_pipei2(rec_movies)
    print(tuple(rec_movies))


