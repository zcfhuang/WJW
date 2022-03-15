
import utils
from ItemCF import ItemBasedCF
from dataset import get_dataset
from utils import LogTime
import random
import os
_path = os.path.dirname(os.path.abspath(__file__)) +'\\data\\my_data\\word.csv'
import logging

def run_model(sim,model_name, dataset_name, dataset_path, test_size=0.3, clean=True,search=False):
    print('*' * 70)
    print('\tThis is %s model trained on %s with test_size = %.2f' % (model_name, dataset_name, test_size))
    logger.info('\tThis is %s model trained on %s with test_size = %.2f' % (model_name, dataset_name, test_size))
    print('*' * 70 + '\n')
    model_manager = utils.ModelManager(sim,dataset_name, test_size)
    trainset,testset = get_dataset(dataset_path, 1-test_size)
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
    recommend_test(model, [1,10,50,100])
    model.test(testset,logger)



def recommend_test(model, user_list):
    for user in user_list:
        recommend = model.recommend(str(user))
        print("recommend for userid = %s:" % user)
        print(recommend)
        print()


if __name__ == '__main__':

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
            run_model(sim, model_type, dataset_name,dataset_path, test_size, False, False)
            main_time.finish()
