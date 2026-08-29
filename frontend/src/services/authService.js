import api from "./api";

const authService = {
  async login(credentials) {
    const response = await api.post("/auth/login", credentials);

    localStorage.setItem("access_token", response.data.access_token);

    return response.data;
  },

  async getMe() {
    const token = localStorage.getItem("access_token");

    const response = await api.get("/auth/me", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    return response.data;
  },
};

export default authService;