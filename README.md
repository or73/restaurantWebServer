# restaurantWebServer
Python Web Server &amp; DB Queries - CRUD

Build a web service in Python that uses a database ot implement CRUD operations.
**CRUD**: **C**reate, **R**ead, **U**pdate, and **D**elete

## Objectives      
1. Opening `http://localhost:8080/restaurants` lists all the restaurant names in the database   
2. After the name of each 'restaurant name' from database there is a link to edit and delete each restaurant   
3. There is a page to create new restaurants at `http://localhost:8080/restaurants/new` with a form for creating a new restaurant.   
4. Users can rename a restaurant by visiting `http://localhost:8080/restaurant/<restaurant name>/edit`.   
5. Clicking `delete` takes a user to a confirmation page that then sends a `POST` command to the database to `delete` the selected restaurant.   

## Files   

| File              | Description                   |
|:---               |:---                           |
| aux_funcs.py      | Auxiliary functions           |
| restaurantCRUD.py | All CRUD operations           |
| restaurantDB.py   | Connection to DB              |
| webserver.py      | Upload server & print message |

## Author   
[Oscar Reyes](https://www.linkedin.com/in/oreyesc/)   
