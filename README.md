# Trust
Code for the paper "Estimating Trust between OSS Developers"

It has following python scripts:
1. train.py:
    Trains the model using a manually labeled dataset and stores the corresponding trained model on             Dateset/Generated/finalized_model.sav.

2. predict.py:
   Predicts the interaction type for rest of the unlabeled comments

3. preprocess_record.py
   Maps interaction types from 1-5 to -1-1.

4. construct_graph.py
   Constructs CDN and assigns edge edge with a corresponding trust values
   
5. trustpropagation.py
    Propagates trust between any pair of developers
    
6. PR_evaluation.py
   Computes trust value for the pull requests that are in a test set
   
   
