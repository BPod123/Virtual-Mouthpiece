import React from "react";

export default function ImagePreviewer(props) {
  const { url, image, showTime, onRuntimeChange } = props;
  if (image && showTime) {
    return (
      <div className="imagePreviewer">
        <span className="preview">
          <img src={url} alt="uploaded" />
          <p className="previewText">{image.name}</p>
        </span>
        <input
          type="text"
          className="timeBox"
          placeholder="Time (seconds)"
        //   defaultValue={5}
          onChange={(e) => onRuntimeChange(url, e.target.value)}
        ></input>
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
