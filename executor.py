import sys
import importlib
import json
import logging

logger = logging.getLogger("execcutor_project_logger")
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))

def execute_step(step, pre_conditions = None, previous_result = None):
    status = "OK"
    func = step['function']

    module = importlib.import_module(func)    
    if 'previous_result' in step['input']:
        params = [previous_result] + step['input'][1:]
    else:
        params = step['input']
    result = None
    try:
        result = module.main(*params)
    except BaseException as error:
        status = "FAILED"
        result = str(error)
        pass
    return {"result": result, 'status': status}


def execute_workflow(workflow_name):
    with open(f"{workflow_name}.json", "rb") as flow:
        workflow = json.load(flow)

    step = workflow['steps'][0]
    return_ = execute_step(step)
    count_steps = 0
    logger.info(f"On step {count_steps}")
    logger.info(f"Status: {return_['status']}")


    while (return_['status'] == 'OK' and count_steps < (len(workflow['steps']) - 1)):
        count_steps += 1
        logger.info(f"On step {count_steps}")
        return_ = execute_step(workflow['steps'][count_steps], previous_result = return_['result'])
        logger.info(f"Status: {return_['status']}")

    
    if return_['status'] != 'OK':
        message_error = f"The step #{step['number']} has failed, the executor stopped, error: {return_['result']}"
        logger.error(message_error) 
    else:
        logger.info("The execution has been complete")


if __name__ == '__main__':
    execute_workflow(sys.argv[1])