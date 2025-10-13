import { FormEvent, useState } from "react";
import axios from "axios";

interface UserFormState {
  email: string;
}

export default function App() {
  const [form, setForm] = useState<UserFormState>({ email: "" });
  const [userId, setUserId] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const submit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    try {
      const response = await axios.post("/api/users", form);
      setUserId(response.data.id);
      setError(null);
    } catch (err) {
      setError((err as Error).message);
    }
  };

  return (
    <div style={{ fontFamily: "system-ui", padding: "2rem", maxWidth: "420px" }}>
      <h1>SLSA Demo Store</h1>
      <form onSubmit={submit}>
        <label htmlFor="email">Email</label>
        <input
          id="email"
          type="email"
          value={form.email}
          onChange={(event) => setForm({ email: event.target.value })}
          style={{ display: "block", margin: "0.5rem 0", width: "100%" }}
          required
        />
        <button type="submit">Create user</button>
      </form>
      {userId && <p>Created user with id: {userId}</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
}
