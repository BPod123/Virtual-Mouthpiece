import React, { useState, useRef } from "react";

const ImageUploader = () => {
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
    <div className="wrapper">
      <div
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
      {previewUrl && (
        <div className="image">
          <img src={previewUrl} alt="image" />
          <span> {image.name} </span>
        </div>
      )}
    </div>
  );
};
export default ImageUploader;
