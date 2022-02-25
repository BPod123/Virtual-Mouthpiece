import React, { useState, useRef } from "react";
import Checkboxes from "./Checkboxes";
import ImagePreviewer from "./ImagePreviewer";
import SendButton from "./SendButton";


export default function ImageUploader() {
  const fileInput = useRef(null);
  const [image, setImage] = useState(null);
  const [previewUrl, setPreviewUrl] = useState("");

  const [fileList, setFileList] = useState([]);
  const [firstTime, setFirstTime] = useState(true);

  function handleFile(file) {
    setImage(file);
    /*bug where program crashes here if canceling image select after selecting image already*/
    /*also weird behavior when user selects the same image consecutively*/
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
    console.log("clicked");
    if (firstTime) {
      setFileList([
        {url:previewUrl, image:image}]);
      setFirstTime(false);
    }
    else {
      setFileList(fileList.concat([
        {url:previewUrl, image:image}]));
    }
  }
  console.log("hi");
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
      <Checkboxes />
      <SendButton image={image}/>
      
      {previewUrl &&
        (<button 
          className="slideshowButton"
          onClick={()=>{onSlideshowClick();}}>
            Add To Slideshow
        </button>)
      }
      {fileList.length > 0 &&
        <div className="slideshowPreview">
          {
            fileList.map(
              data => {return (<ImagePreviewer url={data.url} image={data.image}/>);}
            )
          }
        </div>
    }
    </div>
  );
}
