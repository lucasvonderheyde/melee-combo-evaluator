import { NavLink } from "react-router-dom";
import "./NavBar.css";

export default function Navbar() {
    return (
        <nav>
            <ul>
                <li><NavLink exact to="/" activeClassName="active">Home</NavLink></li>
                <li><NavLink to="/evaluator" activeClassName="active">Evaluator</NavLink></li>
                <li><NavLink to="/login" activeClassName="active">Login</NavLink></li>
            </ul>
        </nav>
    );
}