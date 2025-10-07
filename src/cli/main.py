import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from src.service import user_service, scenario_service, review_service

def user_menu(user):
    while True:
        print("\n=== User Menu ===")
        print("1) Explain Dilemma")
        print("2) View My Scenarios")
        print("3) Logout")
        c = input("Choice: ")

        if c == "1":
            desc = input("\nDescribe your dilemma situation:\n")
            scenario = scenario_service.create_scenario(user["id"], desc)
            print("Situation submitted for review!" if scenario else "Error submitting.")
        elif c == "2":
            scenarios = scenario_service.view_all_scenarios()
            for s in scenarios:
                if s["user_id"] == user["id"]:
                    print(f"\nID: {s['id']} | {s['description']}")
                    reviews = review_service.get_reviews(s["id"])
                    if reviews:
                        for r in reviews:
                            print(f" Positive: {r['positive_advice']}")
                            print(f" Negative: {r['negative_advice']}")
                    else:
                        print(" No reviews yet.")
        elif c == "3":
            break
        else:
            print("Invalid choice!")

def admin_menu(admin):
    while True:
        print("\n=== Admin Menu ===")
        print("1) View All Dilemmas")
        print("2) Add Advice")
        print("3) Logout")
        c = input("Choice: ")

        if c == "1":
            scenarios = scenario_service.view_all_scenarios()
            for s in scenarios:
                print(f"ID: {s['id']} | User: {s['user_id']} | {s['description']}")
        elif c == "2":
            sid = input("Enter Scenario ID: ")
            pos = input("Positive advice: ")
            neg = input("Negative advice: ")
            review = review_service.add_review(int(sid), pos, neg, admin["id"])
            print("Review added!" if review else "Error adding review.")
        elif c == "3":
            break
        else:
            print("Invalid choice!")

def main():
    while True:
        print("\n=== Ethical Decision Simulator ===")
        print("1) Register")
        print("2) Login")
        print("3) Exit")
        ch = input("Choice: ")

        if ch == "1":
            name = input("Name: ")
            email = input("Email: ")
            pwd = input("Password: ")
            role = input("Role (user/admin) [user]: ") or "user"
            user_service.register_user(name, email, pwd, role)
            print("Registered successfully!")

        elif ch == "2":
            email = input("Email: ")
            pwd = input("Password: ")
            user = user_service.login_user(email, pwd)
            if not user:
                print("Invalid credentials.")
            elif user["role"] == "admin":
                admin_menu(user)
            else:
                user_menu(user)
        elif ch == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
