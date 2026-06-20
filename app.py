import streamlit as st
import pandas as pd
import os

# =====================================
# PAGE CONFIG
# =====================================
st.set_page_config(
    page_title="Building Condition Tracker",
    page_icon="🏢",
    layout="wide"
)

st.title("🏢 Building Condition Tracking System")

st.markdown("""
This application allows inspectors to record building conditions,
upload photographs from multiple viewpoints, and maintain a centralized asset database.
""")

# =====================================
# DATABASE FILE
# =====================================
DATABASE = "Building_Condition_Tracker.csv"

if os.path.exists(DATABASE):
    df = pd.read_csv(DATABASE)
else:
    df = pd.DataFrame(columns=[
        "Building ID",
        "Building Name",
        "Condition",
        "Estimated Repair Cost",
        "Front View",
        "Left Side View",
        "Right Side View",
        "Rear View"
    ])

# =====================================
# INPUT FORM
# =====================================
st.header("Building Inspection Form")

with st.form("inspection_form"):

    building_id = st.text_input("Building ID")

    building_name = st.text_input("Building Name")

    condition = st.selectbox(
        "Condition",
        [
            "Good",
            "Minor Repair",
            "Moderate Repair",
            "Major Repair",
            "Critical"
        ]
    )

    repair_cost = st.number_input(
        "Estimated Repair Cost (₱)",
        min_value=0.0
    )

    st.subheader("Upload Building Photos")

    front_view = st.file_uploader(
        "Front View",
        type=["jpg", "jpeg", "png"],
        key="front"
    )

    left_view = st.file_uploader(
        "Left Side View",
        type=["jpg", "jpeg", "png"],
        key="left"
    )

    right_view = st.file_uploader(
        "Right Side View",
        type=["jpg", "jpeg", "png"],
        key="right"
    )

    rear_view = st.file_uploader(
        "Rear View",
        type=["jpg", "jpeg", "png"],
        key="rear"
    )

    submit = st.form_submit_button("Save Inspection")

# =====================================
# SAVE RECORD
# =====================================
if submit:

    new_record = pd.DataFrame({
        "Building ID": [building_id],
        "Building Name": [building_name],
        "Condition": [condition],
        "Estimated Repair Cost": [repair_cost],
        "Front View": [front_view.name if front_view else ""],
        "Left Side View": [left_view.name if left_view else ""],
        "Right Side View": [right_view.name if right_view else ""],
        "Rear View": [rear_view.name if rear_view else ""]
    })

    df = pd.concat([df, new_record], ignore_index=True)

    df.to_csv(DATABASE, index=False)

    st.success("Inspection Record Saved Successfully!")

# =====================================
# VIEW DATABASE
# =====================================
st.header("Inspection Records")

st.dataframe(df, use_container_width=True)

# =====================================
# IMAGE PREVIEW
# =====================================
st.header("Building Image Views")

col1, col2 = st.columns(2)

with col1:
    if front_view:
        st.subheader("Front View")
        st.image(front_view)

    if left_view:
        st.subheader("Left Side View")
        st.image(left_view)

with col2:
    if right_view:
        st.subheader("Right Side View")
        st.image(right_view)

    if rear_view:
        st.subheader("Rear View")
        st.image(rear_view)

# =====================================
# SUMMARY DASHBOARD
# =====================================
st.header("Condition Summary")

if not df.empty:

    summary = df["Condition"].value_counts()

    st.bar_chart(summary)

else:
    st.info("No inspection records yet.")