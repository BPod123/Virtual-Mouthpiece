import "./App.css";
import ImageUploader from "./components/ImageUploader";
import React, { useState, useRef } from "react";

const fileTypes = ["JPG", "PNG", "GIF", "JPEG"];

function App() {
  const fileInput = useRef(null);
  const [image, setImage] = useState(null);
  const [previewUrl, setPreviewUrl] = useState("");
  const handleFile = (file) => {
    setImage(file);
    setPreviewUrl(URL.createObjectURL(file));
  };
  const handleOnDragOver = (event) => {
    event.preventDefault();
  };
  const handleOnDrop = (event) => {
    event.preventDefault();
    event.stopPropagation();
    let imageFile = event.dataTransfer.files[0];
    handleFile(imageFile);
  };

  const blueButton = {
    backgroundColor: "#003057",
    border: "none",
    color: "white",
    padding: "10px",
    margin: "5px",
    textAlign: "center",
    display: "inline-block",
  };
  const redButton = {
    outerWidth: "100%",
    backgroundColor: "#ee4c50",
    border: "none",
    color: "white",
    padding: "10px",
    margin: "5px",
    textAlign: "center",
    display: "inline-block",
  };

  return (
    <div className="App">
      <div className="container">
        <div class="item">
          <button style={redButton}>Create Slideshow</button>
          <h3>Files Uploaded:</h3>
        </div>
        <div class="item">
          <h1>Virtual Mouthpiece</h1>
          <h3>Billboard Updater</h3>
        </div>
        <div class="item">
          <button style={blueButton}>⚙</button>
        </div>
        <div class="item">
          {previewUrl && (
            <div className="image">
              <img src={previewUrl} alt="image"  style={{width:"50px", height:"auto"}}/>
              <span> {image.name} </span>
            </div>
          )}
        </div>
        <div class="item">
          <div className="wrapper" >
            <div style={{ border: "1px solid black", padding: "5px" }}
              className="drop_zone"
              onDragOver={handleOnDragOver}
              onDrop={handleOnDrop}
              onClick={() => fileInput.current.click()}
            >
              <p>Drag and drop image here....</p>
              <input
                type="file"
                accept="image/*"
                ref={fileInput}
                hidden
                onChange={(e) => handleFile(e.target.files[0])}
              />
            </div>
          </div>
        </div>
        <div class="item"></div>
        <div class="item"></div>
        <div class="item">
          <input
            type="checkbox"
            id="front-board"
            name="front-board"
            value="Front Board"
          ></input>
          <label for="front-board">Front Board</label>
          <input
            type="checkbox"
            id="airstrip-board"
            name="airstrip-board"
            value="Airstrip Board"
          ></input>
          <label for="airstrip-board">Airstrip Board</label>
        </div>
        <div class="item"></div>
        <div class="item"></div>
        <div class="item"></div>
        <div class="item">
          <button
            style={redButton}
            onClick={() => {
              const fd = new FormData();
              image && console.log(image.name)
              image && fd.append('file', image)
              fetch('/flask/hello', {
                method: 'POST',
                body: fd
              }).then(resp => {
                resp.json().then(data => {console.log(data)})
              })
            }}
          >
            Send to Billboard
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;
