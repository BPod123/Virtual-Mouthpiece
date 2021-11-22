import "./App.css";
import ImageUploader from "./components/ImageUploader";
import React, { useState, Image } from "react";

const fileTypes = ["JPG", "PNG", "GIF", "JPEG"];

function App() {

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
        </div>
        <div class="item">
          <ImageUploader />
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
          <button style={redButton}>
            Send to Billboard
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;
