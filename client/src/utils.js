// Utility function to build the full API URL
export const getApiUrl = (endpoint) =>
  `http://${config.api_url}:${config.api_port}${endpoint}`;


// Utility function to fetch data via API
export async function fetchData(endpoint, method = 'GET', queryParams = {}, payload = null) {
  try {
    // Construct the base URL using the URL object
    const baseUrl = new URL(getApiUrl(endpoint));

    // If the method is GET or DELETE, append the query parameters to the URL
    if (method === 'GET' || method === 'DELETE') {
      const params = new URLSearchParams(queryParams);
      baseUrl.search = params.toString();
    }

    // Prepare the fetch options
    const fetchOptions = {
      method,
      headers: {
        'Content-Type': 'application/json',
      },
    };

    // If the method is not GET and a payload is provided, include it in the request body
    if ((method === 'POST' || method === 'PUT' || method === 'DELETE') && payload) {
      fetchOptions.body = JSON.stringify(payload);
    }

    // Fetch data using the constructed URL and fetch options
    const response = await fetch(baseUrl.toString(), fetchOptions);

    return response
    
  } catch (error) {
    console.error('Error fetching data:', error);
    // Rethrow the error to be handled by the calling function
    throw error;
  }
}


// API Dictionary
export const config = {
  api_url: "localhost",
  api_port: 8000,
  endpoints: {
    login: { url: "/login", method: "POST" },
    signup: { url: "/signup", method: "POST" },
    getUser: { url: "/getUser", method: "GET" },
    insertUser: { url: "/insertUser", method: "POST" },
    deleteUser: { url: "/deleteUser/{username}", method: "DELETE" },
    updateUser: { url: "/updateUser", method: "PUT" },
    getUserOrders: { url: "/getUserOrders", method: "GET" },
    getOrderInfo: { url: "/getOrderInfo", method: "GET" },
    insertOrder: { url: "/insertOrder", method: "POST" },
    deleteOrder: { url: "/deleteOrder/{order_id}", method: "DELETE" },
    updateOrder: { url: "/updateOrder", method: "PUT" },
    getUniqueProductsCount: {
      url: "/getUniqueProductsCount",
      method: "GET",
    },
    getProducts: {
      url: "/getProducts",
      method: "GET",
    },
    getAllProducts: { url: "/getAllProducts", method: "GET" },
    getByID: { url: "/getByID/{product_id}", method: "GET" },
    getByCategory: { url: "/getByCategory/{category}", method: "GET" },
    getBySearch: { url: "/getBySearch/{search_string}", method: "GET" },
    sortingBy: { url: "/sortingBy/{criteria}", method: "GET" },
    getFilter: { url: "/getFilter", method: "GET" },
    insertProduct: { url: "/insertProduct", method: "POST" },
    deleteProduct: { url: "/deleteProduct/{product_id}", method: "DELETE" },
    updateProduct: { url: "/updateProduct", method: "PUT" },
  },
};
