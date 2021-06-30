<h1> General info </h1>
Web application created with Python and Django to manage a shop. <br>
You can login as:<br>
Owner/Seller -> Username: admin Password: 12345 <br>
Local Address: 127.0.0.1:8000/admin/ <br>
<h4>Seller:<h4> <br>
<li>create new order
<li>search for orders
<li>Add Stock
<li> increase / reduce quantity of products
 <h4> Technologies </h4>
  <p> Project create with</p>
  <li> Python 3.7
  <li> Django 2.2
    <li> Bootstrap 4
      <h2>Setup </h2>
      <p> To run this project on Windows:<br>
        <li>pip install virtualvenv
          <li>py -m venv myvenv
            <li>myvenv\scripts\activate
              <li>pip install -r requirements.txt
                <li>py manage.py runserver
        <p>On Linux/Ubuntu:
          <li>sudo apt install python-pip
            <li>sudo apt install virtualenv
              <li>virtualenv myvenv
                <li>source myvenv/bin/activate
                  <li>pip install -r requirements.txt
                    <li>python manage.py runserver
                      <h1>User Manual</h1>
   <p> Add Product or Stock
     <li> Go to http://127.0.0.1:8000/admin/ (local) Login with login information. Click Categories for add product category.<br>
       Click products for update or add new product and stock.
       <P> Sell Product </p>
       <li> Go to http://127.0.0.1:8000/ (local). Enter product code into the search bar or click on product which product you want sell.<br>
         After clicking the on product, product will save in cart. Select all the product that customer want to buy. Then click on cart incon, a page will appear with order details check it and press checkout button. Fill the customer information and save it. On the left side seller see order summary then he/she confirm make order. A pdf page generate with customer and order details.
       
