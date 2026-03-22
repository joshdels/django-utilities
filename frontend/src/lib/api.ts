export const API_BASE = "http://localhost:8000/api";

export const fetchWithAuth = async (
  endpoint: string,
  token?: string,
  options: any = {},
) => {
  const headers: Record<string, string> = {
    "Context-Type": "application/json",
    ...options.headers,
  };

  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const res = await fetch(`${API_BASE}${endpoint}`, {
    ...options,
    headers,
  });

  if (!res.ok) {
    const error = await res.json().catch(() => ({}));
    throw new Error(error.detail || "API request failed");
  }

  return res.json();
};
