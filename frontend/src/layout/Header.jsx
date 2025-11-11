import { SignedIn, UserButton } from "@clerk/clerk-react";
import NavLinks from "./NavLinks";
import "../layout/layout.css";

export default function Header() {
  return (
    <header className="app-header">
      <div className="header-content">
        <h1>Wolern</h1>
        <SignedIn>
          <NavLinks />
          <UserButton />
        </SignedIn>
      </div>
    </header>
  );
}
