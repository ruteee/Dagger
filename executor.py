from cmath import log
import sys
import importlib
import json
import logging
from unittest import result

logger = logging.getLogger("execcutor_project_logger")
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))

def execute_step(step, pre_conditions = None, previous_results = None):
    status = "OK"
    func = step['function']

    module = importlib.import_module(func)    
    if 'previous_results' in list(step['input'].keys()):
        step['input']['previous_results'] = previous_results
   
    result = None
    try:
        result = module.main(**step['input'])
    except BaseException as error:
        status = "FAILED"
        result = str(error)
        pass
    return {"result": result, 'status': status}


def execute_workflow(workflow_name):
    with open(f"{workflow_name}.json", "rb") as flow:
        workflow = json.load(flow)

    steps_status = {}
    results_list = {}

    step = workflow['steps'][0]
    return_ = execute_step(step)
    
    count_steps = 0
    logger.info(f"On step {count_steps}")
    logger.info(f"Status: {return_['status']}")

    if return_['status'] != 'OK':
        message_error = f"The step #{step['number']} has failed, the executor has stopped, error: {return_['result']}"
        logger.error(message_error)
        return
    else:
        steps_status[0] = 1
        results_list['step_0'] = return_['result']

    while (count_steps < (len(workflow['steps']) - 1)):
        count_steps += 1
        logger.info(f"On step {count_steps}")
        step = workflow['steps'][count_steps]
        pre_conditions = step['pre-conditions']

        conditions_ok = True
        conditions_not_ok = []
        for condition in pre_conditions:
            if steps_status[condition] != 1:
                conditions_ok = False
                conditions_not_ok.append(condition)
        
        return_ = None
        if not conditions_ok:
            steps_status[count_steps] = 0
            logger.error(f"The execcution has failed because pre-conditions {conditions_not_ok} were not attended")
            return
        else:
            return_ = execute_step(step, previous_results=results_list)
            if return_['status'] != 'OK':
                steps_status[count_steps] = 0
                message_error = f"The step #{step['number']} has failed, the executor stopped, error: {return_['result']}"
                logger.error(message_error)
            else:
                steps_status[count_steps] = 1
                results_list[f'step_{count_steps}'] = return_['result']
        
        logger.info(f"Status: {return_['status']}")


    if return_['status'] == 'OK':
        logger.info("The execution has been complete")
        logger.info(f"Result {return_['result']}")
        return return_['result']
    else:
        error_msg = f"The execution has been stopped because step {count_steps} has failed"
        logger.info(error_msg)
        return error_msg




if __name__ == '__main__':
    execute_workflow(sys.argv[1])