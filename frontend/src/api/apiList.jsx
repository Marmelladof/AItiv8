import axios from "axios";

const baseUrl = "https://localhost:8000/";

export const postCrop = async (payload) => {
  // let url = baseUrl + "crop_type";
  let url = "https://85febffd-a07e-4718-8df8-0164313ee004.mock.pstmn.io"
  return await axios.post(url, payload);
};

export const postPlanning = async (payload) => {
  let url = baseUrl + 'optimized_planning'
  return await axios.post(url, payload)
}

export const getSolution = async () => {
  let url = baseUrl + "solution";
  return await axios.get(url);
};
