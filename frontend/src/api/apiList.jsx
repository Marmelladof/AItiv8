import axios from "axios";
import { Buffer } from "buffer";

const baseUrl = "http://localhost:8000/";

export const postCrop = async (payload) => {
  let url = baseUrl + "crop_type";
  // let url = "https://85febffd-a07e-4718-8df8-0164313ee004.mock.pstmn.io";
  const response = await axios.post(url, payload, {
    responseType: "arraybuffer",
  });
  const buffer64 = Buffer.from(response.data, "binary").toString("base64");
  return buffer64;
};

export const postPlanning = async (payload) => {
  let url = baseUrl + "optimized_planning";
  // let url = "https://85febffd-a07e-4718-8df8-0164313ee004.mock.pstmn.io";
  const response = await axios.post(url, payload, {
    responseType: "arraybuffer",
  });
  const buffer64 = Buffer.from(response.data, "binary").toString("base64");
  return buffer64;
};

export const getSolution = async () => {
  let url = baseUrl + "solution";
  return await axios.get(url);
};
