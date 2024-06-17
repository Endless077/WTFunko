// Utils Config
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
    getAllProducts: { url: "/getAllProducts", method: "GET" },
    getProductsFromPage: {
      url: "/getProductsFromPage",
      method: "GET",
    },
    getUniqueProductsCount: {
      url: "/getUniqueProductsCount",
      method: "GET",
    },
    getProduct: { url: "/getProduct/{product_id}", method: "GET" },
    getByCategory: { url: "/getByCategory/{category}", method: "GET" },
    getBySearch: { url: "/getBySearch/{search_string}", method: "GET" },
    sortingBy: { url: "/sortingBy/{criteria}", method: "GET" },
    getFilter: { url: "/getFilter", method: "GET" },
    insertProduct: { url: "/insertProduct", method: "POST" },
    deleteProduct: { url: "/deleteProduct/{product_id}", method: "DELETE" },
    updateProduct: { url: "/updateProduct", method: "PUT" },
  },
};

// Utility function to construct the full URL
//  -replace {params} with replace function by string object (i.e .replace("{username}", username))
//  -use query params to send some data to backend (i.e ?username=${username}&password=${password})
export const getApiUrl = (endpoint) =>
  `http://${config.api_url}:${config.api_port}${endpoint}`;
