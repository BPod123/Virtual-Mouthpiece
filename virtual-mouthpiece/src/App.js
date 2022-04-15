import "./App.css";
import ImageUploader from "./components/ImageUploader";
import Navbar from "./components/Navbar";
import {Toaster} from "react-hot-toast";
import React, {useEffect, useState} from "react";

function App() {

    const [validBoards, setValidBoards] = useState([]);

    useEffect(() => {
        fetch("http://127.0.0.1:5000/flask/upload").then((data) => console.log("data response" + data))
    }, []);
    return (
        <div>
            <div>
                <Toaster/>
            </div>
            <Navbar/>
            <div className="topMargin"></div>
            <ImageUploader/>
        </div>
    );
}

export default App;
