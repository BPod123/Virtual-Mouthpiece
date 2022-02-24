import React, { useState, useRef } from "react";
import Checkboxes from "./Checkboxes";

export default function ImageUploader() {

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

  return (
    <div className="fullComponent">
      <div
        className="dropZone"
        onDragOver={handleOnDragOver}
        onDrop={handleOnDrop}
        onClick={() => fileInput.current.click()}
      >
        <div className="dragText">Drag and drop image here</div>
        <input
          type="file"
          accept="image/*"
          ref={fileInput}
          hidden
          onChange={(e) => handleFile(e.target.files[0])}
        />
      </div>
      <h2>Files Uploaded:</h2>
      <div className="item">
        {previewUrl && (
          <div className="image">
            <img src={previewUrl} alt="image"/>
            <div>{image.name}</div>
          </div>
        )}
      </div>
      <Checkboxes />
      <button
        className="sendButton"
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
  );
  
}
