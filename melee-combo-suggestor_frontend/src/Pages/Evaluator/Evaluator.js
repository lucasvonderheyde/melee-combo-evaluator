import React from 'react';
import FileUpload from "../../components/FileUpload/FileUpload";
import LogoutButton from "../../components/LogoutButton/LogoutButton";
import NavBar from "../../components/NavBar/NavBar";
import './Evaluator.css';

export default function Evaluator() {
    return (
        <div className="evaluator-container">
            <NavBar />
            <div className="content">
                <div className="file-upload-container">
                    <FileUpload />
                </div>
                <div className="logout-button-container">
                    <LogoutButton />
                </div>
            </div>
        </div>
    );
}
