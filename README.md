# **🍅 Pomodoro Time App**

A desktop application to help you manage your time and stay focused using the Pomodoro Technique, integrated with Google services.

## **✨ Features**

* **Classic Pomodoro Timer:** Standard 25-minute work intervals with 5-minute short breaks and 15-minute long breaks.  
* **Task Management:** Simple interface to add, track, and complete your daily tasks.  
* **Google Integration:** (Assumed Feature) Sync your tasks or sessions with Google Calendar or Google Sheets.  
* **Productivity Tracking:** Visualize your work patterns and productivity with simple charts.

## **🚀 Getting Started**

Follow these instructions to get the project up and running on your local machine.

### **Prerequisites**

* Python 3.8 or higher  
* pip (Python package installer)

### **Installation & Setup**

1. **Clone the repository:**  
   git clone \[https://github.com/Dauzm99/Pomodoro-Time-App.git\](https://github.com/Dauzm99/Pomodoro-Time-App.git)  
   cd Pomodoro-Time-App

2. **Install the required packages:**  
   pip install \-r requirements.txt

3. Set up Google API Credentials (Important\!):  
   This application requires Google API credentials to function correctly. You need to obtain a credentials.json file from your Google Cloud Console.  
   * **Step 1:** Go to the [Google Cloud Console](https://console.cloud.google.com/).  
   * **Step 2:** Create a new project or select an existing one.  
   * **Step 3:** In the navigation menu, go to **APIs & Services \-\> Enabled APIs & services** and click **\+ ENABLE APIS AND SERVICES**. Search for and enable the necessary APIs for this project (e.g., **Google Calendar API**, **Google Sheets API**).  
   * **Step 4:** Go to **APIs & Services \-\> Credentials**. Click **\+ CREATE CREDENTIALS** and select **OAuth client ID**.  
   * **Step 5:** If prompted, configure the consent screen. Select **Desktop app** as the application type.  
   * **Step 6:** After creating the OAuth client ID, click the **Download JSON** icon next to it.  
   * **Step 7:** Rename the downloaded file to credentials.json and place it in the **root directory** of this project. The application is configured to look for this file to handle authentication.

## **Usage**

To run the application, execute the main Python script:

python main.py \# or your main script file

## **🛠️ Built With**

* **Tkinter / customtkinter:** For the graphical user interface.  
* **Pandas:** For data manipulation and tracking.  
* **Matplotlib:** For generating productivity charts.  
* **Google API Python Client:** To interact with Google services.

Feel free to contribute to this project by submitting a pull request. If you encounter any issues, please open an issue on the GitHub repository.
