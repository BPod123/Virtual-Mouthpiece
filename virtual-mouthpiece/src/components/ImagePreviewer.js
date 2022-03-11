import React from "react";

export default function ImagePreviewer(props) {

    const {url, image, showTime} = props
    if (image && showTime) {
        return (
            <div class="imagePreviewer">
                <span className="preview">
                    <img src={url} alt="image" />
                    <p className="previewText">{image.name}</p>
                </span>
                <input type="text" className="timeBox" placeholder="Time (seconds)"></input>
            </div>
        );
    }
    else if (image) {
        return (
            <div class="imagePreviewer">
                <span className="preview">
                    <img src={url} alt="image" />
                    <p className="previewText">{image.name}</p>
                </span>
            </div>
        );
    }
    else {
        return <span>Nothing here yet</span>;
    }

}
