import tkinter as tk
from tkinter import ttk, messagebox
import requests 
import random 
import time
from PIL import Image, ImageTk
from tkinter import PhotoImage


class WelcomePage:
    def __init__(self, root, on_start_click):
        self.root = root

        self.root.geometry("500x500")
        self.root.title("welcome")

        # to load background image
        self.bg_image = PhotoImage(file="bg.png")  # Replace with the actual file path
        canvas = tk.Canvas(root, width=self.bg_image.width(), height=self.bg_image.height())
        canvas.pack()
        bg_image_reference = canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_image)        

        # animation for the opening title
        self.animation = PhotoImage(file="giphy.gif")
        canvas.create_image(0, 0, anchor=tk.NW, image=self.animation)

        # Style the Start button with a larger font
        style = ttk.Style()
        style.configure("Start.TButton", font=("Helvetica", 18, "bold"), foreground="darkblue", background="lightblue")
        start_button = ttk.Button(root, text="Start", command=on_start_click, style="Start.TButton")
        start_button.place(relx=0.5, rely=0.80, anchor="center")

   
class CategorySelectionPage:# CategorySelectionPage class handles the page for selecting quiz category, number of questions, and difficulty level

    def __init__(self, root, on_category_selected):
        self.root = root
        self.root.title("Category Selection")
        self.root.geometry("500x400")

        # Create a frame to hold the category buttons and center it
        frame = ttk.Frame(root)
        frame.pack(expand=True, fill="both")

        # Configure columns and rows to center the elements
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        frame.columnconfigure(2, weight=1)
        frame.rowconfigure(0, weight=1)
        frame.rowconfigure(1, weight=1)
        frame.rowconfigure(2, weight=1)
        frame.rowconfigure(3, weight=1)

        self.selected_category = None
        self.selected_num_questions = None
        self.selected_difficulty = None

        # Choosing the category label
        choose_category_label = ttk.Label(frame, text="Choose the category:", font=("Helvetica", 16, "bold"))
        choose_category_label.grid(row=0, column=0, columnspan=3, pady=5)
        
        # Category buttons in a 3x3 layout
        categories = {"General Knowledge": 9, "Art": 25, "History": 23, "Geography": 22, "Animals": 27, "Sports": 21}
        for idx, (category, category_id) in enumerate(categories.items()):
            row = 1 + idx // 3
            col = idx % 3
            
        #category button creation  
            category_button = ttk.Button(frame, text=category,
                                         command=lambda cat=category, cat_id=category_id: self.on_category_selected(on_category_selected, cat, cat_id),
                                         style="Category.TButton")

            category_button.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

        # Choosing the set of questions label
        choose_questions_label = ttk.Label(frame, text="Choose the set of questions:", font=("Helvetica", 16, "bold"))
        choose_questions_label.grid(row=4, column=0, columnspan=3, pady=5)

        # Number of questions boxes
        self.num_questions_5_button = ttk.Button(frame, text="5 Questions",
                                                command=lambda: self.on_num_questions_selected(on_category_selected, "5"),
                                                style="Question.TButton")
        self.num_questions_5_button.grid(row=5, column=0, padx=10, pady=10, sticky="nsew")

        self.num_questions_10_button = ttk.Button(frame, text="10 Questions",
                                                 command=lambda: self.on_num_questions_selected(on_category_selected, "10"),
                                                 style="Question.TButton")
        self.num_questions_10_button.grid(row=5, column=1, padx=10, pady=10, sticky="nsew")

        # Choose the challenge level label
        choose_difficulty_label = ttk.Label(frame, text="Choose the challenge level:", font=("Helvetica", 16, "bold"))
        choose_difficulty_label.grid(row=6, column=0, columnspan=3, pady=5)

        # Difficulty buttons
        self.easy_button = ttk.Button(frame, text="Easy", command=lambda: self.on_difficulty_selected(on_category_selected, "Easy"),
                                      style="Difficulty.TButton")
        self.easy_button.grid(row=7, column=0, padx=10, pady=10, sticky="nsew")

        self.medium_button = ttk.Button(frame, text="Medium", command=lambda: self.on_difficulty_selected(on_category_selected, "Medium"),
                                        style="Difficulty.TButton")
        self.medium_button.grid(row=7, column=1, padx=10, pady=10, sticky="nsew")

        self.hard_button = ttk.Button(frame, text="Hard", command=lambda: self.on_difficulty_selected(on_category_selected, "Hard"),
                                      style="Difficulty.TButton")
        self.hard_button.grid(row=7, column=2, padx=10, pady=10, sticky="nsew")

        # Play button
        self.play_button = ttk.Button(frame, text="Play", command=self.start_trivia_app, state=tk.DISABLED, style="Play.TButton")
        self.play_button.grid(row=8, column=0, columnspan=3, pady=10)

        style = ttk.Style()
        style.configure("Category.TButton", font=("Helvetica", 14, "bold"), foreground="#8A360F", background="#CDAA7D")
        style.configure("Question.TButton", font=("Helvetica", 14, "bold"), foreground="#1E90FF", background="#87CEFA")
        style.configure("Difficulty.TButton", font=("Helvetica", 14, "bold"), foreground="#006400", background="#90EE90")
        style.configure("Play.TButton", font=("Helvetica", 14, "bold"), foreground="#006400", background="#90EE90")

    def on_category_selected(self, callback, category, category_id):
        # Saves the selected category and category ID when a category button is clicked.
        # Also calls check_all_choices_selected() to enable/disable the Play button if all choices are made.
        self.selected_category = category
        self.selected_category_id = category_id
        self.check_all_choices_selected(callback)

    def on_num_questions_selected(self, callback, num_questions):
        # Saves the selected number of questions when a number of questions button is clicked.
       
        self.selected_num_questions = num_questions
        self.check_all_choices_selected(callback)

    def on_difficulty_selected(self, callback, difficulty):
        # Saves the selected difficulty level when a difficulty button is clicked.
        
        self.selected_difficulty = difficulty
        self.check_all_choices_selected(callback)

    def check_all_choices_selected(self, callback):
        # Checks if all trivia options (category, number of questions, difficulty) are selected
        # Enables the Play button if all are selected, disables otherwise
        if self.selected_category and self.selected_num_questions and self.selected_difficulty:
            self.play_button["state"] = tk.NORMAL
        else:
            self.play_button["state"] = tk.DISABLED


# Function to start trivia app
    # start_trivia_app launches the trivia game GUI after validating that the user has selected a category, number of questions, and difficulty level. 
    # It creates a new Tk root window and TriviaApp instance to run the game.
    def start_trivia_app(self):
        if not (self.selected_category and self.selected_num_questions and self.selected_difficulty):
            messagebox.showinfo("Selection Error", "Please select one option from each category.")
            return

        trivia_root = tk.Tk()
        trivia_app = TriviaApp(trivia_root, self.selected_category, self.selected_category_id, self.selected_num_questions, self.selected_difficulty)
        trivia_root.mainloop()



class TriviaApp:


    def __init__(self, root, selected_category, category_id, num_questions, difficulty):
        # Initializes the TriviaApp GUI by creating widgets and layout
        # root: the parent Tk window
        # selected_category: the category ID for retrieving questions 
        # category_id: the category name to display
        # num_questions: number of questions to retrieve and ask
        # difficulty: difficulty level for questions
        self.root = root
        self.root.title("Trivia App")
        self.root.geometry("500x400")

        self.root.configure(bg="cornsilk")

        self.selected_category = selected_category
        self.category_id = category_id
        self.num_questions = num_questions
        self.current_question = 0
        self.score = 0

        self.question_label = ttk.Label(root, text="Question:")
        self.question_label.grid(row=0, column=0, padx=10, pady=10)

        self.question_text = tk.Text(root, height=5, width=50, wrap="word")
        self.question_text.grid(row=0, column=1, padx=10, pady=10)

        self.options_label = ttk.Label(root, text="Options:")
        self.options_label.grid(row=1, column=0, padx=10, pady=10)

        self.options_var = tk.StringVar()
        self.options_radio = []
        for i in range(4):
            radio = ttk.Radiobutton(root, text="", variable=self.options_var, value="", command=self.reveal_result)
            self.options_radio.append(radio)
            radio.grid(row=i + 1, column=1, padx=10, pady=5, sticky="w")

        self.reveal_result_label = ttk.Label(root, text="")
        self.reveal_result_label.grid(row=5, column=0, columnspan=2, pady=10)


        self.next_button = ttk.Button(root, text="Next", command=self.next_question, state=tk.DISABLED)
        self.next_button.grid(row=6, column=1, pady=10)



        self.timer_label = ttk.Label(root, text="Time left: 10 seconds")
        self.timer_label.grid(row=7, column=0, columnspan=2, pady=10)

        self.last_request_time = 0
        self.timer = None

        # Call get_question initially to display the first question
        self.get_question()

    def get_question(self):
        # Retrieves a new trivia question from the API and displays it along with answer options.
        # Handles API errors and cases where no questions are available. Also starts a timer
        # for the user to answer once the question is displayed.
        # Retrieves a new trivia question from the API and displays it along with answer options.
        # Handles API errors and cases where no questions are available. Also starts a timer 
        # for the user to answer once the question is displayed.
        if self.current_question >= int(self.num_questions):
            self.end_game()
            return

        api_url = f"https://opentdb.com/api.php?amount=1&type=multiple&category={self.category_id}"

        try:
            current_time = time.time()
            if current_time - self.last_request_time < 10:
                time.sleep(10 - (current_time - self.last_request_time))
            # Sending the API request
            response = requests.get(api_url)
            response.raise_for_status()

            # Processing the API response
            data = response.json()

            if "results" in data and data["results"]:
                question = data["results"][0]["question"]
                incorrect_answers = data["results"][0]["incorrect_answers"]
                correct_answer = data["results"][0]["correct_answer"]

                options = incorrect_answers + [correct_answer]
                random.shuffle(options)

                self.display_question(question)
                self.display_options(options)
                self.correct_answer = correct_answer
                self.reveal_result_label.config(text="")
                self.next_button["state"] = tk.DISABLED
                self.last_request_time = time.time()

                # Starts the timer for 10 seconds
                self.start_timer(10)
            else:
                self.display_question("No questions available for this category.")
                self.display_options([])
                self.correct_answer = ""
                self.next_button["state"] = tk.NORMAL

        except requests.RequestException as e:
            error_message = f"Error retrieving question: {str(e)}"
            print(error_message)
            self.display_question(error_message)
            self.display_options([])
            self.correct_answer = ""
            self.next_button["state"] = tk.NORMAL

    def display_question(self, question):
        # Displays the given question text in the question label widget.
        # Clears any existing text in the widget before inserting the new question.
        self.question_text.delete(1.0, tk.END)
        self.question_text.insert(tk.END, question)

    def display_options(self, options):
        # Displays the answer options for the current question by configuring the 
        # radio button widgets with the provided options list. Options are displayed
        # sequentially in the radio buttons up to a max of 4. Any extra options are 
        # ignored. Clears any previously configured options.
        for i in range(4):
            if i < len(options):
                self.options_radio[i].config(text=options[i], value=options[i])
            else:
                self.options_radio[i].config(text="", value="")
                self.options_var.set("")

    def reveal_result(self):
        user_answer = self.options_var.get()

        if user_answer == self.correct_answer:
            result_text = f"Correct! The answer is: {self.correct_answer}"
            self.reveal_result_label.config(foreground="blue")  # Sets text color to blue for correct message
            self.score += 1  # Increases the score for correct answers
        else:
            result_text = f"Incorrect! The correct answer is: {self.correct_answer}"
            self.reveal_result_label.config(foreground="red")  # Sets text color to red for incorrect message
        self.reveal_result_label.config(text=result_text)
        self.next_button["state"] = tk.NORMAL

        # Stop the timer when the user selects an answer
        self.stop_timer()
        
    def next_question(self):
        self.current_question += 1
        self.get_question()

    def start_timer(self, seconds):
        # Updates the timer label to show the remaining time and schedules a callback 
        # to decrement the timer after 1 second. Stores the after callback id to 
        # allow cancelling the timer when needed.
        self.timer_label["text"] = f"Time left: {seconds} seconds"
        self.timer = self.root.after(1000, lambda: self.update_timer(seconds - 1))

    def update_timer(self, seconds):
        if seconds > 0:
            self.timer_label["text"] = f"Time left: {seconds} seconds"
            self.timer = self.root.after(1000, lambda: self.update_timer(seconds - 1))
        else:
            self.timer_label["text"] = "Time's up!"
            self.next_question()

    def stop_timer(self):
        if self.timer:
            self.root.after_cancel(self.timer)
            self.timer = None


    def end_game(self):
        messagebox.showinfo("Game Over", f"Your final score is: {self.score}")
        # reset the game or close the application after showing the message box
        self.root.destroy()
    


# Function to start category selection
def start_category_selection():
    root = tk.Tk()
    category_page = CategorySelectionPage(root, lambda cat, cat_id, num_questions, difficulty: start_trivia_app(cat, cat_id, num_questions, difficulty))
    root.mainloop()

# Function to start trivia app
def start_trivia_app(selected_category, category_id, num_questions, difficulty):
    trivia_root = tk.Tk()
    trivia_app = TriviaApp(trivia_root, selected_category, category_id, num_questions, difficulty)
    trivia_root.mainloop()


# Define the on_start_click function
def on_start_click():
    # Destroys the WelcomePage
    welcome_root.destroy()
    # Starts the CategorySelectionPage
    start_category_selection()

# Main section
if __name__ == "__main__":
    # Creates the root for the WelcomePage
    welcome_root = tk.Tk()
    # Creates the WelcomePage instance with the on_start_click function
    welcome_page = WelcomePage(welcome_root, on_start_click)
    # Runs the main loop for the WelcomePage
    welcome_root.mainloop()
