# Austin Animal Center - Dashboard<br>

This project utilizes a Model-View-Controller (MVC) software design pattern, with a Dash dashboard (View), a MongoDB database (Model), and callback functions (Controller). The Dashboard for Grazioso Salvare is designed to interact with the Austin Animal Center (AAC) ‘animals’ collection, which holds data for cats and dogs that the AAC currently houses. The dashboard integrates with the custom mongo_crud.py module’s MongoCrud class to abstract away the tedious nature of connecting to a MongoDB database and executing basic CREATE, READ, UPDATE, and DELETE (CRUD) operations. The user can create new documents to be inserted into the ‘animals’ collection of the’ AAC’ database,  view (read) documents in the database by using custom query filters, update documents, and delete documents based on matching queries. More on functionality later.

![pic](images/Picture1.png)
![pic](images/Picture2.png)
![pic](images/Picture3.png)
![pic](images/Picture4.png)
![pic](images/Picture5.png)
![pic](images/Picture6.png)
![pic](images/Picture7.png)
![pic](images/Picture8.png)

### To run this web app:
* Download and open the .IPYNB file in VSCode
* Click "Run" button to the left of the cell block
* Select "Install/enable suggested extensions: Python + Jupyter"
* Click "Run" button again
* Select "Jupyter Kernel..."
* Select the Python environment to use
* Install any missing modules using pip or another installation method
* Select "Run" once again if needed
* Navigate in your browser to [http://127.0.0.1/15185/](http://127.0.0.1/15185/)
