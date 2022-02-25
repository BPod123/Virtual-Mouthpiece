import React, { useState, useRef } from "react";

export default function ImagePreviewer(props) {

    const {url, image} = props
    if (image && url) {
        return (
            <span className="preview">
                <img src={url} alt="image" />
                <p className="previewText">{image.name}</p>
            </span>
        );
    }
    else {
        return (<span></span>);
    }

}
