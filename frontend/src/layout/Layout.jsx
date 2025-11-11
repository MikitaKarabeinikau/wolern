import { SignedIn, SignedOut } from "@clerk/clerk-react";
import { Outlet, Navigate } from "react-router-dom";
import Header from "./Header";
import "../layout/layout.css";

export function Layout() {
  return (
    <div className="app-layout">
      <Header />

      <main className="app-main">
        <SignedOut>
          <Navigate to="/sign-in" replace />
        </SignedOut>
        <SignedIn>
          <Outlet />
        </SignedIn>
      </main>
    </div>
  );
}
