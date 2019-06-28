# Trust
Code for the paper "Estimating Trust between OSS Developers"

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
1. To generate table 4, use train.py with different regression techniques. For this use preprocomm.json data which can be downloaded from the link https://figshare.com/s/954f57da35d62f870ad8.
2. To generate table 5, use the network constructed using construct_graph.py and use trustpropagation.py. 
3. To generate Figure 4, 5, and 6 , download result_trust_values.txt dataset.
4. To generate generate the data for table 6, download Pull Requests.zip and result_trust_values.txt  data from the link https://figshare.com/s/954f57da35d62f870ad8 and run the required classifiers from the scikit-learn package. 
   
