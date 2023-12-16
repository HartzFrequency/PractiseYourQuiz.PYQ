import tkinter as tk
from tkinter import messagebox, ttk
from ttkbootstrap import Style
import json

# Read quiz data from a JSON file
with open("DataScience\\QuizDataBase.json", "r") as file:
    quiz_data = json.load(file)

# Create a text file to log incorrect answers
log_file = open("incorrect_answers.txt", "w")

# Function to display the current question and choices
def show_question():
    # Get the current question from the quiz_data list
    question_data = quiz_data[current_question]
    qs_label.config(text=question_data["question"])

    # Display the choices on the buttons
    choices = question_data["options"]
    for i in range(4):
        # Reset button state and update wrap length for each button
        choice_btns[i].config(text=choices[i], state="normal", wraplength=200, width=30, height=3)  # Set your desired size

    # Clear the feedback label, correct option label, and disable the next button
    feedback_label.config(text="")
    correct_option_label.config(text="")
    next_btn.config(state="disabled")

    # Update the canvas scroll region
    frame.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))

# Function to check the selected answer and provide feedback
def check_answer(choice):
    # Get the current question from the quiz_data list
    question_data = quiz_data[current_question]
    selected_choice = choice_btns[choice].cget("text")

    # Extract the choice identifier (e.g., "a", "b", "c", "d") from the selected choice
    selected_identifier = selected_choice.split(".")[0].strip().lower()

    # Check if the selected choice identifier matches the correct answer
    if selected_identifier == question_data["correct_option"]:
        # Update the score and display it
        global score
        score += 1
        score_label.config(text="Score: {}/{}".format(score, len(quiz_data)))
        feedback_label.config(text="Correct!", foreground="green")
    else:
        feedback_label.config(text="Incorrect!", foreground="red")
        # Show the correct option in green below the incorrect text
        correct_option_label.config(text="Correct answer: {}".format(question_data["correct_option"]), foreground="green")

        # Log the incorrect answer to the text file
        log_file.write("Quiz {}: Question {}: Incorrect\n".format(question_data["quiz_no"], question_data["question_no"]))

    # Disable all choice buttons and enable the next button
    for button in choice_btns:
        button.config(state="disabled")
    next_btn.config(state="normal")

    # Update the canvas scroll region
    frame.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))

# Function to move to the next question
def next_question():
    global current_question
    current_question += 1

    if current_question < len(quiz_data):
        # If there are more questions, show the next question
        show_question()
    else:
        # If all questions have been answered, display the final score and end the quiz
        messagebox.showinfo("Quiz Completed",
                            "Quiz Completed! Final score: {}/{}".format(score, len(quiz_data)))
        root.destroy()

# Create the main window
root = tk.Tk()
root.title("Quiz App")
root.geometry("500x750")
style = Style(theme="flatly")

# Create a canvas to hold the widgets
canvas = tk.Canvas(root)
canvas.pack(side="left", fill="both", expand=True)

# Create a vertical scrollbar
scrollbar = ttk.Scrollbar(root, command=canvas.yview)
scrollbar.pack(side="right", fill="y")

# Configure the canvas to use the scrollbar
canvas.configure(yscrollcommand=scrollbar.set)

# Create a frame to hold the widgets inside the canvas
frame = ttk.Frame(canvas)

# Add the frame to the canvas
canvas.create_window((0, 0), window=frame, anchor="center")

# Configure the font size for the question and choice buttons
style.configure("TLabel", font=("Helvetica", 20))
style.configure("TButton", font=("Helvetica", 16))

# Create the question label
qs_label = ttk.Label(
    frame,
    anchor="center",
    wraplength=500,
    padding=10
)
qs_label.pack(pady=10)

# Create the choice buttons using tk.Button
choice_btns = []
for i in range(4):
    button = tk.Button(
        frame,
        command=lambda i=i: check_answer(i),
        wraplength=200,  # Set your desired wraplength
        justify="left",  # Align text to the left
        width=30,  # Set your desired width
        height=3  # Set your desired height
    )
    button.pack(pady=5)
    choice_btns.append(button)

# Create the feedback label
feedback_label = ttk.Label(
    frame,
    anchor="center",
    padding=10
)
feedback_label.pack(pady=10)

# Create a label to display the correct option when the answer is incorrect
correct_option_label = ttk.Label(
    frame,
    anchor="center",
    padding=10
)
correct_option_label.pack(pady=10)

# Initialize the score
score = 0

# Create the score label
score_label = ttk.Label(
    frame,
    text="Score: 0/{}".format(len(quiz_data)),
    anchor="center",
    padding=10
)
score_label.pack(pady=10)

# Create the next button
next_btn = ttk.Button(
    frame,
    text="Next",
    command=next_question,
    state="disabled"
)
next_btn.pack(pady=10)

# Initialize the current question index
current_question = 0

# Show the first question
show_question()

# Update the canvas scroll region
frame.update_idletasks()
canvas.configure(scrollregion=canvas.bbox("all"))

# Start the main event loop
root.mainloop()

# Close the log file
log_file.close()
