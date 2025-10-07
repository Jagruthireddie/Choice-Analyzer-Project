from src.dao import scenario_dao

def create_scenario(user_id, description):
    return scenario_dao.add_scenario(user_id, description)

def view_all_scenarios():
    return scenario_dao.get_all_scenarios()
