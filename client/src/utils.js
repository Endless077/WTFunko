// Function to get API URL via given endpoint
export const getApiUrl = (endpoint) =>
  `http://${config.api_url}:${config.api_port}${endpoint}`;


// Function to replace URL Params (if exists)
export function replaceUrlParams(url, params) {
  Object.keys(params).forEach((key) => {
    url = url.replace(`{${key}}`, encodeURIComponent(params[key]));
  });
  return url;
}


// General base fetch data function
export async function fetchData(
  endpoint = "/",
  headers = { "Content-Type": "application/json" },
  method = "GET",
  queryParams = {},
  pathParams = {},
  payload = null
) {
  try {
    // Replace placeholders in the endpoint with actual path parameters
    let replacedEndpoint = replaceUrlParams(endpoint, pathParams);

    // Construct the base URL using the URL object
    const baseUrl = new URL(getApiUrl(replacedEndpoint));

    // If the method is GET or DELETE, append the query parameters to the URL
    if (method === "GET" || method === "DELETE") {
      const params = new URLSearchParams(queryParams);
      baseUrl.search = params.toString();
    }

    // Prepare the fetch options
    const fetchOptions = {
      headers,
      method,
    };

    // If the method is not GET and a payload is provided, include it in the request body
    if (
      (method === "POST" || method === "PUT" || method === "DELETE") &&
      payload
    ) {
      fetchOptions.body = JSON.stringify(payload);
    }

    // Fetch data using the constructed URL and fetch options
    const response = await fetch(baseUrl.toString(), fetchOptions);

    return response;
  } catch (error) {
    console.error("Error fetching data:", error);
    // Rethrow the error to be handled by the calling function
    throw error;
  }
}


// Retrive Token Function
export async function retrieveToken() {
  try {
    // Create the baseUrl of the /retriveToken endpoint
    const baseUrl = new URL(getApiUrl("/retriveTorken"));

    // Create fetchOptions of the /retriveToken endpoint
    const fetchOptions = {
      headers: { "Content-Type": "application/json" },
      method: "GET",
    };

    // Fetch token using the constructed URL and fetch options
    const response = await fetch(baseUrl.toString(), fetchOptions);
    return response.json();
  } catch (error) {
    console.error("Error fetching data:", error);
    // Rethrow the error to be handled by the calling function
    throw error;
  }
}


// API Dictionary (not all entries)
export const config = {
  api_url: "localhost",
  api_port: 8000,
  endpoints: {
    login: { url: "/login", method: "POST" },
    signup: { url: "/signup", method: "POST" },
    deleteAccount: { url: "/deleteAccount/{username}", method: "DELETE" },
    updateUser: { url: "/updateUser", method: "PUT" },
    getUserOrders: { url: "/getUserOrders", method: "GET" },
    getOrderInfo: { url: "/getOrderInfo", method: "GET" },
    insertOrder: { url: "/insertOrder", method: "POST" },
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
    getByProductType: {
      url: "/getByProductType/{product_type)",
      method: "GET",
    },
    getBySearch: { url: "/getBySearch/{search_string}", method: "GET" },
    sortingBy: { url: "/sortingBy/{criteria}", method: "GET" },
    getFilter: { url: "/getFilter", method: "GET" },
  },
};
