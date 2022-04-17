import React from "react";
import toast from "react-hot-toast";

export default function SendButton(props) {
  const { image, checks, imageList, slideshowTitle, runtimes } = props;
  return (
    <button
      className="sendButton"
      onClick={() => {
        const fd = new FormData();

        if (imageList.length === 0) {
          fd.append("images", image);
          fd.append("runtimes", 5);
        } else {
          for (const img of imageList) {
            fd.append("images", img.image);
            fd.append("runtimes", runtimes.has(img.url) ? runtimes.get(img.url) : 5);
          }
        }

        for (const runtime of runtimes) {
          console.log(runtime);
        }

        for (const check of checks['billboard']){
            fd.append("boards", check)
        }
        
        slideshowTitle && fd.append("title", slideshowTitle);

        if (imageList.length === 0 && image == null) {
            toast.error("You need to upload at least one image!");
            return;
        }

        toast.promise(
          //   fetch("/flask/upload", {
          fetch("http://127.0.0.1:5000/flask/upload", {
            method: "POST",
            body: fd,
          }),
          {
            loading: "Sending...",
            success: <b>Sent!</b>,
            error: <b>ERROR! Could not send.</b>,
          }
        );
      }}
    >
      Send to Billboard
    </button>
  );
}