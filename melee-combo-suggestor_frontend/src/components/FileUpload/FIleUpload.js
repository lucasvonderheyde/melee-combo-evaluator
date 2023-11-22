import React, { useState } from 'react'
import ComboVisuals from '../ComboVisuals/ComboVisuals';


const FileUpload = () => {
    const [file, setFile] = useState(null);
    const [combos, setCombos] = useState(null);

    const handleFileChange = (event) => {
        setFile(event.target.files[0]);
    };

    const handleFileUpload = async () => {
        if (file) {
            const formData = new FormData();
            formData.append('slpFile', file);

            try {
                const response = await fetch('http://127.0.0.1:5555/players-uploads', {
                    method: 'POST',
                    body: formData,
                });
                if(response.ok) {
                    const data = await response.json();
                    setCombos(data);
                } else {
                    console.error('Error in response:', await response.text());
                }
            } catch (error) {
                console.error('Error uploading file:', error);
            }
        }
    };

    return (
        <div>
            <input type="file" onChange={handleFileChange} />
            <button onClick={handleFileUpload}>Upload</button>
            {combos && <ComboVisuals combos={combos} />}
        </div>
    );
}

export default FileUpload;