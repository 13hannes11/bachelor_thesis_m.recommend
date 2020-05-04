import sys
import os
import datetime
import pandas as pd
import multiprocessing
import itertools

sys.path.append("./src")
sys.path.append("./evaluation")
from model.product_structure_model import ProductStructureModel
from model.preferences_model import Preferences
from model.configuration_model import ConfigurationModel
from managers.recommendation_manager import SimpleConfigurationMaxSelector
from scoring.scoring_functions import ReduceScoringFunctionFactory
from user_type_mappings import TYPE_ATHLETE, TYPE_CONSUMER, TYPE_ENVIRONMENTALIST, TYPE_OWNER, TYPE_RANDOM
import operator
import time
import numpy as np
import matplotlib.pyplot as pp
import random
import math
import json
with open('./evaluation/product_structure.json') as json_file:
    data = json.load(json_file)
    product_structure = ProductStructureModel(data)

from tinydb import TinyDB


def DB():
    return TinyDB('eval.json')

def DB_CONFIG():
    return DB().table('CONFIG')

def DB_PRODUCT_STRUCTURE():
    return DB().table('PRODUCT_STRUCTURE') 

CONFIGURATIONS_UNFINISHED = []
PREFERENCES_RANDOM_MEMBER = []
PREFERENCES_ALL = []

def generate_group_preferences(user_type_mappings, amount = 1000):
    global PREFERENCES_RANDOM_MEMBER
    global PREFERENCES_ALL

    characteristics = product_structure.get_list_of_characteristics()

    PREFERENCES_ALL = []
    PREFERENCES_RANDOM_MEMBER = []
    for i in range(amount):
        users = []
        single_user = []
        counter = random.randint(0, len(user_type_mappings) - 1)
        for mapping in user_type_mappings:
            ratings = []
            for char in characteristics:
                value = mapping[char.elementId].generateNumber()
                ratings.append({
                    "code": char.elementId,
                    "value": value,
                })
            user = {
                "user": mapping['name'],
                "ratings": ratings,
            }
            users.append(user)
            if counter == 0:
                single_user.append(user)
            counter -= 1
        
        PREFERENCES_ALL.append( Preferences({'preferences' : users}) )
        PREFERENCES_RANDOM_MEMBER.append( Preferences({'preferences' : single_user}) )
    return PREFERENCES_ALL

def generate_unfinished_configurations(fullness=0.3, amount=1000):
    configurations = TinyDB('./evaluation/eval.json').table('CONFIG').all()
    global CONFIGURATIONS_UNFINISHED
    
    characteristics = list(map(lambda x: x.elementId,ProductStructureModel(data).get_list_of_characteristics()))

    CONFIGURATIONS_UNFINISHED = []
    for i in range(amount):
        final_config = configurations[random.randint(0, len(configurations) - 1)]
        codes = list(filter(lambda x: x in characteristics, final_config['configuration']))
        conf_size = math.ceil(len(codes) * fullness)

        unfishied_config = random.sample(codes, conf_size)

        CONFIGURATIONS_UNFINISHED.append(ConfigurationModel({
            "configuration": unfishied_config,
            "variables": []
        }))
    return CONFIGURATIONS_UNFINISHED

def get_ratings(requests, finished_configurations, product_structure, scoring_function=None):
    if scoring_function == None :
        scoring_function = ReduceScoringFunctionFactory.build_scoring_function(
            ["penalty_ratio", "pref_product_simpleSelectedCharacterstics_average"],
            #["pref_average_flat"],
            product_structure,
            oper = operator.mul
        )

    list_ofScoreLists = []
    for (preference, config) in requests:
        list_ofScoreLists.append(list(map(lambda to_rate: scoring_function.calc_score(config, preference, to_rate), finished_configurations)))
    return list_ofScoreLists

def plot_at_y(arr, val):
    pp.plot(arr, np.zeros_like(arr) + val, 'x')

def get_scores_for_one(configurationState, preference, finished_configurations, product_structure, scoring_function=None):
    if scoring_function == None:
        scoring_function = ReduceScoringFunctionFactory.build_scoring_function(
            ["penalty_ratio", "pref_product_simpleSelectedCharacterstics_average"],
            product_structure,
            oper = operator.mul
        )
    return list(map(lambda to_rate: scoring_function.calc_score(configurationState, preference, to_rate), finished_configurations))

def get_scoring_functions():
        product = ReduceScoringFunctionFactory.build_scoring_function(
            ["penalty_ratio", "pref_product_simpleSelectedCharacterstics_average"],
            product_structure,
            oper = operator.mul)
        
        misery = ReduceScoringFunctionFactory.build_scoring_function(
            ["penalty_ratio", "pref_min_simpleSelectedCharacterstics_average"],
            product_structure,
            oper = operator.mul)

        average = ReduceScoringFunctionFactory.build_scoring_function(
            ["penalty_ratio", "pref_average_simpleSelectedCharacterstics_average"],
            product_structure,
            oper = operator.mul)

        return [("multiplication",product), ("least misery", misery), ("best average", average)]

def main(amount=1000, fullness=0.1, center=50, threshold_distance_from_centre = 0, group_type='heterogeneous', outdir="./out"):
    global CONFIGURATIONS_UNFINISHED
    global PREFERENCES_RANDOM_MEMBER
    global PREFERENCES_ALL
    print("Started Evaluation")

    if group_type == 'homogenous':
        group_type_mappings = [TYPE_OWNER, TYPE_OWNER, TYPE_OWNER, TYPE_OWNER]
    elif group_type == 'random':
        group_type_mappings = [TYPE_RANDOM, TYPE_RANDOM, TYPE_RANDOM, TYPE_RANDOM]
    else:
        group_type='heterogeneous'
        group_type_mappings = [TYPE_ATHLETE, TYPE_CONSUMER, TYPE_ENVIRONMENTALIST, TYPE_OWNER]

    settings = "amount-{}__center-{}__tdistance-{}__fullness-{}__group-{}".format(amount, center, threshold_distance_from_centre, fullness, group_type)
    outdir += "/{}__{}".format(datetime.datetime.utcnow().strftime("%Y_%m_%d_T%H-%M-%S%z"), settings)

    # check the directory does not exist
    if not(os.path.exists(outdir)):
        # create the directory you want to save to
        os.mkdir(outdir)
    if not(os.path.exists("{}/data".format(outdir))):
        os.mkdir("{}/data".format(outdir))
    if not(os.path.exists("{}/fig".format(outdir))):
        os.mkdir("{}/fig".format(outdir))

    random.seed(10924892319)
    np.random.seed(seed=956109142)
    
    start_total = start = time.time()
    
    # Generating preferences and unfinished configurations
    generate_group_preferences(group_type_mappings, amount=amount)
    generate_unfinished_configurations(fullness=0.1, amount = amount)
    
    requests_random_member = list(zip(PREFERENCES_RANDOM_MEMBER, CONFIGURATIONS_UNFINISHED))
    requests_all = list(zip(PREFERENCES_ALL, CONFIGURATIONS_UNFINISHED))
    end = time.time()
    print("Done generating data! It took: {} seconds".format(end - start))

    start = time.time()
    finished_configurations = list(map(lambda x: ConfigurationModel(x), TinyDB('./evaluation/eval.json').table('CONFIG').all()))
    random.shuffle(finished_configurations)

    end = time.time()
    print("Done loading finished configurations! It took: {} seconds".format(end - start))

    scoring_function_list = get_scoring_functions()

    results_happiness_db_size_avg_diff = []
    results_unhappiness_db_size_avg_diff = []

    results_happiness_db_size_avg_total_all = []
    results_unhappiness_db_size_avg_total_all = []

    piece_counts = [16, 8, 4, 2, 1]
    scoring_function_labels = list(map(lambda x: x[0], scoring_function_list))
    db_sizes_label = list(map(lambda x: len(finished_configurations) // x, piece_counts))
    
    for label, scoring_function in scoring_function_list:
        print("!!! Starting evaluation of: {} !!!".format(label))

        # Rate configurations
        start = time.time()
        np_scores_random = np.array(get_ratings(requests_random_member,finished_configurations,product_structure, scoring_function=scoring_function))
        np_scores_all = np.array(get_ratings(requests_all,finished_configurations,product_structure, scoring_function=scoring_function))
        end = time.time()
        print("Done rating stored configurations! It took: {} seconds".format(end - start))

        happiness_db_size_avg_diff = []
        unhappiness_db_size_avg_diff = []
        happiness_db_size_avg_total_all = []
        unhappiness_db_size_avg_total_all = []

        happiness_db_size_stdd = []
        unhappiness_db_size_stdd = []

        for piece_count in piece_counts:

            happiness_diff_list = []
            unhappiness_diff_list = []
            happiness_all_list = []
            unhappiness_all_list = []

            step_size = len(finished_configurations) // piece_count
            residual = len(finished_configurations) % piece_count

            for run_count in range(piece_count):
                print("Starting run {} of {} with {} as store size.".format(run_count, (piece_count - 1) ,step_size))
                offset_start = 0
                offset_end = 0
                if residual > 0:
                    residual -= 1
                    offset_end = 1

                start_pos = run_count * step_size + offset_start
                end_pos = (run_count + 1) * step_size + offset_start + offset_end

                offset_start += offset_end


                start = time.time()

                # Filtering data

                modifier_random = np.zeros(np_scores_random.shape)
                modifier_all = np.zeros(np_scores_all.shape)

                modifier_random[:,start_pos:end_pos] += 1
                modifier_all[:,start_pos:end_pos]  += 1

                #np_scores_modified_random = np.multiply(np_scores_random[:], modifier_random)
                np_scores_modified_random = np_scores_random[:]
                np_scores_modified_all = np.multiply(np_scores_all[:], modifier_all)

                index_max_random = np.argmax(np_scores_modified_random, axis=1)
                index_max_all = np.argmax(np_scores_modified_all, axis=1)
                

                end = time.time()
                print("Done getting recommendations! It took: {} seconds".format(end - start))

                # Generate individual scores
                start = time.time()
                scores_individual = [[[] for i in range(len(group_type_mappings))] for i in range(amount)]
                j = 0
                for preference, configurationState  in requests_all:
                    individuals = preference.getIndividualPreferences()
                    i = 0
                    for individual in individuals:
                        scores_individual[j][i] = get_scores_for_one(configurationState, individual, finished_configurations, product_structure, scoring_function=scoring_function)
                        i += 1
                    j += 1
                end = time.time()
                print("Done generating individual scores! It took: {} seconds".format(end - start))


                #Generate hapiness level
                start = time.time()
                avg_happy_diff = 0
                avg_unhappy_diff = 0
                avg_happy_all = 0
                avg_unhappy_all = 0

                individual_index = 0
                for individuals_scores in scores_individual:
                    unhappy_rand = 0
                    unhappy_all = 0
                    happy_rand = 0
                    happy_all = 0

                    for individual_score in individuals_scores:
                        np_individual_score = np.array(individual_score)
                        unhappy_threshold = np.percentile(np_individual_score, center - threshold_distance_from_centre)
                        happy_threshold = np.percentile(np_individual_score, center + threshold_distance_from_centre)

                        score_rand = np_individual_score[index_max_random[individual_index]]
                        score_all = np_individual_score[index_max_all[individual_index]]

                        if score_all > happy_threshold:
                            happy_all += 1
                        elif score_all < unhappy_threshold:
                            unhappy_all += 1
                        if score_rand > happy_threshold:
                            happy_rand += 1
                        elif score_rand < unhappy_threshold:
                            unhappy_rand += 1
                    avg_happy_diff += happy_all - happy_rand
                    avg_unhappy_diff += unhappy_all - unhappy_rand
                    avg_happy_all += happy_all
                    avg_unhappy_all += unhappy_all

                    individual_index += 1

                avg_happy_diff /= amount
                avg_unhappy_diff /= amount
                avg_happy_all /= amount
                avg_unhappy_all /= amount

                happiness_diff_list.append(avg_happy_diff)
                unhappiness_diff_list.append(avg_unhappy_diff)

                happiness_all_list.append(avg_happy_all)
                unhappiness_all_list.append(avg_unhappy_all)

                print("-- Average increase in happiness: {} | Average increase in unhappiness: {}".format(avg_happy_diff, avg_unhappy_diff))
                print("-- Average happiness: {} | Average unhappiness: {}".format(avg_happy_all, avg_unhappy_all))
                end = time.time()
                print("Done rating recommendations! It took: {} seconds".format(end - start))
            
            happiness_db_size_avg_diff.append(np.average(np.array(happiness_diff_list)))
            unhappiness_db_size_avg_diff.append(np.average(np.array(unhappiness_diff_list)))

            happiness_db_size_avg_total_all.append(np.average(np.array(happiness_all_list)))
            unhappiness_db_size_avg_total_all.append(np.average(np.array(unhappiness_all_list)))

        results_happiness_db_size_avg_diff.append(happiness_db_size_avg_diff)
        results_unhappiness_db_size_avg_diff.append(unhappiness_db_size_avg_diff)

        results_happiness_db_size_avg_total_all.append(happiness_db_size_avg_total_all)
        results_unhappiness_db_size_avg_total_all.append(unhappiness_db_size_avg_total_all)

    column_names = db_sizes_label
    row_names = scoring_function_labels
    pd.DataFrame(results_happiness_db_size_avg_diff, index=row_names, columns=column_names).to_csv("{}/data/_happy_increase.csv".format(outdir), index=True, header=True, sep=',')
    pd.DataFrame(results_unhappiness_db_size_avg_diff, index=row_names, columns=column_names).to_csv("{}/data/_unhappy_increase.csv".format(outdir).format(outdir), index=True, header=True, sep=',')
    pd.DataFrame(results_happiness_db_size_avg_total_all, index=row_names, columns=column_names).to_csv("{}/data/_happy_total_all.csv".format(outdir), index=True, header=True, sep=',')
    pd.DataFrame(results_unhappiness_db_size_avg_total_all, index=row_names, columns=column_names).to_csv("{}/data/_unhappy_total_all.csv".format(outdir).format(outdir), index=True, header=True, sep=',')

  
    end_total = time.time()
    print("Done! Total time: {} seconds".format(end_total - start_total))

    axis=[0,150, -1, 0.5]
    pp.figure(figsize=(8,4), dpi=300)
    pp.subplots_adjust(hspace = 0.8, wspace=0.4)
    pp.subplot(1, 2, 1, title="happiness increase average", )

    for result_happy in results_happiness_db_size_avg_diff:
        pp.plot(db_sizes_label, result_happy)

    pp.legend(scoring_function_labels)
    pp.xlabel("number of stored configurations")
    pp.ylabel("number of people")
    pp.axis(axis)

    pp.subplot(1, 2, 2, title="unhappiness increase average")
    

    for result_unhappy in results_unhappiness_db_size_avg_diff:
        pp.plot(db_sizes_label, result_unhappy)
    
    pp.legend(scoring_function_labels)
    pp.xlabel("number of stored configurations")
    pp.ylabel("number of people")
    pp.axis(axis)

    pp.savefig("{}/fig/happy_unhappy_increase.pdf".format(outdir),format="pdf")
    pp.figure(figsize=(8,4), dpi=300)

   
    axis=[0,150, 0, 4]
    pp.subplots_adjust(hspace = 0.8, wspace=0.4)
    pp.subplot(1, 2, 1, title="happiness absolute average", )

    for result_happy in results_happiness_db_size_avg_total_all:
        pp.plot(db_sizes_label, result_happy)

    pp.legend(scoring_function_labels)
    pp.xlabel("number of stored configurations")
    pp.ylabel("number of people")
    pp.axis(axis)

    pp.subplot(1, 2, 2, title="unhappiness absolute average")
    

    for result_unhappy in results_unhappiness_db_size_avg_total_all:
        pp.plot(db_sizes_label, result_unhappy)
    
    pp.legend(scoring_function_labels)
    pp.xlabel("number of stored configurations")
    pp.ylabel("number of people")
    pp.axis(axis)

    pp.savefig("{}/fig/happy_unhappy_total_all.pdf".format(outdir),format="pdf")

def main_tuple(param):
    print("----------------------------------------------------------------------------------------")
    print("----------------------Starting: {}----------------------".format(param))
    print("----------------------------------------------------------------------------------------")
    main(amount=param[0], fullness=param[1],center=param[2] ,threshold_distance_from_centre = param[3], group_type= param[4])
    return True

if __name__ == "__main__":
    num_cores = multiprocessing.cpu_count()

    amounts = [1]
    fullnesses = [0.1]
    centers = [10, 20, 30, 40, 50, 60, 70, 80, 90]
    dists = [5]
    g_types = ["heterogeneous", "random", "homogenous"]

    params = list(itertools.product(amounts, fullnesses, centers, dists, g_types))

    pool = multiprocessing.Pool(processes=num_cores)  
    res = pool.map(main_tuple, params)

