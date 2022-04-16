import "./App.css";
import ImageUploader from "./components/ImageUploader";
import Navbar from "./components/Navbar";
import {Toaster} from "react-hot-toast";
import React, {useEffect, useState} from "react";

function App() {

    const [validBoards, setValidBoards] = useState({});

    useEffect(() => {
        fetch("http://127.0.0.1:5000/flask/upload").then(response => response.json())
            .then(data => {
                setValidBoards(JSON.parse(data));
            })
    }, []);
    return (
        validBoards && <div>
            <div>
                <Toaster/>
            </div>
            <Navbar/>
            <div className="topMargin"></div>
            <ImageUploader boards={validBoards}/>
        </div>

    );
}

export default App;
