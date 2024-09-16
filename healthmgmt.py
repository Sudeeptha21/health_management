#!/usr/bin/env python
# coding: utf-8

# In[126]:


# health management system
import datetime
import os



# In[128]:


print("HEALTH MANAGEMENT SYSTEM: ")

def list_and_choose_files(directory):
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

    workout_files = [f for f in files if '_Workout' in f]
    diet_files = [f for f in files if '_Diet' in f]

    if not workout_files:
        print("No workout files found.")
        return None, None

    print("Available workout files:")
    for i, file in enumerate(workout_files):
        file = file.replace("_", " ").replace('Workout.txt', '')
        print(f"{i + 1}: {file}")

    try:
        workout_choice = int(input("Enter the number of the workout to select it: "))
        if 1 <= workout_choice <= len(workout_files):
            selected_workout = workout_files[workout_choice - 1]
            #Find the corresponding diet file
            base_name = selected_workout.replace('_Workout.txt', '')
            diet_file = f"{base_name}_Diet.txt"
            diet_path = os.path.join(directory, diet_file)
            if diet_file not in diet_files:
                print(f"Corresponding diet file '{diet_file}' not found.")
                return None, None
            workout_path = os.path.join(directory, selected_workout)
            return workout_path, diet_path
        else:
            print("Invalid choice.")
            return None, None
    except ValueError:
        print("Invalid input. Please enter a number.")
        return None, None


# In[ ]:




# In[129]:


#LOGIN FUCNTIONS
def check_user_exists(username):
    #Path to the Users directory
    script_dir = os.getcwd() 
    script_dir = os.path.join(script_dir, "Users")

    user_path = os.path.join(script_dir , username)
    if os.path.isdir(user_path):
        return True
    else:
        return False

def create_user():
    while True:
        username = input("Enter your new username with a  minimum of 3 characters. Press q to go back: ")
        print()
        while True:
            if username == "q":
                return False;
            if(len(username)<3):
                username = input("Your username needs a minimum of three characters, please try again or enter q to go back: ")
                print()
            else:
                break;
        if username == "q":
            return True;
        #Directory of the current script
        script_dir = os.getcwd() 
        script_dir = os.path.join(script_dir, "Users")
        user_path = os.path.join(script_dir, username)

        if not os.path.isdir(user_path):
            try:
                os.makedirs(user_path)
                print("User Created with username: "+username)
                return username;
            except Exception as e:
                print(f"Error creating user '{username}': {e}")
                return False;
        else:
            print("This username already exists, pick another.")

            
def save_settings(username, workout_path, diet_path):
    """Save the selected workout and diet file paths in the settings file."""
    script_dir = os.getcwd()
    users_folder = os.path.join(script_dir, "Users")
    user_folder = os.path.join(users_folder, username)
    settings_file = os.path.join(user_folder, "settings.txt")

    with open(settings_file, 'w') as f:
        if workout_path:
            f.write(f"workout_path={workout_path}\n")
        if diet_path:
            f.write(f"diet_path={diet_path}\n")

    print(f"Settings saved for user '{username}'.")
    
def setup_user(username):
    directory = os.path.join(os.getcwd(), "Exercises_and_Diets")

    print("Select a workout")
    workout_path, diet_path = list_and_choose_files(directory)

    if workout_path and diet_path:
        save_settings(username, workout_path, diet_path)
    else:
        print("Could not save settings due to invalid file choices.")
            


# In[134]:


def fetch_user_data(username):
    script_dir = os.getcwd()
    users_folder = os.path.join(script_dir, "Users")
    user_folder = os.path.join(users_folder, username)
    settings_file = os.path.join(user_folder, "settings.txt")

    if not os.path.isfile(settings_file):
        print(f"No workout found for user '{username}'.")
        setup_user(username)

    workout_path = None
    diet_path = None

    with open(settings_file, 'r') as f:
        for line in f:
            if line.startswith("workout_path="):
                workout_path = line.strip().split('=', 1)[1]
            elif line.startswith("diet_path="):
                diet_path = line.strip().split('=', 1)[1]

    if not workout_path or not diet_path:
        print("Choose a workout to save")
        setup_user(username)
        with open(settings_file, 'r') as f:
            for line in f:
                if line.startswith("workout_path="):
                    workout_path = line.strip().split('=', 1)[1]
                elif line.startswith("diet_path="):
                    diet_path = line.strip().split('=', 1)[1]

    #Prompt the user to choose which file to display
    while True:
        control = int(input("Enter 1 to view workout or 2 to view diet or 0 to go back: "))
        print()
        if control==0:
            break;
        if control == 1:
            if os.path.isfile(workout_path):
                with open(workout_path, 'r') as op:
                    for item in op:
                        print(item,end="")
            else:
                print("Workout file does not exist.")
            print()
        elif control == 2:
            if os.path.isfile(diet_path):
                with open(diet_path, 'r') as op:
                    for item in op:
                        print(item,end="")
            else:
                print("Diet file does not exist.")
            print()
        else:
            print("Invalid selection. Please enter 1 or 2.")
        

# In[131]:


def start_app():
    while True:
        control = input("Enter 0 to quit, 1 to register a user or 2 to continue as a user")
        print()
        try:
            control = int(control)
        except Exception:
            print("Please choose a valid option")
            continue;
        if control not in  [0,1,2]:
            print("Please choose a valid option")
        elif control == 0:
            print("Quitting.....Done")
            break;
        elif control==1:
            user_created = create_user()
            if user_created :
                do_while_logged_in(user_created)
                break;                
                
        else:
            username = login()
            if(username):
                do_while_logged_in(username)
                break;
                

def do_while_logged_in(username):
    while True:
        
        fetch_user_data(username)
        new_workout = int(input("Press 0 to exit or 1 to choose a new workout: "))  
        print()
        if new_workout==1:
            setup_user(username)
        else:
            break;

def login():
    while True:        
        username = input("Enter your username or q to go back:")
        if username == "q":
            return False
        if check_user_exists(username):
            print("Logged in as "+username)
            return username;
        else:
            print("Could not find User please try again.")
        
    

# In[132]:


start_app()

# In[ ]:



