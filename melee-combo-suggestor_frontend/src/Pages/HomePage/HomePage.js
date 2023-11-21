import FileUpload from "../../components/FileUpload/FIleUpload"
import "./HomePage.css"

export default function HomePage() {
    return (
        <div>
            <h1 id="title" >Melee Combo Suggestor</h1>
            <FileUpload />
        </div>
    )
}