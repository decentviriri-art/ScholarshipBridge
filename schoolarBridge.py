import json
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "12345"
scholarships = [
    {
        "name": "DAAD Scholarship",
        "country": "Germany",
        "field": "Data Science",
        "degree": "Masters",
    },
    {
        "name": "Chevening Scholarship",
        "country": "United Kingdom",
        "field": "Any",
        "degree": "Masters",
    },
    {
        "name": "Erasmus Mundus",
        "country": "Europe",
        "field": "Computer Science",
        "degree": "Masters",
    },
    {
        "name": "MEXT Scholarship",
        "country": "Japan",
        "field": "Engineering",
        "degree": "Masters"
    }
    
]
def admin_login():
    username = input("Enter admin username: ").strip()
    password = input("Enter admin password: ").strip()

    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        print("Login successful!")
        return True
    else:
        print("Access denied!")
        return False

def load_scholarships():
    global scholarships

    try:
        with open("scholarships.json", "r") as file:
            scholarships = json.load(file)

    except FileNotFoundError:
        save_scholarships_to_file("scholarships.json")
load_scholarships()

def menu():
  while True: 
        print("===============================================================")
        print("Welcome to the ScholarshipBridge!")
        print("===============================================================")
        print("1. View Scholarship")
        print("2. Search Scholarships by Country")  
        print("3. Search Scholarships by Field of Study") 
        print("4. Search Scholarships by Name")  
        print("5. Admin Login")
        print("6. Export Scholarship Data to JSON")
        print("7. About ScholarshipBridge") 
        print("8. Search Scholarships by Degree Level")  
        print("9. Sort Scholarships (A-Z)")  
        print("10. Exit")
        choice = input("Choose an option (1-10): ")

        if choice == "1":
            view_scholarship()

        elif choice == "2":
            search_country()

        elif choice == "3":
            search_field()

        elif choice == "4":
            search_scholarship_by_name()

        elif choice == "5":
            if admin_login():
             admin_menu()

        elif choice == "6":
            export_scholarships_to_json()

        elif choice == "7":
            about()

        elif choice == "8":
            search_degree()

        elif choice == "9":
            sort_scholarships()

        elif choice == "10":
            print("Thank you for using ScholarshipBridge!")
            break

        else:
            print("Invalid option.")

def admin_menu():
    while True:
        print("\n====================================")
        print("        ADMIN PANEL")
        print("====================================")
        print("1. Add Scholarship")
        print("2. Edit Scholarship")
        print("3. Delete Scholarship")
        print("4. Logout")

        choice = input("Choose an option (1-4): ")

        if choice == "1":
            add_scholarship()

        elif choice == "2":
            edit_scholarship()

        elif choice == "3":
            delete_scholarship()

        elif choice == "4":
            print("Logged out successfully.")
            break

        else:
            print("Invalid option.")
    
def view_scholarship():
        for scholarship in scholarships:
            display_scholarship(scholarship)    
            print("--------------------------------------------------------")
def add_scholarship():
    name = input("Enter the scholarship name: ").strip()

    if name == "":
        print("Scholarship name cannot be empty.")
        return

    # Check duplicates first
    for scholarship in scholarships:
        if scholarship["name"].lower() == name.lower():
            print("Scholarship already exists.")
            return

    country = input("Enter the country: ").strip()
    if country == "":
        print("Country cannot be empty.")
        return

    field = input("Enter the field of study: ").strip()
    if field == "":
        print("Field cannot be empty.")
        return

    degree = input("Enter the degree level: ").strip()
    if degree == "":
        print("Degree cannot be empty.")
        return

    new_scholarship = {
        "name": name,
        "country": country,
        "field": field,
        "degree": degree
    }

    scholarships.append(new_scholarship)

    save_scholarships_to_file("scholarships.json")

    print("Scholarship added successfully!")
    display_scholarship(new_scholarship)
def search_scholarship_by_name():
        name = input("Enter the scholarship name to search: ").strip()
        if name == "":
            print("Scholarship name cannot be empty. Please enter a valid name.")
            return
        found=False
        for scholarship in scholarships:
            if name.lower() in scholarship['name'].lower():
                display_scholarship(scholarship)
                found=True
        if not found:
            print("No scholarships found with the specified name.")
def search_country():
            country = input("Enter the country to search for scholarships: ").strip()
            if country == "":
                print("Country cannot be empty. Please enter a valid country.")
                return
            found=False 
            for scholarship in scholarships:
                if scholarship['country'].lower() == country.lower():
                    display_scholarship(scholarship)
                    found=True
            if not found:
                print("No scholarships found for the specified country.")

def sort_scholarships():
    scholarships.sort(key=lambda x: x['name'].lower())
    save_scholarships_to_file("scholarships.json")
    print("Scholarships sorted alphabetically by name.")
    view_scholarship()

def export_scholarships_to_json():
        filename = input("Enter the filename to export scholarships (e.g., scholarships.json): ").strip()
        if filename == "":
            print("Filename cannot be empty. Please enter a valid filename.")
            return
        save_scholarships_to_file(filename)
        print(f"Scholarships exported to {filename} successfully.")

def search_degree():
        degree = input("Enter the degree level to search for scholarships: ").strip()
        if degree == "":
            print("Degree level cannot be empty. Please enter a valid degree level.")
            return
        found=False
        for scholarship in scholarships:
            if scholarship['degree'].lower() == degree.lower():
                display_scholarship(scholarship)
                found=True
        if not found:
            print("No scholarships found for the specified degree level.")

def search_field():
        field = input("Enter the field of study to search for scholarships: ").strip()
        if field == "":
            print("Field of study cannot be empty. Please enter a valid field.")
            return  
        found=False
        for scholarship in scholarships:
            if scholarship['field'].lower() == field.lower():
                display_scholarship(scholarship)
                found=True
        if not found:
            print("No scholarships found for the specified field of study.")

def display_scholarship(scholarship):
        print(f"Name: {scholarship['name']}")
        print(f"Country: {scholarship['country']}")
        print(f"Field: {scholarship['field']}")
        print(f"Degree: {scholarship['degree']}")

def delete_scholarship():
        name = input("Enter the scholarship name to delete: ").strip()
        if name == "":
            print("Scholarship name cannot be empty. Please enter a valid name.")
            return
        for scholarship in scholarships:
            if scholarship['name'].lower() == name.lower():
                scholarships.remove(scholarship)
                save_scholarships_to_file("scholarships.json")
                print(f"Scholarship '{name}' deleted successfully!")
                return
        print(f"No scholarship found with the name '{name}'.")

def edit_scholarship():
        name = input("Enter the scholarship name to edit: ").strip()
        if name == "":
            print("Scholarship name cannot be empty. Please enter a valid name.")
            return
        for scholarship in scholarships:
            if scholarship['name'].lower() == name.lower():
                new_name = input("Enter the new scholarship name (leave blank to keep current): ").strip()
                new_country = input("Enter the new country (leave blank to keep current): ").strip()
                new_field = input("Enter the new field of study (leave blank to keep current): ").strip()
                new_degree = input("Enter the new degree level (leave blank to keep current): ").strip()

                if new_name:
                    scholarship['name'] = new_name
                if new_country:
                    scholarship['country'] = new_country
                if new_field:
                    scholarship['field'] = new_field
                if new_degree:
                    scholarship['degree'] = new_degree

                print(f"Scholarship '{name}' updated successfully!")
                save_scholarships_to_file("scholarships.json")
                display_scholarship(scholarship)
                return
        print(f"No scholarship found with the name '{name}'.")



def save_scholarships_to_file(filename):
        with open(filename, 'w') as file:
            json.dump(scholarships, file, indent=4)
        print(f"Scholarships saved to {filename} successfully.")

def about():
        print("--------------------------------------------------------")
        print("ScholarshipBridge is a platform that provides information about various scholarships available worldwide.")
        print("You can view scholarships, search by country or field of study, and learn more about the platform.")
        print("--------------------------------------------------------")

menu()
