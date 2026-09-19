import { FormEvent, useState } from "react";
import { supabase } from "../lib/supabase";
import { useAuth } from "../hooks/useAuth";

export function AuthPage() {
  const { session, enabled } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState<string | null>(null);

  async function onSubmit(event: FormEvent) {
    event.preventDefault();
    if (!supabase) return;
    const { error } = await supabase.auth.signInWithPassword({ email, password });
    if (error) {
      const created = await supabase.auth.signUp({ email, password });
      setMessage(created.error?.message ?? "Check your inbox, or you are signed up.");
      return;
    }
    setMessage("Signed in.");
  }

  if (!enabled) {
    return (
      <div className="auth-card">
        <h1 className="serif">Auth is optional for the demo</h1>
        <p>Add VITE_SUPABASE_URL and VITE_SUPABASE_ANON_KEY to enable sign-in.</p>
      </div>
    );
  }

  if (session) {
    return (
      <div className="auth-card">
        <h1 className="serif">You are in</h1>
        <p>{session.user.email}</p>
        <button type="button" className="ghost" onClick={() => void supabase?.auth.signOut()}>
          Sign out
        </button>
      </div>
    );
  }

  return (
    <div className="auth-card">
      <h1 className="serif">Sign in</h1>
      <form onSubmit={(event) => void onSubmit(event)}>
        <input type="email" value={email} onChange={(event) => setEmail(event.target.value)} placeholder="Email" />
        <input
          type="password"
          value={password}
          onChange={(event) => setPassword(event.target.value)}
          placeholder="Password"
        />
        <button type="submit">Continue</button>
      </form>
      {message && <p className="banner">{message}</p>}
    </div>
  );
}
