import sys
import importlib
import json
import logging

logger = logging.getLogger("execcutor_project_logger")
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))

def execute_task(task, previous_results = None):
    status = "OK"
    func = task['function']

    module = importlib.import_module(func)    
    if 'previous_results' in list(task['input'].keys()):
        task['input']['previous_results'] = previous_results
   
    result = None
    try:
        result = module.main(**task['input'])
    except BaseException as error:
        status = "FAILED"
        result = str(error)
        pass
    return {"result": result, 'status': status}


def execute_workflow(workflow_name):
    with open(f"{workflow_name}.json", "rb") as flow:
        workflow = json.load(flow)

    tasks_status = {}
    results_dict = {}

    task = workflow['tasks'][0]
    return_ = execute_task(task)
   
    logger.info("Starting dag flow\n")
    for task in workflow['tasks'][0:]:
        logger.info(f"On task {task['number']}")
        pre_conditions = task['pre-conditions']

        logger.info("Looking for pre-conditions")
        for condition in pre_conditions:
            if f"task_{condition}" not in list(tasks_status.keys()):
                task_in_between = workflow['tasks'][condition]
                return_ = execute_task(task_in_between, previous_results=results_dict)
                if return_['status'] != 'OK':
                    error_msg =f"The execcution has failed because pre-condition {condition} were not attended, error: {return_['result']}"
                    logger.error(error_msg)
                    return
                else:
                    tasks_status[condition] = 1
                    results_dict[f'task_{condition}'] = return_['result']    
                logger.info(f"Status: {return_['status']}")
                            
        return_ = None
        task_previous_results = {}
        for node in pre_conditions:
            task_previous_results.update({f"task_{node}": results_dict[f"task_{node}"]})          

        logger.info("Executing task function")
        return_ = execute_task(task, previous_results=task_previous_results)
        if return_['status'] != 'OK':
            tasks_status[f'task_{task["number"]}'] = 0
            error_msg = f"The task #{task['number']} has failed, the executor stopped, error: {return_['result']}"
            logger.error(error_msg)
            return
        else:
            tasks_status[f'task_{task["number"]}']= 1
            results_dict[f'task_{task["number"]}'] = return_['result']
        logger.info(f"Status: {return_['status']}\n")


    logger.info("The execution has been complete")

    logger.info(f"Result f the final task: {return_['result']}")
    return return_['result']

if __name__ == '__main__':
    execute_workflow(sys.argv[1])