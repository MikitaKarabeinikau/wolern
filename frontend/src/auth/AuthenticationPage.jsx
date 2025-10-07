 import "react"
 import { RedirectToSignIn, SignIn, SignUp, SignedIn, SignedOut } from "@clerk/clerk-react"


export function AuthenticationPage() {


    return <div className="auth-container">
        <SignedOut> 
            <SignIn routing="path"  path="/sign-in"/>
            <SignUp routing="path"  path="/sign-up"/>
        </SignedOut>
        <SignedIn>
            <div className="redicrect-message">
                <p>You are signed in!</p>
            </div>
        </SignedIn>
        

    </div>
}