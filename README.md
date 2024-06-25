![Logo](https://github.com/Endless077/WTFunko/blob/main/client/public/assets/WTF.png)


# WTFunko

An e-commerce selling Funko Pop! via the WTFunko platform, was developed as a university project to implement a NoSQL database.


## More Details

Why develop e-commerce with NoSql database? Here some advantages:

#### *Flexibility and Scalability*

NoSQL databases, like MongoDB, handle unstructured and semi-structured data, making it easy to store diverse information such as product details and user reviews. This flexibility allows quick adaptation to changing business needs without extensive schema modifications.

#### *High Performance and Availability*

NoSQL databases deliver high performance and ensure availability under heavy loads. They distribute data across multiple servers and provide horizontal scalability, keeping e-commerce sites responsive even during traffic spikes.

#### *Efficient Handling of Big Data*

Optimized for big data, NoSQL databases support distributed storage and parallel processing. This enables efficient handling of large datasets, essential for personalized marketing, customer segmentation, and inventory optimization.

#### *Improved User Experience*

NoSQL databases enable real-time recommendations, dynamic pricing, and personalized product suggestions by efficiently managing user data. This leads to tailored content and offers, boosting customer satisfaction and sales.

#### *Simplified Development and Maintenance*

The schema-less nature of NoSQL databases simplifies development and maintenance. Developers can add new fields without breaking existing functionality, accelerating feature deployment and reducing the risk of single points of failure.


## Installation

First, install a local or host a NoSQL MongoDB database. If hosting, update the URI, Database Name, and, if needed, user and password in the database.py file.

Next, ensure you have **Python** installed and create a **virtual environment**. Install the required packages from [`requirements.txt`](server/requirements.txt). To start the server, use **uvicorn** with the --reload option to apply changes, or simply use python3 app.py.

Finally, navigate to the client directory and install the necessary packages with npm install. To start the client, use either npm run dev or npm run.
Steps

#### Install MongoDB:
- Locally install MongoDB or set up a hosted MongoDB instance.
- Update the URI, Database Name, and credentials in database.py if needed.

#### Set up the Python environment

```bash
python3 -m venv venv

# On Windows use `venv\Scripts\activate`
source venv/bin/activate

pip install -r requirements.txt
```

#### Set up the client:

```bash
npm install
```

By following these steps, you can set up and run the project locally or in a hosted environment, ensuring both the server and client are properly configured.


## Deployment

FastAPI needs the requirements installed to be started:

#### Start the server:

```bash
uvicorn app:app --reload
# or
python3 app.py
```

React need the requireemets by NodeJS/npm to be started:

#### Start the client:
```bash
npm run  # or `npm run dev` for dev mode
```


## API Reference

You can view the API documentation using FastAPI by visiting the **/docs** endpoint of your server (i.e http://localhost:8000/docs). Once your application is running and accessible, simply navigate to your server's URL followed by **/docs**. This interactive interface provides a comprehensive list of available APIs, including details on each supported request, required parameters, allowed HTTP methods, and expected responses. It's an invaluable tool for quickly exploring and understanding the functionality offered by your APIs without the need to manually reference static documentation.

## Dataset

The dataset was sourced from **[Kaggle](https://www.kaggle.com/)** and can be accessed [here](https://www.kaggle.com/datasets/victorsoeiro/funko-pop-dataset).

This dataset was extracted using Pandas, analyzed, and cleaned by applying ETL (Extract, Transform, Load) principles. After extraction, a JSON file was created for each collection (Users, Orders, and Products). These JSON files will be used by the server to initially populate the database after establishing the connection.## Acknowledgements


## Acknowledgements

### FastAPI

FastAPI is a modern web framework for building APIs with Python 3.7+ based on standard Python type hints. It offers high performance with automatic interactive documentation (Swagger UI), WebSocket support, GraphQL integration, CORS middleware, OAuth2 authentication, and more.

[More information Here](https://github.com/tiangolo/fastapi)

### MongoDB

MongoDB is a flexible and scalable NoSQL database that stores data in JSON-like documents. It is widely used for modern web applications due to its horizontal scalability, ease of use, and speed.

[More information Here](https://www.mongodb.com/)

### React

React is a JavaScript library for building user interfaces, developed by Facebook. It is known for creating reusable components that efficiently manage application state. React uses a component-based approach to build dynamic and responsive user interfaces. 

[More information Here](https://reactjs.org/)

### Vite

Vite is a fast build tool for modern web development. It is designed to speed up the development server and hot module replacement (HMR) thanks to its ESModule support, enabling JavaScript module imports without a build step.

[More information Here](https://github.com/vitejs/vite)

### Other Various Utilities

In the realm of modern application development, there are numerous useful tools and libraries that enhance productivity and efficiency. Some of these include:

- **[Axios](https://github.com/axios/axios)**: A promise-based HTTP client for making AJAX requests.
- **[Bootstrap](https://getbootstrap.com/)**: CSS framework for building responsive and styled user interfaces.

These tools and technologies are widely adopted in the software development community to improve the quality, maintainability, and performance of modern applications.


## License

This project is licensed under the GNU General Public License v3.0. For more details, see the [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.en.html).

![Static Badge](https://img.shields.io/badge/UniSA-WTFunko-red?style=plastic)


## Authors

**Contributors:**
- [Marco Palmisciano](https://github.com/JewDaiko)
- [Luciano Bercini](https://github.com/Luciano-Bercini)

**Project Manager:**
- [Antonio Garofalo](https://github.com/Endless077)


## Support

For support, email [antonio.garofalo125@gmail.com](mailto:antonio.garofalo125@gmail.com) or contact the project contributors.

### Documentation

See the documentation project docs **[here](https://github.com/Endless077/WTFunko)**.
