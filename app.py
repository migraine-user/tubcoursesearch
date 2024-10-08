import tkinter as tk
from tkinter import ttk

class Course:
    def __init__(self, field, title, credit, exam):
        self.fields = [field]
        self.title = title
        self.credit = credit
        self.exam = exam

    def add_field(self, field):
        if field not in self.fields:  # Avoid duplicates
            self.fields.append(field)

# Load data from CSV file
fields = set()
courses: dict[str, Course] = {}
with open("output.csv", "r") as file:
    for line in file:
        field, title, credit, exam = line.strip().split(",")  # Use strip() to remove newline characters
        credit = int(credit)
        fields.add(field)
        if title in courses:
            courses[title].add_field(field)
        else:
            courses[title] = Course(field, title, credit, exam)

def create_app():
    root = tk.Tk()
    root.title("Course Search")

    # Main frame to hold checkboxes and results
    main_frame = tk.Frame(root)
    main_frame.pack(pady=10, fill=tk.BOTH, expand=True)

    # Frame for checkboxes
    checkbox_frame = tk.Frame(main_frame)
    checkbox_frame.pack(side=tk.LEFT, padx=10, fill=tk.Y)

    # Boolean variables for checkbuttons
    bool_dict = {field: tk.BooleanVar(value=True) for field in fields}

    # Create checkbuttons for each field
    for field in bool_dict:
        checkbox = tk.Checkbutton(checkbox_frame, text=field, variable=bool_dict[field])
        checkbox.pack(anchor="w")

    # Frame for search entry and results
    results_frame = tk.Frame(main_frame)
    results_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Create an entry field for search
    entry = tk.Entry(results_frame)
    entry.pack(pady=10, fill=tk.X)

    # Create a frame for the Treeview and scrollbar
    tree_frame = tk.Frame(results_frame)
    tree_frame.pack(pady=10, fill=tk.BOTH, expand=True)

    # Create Treeview to display results
    columns = ("Title", "Credit", "Exam")
    tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)

    # Configure headings
    tree.heading("Title", text="Title")
    tree.heading("Credit", text="Credit")
    tree.heading("Exam", text="Exam")

    # Adjust column widths
    tree.column("Title", anchor="w")
    tree.column("Credit", anchor="center")
    tree.column("Exam", anchor="center")

    # Set font and padding for rows
    style = ttk.Style()
    style.configure("Treeview", rowheight=30, font=('Arial', 12))  # Adjust row height and font

    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)  # Allow tree to expand

    # Add scrollbar
    scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def search(event=None):
        query = entry.get().lower()  # Get the search query
        for row in tree.get_children():  # Clear previous results
            tree.delete(row)

        results = []
        # Iterate through the courses
        for course_title, course in courses.items():
            # Check if the title contains the search query
            if query in course_title.lower():
                # Check if at least one field is checked
                if any(bool_dict[field].get() for field in course.fields):
                    # Insert the course details into the Treeview
                    results.append(course)
        # sort by a given column.
        if sort_by:
            a = abs(sort_by)
            sgn = True if sort_by > 0 else False
            if a == 1:
                results.sort(key=lambda x: x.title, reverse=sgn)
            elif a == 2:
                results.sort(key=lambda x: x.credit, reverse=sgn)
            else:
                results.sort(key=lambda x: x.exam, reverse=sgn)
        else:
            results.sort(key=lambda x: x.title)
        for course in results:
            tree.insert("", "end", values=(course.title, course.credit, course.exam))
    
    sort_by = None
    def on_header_click(event):
        # Check which region was clicked
        region = tree.identify_region(event.x, event.y)
        
        # Proceed only if the click is in the "heading" region
        if region == "heading":
            column_id = tree.identify_column(event.x)
            if column_id and column_id.startswith('#'):
                # print(f"Header clicked: {column_id} {type(column_id)}")
                nonlocal sort_by
                tmp = int(column_id[1:])
                if tmp == sort_by:
                    sort_by *= -1
                else:
                    sort_by = tmp
                search()
        else:
            selected_item = tree.selection()  # Get the selected item
            if selected_item:
                title = tree.item(selected_item)['values'][0]  # Get the title from the selected row
                root.clipboard_clear()  # Clear the clipboard
                root.clipboard_append(title)  # Append the title to the clipboard
                root.update()  # Keep the clipboard data available

    # Function to select all text in the entry
    def select_all(event):
        entry.select_range(0, tk.END)
        entry.icursor(tk.END)  # Move cursor to the end
        return "break"  # Prevent default handling
    tree.bind("<Button-1>", on_header_click)
    # Bind the Enter key to the search function
    entry.bind("<Return>", search)
    entry.bind("<Control-a>", select_all)

    root.mainloop()

create_app()
