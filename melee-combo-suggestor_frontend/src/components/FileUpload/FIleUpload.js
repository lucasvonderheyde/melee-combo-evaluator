import React, { useState, useContext } from 'react';
import { AuthContext } from '../../AuthContext';
import './FileUpload.css';

const FileUpload = ({ onUploadComplete }) => {
    const [file, setFile] = useState(null);
    const { user } = useContext(AuthContext);

    const handleFileChange = (event) => {
        setFile(event.target.files[0]);
    };

    const handleFileUpload = async () => {
        if (file) {
            const formData = new FormData();
            formData.append('slpFile', file);
            
            // Add user ID to form data if a user is logged in
            if (user && user.id) {
                formData.append('userId', user.id);
            }

            try {
                const response = await fetch('http://127.0.0.1:5555/players-uploads', {
                    method: 'POST',
                    body: formData,
                    credentials: 'include'
                });
                if (response.ok) {
                    const data = await response.json();
                    onUploadComplete(data);
                } else {
                    console.error('Error in response:', await response.text());
                }
            } catch (error) {
                console.error('Error uploading file:', error);
            }
        }
    };

    return (
        <div className="file-upload-container">
            <input type="file" onChange={handleFileChange} className="file-input" />
            <button onClick={handleFileUpload} className="upload-button">Upload</button>
        </div>
    );
};

export default FileUpload;
