from tkinter import *
from tkinter import ttk, messagebox
import random, string
import time

STRING_TARGET_LIMIT = 15

random_mutations = 5
random_addition = 5
random_deletion = 5

def check_empty_string(target_string_entry):
    if not target_string_entry.get():
        messagebox.showwarning("Warning", "The Target String Must Contain Something")
        return 1

def start_simulation(target_string_entry, show_generations_text, generations_number_label, main_window):
    global random_mutations, random_addition, random_deletion
    check = check_empty_string(target_string_entry)
    if check==1:
        return
    
    target_string_entry.config(state=DISABLED)
    random_string = random.choice(string.printable) #assign to "random_string" one random ascii char
    counter=1

    while random_string != target_string_entry.get():
        time.sleep(0.1)
        show_generations_text.insert(float(counter), f"{counter} Generation: {random_string}\n")
        show_generations_text.see(END)
        generations_number_label.config(text=str(counter))

        if len(random_string)>1:
            if random.random() < random_mutations/100:
                random_char = random.choice(string.printable)
                random_index = random.randint(0, len(random_string)-1)
                random_string = random_string[:random_index] + random_char + random_string[random_index+1:]
    
        if len(random_string)>1:
            if random.random() < random_deletion/100:
                random_index = random.randint(0, len(random_string)-1)
                random_string = random_string[:random_index] + random_string[random_index+1:]  

        if len(random_string)<len(target_string_entry.get()):
            if random.random() < random_addition/100:
                random_char = random.choice(string.printable)
                random_string += random_char
        counter+=1
        main_window.update_idletasks()   
    
    target_string_entry.config(state=NORMAL)


def delete_all_history(show_generations_text, target_string_entry):
    show_generations_text.delete(1.0, END)
    target_string_entry.delete(0, END)


def check_string_limit(event, target_string_entry):
    if len(target_string_entry.get()) >= STRING_TARGET_LIMIT:
        return "break"


def block_typing(event):
        return "break"


def modify_mutations(select, percentage, random_m_value_label, random_a_value_label, random_d_value_label):
    global random_mutations, random_addition, random_deletion
    if select==1:
        random_mutations = percentage
        random_m_value_label.config(text=f"{random_mutations}%")
    elif select==2:
        random_addition = percentage
        random_a_value_label.config(text=f"{random_addition}%")
    else:
        random_deletion = percentage
        random_d_value_label.config(text=f"{random_deletion}%")


def main():
    global random_mutations, random_addition, random_deletion

    main_window = Tk()
    main_window.config(height=500, width=1000)
    main_window.title("Artificial Evolution")

    menu_bar = Menu(main_window)
    main_window.config(menu=menu_bar)

    title_label = Label(main_window, text="ARTIFICIAL EVOLUTION SIMULATION", font=("Arial", 25, "bold"), bg="#8a3f38", relief=RAISED, bd=3)
    title_label.grid(row=1, column=1, columnspan=3, pady=10, padx=10)

    text_frame = Frame(main_window)
    text_frame.grid(row=2, column=1, rowspan=7, pady=10, padx=10)

    buttons_frame = Frame(main_window)
    buttons_frame.grid(row=7, column=2, padx=5)

    show_generations_text = Text(text_frame, bg="#c1c2c0", width=50, height=25, wrap="word")
    show_generations_text.pack(side=LEFT, fill=BOTH, expand=True)
    
    scroll_bar = Scrollbar(text_frame, orient="vertical", command=show_generations_text.yview)
    scroll_bar.pack(side=RIGHT, fill=Y)

    show_generations_text.config(yscrollcommand=scroll_bar.set)
    show_generations_text.bind("<Key>", block_typing)

    target_string_label = Label(main_window, text="Target String:", width=35, font=("Arial", 25, "bold"), bg="#95b366")
    target_string_label.grid(row=2, column=2, padx=10)

    target_string_entry = Entry(main_window, width=STRING_TARGET_LIMIT, font=("Arial", 25, "bold"))
    target_string_entry.grid(row=2, column=3, padx=5)
    
    target_string_entry.bind("<Key>", lambda event: check_string_limit(event, target_string_entry) if event.keysym != "BackSpace" else None)

    generations_label = Label(main_window, text="Generations:", width=35, font=("Arial", 25, "bold"), bg="#95b366")
    generations_label.grid(row=3, column=2, padx=10)

    generations_number_label = Label(main_window, text="", font=("Arial", 25, "bold"))
    generations_number_label.grid(row=3, column=3, padx=5)

    random_m_label = Label(main_window, text="Percentage of random mutations:", width=35, font=("Arial", 25, "bold"), bg="#ae6fc7")
    random_m_label.grid(row=4, column=2, padx=5)
    random_m_value_label = Label(main_window, text=f"{random_mutations}%", font=("Arial", 25, "bold"))
    random_m_value_label.grid(row=4, column=3)

    random_a_label = Label(main_window, text="Percentage of random character addition:", width=35, font=("Arial", 25, "bold"), bg="#ae6fc7")
    random_a_label.grid(row=5, column=2, padx=5)
    random_a_value_label = Label(main_window, text=f"{random_addition}%", font=("Arial", 25, "bold"))
    random_a_value_label.grid(row=5, column=3)

    random_d_label = Label(main_window, text="Percentage of character deletion:", width=35, font=("Arial", 25, "bold"), bg="#ae6fc7")
    random_d_label.grid(row=6, column=2, padx=5)
    random_d_value_label = Label(main_window, text=f"{random_deletion}%", font=("Arial", 25, "bold"))
    random_d_value_label.grid(row=6, column=3)

    mutation_percentages = [("1%",1), ("5%",5), ("10%",10)]

    random_a_menu = Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Modify Random Mutations", menu=random_a_menu)
    for (percentage_string, percentage_number) in mutation_percentages:
        random_a_menu.add_command(label=percentage_string, command=lambda percentage_number=percentage_number:modify_mutations(1, percentage_number, random_m_value_label, random_a_value_label, random_d_value_label))
    
    random_d_menu = Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Modify Addition Mutations", menu=random_d_menu)
    for (percentage_string, percentage_number) in mutation_percentages:
        random_d_menu.add_command(label=percentage_string, command=lambda percentage_number=percentage_number:modify_mutations(2, percentage_number, random_m_value_label, random_a_value_label, random_d_value_label))

    random_m_menu = Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Modify Deletion Mutations", menu=random_m_menu)
    for (percentage_string, percentage_number) in mutation_percentages:
        random_m_menu.add_command(label=percentage_string, command=lambda percentage_number=percentage_number:modify_mutations(3, percentage_number, random_m_value_label, random_a_value_label, random_d_value_label))

    delete_button = Button(buttons_frame, text="Delete History", font=("Arial", 20, "bold"), bg="#bf7a75", activebackground="#8a524e")
    delete_button.config(command=lambda:delete_all_history(show_generations_text, target_string_entry))
    delete_button.pack(side=LEFT, padx=10)

    start_button = Button(buttons_frame, text="Start Simulation", font=("Arial", 20, "bold"), bg="#bf7a75", activebackground="#8a524e")
    start_button.config(command=lambda: start_simulation(target_string_entry, show_generations_text, generations_number_label, main_window))
    start_button.pack(side=LEFT, padx=10)

    main_window.mainloop()

main()