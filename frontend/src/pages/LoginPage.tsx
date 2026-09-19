import { FormEvent, useState } from "react";
import { Link, Navigate, useLocation, useNavigate } from "react-router-dom";
import { useAuth } from "@/auth/AuthProvider";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import { Input } from "@/components/ui/Input";

type Mode = "signin" | "signup";

export function LoginPage() {
  const { configured, loading, session, signIn, signUp } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const from = (location.state as { from?: string } | null)?.from || "/radar";

  const [mode, setMode] = useState<Mode>("signin");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [info, setInfo] = useState<string | null>(null);

  if (!loading && session) {
    return <Navigate to={from} replace />;
  }

  async function onSubmit(event: FormEvent) {
    event.preventDefault();
    setError(null);
    setInfo(null);
    setSubmitting(true);
    try {
      if (mode === "signin") {
        await signIn(email.trim(), password);
        navigate(from, { replace: true });
        return;
      }
      const result = await signUp(email.trim(), password);
      if (result === "signed-in") {
        navigate(from, { replace: true });
        return;
      }
      setInfo("Check your email to confirm your account, then sign in.");
      setMode("signin");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong.");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="grid min-h-screen place-items-center bg-nav px-4">
      <div className="w-full max-w-[400px]">
        <Link to={configured ? "/login" : "/radar"} className="mb-8 flex items-center justify-center gap-2.5 text-white">
          <span className="grid h-7 w-7 place-items-center rounded-md bg-primary">
            <span className="h-2.5 w-2.5 rotate-45 rounded-[2px] bg-white" />
          </span>
          <span className="text-lg font-bold tracking-tight">DealSniper</span>
        </Link>

        <Card className="p-6 shadow-card-hover">
          <h1 className="text-xl font-bold tracking-tight">
            {mode === "signin" ? "Sign in" : "Create account"}
          </h1>
          <p className="mt-1.5 text-sm text-muted">
            {configured
              ? "Use your email to save deals and pick up where you left off."
              : "Add Supabase Auth keys to enable sign in for this local demo."}
          </p>

          {!configured ? (
            <div className="mt-5 space-y-3">
              <p className="rounded-lg bg-warning-soft px-3 py-2 text-[13px] text-foreground">
                Set <code className="font-medium">VITE_SUPABASE_URL</code> and{" "}
                <code className="font-medium">VITE_SUPABASE_ANON_KEY</code> in <code>frontend/.env</code>.
              </p>
              <Button className="w-full" onClick={() => navigate("/radar")}>
                Continue without account
              </Button>
            </div>
          ) : (
            <form className="mt-5 space-y-3.5" onSubmit={(event) => void onSubmit(event)}>
              <Input
                label="Email"
                name="email"
                type="email"
                autoComplete="email"
                required
                value={email}
                onChange={(event) => setEmail(event.target.value)}
              />
              <Input
                label="Password"
                name="password"
                type="password"
                autoComplete={mode === "signin" ? "current-password" : "new-password"}
                required
                minLength={6}
                value={password}
                onChange={(event) => setPassword(event.target.value)}
              />
              {error ? (
                <p className="rounded-lg bg-danger-soft px-3 py-2 text-[13px] text-danger">{error}</p>
              ) : null}
              {info ? (
                <p className="rounded-lg bg-primary-soft px-3 py-2 text-[13px] text-foreground">{info}</p>
              ) : null}
              <Button type="submit" className="w-full" disabled={submitting}>
                {submitting ? "Please wait…" : mode === "signin" ? "Sign in" : "Create account"}
              </Button>
            </form>
          )}

          {configured ? (
            <p className="mt-4 text-center text-[13px] text-muted">
              {mode === "signin" ? "Need an account?" : "Already have an account?"}{" "}
              <button
                type="button"
                className="font-medium text-primary hover:text-primary-hover"
                onClick={() => {
                  setMode(mode === "signin" ? "signup" : "signin");
                  setError(null);
                  setInfo(null);
                }}
              >
                {mode === "signin" ? "Create one" : "Sign in"}
              </button>
            </p>
          ) : null}
        </Card>
      </div>
    </div>
  );
}
