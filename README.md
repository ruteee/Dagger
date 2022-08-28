# Dagger

This repo contains a python implementation of a DAG executor (executor.py).

The executor runs throug the reading of a workflow file in the json format, containig the dags definition.

In order for this executor to work, you have to keep the workflow json files in the root folder.

## How to use?

Each workflow file (DAG) must contain a list of tasks, where each task is also defined as an object containg the following attributes: 

    * number - The task ID.
    * function  - The fuction that will be performed in the task.
    * input - An object containing the pairs: parameter name and value, that will be passed to the function.
    * pre-conditions - A list of the tasks IDs the current task depends on.

If you want to access the previous results of the task you depends on, you must pass the parameter 'previous_results' set to "True" 
to the input attribute.

    - "previous_results" : "True"

    - In the function implementation you must access the previous result you need using the key: 'task_id' where 'id' is 
    the id of the task you want the results 
        - Ex: previous_results['task_0]

All of functions used in the tasks, **must** be defined in py script named with the same name of the function. 
In the py script, you have to define a function named **main** (this is mandatory) having thte same parameters indicated in input.

For example, if you have the following task definition:

    {
        "number" : 0,
        "function": "sum_numbers",
        "input": {"number_1": 1, "number_2" : 2]},
        "pre-conditions": []
    }

Suposing your function only sum two numbers, you would create a file named sum_numbers.py and this file will have the following structure:

    def main(number_1, number_2):

        return number_1 + number_2
        
If your functions need to access results of other task, you neeed add the parameter 'previous_results' as a parameter in the function
implementation.
   
   For example, if you have the following task definition:
       {
           "number" : 1,
           "function": "my_function",
           "input": {"previous_results" : "True", "my_param": 1 },
           "pre-conditions": [0]
       }
       
   Then, besides your params, the function definition will have to include previous_results as a param.
   
      def main(previous_results, my_param):
      
         #Form of accessing the result of task 0
         result_task_0 = previous_results['task_0'] 
         #Function body example...
         print(my_param,result_task_0 )
  
   

It is provided in this repo, two workflows example: workflow_data.json an work_flow_test0.json

For a better understanding, we wil briefly explain the workflow_data.json file. But you can always consult the other examples. 

## Workflow_data

In this workflow we will read a dataset named 'sports_data.csv'. This dataset contains informations about sports preferences. 
It possess the following columns: person (the person name), plays (the sport the peerson plays), and birth_dt.


    {
        "tasks": [{
            "number" : 0,
            "function": "drop_nans",
            "input": {"path": "sports_data.csv", "subset": ["plays"]},
            "pre-conditions": []
        },
        {
            "number" : 1,
            "function": "compute_age",
            "input": {"previous_results": "True", "col": "birth_dt"},
            "pre-conditions": [0]
        },

        {
            "number": 2,
            "function": "groupby",
            "input": {"previous_results": "True", "by": ["plays", "age"], "agg_func": "size"},
            "pre-conditions": [1]
        }]
    }


### Tasks description
    Task 0 - Reads the dataset and drop nan values

        function : In this task we execute the function: drop_nans.

        input: The parameters of drop_nans are specified in 'input'. Here we have 'path' - the location of the dataset and
        subset - the columns used as subset for dropping.

        pre-conditions: As this task does not rely in any other, the 'pre-conditions' are set as an empty list

    Task 1 - Receives the results of task 0 and add the column 'age'.

        function : In this task we execute the function: compute_age.

        input: The parameters of drop_nans are specified in 'input'. Here we have 'previous_results' - 
        indicating we want the result of the depending task (0),  and 'col' - indicating the column we will use 
        for computing the age, in this case: 'birth_dt'

        pre-conditions: This task depends on taks 0, since it will use the dataframe without nans to add the column 'age'

    Task 2 - Group the data.

        function: In this taks we perform the function groupby.

        input: The parameters of groupby are speciefied in input. Here we have 'previous_results' - indicating we want 
        the result of the depending task (1), 'by' - the coloumns we will group the data by,
        and agg_func - the aggregation function.

        pre-conditions: This task depends on taks 1, since it will use the column 'age' as one of our groupers, 
        and this columns was added on the task 1
