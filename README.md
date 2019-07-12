DATASET DESCRIPTION:
1. all_projects.csv consists of list of projects corresponding to the different programming language. We have selected Python specific projects only.

2. manual_annotated_pr.json consists of all manually labeled pull requests along with the corresponding interaction types between generator and commenters. This file has an array of json object with the following format:
{project name: {PR ID: {commenter1: score}}}

3. result_trust_values.csv consists of resulting trust values (belief, disbelief, uncertainty) with corresponding PR status (accepted, rejected).

4. PR Requests.zip consists of the response of all pull requests for 179 projects from the GitHub API. Each response is stored as the following:
      PR number:{response}
For the response format refer to the link: https://developer.github.com/v3/pulls/

5. preprocomm.json.zip consists of all the preprocessed comments. The file has an array of json object with the following format:
{projectname: {pr_id: [generator, creation date, {commenter: comment}]}}
6. accuracy_trust_metrics.csv consists of the accuracy metrics (precision, recall, f1-score) obtained using Trust model for 30 different replicas.
7. accuracy_pr_hist.csv consists of the accuracy metrics (precision, recall, f1-score) obtained using History model for 30 different replicas.
8. accuracy_trust_pr_hist.csv consists of the accuracy metrics (precision, recall, f1-score) obtained using Hybrid model for 30 different replicas.

CODE DESCRIPTION:

   It has following python scripts:
1. train.py:
    Trains the model using a manually labeled dataset and stores the corresponding trained model on             Dateset/Generated/finalized_model.sav.

2. predict.py:
   Predicts the interaction type for rest of the unlabeled comments. Unlabeled data should be under the directory        Dataset/Generated with the name preprocomm.json. Each json object has the following format
   {projectname: {pr_id: [generator, creation date, {commenter: comment}]}}

3. preprocess_record.py
   Maps interaction types from 1-5 to -1-1.

4. construct_graph.py
   Constructs CDN and assigns edge edge with a corresponding trust values
   
5. trustpropagation.py
    Propagates trust between any pair of developers
    
6. PR_evaluation.py
   Computes trust value for the pull requests that are in a test set
 
RESULT REPLICATION DESCRIPTION:
1. To generate table 4, use train.py with different regression techniques. For this use preprocomm.json located in Dataset/Generated directory.
2. To generate table 5, use the network constructed using construct_graph.py and use trustpropagation.py. 
3. To generate Figure 4, 5, and 6 , use result_trust_values.txt located in Dataset directory.
4. To generate generate the data for table 6, use Pull-Requests.zip (divided into Pull-Requests-part1.zip, Pull-requests-part2.zip, and Pull-Requests-part3.zip)  and result_trust_values.txt. 
   
