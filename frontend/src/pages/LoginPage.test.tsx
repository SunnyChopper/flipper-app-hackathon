import { fireEvent, render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { describe, expect, it, vi } from "vitest";
import { AuthContext, type AuthContextValue } from "@/auth/AuthProvider";
import { LoginPage } from "@/pages/LoginPage";

function renderLogin(value: Partial<AuthContextValue>) {
  const auth: AuthContextValue = {
    configured: true,
    loading: false,
    session: null,
    user: null,
    signIn: vi.fn().mockResolvedValue(undefined),
    signUp: vi.fn().mockResolvedValue("signed-in"),
    signOut: vi.fn().mockResolvedValue(undefined),
    ...value,
  };
  render(
    <MemoryRouter>
      <AuthContext.Provider value={auth}>
        <LoginPage />
      </AuthContext.Provider>
    </MemoryRouter>,
  );
  return auth;
}

describe("LoginPage", () => {
  it("shows a demo fallback when Supabase Auth is not configured", () => {
    renderLogin({ configured: false });
    expect(screen.getByRole("heading", { name: "Sign in" })).toBeInTheDocument();
    expect(screen.getByText(/VITE_SUPABASE_URL/)).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Continue without account" })).toBeInTheDocument();
  });

  it("renders email and password fields when Auth is configured", () => {
    renderLogin({ configured: true });
    expect(screen.getByLabelText("Email")).toBeInTheDocument();
    expect(screen.getByLabelText("Password")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Sign in" })).toBeInTheDocument();
  });

  it("submits email and password to signIn", async () => {
    const auth = renderLogin({ configured: true });

    fireEvent.change(screen.getByLabelText("Email"), { target: { value: "anoop@example.com" } });
    fireEvent.change(screen.getByLabelText("Password"), { target: { value: "hunter2" } });
    fireEvent.submit(screen.getByRole("button", { name: "Sign in" }).closest("form")!);

    expect(auth.signIn).toHaveBeenCalledWith("anoop@example.com", "hunter2");
  });
});
