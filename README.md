# ProteinCellTaxonomy-DjangoRESTAPI
 
Creating a RESTful web service for a team of scientists who study protein domains in the biosciences, allowing the system to regularly query in order to retrieve the data they have produced.

### Running the project
Below are the instructions to run the project and to access the API endpoints.
1. Extract the zip archive to a location of your choice.
2. There will be two folders and a file: script, bioweb, and requirements.txt.
3. Open a command prompt or terminal in the directory of the extracted files.
4. Create a Python virtual environment using:
python -m virtualenv env
5. Activate the virtual environment if it is not yet activated using:
.\env\Scripts\activate (Windows)
source env/bin/activate (Mac/Linux)
6. Install required packages using:
pip install -r requirements.txt
7. Change directory to the bioweb folder.
8. Run the project using:
python manage.py runserver
9. The API should now be running and accessible at http://127.0.0.1:8000
10. If you require access to the Django Admin site, a superuser account is available with the
following credentials:  
Username: admin  
Password: password123

More information regarding on how to Run the project, Run Tests, Code Organisation, URL Routing, Views and Serialization and Data Loading Script can be found here in the report [ProteinCellTaxonomy_Report.pdf](https://github.com/rizfebriansyah/ProteinCellTaxonomy-DjangoRESTAPI/files/9805541/ProteinCellTaxonomy_Report.pdf)
