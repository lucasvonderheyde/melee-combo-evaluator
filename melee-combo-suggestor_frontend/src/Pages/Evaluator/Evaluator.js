import FileUpload from "../../components/FileUpload/FIleUpload"
import LogoutButton from "../../components/LogoutButton/LogoutButton"
import NavBar from "../../components/NavBar/NavBar"
import './Evaluator.css'

export default function Evaluator() {
    return (
        <div>
            <NavBar />
            <FileUpload />
            <LogoutButton />
        </div>
    )
}