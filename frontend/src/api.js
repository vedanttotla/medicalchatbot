import axios from "axios";

const BASE_URL = "http://127.0.0.1:8000"; // or "http://localhost:8000"

const axiosInstance = axios.create({
  baseURL: BASE_URL,
});

export default axiosInstance;

export const searchQuery = async (query) => {
  const res = await axiosInstance.post("/search-query", { query });
  return res.data;
};
