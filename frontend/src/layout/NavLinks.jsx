import { Link } from "react-router-dom";
import "../layout/layout.css";

export default function NavLinks() {
  return (
    <div className="header-right">
      <div className="nav-links">
        <Link to="/">Home</Link>
        <Link to="/quiz">Quiz</Link>
        <Link to="/vocabularies">Vocabularies</Link>
        <Link to="/exercises">Exercises</Link>
        <Link to="/scanner">Scanner</Link>
        {/* <Link to="/statistics">Statistics</Link> */}
      </div>
    </div>
  );
}
