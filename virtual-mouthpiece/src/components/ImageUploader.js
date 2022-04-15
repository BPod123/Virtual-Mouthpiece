import React, { useState, useRef } from "react";
import ImagePreviewer from "./ImagePreviewer";
import SendButton from "./SendButton";

export default function ImageUploader() {
  const fileInput = useRef(null);
  const [image, setImage] = useState(null);
  const [previewUrl, setPreviewUrl] = useState("");

  const [fileList, setFileList] = useState([]);
  const [firstTime, setFirstTime] = useState(true);

  const [checkboxes, setCheckBoxes] = useState({ billboard: [], response: [] });

  const [slideshowTitle, setSlideshowTitle] = useState("");

  const [runtimes, setRuntimes] = useState(new Map());

  function handleSlideshowTitle(title) {
    setSlideshowTitle(title);
  }

  function handleFile(file) {
    setImage(file);
    const url = URL.createObjectURL(file);
    setPreviewUrl(url);
  }

  function handleOnDragOver(event) {
    event.preventDefault();
  }

  function handleOnDrop(event) {
    event.preventDefault();
    event.stopPropagation();
    let imageFile = event.dataTransfer.files[0];
    handleFile(imageFile);
  }

  function onSlideshowClick() {
    // console.log("clicked");
    if (firstTime && image) {
      setFileList([{ url: previewUrl, image: image }]);
      setFirstTime(false);
    } else if (image) {
      setFileList(fileList.concat([{ url: previewUrl, image: image }]));
    }
    setImage(null);
  }

  function handleRuntimeChange(index, runtime) {
    setRuntimes(new Map(runtimes.set(index, runtime)));
    // console.log(runtimes);
  }

  const handleChange = (e) => {
    // Destructuring
    const { value, checked } = e.target;
    const { billboard } = checkboxes;

    // console.log(`${value} is ${checked}`);
    if (checked) {
      setCheckBoxes({
        billboard: [...billboard, value],
        response: [...billboard, value],
      });
    }

    // Case 2  : The user unchecks the box
    else {
      setCheckBoxes({
        billboard: billboard.filter((e) => e !== value),
        response: billboard.filter((e) => e !== value),
      });
    }
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

      <h2>File Uploaded:</h2>
      <ImagePreviewer url={previewUrl} image={image} />

      {previewUrl && (
        <button
          className="slideshowButton"
          onClick={() => {
            onSlideshowClick();
          }}
        >
          Add To Slideshow
        </button>
      )}
      {fileList.length > 0 && (
        <div className="slideshowPreview">
          <input
            type="text"
            className="titleBox"
            placeholder="Slideshow Title"
            onChange={(e) => handleSlideshowTitle(e.target.value)}
          ></input>
          <br />
          {/* {console.log(slideshowTitle)} */}
          {fileList.map((data) => {
            return (
              <ImagePreviewer
                url={data.url}
                image={data.image}
                showTime={true}
                onRuntimeChange={handleRuntimeChange}
              />
            );
          })}
        </div>
      )}
      <br />
      <div className="checkboxes">
        <div className="top"></div>
        <label className="container">
          Front Board
          <input type="checkbox" onChange={handleChange} value="front"></input>
          <span className="checkmark"></span>
        </label>
        <label className="container">
          Airstrip Board
          <input
            type="checkbox"
            onChange={handleChange}
            value="airstrip"
          ></input>
          <span className="checkmark"></span>
        </label>
        <div className="bottom"></div>
      </div>
      <SendButton
        image={image}
        checks={checkboxes}
        imageList={fileList}
        slideshowTitle={slideshowTitle}
        runtimes={runtimes}
      />
    </div>
  );
}
