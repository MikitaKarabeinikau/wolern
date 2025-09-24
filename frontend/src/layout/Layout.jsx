import "react"
import {SignedIn, SignedOut, UserButton} from "@clerk/clerk-react"
import {Outlet,Link,Navigate} from "react-router-dom"

export function Layout(){
    return <div className="app-layout">
        <header className="app-header">
            <div className="header-content">
                <h1>Wolern</h1>
                <nav>
                    <SignedIn>
                        <Link to="/">Home</Link>
                        <Link to="/quiz">Quiz</Link>
                        <Link to="/vocabularies">Vocabularies</Link>
                        <Link to="/exercises">Exercises</Link>
                        <Link to="/statistics">Statistics</Link>
                        <UserButton/>
                    </SignedIn>
                </nav>
            </div>
        </header>
        <main className="app-main">
            <SignedOut>
                <Navigate to="/sign-in" replace/>
            </SignedOut>
            <SignedIn>
                <Outlet />
            </SignedIn>
        </main>
    </div>
}