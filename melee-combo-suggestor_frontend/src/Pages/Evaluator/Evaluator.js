import React, { useContext } from 'react';
import FileUpload from "../../components/FileUpload/FileUpload";
import LogoutButton from "../../components/LogoutButton/LogoutButton";
import NavBar from "../../components/NavBar/NavBar";
import { AuthContext } from '../../AuthContext';
import './Evaluator.css';

export default function Evaluator() {
    const { user } = useContext(AuthContext); 

    return (
        <div className="evaluator-container">
            <NavBar />
            <div className="content">
                <div className="file-upload-container">
                    <FileUpload />
                </div>
                {user && ( 
                    <div className="logout-button-container">
                        <LogoutButton />
                    </div>
                )}
            </div>
        </div>
    );
}
