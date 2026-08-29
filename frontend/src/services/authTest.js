import authService from "./authService";

async function testAuth() {
  try {
    const result = await authService.login({
      username: "testuser",
      password: "testpassword",
    });

    console.log("LOGIN SUCCESS:");
    console.log(result);

    const user = await authService.getMe();

    console.log("CURRENT USER:");
    console.log(user);
  } catch (error) {
    console.error("AUTH TEST FAILED:");

    if (error.response) {
      console.error(error.response.data);
    } else {
      console.error(error.message);
    }
  }
}

testAuth();