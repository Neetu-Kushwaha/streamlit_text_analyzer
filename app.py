import streamlit as st
import pandas as pd
import base64

def main():
    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

        # Initialize index variables to track current row for text, answer, and feedback
        text_index = st.session_state.get("text_index", 0)
        answer_index = st.session_state.get("answer_index", 0)
        feedback_index = st.session_state.get("feedback_index", 0)

        # Load the feedback dictionary from session state
        feedback_dict = st.session_state.get("feedback_dict", {})
        if not feedback_dict:
            feedback_dict = {i: "" for i in range(len(df))}

        # Custom title for the webpage with a colorful background
        st.markdown(
            """
            <div style='background-color: #f63366; padding: 10px;'>
                <h1 style='color: white; text-align: center;'>Financial Damage</h1>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Display the feedback section with colorful headers
        st.subheader("Feedback:")
        feedback_options = ["Right", "Wrong", "Average"]
        user_feedback = st.selectbox("Select Feedback:", feedback_options)

        # Store the selected feedback for the current index
        feedback_dict[feedback_index] = user_feedback
        st.session_state.feedback_dict = feedback_dict

        # Button to display next entry with a colorful background
        if st.button("Next"):
            # Check if index is within bounds of the DataFrame
            if text_index < len(df) - 1 and answer_index < len(df) - 1 and feedback_index < len(df) - 1:
                # Increment index to display the next entry
                text_index += 1
                answer_index += 1
                feedback_index += 1

        # Button to display previous entry with a colorful background
        if st.button("Previous"):
            # Check if index is greater than 0
            if text_index > 0 and answer_index > 0 and feedback_index > 0:
                # Decrement index to display the previous entry
                text_index -= 1
                answer_index -= 1
                feedback_index -= 1

        # Store the updated index variables in session state
        st.session_state.text_index = text_index
        st.session_state.answer_index = answer_index
        st.session_state.feedback_index = feedback_index

        # Display the current entry
        display_entry(df, text_index, answer_index)

        # Display the selected feedback on the right side with a colorful sidebar
        st.sidebar.subheader("Selected Feedback:")
        st.sidebar.text_area("Feedback:", value=feedback_dict.get(feedback_index, ""), height=100)

        # Save feedback to a CSV file
        save_feedback(feedback_dict)

        # Add a button to download the feedback CSV file
        if st.button("Download Feedback CSV"):
            download_feedback_csv(feedback_dict)


def display_entry(df, text_index, answer_index):
    # Create columns layout with text and answer side by side
    col1, col2 = st.columns(2)

    # Display text in the first column with a colorful background
    with col1:
        st.subheader("Text:")
        text = df.loc[text_index, "texts"]
        text = escape_dollar_signs(text)
        st.write(text)

    # Display answer in the second column with a colorful background
    with col2:
        st.subheader("Answer:")
        answer = df.loc[answer_index, "Answer"]
        answer = escape_dollar_signs(answer)
        st.write(answer)


def escape_dollar_signs(text):
    # Escape dollar signs to prevent Markdown interpretation
    return text.replace("$", "\\$")


def save_feedback(feedback_dict):
    # Convert feedback dictionary to DataFrame
    feedback_df = pd.DataFrame.from_dict(feedback_dict, orient="index", columns=["Feedback"])
    # Add an index column
    feedback_df["Index"] = feedback_df.index
    # Save feedback to a CSV file
    feedback_df.to_csv("feedback.csv", index=False)


def download_feedback_csv(feedback_dict):
    # Convert feedback dictionary to DataFrame
    feedback_df = pd.DataFrame.from_dict(feedback_dict, orient="index", columns=["Feedback"])
    # Add an index column
    feedback_df["Index"] = feedback_df.index
    # Convert DataFrame to CSV
    csv = feedback_df.to_csv(index=False)
    # Encode CSV file to Base64
    b64 = base64.b64encode(csv.encode()).decode()
    # Create a download link
    href = f'<a href="data:file/csv;base64,{b64}" download="feedback.csv">Download Feedback CSV File</a>'
    # Display the download link
    st.markdown(href, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
