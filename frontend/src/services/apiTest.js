import api from "./api";

export async function testBackend() {
  try {
    const response = await api.get("/");
    console.log("Backend response:", response.data);
    return response.data;
  } catch (error) {
    console.error("Backend connection failed:", error);
    throw error;
  }
}