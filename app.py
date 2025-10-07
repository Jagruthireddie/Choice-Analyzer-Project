import streamlit as st
from src.service import user_service, scenario_service, review_service

st.set_page_config(page_title="Ethical Decision Simulator", page_icon="🧭")

# Session state for login
if "user" not in st.session_state:
    st.session_state.user = None


def login():
    st.header("🔑 Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user = user_service.login_user(email, password)
        if user:
            st.session_state.user = user
            st.success(f"Welcome, {user['name']} ({user['role']})!")
        else:
            st.error("Invalid credentials.")


def register():
    st.header("📝 Register")
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    role = st.selectbox("Role", ["user", "admin"])
    if st.button("Register"):
        user_service.register_user(name, email, password, role)
        st.success("Registration successful! Please log in.")


def user_dashboard(user):
    st.header("🙋 User Dashboard")
    st.subheader("Describe Your Ethical Dilemma")
    dilemma = st.text_area("Write about your dilemma situation:")
    if st.button("Submit Dilemma"):
        if dilemma.strip():
            scenario_service.create_scenario(user["id"], dilemma)
            st.success("Your dilemma has been submitted for review.")
        else:
            st.warning("Please describe your dilemma before submitting.")

    st.divider()
    st.subheader("📜 Your Past Dilemmas & Advice")
    scenarios = scenario_service.view_all_scenarios()
    user_scenarios = [s for s in scenarios if s["user_id"] == user["id"]]

    if not user_scenarios:
        st.info("You haven't submitted any dilemmas yet.")
    else:
        for s in user_scenarios:
            st.write(f"**Situation:** {s['description']}")
            reviews = review_service.get_reviews(s["id"])
            if reviews:
                for r in reviews:
                    st.success("✅ Positive Advice: " + r["positive_advice"])
                    st.error("⚠️ Negative Advice: " + r["negative_advice"])
            else:
                st.info("No advice yet from admin.")
            st.markdown("---")

    if st.button("Logout"):
        st.session_state.user = None


def admin_dashboard(user):
    st.header("🧑‍⚖️ Admin Dashboard")
    scenarios = scenario_service.view_all_scenarios()

    if not scenarios:
        st.info("No dilemmas submitted yet.")
    else:
        for s in scenarios:
            st.write(f"**Scenario ID:** {s['id']}")
            st.write(f"**User ID:** {s['user_id']}")
            st.write(f"**Dilemma:** {s['description']}")

            reviews = review_service.get_reviews(s["id"])
            if reviews:
                st.success("✅ Already has advice.")
                for r in reviews:
                    st.write(f"Positive: {r['positive_advice']}")
                    st.write(f"Negative: {r['negative_advice']}")
            else:
                st.subheader("Add Advice:")
                pos = st.text_area(f"Positive advice for scenario {s['id']}", key=f"pos_{s['id']}")
                neg = st.text_area(f"Negative advice for scenario {s['id']}", key=f"neg_{s['id']}")
                if st.button(f"Submit Advice for {s['id']}", key=f"btn_{s['id']}"):
                    review_service.add_review(s["id"], pos, neg, user["id"])
                    st.success("Advice added successfully.")
            st.markdown("---")

    if st.button("Logout"):
        st.session_state.user = None


def main():
    st.title("🧭 Ethical Decision Simulator")

    if st.session_state.user:
        if st.session_state.user["role"] == "admin":
            admin_dashboard(st.session_state.user)
        else:
            user_dashboard(st.session_state.user)
    else:
        choice = st.sidebar.selectbox("Menu", ["Login", "Register"])
        if choice == "Login":
            login()
        elif choice == "Register":
            register()


if __name__ == "__main__":
    main()
