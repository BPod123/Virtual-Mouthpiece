import React, { useState, useRef } from "react";
import ImagePreviewer from "./ImagePreviewer";
import SendButton from "./SendButton";

export default function ImageUploader(props) {
  const boardList = props.boards;

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
  }

  function deleteMethod(deleteBool, data) {
    if (deleteBool) {
      if (fileList.length === 1) {
        setFileList([]);
      }
      const deleteIndex = fileList.indexOf(data);
      if (deleteIndex !== -1) {
        setFileList(fileList.slice(0,deleteIndex).concat(fileList.slice(deleteIndex+1)));
      }
    }
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
          {fileList.map((data) => {
            return (
              <ImagePreviewer
                data={data}
                url={data.url}
                image={data.image}
                showTime={true}
                onRuntimeChange={handleRuntimeChange}
                deleteMethod={deleteMethod}
              />
            );
          })}
        </div>
      )}
      <br />
      <div className="checkboxes">
        <div className="top"></div>

        {Object.keys(boardList).map(function generateCheckboxes(e, i) {
          return (
            <label className="container" key={i}>
              {boardList[e]}
              <input
                type="checkbox"
                onChange={handleChange}
                value={boardList[e]}
              ></input>
              <span className="checkmark"></span>
            </label>
          );
        })}
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
