import React from "react";

export default function ImagePreviewer(props) {
  const { data, url, image, showTime, onRuntimeChange, deleteMethod } = props;
  if (image && showTime) {
    return (
      <div className="imagePreviewer">
        <span className="preview">
          <img src={url} alt="uploaded" />
          <p className="previewText">{image.name}</p>
        </span>
        <span className="timeDeleteSpan">
        <input
          type="text"
          className="timeBox"
          placeholder="Time (seconds)"
        //   defaultValue={5}
          onChange={(e) => onRuntimeChange(url, e.target.value)}
        ></input>
        <button
          className="deleteButton"
          onClick={() => deleteMethod(true,data)}>
            Delete
        </button>
        </span>
      </div>
    );
  } else if (image) {
    return (
      <div className="imagePreviewer">
        <span className="preview">
          <img src={url} alt="uploaded" />
          <p className="previewText">{image.name}</p>
        </span>
      </div>
    );
  } else {
    return "";
  }
}
