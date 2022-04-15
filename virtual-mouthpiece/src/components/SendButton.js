import React from "react";
import toast from "react-hot-toast";

export default function SendButton(props) {
  const { image, checks, imageList, slideshowTitle, runtimes } = props;
  return (
    <button
      className="sendButton"
      onClick={() => {
        // console.log("billboard clicked");
        const fd = new FormData();
        let imageUrlList = [];
        for (const img of imageList) {
            imageUrlList.push({url:img.url, runtime:runtimes.has(img.url) ? runtimes.get(img.url) : "5"});
        }

        imageList.length !== 0 && fd.append("files", imageUrlList);
        image && fd.append("file", image);
        checks && fd.append("board", checks['billboard']);
        slideshowTitle && fd.append("title", slideshowTitle);
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
