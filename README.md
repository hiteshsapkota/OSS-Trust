DATASET DESCRIPTION:
====================
1. all_projects.csv consists of list of projects corresponding to the different programming language. We have selected Python specific projects only.

2. manual_annotated_pr.json consists of all manually labeled pull requests along with the corresponding interaction types between generator and commenters. This file has an array of json object with the following format:
{project name: {PR ID: {commenter1: score}}}

3. result_trust_values.csv consists of resulting trust values (belief, disbelief, uncertainty) with corresponding PR status (accepted, rejected).

4. PR Requests.zip consists of the response of all pull requests for 179 projects from the GitHub API. Each response is stored as the following:
      PR number:{response}
For the response format refer to the link: https://developer.github.com/v3/pulls/

5. preprocomm.json.zip consists of all the preprocessed comments. The file has an array of json object with the following format:
{projectname: {pr_id: [generator, creation date, {commenter: comment}]}}

6. manual_annotation.csv consists of a manually annotated score for the generator from commenter's perspective. Corresponding preprocessed commenter's comment can be fetched as preprocomm[projectname][pr_id][2][commenter] from the preprocomm.json file. 

7. accuracy_trust_metrics.csv consists of the accuracy metrics (precision, recall, f1-score, tp, tn, fp, fn) obtained using Trust model for 30 repetitions.

8. accuracy_pr_hist.csv consists of the accuracy metrics (precision, recall, f1-score, tp, tn, fp, fn) obtained using History model for 30 repetitions.

9. accuracy_trust_pr_hist.csv consists of the accuracy metrics (precision, recall, f1-score, tp, tn, fp, fn) obtained using Hybrid model for 30 repetitions.

10. MAE_classifier.json consists of MAE score for the regression techniques described in Table 4. It has following format:
  {Classifier_name: [MAE values for 30 repetitions]}
11. time_performance_classifier.json: consists of a MAE score for the time based classifier
12. time_performance_regression.json: consists of a MAE score for time based regression models
13. repo_score.json: consists of a MAE score for each repository
14. 

CODE DESCRIPTION:
=================
It has following python scripts:

1. train.py:
    Trains the model using a manually labeled dataset and stores the corresponding trained model on             Dateset/Generated/finalized_model.sav.

2. predict.py:
   Predicts the interaction type for rest of the unlabeled comments. Unlabeled data should be under the directory        Dataset/Generated with the name preprocomm.json. Each json object has the following format
   {projectname: {pr_id: [generator, creation date, {commenter: comment}]}}

3. preprocess_record.py
   Maps interaction types from 1 to 5 -> -1 to 1.

4. construct_graph.py
   Constructs CDN and assigns edge with a corresponding trust values
   
5. trustpropagation.py
    Propagates trust between any pair of developers
    
6. PR_evaluation.py
   Computes trust value for the pull requests that are in a test set
   
7. classifier.py
   Computes and stores the accuracy metrics (precision, recall, f1-score, tp, tn, fp, fn) for Decision Tree classifier for:         (1) History Model, (2) Trust Model, (3) Hybrid Model.
 
RESULT REPLICATION DESCRIPTION:
===============================
1. To generate Table 4, use train.py with different regression techniques. For this use preprocomm.json located in Dataset/Generated directory.
2. To generate Table 5, use the network constructed using construct_graph.py and use trustpropagation.py. 
3. To generate Figure 4, 5, and 6, use result_trust_values.txt located in Dataset directory.
4. To generate generate the data for Table 6, use Pull-Requests.zip (divided into Pull-Requests-part1.zip, Pull-requests-part2.zip, and Pull-Requests-part3.zip) and result_trust_values.txt. 
   
For any questions, please email hxs1943@rit.edu
