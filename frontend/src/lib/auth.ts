export const login = async (username: string, password: string) => {
  const res = await fetch("http://localhost:8000/api/login/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  });

  if (!res.ok) throw new Error("Login failed");

  const data = await res.json();

  localStorage.setItem("access", data.access);
  localStorage.setItem("refresh", data.refresh);

  return data;
};

export const logout = () => {
  localStorage.removeItem("access");
  localStorage.removeItem("refresh");
};
