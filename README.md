# Vehicle Rental System

## Project Description

The Vehicle Rental System is a Python-based application that allows users to manage the rental of various types of vehicles, including cars, bikes, and trucks. Users can add customers, add vehicles, create rental reservations, return vehicles, and check vehicle availability. The system ensures that no double bookings occur and tracks rental history for customers.

## How to Run the Project

### Requirements
- Python 3.10.7 installed on your machine.
- Basic text editor or IDE (e.g., Visual Studio Code, PyCharm, or Jupyter Notebook).

### Steps to Run
1. **Clone or Download the Project:**
   - Clone the repository or download the `Rental_Company.py` file to your local machine.

2. **Open a Terminal/Command Prompt:**
   - Navigate to the directory where the `Rental_company.py` file is located.

3. **Run the Program:**
   - Execute the script using Python:
     ```bash
     python Rental_Company.py
     ```

4. **Interact with the System:**
   - Follow the prompts in the console to add customers, vehicles, make reservations, and return vehicles. The menu will guide you through available actions.

## Known Issues

1. **Limited Date Format:**
   - The date input must follow the `YYYY-MM-DD` format. If an invalid format is provided, the program will display an error message and prompt for the date again.

2. **Basic Input Validation:**
   - The system currently has minimal input validation. For example, entering a non-existent vehicle ID or customer ID may lead to unexpected behavior. Additional checks may be added in future versions to improve robustness.

3. **Rental Period Edge Case:**
   - The current logic assumes a full day rental. It does not handle partial day rentals effectively. For instance, if a vehicle is rented for a day, returning it later the same day would still be considered a full day rental.

4. **Error Handling:**
   - While exceptions are raised for common issues (like vehicle availability), more comprehensive error handling and user feedback could enhance the user experience.

## Future Improvements
- **Input Validation**: Enhance input validation to handle more edge cases and provide better user feedback.
- **Graphical User Interface**: Develop a GUI to improve usability and accessibility for users who prefer not to use the command line.
- **Extended Features**: Implement features like discounts, customer loyalty tracking, or a database for persistent data storage.

## Sample Output

Here is a screenshot of the sample output after running the application:

![Sample Output](sample_output/Screenshot%202024-10-03%20172023.png)
![Sample Output](sample_output/Screenshot%202024-10-03%20172045.png)
![Sample Output](sample_output/Screenshot%202024-10-03%20172116.png)
![Sample Output](sample_output/Screenshot%202024-10-03%20172132.png)
![Sample Output](sample_output/Screenshot%202024-10-03%20172148.png)
![Sample Output](sample_output/Screenshot%202024-10-03%20172201.png)