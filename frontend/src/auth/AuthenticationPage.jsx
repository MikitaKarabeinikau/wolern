 import "react"
 import { SignIn, SignUp, SignedIn, SignedOut } from "@clerk/clerk-react"

 export function AuthenticationPage() {
    return <div className="auth-container">
        <SignedIn>
            <div className="redicrect-message">
                <p>You are signed in!</p>
            </div>
        </SignedIn>
        <SignedOut>
            <div>You are signed out!</div>
            <SignIn path="/sign-in" routing="path" signUpUrl="/sign-up" />
            <SignUp path="/sign-up" routing="path" signInUrl="/sign-in" />
        </SignedOut>

    </div>
}