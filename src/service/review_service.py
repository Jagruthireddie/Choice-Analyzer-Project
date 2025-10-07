from src.dao import review_dao

def add_review(scenario_id, positive, negative, admin_id):
    return review_dao.add_review(scenario_id, positive, negative, admin_id)

def get_reviews(scenario_id):
    return review_dao.get_reviews_for_scenario(scenario_id)
